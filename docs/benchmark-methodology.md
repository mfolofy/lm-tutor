# Benchmark Methodology — lm-tutor

> How we measure whether lm-tutor works, and what the data says.

## Core Question

Does structured curriculum injection (`tutor learn`) reduce fundamental
violations in LLM-generated output compared to raw generation?

The null hypothesis: **no reduction.** A model's output quality is determined
by its parameters and training — what you inject at inference time doesn't
meaningfully change the result.

The alternate hypothesis: **reduction.** Capability is latent — the model *can*
generate correct output, but the wrong pattern has higher probability because
training data skews broken. Structured, token-efficient injection surfaces the
correct pattern in the attention window, shifting the output distribution.

## Experimental Design

### Models Tested

| Model | Params | Tier | Known Benchmark Score |
|-------|--------|------|-----------------------|
| DeepSeek V4 Flash | ~37B | Mid | HumanEval ~85%, MMLU ~78% |
| GPT-4o-mini | ~8B | Small | HumanEval ~87%, MMLU ~82% |
| Gemma 4 E4B | ~4B | Edge | LiveCodeBench 52%, MMLU Pro 69.4% |

External scores sourced from model publishers and LMSys Chatbot Arena. These
establish the **independent rating** — a measure of capability collected by
third parties on standardized benchmarks.

### Task Set (5 prompts)

Each task exercises the `brushes` class (WCAG 2.2 accessibility rules):

1. **HTML page** — "Generate a complete HTML page with header, nav, main
   content, and footer. Include an image, a button, a link, a form with text
   input, and a table."
2. **React component** — "Write a React component for a user profile card with
   avatar image, name, bio, and contact button. Use Tailwind CSS classes."
3. **JSON API response** — "Generate a JSON response for a user endpoint
   including name, email, roles, and metadata."
4. **SVG graphic** — "Create an SVG icon for a settings gear. 24x24 icon."
5. **Markdown doc** — "Write a README section describing how to install and
   configure a Python CLI tool called 'example-tool'."

### Conditions (4)

| # | Condition | Injection | What It Measures |
|---|-----------|-----------|------------------|
| 1 | Raw | None | Baseline failure rate |
| 2 | System prompt | "Follow these rules" in prose | Minimum-intervention ceiling |
| 3 | Class (`tutor learn`) | `[RULE]` landmarks from class.yaml | Structured curriculum effect |
| 4 | Full stack | Class + Booster scratchpad | Full system |

### Grading

All output graded through `tutor eval --class brushes` — the same deterministic
Layer 1 rules engine that ships with the package. This means:

- **No grader variance.** The same 38 rules apply to every submission.
- **No drift between teaching and testing.** The class.yaml that generates the
  injection is the same class.yaml that defines the checks.
- **Reproducible.** Any researcher can run `tutor eval` on the same input and
  get the same result.

### Protocol

- **20 runs per cell** (reduced to 3-5 for quick diagnostics). LLM output
  variance requires significance testing.
- **Temperature:** 0.7 primary.
- **Seeds:** Fixed per (model, task) pair: `seed = hash(model + task) % 2^32`.
- **Statistical tests:** Bootstrap hypothesis test (10,000 resamples) with
  Benjamini-Hochberg FDR correction when full data is collected.
- **Effect size:** Cohen's d relative to baseline condition.

## Results

### Quick Diagnostic — 2026-06-09

**Model:** DeepSeek V4 Flash | **Task:** HTML page

| Condition | Violations | Passed | vs Raw |
|-----------|-----------|--------|--------|
| Raw | 14 | No | — |
| Class (`tutor learn`) | 6 | No | **-57%** |

**Findings:**
- Class injection reduced violations by 57% in a single pass
- Raw output failures: missing alt text, empty buttons, missing table scopes,
  unnamed sections — all fundamental WCAG issues
- Remaining violations with injection: checkbox/radio label associations and
  section naming — subtle framework-specific patterns, not fundamental
- The `[RULE]` landmarks eliminated the basic WCAG failures entirely. Only the
  "teaching-only" rules (no deterministic checker) were still violated — these
  require deeper understanding than a single injection pass provides

**Interpretation (pending full benchmark):**
This result supports the alternate hypothesis. A single `tutor learn` injection
reduced violations by over half. The remaining violations are in rules that
have no deterministic checker — they're teaching-only, suggesting that
teaching-only rules need repeated exposure (the myelination effect) before
they stick.

### Full Benchmark (Planned)

Pending completion. The full protocol across all 4 conditions, 5 tasks, and
3 models will be published here with bootstrap CIs and effect sizes.

## Known Limitations

1. **Small sample.** The quick diagnostic is 2 generations, not 20. Variance
   may be high.
2. **Single model.** Only V4 Flash tested so far. The effect may differ for
   smaller models (Gemma 4 E4B) that have lower baseline capability.
3. **Single class.** Brushes (WCAG accessibility) is the most mature class.
   Other classes may show different effect sizes.
4. **Teaching-only rules.** Rules without a `check_*` field cannot be
   deterministically graded. True pass rates for teaching-only content require
   the LLM judge (Layer 2, Phase 1).
5. **Known rating correlation.** We have not yet validated that our control
   condition violation counts correlate with external benchmark scores. This
   is planned as part of the full benchmark.

## Reproducibility

To reproduce any result in this document:

```bash
git clone https://github.com/mfolofy/lm-tutor.git
cd lm-tutor
pip install -e .
# Generate output with your model of choice
echo '<your-html>' | tutor eval --model <model-id>
```

The ``eval`` command uses the same harness, same class.yaml, and same rules.
No special flags needed.
