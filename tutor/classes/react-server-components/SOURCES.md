# SOURCES — react-server-components (React 19 RSC Architecture)

All rules in `class.yaml` derive from React 19 official documentation, the React
Server Components RFC, and Next.js 15 App Router documentation. Every rule cites
the specific documentation section or RFC that defines the pattern. No rule exists
without a source.

## Primary standards

- **React 19 Documentation** (react.dev).
  <https://react.dev/>
  - Server Components, 'use client', 'use server' directives.
  - `use()` hook, Server Actions, serializable props constraint.
  - All directive rules, hook rules, and composition rules reference react.dev.

- **React Server Components RFC** (GitHub: reactjs/rfcs).
  <https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md>
  - Architecture rationale: zero client JS, Server→Client serialization wire
    format, component tree splitting.
  - All architecture rules reference this RFC.

- **Next.js 15 Documentation — App Router** (nextjs.org/docs).
  <https://nextjs.org/docs/app>
  - File conventions, Server Actions, Route Handlers, Metadata API,
    Streaming/Suspense patterns, caching and revalidation.
  - All framework-specific rules reference the Next.js docs.

## Supporting references

- **Next.js 15 — Server Actions and Mutations**.
  <https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations>
  - `'use server'`, `revalidatePath()`, `revalidateTag()`, form actions,
    progressive enhancement.

- **Next.js 15 — Caching**.
  <https://nextjs.org/docs/app/building-your-application/caching>
  - Full Route Cache, Data Cache, Router Cache, revalidation strategies.

- **Next.js 15 — Image Optimization**.
  <https://nextjs.org/docs/app/api-reference/components/image>
  - `<Image>` component, `priority`, `width`/`height`, CLS prevention.

- **Next.js 15 — Metadata API**.
  <https://nextjs.org/docs/app/api-reference/functions/generate-metadata>
  - Static and dynamic metadata, OpenGraph, Twitter Cards, JSON-LD.

- **React 19 — use() hook**.
  <https://react.dev/reference/react/use>
  - Unwrapping Promises and Context in Client Components.

- **React 19 — Directives**.
  <https://react.dev/reference/rsc/use-client>
  <https://react.dev/reference/rsc/use-server>
  - 'use client' and 'use server' directive semantics and constraints.

## Key articles

- **"Making Sense of React Server Components"** (Josh Comeau, 2024-2025).
  <https://www.joshwcomeau.com/react/server-components/>
  - Practical mental model for RSC boundaries, data flow, and composition.

- **"RSC From Scratch"** (Dan Abramov, GitHub gist, 2024).
  <https://github.com/reactwg/server-components/discussions>
  - Low-level walkthrough of the RSC wire format and streaming protocol.

- **"A Chain Reaction" — React Server Components** (patterns.dev).
  <https://www.patterns.dev/react/react-server-components>
  - Server↔Client composition patterns and colocation tradeoffs.

## Rule-to-standard map

| Rule ID | Primary Source | Secondary Source |
|---------|---------------|------------------|
| `use-client-placement` | react.dev — 'use client' | Next.js docs |
| `use-server-only` | react.dev — 'use server' | Next.js Server Actions |
| `no-hooks-in-server` | react.dev — Server Components | RSC RFC |
| `serializable-props` | react.dev — Server Components | RSC RFC wire format |
| `client-boundary-colocation` | react.dev — 'use client' | patterns.dev, Josh Comeau |
| `async-server-fetch` | react.dev — async components | Next.js data fetching |
| `no-use-effect-fetch` | react.dev — useEffect | Next.js data fetching |
| `no-bare-fetch` | Next.js — data fetching | Dan Abramov RSC guide |
| `use-hook-unwrap` | react.dev — use() hook | React 19 blog |
| `server-actions-mutations` | react.dev — Server Actions | Next.js Server Actions |
| `route-vs-action` | Next.js — Route Handlers | Next.js Server Actions |
| `cache-revalidation` | Next.js — Caching | revalidatePath/revalidateTag |
| `suspense-streaming` | react.dev — Suspense | Next.js loading.tsx |
| `file-conventions` | Next.js — File Conventions | App Router docs |
| `metadata-api` | Next.js — Metadata API | generateMetadata docs |
| `image-optimization` | Next.js — Image | next/image docs |
| `env-public-prefix` | Next.js — Environment Variables | React security |
| `server-imports-client-wrong` | react.dev — Server Components | RSC RFC composition rules |

## Coverage honesty

**Layer 1 (regex) rules** cover codifiable RSC anti-patterns with high
precision: `useState`/`useEffect` outside 'use client', useEffect+fetch
patterns, `'use client'` after imports, Server Components fetching their
own API routes, manual `<title>`/`<Head>` elements, raw `<img>` tags,
and `NEXT_PUBLIC_` secrets. These patterns have a unique textual signature.

**Teaching-only rules (no checker)** cover patterns that require semantic
judgement: boundary colocation strategy, Server Action vs Route Handler
choice, Suspense boundary placement, cache revalidation granularity,
file convention adherence, and Server→Client composition architecture.

The honest coverage boundary:
- ~44% of rules (8/18) are codifiable at Layer 1 via regex
- ~56% (10/18) need human or LLM judgement — documented as teaching-only

## Verification

Each rule with a `check_regex` is FAIL/PASS tested in
`tests/test_react_server_components.py`. Teaching-only rules (no checker)
are tested for content presence only. A rule cannot ship without its test
pair — see CONTRIBUTING.md.
