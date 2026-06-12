"""Tests for css-color class."""
import pytest
from tutor.eval import harness

ALL_RULES = ["hex-rgb-over-oklch","hsl-over-oklch","no-color-mix","no-oklch-default",
             "no-contrast-color","no-light-dark","hardcoded-dark-values","srgb-only-no-p3",
             "opacity-over-alpha","named-colors","no-relative-color","no-color-scheme-property"]
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("css-color")["rules"]}
    for rid in ALL_RULES: assert rid in ids, f"{rid} missing"
def test_examples():
    for rule in harness.load_syllabus("css-color")["rules"]:
        assert any(k.startswith("framework_") for k in rule), f"{rule['id']} missing examples"
def test_count():
    s = harness.load_syllabus("css-color")
    assert s["class"]["rule_count"] == len(s["rules"])
