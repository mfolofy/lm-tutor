# DevOps / Infrastructure Review — lm-tutor (The School for LLMs)

**Reviewer:** Mike (Claude Code / claude-sonnet-4-6)
**Date:** 2026-06-08
**Target:** `SCOPE.md`
**Focus:** Operational reality — deployability, runtime, dependencies, monitoring, infrastructure gaps

---

## 0. What This Review Covers

The SCOPE is a design document, not an implementation. That's fine for Ground Zero. But the SCOPE makes specific operational claims ("separate process," "no PyPI," "MCP is a 50-line wrapper," "zero runtime dependency on Ghost Stack") that have concrete implications for how this system actually runs. This review checks those claims against reality.

---

## 1. Deployability — The `git clone && pip install -e . && school eval` Test

### 1.1 It Works on Paper. It Breaks in Practice.

The SCOPE promises a zero-friction developer experience: clone, pip install, run. Three real problems:

**1.1.1 Monorepo dual-homing is not documented.**

> Location: `projects/school-for-llms/` (monorepo) + `github.com/mfolofy/school-for-llms` (standalone, dual-homed)

The mono-repo path is `projects/school-for-llms/` — but `pip install -e .` needs a `pyproject.toml` at the root of the install target. Inside a monorepo, the typical pattern is `pip install -e projects/school-for-llms/` (from repo root) or an `editable`-aware build backend. If the SCOPE's README says `cd projects/school-for-llms && pip install -e .` this works. If it says `git clone ... && pip install -e .` without specifying which directory, the user runs `pip install -e .` from the repo root which either (a) fails if there's no root pyproject.toml, or (b) installs the entire monorepo as a package, which is not what you want.

The standalone repo path also needs to produce an identical package. Dual-homing means two CI configs, two release processes, two sets of git hooks. The SCOPE doesn't address how these stay in sync — which is the canonical source, how tags flow between them, whether releases are cut from the standalone repo and backported to monorepo or vice versa.

**1.1.2 `school eval` on stdin is underspecified.**

> `echo "<div>" | school eval` — works, no server, no config, no PyPI

What does this evaluate? `echo "<div>"` is an HTML fragment. The eval harness needs a syllabus to grade against — which class's rubric? If it infers from the content ("this looks like HTML, load the brushes rubric"), that's fragile. If it requires a `--class` flag, the one-liner breaks. If it defaults to some curriculum, what happens when there's no model identity context?

More critically: `echo "<div>"` pipes raw bytes on stdin. The eval harness is supposed to be a "separate process" — does stdin mean I pipe to a subprocess CLI, or does the SDK do it internally? If it's CLI-to-CLI (`echo ... | school eval`), that works. If `school eval` is an SDK call that spawns a subprocess internally, stdin has no meaning. The SCOPE needs to distinguish between these two modes and make sure the one-liner actually does what it advertises.

**1.1.3 The "no server" claim conflicts with the MCP architecture.**

The SCOPE says "no server, no config" for the eval use case. Then it defines `school mcp` as the primary integration point for agents. These are the same codebase, same Python process. If `school mcp` runs an MCP server (a long-lived process on stdio or SSE), then the package has a server component. The claim "no server" only holds for the CLI subcommands that don't use MCP. This is confusing and will cause users to wonder why `pip install` pulls in `uvicorn` and `starlette` (transitive from `mcp`) if there's "no server."

### 1.2 What's Missing for Production Deployability

- **A `requirements.txt` or pinned lock file.** `pip install -e .` installs the latest compatible versions of all dependencies. Six months from now, a new `mcp` release could break the School. A lock file (or at minimum an upper-bound pin in the dependencies) is needed for reproducible installs.
- **Dockerfile.** The SCOPE lists Docker as a distribution method but provides no details. A multistage Docker build for the MCP server is table stakes.
- **Environment variable reference.** The MCP server needs external env vars. What env vars does the School need? `SCHOOL_REGISTRY_PATH`? `SCHOOL_CLASSES_DIR`? Not defined.
- **CI/CD.** Zero mention of CI. No test runner config (pytest? unittest?). No linting. No type checking. For a project that claims reproducibility (baseline benchmarks), the absence of CI means every benchmark run is done by hand.

---

## 2. The Eval Harness — "Separate Process, No Shared State"

### 2.1 Process Spawning Is Expensive Here

The eval harness is described as:

> Independent Eval Harness (separate process, no shared state) -> { verified: true/false }

Every `eval_verify(submission_id)` call spawns a new Python process. That's `subprocess.Popen(["python", "-m", "school.eval", "--submission", id])` or similar. Each spawn:

- Loads Python interpreter (~30-50ms cold start on modern hardware, worse on constrained VPS)
- Imports the entire `school` package — including all class modules, the registry, the grading board
- Loads the curriculum YAML for the relevant syllabus
- Runs grading logic
- Exits

For a single eval, this overhead doesn't matter. For the SCOPE's stated use case — "multi-model, multi-task benchmark" with 4 models x 5 tasks x 3 runs = 60 evaluations — that's 60 full Python process startups. On a machine like Smith VPS (2 vCPU, ~4GB RAM, Docker container), this could add 3-5 seconds per eval just in startup overhead, turning a 5-minute benchmark into a 10-minute one.

**Alternative that preserves the "no shared state" design:** Use a persistent worker pool. `multiprocessing.Pool(processes=2)` keeps workers alive between evaluations. Each eval call sends a task to the pool and gets back a result. The workers are still isolated (separate processes, no shared Python state) but avoid the cold-start tax. The SCOPE doesn't consider this — it says "separate process" as if that means "spawn fresh every time."

### 2.2 The "Canonical Truth Source" Claim Has No Verification Mechanism

The eval harness is supposed to be the canonical truth source — even the School's own Grading Board defers to it. But who verifies the verifier?

If the eval harness itself has a bug (wrong rubric loaded, off-by-one in scoring, circular import that silently skips checks), every evaluation downstream is wrong. The "canonical truth" claim depends on the eval harness being correct, but there's no mechanism in the SCOPE for validating the validator — no known-good test suite, no golden outputs checked by hand, no cross-validation against another measurement tool.

This is especially risky because the School claims it will measure its own success (15-20% reduction in violations). If the measuring tool is part of the project, the measurement is not independent. This is not a devops problem per se, but it has a devops implication: the eval harness needs its own CI pipeline with golden test cases that must pass before a release ships.

### 2.3 Syllabus Loading — Which Class, Which Lesson, Which Exercise?

> eval_verify(submission_id) — Independent verification (separate process, canonical truth)

`eval_verify` receives a `submission_id`. To grade it, the harness must load the correct syllabus. How does it know which one?

Options:
1. The submission_id encodes the class/lesson reference (e.g., `brushes-lesson3-exercise1-abc123`)
2. The harness queries some shared state (a database? a file?) to look up the submission's context
3. The calling process passes syllabus context alongside the submission_id

Option 1 is the cleanest but requires submission IDs to be structured. Option 2 creates shared state — exactly what the "no shared state" rule forbids. Option 3 pushes the responsibility to the caller, which means the caller can lie about which syllabus to use.

The SCOPE doesn't specify which approach. This is not an academic question — it determines whether the eval harness can be truly stateless or whether it needs a database of submission metadata.

---

## 3. Model Registry — `models.json` Curated by Hand

### 3.1 The Update Problem Is Worse Than Admitted

> Model ratings are public everywhere — leaderboards, pricing pages, API docs. The registry is the source of truth. Contribute updates when new models drop.

"Contribute updates" means someone opens `registry/models.json`, edits it, commits, and pushes. For a project with the stated distribution model (no PyPI, git clone is the install method), registry updates are deployed by `git pull`. Every user must pull to get the latest model data.

Consider the timeline for a new model release:

- **Day 0:** Model X drops. Pricing page updated. Leaderboard updated. API docs updated.
- **Day 0-7:** Someone needs to (a) notice Model X exists, (b) read its benchmarks, (c) determine its tier and track, (d) write a registry entry, (e) commit, (f) PR review if any, (g) merge, (h) tag a release.
- **Day 7+:** Users who `git pull` get the update. Users who installed from a release wheel are stuck with the old registry until the next release.

**For a project whose entire track assignment depends on the registry being current, a 7-day update latency is a week of wrong track assignments.** A user who runs `school enroll` with a model released 8 days ago gets either "unknown model" or a wrong default track. This is a fundamental design problem — the system's core function (track placement) depends on data that is guaranteed to be stale between releases.

### 3.2 What Happens With Unregistered Models?

The SCOPE shows `school enroll` doing a lookup in `models.json`. What happens when a model says "I'm claude-4-haiku" and there's no entry?

Options:
1. Fail: "Unknown model, cannot enroll" — bad UX, the model learns nothing
2. Default to "remedial" track — safe but penalizes capable models
3. Default to "standard" — optimistic but may overtax small models
4. Prompt for manual track selection — requires interactive input, which breaks in CI

Option 2 is the safest default for an education project, but the SCOPE doesn't state it. Without a defined fallback, `school enroll` has undefined behavior for every model that isn't in the registry. In a world where new models launch monthly, "unregistered" will be a common case.

### 3.3 The Diagnostic Option Undermines the Registry Model

> No diagnostic required. Model ratings are public everywhere.
> Optional `school assess --diagnostic` runs the eval harness for anyone who wants a second opinion.

If the diagnostic produces different results from the registry (e.g., the registry says "standard" but the diagnostic reveals the model performs at "remedial" level), which wins? The SCOPE says the registry is the source of truth, but the diagnostic exists and might disagree. This creates an ambiguity: is the diagnostic informational only, or can it override track placement? If it can override, the registry is not the source of truth. If it cannot override, why offer it?

---

## 4. Dependencies — The "Zero Runtime Dependency on Ghost Stack" Claim

### 4.1 The Claim and Its Limits

> Zero runtime dependency between School and any Ghost Stack project. Knowledge only, no code imports.

This is true at the School-to-Ghost-Stack boundary. But the School has its own dependency tree that needs maintenance:

- `mcp` (and its 14 transitive dependencies: anyio, httpx, httpx-sse, jsonschema, pydantic, pydantic-settings, pyjwt, python-multipart, pywin32, sse-starlette, starlette, typing-extensions, typing-inspection, uvicorn)
- `pydantic` (3 more: annotated-types, pydantic-core, typing-extensions, typing-inspection)
- `pyyaml`

Total: ~18 transitive dependencies for a "50-line MCP wrapper." The MCP SDK is not lightweight. Every dependency is a maintenance burden, a potential security advisory, and a version conflict risk.

### 4.2 Class-Specific Dependencies Will Conflict

The SCOPE defines 9 class modules, each in its own directory. The dependency list in `pyproject.toml` only covers the framework (mcp, pydantic, pyyaml). But the classes will need their own dependencies:

- `brushes` — may need pillow (image generation), beautifulsoup4 (HTML parsing), cssutils
- `security` — different tooling entirely
- `test` — needs a test runner or test-output parser
- `perf` — may need lighthouse CLI, or requests for latency checks, or psutil

The SCOPE says each class has exercises with "automated grading." Those graders will need libraries. If class A needs `pillow==10.4` and class B needs `numpy==1.26` and class C needs `lxml` and they all live in the same Python environment, version conflicts are inevitable.

**What the SCOPE ignores:** The install footprint is not fixed at `git clone && pip install -e .`. It expands with every class added. After 9 classes, the dependency tree may span 50+ packages. The "lightweight" claim is only true at Phase 0 — it degrades linearly with class count.

### 4.3 Python Version Constraint

> requires-python = ">=3.11"

3.11 is already 2 years old. By the time this project ships Phase 1, 3.13+ will be standard. The constraint excludes Python 3.13 systems (some Docker images ship 3.13 as default). This is fine for now but will need active management.

---

## 5. The 8B Booster — What Does "Sandbox" Actually Mean?

### 5.1 `write_to_scratchpad` Is Not a Sandbox

> | `write_to_scratchpad` | Solve logic in sandbox *before* generating code |

The SCOPE calls this a "sandbox" but provides zero architectural detail. Let me enumerate what "sandbox" could mean and the problems with each:

| Interpretation | Reality | Problems |
|---|---|---|
| **Subprocess** | `subprocess.run(["python", "-c", prompt])` | No isolation from the host — can read/write any file, access network, import any module. A malicious or buggy model could `os.system("rm -rf /")`. Also misses the point: the model doesn't write the code, the sandbox has to solve the problem the model was asked to solve without the model. |
| **Container** | Spawns a Docker container per write | ~500ms-2s startup per invocation. The Booster is supposed to be used "on every class" for remedial models — that's potentially dozens of container spawns per `school learn` session. Resource usage is enormous. Also requires Docker to be installed, which conflicts with "no server, no config." |
| **Temporary directory** | `tempfile.mkdtemp()`, writes a file, reads it back | This is just a file, not a sandbox. No process isolation, no memory limits, no network restrictions. The only "sandbox" property is that the directory is cleaned up. |

The SCOPE needs to define what threat the sandbox mitigates. If the concern is "the model generates code that executes and damages the host," then only containerization or a restricted subprocess (`subprocess.Popen` with `subprocess.PIPE` and a timeout) is adequate. If the concern is just "let the model reason before generating," the sandbox is unnecessary — just use a two-turn prompt pattern (first write reasoning, then generate code).

### 5.2 Memory Limits, Timeouts, Cleanup

None of the Booster tools have operational guardrails:

- What happens when `write_to_scratchpad` takes 60 seconds? Does the caller hang? Is there a timeout?
- What happens when the sandbox writes 2GB of data to disk? Is there a disk quota?
- Who cleans up sandbox artifacts? `tempdir` helps for files, but what about spawned processes that don't terminate?
- What happens when `self_consistency_check` or `inject_few_shot` is called with arguments that trigger an OOM in the evaluation process?

For a tool designed to be used by small, unreliable models, the absence of timeouts, resource limits, and cleanup guarantees means every Booster invocation is a potential DoS vector against the host.

### 5.3 Concurrent Usage

If the School is running as an MCP server (`school mcp`), multiple agents might hit Booster tools simultaneously. Are Booster calls serialized? Can two calls spawn overlapping sandbox processes? Is there a global lock? The SCOPE doesn't specify, but concurrent sandbox usage without coordination is a recipe for resource exhaustion and data corruption (two processes writing to the same temp directory).

---

## 6. The "No PyPI" Constraint — Wheels on GitHub Releases

### 6.1 The Claim and Its Motivation

> No PyPI — unreliable
> Pre-built `.whl` on GitHub Releases. Docker. No PyPI.

The SCOPE says PyPI is "unreliable." This needs unpacking. If the concern is "PyPI goes down and we can't install," that hasn't been a meaningful risk since CDN-based distribution (Fastly, CloudFront) was adopted years ago. If the concern is "supply chain attacks on PyPI compromise our users," that's valid but distributing wheels via GitHub Releases on an open-source repo has exactly the same attack surface — a compromised CI pipeline or a malformed release artifact affects all users.

**The real operational cost of "no PyPI":**

- Users who install from the monorepo path need `pip install -e .`, which pulls dependencies from PyPI anyway. The School itself may not be on PyPI, but every dependency (`mcp`, `pydantic`, `pyyaml`) is. You cannot avoid PyPI without vendoring every transitive dependency, which the SCOPE does not propose.
- GitHub Releases has no `pip install school` command. Users must know to find the release, download the `.whl`, and run `pip install path/to/school.whl`. That's a worse UX than `pip install school-for-llms`.
- The standalone repo is the "canonical" release distribution, but the monorepo is where development happens. Every release is a manual or CI-driven copy from one repo to the other. Two repos means two places where the release can break, two sets of tags to manage, two READMEs to update.

### 6.2 `pip install -e .` for Development vs Wheels for Distribution

The SCOPE promises `pip install -e .` for development (editable install) and `.whl` files for distribution. These are not the same thing:

- `pip install -e .` creates an editable install that imports directly from the source tree. This is fine for development but slower for import.
- `.whl` files are built artifacts. They require a build step (`python -m build`) and produce a self-contained archive.

This means the CI pipeline needs to:
1. Run tests from editable install
2. Build `.whl`
3. Test the `.whl` in a clean environment
4. Tag the release
5. Upload the `.whl` to GitHub Releases

The SCOPE doesn't define any of this. "No PyPI" is presented as a one-line decision, but it commits the project to a custom release pipeline with all the associated maintenance.

### 6.3 What About Transitive Dependencies in the Wheel?

A `.whl` file typically declares dependencies in its metadata (`Requires-Dist`). When a user runs `pip install school.whl`, pip resolves and installs all declared dependencies from PyPI. This means even with "no PyPI" for the School itself, pip still hits PyPI for `mcp`, `pydantic`, and their 18 transitive deps. The "no PyPI" constraint only avoids one package name on PyPI — it doesn't reduce dependency risk.

If the intent is truly zero PyPI access (air-gapped install), then ALL dependencies must be vendored or bundled into a single fat wheel. A fat wheel (`--universal` with all deps zipped inside) is possible but non-standard, bloated (~50MB+ with `mcp`'s tree), and bypasses pip's version resolution, which means conflicts with other packages in the same environment are undetectable until runtime.

---

## 7. Monitoring — What Happens When `school mcp` Crashes?

### 7.1 The MCP Server Has No Observability

The SCOPE defines `school mcp` as a "50-line wrapper around the SDK." A production MCP server needs at minimum:

- **stdout/stderr logging** — the MCP protocol runs on stdio by default. If the MCP server logs to stdout, it corrupts the protocol frames. The server must log to a file or stderr (which many MCP hosts forward).
- **Structured logging** — JSON-formatted log lines with request IDs, timestamps, and severity levels. Without this, debugging a failed `evaluate_submission` call requires reading raw exception tracebacks.
- **Crash recovery** — the MCP server runs as a child process of whatever host launched it (Claude Desktop, a custom agent, an MCP gateway). If it crashes mid-class (unhandled exception, OOM, disk full), the host sees a broken pipe. What happens? Does the agent retry? Does it lose the student's progress? Is there checkpoint state?
- **Health check endpoint** — the server has no defined `/health` or MCP tool that returns process health, uptime, memory usage, or recent error counts. Without this, any orchestrator (Kubernetes, Docker, supervisor) cannot distinguish a healthy server from one that's silently failing.

### 7.2 State Loss on Crash Is Not Acknowledged

`school learn` walks through lessons, exercises, and pass/fail gates. If the MCP server crashes in the middle of a lesson:

- The student model loses its session context
- Any partial exercise state is lost (unless the SDK persists it externally)
- The model must re-enroll and restart from the last checkpoint (if checkpoints exist) or from the beginning

The SCOPE mentions a "track state" module in the Registrar but provides no detail on its durability. Is state kept in memory? SQLite? A file? How often is it checkpointed? What's the recovery procedure?

### 7.3 No Metrics Means No Operations Feedback

- How many models are enrolled? Active?
- What's the pass/fail rate per class?
- Which classes take longest to evaluate?
- Which Booster tools are called most often?
- Are there evaluation errors (harness bugs) or student errors (model failures)?

None of these questions can be answered from what's specified. The SCOPE says "Baseline published in README" — but a baseline is a one-time measurement, not a monitoring system. For a project that intends to measure quality improvement over time, the absence of persistent metrics is a design gap.

### 7.4 The "Deferred" Monitoring

The Protocol Engine (Phase 4) is "deferred, gated." But monitoring isn't a Phase 4 feature — it's a Phase 0 requirement. Without logs and metrics, you cannot:

- Debug why a model's track placement is wrong
- Identify which class is producing evaluation errors
- Measure the Booster's actual impact
- Verify the eval harness isn't silently broken

Monitoring is the scaffolding that makes every other Phase's output interpretable. Putting it after classes (Phase 1) and the Grading Board (Phase 2) is building a house without electrical wiring.

---

## 8. Other Operational Gaps

### 8.1 The Benchmarks Are Not Reproducible

> Baseline benchmark: 4 models x 5 tasks x 3 runs. Published in README.

A benchmark is reproducible if:
1. The exact model versions are pinned (not just "DeepSeek V4 Flash" but the specific API endpoint or checkpoint)
2. The system state (temperature, top_p, max_tokens, system prompt) is documented
3. The hardware and Python version are recorded
4. The seed values are fixed
5. The extraction date is noted

The SCOPE doesn't mention any of this. An unreproducible benchmark is not a benchmark — it's an anecdote with numbers.

### 8.2 No Update Strategy for Classes

Classes are static directories under version control. When a source standard evolves (e.g., WCAG adds a new success criterion):

The SCOPE says classes should stay in sync with source standards. This is good for code consistency but doesn't address the operational fall-out: benchmarks need rerunning, pass/fail history may change retroactively, and models that passed on the old rubric may now fail.

### 8.3 The `school mcp` Port and Protocol

MCP servers run on stdio (when launched by an MCP host) or SSE/streamable HTTP (when standalone). The SCOPE doesn't specify which mode `school mcp` uses. If it's stdio-only, it cannot be deployed as a standalone service behind Traefik. If it's SSE, it needs a port assignment, which needs to be collision-free in the existing Ghost Stack network (Mako has services on :8000, :8002, :3000, :5678, :6333, etc.).

---

## Summary — DevOps Gaps by Severity

| Severity | Gap | Impact |
|----------|-----|--------|
| **HIGH** | Eval harness process-spawning overhead for every evaluation | Baseline benchmarks take 2-3x longer than expected; production usage has unacceptable latency |
| **HIGH** | Booster "sandbox" undefined — could be a subprocess with no isolation or a container with no cleanup | Security risk, resource exhaustion, data integrity issues |
| **HIGH** | No monitoring, logging, or metrics defined for the MCP server | Blind operation — cannot debug crashes, measure adoption, or verify the core thesis |
| **HIGH** | Model registry requires manual updates; stale between releases | Wrong track assignments for weeks after every new model launch |
| **MEDIUM** | No lock file or pinned dependencies | Random breakage from `pip install -e .` when transitive deps update |
| **MEDIUM** | Dual-homed repos with no sync strategy | Release drift between monorepo and standalone — users get different behavior depending on install method |
| **MEDIUM** | Class-specific dependencies unaddressed | Version conflicts as classes accumulate; dependency tree grows unbounded |
| **MEDIUM** | No CI/CD defined | Every benchmark is hand-run; every release is hand-crafted; no quality gating |
| **LOW** | "No PyPI" doesn't avoid PyPI for transitive deps | The constraint creates UX friction without delivering the claimed benefit |
| **LOW** | Python version constraint will need updating within the project's lifetime | Maintenance overhead |
| **LOW** | Port collision risk for `school mcp` SSE mode | Integration delay when deploying in existing Ghost Stack environment |

## Recommendation

Ship the eval harness as a persistent worker pool, not a spawn-per-call model. Define the Booster sandbox as a `tempfile.mkdtemp()` with a subprocess timeout and disk quota — document the actual isolation boundaries rather than calling it a "sandbox." Add structured logging (stdout-only for MCP protocol, file-based for diagnostics) before releasing any Phase 0 code. Pin model versions and seed values in the benchmark methodology. Defer dual-homing until Phase 1 — develop in the monorepo, figure out standalone extraction when there's demand.
