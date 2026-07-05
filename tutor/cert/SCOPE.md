# tutor.cert — Constrained-Decoding Certificate (Phase 2)

## What this is

A **certificate** proves that a compiled [Outlines](https://github.com/dottxt-ai/outlines)
constraint makes a **logits-controlled local decoder** produce output that is
*provably* a member of the **complement** of a specific `class.yaml`
`check_regex` R — i.e. the grader's own `re.finditer(R, output)` can never
match. Because regular languages are closed under complement, for a truly
regular R this is exactly a DFA: `constraint = (Σ*·R·Σ*).everythingbut()`.

The deliverable is **Layer A** (structural, model-free): the DFA construction
plus three proofs, materialized as committed JSON certificates. **Layer B**
(a real small model driven by Outlines) only *demonstrates* the mechanism.

## The guarantee — and its exact limits (READ THIS)

For a rule certified `EXACT`, on a **logits-controlled LOCAL decoding path**,
output produced under the certificate's constraint is provably in the
complement of that rule's `check_regex`. That is **invariance of the grader's
own check for that one rule**, proven by DFA-intersection emptiness.

It is **NOT**:

- **Not semantic safety.** A homoglyph such as a Cyrillic `рrint(` (U+0440)
  passes *both* the grader and the certificate — the guarantee is about the
  grader's literal regex, not intent.
- **Not a guarantee about any other rule** — one certificate, one rule id.
- **Not for API-model submissions.** opencode/Claude and any other
  non-logits path remain **detect-only forever**; there is no way to
  constrain their token distribution, so the certificate simply does not
  apply to them.
- **Modulo Outlines** correctly enforcing the char-level DFA at the token
  level (the char-DFA is what we prove; token-level enforcement is Outlines').

## The three proofs (Layer A)

| Proof | What it establishes | How |
|-------|--------------------|-----|
| **A1 Emptiness** (symbolic) | No string the constraint accepts is a grader violation (soundness) | `L(constraint) ∩ L(Σ*RΣ*) == ∅` via greenery DFA intersection + emptiness |
| **A2 Fidelity** (differential fuzz) | Our forbidden-language FSM equals Python `re` semantics | 10⁵ seeded strings incl. adversarial start/end-boundary, char-adjacent-to-`\b`, Unicode-word, and empty-string cases; FSM vs `re.search`. A "FSM says clean, Python says violation" divergence = **forbid-less = HARD FAIL** → equivalence forced to `NONE` |
| **A3 Grader-in-the-loop** (real harness) | The actual scorer agrees | Walk accepting strings of the constraint FSM through the **real** `tutor.eval.harness.grade`; the certified rule must fire **zero** times |

**Equivalence verdict:** any forbid-less divergence → `NONE` (rejected); else
if the constraint forbids a strict superset → `SOUND_OVERAPPROX`; else `EXACT`.
A rewritten/complemented constraint that forbids **less** than the grader is a
**false certificate** and is rejected — never silently passed.

## Semantic-fidelity guards in the rewriter (`rewrite.py`)

greenery's regex parser rejects `(?i)`, `\b`, and lookaround outright, so the
rewriter hand-expands exactly those into an exact `Σ*RΣ*` forbidden-language
regex. Constructs it cannot handle exactly return `NONE` (never a guess).
Two divergences from Python `re` were **caught by the A2 fuzz and fixed**:

1. Python's `\w`/`\d`/`\s`/`\b` are **Unicode-aware** by default; greenery's
   are **ASCII-only**. Rewriter substitutes precise Unicode codepoint ranges
   (computed once from CPython's own `re` engine, `unicode_word_ranges.json`)
   for every `\w`/`\d`/`\s`/`\W`/`\D`/`\S` — greenery never sees the
   shorthand. (Live catch: `éprint(` — Python's `(?<![.\w])` correctly
   refuses to match since `é` is a Python `\w` char; the naive rewrite said
   it should.)
2. A bare unescaped `.` — greenery's `.` matches newline, Python's default
   `.` does not (no `re.DOTALL`) — is **refused**, not passed through.

## MEASURED tier split (from the sweep — NOT a ceiling)

`python -m tutor.cert.compile` sweeps every `check_regex` rule in
`tutor/classes/*/class.yaml`. Measured on this tree:

| Metric | Count |
|--------|-------|
| Total checkable rules (harness `rules_checked`, dedup) | **253** |
| — of which carry a `check_regex` | **230** |
| — of which carry a `check_selector` | **24** (one rule carries both) |
| `check_regex` rules that **compile** to a constraint FSM (Tier A) | **34** |
| `check_regex` rules that do **not** compile (Tier NONE) | **196** |
| **Rules certified `EXACT`** (Layer A, this phase) | **3** |

> Note on 253 vs 254: 253 is the harness's own dedup count; a naive
> "regex-rules + selector-rules" sum double-counts the one rule
> (`css-modern/js-tooltip`) carrying both keys → 254. See
> `tutor/cert/sweep_report.py`.

"Compiles" (Tier A) is necessary but **not sufficient** for `EXACT` — the A1/
A2/A3 proofs decide `EXACT` vs. `SOUND_OVERAPPROX` vs. rejected. This phase
certifies **3** rules `EXACT` (the plan's targets); the remaining 31 Tier-A
rules are compile-eligible but not yet proof-driven.

## The 3 certified rules

| Rule | Source construct | Equivalence |
|------|------------------|-------------|
| `brushes/positive-tabindex` | plain regex, no anchors | `EXACT` |
| `architect/single-operator-mode` | `(?i)` expansion + trailing `\b` | `EXACT` |
| `architect/print-logging` | single-char-class negative lookbehind `(?<![.\w])` | `EXACT` |

Certificates: `tutor/cert/certs/*.json`. Regenerate:
`python -m tutor.cert.certificate`. Re-verify (core + greenery only):
`pytest tests/test_cert_structural.py`.

## Decoder

Outlines (**not** XGrammar — XGrammar is CFG/JSON-schema and has no complement
op). Pipeline: rule regex → `rewrite` (`\b`, `(?i)`, alphabet) → greenery FSM →
`.everythingbut()` (complement) → constraint DFA → Outlines positive
constraint. Layer B deps are optional: `pip install -e '.[cert]'`; core stays
stdlib + pydantic + pyyaml.
