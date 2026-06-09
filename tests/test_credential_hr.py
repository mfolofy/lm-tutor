"""Tests for credential-hr class — regex checks, grader functions, and YAML integrity.

Requirements:
  - pip install pytest pyyaml
  - Run: pytest tests/test_credential_hr.py -v
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

# ── Paths ────────────────────────────────────────────────────────────────────

CLASS_DIR = Path(__file__).resolve().parent.parent / "tutor" / "classes" / "credential-hr"
YAML_PATH = CLASS_DIR / "class.yaml"
SOURCES_PATH = CLASS_DIR / "SOURCES.md"
INIT_PATH = CLASS_DIR / "__init__.py"
REQS_PATH = CLASS_DIR / "_requirements.txt"
GRADER_PATH = CLASS_DIR / "grader.py"
TEST_DIR = Path(__file__).resolve().parent


# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def class_data() -> dict:
    """Load and parse class.yaml."""
    with open(YAML_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def rules(class_data: dict) -> list[dict]:
    """Extract the rules list from class data."""
    return class_data["rules"]


# ── YAML STRUCTURAL TESTS ────────────────────────────────────────────────────


class TestYamlStructure:
    """Verify the YAML file has the correct structural skeleton."""

    def test_class_header(self, class_data: dict):
        cls = class_data["class"]
        assert cls["id"] == "credential-hr"
        assert cls["title"].startswith("Credential-HR")
        assert isinstance(cls["version"], str)
        assert isinstance(cls["sources"], list)
        assert len(cls["sources"]) > 0
        assert isinstance(cls["prerequisites"], list)
        assert isinstance(cls["target_violations"], list)
        assert isinstance(cls["estimated_cost_tokens"], int)

    def test_rule_count(self, rules: list[dict]):
        """Must have 14-17 rules."""
        assert 14 <= len(rules) <= 17, f"Expected 14-17 rules, got {len(rules)}"

    def test_checkable_rule_count(self, rules: list[dict]):
        """Must have 4-6 rules with check_regex."""
        checkable = [r for r in rules if "check_regex" in r]
        assert 4 <= len(checkable) <= 6, (
            f"Expected 4-6 checkable rules, got {len(checkable)}"
        )

    def test_all_rules_have_required_fields(self, rules: list[dict]):
        """Every rule must have id, severity, rule, and at least one framework example."""
        for rule in rules:
            assert "id" in rule, f"Rule missing 'id': {rule}"
            assert "severity" in rule, f"Rule '{rule['id']}' missing severity"
            assert "rule" in rule, f"Rule '{rule['id']}' missing rule text"
            framework_sections = [
                k for k in rule if k.startswith("framework_")
            ]
            assert len(framework_sections) >= 2, (
                f"Rule '{rule['id']}' needs at least 2 framework examples, got {framework_sections}"
            )

    def test_severity_values(self, rules: list[dict]):
        """Severity must be 'fundamental' or 'advanced'."""
        for rule in rules:
            assert rule["severity"] in ("fundamental", "advanced"), (
                f"Rule '{rule['id']}' has invalid severity: {rule['severity']}"
            )

    def test_unique_rule_ids(self, rules: list[dict]):
        """All rule IDs must be unique."""
        ids = [r["id"] for r in rules]
        duplicates = [i for i in ids if ids.count(i) > 1]
        assert len(duplicates) == 0, f"Duplicate rule IDs: {set(duplicates)}"

    def test_target_violations_match_rules(self, class_data: dict):
        """Target violations should be kebab-case and roughly match rule coverage."""
        violations = class_data["class"]["target_violations"]
        for v in violations:
            assert "-" in v, f"Violation '{v}' is not kebab-case"


# ── CHECKABLE RULE REGEX TESTS ──────────────────────────────────────────────


def _get_checkable_rules(rules: list[dict]) -> list[tuple[str, str, str]]:
    """Return (rule_id, rule_text, regex_pattern) for rules with check_regex."""
    result = []
    for r in rules:
        if "check_regex" in r:
            result.append((r["id"], r["rule"], r["check_regex"]))
    return result


class TestCheckableRules:
    """Test each check_regex: FAIL strings must match, PASS strings must not."""

    @pytest.fixture(scope="class")
    def checkable(self, rules: list[dict]) -> list[tuple[str, str, str]]:
        return _get_checkable_rules(rules)

    @pytest.mark.parametrize(
        "rule_id, text, reason",
        [
            # ── confidentiality ──────────────────────────────────────────
            (
                "confidentiality",
                "disclose employee records without authorization",
                "should detect explicit unauthorized disclosure of employee records",
            ),
            (
                "confidentiality",
                "reveal medical information without consent",
                "should detect revealing medical info without consent",
            ),
            (
                "confidentiality",
                "share confidential employee data without need to know",
                "should detect sharing employee data without need to know",
            ),
            # ── anti-discrimination ─────────────────────────────────────
            (
                "anti-discrimination",
                "we only hire recent college graduates",
                "should detect age-discriminatory hiring preference",
            ),
            (
                "anti-discrimination",
                "prefer young candidates for the role",
                "should detect age preference",
            ),
            (
                "anti-discrimination",
                "we want recent grad for this position",
                "should detect recent grad preference",
            ),
            (
                "anti-discrimination",
                "we only hire American-born workers",
                "should detect national origin discrimination",
            ),
            # ── performance-management ──────────────────────────────────
            (
                "performance-management",
                "fire them during the PIP",
                "should detect termination during PIP",
            ),
            (
                "performance-management",
                "terminate the employee without completing the progressive discipline process",
                "should detect termination without progressive discipline",
            ),
            (
                "performance-management",
                "let the employee go without a performance improvement plan",
                "should detect firing without PIP",
            ),
            # ── harassment-prevention ───────────────────────────────────
            (
                "harassment-prevention",
                "it is not a big deal just ignore it",
                "should detect minimizing harassment complaint",
            ),
            (
                "harassment-prevention",
                "do not make a fuss about it",
                "should detect dismissive response to complaint",
            ),
            (
                "harassment-prevention",
                "that is just office banter",
                "should detect excusing harassment as banter",
            ),
            (
                "harassment-prevention",
                "no need to investigate just let it go",
                "should detect dismissing investigation need",
            ),
            # ── compensation-practices ──────────────────────────────────
            (
                "compensation-practices",
                "classify all your employees as exempt",
                "should detect blanket exempt classification",
            ),
            (
                "compensation-practices",
                "label your workers as independent contractors",
                "should detect misclassification as ICs",
            ),
            (
                "compensation-practices",
                "make your staff salaried exempt to avoid overtime",
                "should detect exempt misclassification to avoid OT",
            ),
            # ── recordkeeping ───────────────────────────────────────────
            (
                "recordkeeping",
                "you can delete those old employee records",
                "should detect unauthorized disposal of employee records",
            ),
            (
                "recordkeeping",
                "you do not need to keep those I-9 documents",
                "should detect advice to discard I-9s",
            ),
            (
                "recordkeeping",
                "you can purge the old personnel files from 2020",
                "should detect premature purging of records",
            ),
        ],
    )
    def test_fail_matches(
        self,
        checkable: list[tuple[str, str, str]],
        rule_id: str,
        text: str,
        reason: str,
    ):
        """FAIL: check_regex must match the given violation text."""
        for rid, _rule, regex in checkable:
            if rid == rule_id:
                pattern = re.compile(regex, re.IGNORECASE)
                assert pattern.search(text), (
                    f"FAIL pattern for '{rule_id}' did not match '{text}': {reason}\n"
                    f"  Pattern: {regex}"
                )
                return
        pytest.fail(f"Rule '{rule_id}' not found in checkable rules")

    @pytest.mark.parametrize(
        "rule_id, text, reason",
        [
            # ── confidentiality ──────────────────────────────────────────
            (
                "confidentiality",
                "You should consult your HR department before sharing employee information.",
                "should NOT match legitimate procedural advice",
            ),
            (
                "confidentiality",
                "Only share medical information with authorized personnel on a need-to-know basis.",
                "should NOT match proper confidentiality guidance",
            ),
            # ── anti-discrimination ─────────────────────────────────────
            (
                "anti-discrimination",
                "Focus on skills and experience relevant to the job requirements.",
                "should NOT match legal hiring criteria",
            ),
            (
                "anti-discrimination",
                "Seeking candidates with 3+ years of Python development experience.",
                "should NOT match legitimate job qualification",
            ),
            # ── performance-management ──────────────────────────────────
            (
                "performance-management",
                "Follow progressive discipline: verbal warning, written warning, PIP, then termination if needed.",
                "should NOT match proper progressive discipline advice",
            ),
            (
                "performance-management",
                "Document each step of the disciplinary process thoroughly.",
                "should NOT match documentation advice",
            ),
            # ── harassment-prevention ───────────────────────────────────
            (
                "harassment-prevention",
                "All harassment complaints must be investigated promptly and impartially.",
                "should NOT match proper harassment protocol",
            ),
            (
                "harassment-prevention",
                "Document the complaint and interview the parties involved.",
                "should NOT match investigation steps",
            ),
            # ── compensation-practices ──────────────────────────────────
            (
                "compensation-practices",
                "Exempt classification requires meeting the salary level, salary basis, and duties tests.",
                "should NOT match correct exemption explanation",
            ),
            (
                "compensation-practices",
                "Evaluate each role independently using the economic realities test for IC classification.",
                "should NOT match proper classification advice",
            ),
            # ── recordkeeping ───────────────────────────────────────────
            (
                "recordkeeping",
                "FLSA requires payroll records to be retained for 3 years.",
                "should NOT match retention period explanation",
            ),
            (
                "recordkeeping",
                "Maintain medical records separately from personnel files.",
                "should NOT match proper recordkeeping guidance",
            ),
        ],
    )
    def test_pass_no_match(
        self,
        checkable: list[tuple[str, str, str]],
        rule_id: str,
        text: str,
        reason: str,
    ):
        """PASS: check_regex must NOT match legitimate text."""
        for rid, _rule, regex in checkable:
            if rid == rule_id:
                pattern = re.compile(regex, re.IGNORECASE)
                assert not pattern.search(text), (
                    f"PASS pattern for '{rule_id}' matched '{text}': {reason}\n"
                    f"  Pattern: {regex}"
                )
                return
        pytest.fail(f"Rule '{rule_id}' not found in checkable rules")


# ── TEACHING-ONLY RULE CONTENT TESTS ────────────────────────────────────────


class TestTeachingRules:
    """Verify teaching-only rules have substantive content and no check_regex."""

    def test_no_check_regex_on_teaching_rules(self, rules: list[dict]):
        """Teaching-only rules must NOT have check_regex."""
        teaching_ids = {
            "scope-of-practice",
            "hiring-practices",
            "accommodations",
            "employment-law-flsa",
            "employment-law-fmla",
            "termination",
            "layoff-compliance",
            "labor-relations",
            "immigration-compliance",
            "employee-privacy",
            "disclaimer-presence",
        }
        for rule in rules:
            if rule["id"] in teaching_ids:
                assert "check_regex" not in rule, (
                    f"Teaching-only rule '{rule['id']}' should not have check_regex"
                )

    def test_teaching_rules_have_minimum_rule_length(self, rules: list[dict]):
        """Teaching-only rules must have substantive rule text."""
        teaching_ids = {
            "scope-of-practice",
            "hiring-practices",
            "accommodations",
            "employment-law-flsa",
            "employment-law-fmla",
            "termination",
            "layoff-compliance",
            "labor-relations",
            "immigration-compliance",
            "employee-privacy",
            "disclaimer-presence",
        }
        for rule in rules:
            if rule["id"] in teaching_ids:
                assert len(rule["rule"]) >= 150, (
                    f"Teaching rule '{rule['id']}' rule text too short ({len(rule['rule'])} chars)"
                )


# ── FRAMEWORK EXAMPLE TESTS ──────────────────────────────────────────────────


class TestFrameworkExamples:
    """Verify each framework section has both FAIL and PASS examples."""

    def test_framework_examples_have_fail_and_pass(self, rules: list[dict]):
        """Each framework section should contain both # FAIL and # PASS markers."""
        for rule in rules:
            for key in rule:
                if key.startswith("framework_"):
                    content = rule[key]
                    assert "# FAIL" in content, (
                        f"Rule '{rule['id']}' section '{key}' missing # FAIL example"
                    )
                    assert "# PASS" in content, (
                        f"Rule '{rule['id']}' section '{key}' missing # PASS example"
                    )


# ── FILE EXISTENCE TESTS ─────────────────────────────────────────────────────


class TestFileStructure:
    """Verify all expected files exist."""

    def test_class_yaml_exists(self):
        assert YAML_PATH.exists(), f"Missing: {YAML_PATH}"

    def test_sources_md_exists(self):
        assert SOURCES_PATH.exists(), f"Missing: {SOURCES_PATH}"

    def test_init_py_exists(self):
        assert INIT_PATH.exists(), f"Missing: {INIT_PATH}"

    def test_requirements_txt_exists(self):
        assert REQS_PATH.exists(), f"Missing: {REQS_PATH}"

    def test_grader_py_exists(self):
        assert GRADER_PATH.exists(), f"Missing: {GRADER_PATH}"

    def test_sources_md_substantial(self):
        """SOURCES.md should have meaningful content."""
        content = SOURCES_PATH.read_text(encoding="utf-8")
        assert len(content) > 2000, "SOURCES.md too short"
        assert "FLSA" in content
        assert "FMLA" in content
        assert "ADA" in content
        assert "Title VII" in content
        assert "EEOC" in content

    def test_all_rules_referenced_in_sources(self, rules: list[dict]):
        """Each rule id should appear in the SOURCES.md citation table."""
        content = SOURCES_PATH.read_text(encoding="utf-8")
        for rule in rules:
            assert f"`{rule['id']}`" in content, (
                f"Rule '{rule['id']}' not found in SOURCES.md citation table"
            )


# ── GRADER FUNCTION TESTS ────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def grader_module():
    """Import the grader module (may fail if dependencies missing)."""
    import importlib

    spec = importlib.util.spec_from_file_location("credential_hr_grader", GRADER_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestGraderFunctions:
    """Test the Layer 2 grader functions."""

    def test_aggregate_grader_exists(self, grader_module):
        """The module must export grade_credential_hr."""
        assert hasattr(grader_module, "grade_credential_hr")

    def test_aggregate_grader_returns_list(self, grader_module):
        """grade_credential_hr returns a list of dicts."""
        result = grader_module.grade_credential_hr("This is some neutral text about HR.")
        assert isinstance(result, list)
        assert len(result) > 0
        for item in result:
            assert "grader_id" in item
            assert "pass" in item
            assert "reason" in item
            assert isinstance(item["pass"], bool)

    def test_disclaimer_presence_no_trigger(self, grader_module):
        """No HR advice language = pass (not required)."""
        result = grader_module.grade_disclaimer_presence(
            "The weather today is sunny and warm."
        )
        assert result["pass"] is True

    def test_disclaimer_presence_trigger_no_disclaimer(self, grader_module):
        """HR advice language without disclaimer = fail."""
        result = grader_module.grade_disclaimer_presence(
            "You should hire the candidate with the most experience."
        )
        assert result["pass"] is False

    def test_disclaimer_presence_with_disclaimer(self, grader_module):
        """HR advice language with disclaimer = pass."""
        text = (
            "You should hire the candidate with the most experience. "
            "I am an AI assistant, not an HR professional. "
            "Final hiring decisions must rest with human management. "
            "Consult your HR department for binding decisions."
        )
        result = grader_module.grade_disclaimer_presence(text)
        assert result["pass"] is True

    def test_termination_process_no_trigger(self, grader_module):
        """No termination language = pass."""
        result = grader_module.grade_termination_process(
            "Here is the quarterly financial report."
        )
        assert result["pass"] is True

    def test_termination_process_with_elements(self, grader_module):
        """Termination language with process elements = pass."""
        text = (
            "When terminating an employee, ensure the decision is documented "
            "and provide a termination notice. "
            "The employee must receive COBRA continuation coverage information "
            "and final pay including accrued vacation. "
            "Unemployment insurance eligibility depends on the circumstances."
        )
        result = grader_module.grade_termination_process(text)
        assert result["pass"] is True

    def test_accommodation_missing_interactive_process(self, grader_module):
        """Accommodation language without interactive process = fail."""
        text = (
            "The employee requested an accommodation for their disability. "
            "We should deny it because it would be too expensive."
        )
        result = grader_module.grade_accommodation_interactive_process(text)
        assert result["pass"] is False

    def test_accommodation_with_interactive_process(self, grader_module):
        """Accommodation language with interactive process = pass."""
        text = (
            "When an employee requests a reasonable accommodation, "
            "engage in the interactive process with the employee to "
            "explore potential accommodations on an individualized basis."
        )
        result = grader_module.grade_accommodation_interactive_process(text)
        assert result["pass"] is True

    def test_discipline_without_progression(self, grader_module):
        """Discipline language without progressive steps = fail."""
        text = "Discipline the employee immediately without a written warning."
        result = grader_module.grade_discipline_progression(text)
        assert result["pass"] is False

    def test_discipline_with_progression(self, grader_module):
        """Discipline language with progressive steps = pass."""
        text = (
            "Start with a verbal warning, then a written warning, "
            "then a performance improvement plan before considering termination."
        )
        result = grader_module.grade_discipline_progression(text)
        assert result["pass"] is True

    def test_layoff_without_warn(self, grader_module):
        """Mass layoff language without WARN = fail."""
        text = (
            "The company needs a mass layoff of employees at the Chicago facility next month."
        )
        result = grader_module.grade_layoff_warn(text)
        assert result["pass"] is False

    def test_layoff_with_warn(self, grader_module):
        """Mass layoff language with WARN = pass."""
        text = (
            "Since this layoff affects over 50 employees at a single site, "
            "the WARN Act requires 60 calendar days advance written notice "
            "to employees, the state dislocated worker unit, and local government."
        )
        result = grader_module.grade_layoff_warn(text)
        assert result["pass"] is True
