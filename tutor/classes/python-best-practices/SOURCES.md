# SOURCES — python-best-practices (Python Coding Standards)

All rules in `class.yaml` derive from **PEP 8**, **PEP 257**, and **PEP 484**
(Python.org) plus supporting tool documentation. Every rule cites the specific
standard it codifies. No rule exists without a source.

## Primary standards

- **PEP 8 — Style Guide for Python Code** (Guido van Rossum, Barry Warsaw, Alyssa
  Coghlan). <https://peps.python.org/pep-0008/>
  - Indentation (4 spaces), line length (79/88), blank lines, imports, naming
  - All formatting, naming-convention, and import-style rules reference PEP 8.

- **PEP 257 — Docstring Conventions** (David Goodger, Guido van Rossum).
  <https://peps.python.org/pep-0257/>
  - Triple-quote style, one-line vs multi-line, summary line conventions.
  - All docstring-standards rules reference PEP 257.

- **PEP 484 — Type Hints** (Guido van Rossum, Jukka Lehtosalo, Lukasz Langa).
  <https://peps.python.org/pep-0484/>
  - Function annotations, Optional vs Union[T, None], avoiding Any.
  - All pep484-types rules reference PEP 484.

## Supporting references

- **Python documentation — The Python Standard Library**.
  <https://docs.python.org/3/library/>
  - `re` module (regex checker engine), `typing` module (annotations).

- **Flake8 documentation**. <https://flake8.pycqa.org/en/latest/>
  - F403/F405 (wildcard imports), F601 (mutable defaults detection),
    F811 (redefined variables), F841 (unused variables).

- **Black documentation — The uncompromising code formatter**.
  <https://black.readthedocs.io/en/stable/>
  - Line length default (88), code style conventions, compatibility with PEP 8.
  - All pep8-formatting rules reference Black's 88-char default as an
    acceptable alternative to PEP 8's 79-char limit.

## Additional references

- **PEP 20 — The Zen of Python** (Tim Peters).
  <https://peps.python.org/pep-0020/>
  - "Readability counts," "Simple is better than complex."
  - Philosophical basis for comprehension and loop-patterns rules.

- **PEP 8 -- Frequently Asked Questions**.
  <https://peps.python.org/pep-0008/#frequently-asked-questions>
  - Clarifications on naming conventions, line length exceptions, and
    import style.

- **Ruff documentation**. <https://docs.astral.sh/ruff/>
  - Modern Python linter superseding Flake8. Supports all PEP 8 rules
    plus isort-compatible import sorting.

## Rule-to-standard map

| Rule ID | Primary Standard | Secondary Source | Notes |
|---------|-----------------|------------------|-------|
| `pep8-formatting` | PEP 8 — Indentation, Line Length, Blank Lines | Black docs, Flake8 E3xx/E7xx | 79-char default (88 for Black); 4-space indent |
| `pep484-types` | PEP 484 — Function Annotations | typing module docs | Optional[T] over Union[T, None]; | syntax on 3.10+ |
| `import-style` | PEP 8 — Imports | Flake8 F403/F405 | Absolute over relative; no wildcard; explicit __init__.py |
| `naming-conventions` | PEP 8 — Naming Conventions | PEP 8 Naming Styles | snake_case, PascalCase, UPPER_CASE, _private |
| `docstring-standards` | PEP 257 — Docstring Conventions | Google Python Style Guide | Triple double-quotes; Args/Returns/Raises sections |
| `exception-handling` | Python Docs — Errors and Exceptions | Flake8 E722 (bare except) | Never bare except:; log or re-raise |
| `list-mutation` | Python FAQ — Mutable sequence modification | Flake8's no-iteration-mutation patterns observed | Copy or comprehend, never modify in-place |
| `mutable-defaults` | Python Docs — Default Argument Values | Flake8 B006 (mutable default) | Evaluate once at definition; use None as sentinel |
| `comparison-idioms` | PEP 8 — Programming Recommendations | Flake8 E711/E712 | is None not == None; truthiness not len() |
| `string-formatting` | PEP 498 — Literal String Interpolation | PEP 8 — Programming Recommendations | f-strings preferred over % and .format() |
| `context-managers` | Python Docs — Context Manager Types | with statement specification | with for files, locks, connections |
| `comprehensions` | PEP 202 (List Comps), PEP 274 (Dict Comps) | Python Docs — Data Structures | Prefer comprehensions over map/filter+lambda |
| `boolean-checking` | PEP 8 — Programming Recommendations | Flake8 E712 (comparison to True/False) | Implicit truthiness; avoid == True / == False |
| `loop-patterns` | Python Docs — Looping Techniques | PEP 279 (enumerate) | enumerate, zip, dict.items(); avoid range(len()) |
| `return-consistency` | PEP 8 — Programming Recommendations | Common Python anti-pattern research | Return consistent type; avoid implicit None |
| `dead-code` | Flake8 F401 (unused imports), F841 (unused vars) | Flake8 docs, Ruff docs | Remove unused imports, variables, unreachable code |

## Coverage honesty

**Layer 1 (regex) rules** cover codifiable Python anti-patterns with high
precision: bare `except:`, mutable default arguments, `== None` / `!= None`,
old-style string formatting (`%` and `.format()`), wildcard imports, and
`== True` / `== False`. These patterns have a unique textual signature that
a single regex can capture with near-zero false positives in practice.

**Teaching-only rules (no checker)** cover standards that require semantic
judgement beyond regex scope: formatting, naming conventions, type annotation
quality, docstring completeness, list-mutation intent, context-manager usage,
comprehension preference, loop-pattern style, return consistency, and dead
code detection. These are deferred to the LLM judge (Layer 2, Phase 1) or
existing linter tools (flake8, ruff, mypy, black).

The honest coverage boundary:
- ~38% of rules (6/16) are codifiable at Layer 1 via regex
- ~62% (10/16) need human or LLM judgement — documented as teaching-only rules with no checker

## Verification

Each rule with a `check_regex` is FAIL/PASS tested in
`tests/test_python_best_practices.py`. Teaching-only rules (no checker) are
tested for content presence only. A rule cannot ship without its test pair —
see CONTRIBUTING.md.
