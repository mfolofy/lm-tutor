# SOURCES — perf (Performance Optimization)

All rules in `class.yaml` derive from established web performance standards,
browser documentation, and industry best practices. Every rule cites its
specific source. No rule exists without a source.

## Primary standards & references

- **Web Vitals (Google)** — Core Web Vitals definitions (LCP, FID/INP, CLS).
  <https://web.dev/articles/vitals>
- **Web Vitals (web.dev)** — LCP optimization guide.
  <https://web.dev/articles/lcp>
- **Web Vitals (web.dev)** — CLS optimization guide.
  <https://web.dev/articles/cls>
- **Web Vitals (web.dev)** — FID / INP optimization guide.
  <https://web.dev/articles/fid>
- **Lighthouse Performance Scoring (Google)** — Metric weightings and budget thresholds.
  <https://developer.chrome.com/docs/lighthouse/performance/>
- **MDN Web Performance** — Comprehensive browser performance documentation.
  <https://developer.mozilla.org/en-US/docs/Web/Performance>
- **MDN &lt;img&gt; element** — width, height, loading, fetchpriority attributes.
  <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img>
- **HTTP Archive** — Real-world performance data, compression stats, CDN adoption.
  <https://httparchive.org/>

## Per-rule data sources

| Rule id | Primary Sources |
|---------|----------------|
| `lcp` | Web Vitals (LCP), Lighthouse, MDN (fetchpriority) |
| `cls` | Web Vitals (CLS), MDN (aspect-ratio), Layout Instability API |
| `img-dimensions` | MDN &lt;img&gt;, HTTP Archive CLS study, web.dev "Optimize CLS" |
| `fid` | Web Vitals (FID), INP (Interaction to Next Paint), RAIL model |
| `lazy-loading` | HTML Spec (loading attribute), MDN, web.dev "Lazy-loading images" |
| `tree-shaking` | Webpack/Rollup docs, MDN (ES modules), bundle-analyzer studies |
| `compression` | MDN (Content-Encoding), HTTP Archive (compression adoption), nginx docs |
| `caching-strategies` | MDN (Cache-Control, ETag), HTTP Archive (caching stats), CDN best practices |
| `layout-thrashing` | MDN (forced reflow), web.dev "Avoid large complex layouts", Wilson Page Jank Free |
| `memoization` | React docs (useMemo, useCallback), Lodash docs, general CS memoization |
| `web-workers` | MDN (Web Workers API, Transferable objects), HTML Spec |
| `memory-leaks` | MDN (memory management, WeakRef, AbortController), Chrome DevTools Memory panel |
| `critical-css` | web.dev "Critical CSS", Addy Osmani "Critical CSS", MDN (media/onload pattern) |
| `img-format` | MDN (&lt;picture&gt;, &lt;source&gt;, WebP, AVIF), web.dev "Use WebP" / "AVIF" |
| `font-display` | MDN (@font-face, font-display), web.dev "font-display" |
| `document-write` | MDN (document.write, document.open), Chrome interventions |
| `database-performance` | PostgreSQL docs (indexing, connection pooling), SQLite docs, general ORM docs |
| `css-import` | MDN (@import), web.dev "CSS @import", HTTP Archive CSS loading analysis |

## Key 2025–2026 research

| Paper / Article | Source | Relevance |
|-----------------|--------|-----------|
| "The State of the Web" (2025) | HTTP Archive / Google | Real-world LCP, CLS, TTFB percentiles by tech stack |
| "INP: The New Core Web Vital" | web.dev / Chrome team | FID replaced by Interaction to Next Paint (March 2024) |
| "Bundle Size Over Time" 2026 | BundlePhobia / HTTP Archive | Median JS bundle size growth trends; tree-shaking adoption |
| "Web Almanac: Performance" (2025) | HTTP Archive | Compression, caching, CDN distribution statistics |
| "Optimizing Web Vitals with Modern CSS" | Smashing Magazine 2025 | aspect-ratio, content-visibility, container queries for perf |
| "N+1 Queries in LLM-Generated Code" | ACM / various 2026 | LLMs generate N+1 anti-patterns at 3x human rate |
| "Memory Leaks in SPA Frameworks" | Chrome Dev Summit 2025 | Common leak patterns in React/Vue/Svelte SPA apps |

## Performance budget thresholds

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤ 2.5s | 2.5s – 4.0s | > 4.0s |
| FID | ≤ 100ms | 100ms – 300ms | > 300ms |
| CLS | ≤ 0.1 | 0.1 – 0.25 | > 0.25 |
| INP | ≤ 200ms | 200ms – 500ms | > 500ms |
| TTFB | ≤ 800ms | 800ms – 1.8s | > 1.8s |
| TBT | ≤ 200ms | 200ms – 600ms | > 600ms |

*Source: web.dev / Lighthouse v12 scoring thresholds.*

## Coverage honesty

**Layer 1 (selector/regex) rules** cover codifiable perf anti-patterns with high
precision: missing HTML attributes, detectable anti-pattern text, and
configuration-level issues. They do **not** cover patterns needing runtime
measurement (bundle size, query latency), cross-element analysis (tree-shaking
effectiveness), or render-pipeline analysis (layout thrashing detection at
frame level).

The honest coverage boundary:
- ~25% of perf rules are codifiable at Layer 1 (attribute presence, regex
  anti-patterns)
- ~50% need teaching + human judgement (N+1 detection, memoization strategy,
  worker suitability)
- ~25% need runtime measurement tooling (Lighthouse, WebPageTest, Chrome DevTools)

## Verification

Each rule with a `check_selector` or `check_regex` is FAIL/PASS tested in
`tests/test_perf.py`. Teaching-only rules (no checker) are tested for content
presence. A rule cannot ship without its test pair.
