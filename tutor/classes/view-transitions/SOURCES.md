# SOURCES — view-transitions (View Transitions API Levels 1 & 2)

All rules in `class.yaml` derive from W3C CSS specifications, MDN documentation,
and browser release notes. Every rule cites the specific spec that defines the
feature. No rule exists without a source.

## Primary standards

- **CSS View Transitions Module Level 1** (W3C Candidate Recommendation).
  <https://www.w3.org/TR/css-view-transitions-1/>
  - `document.startViewTransition()`, `view-transition-name`, `::view-transition-old()`,
    `::view-transition-new()`, `::view-transition-group()`, `::view-transition-image-pair()`.
  - All SPA view transitions rules reference this spec.

- **CSS View Transitions Module Level 2** (W3C Editor's Draft, 2026-04-29).
  <https://drafts.csswg.org/css-view-transitions-2/>
  - Cross-document (MPA) transitions (`@view-transition` rule), scoped element
    transitions (`Element.startViewTransition()`), `view-transition-class`,
    `:active-view-transition-type()`.
  - All MPA, scoped, and type-based transition rules reference this spec.

- **MDN Web Docs — View Transitions API**.
  <https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API>
  - Comprehensive API reference, browser support matrix, usage examples.

## Supporting references

- **Chrome 147 Release Notes** (March 2026).
  - `Element.startViewTransition()` shipped stable, cross-document transitions
    in stable, `view-transition-class` shipped.

- **Interop 2026 — View Transitions focus area**.
  <https://web.dev/interop-2026/>
  - Cross-document view transitions, `@view-transition` rule, scoped transitions
    committed by all major browser vendors.

- **WICG scoped-transitions explainer**.
  <https://github.com/WICG/view-transitions/blob/main/scoped-transitions.md>
  - `Element.startViewTransition()` design rationale and use cases.

- **CSS Transitions Level 1** (W3C Working Draft).
  <https://www.w3.org/TR/css-transitions-1/>
  - `@starting-style` at-rule for entry transition initial states.

- **Media Queries Level 5** (W3C Candidate Recommendation).
  <https://www.w3.org/TR/mediaqueries-5/>
  - `prefers-reduced-motion: reduce` media feature (WCAG 2.2 SC 2.3.3).

- **Navigation API** (W3C Working Draft).
  <https://www.w3.org/TR/navigation-api/>
  - `navigation.addEventListener('navigate')`, `navigationType: 'traverse'`
    for back/forward detection.

## Key articles

- **"Smooth and simple transitions with the View Transitions API"** (Chrome Developers, 2025).
  <https://developer.chrome.com/docs/web-platform/view-transitions/>
  - Practical tutorial covering SPA transitions, MPA transitions, and debugging.

- **"View Transitions Level 2 — Cross-Document Transitions"** (CSS-Tricks Almanac, 2026).
  <https://css-tricks.com/almanac/at-rules/view-transition/>
  - Quick reference for `@view-transition` syntax and usage.

- **"Animating Multi-Page Apps with View Transitions"** (web.dev, 2026).
  <https://web.dev/view-transitions-mpa/>
  - Migration guide from JS animation libraries to View Transitions for MPA.

## Rule-to-standard map

| Rule ID | Primary Source | Secondary Source |
|---------|---------------|------------------|
| `js-router-transition` | CSS View Transitions Level 1 | MDN |
| `no-view-transition-name` | CSS View Transitions Level 1 | MDN |
| `no-mpa-transition` | CSS View Transitions Level 2 | Chrome 147 |
| `no-reduced-motion-check` | Media Queries Level 5 | WCAG 2.2 SC 2.3.3 |
| `no-fallback` | CSS View Transitions Level 1 | MDN |
| `old-new-pseudo-missing` | CSS View Transitions Level 1 | MDN |
| `js-animation-library-page` | CSS View Transitions Level 1 | web.dev |
| `scoped-transition-missed` | CSS View Transitions Level 2 | Chrome 147, WICG |
| `wrong-transition-type` | CSS View Transitions Levels 1 & 2 | MDN, web.dev |
| `no-view-transition-class` | CSS View Transitions Level 2 | MDN |
| `hardcoded-duration` | CSS View Transitions Level 1 | MDN |
| `no-types-config` | CSS View Transitions Level 2 | MDN |
| `group-elements-missed` | CSS View Transitions Level 1 | MDN |
| `back-navigation-broken` | Navigation API WD | MDN |
| `no-error-handling` | CSS View Transitions Level 1 | MDN |

## Coverage honesty

**Layer 1 (regex) rules** cover codifiable patterns: JS SPA router animation
libraries (AnimatePresence, CSSTransition, Vue <Transition>), missing
prefers-reduced-motion checks, JS animation library page transitions,
and hardcoded animation durations.

**Teaching-only rules (no checker)** cover patterns requiring semantic
judgement: element naming strategy (view-transition-name), MPA transition
configuration, animation customization (keyframes), scoped transition
boundaries, type-based animation routing, class grouping, element group
containment, and navigation direction detection.

The honest coverage boundary:
- ~40% of rules (6/15) are codifiable at Layer 1 via regex
- ~60% (9/15) need human or LLM judgement — documented as teaching-only

## Verification

Each rule with a `check_regex` is FAIL/PASS tested in
`tests/test_view_transitions.py`. Teaching-only rules (no checker) are
tested for content presence only. A rule cannot ship without its test
pair — see CONTRIBUTING.md.
