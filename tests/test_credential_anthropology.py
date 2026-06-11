"""Tests for the credential-anthropology class — proves each rule's FAIL/PASS behaviour.

Each checkable rule has a FAIL snippet that MUST produce a violation and a
PASS snippet that MUST NOT. Teaching-only rules are tested for content presence
in the syllabus. New rules MUST include their test pair — see CONTRIBUTING.md.
"""

import pytest

from tutor.eval import grade
from tutor.eval.harness import load_syllabus


def _rules_for(submission: str) -> set[str]:
    result = grade(submission, "credential-anthropology")
    return {v.rule for v in result.violations}


# ── DO NO HARM ─────────────────────────────────────────────────────────────────

HARM_CASES = [
    ("do-no-harm",
     "These tribes are primitive and isolated from the modern world.",
     "This community maintains distinct cultural practices adapted to their environment."),
    ("do-no-harm",
     "The villagers are backward in their practices and need development.",
     "Their knowledge systems reflect generations of adaptation."),
    ("do-no-harm",
     "These people are still uncivilized in their approach to life.",
     "Rather than framing as underdeveloped, anthropologists approach different knowledge systems."),
    ("do-no-harm",
     "The natives are simple and stone age in their technology.",
     "The community uses technologies suited to their ecological and social context."),
]


@pytest.mark.parametrize("rule_id,fail,passing", HARM_CASES)
def test_harm_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", HARM_CASES)
def test_harm_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── INFORMED CONSENT ───────────────────────────────────────────────────────────

CONSENT_CASES = [
    ("informed-consent",
     "No need to explain the purpose of your research. Just observe them naturally.",
     "Before beginning fieldwork, explain who you are and how the information will be used."),
    ("informed-consent",
     "No need to tell the community about the nature of your research. It would bias results.",
     "Obtain their consent, both individual and at the community level."),
    ("informed-consent",
     "No need to inform the participants about the nature of the research.",
     "Informed consent is foundational to ethical anthropological practice."),
    ("informed-consent",
     "No need to notify the participants about the nature of the research.",
     "The community has the right to understand the nature and purpose of your work."),
]


@pytest.mark.parametrize("rule_id,fail,passing", CONSENT_CASES)
def test_consent_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CONSENT_CASES)
def test_consent_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── CULTURAL RELATIVISM ────────────────────────────────────────────────────────

RELATIVISM_CASES = [
    ("cultural-relativism",
     "These people still believe strange things about medicine.",
     "This community's healing practices are grounded in their worldview."),
    ("cultural-relativism",
     "It's strange that they practice rituals we would consider bizarre.",
     "From an emic perspective, this practice has internal logic within the cultural system."),
    ("cultural-relativism",
     "These people still think backward things about the natural world.",
     "The role of the anthropologist is to understand, not to judge."),
    ("cultural-relativism",
     "These people still think odd things about the natural world.",
     "Different cultures have different frameworks for understanding the natural world."),
    ("cultural-relativism",
     "It's strange how they superstitiously avoid certain foods.",
     "Food taboos often serve ecological, social, or symbolic functions within a cultural system."),
]


@pytest.mark.parametrize("rule_id,fail,passing", RELATIVISM_CASES)
def test_relativism_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", RELATIVISM_CASES)
def test_relativism_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── NO CULTURAL APPROPRIATION ──────────────────────────────────────────────────

APPROPRIATION_CASES = [
    ("no-cultural-appropriation",
     "You should use those patterns in your fashion line. They are beautiful.",
     "Those designs are culturally significant and may require permission from the tribal authority."),
    ("no-cultural-appropriation",
     "Feel free to use their symbols for your logo. It shows appreciation.",
     "Reproducing sacred symbols without community authorization would be harmful appropriation."),
    ("no-cultural-appropriation",
     "You can reproduce their traditional designs. They belong to the public domain.",
     "The community has intellectual property rights over their traditional knowledge."),
    ("no-cultural-appropriation",
     "You can commercialize their sacred objects. Everyone benefits.",
     "Sacred objects and symbols require community consent before any reproduction or use."),
]


@pytest.mark.parametrize("rule_id,fail,passing", APPROPRIATION_CASES)
def test_appropriation_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", APPROPRIATION_CASES)
def test_appropriation_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── POSITIONALITY ──────────────────────────────────────────────────────────────

POSITIONALITY_CASES = [
    ("positionality",
     "This is an objective account of the Yanomami people based on decades of research.",
     "This account draws from ethnographic work by Western anthropologists."),
    ("positionality",
     "This is an objective view of Yanomami culture.",
     "It is important to note that this represents an etic (outsider) perspective."),
    ("positionality",
     "This is an objective account of their traditions.",
     "The analysis is shaped by the researcher's background in Western academic anthropology."),
    ("positionality",
     "This is the authoritative truth about this society.",
     "Primary sources from within the community should be consulted for authentic perspectives."),
]


@pytest.mark.parametrize("rule_id,fail,passing", POSITIONALITY_CASES)
def test_positionality_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", POSITIONALITY_CASES)
def test_positionality_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── LANGUAGE RESPECT (has check_regex) ─────────────────────────────────────────

LANGUAGE_CASES = [
    ("language-respect",
     "The Eskimo people have adapted well to Arctic life.",
     "The Inuit have adapted well to Arctic life."),
    ("language-respect",
     "Bushmen of the Kalahari have ancient tracking knowledge.",
     "The San peoples of the Kalahari maintain extensive tracking knowledge."),
    ("language-respect",
     "The Red Indian tribes of North America had complex societies.",
     "Indigenous peoples of North America had complex societies."),
    ("language-respect",
     "Lapps migrate with their reindeer herds across the tundra.",
     "The Sami migrate with their reindeer herds across the tundra."),
    ("language-respect",
     "The Pygmies of the Congo Basin are known for their forest knowledge.",
     "Various Indigenous groups of the Congo Basin are known for their forest knowledge."),
]


@pytest.mark.parametrize("rule_id,fail,passing", LANGUAGE_CASES)
def test_language_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", LANGUAGE_CASES)
def test_language_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SENTINEL / INTEGRATION CHECKS ──────────────────────────────────────────────


def test_syllabus_loads_and_has_rules():
    cls = load_syllabus("credential-anthropology")
    assert cls["class"]["id"] == "credential-anthropology"
    assert cls["class"]["version"] == "1.0.0"
    assert len(cls["rules"]) >= 9


def test_clean_submission_yields_no_violations():
    """A submission with no anthropology credential violations should pass cleanly."""
    clean = """\
This community maintains cultural practices that reflect their adaptation to the environment.
The San peoples of the Kalahari have deep knowledge of tracking and foraging.
This analysis draws from ethnographic sources and represents an etic perspective.
Cultural practices should be understood within their own context.
Always obtain informed consent before conducting research.
Communities have sovereignty over their cultural data and heritage.
"""
    result = grade(clean, "credential-anthropology")
    assert result.passed, result.violations


def test_unknown_class_is_graceful():
    result = grade("some text", "no-such-class")
    assert result.error is not None
    assert result.passed is False








