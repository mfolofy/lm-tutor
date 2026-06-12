"""Tests for web-typography class."""
import pytest
from tutor.eval import harness

ALL_RULES = ["no-variable-fonts","no-font-display-swap","no-size-adjust","text-wrap-missing",
             "no-font-optical-sizing","system-fonts-only","no-line-height-unitless",
             "font-face-no-unicode-range","no-hyphens","letter-spacing-caps"]
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("web-typography")["rules"]}
    for rid in ALL_RULES: assert rid in ids, f"{rid} missing"
def test_examples():
    for rule in harness.load_syllabus("web-typography")["rules"]:
        assert any(k.startswith("framework_") for k in rule), f"{rule['id']} missing examples"
def test_count():
    s = harness.load_syllabus("web-typography")
    assert s["class"]["rule_count"] == len(s["rules"])
