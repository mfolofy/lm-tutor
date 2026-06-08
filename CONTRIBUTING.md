# Contributing to lm-tutor

## License

lm-tutor is **MIT licensed** (see `LICENSE`). Your contributions will be
MIT licensed. The code you submit stays MIT — forever.

## Contributor License Agreement (CLA)

We require a signed CLA before merging any external contribution.

**Why:** Every contributor owns a copyright slice of their code. A CLA
grants the project owner the right to sublicense and relicense contributed
code commercially — required for clean IP chain if the project is ever
acquired or forms a legal entity. Without it, every unCLA'd commit is a
liability.

This does NOT change what users receive. Code shipped under MIT stays
MIT. The CLA is an IP housekeeping requirement, not a license change.

**How:** When you open a PR, a bot will ask you to sign via
[cla-assistant.io](https://cla-assistant.io). It takes ~30 seconds via
GitHub OAuth. See `CLA.md` for the full terms.

No CLA = no merge. No exceptions, even for 1-line fixes.

---

## The Unit of Contribution: A Class

The unit of contribution is a **class**. Adding one is exactly three files:

```
tutor/classes/<name>/class.yaml      # the curriculum + the eval checks
tutor/classes/<name>/SOURCES.md      # research citations (written FIRST)
tests/test_<name>.py                 # proves each rule's FAIL/PASS examples
```

That's the whole contract. No code change to the framework is needed for a new
class — the harness discovers `class.yaml` automatically.

## The rules (non-negotiable)

1. **Sources before rules.** Write `SOURCES.md` first. Every rule must cite a
   documented standard (WCAG, OWASP, NIST, IEEE/ACM review research). No rule
   exists "because I think so." A class without `SOURCES.md` is rejected.
2. **One file, no drift.** `class.yaml` carries *both* the teaching examples and
   the `check_selector` / `check_regex` that grade them. What you teach is what
   you test, from the same source of truth.
3. **Every rule is tested.** A rule enters production only with a test proving
   its FAIL examples produce the violation and its PASS examples do not.

## class.yaml format

```yaml
class:
  id: <name>
  title: "Human-readable title"
  version: 1.0.0
  sources: ["WCAG 2.2"]
  prerequisites: []
  target_violations: ["wcag-1.1.1", ...]
  estimated_cost_tokens: 120        # tokens when the rules are injected

rules:
  - id: short-stable-id
    severity: fundamental           # fundamental | advanced
    wcag: "1.1.1"                   # the SC / standard reference
    rule: "One-sentence imperative the model attends to as a [RULE] landmark."
    check_selector: "img:not([alt])"          # a match = a VIOLATION
    # or:
    check_regex: 'aria-label\s*=\s*"\s*"'      # a match = a VIOLATION
    framework_html:  |  # paired, minimal FAIL/PASS — not realistic, just relevant
      <!-- FAIL --> <img src="x.png">
      <!-- PASS --> <img src="x.png" alt="...">
    framework_react: | ...
    framework_vue:   | ...
    framework_vanilla: | ...
```

### Layer 1 selector dialect (stdlib, no bs4)

The Phase 0 harness runs on the standard library so `tutor eval` works right
after `pip install -e .` with no extra deps. Supported selectors:

| Form | Matches |
|------|---------|
| `tag` | every element of that tag |
| `tag[attr]` | tag with `attr` present |
| `tag[attr="v"]` | tag with `attr` equal to `v` |
| `tag[attr=""]` | tag with empty `attr` |
| `tag:not([attr])` | tag with `attr` absent |
| `tag:empty` | tag with no element/text children |
| `a, b, c` | union (comma-separated) |

For anything richer (colour contrast, AST checks), put the deep grader in a
per-class venv via `_requirements.txt` + a `grader.py`, invoked through
`tutor._class_venv.ClassVenvManager.run_in_class_venv`. Keep it **off** the
Layer 1 happy path.

## Per-class dependencies

If a class needs libraries, list them in
`tutor/classes/<name>/_requirements.txt`. They install lazily into
`~/.tutor/venvs/<name>/` on first use — never into the core environment, so
classes never conflict.

## Tests

Pattern (see `tests/test_brushes.py`): for each rule, assert the FAIL example
produces the violation and the PASS example does not.

```bash
pip install pytest
pytest tests/
```

## Severity and tracks

`fundamental` rules are injected for every track; `advanced` rules target
honors. Pick the severity from the standard: a Level A failure is almost always
`fundamental`.
