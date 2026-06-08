# SOURCES — brushes (Web Accessibility)

All rules in `class.yaml` derive from **WCAG 2.2** (W3C Recommendation,
2023-10-05). Every rule cites the specific Success Criterion (SC) it codifies.
No rule exists without a source. This file is the audit trail.

## Primary standard

- **Web Content Accessibility Guidelines (WCAG) 2.2** — W3C Recommendation.
  <https://www.w3.org/TR/WCAG22/>
- **WCAG 2.2 Understanding docs** (per-SC rationale and techniques).
  <https://www.w3.org/WAI/WCAG22/Understanding/>
- **ARIA in HTML** (W3C) for the accessible-name computation referenced by the
  button/link rules. <https://www.w3.org/TR/html-aria/>
- **WAI-ARIA 1.2** for `aria-live` token values.
  <https://www.w3.org/TR/wai-aria-1.2/>

## Rule → Success Criterion map

| Rule id | WCAG SC | Level | Source notes |
|---------|---------|-------|--------------|
| `img-alt` | 1.1.1 Non-text Content | A | Every `<img>` needs a text alternative; `alt=""` marks a decorative image (Understanding 1.1.1, technique H67). |
| `input-image-alt` | 1.1.1 Non-text Content | A | `<input type="image">` is a control with non-text content — requires `alt` (technique H36). |
| `button-name` | 4.1.2 Name, Role, Value | A | Controls must expose an accessible name. A `<button>` gets it from text content, `aria-label`, or `aria-labelledby` (ARIA-in-HTML accessible-name computation). |
| `empty-aria-label` | 4.1.2 Name, Role, Value | A | An empty `aria-label` supplies no name and silently defeats the control's text — a common anti-pattern. |
| `link-name` | 2.4.4 Link Purpose (In Context) | A | Links must have discernible text or an accessible name (technique G91 / H30). |
| `label-for-input` | 3.3.2 Labels or Instructions | A | Text inputs need a programmatic label: `<label for>`, `aria-label`, or `aria-labelledby` (technique H44 / ARIA16). |
| `html-lang` | 3.1.1 Language of Page | A | The page's default human language must be programmatically set via `<html lang>` (technique H57). |
| `title-required` | 2.4.2 Page Titled | A | Pages need a descriptive, non-empty `<title>` (technique H25). |
| `positive-tabindex` | 2.4.3 Focus Order | A | Positive `tabindex` overrides natural DOM focus order and is a documented failure (technique F44 — failure due to using `tabindex` to give a non-sequential order). |
| `aria-live-valid` | 4.1.3 Status Messages | AA | `aria-live` accepts only `polite`, `assertive`, or `off` (WAI-ARIA 1.2 value space). |

## Coverage honesty

These 10 rules cover **codifiable** WCAG SCs that a deterministic
selector/regex check can verify with high precision. They do **not** cover
SCs requiring human judgment — colour-contrast ratios (1.4.3, needs rendered
pixels), meaningful alt-text quality (1.1.1 beyond presence), reading order,
or whether an error message is actually helpful (3.3.3). Those are deferred to
the Layer 2 LLM judge (Phase 1). This is the honest coverage boundary: roughly
40–50% of WCAG A/AA criteria are codifiable at Layer 1.

## Verification

Each rule's `check_selector` / `check_regex` is paired with FAIL and PASS
examples inside `class.yaml`. The test file (`tests/test_brushes.py`, added per
CONTRIBUTING.md) asserts that the FAIL examples produce the violation and the
PASS examples do not — the rule cannot enter production without that test.
