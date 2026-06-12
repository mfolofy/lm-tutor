"""Tests for view-transitions class."""
import pytest
from tutor.eval import harness

ALL_RULES = ["js-router-transition","no-view-transition-name","no-mpa-transition",
             "no-reduced-motion-check","no-fallback","old-new-pseudo-missing",
             "js-animation-library-page","scoped-transition-missed","wrong-transition-type",
             "no-view-transition-class","hardcoded-duration","no-types-config",
             "group-elements-missed","back-navigation-broken","no-error-handling"]
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("view-transitions")["rules"]}
    for rid in ALL_RULES: assert rid in ids, f"{rid} missing"
def test_examples():
    for rule in harness.load_syllabus("view-transitions")["rules"]:
        assert any(k.startswith("framework_") for k in rule), f"{rule['id']} missing examples"
def test_count():
    s = harness.load_syllabus("view-transitions")
    assert s["class"]["rule_count"] == len(s["rules"])
