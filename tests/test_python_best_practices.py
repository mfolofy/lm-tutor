"""Tests for the python-best-practices class — proves each rule's FAIL/PASS behaviour.

For each rule with a check_regex, a FAIL snippet MUST produce that rule's
violation and a PASS snippet MUST NOT. Teaching-only rules (no checker) are
tested for syllabus content presence only.

Run with: pytest tests/
"""

import pytest

from tutor.eval import grade
from tutor.eval.harness import load_syllabus


def _rules_for(submission: str) -> set[str]:
    result = grade(submission, "python-best-practices")
    return {v.rule for v in result.violations}


# ── IMPORT STYLE ──────────────────────────────────────────────────────────────

IMPORT_CASES = [
    ("import-style", "from os import *", "from os import path"),
    ("import-style", "from math import *  # pollutes", "from math import sqrt"),
]


@pytest.mark.parametrize("rule_id,fail,passing", IMPORT_CASES)
def test_import_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", IMPORT_CASES)
def test_import_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── EXCEPTION HANDLING ───────────────────────────────────────────────────────

EXCEPTION_CASES = [
    ("exception-handling",
     "try:\n    x()\nexcept:\n    pass",
     "try:\n    x()\nexcept ValueError:\n    pass"),
    ("exception-handling",
     "try:\n    process()\nexcept:  # noqa\n    pass",
     "try:\n    process()\nexcept Exception as e:\n    log(e)"),
]


@pytest.mark.parametrize("rule_id,fail,passing", EXCEPTION_CASES)
def test_exception_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", EXCEPTION_CASES)
def test_exception_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── MUTABLE DEFAULTS ──────────────────────────────────────────────────────────

MUTABLE_CASES = [
    ("mutable-defaults", "def foo(items=[]):", "def foo(items=None):"),
    ("mutable-defaults",
     "def add(item, data={}):",
     "def add(item, data=None):"),
    ("mutable-defaults",
     "def process(seen=set()):",
     "def process(seen=None):"),
]


@pytest.mark.parametrize("rule_id,fail,passing", MUTABLE_CASES)
def test_mutable_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", MUTABLE_CASES)
def test_mutable_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── COMPARISON IDIOMS ─────────────────────────────────────────────────────────

COMPARISON_CASES = [
    ("comparison-idioms", "if x == None:", "if x is None:"),
    ("comparison-idioms", "if x != None:", "if x is not None:"),
]


@pytest.mark.parametrize("rule_id,fail,passing", COMPARISON_CASES)
def test_comparison_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", COMPARISON_CASES)
def test_comparison_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── STRING FORMATTING ─────────────────────────────────────────────────────────

STRING_CASES = [
    ("string-formatting", '"Hello, %s!" % name', 'f"Hello, {name}!"'),
    ("string-formatting",
     '"Hello {}".format(name)',
     'f"Hello, {name}!"'),
    ("string-formatting",
     '"value: %d" % len(items)',
     'f"value: {len(items)}"'),
]


@pytest.mark.parametrize("rule_id,fail,passing", STRING_CASES)
def test_string_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", STRING_CASES)
def test_string_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── BOOLEAN CHECKING ─────────────────────────────────────────────────────────

BOOLEAN_CASES = [
    ("boolean-checking", "if x == True:", "if x:"),
    ("boolean-checking", "if x == False:", "if not x:"),
    ("boolean-checking",
     "return result == True",
     "return bool(result)"),
]


@pytest.mark.parametrize("rule_id,fail,passing", BOOLEAN_CASES)
def test_boolean_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", BOOLEAN_CASES)
def test_boolean_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SENTINEL / INTEGRATION CHECKS ────────────────────────────────────────────


def test_syllabus_loads_and_has_rules():
    cls = load_syllabus("python-best-practices")
    assert cls["class"]["id"] == "python-best-practices"
    assert cls["class"]["version"] == "1.0.0"
    assert len(cls["rules"]) == 16


def test_clean_snippet_passes():
    clean = (
        "from os import path\n"
        "import sys\n"
        "\n"
        "def greet(name=None):\n"
        '    if name is None:\n'
        '        name = "World"\n'
        '    return f"Hello, {name}!"\n'
    )
    result = grade(clean, "python-best-practices")
    assert result.passed, result.violations


def test_unknown_class_is_graceful():
    result = grade("x = 1", "no-such-class")
    assert result.error is not None
    assert result.passed is False
