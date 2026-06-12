# SOURCES — frontend-architecture (Modern Frontend Patterns)

## Primary standards

- **patterns.dev** — Rendering patterns. <https://www.patterns.dev/>
- **Astro docs** — Islands architecture. <https://docs.astro.build/>
- **Qwik docs** — Resumability. <https://qwik.dev/>
- **Solid.js docs** — Signals. <https://www.solidjs.com/>
- **React 19 docs** — Server Components. <https://react.dev/>
- **Svelte 5 docs** — Runes. <https://svelte.dev/>
- **web.dev — Rendering on the Web**. <https://web.dev/rendering-on-the-web/>

## Rule-to-standard map

| Rule ID | Primary Source |
|---------|---------------|
| `js-only-no-html` | patterns.dev — Progressive Rendering |
| `full-hydration-spa` | Astro docs — Islands |
| `no-signals-vdom` | Solid.js docs, Svelte 5 runes |
| `client-data-fetch-default` | React 19 Server Components |
| `no-streaming-ssr` | React 19 Suspense, Solid renderToStream |
| `mpa-spa-wrong-choice` | web.dev — Rendering on the Web |
| `no-progressive-enhancement` | MDN — Progressive Enhancement |
| `no-islands-pattern` | Astro docs — Islands |
| `no-edge-rendering` | Next.js Edge Runtime, Astro adapters |
| `bundle-size-no-check` | web.dev — Code Splitting |

## Coverage: ~33% Layer 1, ~67% teaching-only. Verified in tests/test_frontend_architecture.py.
