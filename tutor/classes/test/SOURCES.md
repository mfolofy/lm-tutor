# SOURCES — test (TDD & Testing Best Practices)

All rules in `class.yaml` derive from established software testing literature
and community standards. Every rule cites its specific source. No rule exists
without a foundation.

## Primary sources

### xUnit Test Patterns — Gerard Meszaros (2007)

The definitive catalog of test automation patterns and anti-patterns. Defines
the vocabulary: test doubles (stubs, fakes, spies, mocks), test isolation,
fixture management, and assertion patterns.

- **Book:** Meszaros, G. (2007). *xUnit Test Patterns: Refactoring Test Code*.
  Addison-Wesley. ISBN 978-0-13-149505-0.
- **Online:** <http://xunitpatterns.com/>
- **Patterns cited:** Assertion Pattern, Test Double pattern language,
  Shared Fixture, Fresh Fixture, Clean Fixture, Four-Phase Test
  (Setup-Exercise-Verify-Teardown).

### FIRST Principles — Tim Ottinger (Clean Code, 2008)

The five properties every test must satisfy:

- **Fast** — Tests run in milliseconds. Slow tests don't get run.
- **Isolated** — Tests don't depend on each other. Any order, any subset.
- **Repeatable** — Same result every time. No environment sensitivity.
- **Self-validating** — Pass/fail is automatic. No manual output inspection.
- **Timely** — Written at the right time (preferably before the code).

Source: Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software
Craftsmanship*. Prentice Hall. Chapter 9: Unit Tests.

### Practical Test Pyramid — Ham Vocke (2018)

Canonical description of the test pyramid applied to modern microservice
architectures. Covers the ratio of unit/integration/e2e tests, what belongs at
each layer, and common anti-patterns (ice cream cone, inverted pyramid).

- Vocke, H. (2018). "The Practical Test Pyramid."
  <https://martinfowler.com/articles/practical-test-pyramid.html>

### Property-Based Testing — Scott Wlaschin (F# for Fun and Profit)

Comprehensive introduction to property-based testing: defining invariants,
generating random inputs, shrinking failures.

- Wlaschin, S. "Property-Based Testing." *F# for Fun and Profit*.
  <https://fsharpforfunandprofit.com/pbt/>
- MacIver, D., Hatfield-Dodds, Z., & The Hypothesis Authors. "Hypothesis:
  Property-Based Testing for Python." 2013--2026. <https://hypothesis.works/>
- Dubois, N. (2025). *Property-Based Testing with PropEr, Erlang, and Elixir*.
  Pragmatic Bookshelf. (General PBT methodology, beyond Erlang.)

### Test-Driven Development — Kent Beck (2002)

The canonical description of the red-green-refactor cycle and its role in
software design.

- Beck, K. (2002). *Test-Driven Development: By Example*. Addison-Wesley.
  ISBN 978-0-321-14653-3.
- **Red** — Write a test that fails (no code yet).
- **Green** — Write minimum code to make it pass.
- **Refactor** — Improve the code while keeping tests green.

### Testing Anti-Patterns — Ghost Stack / everybody-lies (2026)

Internal reference compiled from the Ghost Stack codebase, codifying the
anti-patterns documented in `superpowers/skills/test-driven-development/`:

- **Testing Mock Behavior** — Asserting on mock elements (`*-mock` test IDs)
  verifies the mock framework, not the code.
- **Test-Only Production Methods** — Adding methods to production classes
  solely for test cleanup or inspection.
- **Mocking Without Understanding** — Over-mocking that breaks the test's own
  dependencies or bypasses essential side effects.
- **Incomplete Mocks** — Partial mock objects missing fields that downstream
  code depends on.

### BDD / Given-When-Then — Dan North (2006)

Behavior-Driven Development and the Given/When/Then template for structuring
test scenarios in natural language.

- North, D. (2006). "Introducing BDD." Better Software Magazine.
- Chelimsky, D. et al. (2010). *The RSpec Book: Behaviour-Driven Development
  with RSpec, Cucumber, and Friends*. Pragmatic Bookshelf.
- Fowler, M. (2013). "GivenWhenThen."
  <https://martinfowler.com/bliki/GivenWhenThen.html>

### Additional sources

- **Flaky Tests Management:** Luo, Q. et al. (2014). "An Empirical Analysis of
  Flaky Tests." *Proceedings of the 22nd ACM SIGSOFT International Symposium on
  Foundations of Software Engineering* (FSE 2014). <https://doi.org/10.1145/2635868.2635920>
- **Parameterized Tests:** Unit test frameworks (pytest `@parametrize`, JUnit
  `@ParameterizedTest`, Jest `test.each`) — all follow the same principle:
  separate test logic from test data.
- **Test Naming Conventions:** Fowler, M. (2020). "Test Naming."
  <https://martinfowler.com/bliki/TestNaming.html>
- **Regression Testing (Red-Green-Refactor):** Beck, K. (2002). *TDD by Example*.
  The bug-fix variant of TDD: reproduce-then-fix.
- **Coverage Criteria:** Myers, G. J., Sandler, C., & Badgett, T. (2011).
  *The Art of Software Testing, 3rd Ed.* Wiley. (Boundary value analysis,
  equivalence partitioning, path coverage.)

## Per-rule source map

| Rule id | Primary Source | Secondary Source |
|---------|---------------|-----------------|
| `test-mock-assert-existence` | Ghost Stack testing anti-patterns (Mock Behavior anti-pattern) | xUnit Test Patterns — assertions on test doubles |
| `test-hardcoded-assert-placeholder` | xUnit Test Patterns — Assertion Pattern | Clean Code ch. 9 — meaningful assertions |
| `test-shared-state` | xUnit Test Patterns — Shared Fixture / Fresh Fixture | FIRST — Isolated |
| `test-skip-without-reason` | xUnit Test Patterns — Conditional Test Fixture | Community convention (pytest docs) |
| `test-pyramid` | Practical Test Pyramid (Ham Vocke, 2018) | xUnit Test Patterns — Test Automation Strategy |
| `first-principles` | FIRST Principles (Clean Code ch. 9) | xUnit Test Patterns — F.I.R.S.T. properties |
| `test-coverage-criteria` | The Art of Software Testing (Myers, 3rd Ed.) | xUnit Test Patterns — Equivalence Class partitioning |
| `test-doubles` | xUnit Test Patterns — Test Double pattern language | Fowler, M. "Mocks Aren't Stubs" (2007) |
| `property-based` | Property-Based Testing (Scott Wlaschin) | Hypothesis docs (Zac Hatfield-Dodds) |
| `regression-test` | TDD by Example (Kent Beck) | Red-Green-Refactor cycle |
| `integration-boundaries` | Practical Test Pyramid (Ham Vocke) | xUnit Test Patterns — Integration tests at boundaries |
| `test-naming-conventions` | Test Naming (Martin Fowler, 2020) | xUnit Test Patterns — Named Test Suite |
| `test-isolation` | FIRST — Isolated principle | xUnit Test Patterns — Fresh Fixture |
| `tdd-cycle` | TDD by Example (Kent Beck) | Red-Green-Refactor |
| `behavior-driven` | BDD (Dan North, 2006) | Given/When/Then (Martin Fowler) |
| `parametrized-tests` | pytest docs / JUnit 5 ParameterizedTest | xUnit Test Patterns — Data-Driven Test |
| `flaky-tests` | "An Empirical Analysis of Flaky Tests" (FSE 2014) | xUnit Test Patterns — Erratic Test |
| `test-assertion-quality` | xUnit Test Patterns — Assertion Pattern | Clean Code ch. 9 — one assert per test |

## Coverage honesty

**Checkable rules (4):** `test-mock-assert-existence`, `test-hardcoded-assert-placeholder`,
`test-shared-state`, `test-skip-without-reason` — these are codifiable as regex
patterns that detect common test anti-patterns in source text. They are
high-precision but narrow: they detect known-bad structural patterns but do not
prove overall test quality.

**Teaching-only rules (14):** Test architecture (pyramid, FIRST, coverage criteria),
test double selection, property-based testing, regression discipline, naming,
isolation, TDD cycle, BDD, parameterization, flaky test management — these
require contextual judgment and domain knowledge. They are evaluated by the LLM
judge (Layer 2) or the Socratic fix step, not by deterministic regex.

**What is NOT covered:** Test effectiveness (mutation testing), code quality of
test code (readability benchmarks), test maintenance cost, flaky test prevalence
measurement, coverage thresholds, or CI pipeline behaviour. These are
organizational and toolchain concerns, not LLM code-generation standards.

## Verification

Rules with `check_regex` are FAIL/PASS tested in `tests/test_test.py`.
Teaching-only rules (no checker) are tested for content presence only via
syllabus loading. A rule ships with at minimum its FAIL/PASS framework
examples — there is always something a student can learn from.
