"""Tests for the design-tokens class."""
import pytest
from tutor.eval import grade, harness

def _r(s): return {v.rule for v in grade(s, "design-tokens").violations}

# no-dark-mode-tokens check_regex
DARK_CASES = [
    ("no-dark-mode-tokens",
     "@media (prefers-color-scheme: dark) { :root { --bg: #111; --text: #eee; } }",
     '[data-theme="dark"] { --color-bg: var(--color-neutral-900); --color-text: var(--color-neutral-0); }'),
]
@pytest.mark.parametrize("rid,fail,p", DARK_CASES)
def test_dark_fail(rid, fail, p): assert rid in _r(fail)
@pytest.mark.parametrize("rid,fail,p", DARK_CASES)
def test_dark_pass(rid, fail, p): assert rid not in _r(p)

TEACHING_RULES = [
    "hardcoded-colors","hardcoded-spacing","flat-token-names","no-token-file",
    "inline-magic-values","no-token-alias","inconsistent-token-scale",
    "no-build-pipeline","no-token-docs","no-validation","no-composite-types",
    "figma-code-drift","token-platform-mismatch","css-root-bloat","no-color-token-enough",
]
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("design-tokens")["rules"]}
    for rid in TEACHING_RULES: assert rid in ids, f"{rid} missing"
def test_all_examples():
    syllabus = harness.load_syllabus("design-tokens")
    for rule in syllabus["rules"]:
        assert any(k.startswith("framework_") for k in rule), f"Rule {rule['id']} has no framework examples"
def test_count():
    s = harness.load_syllabus("design-tokens")
    assert s["class"]["rule_count"] == len(s["rules"])
