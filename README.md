# lm-tutor — The School for LLMs

> Structured AI education for any model. Enrollment → curriculum track → classes → graduation.
> **Status:** Phase 1 — 9 classes live (151 rules, 422 tests). MIT licensed.

Most web data is full of bad practices. Models trained on it reproduce those
patterns — not because they *can't* do better, but because the broken pattern is
the high-probability one without steering. (95.9% of the top million homepages
have WCAG failures [WebAIM 2026]; a model that learned accessible markup from
the other 4.1% still defaults to the majority.)

lm-tutor treats this as a **retrieval/attention problem, not a capability gap.**
It surfaces the correct patterns through structured, token-efficient injection —
making them salient in the attention window at generation time — and grades the
result with a deterministic rules engine.

---

> **Why it works:** lm-tutor maps every design decision to principles from
> neuroscience, cognitive psychology, and evolutionary biology — attention as
> salience (RAS), Hebbian learning, error-driven prediction error, Vygotsky's
> ZPD, myelination via correction loops, working memory limits, dual-process
> theory, neuroplasticity, metacognition, chunking, and context-dependent
> memory. See the full theory at **[docs/theory.md](docs/theory.md)**.

---

> **43% fewer violations on broken training data — 0% on clean data.**
> DeepSeek V4 Flash: HTML/WCAG (~14 raw → ~8 after `tutor learn` injection).
> Python/PEP 8: already clean, no effect needed. Injection's impact is
> proportional to how broken the training data is for the target domain.
> Full methodology at **[docs/benchmark-methodology.md](docs/benchmark-methodology.md)**.

---

## The Classes

| Class | Rules | Standard | Tests |
|-------|-------|----------|-------|
| **brushes** | 34 (10 check) | WCAG 2.2, ARIA, HTML Living Standard | 67 |
| **code-review** | 18 (2 check) | ITIL v4, arXiv 2603.25773, House/everybody-lies | 26 |
| **audit** | 19 (8 check) | SOC2, HIPAA, CMMC 2.0, NIST SP 800-53 | 67 |
| **defense** | 19 (8 check) | OWASP Top 10 2025, OWASP ASVS v5.0, CWE Top 25 | 87 |
| **security** | 20 (6 check) | NIST SP 800-53 Rev 5 (8 families), NIST SP 800-63B | 53 |
| **architect** | 21 (4 check) | Fowler, Richards & Ford, Hohpe & Woolf, SOC2 CC6, RFC 5280/3647 | 26 |
| **test** | 18 (4 check) | xUnit Test Patterns (Meszaros), FIRST Principles, TDD by Example | 23 |
| **perf** | 18 (4 check) | Web Vitals, Lighthouse, MDN Web Performance, HTTP Archive | 16 |
| **prompt-design** | 16 (5 check) | DAIR.AI Guide, OpenAI Guide, Anthropic Guide, Wei et al., Zou et al. | 48 |
| **python-best-practices** | 16 (6 check) | PEP 8, PEP 257, PEP 484, Flake8, Black | 33 |
| **Total** | **167 rules** | **30+ standards cited** | **455 tests** |

---

## How Track Assignment Works

Track is a **function of the capability profile**, never a hardcoded field:

| Condition | Track |
|-----------|-------|
| Unregistered model | `remedial` (conservative — underestimating is safer in education) |
| Unreliable tool calling **OR** context < 8K | `remedial` |
| Reliable multi-step reasoning (≥ 4 steps) **AND** high code-gen across languages | `honors` |
| Everything else | `standard` |

The **8B Booster** activates on a multi-factor working-memory score
`f(context_window, param_count, tool_reliability)` — not a hard parameter line.
Score `< 0.65` → Booster on, following the ZPD principle [Vygotsky 1978]:
less working memory capacity [Miller 1956] gets more scaffolding [Wood et al.
1976]. Honors models never need it — their working memory score exceeds the
threshold.

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
| `tutor profile --model <id>` | Show eval history and per-class pass rates (the metacognitive dashboard). |
| `tutor booster {scratchpad,verify,exemplars,foresee}` | Booster tools for small models (System 2 prosthetics). |

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

## The Eval Harness

Phase 0 ships **Layer 1 only**: a deterministic rules engine that runs on the
core dependency set (stdlib + pydantic). This is deliberate — Layer 1 is
reproducible, fast, and free. Like a multiple-choice test, it's not the deepest
assessment, but it's objective and scalable.

| Layer | Checks | Method | Phase |
|-------|--------|--------|-------|
| 1. Rules Engine | Codifiable rules (WCAG selectors, regex) | Deterministic | **Phase 0 (this build)** |
| 2. LLM Judge | Ambiguous criteria (semantic correctness) | Separate evaluator model, confidence-scored | Future |
| 3. Adversarial | Challenges the judge's own verdict | Same model, different prompt | Future |

Each class's `class.yaml` carries both the teaching examples and the
`check_selector` / `check_regex` that grade them — **no drift between what is
taught and what is tested.** This is assessment validity [Messick 1989]: the
test measures what was taught.

The harness is **authoritative, not infallible.** Its accuracy against human
review is a published metric — the honest position.

---

## Architecture

```
tutor/
├── __main__.py            # single `tutor` console script, argparse subcommands
├── registrar/
│   ├── enroll.py          # track assignment (computed) + Booster threshold
│   ├── state.py           # atomic-write crash-recovery state (~/.tutor/)
│   └── evals.py           # per-model eval history (JSONL, append-only)
├── registry/
│   ├── models.json        # 11 curated capability profiles
│   └── overrides.json     # manual overrides win over auto-sync
├── eval/
│   ├── harness.py         # Layer 1 rules engine (stdlib HTML parser + regex)
│   └── worker_pool.py     # multiprocessing pool (benchmark / MCP path)
├── booster/
│   ├── sandbox.py         # ScratchpadSandbox + SandboxManager (external WM)
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
├── cli/                   # enroll, learn, eval, fix, mcp, list, curriculum, profile, booster
└── classes/               # 9 class directories, each with class.yaml + SOURCES.md
    ├── brushes/           # WCAG 2.2 accessibility
    ├── code-review/       # ITIL v4 / House patterns
    ├── audit/             # SOC2 / HIPAA / CMMC
    ├── defense/           # OWASP Top 10
    ├── security/          # NIST SP 800-53
    ├── architect/         # Fowler / SoD / CP-CPS
    ├── test/              # xUnit / FIRST / TDD
    ├── perf/              # Web Vitals
    └── prompt-design/     # COT / Constitutional AI
```

## Distribution

The **package** is not on PyPI; `git clone && pip install -e .` is primary. Its
**transitive deps** (`mcp`, `pydantic`, `pyyaml`) resolve from PyPI normally.
`requirements.txt` is committed for reproducibility. For truly air-gapped
installs, build the Docker image (`Dockerfile`, multi-stage) — it freezes every
dependency in a layer and needs no further network access.

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `TUTOR_STATE_DIR` | `~/.tutor` | Crash-recovery state directory |
| `TUTOR_CLASS_VENV_DIR` | `~/.tutor/venvs` | Per-class virtual environments |
| `TUTOR_EVAL_POOL_SIZE` | `2` | Worker-pool size |
| `TUTOR_BOOSTER_MAX_CONCURRENT` | `3` | Max concurrent Booster sandboxes |
| `TUTOR_MCP_HEALTH_PORT` | `9090` | Health endpoint port |

---

## References

- **Standards catalog:** [REFERENCES.md](REFERENCES.md) — every standard, framework, paper, and control cited across all 9 classes.
- **Theory references:** [docs/theory.md](docs/theory.md) — full neurobiological foundations with 30+ citations (Hebb, Vygotsky, Kahneman, etc.).

## Contributing

Adding a class is three files: one `class.yaml`, one `SOURCES.md`, one test
file. See [CONTRIBUTING.md](CONTRIBUTING.md). Every class must cite documented
research sources before any code is written — no "because I think so."
