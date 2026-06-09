# SOURCES — prompt-design (Prompt Engineering for LLMs)

All rules in `class.yaml` derive from established prompt engineering research,
industry best practices, and peer-reviewed publications on LLM behavior. Every
rule cites the specific paper, guide, or standard it codifies.

## Primary guides

- **DAIR.AI Prompt Engineering Guide** — comprehensive prompt engineering
  techniques, updated continuously.
  <https://www.promptingguide.ai/>

- **OpenAI Prompt Engineering Guide** — official best practices from OpenAI,
  covering six key strategies.
  <https://platform.openai.com/docs/guides/prompt-engineering>

- **Anthropic Prompt Engineering Guide** — official guide covering chain-of-
  thought, role prompting, XML tags, and multi-turn techniques.
  <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview>

## Key research papers

| Paper | Source | What It Proves |
|-------|--------|----------------|
| "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" | arXiv 2201.11903 (Wei et al., 2022) | Step-by-step reasoning improves accuracy on arithmetic, commonsense, and symbolic reasoning by 15-30%. |
| "Self-Consistency Improves Chain of Thought Reasoning in Language Models" | arXiv 2203.11171 (Wang et al., 2022) | Sampling multiple COT paths and voting improves accuracy further. |
| "Tree of Thoughts: Deliberate Problem Solving with Large Language Models" | arXiv 2305.10601 (Yao et al., 2023) | Extends COT with exploration over multiple reasoning branches. |
| "Meta-Prompting: Enhancing Language Model Performance Through Prompt Generation" | arXiv 2311.12055 | LLMs can generate effective prompts when given quality criteria and examples. |
| "Universal and Transferable Adversarial Attacks on Aligned Language Models" | arXiv 2307.15043 (Zou et al., 2023) | Demonstrates prompt injection vulnerabilities; user input in system context enables adversarial override. |
| "Constitutional AI: Harmlessness from AI Feedback" | Anthropic, arXiv 2212.08073 | Rule-based constraints embedded in system prompt reduce harmful outputs. |
| "Jailbreaking Black Box Large Language Models in Twenty Queries" | arXiv 2310.08419 (Chao et al., 2023) | Prompt injection vectors exist even in well-guarded systems. |
| "The Impact of Reasoning Step Length on Large Language Models" | ACL 2024 | Longer COT chains improve accuracy up to a point; diminishing returns past ~8 steps. |
| "ReAct: Synergizing Reasoning and Acting in Language Models" | arXiv 2210.03629 (Yao et al., 2022) | Interleaved reasoning + action traces outperform pure COT for tool-use tasks. |
| "Automatic Prompt Engineer" | arXiv 2311.01906 (Zhou et al., 2023) | Meta-prompting can discover high-quality prompts automatically. |
| "Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models" | arXiv 2310.06117 | Step-back prompting (asking for abstract principles before specific answers) improves accuracy. |
| "Graph of Thoughts" | arXiv 2308.09687 (Besta et al., 2023) | Extends COT to graph-based reasoning structures. |

## Prompt design techniques and evidence

### Temperature and output quality

- **Code generation** benefits from low temperature (0.0-0.2) to reduce
  hallucination and syntax errors. Chen et al. (2021) and subsequent work on
  Codex/CodeLlama shows deterministic settings for code outperform stochastic
  ones.
- **Creative writing** requires higher temperature (0.7-0.9) to produce varied
  and novel output. The range 0.3-0.6 produces "neither fish nor fowl" — not
  precise enough for code, not varied enough for creativity.

### Few-shot learning

- Brown et al. (2020, "Language Models are Few-Shot Learners") established that
  3-5 examples are optimal for in-context learning. Fewer under-specifies the
  task; more causes the model to overfit to superficial patterns.
- FAIL examples (negative exemplars) are more informative than PASS-only
  examples — they define the decision boundary more precisely (Lewis & Gale,
  1994; applied to LLMs in Min et al., 2022).

### Context window placement

- Liu et al. (2023, "Lost in the Middle: How Language Models Use Long Contexts")
  demonstrates that models attend most strongly to tokens at the beginning and
  end of long contexts — placing critical instructions in the middle reduces
  compliance. This motivates the primacy + recency sandwich pattern.

### Instruction format

- Zhou et al. (2022, "The Unreliability of Explanations in Few-shot Prompting")
  shows that instruction placement relative to examples significantly affects
  output quality.
- Post-hoc constraints (instructions appearing after the generation verb) are
  less reliably followed than pre-positioned constraints — the model has already
  begun its output distribution before reading the constraint.

## Research sources from brush-stroke and kimi-filters

Migrated from `projects/brush-stroke/docs/SOURCES.md` (compiled 2026-06-07)
and `projects/prompt-brush/docs/kimi-filters-research.md`.

### Brush-stroke: LLM output quality research

| Paper | Source | Relevance |
|-------|--------|-----------|
| "A Survey of Vibe Coding with Large Language Models" | arXiv 2025-2026 | Formalizes vibe coding as CMDP. Context engineering > raw prompting. |
| "Vibe Coding: Intention Instead of Implementation" | i-com, Apr 2026 | Intent-Context-Quality model. Without explicit constraints, LLM output is functional but generic. |
| "Vibe Checker: Aligning Code Evaluation with Human Preference" | ICML 2026 | current pass@k misses non-functional instructions — motivates explicit constraint placement. |
| "Bridging the Visual Specification Gap in AI-generated UIs" | UC Berkeley MIMS 2026 | The "tacit ceiling" — you cannot prompt your way to better output without explicit constraints. |

### Kimi-filters: prompt pattern research

Kimi K2.6 research on photographic lens filters reveals how prompt framing
shapes model output:

- **Neutral Density** vs specific filter language — prompts that use precise
  technical terminology ("10-stop neutral density filter") produce more accurate
  domain output than vague descriptions ("make the water smooth").
- **Model-specific phrasing** — GPT-Image-2 and Gemini 3.1 Flash respond
  differently to the same prompt concepts (e.g., "shot with X filter" vs
  "X filter effect"). This motivates per-model prompt adaptation in structured
  output (see `structured-output` rule).
- **Anti-pattern catalogs** — the kimi-filters catalog shows that LLMs generate
  higher-quality output when given explicit negative specifications ("FAIL: no
  color-only indicators") alongside positive ones.

## Per-rule source map

| Rule id | Primary Source(s) | Evidence |
|---------|-------------------|----------|
| `temperature-range` | OpenAI/Anthropic guides, Codex papers | Code gen 0.0-0.2; creative 0.7-0.9; 0.3-0.6 wasteland |
| `verbose-prompting` | DAIR.AI, token-efficiency literature | [RULE] markers save ~15 tokens vs prose |
| `instruction-leak` | Anthropic guide; empirical observation | Meta-instructions in prompts produce compliance boilerplate |
| `prompt-injection` | Zou et al. 2023; arXiv 2310.08419 | User input in system prompt enables adversarial override |
| `constraint-placement` | Zhou et al. 2022; Liu et al. 2023 | Post-hoc constraints less reliable; primacy effect |
| `system-prompt-order` | OpenAI guide; Anthropic guide | Role before task governs model approach |
| `few-shot-design` | Brown et al. 2020; Min et al. 2022 | 3-5 optimal; FAIL examples define decision boundary |
| `chain-of-thought` | Wei et al. 2022 (arXiv 2201.11903) | +15-30% accuracy on multi-step reasoning |
| `structured-output` | OpenAI guide; empirical | Schema prevents key drift; parser reliability |
| `context-window-priority` | Liu et al. 2023 "Lost in the Middle" | Primacy + recency; middle context loss |
| `role-prompting` | Anthropic guide; OpenAI guide | Domain-specific role activates expert knowledge |
| `iteration-pattern` | A11yAgent (ACM W4A 2026); vibe coding research | Generate-detect-repair loop catches ~40% more errors |
| `persona-consistency` | Anthropic guide; empirical | Persona drift confuses output distribution |
| `meta-prompting` | arXiv 2311.12055; Zhou et al. 2023 | LLMs generate effective prompts with quality criteria |
| `output-priming` | OpenAI guide; empirical | First token biases entire generation distribution |
| `negative-instructions` | Constitutional AI (arXiv 2212.08073) | Negative + positive combined > positive-only |

## Coverage honesty

**Layer 1 (regex) rules** cover codifiable prompt anti-patterns with high
precision: temperature values, verbosity markers, instruction leak phrases,
injection vectors, and constraint ordering. They do **not** cover patterns
requiring semantic understanding, cross-turn analysis, or quality assessment —
those are deferred to the LLM judge (Layer 2, Phase 1).

The honest coverage boundary for prompt-design:
- ~30% of prompt quality criteria are codifiable at Layer 1 (formatting,
  constraint placement, literal patterns)
- ~50% need LLM judgement (example quality, persona consistency, reasoning
  soundness)
- ~20% need human evaluation (whether a prompt is actually effective for the
  task)

## Verification

Each rule with a `check_regex` is FAIL/PASS tested in
`tests/test_prompt_design.py`. Teaching-only rules (no checker) are tested for
content presence only. A rule cannot ship without its test pair — see
CONTRIBUTING.md.
