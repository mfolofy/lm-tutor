"""Tests for the test class — proves each check_regex rule's FAIL/PASS behaviour.

For each rule with a check_regex, a FAIL snippet MUST produce that rule's
violation and a PASS snippet MUST NOT. Teaching-only rules (no check_*) are
verified via syllabus loading and content-presence tests.

Run with: pytest tests/
"""

import pytest

from tutor.eval import grade
from tutor.eval.harness import load_syllabus


def _rules_for(submission: str) -> set[str]:
    result = grade(submission, "test")
    return {v.rule for v in result.violations}


# ── MOCK ASSERT EXISTENCE ────────────────────────────────────────────────────

MOCK_CASES = [
    ("test-mock-assert-existence",
     "expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument()",
     "expect(screen.getByRole('navigation')).toBeInTheDocument()"),
    ("test-mock-assert-existence",
     "expect(screen.getByTestId('header-mock')).toBeVisible()",
     "expect(screen.getByTestId('sidebar')).toBeInTheDocument()"),
]


@pytest.mark.parametrize("rule_id,fail,passing", MOCK_CASES)
def test_mock_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", MOCK_CASES)
def test_mock_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── HARDCODED ASSERT PLACEHOLDER ─────────────────────────────────────────────

PLACEHOLDER_CASES = [
    ("test-hardcoded-assert-placeholder",
     "assert True  # placeholder",
     "assert response.status == 200"),
    ("test-hardcoded-assert-placeholder",
     "assert False;  # TODO",
     "assert is_ready() is True"),
]


@pytest.mark.parametrize("rule_id,fail,passing", PLACEHOLDER_CASES)
def test_placeholder_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", PLACEHOLDER_CASES)
def test_placeholder_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SHARED MUTABLE STATE ────────────────────────────────────────────────────

SHARED_STATE_CASES = [
    ("test-shared-state",
     "items = []",
     "    items = []  # inside a function, indented"),
    ("test-shared-state",
     "cache = {}",
     "items = [1, 2, 3]"),
]


@pytest.mark.parametrize("rule_id,fail,passing", SHARED_STATE_CASES)
def test_shared_state_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", SHARED_STATE_CASES)
def test_shared_state_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SKIP WITHOUT REASON ──────────────────────────────────────────────────────

SKIP_CASES = [
    ("test-skip-without-reason",
     "@pytest.mark.skip()",
     '@pytest.mark.skip(reason="not ready")'),
    ("test-skip-without-reason",
     "@pytest.mark.skipif(sys.version_info < (3, 10))",
     '@pytest.mark.skipif(condition, reason="needs >= py3.10")'),
]


@pytest.mark.parametrize("rule_id,fail,passing", SKIP_CASES)
def test_skip_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", SKIP_CASES)
def test_skip_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SENTINEL / INTEGRATION CHECKS ────────────────────────────────────────────


def test_syllabus_loads_and_has_rules():
    cls = load_syllabus("test")
    assert cls["class"]["id"] == "test"
    assert cls["class"]["version"] == "1.0.0"
    assert len(cls["rules"]) >= 17  # 4 checkable + 13+ teaching


def test_all_rules_have_id():
    cls = load_syllabus("test")
    ids = [r["id"] for r in cls["rules"]]
    assert len(ids) == len(set(ids)), "Duplicate rule IDs found"


def test_all_rules_have_severity():
    cls = load_syllabus("test")
    valid = {"fundamental", "advanced", "warning"}
    for r in cls["rules"]:
        assert r.get("severity") in valid, f"{r['id']}: invalid severity"


def test_regex_rules_have_framework_examples():
    cls = load_syllabus("test")
    for r in cls["rules"]:
        if r.get("check_regex"):
            keys = [k for k in r if k.startswith("framework_")]
            assert keys, f"{r['id']}: check_regex rule has no framework examples"


def test_teaching_rules_have_framework_examples():
    cls = load_syllabus("test")
    for r in cls["rules"]:
        if not r.get("check_regex") and not r.get("check_selector"):
            keys = [k for k in r if k.startswith("framework_")]
            assert keys, f"{r['id']}: teaching rule has no framework examples"


def test_clean_test_submission_passes():
    """A clean test file with no testing anti-patterns should pass all checks."""
    clean = """\
import pytest

def test_get_user_returns_name():
    result = get_user(1)
    assert result["name"] == "Alice"

def test_get_user_returns_none_for_missing():
    result = get_user(999)
    assert result is None
"""
    result = grade(clean, "test")
    assert result.passed, f"Expected clean tests to pass, got: {result.violations}"


def test_unknown_class_is_graceful():
    result = grade("<div>", "no-such-class")
    assert result.error is not None
    assert result.passed is False
