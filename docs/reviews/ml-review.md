# ML Engineering Review — lm-tutor (The School for LLMs)

**Reviewer:** Mike (Claude Code / claude-sonnet-4-6) acting as ML reviewer
**Date:** 2026-06-08
**Scope:** SCOPE.md at ground-zero

---

## 1. Central Thesis: "Small models fail on fundamentals because training data is broken"

The School's thesis is roughly: *web data is full of bad practices -> models trained on it reproduce bad practices -> injecting corrective knowledge at generation time fixes this.*

The WebAIM statistic (95.9% of homepages have WCAG failures) is real, but the causal chain from "sites have accessibility bugs" to "models can't produce accessible code" has a missing link. Pre-training on web text gives models fluency in *patterns*, not ground-truth labels for correctness. A model that has seen 10,000 accessible pages and 100,000 inaccessible ones will reproduce the majority distribution. But that is a **representation learning problem** (the correct patterns are in-distribution but low-frequency), not a "training data is broken" problem.

The critical question: is the failure mode that the model *cannot* produce accessible output, or that it *does not prefer* it without steering? The literature on in-context learning (Brown et al., 2020; Wei et al., 2022) strongly suggests the latter. A model that has seen *any* accessible examples during pre-training can surface them with the right prompt. The failure is one of retrieval and attention allocation, not capability. This means the School's approach is sound — it's exactly the kind of structured few-shot steering that works — but the frame is misleading. It's not "fixing broken training data." It's "making existing capabilities reliable through structured prompt intervention."

**Why this matters for the project:** If the thesis were literally true (training data irredeemably broken), fine-tuning would be the only real fix, and inference-side injection would be fighting gravity. Since the failure mode is actually retrieval/attention rather than capability absence, the injection approach is well-motivated. But the School borrows credibility from a scary statistic (95.9%) that doesn't actually prove what it needs to prove. The real experiment worth running: can you elicit the correct behavior from a small model *without* the Booster, using only a well-crafted system prompt? If yes, the Booster is a convenience layer, not a capability unlock. That baseline needs to be measured explicitly.

---

## 2. The 15-20% Reduction Target

### Is it ambitious or timid?

Say a small model currently fails on ~40% of fundamental WCAG checks (a plausible baseline for Gemma 8B on a hard UI task). Reducing that to ~32-34% is a 15-20% *relative* reduction. That is modest. If the baseline failure rate is higher (say 60-70%), the same 15-20% relative reduction means moving from 60% to 48-51% — still failure on roughly half of checks. The absolute improvement is never more than ~12-14 percentage points.

For a system that injects curated, verified, up-to-date knowledge at every generation call, this seems **conservative to the point of underselling**. The theoretical ceiling is much higher. Consider:

- **Few-shot injection** alone can drive task accuracy from 25% to 60%+ on some benchmarks (Brown et al., 2020, Table 3.3).
- **Structured generation** (constrained decoding, grammar guidance) can eliminate whole classes of errors entirely.
- **Self-consistency** (Wang et al., 2022) boosts accuracy by 5-15 points across reasoning tasks by marginalizing over multiple samples.

A 15-20% reduction sounds like it was chosen to be safe — disappointable. I'd argue the ceiling for this kind of intervention is 40-60% reduction on the specific violation types the classes target. The 15-20% figure is reasonable as a *minimum viable effect* for Phase 0, but the scope should acknowledge that it's a floor, not an aspiration.

### Measuring it is harder than it sounds

The reproducibility problem with LLM output variance is real and under-addressed in the SCOPE. Three sources of variance:

1. **Sampling temperature.** Same prompt, same model, temperature=0.7 gives different outputs every time. Even temperature=0 gives nondeterminism on GPU hardware (CUDA non-determinism, TF32 rounding).
2. **Prompt sensitivity.** Small rephrasings of the class content change output quality. The School's class content is prose, which means every class is a different prompt — making cross-class comparisons noisy.
3. **Model update drift.** DeepSeek deploys a new model version on the same API endpoint. Your benchmark from last week is now measuring a different model.

Standard practice: report mean + stddev over **N >= 5 runs** with fixed seed and temperature=0. Compare distributions, not point estimates. The SCOPE mentions "4 models x 5 tasks x 3 runs" as the baseline benchmark — 3 runs is too few for statistical significance on high-variance LLM outputs. Need 10-20 runs per cell.

---

## 3. Model Registry Approach: Tier-by-Model-ID

Assigning curriculum tracks by model ID is **fragile by design**. Here's why:

### Within-tier variance exceeds between-tier variance

DeepSeek V4 Flash ("standard" tier) and Gemma 4 27B (also plausibly "standard") have radically different failure modes. Flash is strong at code generation, weak at structured reasoning. Gemma 4 is the opposite. A "standard" track that treats them identically is throwing away information. Meanwhile, Gemma 4 8B ("small") may outperform Llama 4 8B ("small") on HTML tasks by 20+ points because of different training distributions. The tier is a noisy proxy for actual capability.

### Model versioning is unaddressed

A model update can change everything without changing the ID. Consider these real cases:
- GPT-4 -> GPT-4-Turbo: massive capability jump, same "gpt-4" ID on some APIs
- Claude 3 Sonnet -> Claude 3.5 Sonnet: whole new tier of performance
- DeepSeek V3 -> DeepSeek V4 Flash: architectural rewrite, different tool-use capabilities

The SCOPE says "Contribute updates when new models drop." This is manual. In practice, this file will drift within weeks. An automated ingestion of public leaderboard data (Open LLM Leaderboard, LMSys Chatbot Arena, etc.) would be more honest than a hand-curated JSON file.

### What the SCOPE misses about tier assignment

The actual decision that matters is not "which tier is this model" but "which classes does this specific model need most." Two models in the "standard" tier may need different class sequences — one might be strong on security (trained on OWASP-heavy data) and weak on accessibility, the other the reverse. A diagnostic would catch this. The SCOPE explicitly rejects diagnostics as optional. That's a mistake. The diagnostic should be **recommended** if not required, because the model ID alone is insufficient for optimal track placement.

**Recommendation:** Make the registry a starting point, not the source of truth. Add an optional but encouraged diagnostic that tailors the track based on actual failure modes. The registry maps model -> default track, the diagnostic maps model -> personalized track.

---

## 4. Externalized Reasoning for Small Models (The Booster)

The Booster's four tools — scratchpad, self-consistency check, few-shot injection, downstream lookahead — are well-motivated individually. The question is whether they compose effectively at 8B scale.

### The threshold question

The SCOPE implicitly assumes there's a model size below which CoT stops working, and that the Booster recovers this capability by offloading reasoning to an external server. The literature supports the threshold intuition but the boundary is fuzzy:

- **Wei et al. (2022)** show CoT improves mostly for models >100B parameters. Below that, gains are inconsistent.
- **Wang et al. (2023)** show that smaller models benefit more from *structured* CoT (step-by-step with formatted intermediate steps) than from free-form CoT. This supports the scratchpad approach.
- **Madaan et al. (2023, "Self-Refine")** show iterative self-feedback works at 13B scale but degrades at 7B. The 8B boundary of the Booster sits right at this threshold — it might work, it might not.

The Booster's key insight — that *externalizing* reasoning (offloaded to server-side tools that return structured results) is different from *internal* CoT — is actually well-supported. A small model can't maintain a multi-step reasoning chain in its limited KV cache, but it *can* process one structured interaction at a time. The scratchpad tool essentially extends the model's effective context by letting it "save progress" and reload it, sidestepping the working memory limitation.

### My main concern: the Booster bypasses the model's own capabilities

The danger of externalized reasoning is that it teaches the model to rely on crutches. A model that always uses `write_to_scratchpad` before generating code never learns to hold and manipulate the plan internally, because it doesn't need to. This is fine during School usage (we want correct output), but the model won't generalize this behavior to non-School contexts where the Booster isn't available. The gains measured in-benchmark will not transfer to real-world usage.

This is also an issue for the evaluation methodology. Measuring the School's effectiveness with the Booster active means you're measuring the system, not the model. The SCOPE acknowledges this implicitly ("benchmark WITH and WITHOUT booster") but the Phase 3 plan treats this as a secondary analysis, not a primary metric. It should be the other way around: the primary metric should be the model's standalone performance after School exposure, with the Booster as a secondary "assisted mode" metric.

### A missing tool in the Booster: constrained decoding

If you know the output must be valid HTML with specific ARIA attributes, you can *enforce* this at the token level using constrained decoding (e.g., guidance-ai, outlines, llama.cpp grammar). This eliminates whole categories of errors before the model generates them. It's arguably more powerful than any of the four proposed tools for the use case described. The SCOPE should consider adding it, or at minimum acknowledge why it's excluded.

---

## 5. Class Content Format: Prose + Code vs. Embeddings

The SCOPE proposes classes as structured prose with principles, wrong way, right way, and code per framework. For inference-time injection, this is... fine. But it's worth asking whether it's optimal.

### The case against prose at generation time

When a model processes a class, it concatenates the prose content into its context window. Prose is token-inefficient. A single principle explained in 500 tokens might reduce to 50 tokens of structured checklist. The model then has to attend over those 500 tokens, many of which are explanatory fluff, to extract the actionable signal. At generation time, every token in the prompt competes for attention budget with the task itself.

### What would be more effective

**Checklist-first format.** Instead of "Principle X: always use ARIA labels on interactive elements... here's the wrong way... here's the right way in React...", the class content should be:

```
## ARIA Labels (Checklist)
- [RULE] Every interactive element must have aria-label OR aria-labelledby
- [RULE] aria-label on non-interactive elements SHALL be ignored (WCAG 4.1.2)
- [COUNTEREXAMPLE] <div onclick={...} /> — Focusable? Role? Label? None.
- [EXAMPLE] <button aria-label="Close dialog" onClick={...}>X</button>
```

This is:
- **Token-efficient.** 1/3 the tokens of prose.
- **Easier to attend over.** The model can locate rules by prefix pattern.
- **Directly actionable.** The model generates from "here's what to check" rather than from "here's what I learned."
- **Easier to grade.** Violation rules match 1:1 with eval harness checks.

**Embedding-based retrieval is a different tool for a different problem.** If the model had a vector store with class content, it could retrieve the most relevant rules per task. This would be more token-efficient than injecting the full syllabus. But it adds infrastructure (vector DB, retrieval pipeline) and the model has to learn to use it. The SCOPE's simpler injection approach is the right call for v1. But consider this for Phase 4+.

---

## 6. The Honors Track: "Teach Review First"

The SCOPE claims honors-track classes start with code review and audit rather than fundamentals. The pedagogical rationale is that frontier models can already produce correct code for fundamentals, so their failure modes are architectural (system design, security postures, cross-module interaction) rather than local (syntax, patterns).

This is **plausible but unvalidated.** Two concerns:

### Review requires fundamentals as a prerequisite

Code review is not a standalone skill. To review code competently, a model must know what correct code looks like. The standard track sequence (brushes -> architect -> ... -> code-review) implicitly acknowledges this — review is last. The honors track puts review first. If frontier models truly do internalize fundamentals during pre-training, this works. If they have gaps (and they do — frontier models still hallucinate API calls, forget edge cases, produce insecure defaults), then putting review first means reviewing code without knowing the standards.

The empirical question is straightforward and testable: do frontier models pass fundamental classes on the first try? If yes, skip them. If no, they shouldn't be in the honors track. The SCOPE doesn't mention running this diagnostic before enrolling a model in honors.

### The "review teaches generation" claim

There is evidence that code review experience improves code writing in humans (e.g., Bacchelli & Bird, 2013, "Expectations, Outcomes, and Challenges of Modern Code Review"). But this evidence is about human developers who can reason about review feedback across sessions. For LLMs, which have no persistent memory between calls, the transfer from "review this code" to "write better code" depends entirely on the model having internalized the review patterns during pre-training. If the model can do this, review-first is efficient. If not, it wastes the student's best asset (long context) on tasks it can't learn from.

**Recommendation:** Make honors track adaptive. Start with a screening diagnostic. Frontier models that pass all fundamental classes skip them. The rest get a customized sequence. This is more work than a static track map, but it's honest about heterogeneous capability even among "frontier" models.

---

## 7. The Eval Harness: Can the Verifier Be More Correct Than the Student?

This is the hardest problem in the whole scope and the SCOPE underspecifies it.

### The regress problem

To grade whether a model's output violates WCAG, you need something that knows WCAG. If that something is an LLM (e.g., GPT-5 evaluating DeepSeek V4 Flash), you're trusting a model that might itself be wrong. This is the classic LLM-as-judge regress (Zheng et al., 2024, "Judging LLM-as-a-Judge"): evaluator models have systematic biases (length bias, sycophancy, position bias) and can miss violations that a human expert would catch.

If the evaluator is a **rules engine** — regexes, AST checks, validation libraries — it's deterministic and verifiable but can only check codifiable rules. Many accessibility violations (e.g., "is the visual affordance appropriate?") are not codifiable.

The SCOPE mentions "independent verifier, no shared state, canonical truth source" but doesn't specify what the verifier is. The evasiveness suggests the author hasn't decided. This is the single biggest technical risk in the project.

### Possible approaches, ranked by feasibility

1. **Hybrid: rules + LLM judge.** Codifiable violations go through hardcoded checkers (e.g., `html-validate` for WCAG). Ambiguous cases go through a separate, large evaluator model. The evaluator model publishes its confidence, and scores below threshold are flagged for human review. This is the pragmatic choice for v1.

2. **Rules-only with limited scope.** Accept that the evaluator only checks codifiable rules (required ARIA attributes, heading hierarchy, sufficient color contrast in hex values, etc.). This covers maybe 40-50% of WCAG criteria but is fully deterministic. The school *defines correctness as what the evaluator measures*, acknowledging the gap.

3. **Ensemble of judges.** Multiple evaluator models (different families) vote. Disagreements are flagged. This reduces bias but increases cost and complexity.

4. **Adversarial verification.** The evaluator generates counterexamples to its own judgment. "I said this passes. Here's why it might not." This catches some self-consistency errors but doesn't solve the regress.

**The SCOPE's "canonical truth source" language is too strong for any of these approaches.** None of them produce ground truth. They produce *structured approximations of ground truth.* The honest framing would be: "The eval harness is the authoritative scoring function for the benchmark. It is not perfect. We measure and report its limitations."

### The most dangerous assumption

"Independent process, no shared state" prevents cheating but doesn't prevent correlated errors. If the same training data corrupted both the student model and the evaluator model (e.g., both trained on web data with the same 95.9% WCAG failure rate), they will agree on wrong answers. The SCOPE needs to address evaluator calibration explicitly.

---

## 8. Competitive Landscape: What's Actually New?

The SCOPE doesn't claim novelty, but an honest landscape assessment is important for positioning.

### What exists

| Existing thing | What it does | Overlap with School |
|---|---|---|
| **SWE-bench** | Agentic coding benchmark | Evaluates coding, but not with injected curriculum. No syllabus. |
| **HumanEval / MBPP** | Function-level code generation | Measures correctness, not standard compliance. No teaching. |
| **LLM-as-judge** (Prometheus, JudgeLM, etc.) | Model evaluates model | The eval harness idea, but without curriculum-based grading. |
| **Guidance / Outlines** | Constrained decoding | Enforces output format. Addresses the same problem (bad output from small models) at the token level. |
| **DSPy** | Programmatic prompt optimization | Compiles task description -> optimized prompt. Could parallel the class content pipeline. |
| **Anthropic's "many-shot jailbreaking"** | Context window poisoning | Not relevant directly, but shows that prompt injection is a double-edged sword. |
| **MCP protocol** | Tool server standard | The School uses MCP as transport. Not novel, but the right choice. |

### What the School does that's genuinely new

1. **Inference-time curriculum injection as a core product.** Nobody is shipping "here's a model registry, here's a track, here's a Booster, here's a syllabus, now learn" as a unified CLI/MCP experience. The close integration of registry + classes + eval is novel.

2. **The Booster as first-class architecture.** Externalized reasoning for small models is studied academically but not packaged as a deployable tool suite. The four-tool set (scratchpad, consistency, few-shot, lookahead) is a reasonable first cut.

3. **Track-based curriculum with model-ID gate.** Nobody does this. Most curriculum work is either human-oriented or assumes a single model. The multi-model, multi-track approach with automated enrollment is genuinely novel.

4. **Bidirectional sync with domain projects.** The idea that School classes update from source projects *and* source projects update from School classes is unusual. In practice, the reverse direction (School -> source project) will probably not happen often — but the intent is good.

### What is not new (claims that oversell)

- **"Independent eval harness"** — this is LLM-as-judge with extra steps. The "independent process" framing is technically interesting (avoids shared state corruption) but the core judgment is existing technology.
- **"Canonical truth source"** — no such thing exists for standards compliance. The evaluator is an approximation.
- **"Socratic debug breaks panic loops"** — this is iterative self-correction prompting, known since Self-Refine (Madaan et al., 2023).

### What's missing

- **No mention of human-in-the-loop for evaluation.** Even the best automated evaluators need periodic calibration against human judgment. Where does this happen?
- **No adversarial robustness.** If I inject malicious content into "here's the wrong way" examples, can I poison the model? The class format includes wrong examples — these are prompt injection vectors.
- **No cost analysis.** How many tokens does each class consume? For a remedial student taking 9 classes with the Booster active, the token cost per task could be 10-20x the baseline. Is that acceptable?

---

## Summary Assessment

| Layer | Verdict | Key Risk |
|-------|---------|----------|
| **Thesis** | Plausible but framed incorrectly | It's a retrieval problem, not a training data problem. The 95.9% statistic is rhetorically useful but logically disconnected from the intervention. |
| **15-20% target** | Under-ambitious | The ceiling is probably 40-60% reduction for targeted violations. 15-20% is a safe floor, not an aspiration. |
| **Model registry** | Fragile | Version drift and within-tier variance make static ID-to-track mapping unreliable. Needs automated refresh and optional diagnostics. |
| **Booster** | Well-motivated, unvalidated at 8B threshold | The externalization strategy has theoretical support but sits right at the model size boundary where CoT gains are uncertain. Missing constrained decoding. |
| **Class format** | Suboptimal | Prose is token-inefficient. Checklist-first format would be more effective for inference-time injection. |
| **Honors track** | Unvalidated assumption | Frontier models might not actually know fundamentals. Should screen, not assume. |
| **Eval harness** | **Biggest risk** | The regress problem (who evaluates the evaluator?) is underspecified. Need to commit to rules vs. LLM judge vs. hybrid. |
| **Novelty** | Genuine at the system level | Individual components exist. The integration (registry + curriculum + booster + eval) is new. This is the right way to build a v1. |

### Go/no-go assessment

The project thesis is defensible, the architecture is clean, and the deliberate exclusion of fine-tuning is the right engineering call for an inference-side tool. The two real blockers are:

1. **The evaluator must be built and validated before anything else.** A grading board that self-contradicts or misses violations makes every other component untestable. Phase 0 should ship the evaluator first, then the SDK scaffold, then the registry.

2. **The booster baseline (model alone, no booster, with good prompting) must be established before claiming booster effectiveness.** Otherwise the 15-20% target is not attributable to the intervention.

The project should go ahead, but with a slightly humbler evaluator claim and a tighter focus on measuring what is actually being measured.
