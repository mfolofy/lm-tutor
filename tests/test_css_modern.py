"""Tests for the css-modern class — validates syllabus structure."""
import pytest
from tutor.eval import harness

ALL_RULES = ["js-tooltip","no-lazy-loading","focus-not-focus-visible","important-cascade-war",
             "div-modal","100vh-viewport-bug","hex-over-oklch","no-accent-color","no-color-scheme",
             "no-inert","popover-js-reimpl","long-headline-no-balance","physical-not-logical",
             "media-over-container","no-subgrid","px-font-size","no-fetchpriority-lcp",
             "js-scroll-animation","no-starting-style","flat-selectors-no-nesting",
             "no-cascade-layer","js-has-workaround"]

def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("css-modern")["rules"]}
    for rid in ALL_RULES: assert rid in ids, f"{rid} missing"
def test_examples():
    for rule in harness.load_syllabus("css-modern")["rules"]:
        assert any(k.startswith("framework_") for k in rule), f"{rule['id']} missing examples"
def test_count():
    s = harness.load_syllabus("css-modern")
    assert s["class"]["rule_count"] == len(s["rules"])
