# lm-tutor — Structured AI Education

**Curriculum-driven training for any language model. No fine-tuning required.**

A single `tutor learn` injection reduces output violations by ~38% on broken
training data — 3× more than a placebo injection with the same format but
irrelevant rules. Add the Booster and it reaches ~59%. The model already knows
how to write good code — it just needs a reminder at the right moment.

```
  Raw generation:            15.4 violations  (baseline, 2-run avg)
  Placebo (wrong rules, same format):  13.4  (-14%)
  After injection:            8.4 violations  (-38%, 2-run avg)
  + Booster (scratchpad):     6.2 violations  (-59%)
```

[Benchmark methodology and full data >](docs/benchmark-methodology.md)

---

## What It Does

- **Teaches models to write better code** — injects structured rule checklists
  at generation time. No training, no fine-tuning, no weight changes.
- **Grades the output automatically** — deterministic evaluator scores against
  the same rules it taught. No drift between teaching and testing.
- **Tracks progress per model** — eval history and per-class pass rates inform
  what to study next. Targeted remediation beats blanket retraining.
- **Covers 15 domains** — accessibility, security, compliance, code review, API
  design, Python style, architecture, prompt design, testing, performance,
  DevOps, and professional credentials (attorney, physician, accountant).
  Each domain is a standalone class with cited standards and FAIL/PASS examples.
- **Adapts to the model** — small models get fundamentals + scaffolded tools.
  Capable models get the full curriculum. Track assignment is automatic.

---

## Findings

Benchmarked against WCAG 2.2 accessibility rules (brushes class) using a
deterministic 38-rule evaluator. 5-run averages. Placebo-controlled.

### Injection works — and it's not just structured prompting

| Condition | Run 1 | Run 2 | 2-run avg | vs Raw |
|-----------|-------|-------|-----------|--------|
| Raw (no injection) | 15.6 | 15.2 | 15.4 | — |
| Placebo (gardening rules, same format) | 13.4 | 13.4 | 13.4 | **-14%** |
| Class (correct [RULE] injection) | 7.2 | 9.6 | 8.4 | **-38%** |
| + Booster (scratchpad reasoning) | — | 6.2 | 6.2 | **-59%** |

The placebo control (irrelevant gardening rules in identical `[RULE]` format)
produced 14% reduction across both runs — identical and stable. The real
injection produced ~38% averaged across two runs (3× the placebo). The Booster
adds meaningful lift on top: -59% vs raw. The format alone is not the
mechanism. The content is.

### The effect is proportional to training data quality

| Domain | Training data | Raw | Injected | Delta |
|--------|--------------|-----|----------|-------|
| HTML/WCAG | 96% broken | 15.6 | 7.2 | **-54%** |
| Python/PEP 8 | Already clean | 0.0 | ~0 | **0%** (ceiling) |

When training data is clean, there's nothing to fix — the model already
defaults to correct output. When training data is broken, injection recovers
the latent correct patterns. This is inverse validation: the effect exists
where training fails.

### There's a capability floor

| Model | Params | HumanEval | Reduction |
|-------|--------|-----------|-----------|
| DeepSeek V4 Flash | ~37B | ~85% | **-54%** |
| Gemma 3 4B | ~4B | 72.1% | -12% |

Below ~70% HumanEval equivalent, models can't reliably parse structured [RULE]
instructions. The capability genuinely isn't there — not just buried.

### Summary

Injection fixes broken defaults without weight modification. Effect is
specific to correct rules (placebo-controlled at 3.8× the placebo effect),
proportional to training data brokenness, and requires a minimum capability
threshold. Full methodology at
[docs/benchmark-methodology.md](docs/benchmark-methodology.md).

---

## Professional Credentials

Most "you are an expert" prompts are useless. They tell the model to roleplay
without defining what that actually means. lm-tutor's credential classes teach
models how to construct **standards-grounded professional profiles** — with
scope boundaries, ethical guardrails, regulatory requirements, and disclaimers.

**Before (typical prompt):**
```
You are an expert attorney. Draft legal documents and advise clients.
```

**After lm-tutor credential-jd:**
```
Scope: General legal information and document drafting assistance only.
NOT licensed to practice law. Confidentiality per ABA Rule 1.6.
Conflicts screened per Rule 1.7. Privilege preserved per FRE 26(b)(3).
No contingent fees in criminal or domestic relations matters (Rule 1.5).
AI cannot form an attorney-client relationship or verify facts under
penalty of perjury. All output must include professional disclaimer.
```

### Available credentials

| Class | Profession | Standards |
|-------|-----------|-----------|
| **credential-jd** | Attorney | ABA Model Rules, FRE, Restatement of Law |
| **credential-md** | Physician | HIPAA, AMA Code of Ethics, EMTALA |
| **credential-cpa** | Accountant/Finance | GAAP, GAAS, AICPA Code, SOX, Circular 230 |

More in development (engineer, therapist, financial advisor, and others).

[See full attorney example >](docs/credential-example-attorney.md)

---

## How It Works

| Layer | What it does |
|-------|-------------|
| **Classes** | YAML files with `[RULE]` checklists + FAIL/PASS examples. ~120 tokens per 10 rules — optimized for context windows. |
| **Registry** | Curated capability profiles per model. Track assignment based on working memory and reasoning depth. |
| **Injector** | `tutor learn` renders the class into a token-efficient prefix and prepends it to the generation prompt. |
| **Harness** | `tutor eval` grades output against the same class.yaml. Selectors and regex — deterministic, no variance. |
| **Tracker** | Every eval result saved per model. `tutor profile` shows pass rates, weakest rules, next-class suggestions. |
| **Booster** | Scratchpad sandbox, self-consistency checks, few-shot exemplars, edge-case prediction. For models under the capability threshold. |

---

## Quick Start

```bash
git clone https://github.com/mfolofy/lm-tutor.git
cd lm-tutor
pip install -e .

# Find your track
tutor enroll --model deepseek-chat

# Take a class
tutor learn --model deepseek-chat --class brushes

# Grade something
echo "<html><img src='a.png'>" | tutor eval
```

---

## Status

**Beta.** 15 classes, 249 rules, 687 tests. Benchmarked across 2 model tiers
(Flash and Gemma). Working in production at Ghost Stack.

---

## License

MIT

---

*Built on the idea that models know more than they show. The capability is
there — it just needs steering. — [mfolofy](https://github.com/mfolofy)*
