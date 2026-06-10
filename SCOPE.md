# lm-tutor — The School for LLMs

> **Tagline:** "The School for LLMs"
> **Project:** `lm-tutor`
> **Status:** SCOPE — ground zero
> **Date:** 2026-06-08

---

## Identity

| Field | Value |
|-------|-------|
| **Name** | `lm-tutor` |
| **What it is** | Structured AI education for any model. Everyone's welcome. Enrollment → curriculum track → classes → graduation. |
| **Location** | `projects/lm-tutor/` (monorepo) + `github.com/mfolofy/lm-tutor` (standalone, dual-homed) |
| **CLI** | `tutor enroll` — model says who it is, track assigned. `tutor learn` — take a class. `tutor eval` — grade output. `tutor assess --diagnostic` — optional baseline test. `tutor mcp` — launch MCP server. `tutor list` — list available classes. |
| **Distribution** | `git clone && pip install -e .`. Pre-built wheels on GitHub Releases. Docker image. The package is NOT on PyPI; transitive dependencies (mcp, pydantic, pyyaml) resolve from PyPI normally. Lock file committed for reproducibility. |
| **License** | MIT. |
| **North star** | Usability > documentation (which IS the showcase) > everything else. |

---

## Scope Boundary

| IN SCOPE | OUT OF SCOPE |
|----------|--------------|
| SDK + CLI: `git clone && pip install -e . && echo "<div>" | tutor eval` works with no additional arguments | No PyPI for the package name |
| MCP server: thin wrapper (~50 lines) around the same SDK | No Protocol Engine (UEP, Handoff, Twin) until core thesis is validated |
| Curriculum tracks: remedial (fundamentals + Booster) / standard / honors | No external runtime dependencies |
| Model registry: curated `models.json` with capability profiles | No modules without documented research sources in `SOURCES.md` |
| Classes: YAML checklist format with rules, FAIL/PASS examples, check selectors | No pricing, GTM, or sales materials |
| Eval harness: 3-layer hybrid (rules → LLM judge → adversarial verification). Phase 0 ships Layer 1 only. | No community infrastructure before v1 ships |
| 8B Booster Protocol: remedial track only, multi-factor activation threshold, subprocess sandbox with documented limitations | |
| Per-class virtual environments for dependency isolation | |
| Docs ARE the showcase | |
| Bidirectional sync: Tutor class ↔ source project standard updates in same commit | |

---

## How It Works

### 1. Enrollment

A model enrolls by identifying itself. `tutor enroll` looks up `models.json` and returns the curriculum track. No diagnostic required — model ratings are public everywhere.

```json
{
  "deepseek/deepseek-v4-flash": {
    "tier": "mid",
    "capabilities": {
      "context_window": 65536,
      "code_generation": {"html": "high", "react": "high", "python": "high", "sql": "high"},
      "tool_calling": {"reliability": "high", "parallel_calls": true},
      "reasoning": {"max_reliable_steps": 5, "cot_reliable": true}
    }
  },
  "gemma4:latest": {
    "tier": "small",
    "capabilities": {
      "context_window": 8192,
      "code_generation": {"html": "low", "react": "low", "python": "medium", "sql": "low"},
      "tool_calling": {"reliability": "low", "parallel_calls": false},
      "reasoning": {"max_reliable_steps": 2, "cot_reliable": false}
    }
  },
  "claude-opus-4-8": {
    "tier": "ultra",
    "capabilities": {
      "context_window": 200000,
      "code_generation": {"html": "high", "react": "high", "python": "high", "sql": "high"},
      "tool_calling": {"reliability": "very_high", "parallel_calls": true},
      "reasoning": {"max_reliable_steps": 10, "cot_reliable": true}
    }
  }
}
```

**Track assignment** is a function of the capability profile, not a hardcoded field. Models with reliable multi-step reasoning (4+ steps) and high code gen across languages qualify for honors. Models with limited reasoning depth get standard. Models with unreliable tool calling or sub-8K context get remedial.

**Unregistered models** default to remedial (conservative — underestimating is safer than overestimating in an education context).

**Diagnostic override:** Optional `tutor assess --diagnostic` runs 20 benchmark tasks. If results contradict the registry, the diagnostic wins for the session. Override expires after 30 days.

### 2. Tracks

| Track | Typical Student | Class Order | Booster |
|-------|----------------|-------------|---------|
| **Honors** | Frontier (Opus, GPT-5, Gemini Pro) | code-review → audit → architect → prompt-design → security → defense → test → perf → brushes | No |
| **Standard** | Mid-tier (DeepSeek V4 Flash, Gemini Flash) | brushes → architect → defense → security → test → perf → code-review → audit → prompt-design | Optional |
| **Remedial** | Small (Gemma 8B, Qwen 3.5, Llama 4) | brushes → defense → security → test → architect → perf → code-review → audit → prompt-design | Yes — every class |

**Honors track verification:** Before starting, a 20-task screening diagnostic confirms >= 90% pass rate on fundamental violations without class injection. Models below 90% are placed in standard. This prevents assuming frontier competency without evidence.

### 3. Classes

Each class is a YAML file with:
- **Rules** — checklist in `[RULE]` prefix format, optimized for token-efficient injection (~120 tokens vs ~500 for prose)
- **FAIL/PASS examples** — paired, minimal, per-framework (html, react, vue, vanilla)
- **Check selectors/regex** — the same file defines how the eval harness tests it. No drift between teaching and testing.
- **Prerequisites, target violations, estimated injection cost**

### 4. The 8B Booster Protocol (Remedial Track)

Activated by multi-factor threshold: `f(context_window, param_count, tool_reliability)` with threshold at 0.65. Not a hard 8B line — depends on working memory score.

| Tool | What it does | Sandbox used? |
|------|-------------|---------------|
| `write_to_scratchpad` | Solve logic in sandbox before generating code | Yes — subprocess with 30s timeout, 50MB disk quota |
| `self_consistency_check` | List assumptions → server validates → model confirms | Yes |
| `inject_few_shot` | Embed concrete frontier-tier examples per task | No (static prompt construction) |
| `downstream_lookahead` | Predict edge cases 50 lines ahead from current choices | No (static analysis) |

**Sandbox:** Three-layer design. Phase 0 ships Layer 1 (tempdir + subprocess + resource limits). Limitations documented in tool descriptions (no network isolation, no memory caps, same OS user). Concurrent calls managed by semaphore (default: 3 max).

**Fallback when sandbox unavailable:** Static injection degradation with explicit logging. `write_to_scratchpad` becomes a system prompt instruction. `self_consistency_check` and `downstream_lookahead` are unavailable.

### 5. Grading

**Eval harness:** Three-layer hybrid. Phase 0 ships Layer 1 only.

| Layer | What it checks | Method | Phase |
|-------|---------------|--------|-------|
| 1. Rules Engine | Codifiable rules (WCAG, OWASP patterns, syntax) | Deterministic selectors, regex, AST checks. ~30-40 rules, ~40-50% coverage. Fully testable. | Phase 0 |
| 2. LLM Judge | Ambiguous criteria (semantic correctness, visual affordance) | Separate evaluator model (different family from student). Confidence-scored (>= 0.80 accepted, 0.60-0.80 weighted, < 0.60 human review). | Phase 1 |
| 3. Adversarial Verification | Challenges the judge's own verdict | Same evaluator model, different prompt ("find what the judge missed"). Catches self-contradiction and position bias. | Phase 1 |

**Human calibration loop:** Weekly audit of flagged evaluations. Accuracy metric published in README. Tunes thresholds and catches evaluator drift.

**The harness is authoritative, not infallible.** Its accuracy against human review is a published metric. This is the honest position.

---

## Architecture

```
lm-tutor/
├── pyproject.toml                # Core deps only: mcp, pydantic, pyyaml
├── requirements.txt              # Lock file (committed, CI-verified)
├── Dockerfile                    # Multi-stage build for air-gapped installs
│
├── tutor/
│   ├── __init__.py
│   ├── __main__.py               # CLI entry point
│   │
│   ├── registrar/                # Enrollment and state
│   │   ├── enroll.py             # Registry lookup, track assignment
│   │   └── state.py              # Crash-recovery state store (atomic-write JSON)
│   │
│   ├── registry/
│   │   ├── models.json           # Curated capability profiles
│   │   ├── overrides.json        # Manual overrides (win over auto-synced data)
│   │   └── sync.py               # Scrape OpenRouter/LMSys for updates
│   │
│   ├── classes/                  # One directory per class
│   │   ├── brushes/class.yaml    # Rules, FAIL/PASS examples, check selectors
│   │   ├── code-review/class.yaml
│   │   ├── prompt-design/class.yaml
│   │   ├── audit/class.yaml
│   │   ├── architect/class.yaml
│   │   ├── defense/class.yaml
│   │   ├── perf/class.yaml
│   │   ├── test/class.yaml
│   │   └── security/class.yaml
│   │
│   ├── booster/                  # 8B Booster Protocol
│   │   ├── sandbox.py            # ScratchpadSandbox + SandboxManager
│   │   └── tools.py              # write_to_scratchpad, consistency_check, etc.
│   │
│   ├── grading/                  # Grading Board
│   │   ├── evaluate.py           # evaluate_submission()
│   │   └── socratic_debug.py     # Hypothesis → Proof → Fix cycle
│   │
│   ├── eval/                     # Eval harness (authoritative scoring function)
│   │   ├── worker_pool.py        # multiprocessing.Process pool (2 workers, forked at startup)
│   │   ├── harness.py            # Layer 1: rules engine
│   │   ├── llm_judge.py          # Layer 2: LLM judge (Phase 1)
│   │   └── adversarial.py        # Layer 3: adversarial verification (Phase 1)
│   │
│   ├── mcp/                      # MCP server (thin wrapper)
│   │   ├── server.py             # ~50-line MCP server
│   │   ├── logging.py            # NDJSON to stderr (never stdout)
│   │   ├── health.py             # HTTP :9090 + MCP tool
│   │   └── metrics.py            # In-memory counters and latency histograms
│   │
│   ├── _class_venv.py            # Per-class virtual environment manager
│   │
│   └── cli/                      # CLI entry points
│       ├── enroll.py
│       ├── learn.py
│       ├── eval.py               # syllabus inference heuristic
│       ├── mcp.py
│       └── list.py
│
├── docs/
│   └── reviews/
│       ├── adversarial-critique.md
│       ├── strategic-review.md
│       ├── adversarial-review.md
│       ├── devops-review.md
│       ├── ml-review.md
│       ├── devops-architecture.md
│       └── ml-curriculum.md
```

### Eval Harness Architecture

```python
# Worker pool: Process isolation without cold-start tax
pool = PoolManager(size=2)        # forks at startup, keeps alive
pool.grade(submission, syllabus)  # sends to queue, worker grades, returns result

# Layer 1: Rules Engine (Phase 0)
rules = load_syllabus(syllabus)   # class.yaml → list of rules
for rule in rules:
    violations += check_selector(rule.selector, submission)
    violations += check_regex(rule.regex, submission)

# Layer 2: LLM Judge (Phase 1)
judge = LLMJudge(model="claude-opus-4-8")
verdict = judge.evaluate(submission, rubric)
# confidence >= 0.80 accepted, 0.60-0.80 weighted, < 0.60 human review

# Layer 3: Adversarial Verification (Phase 1)
verifier = AdversarialVerifier(model=judge.model)
crosscheck = verifier.challenge(verdict)
# if judge and verifier disagree: human review queue
```

### Observability

- **Logging:** NDJSON to stderr only. Never stdout (would corrupt MCP stdio protocol).
- **Health:** HTTP endpoint on port 9090 (works with Docker HEALTHCHECK, K8s probes). Also exposed as MCP tool.
- **Metrics:** In-memory counters for eval tasks, Booster invocations, enrollments, per-tool call counts. Latency histograms with p99.
- **Crash recovery:** Atomic-write JSON state file at `~/.tutor/track_state.json`, checkpointed after every exercise. On restart, model resumes from last checkpoint.

### Dependency Isolation

- **Core deps** (3): `mcp`, `pydantic`, `pyyaml` — pinned in `pyproject.toml` with upper bounds.
- **Class deps:** Per-class virtual environments created lazily on first use. Each class's `_requirements.txt` installed into its own venv. `pip install -e .` stays lightweight. Class A (pillow) and Class B (numpy 2.x) never conflict.
- **Lock file:** `requirements.txt` committed, CI-verified against `pyproject.toml`.
- **Docker:** Multi-stage build freezes all deps in a layer. Air-gapped installs use the Docker image.

---

## Benchmark Methodology

### The Honest Claim

**Minimum viable effect:** 15-20% reduction in fundamental violations for small models using lm-tutor.
**Aspirational target:** 40-60% reduction on targeted violation types as classes mature.

Both are published. Phase 0 targets the minimum. Phases 1-3 target the aspirational.

### Baseline Conditions

Every benchmark includes four conditions to isolate the marginal value:

| Condition | What it measures |
|-----------|-----------------|
| 1. Raw model, no injection | Baseline failure rate |
| 2. Model + best-prompt system prompt | Minimum intervention ceiling — what does just telling the rules do? |
| 3. Model + class injection | Tutor effect — what does structured curriculum add? |
| 4. Model + class + Booster | Full system — what does the complete stack do? |

### Statistical Protocol

- **20 runs per cell** (not 3). LLM output variance requires this for statistical significance.
- **Temperature:** 0.7 primary, 0.0 ablation (5 runs). Reported separately.
- **Seeds:** Fixed per model per task. `seed = hash(model_id + task_name) % 2^32`.
- **Significance:** Bootstrap hypothesis test (10,000 resamples) with Benjamini-Hochberg FDR correction.
- **Effect size:** Cohen's d relative to baseline. 95% CI reported via bootstrap.
- **Reporting:** Mean violation count, standard deviation, pass rate per model per task. Per-violation-type stratified results.

### Phase 0 Benchmark

- **Models:** DeepSeek V4 Flash, Gemma 4 8B, Llama 4 8B, GPT-4o-mini
- **Tasks:** HTML page, React component, JSON API response, SVG graphic, Markdown doc
- **Classes:** 1 (brushes/accessibility — Phase 0 ships only Layer 1 eval)
- **Conditions:** 4 (raw, best-prompt, class, class+booster)
- **Total evaluations:** 4 x 5 x 4 x 20 = 1,600
- **Estimated cost:** ~$2-5 per full benchmark run
- **Output:** Published in README. Per model per task, honest, reproducible.

---

## The Core Thesis

Models internalize both correct and incorrect patterns during pre-training. Without steering, the output distribution reflects the training distribution (mostly broken — 95.9% of top 1M homepages have WCAG failures). lm-tutor surfaces the correct patterns through structured, token-efficient injection — making them salient in the attention window at generation time.

This is a **retrieval/attention problem**, not a capability absence. Models have seen correct examples. They default to incorrect ones because the training distribution skews that way. lm-tutor changes what the model attends to at generation time.

**Architecture implication:** Class format is optimized for attention (checklist-first, `[RULE]` landmarks, paired FAIL/PASS examples) rather than for teaching (prose explanations). The eval harness uses deterministic rules where possible so benchmarks are reproducible.

**Literature grounding:** Brown et al. 2020 (in-context learning surfaces latent patterns), Min et al. 2022 (few-shot examples > instructions), Wei et al. 2022 (CoT benefits inconsistent below 100B), Wang et al. 2023 (structured CoT helps small models more), Zheng et al. 2024 (LLM-as-judge has systematic biases).

---

## Research Requirement

Every class must have `SOURCES.md` before any code is written. No "because I think so."

| Standard | Domain | What to extract |
|----------|--------|----------------|
| WCAG 2.2 | UI/UX accessibility | Codifiable SC criteria, failure patterns, exceptions |
| OWASP Top 10 (2025) | Application security | Detectable violations → remediation patterns |
| NIST SP 800-53 / SOC2 | Audit & compliance | Evidence requirements, tamper-evident standards, retention |
| Code review research (IEEE/ACM) | Review process | What actually catches bugs vs what doesn't |

---

## Relationship to Source Projects

lm-tutor classes are independent from any specific source project. Classes cite
external standards only (WCAG, OWASP, IEEE, NIST). Content from external
projects is absorbed during Phase 1 through research audit, with full attribution
in each class's `SOURCES.md`.

**Zero runtime dependency.** lm-tutor does not import code from any Ghost Stack project. Knowledge only.

---

## Phases

### Phase 0 — Skeleton + Rules Engine (BUILD READY)

- SDK scaffold, CLI entry points (`tutor enroll`, `tutor learn`, `tutor eval`, `tutor mcp`, `tutor list`)
- Model registry: static `models.json` with capability profiles
- `tutor/eval/worker_pool.py` — multiprocessing process pool
- `tutor/eval/harness.py` — Layer 1 rules engine (~30-40 rules)
- `tutor/eval/cli.py` — syllabus inference heuristic
- `tutor/booster/sandbox.py` — ScratchpadSandbox + SandboxManager
- `tutor/_class_venv.py` — per-class virtual environment manager
- `tutor/mcp/` — server, logging (stderr NDJSON), health (:9090), metrics (in-memory)
- `tutor/registrar/state.py` — crash recovery state store
- Dockerfile, requirements.txt lock file
- Baseline benchmark (1,600 evaluations, published in README)
- Docs: README.md, quickstart, tool reference. Docs ARE the showcase.

### Phase 1 — Classes (one at a time, each with SOURCES.md)

1. `brushes` — UI/UX accessibility. Compatibility analysis first.
2. `code-review` — House patterns. Research audit required.
3. `prompt-design` — Prompt Brush pipeline. Research audit required.
4. `audit` — Agentic Chain. Research audit required.
5. Architect, defense, perf, test, security — standard references.
6. `tutor/registry/sync.py` — automated refresh from public benchmarks.
7. `tutor/eval/llm_judge.py` — Layer 2 LLM judge.
8. `tutor/eval/adversarial.py` — Layer 3 adversarial verification.

### Phase 2 — Grading Board

- Wire `evaluate_submission` to class syllabus (read from `class.yaml check_*` fields).
- Track progression: class pass/fail → next class unlock.
- Human calibration loop: weekly audit, accuracy metric published.

### Phase 3 — Booster Integration

- Wire Booster into remedial track.
- Benchmark: booster alone vs classes alone vs both.

### Phase 4 — Protocol Engine (DEFERRED, gated)

- Only if Phases 0-3 validate the core thesis. Not before.

---

## Success Criteria

1. **15-20% reduction** in fundamental violations for remedial-track models on the Phase 0 benchmark (measured by eval harness, published in README).
2. **`git clone && pip install -e . && echo "<div>" | tutor eval`** — works with zero additional arguments. Syllabus auto-detected from content.
3. **Model registry** — curated `models.json`. Enrollment returns track from identity. No diagnostic required.
4. **Class template + CONTRIBUTING.md** — adding a class = one `class.yaml` + one `SOURCES.md` + one test file.
5. **Baseline published** — per model per task, honest methodology, all four conditions, bootstrap CIs.
6. **Eval harness accuracy** — measured against human review, published in README.

---

## Ideas Deferred

| Idea | Why |
|------|-----|
| Protocol Engine (UEP, Handoff, Twin) | Gated on core thesis validation |
| External agent governance integration | Different problem space |
| Go/Rust binary | Python SDK first |
| Community infra | v1 first, v2 community |
| Training / fine-tuning | Inference-side only |
| PyPI publishing | Unreliable. Clone + `pip install -e .` is primary. |
| **Building Outward** — multi-class prefix composition (`tutor prefix`), agent integration (Hermes/OpenCode call tutor before code gen), universal generation-time quality floor | **In progress** — JS class shipped 2026-06-09 (`github.com/mfolofy/lm-tutor`). Next: TS class, then `tutor prefix` command. Agent integration still deferred until prefix ships. |

---

## Boundaries

- **lm-tutor does NOT depend on any Ghost Stack project** — it imports no Ghost Stack code, has no Ghost Stack runtime dependency. Classes cite external standards only (WCAG, OWASP, IEEE, NIST). Zero coupling.
- **lm-tutor is NOT an evaluation platform** — the eval harness is a teaching feedback tool, not a certification engine. No grading board, no progression tracking, no human-facing audit dashboards.
- **lm-tutor is NOT a linter or CI tool** — it does not run in CI pipelines, does not produce build-fail signals, does not replace axe-core, Lighthouse, or any human-facing audit tool. The eval harness is a model's feedback loop, not a human's QA gate.
- **lm-tutor is architecturally independent** of any other project. The standalone repo (`github.com/mfolofy/lm-tutor`) is the canonical distribution.

## Locked Decisions

These decisions cannot be re-litigated without Miguel:

1. **Classes ARE the product.** The unit of delivery is a `class.yaml` with `[RULE]` checklists, FAIL/PASS framework examples, and a `SOURCES.md` with cited research. No evaluation infrastructure beyond Layer 1 (selector/regex). No computation engines. No CSS parsers.
2. **No human-facing audit tools.** No dashboards, no CI integrations, no grading scorecards for humans. The eval harness (`tutor eval`) is a CLI tool for models — pipe content in, get violations out. That is the ceiling.
3. **No evaluation infrastructure for Phase 0.** No benchmarks, no grading board, no progression tracking. The benchmark protocol in Success Criteria #1 is aspirational — not a build requirement.
4. **Research-first class creation.** Every class requires a `SOURCES.md` with cited standards before any YAML is written. No "because I think so" rules.
5. **Per-class virtual environments** for dependency isolation. No core dependency bloat.
6. **CLI-only delivery.** No daemon mode, no persistent server (the MCP server is a thin wrapper for IDE/agent integration, not a primary delivery target).

## Last Reviewed

- **Date:** 2026-06-09
- **Reviewer:** Mike (Claude Code / deepseek-v4-flash)
- **Approved by:** Miguel

## Building Outward — Progress

- **2026-06-09:** `javascript-best-practices` class shipped (16 rules, 44% checkable by regex). Committed to `github.com/mfolofy/lm-tutor` standalone repo.
- **Next:** TypeScript class, then `tutor prefix` command for multi-class composition.
