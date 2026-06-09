"""Tests for the api-design class — proves each rule's FAIL/PASS behaviour.

For each rule with a check_regex, a FAIL snippet MUST produce that rule's
violation and a PASS snippet MUST NOT. Teaching-only rules (no checker) are
tested for syllabus content presence only.

Run with: pytest tests/
"""

import pytest

from tutor.eval import grade
from tutor.eval.harness import load_syllabus


def _rules_for(submission: str) -> set[str]:
    result = grade(submission, "api-design")
    return {v.rule for v in result.violations}


# ── REST RESOURCE NAMING ────────────────────────────────────────────────────

RESOURCE_CASES = [
    ("rest-resource-naming",
     'GET /api/v1/createUser HTTP/1.1',
     'GET /api/v1/users HTTP/1.1'),
    ("rest-resource-naming",
     'POST /api/v1/getOrders',
     'POST /api/v1/orders'),
    ("rest-resource-naming",
     '"path": "/api/v1/deleteItem"',
     '"path": "/api/v1/items"'),
]


@pytest.mark.parametrize("rule_id,fail,passing", RESOURCE_CASES)
def test_resource_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", RESOURCE_CASES)
def test_resource_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── STATUS CODES ────────────────────────────────────────────────────────────

STATUS_CASES = [
    ("status-codes",
     'return 200, {"error": "not found"}',
     'raise HTTPException(status_code=404, detail="User not found")'),
    ("status-codes",
     'status_code = 200  # error',
     'status_code = 404  # not found'),
    ("status-codes",
     'HTTP_200_OK + "error body"',
     'HTTP_201_CREATED'),
]


@pytest.mark.parametrize("rule_id,fail,passing", STATUS_CASES)
def test_status_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", STATUS_CASES)
def test_status_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── ERROR FORMAT ────────────────────────────────────────────────────────────

ERROR_CASES = [
    ("error-format",
     'Traceback (most recent call last):\n  File "/app/db.py", line 42',
     '{"error": "NOT_FOUND", "message": "User not found", "request_id": "req_abc"}'),
    ("error-format",
     'Stacktrace: at org.example.UserService.getUser',
     '{"error": "INTERNAL_ERROR", "message": "Unexpected error"}'),
    ("error-format",
     'Internal Server Error #42',
     'HTTP 500 {"error": "INTERNAL_ERROR", "message": "Server error"}'),
]


@pytest.mark.parametrize("rule_id,fail,passing", ERROR_CASES)
def test_error_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", ERROR_CASES)
def test_error_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── VERSIONING ──────────────────────────────────────────────────────────────

VERSION_CASES = [
    ("versioning",
     '"path": "/api/users"',
     '"path": "/api/v1/users"'),
    ("versioning",
     "'/api/orders'",
     "'/api/v2/orders'"),
    ("versioning",
     '"/api/products"',
     '"/api/v1/products"'),
]


@pytest.mark.parametrize("rule_id,fail,passing", VERSION_CASES)
def test_versioning_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", VERSION_CASES)
def test_versioning_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── AUTHENTICATION ──────────────────────────────────────────────────────────

AUTH_CASES = [
    ("authentication",
     'api_key=abc123def456',
     'Authorization: Bearer eyJhbGciOiJIUzI1NiIs'),
    ("authentication",
     'token=eyJhbGciOiJIUzI1NiIs&user=5',
     'Authorization: Bearer eyJhbG'),
    ("authentication",
     'apikey=sk-abc123def456',
     'Authorization: Bearer valid_token'),
]


@pytest.mark.parametrize("rule_id,fail,passing", AUTH_CASES)
def test_auth_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", AUTH_CASES)
def test_auth_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── GRAPHQL NAMING ──────────────────────────────────────────────────────────

GRAPHQL_CASES = [
    ("graphql-naming",
     'type user {\n  id: Int\n  name: String\n}',
     'type User {\n  id: Int\n  name: String\n}'),
    ("graphql-naming",
     'type orderItem {\n  id: Int\n}',
     'type OrderItem {\n  id: Int\n}'),
    ("graphql-naming",
     'type userProfile {\n  firstName: String\n}',
     'type UserProfile {\n  firstName: String\n}'),
]


@pytest.mark.parametrize("rule_id,fail,passing", GRAPHQL_CASES)
def test_graphql_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", GRAPHQL_CASES)
def test_graphql_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SENTINEL / INTEGRATION CHECKS ───────────────────────────────────────────


def test_syllabus_loads_and_has_rules():
    cls = load_syllabus("api-design")
    assert cls["class"]["id"] == "api-design"
    assert cls["class"]["version"] == "1.0.0"
    assert len(cls["rules"]) == 18


def test_clean_snippet_passes():
    clean = (
        'GET /api/v1/users HTTP/1.1\n'
        'Authorization: Bearer eyJhbGciOiJIUzI1NiIs\n'
        'Content-Type: application/json\n'
        'Accept: application/json\n'
    )
    result = grade(clean, "api-design")
    assert result.passed, result.violations


def test_unknown_class_is_graceful():
    result = grade("GET /api/v1/users", "no-such-class")
    assert result.error is not None
    assert result.passed is False
