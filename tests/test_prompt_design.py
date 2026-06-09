"""Tests for the prompt-design class — proves each check_regex rule's FAIL/PASS behaviour.

For each rule with a check_regex, a FAIL snippet MUST produce that rule's
violation and a PASS snippet MUST NOT. Teaching-only rules (no check_*) are
verified via syllabus loading and content-presence tests.

Run with: pytest tests/
"""

import pytest

from tutor.eval import grade
from tutor.eval.harness import load_syllabus


def _rules_for(submission: str) -> set[str]:
    result = grade(submission, "prompt-design")
    return {v.rule for v in result.violations}


# ── TEMPERATURE RANGE ─────────────────────────────────────────────────────────

TEMP_CASES = [
    ("temperature-range",
     'temperature: 0.4',
     'temperature: 0.1'),
    ("temperature-range",
     'temperature = 0.5',
     'temperature = 0.0'),
    ("temperature-range",
     'temperature="0.6"',
     'temperature: 0.8'),
    ("temperature-range",
     '"temperature": 0.35',
     '"temperature": 0.0'),
    ("temperature-range",
     'temperature: 0.3',
     'temperature: 0.2'),
]


@pytest.mark.parametrize("rule_id,fail,passing", TEMP_CASES)
def test_temperature_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", TEMP_CASES)
def test_temperature_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── VERBOSE PROMPTING ─────────────────────────────────────────────────────────

VERBOSE_CASES = [
    ("verbose-prompting",
     "It is important to note that you should validate user inputs.",
     "[RULE] Validate all user inputs server-side before processing."),
    ("verbose-prompting",
     "it is essential to remember that the API key must be stored securely.",
     "Store the API key securely using environment variables."),
    ("verbose-prompting",
     "Kindly review the following code for correctness.",
     "Review the following code for correctness."),
    ("verbose-prompting",
     "Please be sure to include comprehensive error handling.",
     "Include error handling for: network, auth, and rate limits."),
    ("verbose-prompting",
     "It is critical to understand that ordering matters here.",
     "[RULE] Order matters: role before task, constraint before generation."),
]


@pytest.mark.parametrize("rule_id,fail,passing", VERBOSE_CASES)
def test_verbose_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", VERBOSE_CASES)
def test_verbose_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── INSTRUCTION LEAK ──────────────────────────────────────────────────────────

LEAK_CASES = [
    ("instruction-leak",
     "Remember that you are a helpful assistant. Generate a summary.",
     "You are a helpful assistant. Generate a summary of the text."),
    ("instruction-leak",
     "Don't forget you should respond in valid JSON format.",
     "Respond in valid JSON format with keys: title, summary, confidence."),
    ("instruction-leak",
     "Keep in mind that you can use the tools provided to answer questions.",
     "You can use the tools provided to answer questions."),
    ("instruction-leak",
     "Please note that you are expected to provide citations for all claims.",
     "Provide citations for all claims."),
]


@pytest.mark.parametrize("rule_id,fail,passing", LEAK_CASES)
def test_leak_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", LEAK_CASES)
def test_leak_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── PROMPT INJECTION ──────────────────────────────────────────────────────────

INJECTION_CASES = [
    ("prompt-injection",
     'f"You are a helpful assistant. The user says: {user_input}. Respond helpfully."',
     '"You are a helpful assistant. Keep responses concise."'),
    ("prompt-injection",
     'f"Your task is to answer the following: {question}"',
     'system_prompt = "You are a classifier. Classify the sentiment."'),
    ("prompt-injection",
     'system = f"You will process this request: {message}"',
     'user_message = user_input'),
]


@pytest.mark.parametrize("rule_id,fail,passing", INJECTION_CASES)
def test_injection_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", INJECTION_CASES)
def test_injection_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── CONSTRAINT PLACEMENT ──────────────────────────────────────────────────────

CONSTRAINT_CASES = [
    ("constraint-placement",
     "Write a Python function. Add comprehensive type hints, error handling, "
     "and edge case coverage. Do not use built-in sort functions.",
     "Do not use built-in sort functions. Write a Python function to sort a list."),
    ("constraint-placement",
     "Create a React component. It should handle loading, empty, and error "
     "states with proper accessibility attributes. Avoid using any external "
     "table libraries. Always handle edge cases in every component.",
     "Avoid external table libraries. Create a React component for a data table."),
    ("constraint-placement",
     "Implement a search endpoint with pagination, filtering, sorting, and "
     "caching. Make sure to add rate limiting and input validation.",
     "Make sure to add rate limiting. Implement a search endpoint."),
]


@pytest.mark.parametrize("rule_id,fail,passing", CONSTRAINT_CASES)
def test_constraint_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CONSTRAINT_CASES)
def test_constraint_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SENTINEL / INTEGRATION CHECKS ─────────────────────────────────────────────


def test_syllabus_loads_and_has_rules():
    cls = load_syllabus("prompt-design")
    assert cls["class"]["id"] == "prompt-design"
    assert cls["class"]["version"] == "1.0.0"
    assert len(cls["rules"]) >= 16  # minimum 16 rules


def test_all_rules_have_id():
    cls = load_syllabus("prompt-design")
    ids = [r["id"] for r in cls["rules"]]
    assert len(ids) == len(set(ids)), "Duplicate rule IDs found"


def test_all_rules_have_severity():
    cls = load_syllabus("prompt-design")
    valid = {"fundamental", "advanced", "warning"}
    for r in cls["rules"]:
        assert r.get("severity") in valid, f"{r['id']}: invalid severity"


def test_regex_rules_have_framework_examples():
    cls = load_syllabus("prompt-design")
    for r in cls["rules"]:
        if r.get("check_regex"):
            keys = [k for k in r if k.startswith("framework_")]
            assert keys, f"{r['id']}: check_regex rule has no framework examples"


def test_teaching_rules_have_framework_examples():
    cls = load_syllabus("prompt-design")
    for r in cls["rules"]:
        if not r.get("check_regex") and not r.get("check_selector"):
            keys = [k for k in r if k.startswith("framework_")]
            assert keys, f"{r['id']}: teaching rule has no framework examples"


def test_well_structured_prompt_passes_all_checks():
    """A well-structured prompt should pass all Layer 1 regex checks."""
    prompt = (
        "You are a senior Python developer.\n"
        "Constraints: use only stdlib, no pandas dependency, handle quoted fields.\n"
        "Do not use eval() or exec(). Do not import csv module either.\n"
        "Temperature: 0.1\n"
        "Write a function to parse CSV files.\n"
        "Output: Python code with type hints.\n"
        "Return the complete function definition."
    )
    result = grade(prompt, "prompt-design")
    assert result.passed, f"Expected clean prompt to pass, got: {result.violations}"


def test_compact_prompt_with_landmarks_passes():
    """A compact prompt using [RULE] markers should pass verbose check."""
    prompt = (
        "[RULE] Role: senior backend engineer\n"
        "[RULE] Task: review auth middleware for token handling\n"
        "[RULE] Output: list of findings with severity and line numbers\n"
        "[RULE] Temperature: 0.0\n"
    )
    result = grade(prompt, "prompt-design")
    assert result.passed, f"Expected compact prompt to pass, got: {result.violations}"


def test_unknown_class_is_graceful():
    result = grade("<div>", "no-such-class")
    assert result.error is not None
    assert result.passed is False
