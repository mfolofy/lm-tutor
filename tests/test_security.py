"""Tests for the security class — proves each check_regex rule's FAIL/PASS behaviour.

Each checkable rule has a FAIL snippet that MUST produce a violation and a
PASS snippet that MUST NOT. Teaching-only rules are tested for content presence
in the syllabus. New rules MUST include their test pair — see CONTRIBUTING.md.

Run with: pytest tests/test_security.py
"""

import pytest

from tutor.eval import grade
from tutor.eval.harness import load_syllabus


def _rules_for(submission: str) -> set[str]:
    result = grade(submission, "security")
    return {v.rule for v in result.violations}


# ── PERMISSIVE CORS ─────────────────────────────────────────────────────────────

CORS_CASES = [
    ("ac-permissive-cors",
     "Access-Control-Allow-Origin: *",
     "Access-Control-Allow-Origin: https://app.example.com"),
    ("ac-permissive-cors",
     'allow_origins: ["*"]',
     'allow_origins: ["https://app.example.com"]'),
    ("ac-permissive-cors",
     'allowed_origins: "*"',
     'allowed_origins: "https://app.example.com"'),
    ("ac-permissive-cors",
     "cors_origin: *",
     'allow_origins: ["https://admin.example.com", "https://app.example.com"]'),
]


@pytest.mark.parametrize("rule_id,fail,passing", CORS_CASES)
def test_cors_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CORS_CASES)
def test_cors_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── DEBUG ENABLED ───────────────────────────────────────────────────────────────

DEBUG_CASES = [
    ("ac-debug-enabled",
     "DEBUG = True",
     "DEBUG = False"),
    ("ac-debug-enabled",
     "debug: true",
     "debug: false"),
    ("ac-debug-enabled",
     "debug_mode = 1",
     "debug_mode = 0"),
    ("ac-debug-enabled",
     "verbose_errors: true",
     "verbose_errors: false"),
]


@pytest.mark.parametrize("rule_id,fail,passing", DEBUG_CASES)
def test_debug_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", DEBUG_CASES)
def test_debug_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── WEAK PASSWORD POLICY ────────────────────────────────────────────────────────

PASSWORD_CASES = [
    ("ia-weak-password-policy",
     "password_min_length: 6",
     "password_min_length: 12"),
    ("ia-weak-password-policy",
     "PASSWORD_MIN_LENGTH = 6",
     "PASSWORD_MIN_LENGTH = 12"),
    ("ia-weak-password-policy",
     "min_password_length: 4",
     "min_password_length: 10"),
    ("ia-weak-password-policy",
     "password_minimum: 6",
     "password_minimum: 10"),
]


@pytest.mark.parametrize("rule_id,fail,passing", PASSWORD_CASES)
def test_password_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", PASSWORD_CASES)
def test_password_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SQL INJECTION ───────────────────────────────────────────────────────────────

SQL_CASES = [
    ("si-sql-injection",
     "cursor.execute(f\"SELECT * FROM users WHERE id = {user_id}\")",
     'cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))'),
    ("si-sql-injection",
     "db.execute(f\"INSERT INTO logs VALUES ('{msg}')\")",
     'db.execute("INSERT INTO logs VALUES (?)", [msg])'),
    ("si-sql-injection",
     "db.query(f\"UPDATE items SET name = '{name}' WHERE id = {item_id}\")",
     'connection.execute("UPDATE items SET name = $1 WHERE id = $2", [name, item_id])'),
    ("si-sql-injection",
     "connection.raw(f\"DELETE FROM cache WHERE key = {key}\")",
     'cursor.execute("DELETE FROM cache WHERE key = ?", (key,))'),
]


@pytest.mark.parametrize("rule_id,fail,passing", SQL_CASES)
def test_sql_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", SQL_CASES)
def test_sql_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SHELL INJECTION ─────────────────────────────────────────────────────────────

SHELL_CASES = [
    ("si-shell-injection",
     "os.system(f\"rm -rf {path}\")",
     'os.system("ls -la")'),
    ("si-shell-injection",
     "subprocess.run(f\"grep {pattern} /var/log\", shell=True)",
     'subprocess.run(["rm", "-rf", path])'),
    ("si-shell-injection",
     "subprocess.Popen(f\"cat {filename}\", shell=True)",
     'subprocess.Popen(["cat", filename])'),
]


@pytest.mark.parametrize("rule_id,fail,passing", SHELL_CASES)
def test_shell_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", SHELL_CASES)
def test_shell_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── INSECURE DESERIALIZATION ────────────────────────────────────────────────────

DESERIALIZE_CASES = [
    ("si-insecure-deserialization",
     "pickle.loads(data)",
     "json.loads(data)"),
    ("si-insecure-deserialization",
     "pickle.load(fileobj)",
     "yaml.safe_load(user_input)"),
    ("si-insecure-deserialization",
     "yaml.load(user_input)",
     "json.loads(safe_json)"),
    ("si-insecure-deserialization",
     "marshal.load(fileobj)",
     "pickle.dumps(data)"),
]


@pytest.mark.parametrize("rule_id,fail,passing", DESERIALIZE_CASES)
def test_deserialize_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", DESERIALIZE_CASES)
def test_deserialize_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SENTINEL / INTEGRATION CHECKS ───────────────────────────────────────────────


def test_syllabus_loads_and_has_rules():
    cls = load_syllabus("security")
    assert cls["class"]["id"] == "security"
    assert cls["class"]["version"] == "1.0.0"
    assert len(cls["rules"]) >= 19  # 6 checkable + 13 teaching = 19


def test_all_rules_have_id():
    cls = load_syllabus("security")
    ids = [r["id"] for r in cls["rules"]]
    assert len(ids) == len(set(ids)), "Duplicate rule IDs found"


def test_all_rules_have_severity():
    cls = load_syllabus("security")
    valid = {"fundamental", "advanced", "warning"}
    for r in cls["rules"]:
        assert r.get("severity") in valid, f"{r['id']}: invalid severity"


def test_regex_rules_have_framework_examples():
    cls = load_syllabus("security")
    for r in cls["rules"]:
        if r.get("check_regex"):
            keys = [k for k in r if k.startswith("framework_")]
            assert keys, f"{r['id']}: check_regex rule has no framework examples"


def test_teaching_rules_have_framework_examples():
    cls = load_syllabus("security")
    for r in cls["rules"]:
        if not r.get("check_regex") and not r.get("check_selector"):
            keys = [k for k in r if k.startswith("framework_")]
            assert keys, f"{r['id']}: teaching rule has no framework examples"


def test_clean_submission_passes():
    """A submission with no security anti-patterns should pass cleanly."""
    clean = """\
api:
  version: 1.0

cors:
  allow_origins: ["https://app.example.com"]

server:
  debug: false

auth:
  password_min_length: 12
  mfa: required
  session_timeout: 900

database:
  query: "SELECT * FROM users WHERE id = $1"
  encryption: aes256

logging:
  security_events: [login, access_denied]

files:
  permissions: 0640
"""
    result = grade(clean, "security")
    assert result.passed, f"Expected clean submission to pass, got: {result.violations}"


def test_unknown_class_is_graceful():
    result = grade("<div>", "no-such-class")
    assert result.error is not None
    assert result.passed is False
