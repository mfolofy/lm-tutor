"""Tests for web-vitals class."""
import pytest
from tutor.eval import harness

ALL_RULES = ["no-lcp-priority","no-image-dimensions","no-font-display","render-blocking-scripts",
             "no-preconnect","long-task-over-50ms","no-srcset","no-bfcache-test",
             "no-speculation-rules","no-lazy-below-fold","no-inp-measurement","hydration-blocking-tti"]
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("web-vitals")["rules"]}
    for rid in ALL_RULES: assert rid in ids, f"{rid} missing"
def test_examples():
    for rule in harness.load_syllabus("web-vitals")["rules"]:
        assert any(k.startswith("framework_") for k in rule), f"{rule['id']} missing examples"
def test_count():
    s = harness.load_syllabus("web-vitals")
    assert s["class"]["rule_count"] == len(s["rules"])
