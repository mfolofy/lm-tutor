# SOURCES — brushes (Web Accessibility)

All rules in `class.yaml` derive from **WCAG 2.2** (W3C Recommendation,
2023-10-05) and supporting standards. Every rule cites the specific Success
Criterion (SC) it codifies. No rule exists without a source.

## Primary standards

- **Web Content Accessibility Guidelines (WCAG) 2.2** — W3C Recommendation.
  <https://www.w3.org/TR/WCAG22/>
- **WCAG 2.2 Understanding docs** (per-SC rationale and techniques).
  <https://www.w3.org/WAI/WCAG22/Understanding/>
- **ARIA in HTML** (W3C) for accessible-name computation.
  <https://www.w3.org/TR/html-aria/>
- **WAI-ARIA 1.2** — role taxonomy and states.
  <https://www.w3.org/TR/wai-aria-1.2/>
- **HTML Living Standard** — element semantics.
  <https://html.spec.whatwg.org/multipage/>

## Brush-stroke research sources

Migrated from `projects/brush-stroke/docs/SOURCES.md` (compiled 2026-06-07 via
5 parallel research agents covering accessibility, color/typography,
layout/spacing, interaction/forms, visual hierarchy).

### Key 2026 papers supporting the thesis

| Paper | Source | Relevance |
|-------|--------|-----------|
| "Measuring the Semantic Accessibility Gap in LLM-Generated Web UIs" | ACM CHI 2026 | 541 semantic violations across 300 UIs. LLMs optimize render tree, generate near-zero accessibility tree info. |
| "Bridging the Visual Specification Gap in AI-generated UIs" | UC Berkeley MIMS 2026 | The "tacit ceiling" — you cannot prompt your way to better UI. |
| "AI-Generated UI Is Inaccessible by Default" | FrontendMasters 2026 | 10 distinct accessibility failures in AI sidebar UI. |
| "Good from Afar, But Far from Good: AI Prototyping" | NN/g 2025 | AI tools miss visual hierarchy, spacing, contrast, meaningful grouping. |
| "A11yAgent: Multi-Agent Framework for Accessible Web Code" | ACM W4A 2026 | Generate → detect → repair loop significantly reduces WCAG violations. |
| "Access Over Deception: Fighting Deceptive Patterns through Accessibility" | CHI 2026 | 3 dark patterns implicated by WCAG. |
| "Vibe Checker: Aligning Code Evaluation with Human Preference" | ICML 2026 | current pass@k misses non-functional instructions. |

### WebAIM Million 2026

- **95.9%** of top 1M homepages have WCAG failures
- **56.1 errors per page** — 10.1% increase YoY
- **First reversal** of 6 years of gradual improvement
- **Attributed to:** AI-assisted coding practices
- Source: AudioEye — "Why LLMs Can't Fix Accessibility"

### Anti-pattern catalogs

**Impeccable (Paul Bakaus, ex-Google Chrome DevRel):** 25 design anti-patterns
for AI-generated UI — AI Slop Tells (side-tab accent borders, gradient text,
purple/violet gradients, frozen fonts), Quality & A11y (cramped padding, flat
type hierarchy, low contrast, pure black/white).

**WCAG Failure Techniques (W3C Official):**
- F42 — Scripting events to emulate links
- F59 — div/span as UI controls
- F44 — tabindex mismatch with visual order
- F55 — Script removes focus on focus event
- F89 — Empty alt on linked images

## Per-brush data sources

| Brush | Primary Sources |
|-------|----------------|
| navigation-landmarks | WCAG 1.3.1, 2.4.1, 4.1.2, ARIA Authoring Practices, MDN |
| interactive-roles | WCAG 4.1.2, 2.1.1, F42, F59, HTML spec |
| heading-hierarchy | WCAG 1.3.1, 2.4.6, 2.4.10, NN/g, F43 |
| color-contrast | WCAG 1.4.3, 1.4.6, 1.4.11, WebAIM, oklch spec |
| spacing-system | Material Design M3, NN/g Proximity Principle |
| form-labels | WCAG 1.3.1, 3.3.2, 4.1.2, H44, H71, H93, F68 |
| card-hierarchy | NN/g, Material Design, Apple HIG |
| typography-scale | WCAG 1.4.4, 1.4.12, AFTDS (Frontiers 2026), Bringhurst |
| responsive-breakpoints | MDN, CSS specs, common device data |
| focus-management | WCAG 2.4.3, 2.4.7, 2.4.11, F44, F55, ARIA APG |
| touch-targets | WCAG 2.5.8 (new AA), Apple HIG, Material Design |
| semantic-tables | WCAG 1.3.1, H43, H63 |
| list-semantics | WCAG 1.3.1, H48 |
| skip-navigation | WCAG 2.4.1 |
| motion-animation | WCAG 2.3.3 |
| data-viz-a11y | WCAG 1.1.1, SVG ARIA |
| loading-skeleton | WCAG 4.1.3, ARIA 1.2 |
| performance-web-vitals | WCAG 2.2.2, Web Vitals |
| stacking-context | CSS Spec, MDN |
| error-states | WCAG 3.3.1, 3.3.4, ARIA 1.2 |
| i18n-rtl | WCAG 3.1.1, HTML Spec |
| input-patterns | WCAG 3.3.2, H44, H71 |

## Rule → Success Criterion map

| Rule id | WCAG SC | Level | Notes |
|---------|---------|-------|-------|
| `img-alt` | 1.1.1 Non-text Content | A | Every `<img>` needs a text alternative; `alt=""` marks decorative (H67). |
| `input-image-alt` | 1.1.1 Non-text Content | A | `<input type="image">` requires `alt` (H36). |
| `button-name` | 4.1.2 Name, Role, Value | A | Controls must expose an accessible name. |
| `empty-aria-label` | 4.1.2 Name, Role, Value | A | Empty `aria-label` silently defeats accessible name. |
| `link-name` | 2.4.4 Link Purpose (In Context) | A | Links need discernible text or accessible name (G91/H30). |
| `label-for-input` | 3.3.2 Labels or Instructions | A | Text inputs need programmatic label (H44/ARIA16). |
| `html-lang` | 3.1.1 Language of Page | A | Page language via `<html lang>` (H57). |
| `title-required` | 2.4.2 Page Titled | A | Descriptive non-empty `<title>` (H25). |
| `positive-tabindex` | 2.4.3 Focus Order | A | Positive tabindex overrides natural DOM order (F44). |
| `aria-live-valid` | 4.1.3 Status Messages | AA | `aria-live` accepts polite, assertive, or off. |
| `select-label` | 3.3.2 Labels or Instructions | A | Select menus need programmatic label. |
| `textarea-label` | 3.3.2 Labels or Instructions | A | Textareas need programmatic label. |
| `input-email-label` | 3.3.2 Labels or Instructions | A | Email inputs need label. |
| `input-password-label` | 3.3.2 Labels or Instructions | A | Password inputs need label. |
| `input-checkbox-label` | 3.3.2 Labels or Instructions | A | Checkboxes need label. |
| `input-radio-label` | 3.3.2 Labels or Instructions | A | Radio buttons need label. |
| `error-association` | 3.3.1 Error Identification | A | Error message must be programmatically associated. |
| `section-name` | 1.3.1 Info and Relationships | A | Sections need accessible name. |
| `nav-landmark` | 1.3.1 Info and Relationships | A | Use `<nav>` not `<div role="navigation">`. |
| `th-scope` | 1.3.1 Info and Relationships | A | Header cells need scope (H63). |
| `table-caption` | 1.3.1 Info and Relationships | A | Data tables should have a caption (H39). |
| `list-structure` | 1.3.1 Info and Relationships | A | Lists must contain only list item children (H48). |
| `skip-link` | 2.4.1 Bypass Blocks | A | First focusable element should be a skip link (G1). |
| `outline-none` | 2.4.7 Focus Visible | AA | Removing focus outline without replacement fails SC. |
| `viewport-meta` | 1.4.4 Resize Text | AA | Viewport meta needed for mobile text resize. |
| `input-autocomplete` | 3.3.2 Labels or Instructions | A | Personal info inputs should autocomplete. |
| `prefers-reduced-motion` | 2.3.3 Animation from Interactions | AAA | Animations must respect motion preference. |
| `dir-attribute` | 3.1.1 Language of Page | A | RTL languages need dir="rtl". |
| `color-contrast` | 1.4.3 Contrast Minimum | AA | 4.5:1 minimum ratio (3:1 for large text). |
| `heading-order` | 1.3.1 Info and Relationships | A | Sequential heading hierarchy, one h1. |
| `touch-target` | 2.5.8 Target Size Minimum | AA | 24×24px minimum target size. |
| `spacing-system` | 1.4.8 Visual Presentation | AAA | Consistent spacing scale for readability. |
| `typography-minimum` | 1.4.4 Resize Text | AA | 16px minimum body, 1.5 line-height, 80ch max. |

## Coverage honesty

**Layer 1 (selector/regex) rules** cover codifiable WCAG SCs with high
precision: attribute presence, ARIA roles, structural elements. They do **not**
cover SCs needing rendered-pixel computation, semantic judgement, or
cross-element analysis — those are handled by the per-class ``grader.py``
(Layer 1.5, Phase 0) or the LLM judge (Layer 2, Phase 1).

The honest coverage boundary for the 24-brush migration:
- ~40–50% of WCAG A/AA criteria are codifiable at Layer 1
- ~20% need computation (color ratios, dimensions, heading hierarchy)
- ~30–40% need human or LLM judgement (alt quality, helpful error messages)

## Verification

Each rule's `check_selector` / `check_regex` is FAIL/PASS tested in
`tests/test_brushes.py`. Grader-only rules (`deep_check: true`) are tested
separately in the grader test section. A rule cannot ship without its test
pair — see CONTRIBUTING.md.

## Per-class grader

`grader.py` (`tutor/classes/brushes/grader.py`) implements computation-heavy
WCAG checks: color-contrast ratio computation (WCAG formula), heading
hierarchy validation, touch-target sizing, typography minimums, and spacing
scale adherence. Called by the harness after Layer 1 checks when
`deep_check: true` rules are present.
