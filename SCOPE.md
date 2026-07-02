# lm-tutor — The School for LLMs

> **Tagline:** "The School for LLMs"
> **Project:** `lm-tutor`
> **Status:** SCOPE — ground zero
> **Date:** 2026-06-10

---

## Identity

| Field | Value |
|-------|-------|
| **Name** | `lm-tutor` |
| **What it is** | Structured AI education for any model. Everyone's welcome. Enrollment → curriculum track → classes → graduation. |
| **Location** | `projects/lm-tutor/` (monorepo) + `github.com/mfolofy/lm-tutor` (standalone, dual-homed) |
| **CLI** | `tutor enroll` — model says who it is, track assigned. `tutor learn` — take a class. `tutor eval` — grade output. `tutor fix` — iterative correction loop. `tutor booster` — sandbox tools (scratchpad, verify, exemplars, foresee). `tutor prefix` — compose multiple class prefixes. `tutor curriculum` — ordered class list per track. `tutor profile` — pass rate history per class. `tutor class --new` — scaffold a new class. `tutor install-opencode` — inject rules into OpenCode config. `tutor list` — list available classes. `tutor mcp` — launch MCP server. |
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
| Classes: YAML checklist format with rules, FAIL/PASS examples, check selectors/regex | No pricing, GTM, or sales materials |
| 56 classes across core tracks, best-practices tracks, credential tracks, and web-design & frontend tracks | No community infrastructure before v1 ships |
| Eval harness: 3-layer hybrid (rules → LLM judge → adversarial verification). Layer 1 (selector/regex) ships in Phase 0. Layers 2-3 in Phase 1. | |
| 8B Booster Protocol: remedial track only, multi-factor activation threshold, subprocess sandbox with documented limitations | |
| Benchmark infrastructure (`tutor/benchmark.py`) — runs real model evaluations against class rules. Published results in README. | |
| Per-class virtual environments for dependency isolation | |
| Docs ARE the showcase | |
| Bidirectional sync: Tutor class ↔ source project standard updates in same commit | |
| Fable 5 self-admitted validation — external model self-evaluates against class rules (`docs/validation/FABLE5_SELF_ADMITTED.md`) | |

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
  "claude-sonnet-4-6": {
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

### 2. Tracks

| Track | Typical Student | Booster |
|-------|----------------|---------|
| **Honors** | Frontier (Opus, GPT-5, Gemini Pro) | No |
| **Standard** | Mid-tier (DeepSeek V4 Flash, Gemini Flash) | Optional |
| **Remedial** | Small (Gemma 8B, Qwen 3.5, Llama 4) | Yes — every class |

**Class sequencing** per track is defined by `tutor curriculum --model <id>`. The model's capability profile and previous eval history determine the optimal learning path. Honors-track models start on code-review → architect → security. Remedial starts on brushes → defense → test.

### 3. Classes

Each class is a directory with:
- **`class.yaml`** — rules in `[RULE]` prefix format (~120 tokens per rule), FAIL/PASS examples per framework, `check_selector`/`check_regex` for deterministic grading. No drift between teaching and testing.
- **`SOURCES.md`** — cited external standards (WCAG, OWASP, NIST, IEEE, etc.). Every rule must trace to a standard.
- **`grader.py`** (optional) — custom grading logic for credential classes that need domain-specific scoring beyond Layer 1.

**56 classes** across four families:

**Core (10):** brushes, code-review, audit, security, architect, defense, perf, test, prompt-design, api-design

**Best-Practices (4):** python-best-practices, javascript-best-practices, typescript-best-practices, devops

**Web Design & Frontend (18):** css-modern, react-server-components, view-transitions, design-tokens, css-color, web-animation, frontend-architecture, web-vitals, web-components, build-tooling, three-js, html-apis, responsive-design, web-typography, astro, webgpu, webxr, svelte-5

**Credential (24):** credential-jd (legal), credential-md (medical), credential-cpa (accounting), credential-pe (engineering), credential-lcsw (social work), credential-journalist, credential-finra (finance), credential-pharmacist, credential-ra (regulatory), credential-rn (nursing), credential-pilot, credential-realtor, credential-pm (project management), credential-dentist, credential-paramedic, credential-adjuster, credential-electrician, credential-judge, credential-socialworker, credential-vet, credential-hr, credential-psychiatry, credential-anthropology, credential-marketing-sales-ui

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
| 1. Rules Engine | Codifiable rules (WCAG, OWASP patterns, syntax) | Deterministic selectors, regex. 253 checkable rules of 838 total across 56 classes (10 classes have no machine-checkable rules and report `rules_checked: 0`). Fully testable. | Phase 0 |
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
│   ├── __main__.py               # CLI entry point (dispatches 12 commands)
│   │
│   ├── registrar/                # Enrollment and state
│   │   ├── enroll.py             # Registry lookup, track assignment
│   │   ├── evals.py              # Eval history store (JSONL, per-model)
│   │   └── state.py              # Crash-recovery state store (atomic-write JSON)
│   │
│   ├── registry/
│   │   ├── models.json           # Curated capability profiles
│   │   ├── overrides.json        # Manual overrides (win over auto-synced data)
│   │   └── sync.py               # Scrape OpenRouter/LMSys for updates (Phase 1)
│   │
    │   ├── classes/                  # 56 classes — see MANIFEST.json for full listing

│   ├── booster/                  # 8B Booster Protocol
│   │   ├── sandbox.py            # ScratchpadSandbox + SandboxManager
│   │   └── tools.py              # write_to_scratchpad, consistency_check, etc.
│   │
│   ├── grading/                  # Grading Board (Phase 2)
│   │   ├── evaluate.py           # evaluate_submission()
│   │   └── socratic_debug.py     # Hypothesis → Proof → Fix cycle
│   │
│   ├── eval/                     # Eval harness (authoritative scoring function)
│   │   ├── worker_pool.py        # multiprocessing.Process pool (2 workers)
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
│   ├── benchmark.py              # Peer review benchmark runner
│   │
│   └── cli/                      # CLI entry points (12 commands)
│       ├── enroll.py             #   tutor enroll
│       ├── learn.py              #   tutor learn
│       ├── eval.py               #   tutor eval (syllabus inference heuristic)
│       ├── fix.py                #   tutor fix (iterative correction loop)
│       ├── booster.py            #   tutor booster (scratchpad/verify/exemplars/foresee)
│       ├── prefix.py             #   tutor prefix (multi-class composition)
│       ├── curriculum.py         #   tutor curriculum (ordered class list per track)
│       ├── profile.py            #   tutor profile (pass rate history)
│       ├── new_class.py          #   tutor class --new (scaffold generator)
│       ├── install_opencode.py   #   tutor install-opencode (OpenCode injection)
│       ├── list.py               #   tutor list
│       └── mcp.py                #   tutor mcp (MCP server launch)
│
├── docs/
│   ├── reviews/
│   │   ├── strategic-review.md
│   │   ├── adversarial-review.md
│   │   ├── devops-review.md
│   │   ├── ml-review.md
│   │   └── scenario-assessment.md
│   ├── designs/
│   │   ├── devops-architecture.md
│   │   └── ml-curriculum.md
│   └── validation/
│       └── FABLE5_SELF_ADMITTED.md  # Fable 5 self-validation protocol
│
├── paper/
│   ├── arxiv-latex.tex           # Academic paper (pre-print)
│   ├── arxiv-paper.md            # Paper markdown source
│   └── peer-review-test-plan.md  # Peer review plan
│
└── tests/                        # 1,869 tests, 57 test files
    ├── test_brushes.py
    ├── test_code_review.py
    └── ... (one per class)
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
judge = LLMJudge(model="claude-sonnet-4-6")
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

### Phase 0 Benchmark Results (Published 2026-06-10)

5 peer review benchmarks run against DeepSeek V4 Flash and DeepSeek Reasoner:

| Test | Finding |
|------|---------|
| Test 1 (Pro 5-run) | Reasoner: raw 14.0 → class 1.0 (**-93%**). 3/5 runs passed with injection. |
| Test 2 (Explicit Follow-Up) | Flash raw 14.6 → fix 12.8 (**-12%**). Injection is real steering, not just a reminder. |
| Test 3 (Difficulty Ladder) | Inverted-U confirmed: simple 0%, complex **-68%**, SPA -13%. Peak effect on complex tasks. |
| Test 4 (Cross-Class) | All 0.0 violations for non-HTML tasks — ceiling effect. |
| Test 5 (Follow-Up Additive) | Class alone avg 5.2 = class + fix avg 5.2 (**0% additive benefit**). Fix after class adds nothing. |

**Core thesis validated:** injection is steering (not reminder), scales with model intelligence, peaks on complex tasks.

### Statistical Protocol (Aspirational — for publication)

- **20 runs per cell** (not 3). LLM output variance requires this for statistical significance.
- **Temperature:** 0.7 primary, 0.0 ablation (5 runs). Reported separately.
- **Seeds:** Fixed per model per task. `seed = hash(model_id + task_name) % 2^32`.
- **Significance:** Bootstrap hypothesis test (10,000 resamples) with Benjamini-Hochberg FDR correction.
- **Effect size:** Cohen's d relative to baseline. 95% CI reported via bootstrap.
- **Reporting:** Mean violation count, standard deviation, pass rate per model per task. Per-violation-type stratified results.

### Fable 5 Self-Admitted Validation

**New — first external model validation (2026-06-10).**

Protocol (`docs/validation/FABLE5_SELF_ADMITTED.md`):
1. Fable 5 receives a production task + lm-tutor class rules for the relevant domain
2. Fable 5 produces output (code, analysis, etc.)
3. Fable 5 self-evaluates output against class rules using `tutor eval`
4. Fable 5 reports violations with evidence
5. Results recorded and compared against non-injected baseline

Run by Miguel in Claude Code. This is the first test of lm-tutor's thesis on a model that was NOT involved in class creation — eliminating training-set contamination.

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
| Profession-specific standards (ABA, AMA, AICPA, etc.) | Credential classes | Domain-specific professional standards |

---

## Relationship to Source Projects

lm-tutor classes are independent from any specific source project. Classes cite
external standards only (WCAG, OWASP, IEEE, NIST, ABA, AMA, AICPA). Content from external
projects is absorbed during Phase 1 through research audit, with full attribution
in each class's `SOURCES.md`.

**Zero runtime dependency.** lm-tutor does not import code from any Ghost Stack project. Knowledge only.

---

## Phases

### Phase 0 — Skeleton + Rules Engine ✅ COMPLETE

- SDK scaffold, CLI entry points (12 commands)
- Model registry: static `models.json` with capability profiles
- `tutor/eval/worker_pool.py` — multiprocessing process pool
- `tutor/eval/harness.py` — Layer 1 rules engine (838 rules, 253 checkable)
- `tutor/booster/sandbox.py` — ScratchpadSandbox + SandboxManager
- `tutor/_class_venv.py` — per-class virtual environment manager
- `tutor/mcp/` — server, logging (stderr NDJSON), health (:9090), metrics (in-memory)
- `tutor/registrar/state.py` — crash recovery state store
- `tutor/registrar/evals.py` — eval history (JSONL, per-model isolation)
- `tutor/benchmark.py` — peer review benchmark runner
- Dockerfile, requirements.txt lock file
- Peer benchmarks published (5 tests, thesis validated)
- Docs: README.md, SCOPE.md, CONTRIBUTING.md. Docs ARE the showcase.
- Fable 5 self-admitted validation protocol

### Phase 1 — Classes ✅ COMPLETE

**56 classes built across four families (37 original + 18 web design + credential-marketing-sales-ui):**

**Core (10):** brushes, code-review, audit, security, architect, defense, perf, test, prompt-design, api-design

**Best-Practices (4):** python-best-practices, javascript-best-practices, typescript-best-practices, devops

**Web Design & Frontend (18):** css-modern, react-server-components, view-transitions, design-tokens, css-color, web-animation, frontend-architecture, web-vitals, web-components, build-tooling, three-js, html-apis, responsive-design, web-typography, astro, webgpu, webxr, svelte-5

**Credential (24):** credential-jd, credential-md, credential-cpa, credential-pe, credential-lcsw, credential-journalist, credential-finra, credential-pharmacist, credential-ra, credential-rn, credential-pilot, credential-realtor, credential-pm, credential-dentist, credential-paramedic, credential-adjuster, credential-electrician, credential-judge, credential-socialworker, credential-vet, credential-hr, credential-psychiatry, credential-anthropology, credential-marketing-sales-ui

Each with `class.yaml` + `SOURCES.md`. 51 of 56 classes have a dedicated test file — credential-cpa, credential-md, credential-marketing-sales-ui, javascript-best-practices, and typescript-best-practices do not (open gap). 9 credential classes include optional `grader.py` for domain-specific scoring.

**Phase 1 deferred (moved to Phase 1+):**
- `tutor/registry/sync.py` — automated refresh from public benchmarks
- `tutor/eval/llm_judge.py` — Layer 2 LLM judge
- `tutor/eval/adversarial.py` — Layer 3 adversarial verification

### Phase 2 — Grading Board 🟡 DEFERRED

- Wire `evaluate_submission` to class syllabus (read from `class.yaml check_*` fields).
- Track progression: class pass/fail → next class unlock.
- Human calibration loop: weekly audit, accuracy metric published.

### Phase 3 — Booster Integration ✅ COMPLETE

- `tutor learn --auto` — auto-runs Booster foresight + exemplars for remedial models.
- `tutor fix --booster` — Booster context before fix suggestions.
- Benchmark pipeline validated: learn --auto, fix --booster, eval all pass.
- **Gate:** thesis validated 2026-06-10. Built 2026-06-11.

### Phase 4 — Protocol Engine 🔴 DEFERRED

- Only if Phases 0-3 validate the core thesis. Not before.

---

## Success Criteria

1. **15-20% reduction** in fundamental violations for remedial-track models on the Phase 0 benchmark (measured by eval harness, published in README). **Validated: -68% on complex tasks (Test 3), -93% for Reasoner (Test 1).**
2. **`git clone && pip install -e . && echo "<div>" | tutor eval`** — works with zero additional arguments. Syllabus auto-detected from content.
3. **Model registry** — curated `models.json`. Enrollment returns track from identity. No diagnostic required.
4. **Class template + CONTRIBUTING.md** — adding a class = one `class.yaml` + one `SOURCES.md` + one test file.
5. **Peer benchmarks published** — per model per task, honest methodology, all four conditions.
6. **Eval harness accuracy** — measured against human review, published in README.
7. **Fable 5 self-admitted validation** — external model verifies thesis without training-set contamination risk.

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
| Agent integration (Hermes/OpenCode hook) | Deferred. `tutor install-opencode` exists as experimental — formalize after thesis validation. |

---

## Boundaries

- **lm-tutor does NOT depend on any Ghost Stack project** — it imports no Ghost Stack code, has no Ghost Stack runtime dependency. Classes cite external standards only (WCAG, OWASP, IEEE, NIST, ABA, AMA, AICPA). Zero coupling.
- **lm-tutor is NOT an evaluation platform** — the eval harness is a teaching feedback tool, not a certification engine. No grading board, no progression tracking, no human-facing audit dashboards. `tutor profile` shows the model its own history (feedback loop), not a human-facing scorecard.
- **lm-tutor is NOT a linter or CI tool** — it does not run in CI pipelines, does not produce build-fail signals, does not replace axe-core, Lighthouse, or any human-facing audit tool. The eval harness is a model's feedback loop, not a human's QA gate.
- **lm-tutor is architecturally independent** of any other project. The standalone repo (`github.com/mfolofy/lm-tutor`) is the canonical distribution.

## Locked Decisions

These decisions cannot be re-litigated without Miguel:

1. **Classes ARE the product.** The unit of delivery is a `class.yaml` with `[RULE]` checklists, FAIL/PASS framework examples, and a `SOURCES.md` with cited research. No evaluation infrastructure beyond Layer 1 (selector/regex). No computation engines. No CSS parsers. *(Exception: credential `grader.py` files are in-scope as optional domain-specific scoring adjuncts to Layer 1.)*
2. **No human-facing audit tools.** No dashboards, no CI integrations, no grading scorecards for humans. The eval harness (`tutor eval`) is a CLI tool for models — pipe content in, get violations out. `tutor profile` is a model's own feedback loop, not a human dashboard.
3. **Benchmarks are in scope.** The benchmark runner (`tutor/benchmark.py`) and published peer review results are a required validation layer. They are NOT evaluation infrastructure (not a dashboard, not a progression tracker). The 5-run peer review protocol is the standard; the 20-run/1,600-eval statistical protocol is aspirational for publication.
4. **Research-first class creation.** Every class requires a `SOURCES.md` with cited standards before any YAML is written. No "because I think so" rules.
5. **Per-class virtual environments** for dependency isolation. No core dependency bloat.
6. **CLI-only delivery.** No daemon mode, no persistent server (the MCP server is a thin wrapper for IDE/agent integration, not a primary delivery target).
7. **Credential classes are in scope** as domain-specific professional-standards education. Each maps to an external professional standard body. `grader.py` files are optional adjuncts for domain-specific scoring, NOT evaluation infrastructure.

## Last Reviewed

- **Date:** 2026-06-11
- **Reviewer:** Mike (Claude Code / claude-sonnet-4-6)
- **Approved by:** Miguel

## Building Outward — Progress

- **2026-06-09:** `javascript-best-practices` class shipped (16 rules). `typescript-best-practices` shipped (16 rules). `tutor prefix` command shipped (multi-class composition). `tutor install-opencode` shipped (experimental agent injection).
- **2026-06-09:** `tutor class --new` scaffold shipped. Class audit + hardening complete (all 34 classes verified at the time; expanded to 37 on 2026-06-11).
- **2026-06-10:** Phase 1 complete — 37 classes, 602 rules, 1,733+ tests. Peer benchmarks published — core thesis validated. SCOPE updated with all 37 classes + credential tracks + Fable 5 validation.
- **2026-06-11:** Phase 3 complete — Booster wired into remedial track (`tutor learn --auto`, `tutor fix --booster`). credential-psychiatry + credential-anthropology shipped (Mai dependency). 37 classes, 1,733+ tests.
- **2026-06-11:** Web Design & Frontend curriculum shipped — 18 new classes (199 rules, 67 tests) across 4 tiers. Deep-research-validated (109 agents, 27 sources, 12 confirmed claims). Covers: modern CSS platform features, React 19 Server Components, View Transitions, Design Tokens (DTCG v2025.10), CSS Color Level 5, scroll-driven animations, frontend architecture patterns, Core Web Vitals, Web Components, Rust-era build tooling, Three.js, modern HTML APIs, responsive design, web typography, Astro islands, WebGPU, WebXR, Svelte 5 runes. Total: 55 classes.
- **2026-07-02:** Adversarial review reconciliation — `credential-marketing-sales-ui` had shipped undocumented (scope drift; now listed, total: 56 classes). Counts corrected against the tree: 838 rules, 253 machine-checkable, 1,869 tests / 57 files; 10 web classes carry no machine-checkable rules and the harness now reports `rules_checked: 0` for them instead of implying a verified pass. MANIFEST.json regenerated (was stale at 37 entries). `tutor fix --auto` wired and made functional (flag was documented but never registered; the loop could never read a second submission from a pipe). `tutor learn --auto` exemplar block now actually contains the class's FAIL/PASS examples (was injecting an empty header). `pip install -e .` fixed (package-data key rejected by setuptools >= 74).
