# lm-tutor — Structured AI Education

**Curriculum-driven training for any language model. No fine-tuning required.**

A single `tutor learn` injection reduces output violations by 54% on broken
training data — 3.8× more than a placebo injection with the same format but
irrelevant rules. The model already knows how to write good code — it just
needs a reminder at the right moment.

```
  Raw generation:   15.6 violations  (baseline)
  Placebo (wrong rules, same format):  13.4  (-14%)
  After injection:   7.2 violations  (-54%)
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
- **Covers 11 domains** — accessibility, security, compliance, code review, API
  design, Python style, architecture, prompt design, testing, performance.
  Each domain is a standalone class with cited standards and FAIL/PASS examples.
- **Adapts to the model** — small models get fundamentals + scaffolded tools.
  Capable models get the full curriculum. Track assignment is automatic.

---

## Findings

Benchmarked against WCAG 2.2 accessibility rules (brushes class) using a
deterministic 38-rule evaluator. 5-run averages. Placebo-controlled.

### Injection works — and it's not just structured prompting

| Condition | Violations | vs Raw |
|-----------|-----------|--------|
| Raw (no injection) | 15.6 | -- |
| Placebo (gardening rules, same format) | 13.4 | -14% |
| Class (correct [RULE] injection) | 7.2 | **-54%** |

The placebo control (irrelevant gardening rules in identical `[RULE]` format)
produced 14% reduction. The real injection produced 54% — 3.8× the placebo.
The format alone is not the mechanism. The content is.

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
