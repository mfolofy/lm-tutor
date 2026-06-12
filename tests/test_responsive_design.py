"""Tests for responsive-design class."""
import pytest
from tutor.eval import grade, harness
def _r(s): return {v.rule for v in grade(s, "responsive-design").violations}

CASES = [
    ("100vh-mobile-bug", ".hero { min-height: 100vh; }", ".hero { min-height: 100dvh; }"),
    ("px-font-size", "body { font-size: 16px; }", "body { font-size: 1rem; }"),
]
@pytest.mark.parametrize("rid,fail,p", CASES)
def test_fail(rid, fail, p): assert rid in _r(fail)
@pytest.mark.parametrize("rid,fail,p", CASES)
def test_pass(rid, fail, p): assert rid not in _r(p)

TEACH = ["media-over-container","viewport-over-container-units","no-fluid-typography","no-min-max-clamp","picture-srcset-missing","hard-breakpoints-only","orientation-query-missing","content-based-layout"]
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("responsive-design")["rules"]}
    for rid in TEACH: assert rid in ids
def test_count(): s = harness.load_syllabus("responsive-design"); assert s["class"]["rule_count"] == len(s["rules"])
