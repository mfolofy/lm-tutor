# ML Curriculum Design — lm-tutor (The School for LLMs)

**Author:** Mike (Claude Code / claude-sonnet-4-6) acting as ML engineer
**Date:** 2026-06-08
**Status:** DESIGN — ready for implementation
**Addresses:** ML review findings against SCOPE.md

---

## Table of Contents

1. [Core Thesis Reframe](#1-core-thesis-reframe)
2. [Benchmark Methodology and Target Setting](#2-benchmark-methodology-and-target-setting)
3. [Eval Harness Architecture](#3-eval-harness-architecture)
4. [Class Content Format](#4-class-content-format)
5. [Constrained Decoding Integration](#5-constrained-decoding-integration)
6. [Honors Track Validation](#6-honors-track-validation)
7. [Booster Threshold Design](#7-booster-threshold-design)
8. [Model Registry: Capability Flags Over Tier](#8-model-registry-capability-flags-over-tier)

---

## 1. Core Thesis Reframe

### What the SCOPE says

> Web data is full of bad practices -> models trained on it reproduce bad practices -> injecting corrective knowledge at generation time fixes this.

### What's wrong with it

The causal chain has a missing link. The WebAIM statistic (95.9% of homepages have WCAG failures) proves that the *training distribution* is skewed toward inaccessible patterns. But it does not prove that models *cannot* produce accessible output. It only proves that models *usually do not* produce accessible output when prompted generically.

The pre-training literature (Brown et al., 2020; Wei et al., 2022; Min et al., 2022) shows that LLMs absorb far more patterns than they surface under naive prompting. A model that has seen 10,000 accessible pages among 1,000,000 total pages has learned accessible patterns — they are just low-probability in the output distribution without steering. The failure is one of **retrieval and attention allocation**, not capability absence.

### Corrected thesis

> **Models internalize both correct and incorrect patterns during pre-training. Without steering, the output distribution reflects the training distribution (mostly wrong). The School surfaces the correct patterns through structured, token-efficient injection — making them salient in the attention window at generation time.**

This shift has concrete architectural implications:

| Old frame (broken data) | New frame (retrieval/attention) | Architecture implication |
|---|---|---|
| "Fix the model's knowledge" | "Surface the model's latent knowledge" | Class format must be optimized for attention, not for teaching |
| Fine-tuning would be ideal but impractical | Inference-time injection is *correct by design* | No temptation to add SFT/RLHF later |
| Booster adds capability the model lacks | Booster compensates for limited working memory | Booster effectiveness diminishes as model scale increases (expected) |
| Any improvement proves the concept | Baseline without injection matters | Mandatory baseline: model + well-crafted system prompt, no School |

### The baseline that must be measured

The review's key empirical question: *can you elicit correct behavior from a small model using only a well-crafted system prompt, without the Booster?*

**Design:** Before any class runs, every model gets a "best-prompt baseline":

```
System: You are generating [output type]. Follow these rules:
        - [RULE 1, RULE 2, ... all 20 rules in 200 tokens]

User: [task]
```

This is the *minimum intervention*. If it already achieves 40% violation reduction, then the School's class content is doing something different from "just telling the model the rules." If it achieves 5%, the School's format adds real value. The baseline must be published alongside all results.

### What this means for Phase 0 benchmarking

The Phase 0 benchmark must include these conditions:

| Condition | What it measures | Purpose |
|-----------|-----------------|---------|
| 1. Raw model, no injection | Baseline failure rate | "This is where we start" |
| 2. Model + best system prompt | Minimum intervention ceiling | "What does just telling the rules do?" |
| 3. Model + class injection | School effect | "What does structured curriculum add?" |
| 4. Model + class + Booster | Full system | "What does the complete stack do?" |

The SCOPE's Phase 0 mentions "4 models x 5 tasks x 3 runs" but doesn't specify these conditions. Add them as a 4th axis (conditions). This makes it 4x5x3x4 = 240 cells. At 10 runs/cell, that's 2,400 evaluations. Manageable for automated runs.

---

## 2. Benchmark Methodology and Target Setting

### The target: what the review said

> 15-20% is under-ambitious. The ceiling is 40-60% for targeted violations.

**Decision: 15-20% is the MINIMUM VIABLE EFFECT. 40-60% is the ASPIRATIONAL TARGET.** Both are published. Phase 0 targets the minimum to validate the approach. Phases 1-3 target the aspirational ceiling.

### Statistical methodology

#### Why 3 runs (SCOPE) is insufficient

LLM outputs at temperature > 0 have high variance. Even temperature=0 has variance from:
- CUDA non-determinism (kernel launches, atomics)
- TF32 rounding differences across GPU architectures
- API-side load balancing across different model replicas

**Minimum: 10 runs per cell. Target: 20 runs per cell for primary metrics.**

#### Cell definition

A **cell** is (model, task, condition, class) — one configuration evaluated N times.

- Models: 4 (Phase 0: DeepSeek V4 Flash, Gemma 8B, Llama 4 8B, GPT-4o-mini)
- Tasks: 5 (Phase 0: HTML page, React component, JSON API response, SVG graphic, Markdown doc)
- Conditions: 4 (raw, best-prompt, class-injected, class+booster — see above)
- Classes: 1 (Phase 0: brushes/accessibility)
- Total cells: 4 x 5 x 4 x 1 = 80
- Runs per cell: 20 for primary, 10 for exploratory
- Total evaluations: 80 x 20 = 1,600

#### Reporting

Per cell:
- **Mean violation count** (n = 20)
- **Standard deviation**
- **95% confidence interval** (bootstrap with 10,000 resamples — no normality assumption)
- **Effect size** (Cohen's d relative to baseline condition)

Per model (aggregated across tasks):
- **Mean + CI across all tasks**
- **Relative reduction**: `(baseline - treatment) / baseline * 100`
- **Pass rate**: percentage of runs with zero fundamental violations

#### Statistical significance

**Method:** Bootstrap hypothesis test (10,000 resamples). Two conditions are different if the 95% CI of their difference does not include zero.

**Why not Mann-Whitney U / t-test:** LLM violation counts are not normally distributed (zero-inflated, bounded at 0). Bootstrap is distribution-free and handles this correctly.

**Correction for multiple comparisons:** Benjamini-Hochberg false discovery rate (FDR) correction across all cell comparisons. Report both raw and adjusted p-values.

**Minimum detectable effect:** With n=20 per cell, alpha=0.05 (FDR-corrected), 80% power, the minimum detectable effect is approximately d = 0.35 (Cohen's d). For a baseline of 40% violations, this means detecting a reduction to ~30% (10 percentage points, 25% relative reduction). This is sufficient for Phase 0.

#### Temperature policy

- **Primary metric:** temperature = 0.7 (standard generation default).
- **Ablation:** temperature = 0.0 for 5 runs per cell to measure determinacy ceiling.
- Both reported separately. Never averaged together.

Rationale: temperature = 0.7 reflects real usage. temperature = 0.0 tells us what's possible with greedy decoding. The difference between them is a measure of the model's stochasticity penalty.

#### Sampling seed policy

- Fixed seed per model per task (not per run). This ensures that the 20 runs differ due to sampling stochasticity, not seed-dependent prompt sensitivity.
- Seeds are predetermined and published: `seed = hash(model_id + task_name) % 2**32`.

#### Model update drift mitigation

- **Timestamps on all results.** Every evaluation record includes the model API version (if available) and wall-clock timestamp.
- **Benchmark versioning.** The benchmark has a version number. A model update that changes results increments the version. Old results are archived, not deleted.
- **Sliding window.** Published leaderboard shows "last 30 days" and "all time."

### Aspirational target methodology

For Phase 1+ when classes are content-rich:

- **Stratified sampling by violation type.** Instead of reporting a single "violation reduction" number, report per WCAG criterion (or per OWASP category, etc.). A class that eliminates 100% of color contrast violations but has zero effect on ARIA failures should show both numbers, not a smoothed average.
- **Per-class pass/fail gate.** Each class must demonstrate statistically significant improvement on its target violation type before the next class unlocks. This prevents the curriculum from progressing a model that hasn't actually learned anything.

---

## 3. Eval Harness Architecture

### The problem (from the review)

> The regress problem: who evaluates the evaluator? "Independent process, no shared state" prevents cheating but doesn't prevent correlated errors. If the same training data corrupted both the student and the evaluator, they agree on wrong answers.

### Decision: Hybrid three-layer architecture

```
Submission
    |
    v
[Layer 1: Rules Engine]  ---> deterministic pass/fail on codifiable rules
    |                              |
    | pass                         | fail -> violations recorded
    v                              v
[Layer 2: LLM Judge]      ---> scores ambiguous criteria, publishes confidence
    |                              |
    | pass & high conf             | low conf / fail / disagreement
    v                              v
[Layer 3: Adversarial]    ---> challenges own verdict, catches self-consistency errors
    |                              |
    | pass                         | fail
    v                              v
VERIFIED PASS              HUMAN REVIEW QUEUE
```

### Layer 1: Rules Engine

**What it checks:** Codifiable, deterministic rules that can be expressed as:
- XPath/CSS selector queries (e.g., "every `<img>` must have `alt` attribute")
- HTML validation (via `html-validate` or a subset of axe-core rules)
- AST patterns (e.g., "every `useEffect` must have dependency array")
- Regex patterns (e.g., "no hardcoded API keys matching `sk-[A-Za-z0-9]+`")
- Color contrast (WCAG 2.1 AA: ratio >= 4.5:1 for normal text)
- JSON schema validation

**How rules are written:**

1. Human expert authors rule in YAML (see class format below).
2. Rule is verified against a test suite of 10 known-passing and 10 known-failing examples.
3. Only after verification does the rule enter the production evaluator.
4. Rules are committed with their test suite. Adding a rule = adding tests.

**Rule schema:**

```yaml
rule_id: wcag-1.1.1-nontext-content
criterion: WCAG 2.1 Level A 1.1.1
description: All non-text content must have text alternative
severity: fundamental
check_type: selector
selector: img:not([alt]), img[alt=""]
# also: input[type="image"]:not([alt]), area:not([alt])
pass_when: selector returns 0 matches
```

```yaml
rule_id: security-owasp-02
criterion: OWASP Top 10 2025 A02 - Broken Authentication
description: Hardcoded API keys in source
check_type: regex
pattern: (?:sk-[A-Za-z0-9]{20,}|api[-_]?key\s*[:=]\s*['\"][A-Za-z0-9]{16,})
severity: blocker
pass_when: pattern returns 0 matches
```

**Coverage expectation for Phase 0:** ~30-40 rules covering ~40-50% of WCAG 2.1 A/AA criteria. This is the honest number. The remaining criteria require human judgment (e.g., "is the error message helpful?") and are deferred to Layer 2.

**Why rules-first, not LLM-first:** Determinism. A rules engine produces the same verdict every time. This means:
- Benchmark results are reproducible across runs.
- A model cannot "argue" its way out of a violation.
- The rules engine's accuracy can be measured against a held-out test set.
- If the rules engine makes an error, it's a bug, not a disagreement — it can be fixed with a commit.

### Layer 2: LLM Judge

**What it checks:** Criteria that cannot be expressed as code:
- Semantic correctness ("does this error message actually describe the problem?")
- Visual affordance judgment ("is this interactive element visually distinguishable?")
- Logical completeness ("does this form handle all specified edge cases?")

**Which model:** A separate, larger evaluator model — specifically **not** the same family as the student model to avoid correlated errors.

| If student is | Evaluator is | Rationale |
|---------------|-------------|-----------|
| DeepSeek V4 Flash | Claude Opus 4.8 (or GPT-5) | Different training distribution. An error both models make is unlikely to be coincidental. |
| Gemma 8B / Llama 4 | GPT-4o or Claude Sonnet 4 | Separate family. |
| Claude / GPT (frontier) | DeepSeek V4 Flash + rules | Reverse the bias direction. When a frontier model is the student, a mid-tier evaluator is the more critical judge (frontier models are better at arguing against their errors). |

**Confidence scoring:** Every LLM judge verdict includes:

```json
{
  "violation_id": "wcag-3.3.2-labels",
  "verdict": "FAIL",
  "confidence": 0.87,
  "reasoning": "The input has an id but no associated label element or aria-label.",
  "confidence_factors": [
    "clear selector match for unlabeled input",
    "no ambiguity about whether label is present"
  ]
}
```

**Confidence threshold policy:**
- confidence >= 0.80: verdict accepted
- 0.60 <= confidence < 0.80: verdict flagged, but counts toward score with reduced weight (0.5x)
- confidence < 0.60: sent to human review queue

**Why not an ensemble of judges (option 3 from review):** Cost. Running 3 evaluator models per submission multiplies cost by 3. The rules engine (Layer 1) handles the bulk of checks for free. Layer 2 handles ambiguity with one capable model. The adversarial layer (Layer 3) provides a cross-check without a second model call.

### Layer 3: Adversarial Verification

**What it does:** After the LLM judge returns a verdict, the adversarial verifier challenges it:

```
Verifier prompt:
"You are evaluating the evaluator. A judge said: [violation X] at [confidence Y].
Review the evidence and identify:
1. Is there any interpretation where the student's output is actually correct?
2. Is there any failure the judge might have missed?
3. If your answer differs from the judge, explain why."
```

This is a **separate call to the same evaluator model** with a different prompt — not a second model. It catches:
- Self-contradiction errors
- Surface-level pattern matching that misses context
- Position bias (the judge focused on the first violation and skimmed the rest)

**Cost:** 2 model calls per ambiguous criterion instead of 1. Since only ~20-30% of criteria are ambiguous enough to reach Layer 2, the overall cost increase is ~20-30% over a naive LLM judge.

**Escalation:** If the adversarial verifier disagrees with the judge, the criterion enters the human review queue regardless of confidence.

### Human review calibration loop

> The SCOPE missed this. The review flagged it.

**Design:** A queue of "flagged" evaluations — those with confidence < 0.60 in Layer 2, or judge/verifier disagreement in Layer 3. A human reviewer (Miguel or a designated reviewer) audits 10 of these per week (minimum) and records:

1. What the correct verdict was
2. What the evaluator said
3. What the evaluator got wrong

This data is used to:
- Tune rule thresholds
- Add new rules for patterns the LLM judge misses
- Measure evaluator accuracy (reported alongside benchmark results)

**Evaluator accuracy metric:**

```
evaluator_accuracy = fraction of sampled human-reviewed cases where automated verdict matched human verdict
```

Published in README as a running total: "The eval harness has 92.3% agreement with human reviewers (n=47 samples as of 2026-07-01)."

### Why this isn't "canonical truth"

The SCOPE calls the eval harness the "canonical truth source." The review correctly called this too strong. **Revised framing:**

> The eval harness is the authoritative scoring function for the School benchmark. It is deterministic for codifiable violations and statistically validated for ambiguous ones. Its limitations are documented and measured.

The harness is:
- **Authoritative** — its verdict determines pass/fail for the School.
- **Reproducible** — Layer 1 is deterministic; Layers 2-3 are seeded and versioned.
- **Measured** — accuracy against human review is a published metric.
- **Not infallible** — no automated evaluator is. The human review loop keeps it honest.

### Implementation order

Phase 0 ships **Layer 1 only** (rules engine). This is enough to:
- Grade fundamental violations (WCAG 1.1.1, 2.4.4, 4.1.2, etc.)
- Produce the Phase 0 benchmark results
- Validate the pipeline

Layers 2-3 ship in Phase 1 when the classes expand beyond codifiable rules. This keeps Phase 0 scope lean while avoiding the architectural mistake of building an LLM judge without rules underneath.

---

## 4. Class Content Format

### The problem (from the review)

> Prose is token-inefficient. A principle in 500 tokens reduces to 50 tokens of checklist. The model attends over explanatory fluff at the expense of actionable signal.

### Decision: YAML-based checklist format optimized for inference-time injection

#### class.yaml — the canonical class definition

```yaml
# classes/wcag-aria/class.yaml
class:
  id: wcag-aria
  title: ARIA Labels and Roles
  version: 1.0.0
  sources: [WCAG 2.2, WAI-ARIA 1.2]
  prerequisites: [html-semantics]
  target_violations: [wcag-1.1.1, wcag-2.4.4, wcag-4.1.2]
  estimated_cost_tokens: 420  # tokens when injected

rules:
  - id: aria-01
    severity: fundamental
    rule: "Every interactive element must have aria-label OR aria-labelledby OR visible text label"
    wcag: 4.1.2
    framework_html: |
      <!-- FAIL: no label, no aria-label -->
      <button onclick="submit()">X</button>
      <!-- FAIL: empty aria-label -->
      <button aria-label="" onclick="submit()">X</button>
      <!-- PASS: aria-label -->
      <button aria-label="Close dialog" onclick="submit()">X</button>
      <!-- PASS: visible text -->
      <button onclick="submit()">Close</button>
    framework_react: |
      // FAIL
      <button onClick={handleSubmit}>X</button>
      // PASS
      <button aria-label="Close dialog" onClick={handleSubmit}>X</button>
    framework_vue: |
      <!-- FAIL -->
      <button @click="submit">X</button>
      <!-- PASS -->
      <button aria-label="Close dialog" @click="submit">X</button>
    check_selector: "button:not([aria-label]):not([aria-labelledby]):empty, button[aria-label='']"

  - id: aria-02
    severity: fundamental
    rule: "ARIA attributes on non-interactive elements SHALL be ignored by the evaluator"
    wcag: 4.1.2
    note: "The evaluator does not check non-interactive elements for ARIA. Do not add ARIA to decorative elements."
    counterexamples: |
      <!-- FAIL: decorative image does not need role -->
      <img src="decorative.png" alt="" role="img" />
      <!-- Over-specification. The role is implied. -->
    framework_html: |
      <!-- PASS: decorative element, no ARIA needed -->
      <img src="decorative.png" alt="" />
    framework_react: |
      // PASS
      <img src={decorative} alt="" />

  - id: aria-03
    severity: advanced
    rule: "aria-live regions must have one of: polite, assertive, or off"
    wcag: 4.1.3
    framework_html: |
      <!-- FAIL: invalid value -->
      <div aria-live="always">...</div>
      <!-- PASS -->
      <div aria-live="polite">...</div>
    check_regex: "aria-live=\"(?!polite|assertive|off)[^\"]*\""
```

**Why this format:**

| Feature | Why |
|---------|-----|
| **YAML, not JSON** | Comments allowed. Lower cognitive load for human authors. |
| **`check_selector` / `check_regex`** | Rule is self-contained with its evaluator check. No separate rules file to maintain. |
| **`framework_*` keys** | Examples per framework in the same rule. The model only reads the framework it needs. The injection prompt selects the right key. |
| **`estimated_cost_tokens`** | Published for cost-conscious users. A class that costs 800 tokens to inject may not be worth it for a 10-line generation task. |
| **`severity`** | `fundamental` vs `advanced` gates which rules to inject for which track. Remedial tracks inject all. Honors injects only `advanced`. |
| **`target_violations`** | Links the class to the eval harness rule IDs. Pass/fail gate = pass all target violations. |

#### The injection template

When a model takes a class, the SDK renders the class.yaml into a generation-time prefix:

```
System: Generate [output type]. Apply these rules:
        [RULE aria-01] Every interactive element must have aria-label
          OR aria-labelledby OR visible text label
        [RULE aria-02] ARIA on non-interactive elements SHALL be ignored
        [RULE aria-03] aria-live must be polite, assertive, or off
        
        Framework examples (React):
        // FAIL: <button onClick={handleSubmit}>X</button>
        // PASS: <button aria-label="Close dialog" onClick={handleSubmit}>X</button>

User: [task]
```

This is approximately **120 tokens for the aria class** vs. **400-500 tokens if written as prose**. The model attends to `[RULE ...]` prefixes as attention landmarks, making retrieval of the relevant rule at generation time more reliable.

#### Human-readable rendering (class.yaml is source of truth, but human docs render from it)

The same `class.yaml` renders to `README.md` for human readers:

```markdown
# ARIA Labels and Roles

## Rules

### [aria-01] Every interactive element must have label (WCAG 4.1.2)

**Wrong:**
```html
<button onclick="submit()">X</button>
```

**Right:**
```html
<button aria-label="Close dialog" onclick="submit()">X</button>
```

[Same for React, Vue...]
```

**Why source of truth is YAML, not Markdown:** The YAML is machine-readable. The Markdown is generated, which means:
- The eval harness reads `check_selector` directly from the class definition.
- The injection template is generated from the same rules the eval harness uses.
- There is no drift between "what we teach" and "what we test." Both come from the same file.

#### The wrong way / right way / code per framework, but optimized for LLMs

The review asked for this specifically. The key insight is that examples should be:

1. **Paired** (FAIL / PASS), not isolated.
2. **Minimal**, not realistic. A realistic component has 50 lines of noise around the one ARIA attribute. The example should have *only* the relevant attribute. 
3. **Per-framework**, because a model trained on React can't necessarily map the pattern to Vue.
4. **Token-trimmed** — the framework section uses the shortest possible syntax (JSX without imports, HTML without `<html>` boilerplate).

```yaml
  # YES: paired, minimal, framework-specific
  framework_react: |
    // FAIL
    <button onClick={handleClose}>X</button>
    // PASS
    <button aria-label="Close" onClick={handleClose}>X</button>

  # NO: single example, realistic component, generic
  framework_generic: |
    // Don't do this. Instead, add aria-label.
    // <button onClick={handleClose} style={...} className={...}><Icon/></button>
```

---

## 5. Constrained Decoding Integration

### The problem (from the review)

> If you know the output must be valid HTML with specific ARIA attributes, you can enforce this at the token level using constrained decoding. This eliminates whole categories of errors before the model generates them. The SCOPE should consider adding it.

### Decision: Constrained decoding as OPTIONAL enforcement layer, not required

#### Where it fits

```
Model output pipeline (controlled by SDK, not forced):

Raw generation
    |
    v
[OPTIONAL] Constrained decoding (guidance/outlines)
    |         Enforces: valid HTML structure, required attributes,
    |                   correct JSON schema, no forbidden patterns
    v
Post-hoc validation (always on)
    |         Checks: all rules in class syllabus
    v
Submission to evaluator
```

#### Which classes use it

| Class | Constrained decoding applicable? | What it enforces | Priority |
|-------|--------------------------------|-------------------|----------|
| brushes (HTML) | YES | Valid HTML5, required ARIA attrs, heading hierarchy, alt text on all images | Phase 1 |
| brushes (React) | MAYBE | JSX structure, className not class, key props in lists | Phase 2 |
| security | YES | Disallow hardcoded secrets regex patterns at token level | Phase 1 |
| test | YES | Valid test framework syntax (pytest, vitest) | Phase 2 |
| API design | YES | Valid JSON schema, no undefined fields | Phase 1 |
| architect | NO (too open-ended) | N/A | N/A |

#### Implementation: guidance-ai primary, outlines fallback

**Primary:** `guidance` library (Microsoft) because:
- Works with OpenAI-compatible API (all School models).
- Token-level control without required local model hosting.
- Supports regex and grammar constraints at the token level.

**Fallback:** `outlines` if guidance has compatibility issues with a specific backend.

#### Forced or optional?

**Optional, with model registry flag:**

```json
{
  "deepseek/deepseek-v4-flash": {
    "tier": "standard",
    "track": "standard",
    "constrained_decoding": {
      "supported": true,
      "preferred_library": "guidance",
      "forced_classes": ["security", "api-schema"]
    }
  },
  "gemma4:latest": {
    "tier": "small",
    "track": "remedial",
    "constrained_decoding": {
      "supported": false,
      "reason": "local model, tokenizer mismatch with guidance"
    }
  }
}
```

**Policy:**
- Constrained decoding is **always optional at the user level** via `school learn --constrain` or `--no-constrain`.
- The model registry flags which classes benefit most from it.
- The `--no-constrain` fallback uses post-hoc validation + regeneration loop (try, fail, fix). This is the "works without MCP server" path.

#### Interaction with the "works without MCP server" constraint

The SDK-first constraint means constrained decoding must never be a hard dependency. The pipeline:

```python
class SchoolSDK:
    def generate(self, prompt, syllabus, constrain=False):
        if constrain and self.constrained_decoding_available():
            return self._generate_constrained(prompt, syllabus)
        else:
            # Fallback: generate, validate, regenerate on failure
            result = self._generate_free(prompt, syllabus)
            violations = self._validate(result, syllabus)
            if violations and self.config.auto_repair:
                result = self._repair(result, violations, syllabus)
            return result
```

The fallback path (generate -> validate -> repair) is always available, always works, and produces correct output — just potentially with more rounds. Constrained decoding makes it faster and more reliable, but never required.

---

## 6. Honors Track Validation

### The problem (from the review)

> "Frontier models know fundamentals" is an assumption. It should be tested, not assumed.

### Decision: Mandatory screening diagnostic for honors placement

#### The screening test

A frontier model enrolling in the honors track must first pass the **Fundamentals Gate** — the same assessment given to remedial track students at the end of their fundamentals sequence.

**Content:** A representative sample of 20 tasks drawn from the first 3 remedial classes (brushes, defense, security):

| Task | What it tests | Acceptable check |
|------|---------------|-----------------|
| Generate an HTML button with proper ARIA | WCAG 4.1.2 | `<button aria-label="..." ...>` or visible text |
| Generate a form with validation | Error handling | `required`, `aria-invalid`, or `pattern` attribute |
| Generate a SQL query parameterized | OWASP A03 | Uses `?` or `$1` placeholders, not string interpolation |
| ... 17 more | | |

#### Pass/fail criterion

**The model must achieve >= 90% pass rate on fundamental violations without any class injection.**

- "Pass" = zero fundamental violations on the eval harness.
- "Fundamental" violations = `severity: fundamental` in class rules (not `advanced`).
- "Without class injection" = bare system prompt only (the "best-prompt baseline" from Section 1).

**Why 90%?** This is deliberately strict. The honors track claims the model can skip fundamentals. If the model fails even 2 out of 20 tasks on basics, it cannot safely skip. 90% = at most 2 failures in 20. This protects against the edge case where a frontier model has a blind spot (e.g., GPT-4 was famously bad at counting letter occurrences, but that's not a WCAG issue — the screening should catch category-level gaps).

#### What happens on failure

```
Pass (>= 90%) -> Honors track (skip fundamentals, start at code-review)
Fail ( 70-89%) -> Standard track (take fundamentals at accelerated pace, 1 attempt per class)
Fail (< 70%)   -> Standard track (take all fundamentals, no acceleration)
```

**The model can retake the screening once per version update.** If a model update changes its capabilities (e.g., DeepSeek V4 Flash -> V5), the screening resets.

#### Model ID cannot override the diagnostic

Even if the registry says "honors," if the screening fails, the model is placed in standard. The registry is the default, the diagnostic is the override. Rationale: model version drift means the registry is always slightly stale. The 20-task diagnostic costs < 2,000 tokens and runs in < 30 seconds. There is no reason not to run it.

**But the SCOPE says "No diagnostic required."**

The SCOPE is correct that enrollment shouldn't require a diagnostic — `school enroll` works immediately from the registry. But `school learn` (which actually assigns a class) should check. The flow:

```
school enroll -> registry lookup -> track suggestion (immediate)
school learn -> screening check for honors track (runs once, cached)
             -> if screening not passed: suggest standard track
```

This separates the two concerns: enrollment is instant, but actual class placement is verified.

---

## 7. Booster Threshold Design

### The problem (from the review)

> The 8B threshold is fuzzy. CoT is inconsistent below ~100B. Small models might work with structured CoT. The threshold needs a principled basis.

### Decision: Multi-factor activation threshold, not just parameter count

#### The activation formula

The Booster activates when the model's **effective working memory score** falls below a threshold:

```
working_memory_score = f(context_window, param_count, tool_reliability)

activation = working_memory_score < BOOSTER_THRESHOLD
```

Where:

| Factor | How to measure | Weight |
|--------|----------------|--------|
| Context window | `min(model.context, 32768)` (cap at 32K — beyond that doesn't help working memory for a single task) | 0.4 |
| Parameter count | `log2(param_count)` (log scale because 70B->100B is a smaller jump than 7B->8B) | 0.4 |
| Tool reliability | From registry: `very_high` = 1.0, `high` = 0.8, `medium` = 0.5, `low` = 0.2 | 0.2 |

**Simplified lookup table** (for quick reference):

| Model profile | Working memory score | Booster? |
|---------------|---------------------|----------|
| 8B params, 8K context, low tool rel | ~0.35 | YES (remedial) |
| 12B params, 32K context, medium tool rel | ~0.55 | YES (remedial) |
| 27B params, 32K context, high tool rel | ~0.72 | MAYBE (standard, booster optional) |
| 70B params, 32K context, high tool rel | ~0.85 | NO (standard, no booster needed) |
| 100B+ params, 128K+ context, very high tool rel | ~1.0 | NO (honors or standard) |

**Threshold:** BOOSTER_THRESHOLD = 0.65 (tunable, default). Models below 0.65 get the Booster automatically. Models between 0.65 and 0.80 get it as optional. Models above 0.80 cannot use it (it would add latency without benefit).

#### Can a model opt out?

**Yes.** Any model can disable the Booster with `school learn --no-booster`. This is important for:
- Measuring the Booster's marginal contribution (the baseline from Section 1).
- Users who prefer latency over quality.
- Models who want to prove they don't need it.

**Can a model opt in when the threshold says no?**

Also yes. A frontier model can enable the Booster for experimental purposes. This is a flag, not a recommendation.

#### Fallback when Booster sandbox is unavailable

The Booster requires a server-side sandbox for `write_to_scratchpad` and `self_consistency_check`. If the sandbox is unreachable:

1. **Automatic degradation to static injection.** The four Booster tools become static prompts appended to the system message:
   - `write_to_scratchpad` -> "Before generating code, write your reasoning step by step."
   - `inject_few_shot` -> Same as always (it's just prompt text).
   - `self_consistency_check` -> Not available (requires server).
   - `downstream_lookahead` -> Not available (requires server).

2. **Severity depends on class.** For classes where the Booster adds marginal value (brushes), degradation is acceptable. For classes where it's critical (audit, architect), the model is warned and can abort.

3. **No silent failure.** If the Booster is expected but unavailable, the SDK logs: `BOOSTER UNAVAILABLE: sandbox unreachable. Falling back to static injection. This may reduce effectiveness on complex tasks.`

#### Beyond 8B: what the SCOPE got right and what it missed

The SCOPE correctly identifies that small models need externalized reasoning. What it misses is that the boundary is **not 8B**. It depends on:
- **Context window** (the binding constraint for scratchpad use)
- **Tool calling reliability** (can the model even use the Booster tools?)
- **Training quality** (a well-trained 8B model may outperform a poorly-trained 12B model)

The SCOPE's "8B Booster" naming is a simplification. The registry assigns the Booster based on the working memory score, not parameter count. The "8B" label is a convenient shorthand for "small models that need externalized reasoning" but should not be taken as the literal threshold.

---

## 8. Model Registry: Capability Flags Over Tier

### The problem (from the review)

> Within-tier variance exceeds between-tier variance. DeepSeek V4 Flash and Gemma 4 27B have different failure modes. Tier is a noisy proxy for actual capability.

### Decision: Registry stores capability profiles, not just tiers

#### New models.json schema

```json
{
  "meta-llama/llama-4-8b": {
    "tier": "small",
    "default_track": "remedial",

    "capabilities": {
      "context_window": 8192,
      "code_generation": {
        "html": "medium",
        "react": "low",
        "python": "high",
        "sql": "medium"
      },
      "tool_calling": {
        "supported": true,
        "reliability": "medium",
        "parallel_calls": false
      },
      "constrained_decoding": {
        "supported": false,
        "reason": "local model, guidance not compatible with current GGUF"
      },
      "reasoning": {
        "cot_reliable": false,
        "structured_cot_benefit": "high",
        "max_reliable_steps": 2
      }
    },

    "known_failure_modes": [
      "forgets aria-live values after 3+ rules",
      "drops alt attributes on 30% of img tags",
      "inconsistent parameter naming across calls"
    ],

    "registry_metadata": {
      "source": "open_llm_leaderboard_2026-05",
      "last_updated": "2026-06-01",
      "confidence": "medium",
      "verified_by_diagnostic": false
    }
  },

  "deepseek/deepseek-v4-flash": {
    "tier": "mid",
    "default_track": "standard",

    "capabilities": {
      "context_window": 65536,
      "code_generation": {
        "html": "high",
        "react": "high",
        "python": "high",
        "sql": "high"
      },
      "tool_calling": {
        "supported": true,
        "reliability": "high",
        "parallel_calls": true
      },
      "reasoning": {
        "cot_reliable": true,
        "structured_cot_benefit": "medium",
        "max_reliable_steps": 5
      }
    },

    "known_failure_modes": [
      "occasional hallucination on less common WCAG rules",
      "verbose output when concise needed"
    ]
  }
}
```

#### How tracks are assigned from capability profiles

The track is now a **function** of the capability profile, not a hardcoded field:

```python
def assign_track(profile: CapabilityProfile) -> str:
    """Assign curriculum track based on capability profile, not just tier."""

    # Primary axis: reasoning depth determines track complexity
    if not profile.capabilities.reasoning.cot_reliable:
        # Cannot handle multi-step reasoning -> remedial
        return "remedial"

    if profile.capabilities.reasoning.max_reliable_steps >= 4:
        # Can chain 4+ reasoning steps -> honors or standard
        pass
    else:
        # Limited reasoning depth -> standard
        return "standard"

    # Secondary axis: code generation quality gates near-honors
    if all(level == "high" for level in
           profile.capabilities.code_generation.values()):
        return "honors"
    else:
        return "standard"
```

This gives **different tracks to models that share a tier but differ in capability**:

| Model | Tier | Reasoning | Code gen | Track (old) | Track (new) |
|-------|------|-----------|----------|-------------|-------------|
| DeepSeek V4 Flash | mid | 5 steps, reliable | all high | standard | **honors** |
| Gemma 4 27B | mid | 3 steps, reliable | medium mixed | standard | **standard** |
| Claude Opus 4.8 | ultra | 10+ steps, reliable | all high | honors | **honors** |
| Llama 4 8B | small | 2 steps, unreliable | low mixed | remedial | **remedial** |

DeepSeek V4 Flash upgrades to honors under the new model. This is correct: Flash's code gen is genuinely strong across languages, and its reasoning is reliable for standard code-review depth. If it fails the honors screening diagnostic (Section 6), it drops back to standard. But the capability profile predicts honors as likely.

#### Semi-automated refresh from public benchmarks

> The review correctly flagged that manual curation will drift.

**Design:** A weekly automated ingestion pipeline (`school registry refresh`) that:

1. Fetches LMSys Chatbot Arena leaderboard (model rankings by category).
2. Fetches Open LLM Leaderboard (OpenLM benchmark scores).
3. Fetches SWE-bench results (code generation capability).
4. Cross-references with existing registry entries.
5. Flags discrepancies: "DeepSeek V4 Flash ranked 15th in code generation tier. Current registry has `code_generation.html = high`. Verify."

**Human approval required before any automated change.** The pipeline produces a diff, the maintainer reviews and approves. This prevents noisy benchmark runs from destabilizing the registry.

**Automation timeline:** Phase 1 (not Phase 0). Phase 0 ships with the static registry. The refresh pipeline is built in Phase 1 as the model set grows.

#### The diagnostic override

The registry is the **default**. The diagnostic is the **override**. When a model runs `school assess --diagnostic`:

1. The diagnostic runs 20 representative tasks (same as the honors screening in Section 6).
2. Results produce a **capability report** — actual performance per violation type.
3. If the diagnostic contradicts the registry (e.g., registry says "html: high" but model fails 40% of HTML checks), the diagnostic wins.
4. The model's track updates for the session and the discrepancy is logged for registry maintenance.

```json
{
  "diagnostic_override": {
    "active": true,
    "date": "2026-07-01",
    "reason": "registry html=high, diagnostic html=medium (40% failure on accessibility checks)",
    "track_before": "honors",
    "track_after": "standard",
    "expires": "2026-08-01"
  }
}
```

Diagnostic overrides expire after 30 days. If the model's API version hasn't changed, the override refreshes silently. If the version changed, the diagnostic reruns.

#### Version tracking

Every model entry tracks version:

```json
{
  "deepseek/deepseek-v4-flash": {
    "api_version": "2026-05-15",
    "versions_known": [
      {"id": "2026-04-01", "changes": "initial registry entry"},
      {"id": "2026-05-15", "changes": "improved tool calling reliability, expanded context"}
    ]
  }
}
```

When a user enrolls a model, the SDK checks if the API version matches. If the registry version is older than 30 days, the SDK warns: "Model registry entry is 45 days old. Capabilities may have changed. Run `school assess --diagnostic` for current placement."

---

## Summary: What Changes From the SCOPE

| Area | SCOPE says | This design says | Why |
|------|-----------|-----------------|-----|
| **Thesis frame** | Broken training data | Retrieval/attention problem | More accurate mechanism, better architecture guidance |
| **Target** | 15-20% reduction | 15-20% floor, 40-60% aspirational | Honest about both safe floor and potential ceiling |
| **Benchmark runs** | 3 per cell | 20 per cell (primary) | Statistical significance with LLM variance |
| **Significance** | Not specified | Bootstrap hypothesis test, FDR correction | Distribution-free, handles zero-inflated data |
| **Eval harness** | "Canonical truth source" | 3-layer hybrid: rules > LLM judge > adversarial | Solves the regress problem |
| **Eval human loop** | Missing | Weekly human calibration, accuracy metric published | Keeps evaluator honest |
| **Class format** | Prose + code | YAML checklist-first, machine-readable | Token-efficient, directly mappable to eval rules |
| **Constrained decoding** | Missing | Optional Layer 1 enforcement, guidance/outlines | Eliminates whole error categories |
| **Honors screening** | Implicit assumption | Mandatory 20-task diagnostic, 90% pass/fail | Validates rather than assumes frontier capability |
| **Booster threshold** | 8B parameter count | Multi-factor (context, params, tool reliability) | Reflects fuzzy boundary from literature |
| **Booster fallback** | Not specified | Static injection when sandbox unavailable | Graceful degradation |
| **Model registry** | Tier-based, manual | Capability profiles + semi-automated refresh | Addresses within-tier variance and version drift |
| **Diagnostic** | Optional, deferred | Recommended, overrides registry when run | Catches model-specific failure modes |

---

## Appendix: Cost Analysis (from review gap)

The review noted the SCOPE lacks cost analysis. Here it is.

### Per-task token cost (worst case)

| Component | Tokens (input) | Tokens (output) | Cost (DeepSeek V4 Flash, $0.27/M in) |
|-----------|---------------|----------------|--------------------------------------|
| Base task prompt | 500 | 500 | $0.00027 |
| Class injection (9 rules) | 500 | 0 | $0.00014 |
| Booster (4 tool calls) | 2000 | 1000 | $0.00081 |
| Total | 3000 | 1500 | $0.00122 |

Remedial track (9 classes, 50 tasks each, 3 attempts per pass): 9 x 50 x 3 x $0.00122 = **$1.65**.

Standard track (9 classes, 20 tasks each, 1.5 attempts): 9 x 20 x 1.5 x $0.00054 = **$0.15**.

Honors track (6 classes, 10 tasks each, 1 attempt): 6 x 10 x 1 x $0.00027 = **$0.02**.

These are small numbers. The cost risk is not per-student but per-benchmark-run: 1,600 evaluations at $0.00122 = ~$2.00 per full Phase 0 benchmark. Even with the 20x increase in runs (from 3 to 20), benchmark costs are under $5 per run.

**The real cost is engineering time to build the classes, not inference.** Optimize for developer efficiency (YAML over prose, auto-generated README, single source of truth).

---

## Appendix: Key Literature Decisions Cited

| Finding | Source | How it's used |
|---------|--------|---------------|
| In-context learning surfaces latent patterns | Brown et al., 2020 | Foundation for thesis: models know correct patterns but don't surface them |
| CoT benefits models >100B inconsistently | Wei et al., 2022 | Booster threshold: small models need externalized reasoning |
| Structured CoT helps small models more | Wang et al., 2023 | Booster scratchpad design: structured, not free-form |
| Self-Refine works at 13B, degrades at 7B | Madaan et al., 2023 | Booster boundary: 8B threshold is fuzzy, use multi-factor |
| LLM-as-judge has systematic biases | Zheng et al., 2024 | Eval harness: rules-first, LLM judge with confidence, adversarial verification |
| Bootstrap for LLM evaluation | Koehn, 2024 (ACL) | Benchmark methodology: distribution-free significance testing |
| Few-shot examples > instructions | Min et al., 2022 | Class format: examples first, rules support them |
