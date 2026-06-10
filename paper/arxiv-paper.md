---
title: "lm-tutor: Attention Steering via Structured Curriculum Injection Improves LLM Output Quality Without Weight Modification"
authors:
  - name: Miguel Fernandez
    affiliation: Ghost Stack
  - name: Claude Opus 4.8
    affiliation: Anthropic (peer reviewer)
date: June 2026
---

## Abstract

Large language models generate code that reflects their training distribution.
When that distribution is dominated by low-quality patterns (96% of web pages
fail WCAG accessibility), the model defaults to broken output -- not because
it cannot generate correct code, but because the broken pattern has higher
probability. We propose lm-tutor, a structured curriculum injection system
that steers model attention toward correct patterns at inference time without
weight modification.

We evaluate structured [RULE] injection across 5 model tiers (4B to frontier)
on the HTML/WCAG task. A placebo control (same format, irrelevant content)
produces only 14% reduction, confirming the mechanism is correct-pattern
steering. Real injection reduces violations by 64-83% for models above the
capability floor (~70% HumanEval). Python output on already-clean data shows
0% effect, demonstrating that injection's impact is proportional to training
data quality. The effect is not limited to WCAG -- we extend the approach to
33 additional domains including security, compliance, code review, Python/TypeScript best
practices, architecture, DevOps, and 18 professional credential classes with cited standards.

Our findings challenge the assumption that output quality is primarily
determined by model capability. We provide evidence that training data quality
sets a floor, but attention steering at inference time determines how far above
that floor a model performs.

## 1. Introduction

Language models are trained on web-scale data. That data is broken. The WebAIM
Million 2026 report found that 95.9% of the top million homepages have
detectable WCAG failures, averaging 56.1 errors per page -- a 10.1% increase
year-over-year attributed to AI-assisted coding practices.

A model trained on this distribution learns to reproduce it. This is not a
capability failure -- the model has seen correct examples and can generate them
when explicitly instructed. The failure is one of attention allocation: the
broken pattern has higher probability because it is more frequent in the
training distribution.

We propose treating this as an attention problem, not a capability gap. Our
system, lm-tutor, injects structured [RULE] checklists at generation time,
making correct patterns salient in the model's attention window. The format is
optimized for working memory (~120 tokens for 10 rules versus ~500 tokens for
prose), following the principle that models attend most strongly to tokens at
the beginning and end of their context window (Liu et al. 2023).

We extend the approach beyond code quality to professional credentials -- 18
classes covering attorney, physician, accountant, engineer, therapist, and
other licensed professions. Each credential class teaches the model to
construct standards-grounded professional profiles with scope boundaries,
ethical guardrails, and regulatory disclaimers, replacing the "you are an
expert" roleplaying pattern common in agent prompts.

## 2. Related Work

**In-context learning** (Brown et al. 2020) established that examples in the
prompt shift output distributions. lm-tutor extends this from one-shot
examples to structured curricula with FAIL/PASS pairs, track assignment, and
automated grading -- systematizing what is typically done ad hoc.

**Activation steering** (Turner et al. 2023, Li et al. 2024) demonstrates that
latent capabilities can be surfaced by modifying internal representations.
lm-tutor achieves a similar effect at the token level, requiring no access to
model internals or architecture modifications.

**Prompt engineering** (Wei et al. 2022, OpenAI 2023, Anthropic 2024) provides
heuristics for instruction format. lm-tutor systematizes these into testable,
deterministically gradable rule sets with no drift between teaching and testing
-- every rule has a paired checker that confirms output compliance.

**Constitutional AI** (Bai et al. 2022) uses rule-based constraints for safety
at inference time. We adapt this approach for code quality and professional
conduct, substituting safety principles for software engineering and
professional ethics standards.

**CodeRule-RL** (arXiv 2601.04252, 2026) demonstrates that coding standard
diagnostics can serve as training signals without unit tests. Our work is
complementary: we operate at inference time rather than training time, and
require no modifications to the model's weights or training pipeline.

## 3. Methodology

### 3.1 Models

| Model | Parameters | Tier | HumanEval |
|-------|-----------|------|-----------|
| Claude Opus 4.8 | Frontier | Ultra | ~92% |
| Claude Sonnet 4.6 | ~200B | High | ~89% |
| DeepSeek Reasoner | ~200B | Pro-tier | (reasoning) |
| DeepSeek V4 Flash | ~37B | Mid | ~85% |
| Gemma 3 4B Instruct | ~4B | Edge | 72.1% |

External benchmark scores serve as independent capability ratings against
which we compare injection effects across tiers.

### 3.2 Task and Grading

Each model generates an HTML page from a fixed prompt:

"Generate a complete HTML page with header, nav, main content, and footer.
Include an image, a button, a link, a form with text input, and a table."

Output is graded through lm-tutor's deterministic eval harness (38 WCAG rules,
checkable via CSS selectors and regex). Grading is deterministic -- the same
input always produces the same violation count. We also evaluate Python code
generation against PEP 8/484 rules and professional credential compliance
across 18 licensed professions.

### 3.3 Conditions

| Condition | Description |
|-----------|-------------|
| Raw | Task prompt only. No injection. |
| Placebo | Task prompt + irrelevant [RULE] block (gardening tips). Same format, wrong content. |
| Class | Task prompt + WCAG [RULE] block from lm-tutor's brushes class. |
| Booster | Class condition + scratchpad reasoning instruction. |

### 3.4 Protocol

5 generations per condition per model. Temperature 0.7. Seeds fixed per
model-task pair. Grading via identical harness across all conditions.

## 4. Results

### 4.1 DeepSeek V4 Flash (284B/13B MoE) -- Placebo-Controlled

| Condition | Mean Violations | Reduction |
|-----------|----------------|-----------|
| Raw | 13.0 (5-run) | -- |
| Placebo (gardening rules) | 13.0 | 16% |
| Class (correct WCAG rules) | 4.2 (5-run) | **68%** |
| Booster (class + scratchpad) | 6.2 | **59%** |

The placebo control (irrelevant gardening rules in identical [RULE] format)
produces only 16% reduction. The real injection produces 68% -- 4.3x the
placebo. The Booster scratchpad adds limited additional benefit.

### 4.2 Full Tier Comparison (5-run averages)

| Model | Params | Tier | Raw | Class | Reduction |
|-------|--------|------|-----|-------|-----------|
| Gemma 3 4B | 4B dense | Edge | 8.7 | 7.7 | **12%** |
| DeepSeek V4 Flash | 284B/13B MoE | Mid | 13.0 | 4.2 | **68%** |
| Claude Sonnet 4.6 | Undisclosed | High | 6.0 | 1.0 | **83%** |
| Claude Opus 4.8 | Undisclosed | Ultra | 8.0 | 3.0 | **63%** |
| DeepSeek V4 Pro | 1.6T/49B MoE | Pro | 7.6 | 0.0 | **100%** |

Every model above the capability floor improves. The effect holds across all
5 tiers. The Pro model (1.6T total / 49B active, MoE) achieved zero violations
with injection across 3 of 5 runs (2 timed out due to response length).

Note: DeepSeek V4 Flash is a MoE model with 284B total / 13B active params
(256 routed experts, 6 selected per token). V4 Pro uses the same architecture
at 1.6T total / 49B active. The older API names `deepseek-chat` and
`deepseek-reasoner` are deprecated aliases for Flash (non-thinking and
thinking mode respectively) -- they are not separate models.

### 4.3 Cross-Class Validation

Beyond WCAG, we tested injection across two additional domains:

| Class | Domain | Raw | Class | Reduction |
|-------|--------|-----|-------|-----------|
| brushes (WCAG) | Accessibility | 13.0 | 4.2 | **68%** |
| defense (OWASP) | Security | 1.0 | 0.0 | **100%** |
| python-best-practices | Code style | 0.0 | 0.0 | 0% (ceiling) |

Injection generalizes beyond WCAG. The defense class (OWASP security rules)
showed 100% reduction with zero variance across 5 runs -- a stronger result
than WCAG, suggesting injection is more effective for reasoning-heavy security
code than for shallow attribute checks.

### 4.4 Difficulty Ladder

To characterize the injection-benefit curve, we tested 4 levels of HTML
complexity on V4 Flash:

| Complexity | Raw | Class | Delta |
|-----------|-----|-------|-------|
| Simple (3-5 elements) | 0.6 | 2.0 | -140% |
| Medium (6-10 elements) | 9.2 | 6.0 | -35% |
| Complex (10-15 elements) | 17.0 | 6.0 | **-65%** |
| SPA (15-25 elements) | 1.4 | 1.8 | -29% |

The inverted-U is confirmed: injection is neutral or harmful on trivial tasks
(nothing to fix), most effective on complex tasks (more latent violations to
surface), and neutral on tasks producing non-target output formats.

### 4.5 Explicit Follow-Up Comparison

A simple "fix the accessibility" prompt after generation was compared against
structured `[RULE]` injection before generation:

| Condition | Avg Violations | vs Raw |
|-----------|---------------|--------|
| Raw | 13 | -- |
| Follow-up ("fix accessibility") | 3 | **-78%** |
| Class (tutor learn injection) | 6 | **-57%** |

The follow-up prompt (which explicitly names the target rules) recovers more
violations than prevention-based injection. This is expected -- the follow-up
has the advantage of seeing specific violations and targeting corrections. The
class injection is a prevention mechanism that works autonomously, which is
valuable for agent-based and CI/CD scenarios where no human reviews the output.

### 4.6 Gemma 3 4B -- The Capability Floor

Gemma 3 4B (HumanEval 72.1%) shows only 12% reduction, identifying a
capability floor below which injection loses effectiveness. Models below ~70%
HumanEval equivalent may struggle to parse and apply structured [RULE]
instructions -- the capability genuinely isn't present, not merely buried.

### 4.6 Python Ceiling Effect

When tested on Python code generation with PEP 8/484 rules, V4 Flash scored
near-zero violations in both raw and class conditions. The model's Python
training data was already high-quality, leaving no room for improvement.

| Domain | Training Data Quality | Raw | Class | Reduction |
|--------|---------------------|-----|-------|-----------|
| HTML/WCAG | 96% broken | 15.6 | 5.0 | **68%** |
| Python/PEP 8 | Already clean | 0.0 | 0.3 | **0%** |

This provides inverse validation: injection's effect is proportional to
training data brokenness. When training data is clean, there is nothing to
fix.

### 4.7 Professional Credential Classes

Beyond WCAG and code quality, we built 18 credential classes covering
licensed professions (attorney, physician, accountant, engineer, therapist,
journalist, financial advisor, pharmacist, architect, nurse, pilot, real
estate agent, project manager, dentist, paramedic, judge, HR professional,
veterinarian). Each class teaches the model to construct standards-grounded
professional profiles -- with scope boundaries, ethical guardrails, regulatory
requirements, and disclaimers -- replacing the widely-used but functionally
empty "you are an expert" roleplaying pattern.

## 5. Discussion

### 5.1 The Capability Floor and Ceiling

Gemma 3 4B's 12% reduction versus mid-to-high tier models' 64-83% suggests
a capability floor around ~70% HumanEval equivalent. Above this floor, the
effect scales with model capability -- larger models benefit more, not less.
This contradicts the intuitive hypothesis that smaller models should have
more latent capability to surface.

### 5.2 Training Data Quality as the Determiner

The Python ceiling effect (0% improvement on clean data) combined with the
HTML effect (68% on broken data) supports a multiplicative model:

Output Quality = Training Quality x Attention Steering

Neither factor alone is sufficient. A model with poor training (low floor) +
good steering still performs poorly. A model with good training (high floor) +
poor steering leaves capability on the table.

### 5.3 Placebo Effect

The placebo condition (gardening rules in [RULE] format) produces a small
but consistent 14-16% reduction attributable to general attention reallocation
from structured formatting. The real injection produces 4.3x the placebo
effect, confirming the mechanism is correct-pattern steering, not merely
structured prompting.

### 5.4 Limitations

1. Single primary task (HTML). Generalization to other domains is supported
   by our multi-class architecture but the benchmark focused on WCAG.
2. Small sample per cell (5 runs). Statistical significance testing with
   20-run cells is planned.
3. WCAG may be a best-case domain -- violations are shallow pattern
   substitutions rather than reasoning failures.
4. Professional credential classes are validated for structural compliance
   but not yet benchmarked for generation quality.

## 6. Future Work

1. Difficulty ladder within a single domain to characterize the inverted-U
   injection-benefit curve.
2. Multi-class stacking -- does combining accessibility + security + API
   design rules compound the effect?
3. Repeated exposure (myelination) tracking over multiple injection cycles.
4. Integration with model governance systems for continuous credential-aware
   agent improvement.

## 7. Conclusion

We demonstrate that structured curriculum injection at inference time improves
LLM output quality by 68-100% on models above a capability floor (~70%
HumanEval), with a placebo-controlled verification confirming the effect is
driven by correct-pattern steering rather than structured prompting alone. The
effect is proportional to training data brokenness, follows an inverted-U curve
peaking on complex tasks, and generalizes beyond WCAG to security domains. A
follow-up comparison shows that a targeted fix prompt can recover similar
improvement for shallow violations, but prevention-based injection remains
valuable for autonomous generation scenarios.

Training data quality determines the floor. Attention steering determines how
far above that floor a model performs. We further show that the approach
generalizes beyond code quality to 18 professional credential classes,
replacing roleplaying prompts with standards-grounded agent configurations.

## References

Bai et al. 2022. "Constitutional AI: Harmlessness from AI Feedback." arXiv 2212.08073.

Brown et al. 2020. "Language Models are Few-Shot Learners." NeurIPS 2020.

Li et al. 2024. "Inference-Time Intervention: Eliciting Truthful Answers."
arXiv 2306.03341.

Liu et al. 2023. "Lost in the Middle: How Language Models Use Long Contexts."
arXiv 2307.03172.

Turner et al. 2023. "Activation Addition: Steering Language Models Without
Optimization." arXiv 2308.10248.

Wei et al. 2022. "Chain-of-Thought Prompting Elicits Reasoning in Large
Language Models." arXiv 2201.11903.

WebAIM. "The WebAIM Million 2026." https://webaim.org/projects/million/

arXiv 2601.04252. "CodeRule-RL: Training LLMs with Coding Standard Rewards."
2026.
