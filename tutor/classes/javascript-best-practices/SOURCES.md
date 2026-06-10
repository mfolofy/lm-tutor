# SOURCES — javascript-best-practices (JavaScript Coding Standards)

All rules in `class.yaml` derive from **MDN Web Docs**, **ECMAScript Specification**,
**Airbnb JavaScript Style Guide**, and **Google JavaScript Style Guide** plus
supporting tool documentation. Every rule cites the specific standard it
codifies. No rule exists without a source.

## Primary standards

- **MDN Web Docs — JavaScript Guide** (Mozilla).
  <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide>
  - `const`/`let` over `var`, template literals, destructuring, arrow functions,
    async/await, class syntax, all core language features.
  - Covers: no-var, template-literals, destructuring, arrow-functions,
    async-patterns, class-syntax rules.

- **ECMAScript® 2026 Language Specification (ECMA-262)**.
  <https://tc39.es/ecma262/>
  - Language semantics for `const`/`let` block scoping, strict mode,
    evaluation semantics, prototype chain, `with` statement prohibition.
  - Covers: no-var, strict-mode, no-with.

- **Airbnb JavaScript Style Guide**.
  <https://github.com/airbnb/javascript>
  - Industry-standard conventions: `const` over `let`, no `var`, strict equality,
    no `eval()`, no iterator mutation, array methods over loops, no prototype
    extension, named exports, JSDoc conventions.
  - Covers: const-over-let, strict-equality, no-eval, no-iterator-mutation,
    array-methods, no-prototype-mutation, named-exports, jsdoc.

- **Google JavaScript Style Guide**.
  <https://google.github.io/styleguide/jsguide.html>
  - `const`/`let` (no `var`), file-level strict mode, no `eval()`,
    no `with()`, `===` / `!==`, JSDoc requirements, class syntax.
  - Covers: no-var, strict-mode, no-eval, no-with, strict-equality, jsdoc.

## Supporting references

- **ESLint Rules Documentation**.
  <https://eslint.org/docs/latest/rules/>
  - `no-var` — enforces `const`/`let` over `var`.
  - `eqeqeq` — requires `===` and `!==`.
  - `no-eval` — bans `eval()` and `Function()` constructor.
  - `no-with` — bans `with` statements.
  - `no-prototype-builtins` — bans calling `hasOwnProperty` directly on objects.
  - `no-new-wrappers` — bans `new String()`, `new Number()`, `new Boolean()`.
  - `prefer-template` — prefers template literals over string concatenation.
  - `prefer-const` — prefers `const` when variable is never reassigned.
  - `prefer-destructuring` — prefers destructuring for array/object access.
  - `no-array-constructor` — bans `new Array()` with single argument (ambiguous).
  - `no-promise-executor-return` — bans returning values from promise executors.
  - `require-await` — warns on async functions without await.
  - `max-nested-callbacks` — limits callback nesting depth.
  - `no-return-await` — bans redundant `return await` in async functions.
  - `no-throw-literal` — requires throwing `Error` objects, not literals.

- **Node.js Documentation**.
  <https://nodejs.org/en/docs/guides/>
  - Error handling patterns, callback conventions, module system.
  - Covers: error-handling, no-sync-in-server (teaching rule for Node.js).

- **JSDoc Documentation**.
  <https://jsdoc.app/>
  - Block tag conventions (`@param`, `@returns`, `@type`) for documenting
    function signatures.

## Additional references

- **You Don't Know JS (YDKJS) Series** — Kyle Simpson.
  <https://github.com/getify/You-Dont-Know-JS>
  - Scope & Closures: `var` hoisting vs block scoping, IIFE patterns.
  - `this` & Object Prototypes: prototype chain, `this` binding rules.
  - Async & Performance: callbacks, promises, async/await evolution.

- **Node.js Best Practices** — Yoni Goldberg.
  <https://github.com/goldbergyoni/nodebestpractices>
  - Error handling, async patterns, security, code style.
  - Covers: error-handling, no-sync-in-server, async-patterns.

- **Clean Code JavaScript** — Ryan McDermott.
  <https://github.com/ryanmcdermott/clean-code-javascript>
  - Readability-focused JavaScript conventions: naming, function purity,
    single responsibility, meaningful abstractions.

- **State of JS Survey**.
  <https://stateofjs.com>
  - Ecosystem adoption data for language features (const/let adoption: >95%
    as of 2025, async/await adoption: >90%). Justifies rule priority based
    on community consensus, not personal preference.

## Rule-to-standard map

| Rule ID | Primary Standard | Secondary Source | Notes |
|---------|-----------------|------------------|-------|
| `no-var` | ECMA-262 §13.3 — Block Scoping | Airbnb §2 — References, ESLint no-var | `const`/`let` are block-scoped; `var` leaks scope |
| `const-over-let` | Airbnb §2.1 — `const` for all references | ESLint prefer-const | `const` signals non-reassignment; use `let` only when reassigning |
| `strict-equality` | ECMA-262 §12.10 — Equality Comparisons | Airbnb §5 — Equality, ESLint eqeqeq | `==` coerces types; `===` does not |
| `no-eval` | ECMA-262 §18.2.1 — eval(x) | Airbnb §4 — Eval, ESLint no-eval | `eval` executes arbitrary code in caller's scope |
| `no-with` | ECMA-262 §14.2 — with Statement | Google JS Guide — with, ESLint no-with | `with` adds object to scope chain; banned in strict mode |
| `strict-mode` | ECMA-262 §10.2.1 — Strict Mode | Google JS Guide — Use Strict | `'use strict'` at file level; prevents silent errors |
| `template-literals` | ECMA-262 §12.8 — Template Literals | Airbnb §3.6 — Template Literals, ESLint prefer-template | Template literals are readable, support multi-line, expressions |
| `destructuring` | ECMA-262 §13.3.5 — Destructuring | Airbnb §3.8 — Destructuring, ESLint prefer-destructuring | Object/array destructuring reduces repetition |
| `arrow-functions` | ECMA-262 §14.2 — Arrow Functions | Airbnb §8 — Arrow Functions | Lexical `this`, concise syntax; avoids `that = this` pattern |
| `async-patterns` | ECMA-262 §15.8 — Async Functions | Airbnb §7 — Async/Await, Node.js Best Practices | `async`/`await` over raw promises; avoid callback nesting >3 deep |
| `no-prototype-mutation` | ECMA-262 §9.4 — Built-in Prototypes | Airbnb §16 — jQuery patterns / Docs | Mutating built-in prototypes breaks all instances; use `extends` instead |
| `no-new-wrappers` | ECMA-262 §9.3 — Primitive Wrappers | Airbnb §3.3 — Primitives, ESLint no-new-wrappers | `new String()`, `new Number()`, `new Boolean()` produce objects, not primitives |
| `array-methods` | MDN — Array Methods Guide | Airbnb §5 — Iteration | `forEach`/`map`/`filter`/`find`/`reduce` over `for`/`for...in` for array iteration |
| `error-handling` | MDN — Error Handling Guide | Node.js Best Practices §2 | Always use `try`/`catch` with async/await; throw `Error` objects |
| `no-document-write` | MDN — document.write() | Airbnb §17 — DOM | Overwrites document; never use in modern JS |
| `jsdoc` | JSDoc Standard | Google JS Guide — JSDoc | Document params, returns, types for public functions |

## Coverage honesty

**Layer 1 (regex) rules** cover codifiable JavaScript anti-patterns with high
precision: `var` declarations, `==` / `!=` comparisons, `eval()` calls,
`with()` statements, `document.write()`, prototype mutation, and primitive
wrapper constructors. These patterns have a unique textual signature that
a single regex can capture with near-zero false positives in practice.

**Teaching-only rules (no checker)** cover standards that require semantic
judgement beyond regex scope: `const` vs `let` correctness, template literal
preference, destructuring usage, arrow function appropriateness, async/await
patterns, array method preference, error handling completeness, JSDoc quality,
and callback depth. These are deferred to the LLM judge (Layer 2, Phase 1) or
existing linter tools (ESLint, Prettier).

The honest coverage boundary:
- ~44% of rules (7/16) are codifiable at Layer 1 via regex
- ~56% (9/16) need human or LLM judgement — documented as teaching-only rules with no checker

## Verification

Each rule with a `check_regex` is FAIL/PASS tested in
`tests/test_javascript_best_practices.py`. Teaching-only rules (no checker) are
tested for content presence only. A rule cannot ship without its test pair —
see CONTRIBUTING.md.
