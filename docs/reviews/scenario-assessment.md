# SCENARIO ASSESSMENT: 4B Model Using lm-tutor

**Assessor:** Mike (Claude Code / claude-sonnet-4-6)
**Date:** 2026-06-08
**Target:** lm-tutor Phase 0 — real-world usability for a small model
**Method:** Trace every code path the scenario exercises

---

## The Scenario

> User installs a ~4B parameter model. Instructs it: "any time you create HTML
> or wire up UX, use lm-tutor first." Model reads the rules → generates better
> output than without schooling.

---

## Flow Trace: What Actually Happens

### 1. `tutor enroll <model-id>`

```python
# Unregistered 4B model:
resolve_model("qwen3-4b") → None
# Returns:
{
  "registered": False,
  "track": "remedial",
  "booster": True,
  "working_memory_score": 0.0  # param_count_b unknown
}
```

**Verdict:** ✅ Works. Defaults to remedial + Booster ON — correct for a 4B model.

**But:** `working_memory_score` = 0.0 because `param_count_b` is missing. The
Booster activates, but the threshold calculation is meaningless without data.
A registered 4B model would score ~0.23 (well below 0.65 threshold — still
activates, but the provenance is transparent).

### 2. `tutor learn brushes`

Output (~120 tokens):

```
# WCAG 2.2 Accessibility
Apply these rules:
  [RULE img-alt] Every <img> must have non-empty alt text or aria-label.
  [RULE input-image-alt] <input type="image"> must have non-empty alt text.
  [RULE button-name] Every <button> must have an accessible name.
  [RULE empty-aria-label] aria-label must not be empty.
  [RULE link-name] Every <a> needs accessible name (text, aria-label, aria-labelledby).
  [RULE label-for-input] Every <input> needs a <label> or aria-label.
  [RULE html-lang] <html> must have a lang attribute.
  [RULE title-required] <title> must be non-empty.
  [RULE positive-tabindex] Avoid positive tabindex values.
  [RULE aria-live-valid] aria-live values must be valid.
```

Plus checkpoint saved to `~/.tutor/track_state.json` (crash recovery).

**Verdict:** ✅ Fits in ~1.5% of an 8K context window. Token-efficient format.
No comprehension check — model must discover gaps via eval failures.

### 3. Model generates HTML with rules in context

The model attends to `[RULE ...]` landmarks during generation. The format
eliminates prose overhead — rules are checklists, not paragraphs. This is
consistent with the research grounding (Min et al. 2022: few-shot examples
> instructions; Wei et al. 2022: structured prompting helps small models).

**Verdict:** ✅ Architecture matches the thesis. No code change needed.

### 4. `tutor eval < output.html`

```json
{
  "syllabus": "brushes (auto-detected)",
  "passed": false,
  "rules_checked": 10,
  "violations": [
    {"rule": "img-alt", "severity": "fundamental", "matched": "<img src=\"x.png\">"}
  ],
  "hint": null,
  "error": null
}
```

`infer_syllabus()` detects HTML tags → maps to `brushes`. 10 rules checked.
Deterministic, stdlib-only, no class venv needed.

**Verdict:** ✅ Works perfectly. Structured feedback enables iterative improvement.
Exit code 0 even with violations (successful grade ≠ pass).

### 5. Booster Protocol activation

For a 4B model: `working_memory_score` ~0.23 → Booster ACTIVE.

The model should get:
- `write_to_scratchpad` — sandbox for reasoning before code generation
- `self_consistency_check` — verify assumptions before committing
- `inject_few_shot` — get concrete PASS/FAIL examples for the task
- `downstream_lookahead` — predict edge cases from current choices

**Verdict:** ❌ **BLOCKED.** All four tools are Python API only
(`tutor.booster.tools`). No CLI subcommand. No MCP tool. A model calling
lm-tutor as a subprocess cannot invoke any Booster tool.

| Tool | CLI? | MCP? | Python API? |
|------|------|------|-------------|
| `write_to_scratchpad` | ❌ | ❌ | ✅ |
| `self_consistency_check` | ❌ | ❌ | ✅ |
| `inject_few_shot` | ❌ | ❌ | ✅ |
| `downstream_lookahead` | ❌ | ❌ | ✅ |

---

## Gap Analysis

### Critical (P1 — blocks the autonomous workflow)

| # | Gap | File | Impact |
|---|-----|------|--------|
| G-01 | Booster tools not CLI-accessible | `booster/tools.py` + `cli/` | A 4B model using lm-tutor as a subprocess can't call scratchpad, consistency check, few-shot construction, or lookahead. These are the tools designed specifically for small models. |
| G-02 | `tutor learn` has no Booster integration | `cli/learn.py` | When Booster is active, learn should automatically inject few-shot examples and suggest scratchpad usage. Currently just dumps rules — ignores the model's capability profile at the point of delivery. |
| G-03 | No correction loop (`tutor fix`) | `grading/socratic_debug.py` | Eval reports violations but can't trigger a fix cycle. The Socratic Debug skeleton has data structures but no LLM-driven generate → eval → repair loop. Model must manually fix and re-eval. |

### Important (P2 — reduces improvement velocity)

| # | Gap | File | Impact |
|---|-----|------|--------|
| G-04 | No 4B model in registry | `registry/models.json` | Smallest registered is Gemma 4 at 8.7B. Unregistered models get `working_memory_score: 0.0` — correct track assignment but meaningless Booster threshold. |
| G-05 | No curriculum progression | `cli/learn.py` | SCOPE defines per-track class ordering but no `tutor curriculum` command. Model must manually know "remedial: brushes → defense → security → ..." |
| G-06 | `tutor learn` doesn't verify comprehension | `cli/learn.py` | No check that the model understood the rules before checkpointing "complete." |
| G-07 | Sandbox tools throw cryptic errors | `booster/sandbox.py` | Subprocess failures surface Python tracebacks — not model-friendly error messages. |

### Polish (P3 — cosmetic, doesn't block)

| # | Gap | File | Impact |
|---|-----|------|--------|
| G-08 | No `.dockerignore` | project root | Docker COPY includes `__pycache__` and `.egg-info` |
| G-09 | `harness.py` silent `except: pass` | `eval/harness.py:103-104` | HTML parse errors swallowed — masks real bugs |
| G-10 | `health.py` reloads registry per check | `mcp/health.py:26` | Reads JSON on every Docker HEALTHCHECK — negligible but sloppy |

---

## Assessment Summary

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| One-shot learn + eval | ✅ PASS | Model learns rules → generates → eval catches violations. Core loop works. |
| Autonomous Booster tools | ❌ FAIL | Python API only. Model can't call any Booster tool via subprocess. |
| Self-correcting loop | 🟡 PARTIAL | Eval reports violations but can't auto-fix. Manual iteration only. |
| Token efficiency | ✅ PASS | ~120 tokens for 10 rules. Fits small-context models. |
| Crash resilience | ✅ PASS | Atomic writes, corrupt state = fresh start, sandbox graceful degradation. |
| Security boundary honesty | ✅ PASS | Limitations documented verbatim in tool output. |
| **Overall** | **🟡 SHIPPABLE with caveats** | Core thesis testable. Autonomous workflow needs G-01 through G-03. |

### The Honest Claim

> **With the current Phase 0 code, a 4B model instructed to use `tutor learn`
> + `tutor eval` would likely produce better HTML than without.** The eval
> harness alone provides structured feedback that beats raw generation. The
> thesis is structurally sound.
>
> **But the model cannot autonomously use the Booster tools.** The tools
> designed specifically for small-model support are invisible from the CLI.
> This is the gap between "usable" and "the vision works as described."

---

## Execution Protocol

### P1 — Ship-blocking (estimate: 3 sessions)

| # | Work Item | Files | Est. |
|---|-----------|-------|------|
| PR-01 | `tutor booster` CLI — 4 subcommands (scratchpad, check, fewshot, lookahead) wrapping the Booster tools | `cli/booster.py` (new), `__main__.py` (register) | 1 session |
| PR-02 | `tutor learn` Booster integration — auto-inject few-shot when Booster active | `cli/learn.py` | 0.5 session |
| PR-03 | `tutor fix` — eval → fix → re-eval loop. Wire `socratic_debug.py` into a CLI command that reads violations, extracts PASS examples from class.yaml, and prints a fix-targeted prompt. | `cli/fix.py` (new), `grading/socratic_debug.py` (extend) | 1.5 sessions |

### P2 — Improvement (estimate: 2 sessions)

| # | Work Item | Files | Est. |
|---|-----------|-------|------|
| PR-04 | Add a ~4B class model to `registry/models.json` (e.g. Qwen2.5-4B, Gemma-4B if available) | `registry/models.json` | 0.2 session |
| PR-05 | `tutor curriculum` — output ordered class list for a track | `cli/curriculum.py` (new), `__main__.py` | 0.5 session |
| PR-06 | Sandbox error messages: surface machine-parseable error codes instead of tracebacks | `booster/sandbox.py` | 0.3 session |

### P3 — Polish (estimate: 0.5 session)

| # | Work Item | Files | Est. |
|---|-----------|-------|------|
| PR-07 | `.dockerignore` | project root (new) | 0.1 session |
| PR-08 | `harness.py` log instead of silent pass | `eval/harness.py` | 0.1 session |
| PR-09 | Cache registry reads in `health.py` | `mcp/health.py` | 0.1 session |

**Total estimate:** 5.5 sessions (P1: 3, P2: 2, P3: 0.5)

---

## Open Questions for Miguel

1. **Booster tool naming** — `tutor booster scratchpad`, `tutor booster check`,
   etc. Or shorter aliases (`tutor scratch`, `tutor verify`, `tutor show`)?
2. **`tutor fix` scope** — Should it auto-iterate (eval → fix → eval → fix
   until pass) or one-shot (eval → print fix suggestions → exit)?
3. **4B model selection** — Which specific model to add to registry?

