# SOURCES — typescript-best-practices (TypeScript Coding Standards)

All rules in `class.yaml` derive from the **TypeScript Handbook**, **TypeScript
ESLint**, **Microsoft TypeScript Coding Guidelines**, and **Google TypeScript
Style Guide** plus supporting tool documentation. Every rule cites the specific
standard it codifies. No rule exists without a source.

## Primary standards

- **TypeScript Handbook** (Microsoft).
  <https://www.typescriptlang.org/docs/handbook/>
  - Everyday Types, Narrowing, More on Functions, Object Types, Generics,
    Keyof/Typeof, Indexed Access, Conditional Types, Mapped Types, Template
    Literal Types, Modules.
  - Covers: no-any, unknown-over-any, generics, narrowing, satisfies,
    utility-types, readonly, modules rules.

- **TypeScript ESLint — Strict Rules**.
  <https://typescript-eslint.io/rules/>
  - `no-explicit-any` — bans `any` type annotation.
  - `no-unused-vars` — bans unused variables (with `_` prefix escape hatch).
  - `no-non-null-assertion` — bans `!` postfix expression.
  - `no-require-imports` — bans `require()` calls.
  - `prefer-as-const` — prefers `as const` over literal type annotation.
  - `prefer-readonly` — prefers `readonly` on never-reassigned properties.
  - `prefer-enum-initializer` — requires explicit enum member values.
  - `consistent-type-definitions` — prefers `interface` over `type` for object shapes.
  - `method-signature-style` — prefers property signatures for strict variance.
  - `array-type` — prefers `T[]` over `Array<T>` for simple types.
  - Covers: no-explicit-any, no-unused-vars, no-non-null-assertion,
    no-require, readonly, enum-preference, interface-over-type, array-type rules.

- **Microsoft TypeScript Coding Guidelines**.
  <https://github.com/microsoft/TypeScript/wiki/Coding-guidelines>
  - Official Microsoft conventions: naming, `null` vs `undefined`, types in
    public APIs, module structure, JSDoc conventions.
  - Covers: naming-conventions, null-vs-undefined, public-api-types rules.

- **Google TypeScript Style Guide**.
  <https://google.github.io/styleguide/tsguide.html>
  - No `any`, no `namespace`, no `require()`, no `!` assertion,
    `const` by default, optional parameters, JSDoc restrictions.
  - Covers: no-any, no-namespace, no-require, no-non-null-assertion rules.

## Supporting references

- **TypeScript Deep Dive** — Basarat Ali Syed.
  <https://basarat.gitbook.io/typescript/>
  - Practical patterns: type guards, discriminated unions, branded types,
    nominal typing, never type exhaustiveness checks.
  - Covers: branded-types, discriminated-unions, exhaustive-check rules.

- **Clean Code TypeScript** — Labs42.
  <https://labs42io.github.io/clean-code-typescript/>
  - Readability-focused TypeScript conventions: naming, function purity,
    single responsibility, dependency injection patterns.

- **TypeScript Design Patterns**.
  <https://refactoring.guru/design-patterns/typescript>
  - Factory, Builder, Strategy patterns with TypeScript generics.
  - Covers: generics rule (proper generic typing for reusable patterns).

## Rule-to-standard map

| Rule ID | Primary Standard | Secondary Source | Notes |
|---------|-----------------|------------------|-------|
| `no-explicit-any` | TS Handbook — TypeScript ESLint | Google TS Guide | `any` disables type checking entirely. Use `unknown` |
| `unknown-over-any` | TS Handbook — unknown type | TS Deep Dive | `unknown` forces narrowing before use; `any` does not |
| `interface-over-type` | TS Handbook — Interfaces vs Types | TS ESLint consistent-type-definitions | `interface` for objects (extendable); `type` for unions/intersections |
| `generics` | TS Handbook — Generics | Clean Code TS | Constrain with `extends`, prefer generic over `any` |
| `no-non-null-assertion` | TS ESLint no-non-null-assertion | Google TS Guide | `!` hides null from the type checker; use narrowing instead |
| `no-unused-vars` | TS ESLint no-unused-vars | Clean Code TS | Prefix unused params with `_`; remove unused imports |
| `readonly` | TS Handbook — Readonly Properties | TS ESLint prefer-readonly | Mark never-reassigned properties `readonly` for immutability |
| `narrowing` | TS Handbook — Narrowing | TypeScript Deep Dive | Use type guards, discriminated unions, `in`, `typeof`, `instanceof` |
| `satisfies` | TS Handbook — satisfies operator | TS 4.9+ feature | Validates types without widening the inferred type |
| `utility-types` | TS Handbook — Utility Types | lib.es5.d.ts | Partial, Pick, Omit, Record, Exclude, Extract, ReturnType |
| `enum-preference` | TS Handbook — Enums | TS ESLint prefer-enum-initializer | Prefer `const enum` or union of string literals over regular enums |
| `no-require` | TS ESLint no-require-imports | Google TS Guide | Use `import`/`export` (ES modules), not `require()` |
| `branded-types` | TypeScript Deep Dive — Nominal Typing | — | Branded types give nominal typing; use for IDs/sensitive types |
| `exhaustive-check` | TS Handbook — Exhaustiveness Checking | TypeScript Deep Dive | Use `never` in default cases to catch unhandled union members |
| `no-namespace` | Google TS Guide | TS Handbook — Modules | Prefer ES modules over `namespace` (allowed for .d.ts ambient decls) |
| `array-type` | TS ESLint array-type | — | Prefer `T[]` for simple element types; `Array<T>` for complex generics |

## Coverage honesty

**Layer 1 (regex) rules** cover codifiable TypeScript anti-patterns with high
precision: explicit `: any` annotations, non-null assertion (`!`), `require()`
calls, `namespace` declarations, `as` type assertions, `new Array()` constructor,
and unused variables that don't start with `_`. These patterns have a unique
textual signature that a single regex can capture.

**Teaching-only rules (no checker)** cover standards that require semantic
judgement beyond regex scope: proper generic constraints, `unknown` over `any`
distinction, interface vs type appropriateness, readonly correctness, narrowing
quality, utility type selection, enum choice, branded type usage, exhaustiveness
checking, and `satisfies` operator usage. These are deferred to the LLM judge
(Layer 2, Phase 1) or existing linter tools (TypeScript ESLint, tsconfig strict).

The honest coverage boundary:
- ~44% of rules (7/16) are codifiable at Layer 1 via regex
- ~56% (9/16) need human or LLM judgement — documented as teaching-only rules with no checker

## Verification

Each rule with a `check_regex` is FAIL/PASS tested in
`tests/test_typescript_best_practices.py`. Teaching-only rules (no checker) are
tested for content presence only. A rule cannot ship without its test pair —
see CONTRIBUTING.md.
