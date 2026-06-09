"""Tests for the credential-jd class — proves each rule's FAIL/PASS behaviour.

Each checkable rule has a FAIL snippet that MUST produce a violation and a
PASS snippet that MUST NOT. Teaching-only rules are tested for content presence
in the syllabus. New rules MUST include their test pair — see CONTRIBUTING.md.
"""

import pytest

from tutor.eval import grade
from tutor.eval.harness import load_syllabus


def _rules_for(submission: str) -> set[str]:
    result = grade(submission, "credential-jd")
    return {v.rule for v in result.violations}


# ── CONFIDENTIALITY ───────────────────────────────────────────────────────────

CONFIDENTIALITY_CASES = [
    ("confidentiality",
     "disclose client confidential information without consent",
     "Client information is protected under ABA Rule 1.6."),
    ("confidentiality",
     "reveal client privileged data without informed authorization",
     "We must obtain informed consent before sharing any client data."),
    ("confidentiality",
     "divulge client sensitive detail absent permission",
     "This matter is confidential and cannot be discussed with third parties."),
    ("confidentiality",
     "disclose confidential communication without authorization",
     "Confidentiality obligations survive termination of representation."),
]


@pytest.mark.parametrize("rule_id,fail,passing", CONFIDENTIALITY_CASES)
def test_confidentiality_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CONFIDENTIALITY_CASES)
def test_confidentiality_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── PRIVILEGE PRESERVATION ────────────────────────────────────────────────────

PRIVILEGE_CASES = [
    ("privilege-preservation",
     "forward this privileged communication to a third party",
     "These privileged communications are protected from disclosure."),
    ("privilege-preservation",
     "send the privileged email to outside counsel",
     "Privileged communications must be marked PRIVILEGED AND CONFIDENTIAL."),
    ("privilege-preservation",
     "share these privileged notes with anyone else",
     "The document is labelled privileged and stored securely."),
    ("privilege-preservation",
     "transmit the privileged correspondence to an external recipient",
     "Attorney-client privilege protects our internal communications."),
]


@pytest.mark.parametrize("rule_id,fail,passing", PRIVILEGE_CASES)
def test_privilege_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", PRIVILEGE_CASES)
def test_privilege_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── FEE PROHIBITED ARRANGEMENTS ───────────────────────────────────────────────

FEE_CASES = [
    ("fee-prohibited-arrangements",
     "We can structure a contingency fee agreement for your divorce case",
     "Hourly billing at $350 per hour is standard for criminal defense."),
    ("fee-prohibited-arrangements",
     "This matter can be handled on a success fee basis for criminal cases",
     "Legal fees must be reasonable under ABA Model Rule 1.5."),
    ("fee-prohibited-arrangements",
     "A percentage fee arrangement works well for child custody matters",
     "Flat fees and hourly rates are common in family law practice."),
    ("fee-prohibited-arrangements",
     "We offer no win no fee structure for domestic relations cases",
     "Fee agreements should be in writing and signed by the client."),
]


@pytest.mark.parametrize("rule_id,fail,passing", FEE_CASES)
def test_fee_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", FEE_CASES)
def test_fee_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── PROHIBITION ON PRACTICE (DISCLAIMER) ──────────────────────────────────────

DISCLAIMER_CASES = [
    ("prohibition-practice-disclaimer",
     "I am your attorney and will handle this matter for you.",
     "I am an AI assistant with knowledge of legal procedures."),
    ("prohibition-practice-disclaimer",
     "I am a lawyer with twenty years of experience.",
     "I am not a licensed attorney. Please consult a qualified lawyer."),
    ("prohibition-practice-disclaimer",
     "I am your legal counsel and can represent you in court.",
     "I am an AI tool designed to assist with legal research."),
    ("prohibition-practice-disclaimer",
     "I'm an attorney licensed to practice in New York.",
     "I am an AI system and cannot form an attorney-client relationship."),
]


@pytest.mark.parametrize("rule_id,fail,passing", DISCLAIMER_CASES)
def test_disclaimer_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", DISCLAIMER_CASES)
def test_disclaimer_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── DOCUMENT FORMAT (PLACEHOLDER BRACKETS) ────────────────────────────────────

DOCFORMAT_CASES = [
    ("document-format",
     "[Plaintiff] v. [Defendant] Case No. [Case Number]",
     "John Doe v. Jane Smith, Case No. 2026-CV-1234."),
    ("document-format",
     "IN THE COURT OF [Court Name] [Caption] is missing",
     "The complaint must include a proper caption with court name and parties."),
    ("document-format",
     "Signed: [Attorney Name] Bar No. [Bar Number]",
     "Signed by Attorney Jane Smith, Bar No. 123456."),
    ("document-format",
     "Filed by [Filing Party] on [Date]",
     "The document was filed on June 9, 2026."),
]


@pytest.mark.parametrize("rule_id,fail,passing", DOCFORMAT_CASES)
def test_docformat_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", DOCFORMAT_CASES)
def test_docformat_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── PROHIBITED REPRESENTATION ─────────────────────────────────────────────────

CONFLICT_REP_CASES = [
    ("prohibited-representation",
     "I can represent both parties in this dispute.",
     "This client has interests adverse to another client I am assisting."),
    ("prohibited-representation",
     "I will handle both sides to save legal costs.",
     "I must decline this matter due to a conflict of interest."),
    ("prohibited-representation",
     "I can take both clients even though they are adverse.",
     "Simultaneous representation of adverse parties is prohibited."),
    ("prohibited-representation",
     "I represent adverse interests in this matter.",
     "Opposing counsel is representing the other party."),
]


@pytest.mark.parametrize("rule_id,fail,passing", CONFLICT_REP_CASES)
def test_conflict_rep_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CONFLICT_REP_CASES)
def test_conflict_rep_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SENTINEL / INTEGRATION CHECKS ─────────────────────────────────────────────


def test_syllabus_loads_and_has_rules():
    cls = load_syllabus("credential-jd")
    assert cls["class"]["id"] == "credential-jd"
    assert cls["class"]["version"] == "1.0.0"
    assert len(cls["rules"]) >= 16


def test_clean_submission_yields_no_violations():
    """A submission with no JD credential violations should pass cleanly."""
    clean = """\
I am an AI legal assistant with knowledge of legal concepts.
I am not a licensed attorney and cannot provide legal advice.
Client confidences are protected under ABA Model Rule 1.6.
All output should be reviewed by a licensed attorney before use.
Hourly billing at standard market rates applies to all work.
Legal documents must include proper caption and signature blocks.
Conflicts of interest must be identified and addressed before proceeding.
Attorney-client privilege protects our communications from disclosure.
Work product prepared in anticipation of litigation is protected.
"""
    result = grade(clean, "credential-jd")
    assert result.passed, result.violations


def test_unknown_class_is_graceful():
    result = grade("some text", "no-such-class")
    assert result.error is not None
    assert result.passed is False
