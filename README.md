# lm-tutor — Structured AI Education

**Curriculum-driven training for any language model. No fine-tuning required.**

A single `tutor learn` injection reduces output violations by 64–83% on
mid-to-frontier models — and does so through correct-pattern steering,
not structured prompting (placebo-controlled at 3× the format effect).
The model already knows how to write good code — it just needs steering.

```
Tier     Model              Raw → Class   Reduction
Edge     Gemma 3 4B (4B)             8.7 → 7.7   12%
Mid      DeepSeek V4 Flash (284B/13B MoE)  14.0 → 5.0  64%
High     Claude Sonnet 4.6 (undisclosed)  6.0 → 1.0   83%
Ultra    Claude Opus 4.8 (undisclosed)    8.0 → 3.0   63%
Pro      DeepSeek V4 Pro (1.6T/49B MoE)   15.0 → 0.0  100%
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
- **Covers 30 domains** — accessibility, security, compliance, code review, API
  design, Python style, architecture, prompt design, testing, performance,
  DevOps, and 18 professional credentials (attorney through paramedic).
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

### The effect holds across all capable model tiers

| Model | Tier | Reduction |
|-------|------|-----------|
| Gemma 3 4B | Edge (~72% HumanEval) | -12% |
| DeepSeek V4 Flash | Mid (~85%) | -38% avg, -59% with Booster |
| DeepSeek V4 Pro | Pro | **-100%** (zero violations) |
| Claude Sonnet 4.6 | High | **-83%** |
| Claude Opus 4.8 | Frontier | **-63%** |

Below ~70% HumanEval equivalent, models can't reliably parse structured [RULE]
instructions. Above that floor, injection works consistently — and the effect
is substantial even at the frontier.

### Summary

Injection fixes broken defaults without weight modification. Effect is
placebo-controlled (3× the placebo), holds across 5 model tiers, and
requires a minimum capability threshold (~70% HumanEval). Full methodology at
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
| **credential-pe** | Engineer | NSPE Code of Ethics, IBC, ASCE, state licensure |
| **credential-lcsw** | Therapist | NASW/APA Codes, HIPAA, Tarasoff |
| **credential-journalist** | Journalist | SPJ Code of Ethics, AP Stylebook |
| **credential-finra** | Financial Advisor | SEC, FINRA, Investment Advisers Act |
| **credential-pharmacist** | Pharmacist | DEA, USP 795/797, OBRA '90 |
| **credential-ra** | Architect | AIA Code of Ethics, IBC, ADA |
| **credential-rn** | Registered Nurse | ANA Code of Ethics, NPA, NPSG |
| **credential-pilot** | Pilot | FARs (14 CFR), FAA AIM, PHAK |
| **credential-realtor** | Real Estate Agent | NAR Code of Ethics, Fair Housing Act |
| **credential-pm** | Project Manager | PMBOK 7th Ed, PMP Code, PMI |
| **credential-dentist** | Dentist | ADA Code, CDC/OSHA, DEA |
| **credential-paramedic** | Paramedic/EMT | NREMT, NHTSA EMS Agenda |

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

**Beta.** 30 classes, 487 rules, 1,255+ tests. Benchmarked across 5 model tiers
(Gemma 3 4B through Claude Opus 4.8). Working in production at Ghost Stack.

---

## License

MIT

---

*Built on the idea that models know more than they show. The capability is
there — it just needs steering. — [Miguel Fernandez](https://github.com/mfolofy)*
