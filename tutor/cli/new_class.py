"""``tutor class --new`` — scaffold a new lm-tutor class.

Generates the three required files for a new class contribution:
    1. ``tutor/classes/<name>/class.yaml``   — curriculum + eval checks
    2. ``tutor/classes/<name>/SOURCES.md``    — research citations stub
    3. ``tests/test_<name>.py``               — test skeleton

Usage::

    tutor class --new my-class --title "My Class" --sources "WCAG 2.2, OWASP"
    tutor class --new perf-hooks --dry-run

The generated ``class.yaml`` follows the CONTRIBUTING.md template exactly —
one example rule with a ``check_selector``, one with ``check_regex``, and
the standard class metadata header. Replace the examples with real rules
after you have written ``SOURCES.md``.
"""

import sys
from pathlib import Path

_CLASSES_DIR = Path(__file__).parent.parent / "classes"
_TESTS_DIR = Path(__file__).parent.parent.parent / "tests"

# ── Templates ──────────────────────────────────────────────────────────────

_CLASS_YAML_TEMPLATE = """# {class_id} — {title}
#
# Source standard: {sources_text}. See SOURCES.md for per-rule citations.
# Every rule is self-contained: it carries teaching examples and, where
# detectable, a deterministic check (check_selector / check_regex) that
# the Layer 1 harness runs. No drift between teaching and testing.

class:
  id: {class_id}
  title: "{title}"
  version: 0.1.0
  sources: [{sources_list}]
  prerequisites: []
  target_violations:
{targets}
  estimated_cost_tokens: {token_est}

rules:

  # -- EXAMPLE RULE: selector-based check --
  # Replace these two examples with real rules after you have written SOURCES.md.

  - id: {class_id}-01
    severity: fundamental
    rule: "REPLACE: One-sentence imperative. The model attends to this as a [RULE] landmark."
    check_selector: "tag:not([required-attr])"
    framework_html: |
      <!-- FAIL: missing required attribute -->
      <!-- PASS: has the attribute -->

  # -- EXAMPLE RULE: regex-based check --
  - id: {class_id}-02
    severity: advanced
    rule: "REPLACE: Another one-sentence imperative rule."
    check_regex: 'TODO: write a regex — a match = a VIOLATION'
    framework_python: |
      # FAIL: pattern that violates the rule
      # PASS: pattern that satisfies the rule
"""

_SOURCES_STUB = """# {title} — Sources

> **IMPORTANT:** Write this file FIRST, before any rules.
> Every rule in class.yaml must cite a documented standard from the sources below.
> No rule exists "because I think so."

## Standards

<!-- List the external standards your class draws from. Examples:

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) — Web Content Accessibility Guidelines
- [OWASP Top 10 (2025)](https://owasp.org/www-project-top-ten/) — Application Security Risks
- [NIST SP 800-53 Rev 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final) — Security and Privacy Controls
- [PEP 8](https://peps.python.org/pep-0008/) — Style Guide for Python Code
- [ECMAScript 2024](https://tc39.es/ecma262/) — JavaScript Language Specification
-->

## Rule Citations

<!-- For each rule in class.yaml, cite the specific section/paragraph:

| Rule ID | Standard | Section | Quote |
|---------|----------|---------|-------|
| {class_id}-01 | ... | ... | ... |
| {class_id}-02 | ... | ... | ... |
-->
"""

_TEST_TEMPLATE = '''"""Tests for the {class_id} class.

Pattern: for each rule, assert the FAIL example produces the violation
and the PASS example does not.

Run::

    cd projects/lm-tutor
    pip install pytest
    pytest tests/test_{class_id}.py -v
"""

import pytest
import yaml
from pathlib import Path

from tutor.eval.harness import grade, Violation

CLASS_ID = "{class_id}"
_CLASSES = Path(__file__).parent.parent / "tutor" / "classes"


def _load_syllabus() -> dict:
    """Load class.yaml for this class."""
    path = _CLASSES / CLASS_ID / "class.yaml"
    assert path.exists(), f"Missing class.yaml for {{CLASS_ID}} at {{path}}"
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {{}}


def _find_rule(rule_id: str) -> dict:
    """Retrieve a single rule by id from the syllabus."""
    syllabus = _load_syllabus()
    rules = syllabus.get("rules", [])
    for r in rules:
        if r.get("id") == rule_id:
            return r
    return {{}}


# -- Example test -- replace with real tests --


def test_{class_id}_01_fail():
    """Rule {class_id}-01: FAIL example produces a violation."""
    rule = _find_rule("{class_id}-01")
    if not rule:
        pytest.skip("Rule {class_id}-01 not found - replace example rules")
    fail_html = rule.get("framework_html", "")
    result = grade(fail_html, CLASS_ID)
    violations = [v for v in result.violations if v.rule == "{class_id}-01"]
    assert len(violations) >= 1, f"Expected at least 1 violation, got {{len(violations)}}"


def test_{class_id}_01_pass():
    """Rule {class_id}-01: PASS example produces no violation."""
    rule = _find_rule("{class_id}-01")
    if not rule:
        pytest.skip("Rule {class_id}-01 not found - replace example rules")
    pass_html = rule.get("framework_html", "")
    result = grade(pass_html, CLASS_ID)
    violations = [v for v in result.violations if v.rule == "{class_id}-01"]
    assert len(violations) == 0, f"Expected 0 violations, got {{len(violations)}}"


def test_{class_id}_02_fail():
    """Rule {class_id}-02: FAIL example produces a violation."""
    rule = _find_rule("{class_id}-02")
    if not rule:
        pytest.skip("Rule {class_id}-02 not found - replace example rules")
    fail_python = rule.get("framework_python", "")
    result = grade(fail_python, CLASS_ID)
    violations = [v for v in result.violations if v.rule == "{class_id}-02"]
    assert len(violations) >= 1, f"Expected at least 1 violation, got {{len(violations)}}"


def test_{class_id}_02_pass():
    """Rule {class_id}-02: PASS example produces no violation."""
    rule = _find_rule("{class_id}-02")
    if not rule:
        pytest.skip("Rule {class_id}-02 not found - replace example rules")
    pass_python = rule.get("framework_python", "")
    result = grade(pass_python, CLASS_ID)
    violations = [v for v in result.violations if v.rule == "{class_id}-02"]
    assert len(violations) == 0, f"Expected 0 violations, got {{len(violations)}}"


def test_syllabus_loads():
    """Sanity: syllabus loads and has rules."""
    syllabus = _load_syllabus()
    assert "class" in syllabus, "Missing class metadata section"
    meta = syllabus["class"]
    assert meta.get("id") == CLASS_ID, f"class.id expected {{CLASS_ID}}, got {{meta.get('id')}}"
    rules = syllabus.get("rules", [])
    assert len(rules) >= 1, "At least one rule required"
'''

# ── Helpers ────────────────────────────────────────────────────────────────


def _sanitize_name(name: str) -> str:
    """Sanitize a class name: lowercase, hyphens, alphanumeric only."""
    import re
    cleaned = name.lower().strip()
    cleaned = re.sub(r'[^a-z0-9-]', '-', cleaned)
    cleaned = re.sub(r'-+', '-', cleaned)
    return cleaned.strip('-')


def _default_title(class_id: str) -> str:
    """Generate a title from the class ID."""
    return class_id.replace('-', ' ').title()


def _format_sources_csv(sources_str: str) -> tuple[str, str, str]:
    """Convert a comma-separated sources string into three forms:
    - sources_text: prose form for the comment header
    - sources_list: YAML list form for the class metadata
    - targets: two-space indented target_violations list.
    """
    parts = [s.strip() for s in sources_str.split(",") if s.strip()]
    if not parts:
        parts = ["TODO: add source standard"]
    sources_text = ", ".join(parts)
    sources_list = ", ".join(f'"{p}"' for p in parts)
    targets = "\n".join(f"    - \"{_sanitize_name(p)}\"" for p in parts)
    return sources_text, sources_list, targets


# ── Scaffold ───────────────────────────────────────────────────────────────


def scaffold(class_id: str, title: str | None = None,
             sources: str = "", dry_run: bool = False) -> int:
    """Create the three files for a new class."""
    class_id = _sanitize_name(class_id)
    if not class_id:
        print("[tutor class] Error: class name cannot be empty.", file=sys.stderr)
        return 1

    title = title or _default_title(class_id)
    sources_text, sources_list, targets = _format_sources_csv(sources)

    class_dir = _CLASSES_DIR / class_id
    class_yaml_path = class_dir / "class.yaml"
    sources_path = class_dir / "SOURCES.md"
    test_path = _TESTS_DIR / f"test_{class_id}.py"

    # Check for conflicts.
    conflicts = [p for p in (class_yaml_path, sources_path, test_path) if p.exists()]
    if conflicts:
        print("[tutor class] Error: these files already exist:", file=sys.stderr)
        for p in conflicts:
            print(f"  {p}", file=sys.stderr)
        print("Use a different class name or remove existing files first.", file=sys.stderr)
        return 2

    # Estimate token cost: 2 rules * ~12 tokens each = ~24.
    token_est = 50  # conservative default for a new class with examples

    class_yaml_content = _CLASS_YAML_TEMPLATE.format(
        class_id=class_id,
        title=title,
        sources_text=sources_text,
        sources_list=sources_list,
        targets=targets,
        token_est=token_est,
    )

    sources_content = _SOURCES_STUB.format(
        class_id=class_id,
        title=title,
    )

    test_content = _TEST_TEMPLATE.format(class_id=class_id)

    if dry_run:
        print(f"[tutor class] DRY RUN — would create:")
        print(f"  {class_yaml_path}")
        print(f"  {sources_path}")
        print(f"  {test_path}")
        print()
        print(f"[tutor class] {class_id}: title='{title}', sources='{sources_text}'")
        return 0

    # Create.
    class_dir.mkdir(parents=True, exist_ok=True)
    class_yaml_path.write_text(class_yaml_content, encoding="utf-8")
    sources_path.write_text(sources_content, encoding="utf-8")

    _TESTS_DIR.mkdir(parents=True, exist_ok=True)
    test_path.write_text(test_content, encoding="utf-8")

    print(f"[tutor class] Scaffolded '{class_id}' — 3 files:")
    print(f"  {class_yaml_path}")
    print(f"  {sources_path}")
    print(f"  {test_path}")
    print()
    print("  Next steps:")
    print(f"    1. Write {sources_path} FIRST (cite standards)")
    print(f"    2. Replace example rules in {class_yaml_path}")
    print(f"    3. Replace example tests in {test_path}")
    print(f"    4. pytest tests/test_{class_id}.py")

    return 0


def run(args) -> int:
    name = getattr(args, "name", "")
    title = getattr(args, "title", None) or None
    sources = getattr(args, "sources", "") or ""
    dry_run = getattr(args, "dry_run", False)

    if not name:
        print("Usage: tutor class --new <name> [--title ...] [--sources ...] [--dry-run]", file=sys.stderr)
        return 1

    return scaffold(name, title=title, sources=sources, dry_run=dry_run)
