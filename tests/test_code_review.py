"""Tests for the code-review class -- proves each check_regex rule's FAIL/PASS behaviour.

For each rule with a check_regex, a FAIL snippet MUST produce that rule's
violation and a PASS snippet MUST NOT. Teaching-only rules (no check_*) are
verified via syllabus loading and content-presence tests.

Run with: pytest tests/
"""

import pytest

from tutor.eval import grade
from tutor.eval.harness import load_syllabus


def _rules_for(submission: str) -> set[str]:
    result = grade(submission, "code-review")
    return {v.rule for v in result.violations}


# ── RUBBER-STAMPING ───────────────────────────────────────────────────────────

RUBBER_STAMPING_CASES = [
    ("rubber-stamping", "LGTM",
     "The implementation looks correct. I verified the auth flow at "
     "auth_service.py:142 handles the race condition properly. Clean."),
    ("rubber-stamping", "Looks good to me",
     "Reviewed the PR thoroughly. The config change at config.py:12 is "
     "environment-aware. One P3: add a comment explaining the fallback."),
    ("rubber-stamping", "Ship it",
     "Approved after verifying: (1) parameterized queries at db.py:44-60, "
     "(2) tests pass, (3) rollback plan documented in PR description."),
    ("rubber-stamping", "Looks good",
     "Looks good on the logic. One P3: the error handler at line 42 should "
     "use a more specific exception type."),
    ("rubber-stamping", "Approved",
     "Approved. Pre-scan clean, no P1 findings, rollback documented."),
]


@pytest.mark.parametrize("rule_id,fail,passing", RUBBER_STAMPING_CASES)
def test_rubber_stamping_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", RUBBER_STAMPING_CASES)
def test_rubber_stamping_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── P1-AUTOREJECT ─────────────────────────────────────────────────────────────

P1_AUTOREJECT_CASES = [
    ("p1-autoreject",
     "There is a P1 finding about credential storage but I will approve "
     "since it is urgent.",
     "P1 finding: credentials.py:15 stores API keys in plaintext. "
     "Fix before commit."),
    ("p1-autoreject",
     "P1 issue found in token handling. Approving anyway to meet deadline.",
     "P1 issue found in token handling. Rejecting until this is fixed."),
    ("p1-autoreject",
     "P1 finding: SQL injection in search endpoint. PR approved because "
     "tests pass.",
     "P1 finding: SQL injection in search endpoint. REJECTED."),
    ("p1-autoreject",
     "P1 critical security vulnerability. Merge immediately.",
     "P1 critical security vulnerability. Fix and resubmit."),
]


@pytest.mark.parametrize("rule_id,fail,passing", P1_AUTOREJECT_CASES)
def test_p1_autoreject_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", P1_AUTOREJECT_CASES)
def test_p1_autoreject_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SENTINEL / INTEGRATION CHECKS ─────────────────────────────────────────────


def test_syllabus_loads_and_has_rules():
    cls = load_syllabus("code-review")
    assert cls["class"]["id"] == "code-review"
    assert cls["class"]["version"] == "1.0.0"
    assert len(cls["rules"]) >= 16  # minimum 16 teaching rules


def test_all_rules_have_id():
    cls = load_syllabus("code-review")
    ids = [r["id"] for r in cls["rules"]]
    assert len(ids) == len(set(ids)), "Duplicate rule IDs found"


def test_all_rules_have_severity():
    cls = load_syllabus("code-review")
    valid = {"fundamental", "advanced", "warning"}
    for r in cls["rules"]:
        assert r.get("severity") in valid, f"{r['id']}: invalid severity"


def test_regex_rules_have_framework_examples():
    cls = load_syllabus("code-review")
    for r in cls["rules"]:
        if r.get("check_regex"):
            keys = [k for k in r if k.startswith("framework_")]
            assert keys, f"{r['id']}: check_regex rule has no framework examples"


def test_teaching_rules_have_framework_examples():
    cls = load_syllabus("code-review")
    for r in cls["rules"]:
        if not r.get("check_regex") and not r.get("check_selector"):
            keys = [k for k in r if k.startswith("framework_")]
            assert keys, f"{r['id']}: teaching rule has no framework examples"


def test_well_structured_review_passes_all_checks():
    """A complete, well-structured code review should pass all regex checks."""
    review = (
        "Change type: Normal\n"
        "Risk score: 2.5/5 -> standard tier\n"
        "Scope: verify SQL injection fix in user search endpoint only\n\n"
        "Findings:\n"
        "  P2: user_service.py:142 -- string interpolation in SQL query. "
        "Replace with parameterized query.\n"
        "  P3: error_handler.py:88 -- broad exception catch. Log the error.\n\n"
        "No P1 findings. Rollback plan: git revert + deploy previous tag.\n"
        "RFC record complete. Compliance checklist verified.\n"
        "Verdict: APPROVED (P2 must be fixed, P3 deferred with ticket PROJ-42)\n"
    )
    result = grade(review, "code-review")
    assert result.passed, f"Expected clean review to pass, got: {result.violations}"


def test_substantive_approval_passes():
    """A detailed approval with verification evidence should not be rubber-stamping."""
    review = (
        "Approved after verifying:\n"
        "1. All SQL queries use parameterized statements (db.py:44-60)\n"
        "2. No hardcoded credentials\n"
        "3. Config is environment-aware (config.py:12)\n"
        "4. All existing tests pass\n"
        "5. Rollback: git revert <sha> + deploy previous tag\n"
    )
    assert "rubber-stamping" not in _rules_for(review)


def test_unknown_class_is_graceful():
    result = grade("<div>", "no-such-class")
    assert result.error is not None
    assert result.passed is False
