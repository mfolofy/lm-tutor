# SOURCES — web-vitals (Core Web Vitals & Performance)

## Primary standards

- **web.dev/vitals** — Core Web Vitals. <https://web.dev/vitals/>
- **MDN Web Docs** — Performance. <https://developer.mozilla.org/en-US/docs/Web/Performance>
- **W3C Event Timing API**. <https://www.w3.org/TR/event-timing/>
- **Lighthouse CI docs**. <https://github.com/GoogleChrome/lighthouse-ci>

## Rule-to-standard map

| Rule ID | Primary Source |
|---------|---------------|
| `no-lcp-priority` | web.dev — LCP optimization |
| `no-image-dimensions` | web.dev — CLS optimization |
| `no-font-display` | MDN — @font-face, web.dev — font-best-practices |
| `render-blocking-scripts` | MDN — script element, web.dev |
| `no-preconnect` | MDN — preconnect, web.dev |
| `long-task-over-50ms` | web.dev — INP optimization |
| `no-srcset` | MDN — responsive images |
| `no-bfcache-test` | web.dev — bfcache |
| `no-speculation-rules` | Chrome DevTools — Speculation Rules API |
| `no-lazy-below-fold` | MDN — loading attribute |
| `no-inp-measurement` | web.dev — INP |
| `hydration-blocking-tti` | web.dev — TTI, Astro — Partial Hydration |

## Coverage: ~50% Layer 1, ~50% teaching-only. Verified in tests/test_web_vitals.py.
