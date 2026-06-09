"""Tests for the architect class — proves each rule's FAIL/PASS behaviour.

For each rule with check_regex, a FAIL snippet MUST produce that rule's
violation and a PASS snippet MUST NOT. Teaching-only rules are tested for
content presence in the syllabus only.

Run with: pytest tests/
"""

import pytest

from tutor.eval import grade
from tutor.eval.harness import load_syllabus


def _rules_for(submission: str) -> set[str]:
    result = grade(submission, "architect")
    return {v.rule for v in result.violations}


# ── CHECKABLE RULES (4, check_regex) ─────────────────────────────────────────

REGEX_CASES = [
    # api-no-version
    (
        "api-no-version",
        '@router.get("/api/users")',
        '@router.get("/api/v1/users")',
    ),
    (
        "api-no-version",
        'route("/api/orders/")',
        'route("/api/v2/orders/")',
    ),
    # credential-injection
    (
        "credential-injection",
        "password: \"hunter2\"",
        'password: "${DB_PASSWORD}"',
    ),
    (
        "credential-injection",
        "api_key: \"sk-abc123def456\"",
        "api_key: \"{{API_KEY}}\"",
    ),
    (
        "credential-injection",
        'token = "ghp_abc123def456"',
        'token = os.getenv("GITHUB_TOKEN")',
    ),
    # single-operator-mode
    (
        "single-operator-mode",
        "single_operator: true",
        "dual_approval: true",
    ),
    (
        "single-operator-mode",
        "single_operator = yes",
        'single_operator: false',
    ),
    (
        "single-operator-mode",
        "single_operator_mode: 1",
        'single_operator_mode: false',
    ),
    # print-logging
    (
        "print-logging",
        'print("processing order")',
        'logger.info("processing order")',
    ),
    (
        "print-logging",
        '    print(f"User {id} logged in")',
        '    logger.info(f"User {id} logged in")',
    ),
]


@pytest.mark.parametrize("rule_id,fail,passing", REGEX_CASES)
def test_regex_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", REGEX_CASES)
def test_regex_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── EDGE CASES ────────────────────────────────────────────────────────────────

def test_print_not_mistaken_for_method_call():
    """print() is OK when it's a method call, not a bare print statement."""
    assert "print-logging" not in _rules_for("obj.print()")
    assert "print-logging" not in _rules_for("pprint(data)")


def test_versioned_api_v1dot0_passes():
    """Versioned routes with dotted versions (v1.0) must pass."""
    assert "api-no-version" not in _rules_for('@router.get("/api/v1.0/users")')


def test_credential_env_var_with_dollar_passes():
    """Credentials referencing $VAR or {{TEMPLATE}} must pass."""
    assert "credential-injection" not in _rules_for('password: "$SECRET"')
    assert "credential-injection" not in _rules_for('password: "{{SECRET}}"')
    assert "credential-injection" not in _rules_for("password = os.environ.get(\"DB_PASSWORD\")")


# ── SENTINEL / INTEGRATION CHECKS ────────────────────────────────────────────


def test_syllabus_loads_and_has_rules():
    cls = load_syllabus("architect")
    assert cls["class"]["id"] == "architect"
    assert cls["class"]["version"] == "1.0.0"
    assert len(cls["rules"]) >= 18


def test_clean_submission_passes():
    clean = (
        '@router.get("/api/v1/users")\n'
        'logger.info("startup complete")\n'
        'password: "${DB_PASSWORD}"\n'
        'dual_approval: true\n'
    )
    result = grade(clean, "architect")
    assert result.passed, result.violations


def test_unknown_class_is_graceful():
    result = grade("some text", "no-such-class")
    assert result.error is not None
    assert result.passed is False
