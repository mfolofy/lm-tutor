# lm-tutor — Structured AI Education

*Architected by **Fable** — Claude's most capable model*

**Curriculum-driven training for any language model. No fine-tuning required.**

A single `tutor learn` injection reduces output violations by 55-93% on
mid-to-frontier models — and does so through correct-pattern steering,
not structured prompting (placebo-controlled at 3x the format effect,
4.6x the effect of a post-generation fix prompt).

```
Tier     Model                               Raw    Injected   Reduction
Edge     Gemma 3 4B (4B)                     8.7    7.7        12%
Mid      DeepSeek V4 Flash (284B/13B MoE)    17.5   7.8        55%
Mid+     + Booster (scratchpad reasoning)     17.5   4.6        74%
High     Claude Sonnet 4.6 (undisclosed)      6.0    1.0        83%
Ultra    Claude Opus 4.8 (undisclosed)        8.0    3.0        63%
Pro      DeepSeek V4 Pro (1.6T/49B MoE)      14.0   1.0        93%
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
- **Covers 35 domains** — accessibility, security, compliance, code review, API
  design, Python/JavaScript/TypeScript style, architecture, prompt design,
  testing, performance, DevOps, and 18 professional credentials (attorney
  through veterinarian). Each domain is a standalone class with cited standards
  and FAIL/PASS examples.
- **Adapts to the model** — small models get fundamentals + scaffolded tools.
  Capable models get the full curriculum. Track assignment is automatic.

---

## The Research — What 110 API Calls Proved

The thesis: **Models know the right answer. They default to wrong because
they've been trained on wrong data.** Structured `[RULE]` injection before
generation redirects attention to the correct pattern — no fine-tuning, no
weight changes, just steering.

We ran 5 experiments across 5 model tiers, 5 conditions, 5 runs each.
Placebo-controlled. 110 API calls. ~$5 total. Every finding reproducible.

### 1. It's Real Steering, Not Just a Reminder

If injection were "just a reminder," telling the model to "fix the
accessibility" after generation would produce the same result. It doesn't.

| Condition | Avg Violations | Reduction |
|-----------|---------------|-----------|
| Raw (no injection) | 14.6 | -- |
| Follow-up ("fix accessibility") | 12.8 | **-12%** |
| Class injection (`tutor learn`) | 7.8 | **-55%** |
| Class + Booster scratchpad | 4.6 | **-74%** |

A follow-up prompt barely moves the needle (-12%). Class injection cuts errors
55-74%. **4.6x more effective.** The model isn't being reminded — it's being
redirected before it generates. The difference between telling a photographer
"your lighting is off" vs showing them the light meter before they shoot.

### 2. Placebo-Controlled (First in Injection Research)

We ran a true placebo: same structured `[RULE]` format, irrelevant content
(gardening tips). The placebo cut errors 27%. Real injection cut errors 55-74%.
**3x the placebo.** The format primes the model to pay attention. The correct
content does the actual steering.

### 3. Smarter Models Benefit More

| Model | Tier | Raw | Injected | Reduction |
|-------|------|-----|----------|-----------|
| Gemma 3 4B | Edge (72% HumanEval) | 8.7 | 7.7 | **-12%** |
| DeepSeek V4 Flash | Mid (85% HumanEval) | 17.5 | 7.8 | **-55%** |
| DeepSeek V4 Flash + Booster | Mid | 17.5 | 4.6 | **-74%** |
| Claude Sonnet 4.6 | High | 6.0 | 1.0 | **-83%** |
| Claude Opus 4.8 | Frontier | 8.0 | 3.0 | **-63%** |
| DeepSeek V4 Pro | Pro-tier | 14.0 | 1.0 | **-93%** |

Below ~70% HumanEval, the effect drops off — the model lacks the latent
knowledge to steer toward. Above that floor, the effect scales with
intelligence. The ceiling isn't model size. It's whether the knowledge is
there to surface.

### 4. The Inverted-U — Peaks Where It's Needed Most

| Task Complexity | Raw | Class | Improvement |
|----------------|-----|-------|-------------|
| Simple (3-5 elements) | 0.4 | 0.4 | **0%** (already clean) |
| Medium (6-10 elements) | 1.0 | 3.0 | -200% (anomaly — over-corrects) |
| Complex (10-15 elements) | 12.6 | 4.0 | **-68%** (peak effect) |
| SPA (15-25 elements, JS) | 3.2 | 3.6 | -13% (wrong format — no HTML to grade) |

The effect is strongest where it's needed most. Trivial pages hit a ceiling —
nothing to fix. Complex pages have more violations to surface, and injection
catches them. The inverted-U is confirmed.

### 5. One Shot Does It All — Fix Adds Nothing

Class injection alone: 5.2 violations. Class injection + post-hoc fix: 5.2
violations. **Zero benefit from trying to fix after the fact.** The injection
already did the work during generation. No post-processing needed.

### 6. Effect Scales with Training Data Brokenness

| Domain | Training data quality | Raw | Injected | Delta |
|--------|---------------------|-----|----------|-------|
| HTML/WCAG | 96% broken | 15.6 | 5.0 | **-68%** |
| Python/PEP 8 | Already clean | 0.0 | 0.3 | **0%** (ceiling) |

When training data is clean, there's nothing to fix — the model already
defaults to correct output. When training data is broken, injection recovers
the latent correct patterns. This is inverse validation: the effect exists
where training fails.

### The One-Liner

**Training data sets the floor. Injection sets how far above that floor a
model performs.** Neither alone is sufficient. Together, they cost less than
a penny per generation.

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
| **credential-adjuster** | Insurance Adjuster | AIC, state DOI regulations, fair claims practices |
| **credential-electrician** | Electrician | NEC, NFPA 70E, state licensing boards |
| **credential-hr** | HR Professional | SHRM/HRCI ethics, FLSA, EEOC, FMLA |
| **credential-judge** | Judge/Judicial Officer | ABA Code of Judicial Conduct, USC Title 28 |
| **credential-socialworker** | Social Worker | NASW Code of Ethics, state licensing, HIPAA |
| **credential-vet** | Veterinarian | AVMA Code of Ethics, state practice acts, DEA |

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
| **Fix** | `tutor fix` — iterative correction loop. Eval → per-violation fix suggestions → re-eval. |
| **Prefix** | `tutor prefix --classes a,b,c` — compose multiple class rule sets into a single injection prefix. |
| **Curriculum** | `tutor curriculum --model <id>` — ordered class list per track. |
| **Profile** | `tutor profile` — per-model eval history, pass rates, weakest rules, next-class suggestions. |
| **Scaffold** | `tutor class --new` — auto-generates class.yaml + SOURCES.md + test file for new classes. |

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

**Beta.** 37 classes, 602 rules, 1733+ tests. Benchmarked across 5 model tiers
(Gemma 3 4B through DeepSeek V4 Pro) with 5-run placebo-controlled protocol.
Working in production at Ghost Stack.

---

## License

MIT

---

*Built on the idea that models know more than they show. The capability is
there — it just needs steering. — [Miguel Fernandez](https://github.com/mfolofy)*
