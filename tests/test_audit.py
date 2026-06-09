"""Tests for the audit class — proves each rule's FAIL/PASS behaviour.

Each checkable rule has a FAIL snippet that MUST produce a violation and a
PASS snippet that MUST NOT. Teaching-only rules are tested for content presence
in the syllabus. New rules MUST include their test pair — see CONTRIBUTING.md.
"""

import pytest

from tutor.eval import grade
from tutor.eval.harness import load_syllabus


def _rules_for(submission: str) -> set[str]:
    result = grade(submission, "audit")
    return {v.rule for v in result.violations}


# ── HARDCODED SECRETS ────────────────────────────────────────────────────────

SECRETS_CASES = [
    ("hardcoded-secrets",
     "password: 'P@ssw0rd!'",
     "password: '${DB_PASSWORD}'"),
    ("hardcoded-secrets",
     'api_key: "sk-abc123"',
     'api_key: "${API_KEY}"'),
    ("hardcoded-secrets",
     'SECRET = "my-insecure-key"',
     'SECRET = os.getenv("SECRET")'),
    ("hardcoded-secrets",
     'access_token: "ghp_abc123def456"',
     'access_token: "${GITHUB_TOKEN}"'),
    ("hardcoded-secrets",
     'private_key: "-----BEGIN RSA PRIVATE KEY-----"',
     'private_key: "${VAULT_PRIVATE_KEY}"'),
]


@pytest.mark.parametrize("rule_id,fail,passing", SECRETS_CASES)
def test_secrets_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", SECRETS_CASES)
def test_secrets_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── AUDIT LOGGING DISABLED ───────────────────────────────────────────────────

LOGGING_CASES = [
    ("audit-logging-disabled",
     "audit_enabled: false",
     "audit_enabled: true"),
    ("audit-logging-disabled",
     "audit_logging: off",
     "audit_logging: on"),
    ("audit-logging-disabled",
     "audit.enabled = 0",
     "audit.enabled = 1"),
    ("audit-logging-disabled",
     "logging.audit: disabled",
     "logging.audit: enabled"),
    ("audit-logging-disabled",
     "audit_enabled = no",
     "audit_enabled = yes"),
]


@pytest.mark.parametrize("rule_id,fail,passing", LOGGING_CASES)
def test_logging_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", LOGGING_CASES)
def test_logging_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── WEAK CRYPTO ──────────────────────────────────────────────────────────────

CRYPTO_CASES = [
    ("weak-crypto",
     "hash_algorithm: md5",
     "hash_algorithm: sha256"),
    ("weak-crypto",
     "cipher: des",
     "cipher: aes256-gcm"),
    ("weak-crypto",
     "tls_version: 'TLS 1.0'",
     'tls_version: "TLS 1.3"'),
    ("weak-crypto",
     "import hashlib; hashlib.md5(data)",
     "import hashlib; hashlib.sha256(data)"),
    ("weak-crypto",
     "cipher: rc4",
     "cipher: aes256-gcm"),
    ("weak-crypto",
     "hash: sha1",
     "hash: sha256"),
]


@pytest.mark.parametrize("rule_id,fail,passing", CRYPTO_CASES)
def test_crypto_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CRYPTO_CASES)
def test_crypto_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── WORLD READABLE ───────────────────────────────────────────────────────────

PERM_CASES = [
    ("world-readable",
     "permissions: 0777",
     "permissions: 0600"),
    ("world-readable",
     'file_mode = "0777"',
     'file_mode = "0640"'),
    ("world-readable",
     "chmod = 0777",
     "chmod = 0640"),
    ("world-readable",
     "mode: 0777",
     "mode: 0640"),
]


@pytest.mark.parametrize("rule_id,fail,passing", PERM_CASES)
def test_perm_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", PERM_CASES)
def test_perm_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── MISSING ENCRYPTION ───────────────────────────────────────────────────────

ENCRYPT_CASES = [
    ("missing-encryption",
     "encryption: none",
     "encryption: aes256"),
    ("missing-encryption",
     "encrypt: false",
     "encrypt: true"),
    ("missing-encryption",
     "encryption = off",
     "encryption = on"),
    ("missing-encryption",
     "encryption: disabled",
     "encryption: enabled"),
]


@pytest.mark.parametrize("rule_id,fail,passing", ENCRYPT_CASES)
def test_encrypt_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", ENCRYPT_CASES)
def test_encrypt_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SINGLE OPERATOR MODE ──────────────────────────────────────────────────────

SINGLE_OP_CASES = [
    ("single-operator-mode",
     "single_operator: true",
     "single_operator: false"),
    ("single-operator-mode",
     "single_operator = yes",
     "single_operator = no"),
    ("single-operator-mode",
     "single_operator: 1",
     "single_operator: 0"),
    ("single-operator-mode",
     'GHOST_SINGLE_OPERATOR="true"',
     'GHOST_SINGLE_OPERATOR="false"'),
]


@pytest.mark.parametrize("rule_id,fail,passing", SINGLE_OP_CASES)
def test_single_op_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", SINGLE_OP_CASES)
def test_single_op_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── CHAIN VERIFICATION OFF ───────────────────────────────────────────────────

CHAIN_CASES = [
    ("chain-verification-off",
     "verify_chain: false",
     "verify_chain: true"),
    ("chain-verification-off",
     "integrity_check: false",
     "integrity_check: true"),
    ("chain-verification-off",
     "hash_verification: off",
     "hash_verification: on"),
    ("chain-verification-off",
     "chain_validation: disabled",
     "chain_validation: enabled"),
]


@pytest.mark.parametrize("rule_id,fail,passing", CHAIN_CASES)
def test_chain_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CHAIN_CASES)
def test_chain_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SENTINEL / INTEGRATION CHECKS ────────────────────────────────────────────


def test_syllabus_loads_and_has_rules():
    cls = load_syllabus("audit")
    assert cls["class"]["id"] == "audit"
    assert cls["class"]["version"] == "1.0.0"
    assert len(cls["rules"]) >= 17  # 8 checkable + 9 teaching


def test_pass_submission_yields_no_violations():
    """A submission with no audit anti-patterns should pass cleanly."""
    clean = """\
audit:
  enabled: true
  backend: wormchain
  retention: 365

security:
  encryption: aes256
  hash_algorithm: sha256
  tls_version: "TLS 1.3"
  single_operator: false

database:
  password: "${DB_PASSWORD}"
  permissions: 0600

chain:
  verify_chain: true
"""
    result = grade(clean, "audit")
    assert result.passed, result.violations


def test_unknown_class_is_graceful():
    result = grade("<div>", "no-such-class")
    assert result.error is not None
    assert result.passed is False
