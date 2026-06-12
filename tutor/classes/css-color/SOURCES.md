# SOURCES — css-color (Modern CSS Color)

All rules derive from W3C CSS Color specifications and Interop 2026 commitments.

## Primary standards

- **CSS Color Module Level 4** (W3C Candidate Recommendation).
  <https://www.w3.org/TR/css-color-4/>
  - `oklch()`, `oklab()`, `color()` function, P3/Display P3 color space,
    predefined color spaces, named colors deprecation guidance.

- **CSS Color Module Level 5** (W3C Editor's Draft, 2026-06-05).
  <https://drafts.csswg.org/css-color-5/>
  - `color-mix()`, `contrast-color()`, `color-contrast()`, Relative Color Syntax
    (RCS), `light-dark()`. CSSWG Resolution #10484 (March 2026): oklab is the
    default interpolation color space for `color-mix()`.

- **CSS Color Adjustment Module Level 4** (W3C Candidate Recommendation).
  <https://www.w3.org/TR/css-color-adjust-4/>
  - `color-scheme` property, `forced-color-adjust`.

- **Interop 2026** — Cross-browser interoperability dashboard.
  <https://web.dev/interop-2026/>
  - `contrast-color()` committed by Chrome, Firefox, Safari.

## Supporting references

- **WebKit Blog — "contrast-color(): Auto Text on Any Background"**.
  <https://webkit.org/blog/16929/contrast-color/>
  - Safari 26.0 implementation details and usage examples.

- **"OKLCH Color Picker & Converter"** (oklch.com).
  <https://oklch.com/>
  - Interactive tool for exploring the oklch color space.

- **"Why OKLCH Is Better Than HSL for Design Systems"** (Evil Martians, 2024).
  <https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl>
  - Practical case for oklch over hsl/rgb with real design system examples.

- **"P3 Color on the Web"** (web.dev, 2025).
  <https://web.dev/display-p3/>
  - Progressive enhancement pattern for wide-gamut colors with sRGB fallback.

- **WCAG 2.2 — Success Criterion 1.4.3** (W3C).
  <https://www.w3.org/TR/WCAG22/#contrast-minimum>
  - 4.5:1 minimum contrast ratio, relevant to `contrast-color()` usage.

## Rule-to-standard map

| Rule ID | Primary Source | Secondary Source |
|---------|---------------|------------------|
| `hex-rgb-over-oklch` | CSS Color Level 4 — oklch() | Evil Martians |
| `hsl-over-oklch` | CSS Color Level 4 — oklch() | oklch.com |
| `no-color-mix` | CSS Color Level 5 — color-mix() | CSSWG #10484 |
| `no-oklch-default` | CSSWG Resolution #10484 | CSS Color Level 5 |
| `no-contrast-color` | CSS Color Level 5 — contrast-color() | WebKit blog, Interop 2026 |
| `no-light-dark` | CSS Color Level 5 — light-dark() | CSS Color Adjust 4 |
| `hardcoded-dark-values` | CSS Color Level 5 — RCS | Evil Martians |
| `srgb-only-no-p3` | CSS Color Level 4 — color()/P3 | web.dev P3 guide |
| `opacity-over-alpha` | CSS Color Level 4 — alpha | MDN |
| `named-colors` | CSS Color Level 4 — named colors | MDN |
| `no-relative-color` | CSS Color Level 5 — RCS | MDN |
| `no-color-scheme-property` | CSS Color Adjust Level 4 | MDN |

## Coverage honesty

**Layer 1 (regex) rules** cover: hex/rgb in custom property definitions, hsl()/hsla()
usage, hardcoded dark mode overrides, named CSS colors, and missing color-scheme
on :root. These patterns have unique textual signatures.

**Teaching-only rules** cover: color-mix() strategy, oklch default interpolation
rationale, contrast-color() usage context, Relative Color Syntax patterns,
P3 progressive enhancement, and alpha-channel vs opacity decisions. These
require semantic or design-system-level judgement.

~58% of rules (7/12) are codifiable at Layer 1. ~42% (5/12) are teaching-only.

## Verification

Each rule with a `check_regex` is FAIL/PASS tested in `tests/test_css_color.py`.
