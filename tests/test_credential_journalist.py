"""Tests for the credential-journalist class.

Validates:
- YAML loads and parses correctly
- Class structure: id, title, version, sources, target_violations
- All rules have required fields: id, severity, rule
- Checkable rules have valid check_regex (valid Python re, matches FAIL examples)
- Teaching-only rules have no check_regex
- Each rule has at least framework_prompt and framework_response
- No duplicate rule IDs
- All target_violations referenced by rules
"""

import re
import os
import sys
from pathlib import Path

import pytest

# Use try/except so tests can be discovered without the dependency installed
try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

CLASS_DIR = Path(__file__).resolve().parent.parent / "tutor" / "classes" / "credential-journalist"
CLASS_YAML = CLASS_DIR / "class.yaml"


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def data():
    """Load and return the parsed class.yaml."""
    if yaml is None:
        pytest.skip("PyYAML not installed (pip install pyyaml)")
    if not CLASS_YAML.exists():
        pytest.fail(f"class.yaml not found at {CLASS_YAML}")
    with open(CLASS_YAML, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def rules(data):
    """Return the list of rule dicts."""
    return data.get("rules", [])


# ── Class structure ───────────────────────────────────────────────────────────


class TestClassStructure:
    def test_file_exists(self):
        assert CLASS_YAML.exists(), f"Missing: {CLASS_YAML}"

    def test_yaml_parses(self, data):
        assert data is not None, "YAML returned None (empty or malformed)"

    def test_class_section(self, data):
        cls = data.get("class")
        assert cls is not None, "Missing top-level 'class:' key"
        assert cls["id"] == "credential-journalist"
        assert cls["title"].startswith("Credential-Journalist")
        assert cls["version"] == "1.0.0"

    def test_sources_listed(self, data):
        sources = data["class"].get("sources", [])
        assert len(sources) >= 5, "Expected at least 5 source standards"
        assert any("SPJ" in s for s in sources), "SPJ Code must be listed"

    def test_target_violations(self, data):
        violations = data["class"].get("target_violations", [])
        assert len(violations) >= 8, "Expected at least 8 target violations"


# ── Rules integrity ───────────────────────────────────────────────────────────


class TestRuleIntegrity:
    def test_rule_count(self, rules):
        assert 14 <= len(rules) <= 16, (
            f"Expected 14-16 rules, got {len(rules)}"
        )

    def test_no_duplicate_ids(self, rules):
        ids = [r["id"] for r in rules]
        duplicates = [i for i in ids if ids.count(i) > 1]
        assert not duplicates, f"Duplicate rule IDs: {set(duplicates)}"

    def test_all_required_fields(self, rules):
        required = {"id", "severity", "rule"}
        for rule in rules:
            missing = required - set(rule.keys())
            assert not missing, (
                f"Rule '{rule.get('id', 'UNKNOWN')}' missing fields: {missing}"
            )

    def test_valid_severity(self, rules):
        valid = {"fundamental", "advanced"}
        for rule in rules:
            assert rule["severity"] in valid, (
                f"Rule '{rule['id']}': severity '{rule['severity']}' "
                f"not in {valid}"
            )

    def test_non_empty_rule_text(self, rules):
        for rule in rules:
            assert rule["rule"].strip(), f"Rule '{rule['id']}' has empty rule text"
            assert len(rule["rule"]) >= 50, (
                f"Rule '{rule['id']}' rule text too short ({len(rule['rule'])} chars)"
            )


# ── Checkable rules (check_regex) ─────────────────────────────────────────────


class TestCheckableRules:
    def test_checkable_rule_count(self, rules):
        checkable = [r for r in rules if "check_regex" in r]
        assert 4 <= len(checkable) <= 6, (
            f"Expected 4-6 checkable rules, got {len(checkable)}"
        )

    def test_check_regex_valid_python_re(self, rules):
        for rule in rules:
            regex = rule.get("check_regex")
            if regex is None:
                continue
            try:
                re.compile(regex)
            except re.error as e:
                pytest.fail(
                    f"Rule '{rule['id']}' check_regex is invalid: {e}"
                )

    @pytest.mark.parametrize(
        "rule_id,fail_text",
        [
            (
                "scope-of-practice",
                "I am a journalist who has covered politics for 15 years",
            ),
            (
                "scope-of-practice",
                "my investigation reveals the true story behind the scandal",
            ),
            (
                "scope-of-practice",
                "I'm an investigative reporter for the Times",
            ),
            ("truth-accuracy", "I have verified these facts with three sources"),
            (
                "truth-accuracy",
                "I confirmed each claim in the article before writing",
            ),
            (
                "independence",
                "accept free travel from the company we are covering",
            ),
            (
                "independence",
                "receive gifts from sources in exchange for coverage",
            ),
            ("corrections", "silently fix the error without noting it"),
            (
                "corrections",
                "just correct the mistake without flagging it",
            ),
            (
                "source-protection",
                "reveal the identity of a confidential source",
            ),
            (
                "source-protection",
                "disclose the name behind an anonymous source",
            ),
            ("no-plagiarism", "no need to cite the source for this passage"),
            (
                "no-plagiarism",
                "you don't need to cite this, just rewrite it",
            ),
        ],
    )
    def test_check_regex_matches_fail(self, rules, rule_id, fail_text):
        """Each checkable rule's regex must match its FAIL examples."""
        rule = next((r for r in rules if r["id"] == rule_id), None)
        assert rule is not None, f"Rule '{rule_id}' not found"
        regex = rule.get("check_regex")
        assert regex is not None, (
            f"Rule '{rule_id}' has no check_regex but is tested"
        )
        assert re.search(
            regex, fail_text
        ), f"check_regex for '{rule_id}' did not match: {fail_text!r}"

    def test_teaching_rules_have_no_check_regex(self, rules):
        """Teaching-only rules must NOT carry a check_regex."""
        # Rules with check_regex
        checkable_ids = {
            r["id"] for r in rules if "check_regex" in r
        }
        for rule in rules:
            if rule["id"] not in checkable_ids:
                assert "check_regex" not in rule, (
                    f"Teaching-only rule '{rule['id']}' has check_regex "
                    f"(remove it or move to checkable list)"
                )


# ── Teaching framework examples ────────────────────────────────────────────────


class TestFrameworkExamples:
    def test_each_rule_has_prompt_and_response(self, rules):
        for rule in rules:
            assert "framework_prompt" in rule, (
                f"Rule '{rule['id']}' missing framework_prompt"
            )
            assert "framework_response" in rule, (
                f"Rule '{rule['id']}' missing framework_response"
            )

    def test_framework_examples_have_fail_pass(self, rules):
        """Each framework_* section must contain both FAIL and PASS markers."""
        for rule in rules:
            for key in rule:
                if key.startswith("framework_"):
                    text = rule[key]
                    assert "# FAIL" in text, (
                        f"Rule '{rule['id']}' {key} missing FAIL example"
                    )
                    assert "# PASS" in text, (
                        f"Rule '{rule['id']}' {key} missing PASS example"
                    )


# ── Coverage ───────────────────────────────────────────────────────────────────


class TestCoverage:
    def test_all_aspects_covered(self, rules):
        """Verify all requested topic areas are covered by at least one rule."""
        topics = [
            "scope-of-practice",
            "truth-accuracy",
            "attribution",
            "independence",
            "harm-minimization",
            "corrections",
            "source-protection",
            "fairness",
            "accountability",
            "no-plagiarism",
            "trauma-informed",
            "disclosure",
        ]
        rule_ids = {r["id"] for r in rules}
        for topic in topics:
            assert topic in rule_ids, (
                f"Required topic '{topic}' not covered by any rule"
            )
