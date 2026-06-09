"""Tests for the defense class — proves each rule's FAIL/PASS behaviour.

Each checkable rule has a FAIL snippet that MUST produce a violation and a
PASS snippet that MUST NOT. Teaching-only rules are tested for content presence
in the syllabus. New rules MUST include their test pair — see CONTRIBUTING.md.
"""

import pytest

from tutor.eval import grade
from tutor.eval.harness import load_syllabus


def _rules_for(submission: str) -> set[str]:
    result = grade(submission, "defense")
    return {v.rule for v in result.violations}


# ── INPUT VALIDATION ───────────────────────────────────────────────────────────

INPUT_VALIDATION_CASES = [
    ("input-validation",
     'f"SELECT * FROM users WHERE id = {user_id}"',
     'cursor.execute("SELECT * FROM users WHERE id = ?", (uid,))'),
    ("input-validation",
     'cursor.execute(f"SELECT id FROM orders WHERE uid = {uid}")',
     'query = "SELECT * FROM users WHERE id = ?"'),
    ("input-validation",
     '"SELECT * FROM users WHERE id = " + user_id',
     '"SELECT count(*) FROM users"'),
    ("input-validation",
     '"SELECT * FROM users WHERE id = %s" % user_id',
     '"SELECT name, email FROM accounts WHERE id = ?"'),
    ("input-validation",
     'db.query(`UPDATE users SET name = ${name} WHERE id = ${id}`)',
     'db.query("UPDATE users SET name = $1 WHERE id = $2", [name, id])'),
]


@pytest.mark.parametrize("rule_id,fail,passing", INPUT_VALIDATION_CASES)
def test_input_validation_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", INPUT_VALIDATION_CASES)
def test_input_validation_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── HARDCODED CREDENTIALS ──────────────────────────────────────────────────────

CREDS_CASES = [
    ("authentication-hardcoded-creds",
     'password: "P@ssw0rd!"',
     'password: "${DB_PASSWORD}"'),
    ("authentication-hardcoded-creds",
     'api_key: "sk-abc123def456"',
     'api_key: "${API_KEY}"'),
    ("authentication-hardcoded-creds",
     'secret: "ghp_abc123"',
     'secret: "${GITHUB_TOKEN}"'),
    ("authentication-hardcoded-creds",
     'password: "s3cret!"',
     'password: "${DB_PASSWORD}"'),
    ("authentication-hardcoded-creds",
     'const apiKey = \'abc123def456\'',
     'const apiKey = process.env.API_KEY'),
]


@pytest.mark.parametrize("rule_id,fail,passing", CREDS_CASES)
def test_creds_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CREDS_CASES)
def test_creds_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── INSECURE SESSION ───────────────────────────────────────────────────────────

SESSION_CASES = [
    ("session-insecure",
     "http_only: false",
     "http_only: true"),
    ("session-insecure",
     'httponly: false',
     'httponly: true'),
    ("session-insecure",
     "secure: false",
     "secure: true"),
    ("session-insecure",
     'same_site: false',
     'same_site: true'),
    ("session-insecure",
     'session.httpOnly = false',
     'session.httpOnly = true'),
]


@pytest.mark.parametrize("rule_id,fail,passing", SESSION_CASES)
def test_session_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", SESSION_CASES)
def test_session_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── CORS MISCONFIGURATION ──────────────────────────────────────────────────────

CORS_CASES = [
    ("cors-misconfiguration",
     'Access-Control-Allow-Origin: *',
     'Access-Control-Allow-Origin: https://app.example.com'),
    ("cors-misconfiguration",
     'Access-Control-Allow-Origin:*',
     'Access-Control-Allow-Origin: https://admin.example.com'),
    ("cors-misconfiguration",
     'res.setHeader("Access-Control-Allow-Origin", "*")',
     'res.setHeader("Access-Control-Allow-Origin", "https://app.example.com")'),
    ("cors-misconfiguration",
     'Access-Control-Allow-Origin = "*"',
     'Access-Control-Allow-Origin = "https://app.example.com"'),
    ("cors-misconfiguration",
     'allowed_origins: "*"',
     'allowed_origins: ["https://app.example.com"]'),
]


@pytest.mark.parametrize("rule_id,fail,passing", CORS_CASES)
def test_cors_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CORS_CASES)
def test_cors_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── WEAK CRYPTOGRAPHY ───────────────────────────────────────────────────────────

CRYPTO_CASES = [
    ("cryptography-weak",
     "hash_algorithm: md5",
     "hash_algorithm: sha256"),
    ("cryptography-weak",
     "cipher: des",
     "cipher: aes256-gcm"),
    ("cryptography-weak",
     "tls_version: 'TLS 1.0'",
     'tls_version: "TLS 1.3"'),
    ("cryptography-weak",
     "import hashlib; hashlib.md5(data)",
     "import hashlib; hashlib.sha256(data)"),
    ("cryptography-weak",
     "cipher: rc4",
     "cipher: aes256-gcm"),
    ("cryptography-weak",
     'ssl_version: "SSL 3.0"',
     "cipher: aes256-gcm"),
]


@pytest.mark.parametrize("rule_id,fail,passing", CRYPTO_CASES)
def test_crypto_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CRYPTO_CASES)
def test_crypto_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── STACK TRACE EXPOSURE ───────────────────────────────────────────────────────

STACK_CASES = [
    ("error-exposing-stack-trace",
     "server.debug: true",
     "server.debug: false"),
    ("error-exposing-stack-trace",
     "stack_trace: true",
     "stack_trace: false"),
    ("error-exposing-stack-trace",
     "traceback = true",
     "traceback = false"),
    ("error-exposing-stack-trace",
     "show_details: true",
     "show_details: false"),
    ("error-exposing-stack-trace",
     "debug = yes",
     "debug = no"),
]


@pytest.mark.parametrize("rule_id,fail,passing", STACK_CASES)
def test_stack_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", STACK_CASES)
def test_stack_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── LOGGING SENSITIVE DATA ─────────────────────────────────────────────────────

LOGGING_CASES = [
    ("logging-sensitive-data",
     'log("password=P@ssw0rd")',
     'log("User logged in")'),
    ("logging-sensitive-data",
     'log(f"token={access_token}")',
     'log(f"request_id={rid}")'),
    ("logging-sensitive-data",
     'log(f"secret={SECRET_KEY}")',
     'log("Processing complete")'),
    ("logging-sensitive-data",
     'log(f"password={password}")',
     'log(f"status={status_code}")'),
    ("logging-sensitive-data",
     "print(f'api_key = {api_key}')",
     'print(f"status={status_code}")'),
]


@pytest.mark.parametrize("rule_id,fail,passing", LOGGING_CASES)
def test_logging_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", LOGGING_CASES)
def test_logging_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── TLS DISABLED ───────────────────────────────────────────────────────────────

TLS_CASES = [
    ("tls-disabled",
     "verify_ssl: false",
     "verify_ssl: true"),
    ("tls-disabled",
     "verify_ssl = false",
     "verify_ssl = true"),
    ("tls-disabled",
     "ssl_verify: false",
     "ssl_verify: true"),
    ("tls-disabled",
     "rejectUnauthorized: false",
     "rejectUnauthorized: true"),
    ("tls-disabled",
     "verify_cert: false",
     "verify_cert: true"),
    ("tls-disabled",
     "verify_peer = no",
     "verify_peer = yes"),
]


@pytest.mark.parametrize("rule_id,fail,passing", TLS_CASES)
def test_tls_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", TLS_CASES)
def test_tls_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SENTINEL / INTEGRATION CHECKS ──────────────────────────────────────────────


def test_syllabus_loads_and_has_rules():
    cls = load_syllabus("defense")
    assert cls["class"]["id"] == "defense"
    assert cls["class"]["version"] == "1.0.0"
    assert len(cls["rules"]) >= 19  # 8 checkable + 11 teaching


def test_pass_submission_yields_no_violations():
    """A submission with no defense anti-patterns should pass cleanly."""
    clean = """\
security:
  encryption: aes256-gcm
  hash_algorithm: sha256
  tls_version: "TLS 1.3"

database:
  password: "${DB_PASSWORD}"
  query: "SELECT * FROM users WHERE id = ?"

session:
  http_only: true
  secure: true
  same_site: lax

server:
  debug: false
  error_detail: log_only

cors:
  allowed_origins: ["https://app.example.com"]

logging:
  sanitize_headers: true
  log_request_body: false

http:
  verify_ssl: true
"""
    result = grade(clean, "defense")
    assert result.passed, result.violations


def test_unknown_class_is_graceful():
    result = grade("<div>", "no-such-class")
    assert result.error is not None
    assert result.passed is False
