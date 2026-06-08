"""Tests for the brushes class — proves each rule's FAIL/PASS behaviour.

This is the template every new class follows (see CONTRIBUTING.md): for each
rule, a FAIL snippet must produce that rule's violation and a PASS snippet must
not. Run with: pytest tests/
"""

import pytest

from tutor.eval import grade
from tutor.eval.harness import load_syllabus


def _rules_for(submission: str) -> set[str]:
    result = grade(submission, "brushes")
    return {v.rule for v in result.violations}


# (rule_id, FAIL snippet, PASS snippet)
CASES = [
    ("img-alt", '<img src="a.png">', '<img src="a.png" alt="A logo">'),
    ("img-alt", '<img src="d.png">', '<img src="d.png" alt="">'),  # decorative PASS
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


@pytest.mark.parametrize("rule_id,fail,passing", CASES)
def test_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CASES)
def test_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


def test_syllabus_loads_and_has_rules():
    cls = load_syllabus("brushes")
    assert cls["class"]["id"] == "brushes"
    assert len(cls["rules"]) >= 10


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
