"""Tests for the perf class — proves each rule's FAIL/PASS behaviour.

For each rule with a checker (check_selector or check_regex), a FAIL snippet
MUST produce that rule's violation and a PASS snippet MUST NOT. Teaching-only
rules (no checker) are validated for content presence only.

Run with: pytest tests/
"""

import pytest

from tutor.eval import grade
from tutor.eval.harness import load_syllabus


def _rules_for(submission: str) -> set[str]:
    result = grade(submission, "perf")
    return {v.rule for v in result.violations}


# ── CHECKER RULES (4 rules with check_selector / check_regex) ────────────────

CHECKER_CASES = [
    # (rule_id, FAIL snippet, PASS snippet)
    # img-dimensions — check_selector: img[src]:not([width]):not([height])
    ("img-dimensions",
     '<img src="photo.jpg">',
     '<img src="photo.jpg" width="800" height="600">'),
    # css-import — check_regex: @import\s+url
    ("css-import",
     '@import url("components.css");',
     '<link rel="stylesheet" href="components.css">'),
    ("css-import",
     "@import url('components.css');",
     '<link rel="stylesheet" href="components.css">'),
    # font-display — check_regex: font-display:\s*block\b
    ("font-display",
     '@font-face { font-display: block; }',
     '@font-face { font-display: swap; }'),
    ("font-display",
     '@font-face { font-display:block; }',
     '@font-face { font-display: fallback; }'),
    # document-write — check_regex: document\.write\s*\(
    ("document-write",
     '<script>document.write("hello");</script>',
     '<script>console.log("hello");</script>'),
]


@pytest.mark.parametrize("rule_id,fail,passing", CHECKER_CASES)
def test_checker_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CHECKER_CASES)
def test_checker_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SENTINEL / INTEGRATION CHECKS ────────────────────────────────────────────


def test_syllabus_loads_and_has_rules():
    cls = load_syllabus("perf")
    assert cls["class"]["id"] == "perf"
    assert cls["class"]["version"] == "1.0.0"
    assert len(cls["rules"]) >= 16  # 18 rules expected


def test_clean_page_passes():
    clean = (
        '<html><head><title>Perf Test</title>'
        '<link rel="stylesheet" href="styles.css">'
        '<style>@font-face { font-family: "Inter"; font-display: swap; }</style>'
        '</head><body>'
        '<img src="hero.webp" width="1200" height="600" alt="Hero">'
        '<script>console.log("ready");</script>'
        '</body></html>'
    )
    result = grade(clean, "perf")
    assert result.passed, result.violations


def test_unknown_class_is_graceful():
    result = grade("<div>", "no-such-class")
    assert result.error is not None
    assert result.passed is False


# ── LCP TEACHING CONTENT ─────────────────────────────────────────────────────


def test_lcp_rule_exists_and_teaches():
    """LCP is a teaching-only rule (no checker). Verify it's in the syllabus."""
    cls = load_syllabus("perf")
    rule_ids = {r["id"] for r in cls["rules"]}
    assert "lcp" in rule_ids
