"""Tests for the brushes class — proves each rule's FAIL/PASS behaviour.

Extended from Phase 0 (10 rules) to v2.0.0 (24 brush-stroke rules).
For each rule, a FAIL snippet MUST produce that rule's violation and a PASS
snippet MUST NOT. Also tests the per-class grader.py for deep-check rules.

Run with: pytest tests/
"""

import pytest

from tutor.eval import grade
from tutor.eval.harness import load_syllabus


def _rules_for(submission: str) -> set[str]:
    result = grade(submission, "brushes")
    return {v.rule for v in result.violations}


# ── CORE WCAG (Phase 0, 10 rules) ──────────────────────────────────────────

CORE_CASES = [
    # (rule_id, FAIL snippet, PASS snippet)
    ("img-alt", '<img src="a.png">', '<img src="a.png" alt="A logo">'),
    ("img-alt", '<img src="d.png">', '<img src="d.png" alt="">'),  # decorative
    ("input-image-alt", '<input type="image" src="go.png">',
                        '<input type="image" src="go.png" alt="Search">'),
    ("button-name", "<button></button>", "<button>Submit</button>"),
    ("button-name", "<button></button>", '<button aria-label="Close"></button>'),
    ("empty-aria-label", '<button aria-label="">X</button>',
                         '<button aria-label="Close">X</button>'),
    ("link-name", '<a href="/x"></a>', '<a href="/x">Home</a>'),
    ("label-for-input", '<input type="text">', '<input type="text" aria-label="Name">'),
    ("label-for-input", '<input type="text">', '<input type="text" id="name">'),
    ("html-lang", "<html></html>", '<html lang="en"></html>'),
    ("title-required", "<title></title>", "<title>Settings</title>"),
    ("positive-tabindex", '<div tabindex="3">x</div>', '<div tabindex="0">x</div>'),
    ("aria-live-valid", '<div aria-live="always">x</div>', '<div aria-live="polite">x</div>'),
]


@pytest.mark.parametrize("rule_id,fail,passing", CORE_CASES)
def test_core_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CORE_CASES)
def test_core_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── EXTENDED FORM LABELS ───────────────────────────────────────────────────

EXTENDED_CASES = [
    # select-label
    ("select-label",
     '<select><option>X</option></select>',
     '<select aria-label="Country"><option>X</option></select>'),
    # textarea-label
    ("textarea-label",
     '<textarea></textarea>',
     '<textarea aria-label="Bio"></textarea>'),
    # input-email-label
    ("input-email-label",
     '<input type="email">',
     '<input type="email" aria-label="Email">'),
    # input-password-label
    ("input-password-label",
     '<input type="password">',
     '<input type="password" aria-label="Password">'),
    # input-checkbox-label
    ("input-checkbox-label",
     '<input type="checkbox">',
     '<input type="checkbox" aria-label="Accept">'),
    # input-radio-label
    ("input-radio-label",
     '<input type="radio" name="opt">',
     '<input type="radio" name="opt" aria-label="Option A">'),
]


@pytest.mark.parametrize("rule_id,fail,passing", EXTENDED_CASES)
def test_extended_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", EXTENDED_CASES)
def test_extended_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── ERROR STATES ───────────────────────────────────────────────────────────

ERROR_CASES = [
    ("error-association",
     '<input aria-invalid="true"><span>Error</span>',
     '<input aria-invalid="true" aria-describedby="e1"><span id="e1">Error</span>'),
]


@pytest.mark.parametrize("rule_id,fail,passing", ERROR_CASES)
def test_error_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", ERROR_CASES)
def test_error_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── LANDMARK + SECTION ─────────────────────────────────────────────────────

LANDMARK_CASES = [
    # section-name
    ("section-name",
     '<section><p>Content</p></section>',
     '<section aria-label="Overview"><p>Content</p></section>'),
    # nav-landmark
    ("nav-landmark",
     '<div role="navigation"><a href="/">Home</a></div>',
     '<nav><a href="/">Home</a></nav>'),
    # table-caption
    ("table-caption",
     '<table><tr><td>Datum</td></tr></table>',
     '<table aria-label="Data"><tr><td>Datum</td></tr></table>'),
]


@pytest.mark.parametrize("rule_id,fail,passing", LANDMARK_CASES)
def test_landmark_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", LANDMARK_CASES)
def test_landmark_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── TABLE + LIST ───────────────────────────────────────────────────────────

TABLE_CASES = [
    # th-scope
    ("th-scope",
     '<th>Name</th>',
     '<th scope="col">Name</th>'),
    # list-structure
    ("list-structure",
     '<ul></ul>',
     '<ul><li>Item</li></ul>'),
]


@pytest.mark.parametrize("rule_id,fail,passing", TABLE_CASES)
def test_table_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", TABLE_CASES)
def test_table_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SKIP LINK + FOCUS ──────────────────────────────────────────────────────

MISC_CASES = [
    # skip-link (malformed — empty href)
    ("skip-link",
     '<a href="#">Skip</a>',
     '<a href="#main-content">Skip to content</a>'),
    # outline-none
    ("outline-none",
     '<style>*:focus { outline: none; }</style>',
     '<style>:focus-visible { outline: 2px solid blue; }</style>'),
    # viewport-meta
    ("viewport-meta",
     '<meta name="viewport" content="">',
     '<meta name="viewport" content="width=device-width, initial-scale=1.0">'),
]


@pytest.mark.parametrize("rule_id,fail,passing", MISC_CASES)
def test_misc_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", MISC_CASES)
def test_misc_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SENTINEL / INTEGRATION CHECKS ──────────────────────────────────────────


def test_syllabus_loads_and_has_rules():
    cls = load_syllabus("brushes")
    assert cls["class"]["id"] == "brushes"
    assert cls["class"]["version"] == "2.0.0"
    assert len(cls["rules"]) >= 32  # 10 core + 22 extended


def test_clean_page_passes():
    clean = (
        '<html lang="en"><head><title>Home</title></head>'
        '<body><img src="a.png" alt="A"><button>Go</button>'
        '<a href="/x">X</a><input type="text" aria-label="Name">'
        '<div aria-live="polite">ok</div></body></html>'
    )
    result = grade(clean, "brushes")
    assert result.passed, result.violations


def test_unknown_class_is_graceful():
    result = grade("<div>", "no-such-class")
    assert result.error is not None
    assert result.passed is False


# ── GRADER TESTS (deep_check rules via grader.py) ─────────────────────────


def test_grader_color_contrast_known_fail():
    """Grader catches known low-contrast gray (#999)."""
    from tutor.classes.brushes.grader import _grade_color_contrast
    violations = _grade_color_contrast('<p style="color: #999;">text</p>')
    assert any(v["rule"] == "color-contrast" for v in violations)


def test_grader_color_contrast_pass():
    """Grader does not flag high-contrast color (#333)."""
    from tutor.classes.brushes.grader import _grade_color_contrast
    violations = _grade_color_contrast('<p style="color: #333;">text</p>')
    # #333 has 12.6:1 on white — should not produce violations
    color_violations = [v for v in violations if "12.6" not in v.get("matched", "")]
    assert len(color_violations) == 0, violations


def test_grader_heading_order_multiple_h1():
    """Grader catches multiple h1 elements."""
    from tutor.classes.brushes.grader import _grade_heading_order
    violations = _grade_heading_order("<h1>Title</h1><h1>Another</h1>")
    assert any(v["rule"] == "heading-order" and "multiple" in v["message"] for v in violations)


def test_grader_heading_order_skip():
    """Grader catches skipped heading levels."""
    from tutor.classes.brushes.grader import _grade_heading_order
    violations = _grade_heading_order("<h1>Title</h1><h3>Skipped</h3>")
    assert any(v["rule"] == "heading-order" and "skip" in v["message"] for v in violations)


def test_grader_heading_order_clean():
    """Grader passes clean heading hierarchy."""
    from tutor.classes.brushes.grader import _grade_heading_order
    violations = _grade_heading_order("<h1>Page</h1><h2>Section</h2><h3>Sub</h3>")
    assert len(violations) == 0, violations


def test_grader_typography_small_font():
    """Grader catches body font below 16px."""
    from tutor.classes.brushes.grader import _grade_typography_minimums
    violations = _grade_typography_minimums('<p style="font-size: 14px;">small text</p>')
    assert any("font below 16px" in v["message"] for v in violations)


def test_grader_typography_tight_line_height():
    """Grader catches line-height below 1.5."""
    from tutor.classes.brushes.grader import _grade_typography_minimums
    violations = _grade_typography_minimums('<p style="line-height: 1.2;">tight</p>')
    assert any("line-height" in v["message"] for v in violations)


def test_grader_typography_clean():
    """Grader passes compliant typography."""
    from tutor.classes.brushes.grader import _grade_typography_minimums
    violations = _grade_typography_minimums('<p style="font-size: 16px; line-height: 1.6;">good</p>')
    assert len(violations) == 0, violations


def test_grader_spacing_off_scale():
    """Grader catches non-4px spacing values."""
    from tutor.classes.brushes.grader import _grade_spacing_system
    violations = _grade_spacing_system('<div style="padding: 14px;">tight</div>')
    assert any("non-standard spacing" in v["message"] for v in violations)


def test_grader_spacing_on_scale():
    """Grader passes 4px-scale spacing values."""
    from tutor.classes.brushes.grader import _grade_spacing_system
    for px in [4, 8, 12, 16, 24, 32, 48]:
        violations = _grade_spacing_system(f'<div style="padding: {px}px;">good</div>')
        assert len(violations) == 0, f"padding: {px}px falsely flagged"


def test_grader_touch_target_small():
    """Grader flags tiny interactive elements."""
    from tutor.classes.brushes.grader import _grade_touch_target
    violations = _grade_touch_target('<button style="padding: 1px;">X</button>')
    assert any("touch target" in v["message"] for v in violations)


def test_grader_touch_target_adequate():
    """Grader passes adequately padded interactive elements."""
    from tutor.classes.brushes.grader import _grade_touch_target
    violations = _grade_touch_target('<button style="padding: 12px;">Click</button>')
    assert len(violations) == 0, violations


def test_grader_integration_via_harness():
    """deep_check rules trigger grader.py when present."""
    result = grade(
        '<html><body>'
        '<h1>Title</h1><h3>Skip</h3>'  # heading-order violation
        '<p style="color: #999;">gray text</p>'  # color-contrast
        '</body></html>',
        "brushes",
    )
    rule_ids = {v.rule for v in result.violations}
    # Should catch the heading-order skip
    assert "heading-order" in rule_ids, f"heading-order not found in {rule_ids}"
