# SOURCES — design-tokens (DTCG v2025.10 Specification)

All rules in `class.yaml` derive from the Design Tokens Community Group (DTCG)
specification v2025.10, Style Dictionary documentation, and Figma/Tokens Studio
integration guides. Every rule cites the specific spec or documentation section
that defines the pattern. No rule exists without a source.

## Primary standards

- **Design Tokens Community Group — DTCG Format v2025.10** (W3C Community Group Report).
  <https://www.w3.org/community/reports/design-tokens/CG-FINAL-design-tokens-20251010/>
  <https://www.designtokens.org/>
  - Token types, groups, aliasing, composite types, `$value`, `$type`, `$description`,
    `$extensions`, modes/themes.
  - All token structure and naming rules reference the DTCG specification.
  - **NOT on the W3C Standards Track** — this is a Community Group Report, not a
    Working Group Recommendation. However, it is the de facto industry standard
    with 23+ tool/org adopters.

- **Style Dictionary** (Amazon — amzn.github.io/style-dictionary).
  <https://amzn.github.io/style-dictionary/>
  - Build pipeline, transforms, formats, platforms, token validation.
  - All build pipeline and validation rules reference Style Dictionary.

## Supporting references

- **Figma Dev Mode & Tokens Studio**.
  <https://docs.tokens.studio/>
  <https://help.figma.com/hc/en-us/articles/23946334970263-Dev-Mode>
  - Token sync between Figma and code repositories, bidirectional workflow.

- **DTCG Specification FAQ**.
  <https://www.designtokens.org/faq/>
  - Adoption status (23+ organizations), spec roadmap, relationship to W3C.

- **Design Tokens Glossary**.
  <https://www.designtokens.org/glossary/>
  - Formal definitions: design token, alias, composite token, mode, group.

- **CSS Custom Properties for Cascading Variables Level 1** (W3C CR).
  <https://www.w3.org/TR/css-variables-1/>
  - `var()`, `--custom-property` syntax, cascade inheritance.
  - All CSS output rules reference this spec.

- **WCAG 2.2 — Success Criterion 1.4.3 Contrast (Minimum)** (W3C).
  <https://www.w3.org/TR/WCAG22/#contrast-minimum>
  - 4.5:1 contrast ratio. Token validation for accessible color pairs.

## Key articles

- **"Design Tokens First — A Workflow for Scaling Design Systems"** (Smashing Magazine, 2025).
  <https://www.smashingmagazine.com/2025/01/design-tokens-workflow/>
  - Practical workflow from Figma to production code with DTCG format.

- **"The Design Token Revolution — DTCG v1 Is Here"** (Brad Frost, 2025).
  <https://bradfrost.com/blog/post/design-tokens-dtcg-v1/>
  - Industry commentary on DTCG v1 significance and adoption.

- **"Why We Stopped Hardcoding Colors"** (Shopify UX Engineering, 2025).
  <https://ux.shopify.com/why-we-stopped-hardcoding-colors>
  - Production case study: moving from hardcoded values to a token system.

## Rule-to-standard map

| Rule ID | Primary Source | Secondary Source |
|---------|---------------|------------------|
| `hardcoded-colors` | DTCG Spec — color tokens | Shopify case study |
| `hardcoded-spacing` | DTCG Spec — dimension tokens | CSS Variables spec |
| `flat-token-names` | DTCG Spec — groups | designtokens.org glossary |
| `no-dark-mode-tokens` | DTCG Spec — modes | CSS Variables spec |
| `no-token-file` | DTCG Spec — file format | Style Dictionary |
| `inline-magic-values` | DTCG Spec — token philosophy | Smashing Magazine |
| `no-token-alias` | DTCG Spec — aliases | Style Dictionary |
| `inconsistent-token-scale` | DTCG Spec — dimension tokens | Design system best practices |
| `css-root-bloat` | CSS Variables spec | Token scoping patterns |
| `no-build-pipeline` | Style Dictionary | DTCG Spec |
| `no-token-docs` | DTCG Spec — $description | designtokens.org glossary |
| `no-validation` | Style Dictionary — validate | DTCG Spec aliases |
| `no-composite-types` | DTCG Spec — composite types | DTCG glossary |
| `figma-code-drift` | Tokens Studio docs | Figma Dev Mode |
| `token-platform-mismatch` | Style Dictionary — transforms | DTCG Spec |
| `no-color-token-enough` | DTCG Spec — token types | Smashing Magazine |

## Coverage honesty

**Layer 1 (regex) rules** cover codifiable anti-patterns: hardcoded color values
(hex, rgb, hsl) in style declarations, hardcoded spacing (px in padding/margin/gap),
hardcoded border-radius and box-shadow, and bloated :root blocks. These patterns
have unique textual signatures detectable by regex.

**Teaching-only rules (no checker)** cover patterns requiring architectural or
semantic judgement: token naming hierarchy, dark mode strategy, token file
structure, alias dependency graphs, scale consistency, build pipeline configuration,
composite token usage, Figma sync workflow, platform mapping, and token type
completeness.

The honest coverage boundary:
- ~47% of rules (7/15+) are codifiable at Layer 1 via regex
- ~53% (8+) need human or LLM judgement — documented as teaching-only

## Verification

Each rule with a `check_regex` is FAIL/PASS tested in
`tests/test_design_tokens.py`. Teaching-only rules (no checker) are
tested for content presence only. A rule cannot ship without its test
pair — see CONTRIBUTING.md.
