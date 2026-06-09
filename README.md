# lm-tutor — The School for LLMs

> Structured AI education for any model. Enrollment → curriculum track → classes → graduation.
> **Status:** Phase 1 — 9 classes live (151 rules, 160 checkable + teaching). MIT licensed.

Most web data is full of bad practices. Models trained on it reproduce those
patterns — not because they *can't* do better, but because the broken pattern is
the high-probability one without steering. (95.9% of the top million homepages
have WCAG failures; a model that learned accessible markup from the other 4.1%
still defaults to the majority.)

lm-tutor treats this as a **retrieval/attention problem, not a capability gap**.
It surfaces the correct patterns through structured, token-efficient injection —
making them salient in the attention window at generation time — and grades the
result with a deterministic rules engine.

---

## Quickstart

```bash
git clone https://github.com/mfolofy/lm-tutor.git
cd lm-tutor
pip install -e .
echo "<div>" | tutor eval
```

That last line works with **zero additional arguments**. The syllabus is
auto-detected from the content. Output is JSON on stdout:

```json
{
  "syllabus": "brushes (auto-detected)",
  "passed": true,
  "rules_checked": 10,
  "violations": [],
  "hint": "No fundamental violations found by Layer 1.",
  "error": null
}
```

Pipe in something with real accessibility problems and the engine names them:

```bash
$ printf '<html><img src="a.png"><button></button></html>' | tutor eval
```
```json
{
  "syllabus": "brushes (auto-detected)",
  "passed": false,
  "rules_checked": 10,
  "violations": [
    {"rule": "img-alt",     "severity": "fundamental", "wcag": "1.1.1", "message": "Every <img> must have an alt attribute...", "matched": "<img src=\"a.png\">"},
    {"rule": "button-name", "severity": "fundamental", "wcag": "4.1.2", "message": "Buttons must have an accessible name...",     "matched": "<button>"},
    {"rule": "html-lang",   "severity": "fundamental", "wcag": "3.1.1", "message": "The root <html> element must declare a lang attribute.", "matched": "<html>"}
  ]
}
```

`tutor eval` exits **0 on any successful grade** — violations are a result, not
an error. A non-zero exit means the grade itself could not run (e.g. unknown
class).

---

## The CLI

| Command | What it does |
|---------|--------------|
| `tutor enroll --model <id>` | Look the model up in the registry and print its curriculum track + Booster status. |
| `tutor learn --model <id> --class <name>` | Render the class's token-efficient injection prefix; checkpoint progress. |
| `tutor eval [--class <name>]` | Grade a submission read from **stdin** with the Layer 1 rules engine. |
| `tutor fix [--class <name>]` | Eval → fix → re-eval correction loop with `--once` or `--auto`. |
| `tutor mcp [--no-health]` | Launch the MCP server (stdio) + HTTP health on `:9090`. |
| `tutor list` | List available classes. |
| `tutor curriculum --model <id>` | Show ordered class list for the model's track. |
| `tutor booster {scratchpad,verify,exemplars,foresee}` | Booster tools for small models. |

```bash
$ tutor enroll --model claude-opus-4-8
Model:   claude-opus-4-8
Status:  registered
Tier:    ultra
Track:   honors
Booster: off  (working-memory score 1.0)

$ tutor enroll --model gemma4:latest
Track:   remedial
Booster: ON  (working-memory score 0.2788)
```

### Two modes

- **CLI mode (default):** no daemon, no open ports. The process runs, grades, exits.
- **MCP server mode (`tutor mcp`):** long-lived stdio server for IDE/agent
  integration, with an HTTP health endpoint and in-memory metrics. The MCP
  tools (`enroll`, `eval_submission`, `list_available_classes`, `health`) wrap
  the same SDK the CLI uses.

---

## How track assignment works

Track is a **function of the capability profile**, never a hardcoded field:

| Condition | Track |
|-----------|-------|
| Unregistered model | `remedial` (conservative — underestimating is safer in education) |
| Unreliable tool calling **OR** context < 8K | `remedial` |
| Reliable multi-step reasoning (≥ 4 steps) **AND** high code-gen across languages | `honors` |
| Everything else | `standard` |

The **8B Booster** activates on a multi-factor working-memory score
`f(context_window, param_count, tool_reliability)` — not a hard parameter line.
Score `< 0.65` → Booster on. Honors models never use it.

---

## The eval harness

Phase 0 ships **Layer 1 only**: a deterministic rules engine that runs on the
core dependency set (stdlib + pydantic). This is deliberate — Layer 1 is
reproducible, fast, and free.

| Layer | Checks | Method | Phase |
|-------|--------|--------|-------|
| 1. Rules Engine | Codifiable rules (WCAG selectors, regex) | Deterministic | **Phase 0 (this build)** |
| 2. LLM Judge | Ambiguous criteria | Separate evaluator model, confidence-scored | Phase 1 |
| 3. Adversarial | Challenges the judge's verdict | Same model, different prompt | Phase 1 |

Each class's `class.yaml` carries both the teaching examples and the
`check_selector` / `check_regex` that grade them — **no drift between what is
taught and what is tested.**

The harness is **authoritative, not infallible.** Its accuracy against human
review is a published metric (Phase 1, once Layer 2 ships).

---

## Benchmark methodology

The honest claim, published up front:

- **Minimum viable effect:** 15–20% reduction in fundamental violations for
  small models using lm-tutor. *(Phase 0 target.)*
- **Aspirational target:** 40–60% reduction on targeted violation types as
  classes mature. *(Phases 1–3.)*

Every benchmark isolates the marginal value with four conditions:

1. Raw model, no injection (baseline failure rate)
2. Model + best-prompt system prompt (minimum-intervention ceiling)
3. Model + class injection (the tutor effect)
4. Model + class + Booster (full stack)

**Protocol:** 20 runs per cell · temperature 0.7 primary, 0.0 ablation · fixed
seed per (model, task) · bootstrap hypothesis test (10,000 resamples) with
Benjamini-Hochberg FDR correction · Cohen's d effect sizes with 95% bootstrap CIs.

**Phase 0 benchmark plan:** 4 models (DeepSeek V4 Flash, Gemma 4 8B, Llama 4 8B,
GPT-4o-mini) × 5 tasks × 4 conditions × 20 runs = **1,600 evaluations**,
estimated ~$2–5 per full run.

### Results

> **Pending.** Phase 0 ships the harness and the methodology. The 1,600-eval
> baseline has **not yet been run**, so no results table is published here. This
> section will be filled with per-model, per-task numbers — means, standard
> deviations, bootstrap CIs, and all four conditions — once the run completes.
> No invented numbers. That is the whole point of the project.

---

## Success criteria (Phase 0)

| # | Criterion | Status |
|---|-----------|--------|
| 1 | `git clone && pip install -e . && echo "<div>" \| tutor eval` works with zero args | ✅ |
| 2 | Syllabus auto-detected from content | ✅ |
| 3 | Curated `models.json`; enrollment returns track from identity, no diagnostic | ✅ |
| 4 | Class template + `CONTRIBUTING.md`: a class = one `class.yaml` + `SOURCES.md` + one test | ✅ |
| 5 | Layer 1 rules engine, deterministic, stdlib-only on the happy path | ✅ |
| 6 | Baseline benchmark published (per model/task, four conditions, CIs) | ⏳ pending run |
| 7 | Eval-harness accuracy vs human review published | ⏳ Phase 1 (needs Layer 2) |

---

## Architecture (Phase 0)

```
tutor/
├── __main__.py            # single `tutor` console script, argparse subcommands
├── registrar/
│   ├── enroll.py          # track assignment (computed) + Booster threshold
│   └── state.py           # atomic-write crash-recovery state (~/.tutor/)
├── registry/
│   ├── models.json        # 11 curated capability profiles
│   └── overrides.json     # manual overrides win over auto-sync
├── eval/
│   ├── harness.py         # Layer 1 rules engine (stdlib HTML parser + regex)
│   └── worker_pool.py     # multiprocessing pool (benchmark / MCP path)
├── booster/
│   ├── sandbox.py         # ScratchpadSandbox + SandboxManager (subprocess)
│   └── tools.py           # 4 Booster tools, static fallback when no sandbox
├── grading/
│   ├── evaluate.py        # evaluate_submission() wired to class.yaml
│   └── socratic_debug.py  # Hypothesis → Proof → Fix cycle
├── mcp/
│   ├── server.py          # ~50-line FastMCP wrapper
│   ├── logging.py         # NDJSON to stderr ONLY (never stdout)
│   ├── health.py          # HTTP :9090 + MCP tool
│   └── metrics.py         # in-memory counters + p99 latency
├── _class_venv.py         # per-class venvs, lazy creation (~/.tutor/venvs/)
├── cli/                   # enroll, learn, eval, mcp, list handlers
└── classes/brushes/       # first class: accessibility (WCAG 2.2)
```

### Why the CLI doesn't use the worker pool

`tutor eval` calls `grade()` **in-process**. A single grade through a spawned
multiprocessing pool would pay the import tax for nothing (and on Windows/3.14,
spawn re-imports the main module). The pool exists for the long-lived paths —
benchmarks and the MCP server — where startup is amortised over many evals.

### Distribution & the "no PyPI" note (honest)

The **package** is not on PyPI; `git clone && pip install -e .` is primary. Its
**transitive deps** (`mcp`, `pydantic`, `pyyaml`) resolve from PyPI normally.
`requirements.txt` is committed for reproducibility. For truly air-gapped
installs, build the Docker image (`Dockerfile`, multi-stage) — it freezes every
dependency in a layer and needs no further network access.

---

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `TUTOR_STATE_DIR` | `~/.tutor` | Crash-recovery state directory |
| `TUTOR_CLASS_VENV_DIR` | `~/.tutor/venvs` | Per-class virtual environments |
| `TUTOR_EVAL_POOL_SIZE` | `2` | Worker-pool size |
| `TUTOR_BOOSTER_MAX_CONCURRENT` | `3` | Max concurrent Booster sandboxes |
| `TUTOR_MCP_HEALTH_PORT` | `9090` | Health endpoint port |

---

## Contributing

Adding a class is three files: one `class.yaml`, one `SOURCES.md`, one test
file. See [CONTRIBUTING.md](CONTRIBUTING.md). Every class must cite documented
research sources before any code is written — no "because I think so."
