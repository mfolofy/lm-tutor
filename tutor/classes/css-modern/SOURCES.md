# SOURCES — css-modern (Modern CSS Platform Features)

All rules in `class.yaml` derive from W3C CSS specifications (Working Drafts through
Candidate Recommendations) and Interop 2026. Every rule cites the specific spec or
standard that defines the feature. No rule exists without a source.

## Primary standards

- **CSS Anchor Positioning Level 1** (W3C Working Draft, 2025-10-07).
  <https://www.w3.org/TR/2025/WD-css-anchor-position-1-20251007/>
  - `anchor()` function grammar, scope restrictions (inset properties only),
    fallback behavior, anchor-name/anchor-scope properties.
  - All js-tooltip, popover-js-reimpl rules reference this spec.

- **CSS Nesting Module Level 1** (W3C Candidate Recommendation).
  <https://www.w3.org/TR/css-nesting-1/>
  - `&` nesting syntax, @nest rule, relative selectors within nested blocks.
  - All flat-selectors-no-nesting rules reference this spec.

- **CSS Containment Module Level 3** (W3C Candidate Recommendation).
  <https://www.w3.org/TR/css-contain-3/>
  - Container queries (`@container`), container-type, container-name,
    container units (cqw, cqi, cqb, cqh).
  - All media-over-container rules reference this spec.

- **Selectors Level 4** (W3C Candidate Recommendation).
  <https://www.w3.org/TR/selectors-4/>
  - `:has()` relational pseudo-class, `:focus-visible` pseudo-class.
  - All js-has-workaround, focus-not-focus-visible rules reference this spec.

- **CSS Scroll-driven Animations Level 1** (W3C Working Draft).
  <https://www.w3.org/TR/scroll-animations-1/>
  - `animation-timeline: scroll()`, `animation-timeline: view()`,
    scroll-timeline, view-timeline CSS properties.
  - All js-scroll-animation rules reference this spec.

- **CSS Text Module Level 4** (W3C Working Draft).
  <https://www.w3.org/TR/css-text-4/>
  - `text-wrap: balance`, `text-wrap: pretty`, `text-wrap: stable`.
  - All long-headline-no-balance rules reference this spec.

- **CSS Grid Layout Module Level 2** (W3C Candidate Recommendation).
  <https://www.w3.org/TR/css-grid-2/>
  - `subgrid` value for `grid-template-columns` and `grid-template-rows`.
  - All no-subgrid rules reference this spec.

- **CSS Cascading and Inheritance Level 5** (W3C Candidate Recommendation).
  <https://www.w3.org/TR/css-cascade-5/>
  - `@layer` at-rule syntax, layer ordering, layer merging, `revert-layer`.
  - All no-cascade-layer rules reference this spec.

- **CSS Logical Properties and Values Level 1** (W3C Candidate Recommendation).
  <https://www.w3.org/TR/css-logical-1/>
  - inline-size, block-size, margin-inline, padding-block, border-inline-start,
    and all flow-relative property mappings.
  - All physical-not-logical rules reference this spec.

- **CSS Values and Units Module Level 4** (W3C Candidate Recommendation).
  <https://www.w3.org/TR/css-values-4/>
  - Viewport-relative units: dvh, svh, lvh, dvw, svw, lvw, vi, vb.
  - `min()`, `max()`, `clamp()` math functions.
  - All 100vh-viewport-bug, px-font-size rules reference this spec.

## HTML platform APIs (CSS-adjacent)

- **HTML Living Standard — Popover API** (WHATWG).
  <https://html.spec.whatwg.org/multipage/popover.html>
  - `[popover]` attribute, `popovertarget`, `popoveraction`, `::backdrop`.
  - All popover-js-reimpl rules reference this spec.

- **HTML Living Standard — dialog element** (WHATWG).
  <https://html.spec.whatwg.org/multipage/interactive-elements.html#the-dialog-element>
  - `<dialog>`, `showModal()`, `show()`, `close()`, `::backdrop`.
  - All div-modal rules reference this spec.

- **HTML Living Standard — inert attribute** (WHATWG).
  <https://html.spec.whatwg.org/multipage/interaction.html#the-inert-attribute>
  - `inert` global attribute — removes element from accessibility tree,
    focus order, and hit-testing.
  - All no-inert rules reference this spec.

- **HTML Living Standard — lazy loading** (WHATWG).
  <https://html.spec.whatwg.org/multipage/urls-and-fetching.html#lazy-loading-attributes>
  - `loading="lazy"` and `loading="eager"` on `<img>` and `<iframe>`.
  - All no-lazy-loading rules reference this spec.

- **HTML Living Standard — fetchpriority** (WHATWG).
  <https://html.spec.whatwg.org/multipage/urls-and-fetching.html#fetch-priority-attributes>
  - `fetchpriority="high"|"low"|"auto"` on `<img>`, `<link>`, `<script>`.
  - All no-fetchpriority-lcp rules reference this spec and the LCP spec.

## Color specifications

- **CSS Color Module Level 4** (W3C Candidate Recommendation).
  <https://www.w3.org/TR/css-color-4/>
  - `oklch()`, `oklab()`, `color()` function, P3/Display P3 color space.
  - All hex-over-oklch rules reference this spec.

- **CSS Color Module Level 5** (W3C Editor's Draft, 2026-06-05).
  <https://drafts.csswg.org/css-color-5/>
  - `color-mix()`, `contrast-color()`, Relative Color Syntax.
  - All hex-over-oklch rules (color manipulation aspects) reference this spec.

- **CSS Color Adjustment Module Level 4** (W3C Candidate Recommendation).
  <https://www.w3.org/TR/css-color-adjust-4/>
  - `color-scheme`, `forced-color-adjust`, `print-color-adjust`.
  - All no-color-scheme rules reference this spec.

## UI theming

- **CSS Basic User Interface Module Level 4** (W3C Candidate Recommendation).
  <https://www.w3.org/TR/css-ui-4/>
  - `accent-color` property for themed form controls.
  - All no-accent-color rules reference this spec.

## Interop commitments

- **Interop 2026** — Cross-browser interoperability initiative.
  <https://web.dev/interop-2026/>
  - Includes: Anchor Positioning, View Transitions, `contrast-color()`,
    Container Queries, `@starting-style`, scroll-driven animations,
    CSS Nesting, `text-wrap: balance`.
  - Referenced as the practical shipping signal for features still in WD/CR.

## CSS font sizing

- **CSS Fonts Module Level 4** (W3C Candidate Recommendation).
  <https://www.w3.org/TR/css-fonts-4/>
  - `font-size` with relative units, `rem`, user preference cascade.
  - Referenced by px-font-size, no-lazy-loading rules.

## Key papers and articles

- **"CSS Anchor Positioning — A New Way to Position Popovers"** (web.dev, 2025).
  <https://web.dev/anchor-positioning/>
  - Practical guide to anchor positioning replacing JS popover libraries.

- **"View Transitions API — Smooth Page Transitions Without JavaScript"** (MDN, 2025).
  <https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API>

- **"The Popover API — Finally, a Native Popup"** (Chrome Developers, 2025).
  <https://developer.chrome.com/docs/css-ui/popover-api>

- **WebAIM Million 2026** — 95.9% of top 1M homepages have WCAG failures.
  <https://webaim.org/projects/million/>
  - Directly relevant: many failures stem from JS-reimplemented native features
    that break accessibility (div modals, custom form controls, JS tooltips).

## Rule-to-standard map

| Rule ID | Primary Standard | Secondary Source |
|---------|-----------------|------------------|
| `js-tooltip` | CSS Anchor Positioning Level 1 (WD) | web.dev anchor positioning guide |
| `no-lazy-loading` | WHATWG HTML — lazy loading | web.dev performance |
| `focus-not-focus-visible` | Selectors Level 4 (CR) | MDN :focus-visible |
| `important-cascade-war` | CSS Cascading Level 5 (CR) | MDN @layer |
| `div-modal` | WHATWG HTML — dialog element | MDN dialog |
| `100vh-viewport-bug` | CSS Values 4 (CR) — viewport units | web.dev dvh guide |
| `hex-over-oklch` | CSS Color Level 4 (CR) + Level 5 (ED) | oklch.com, MDN |
| `no-accent-color` | CSS UI Level 4 (CR) | MDN accent-color |
| `no-color-scheme` | CSS Color Adjust Level 4 (CR) | MDN color-scheme |
| `no-inert` | WHATWG HTML — inert attribute | MDN inert |
| `popover-js-reimpl` | WHATWG HTML — Popover API | Chrome Developers |
| `long-headline-no-balance` | CSS Text Level 4 (WD) | MDN text-wrap |
| `physical-not-logical` | CSS Logical Properties Level 1 (CR) | MDN logical properties |
| `media-over-container` | CSS Containment Level 3 (CR) | MDN @container |
| `no-subgrid` | CSS Grid Level 2 (CR) | MDN subgrid |
| `px-font-size` | CSS Fonts Level 4 (CR) + WCAG 1.4.4 | MDN font-size |
| `no-fetchpriority-lcp` | WHATWG HTML — fetchpriority | web.dev LCP, MDN |
| `js-scroll-animation` | Scroll-driven Animations Level 1 (WD) | MDN animation-timeline |
| `no-starting-style` | CSS Transitions (CR) + Interop 2026 | MDN @starting-style |
| `flat-selectors-no-nesting` | CSS Nesting Level 1 (CR) | MDN CSS nesting |
| `no-cascade-layer` | CSS Cascading Level 5 (CR) | MDN @layer |
| `js-has-workaround` | Selectors Level 4 (CR) | MDN :has() |

## Coverage honesty

**Layer 1 (selector/regex) rules** cover codifiable CSS anti-patterns with high
precision: missing `loading="lazy"`, `:focus` without `:focus-visible`,
`!important`, div-based modals, `100vh`, hex color codes, JS tooltip/popover
libraries, `font-size: Npx`, missing `fetchpriority`, and JS scroll listeners
for animation. These patterns have a unique textual or structural signature.

**Teaching-only rules (no checker)** cover standards that require semantic
judgement beyond selector/regex scope: cascade layer strategy, CSS nesting
preference (vs flat selectors), `:has()` parent-styling (vs JS class toggling),
logical property adoption (context-dependent), subgrid alignment (layout-level),
scroll-driven animation intent (vs JS), `@starting-style` entry patterns
(context of what is being animated), and `@container` vs `@media` intent.

The honest coverage boundary:
- ~55% of rules (12/22) are codifiable at Layer 1 via selector or regex
- ~45% (10/22) need human or LLM judgement — documented as teaching-only

## Verification

Each rule with a `check_selector` or `check_regex` is FAIL/PASS tested in
`tests/test_css_modern.py`. Teaching-only rules (no checker) are tested for
content presence only. A rule cannot ship without its test pair — see
CONTRIBUTING.md.
