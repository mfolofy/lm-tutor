"""Tests for web-animation class."""
import pytest
from tutor.eval import grade, harness

def _r(s): return {v.rule for v in grade(s, "web-animation").violations}

# js-scroll-animation check_regex still active
SCROLL_CASES = [
    ("js-scroll-animation",
     "window.addEventListener('scroll', () => { box.style.opacity = scrollY / 1000; });",
     "@keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }"),
]
@pytest.mark.parametrize("rid,fail,p", SCROLL_CASES)
def test_scroll_fail(rid, fail, p): assert rid in _r(fail)
@pytest.mark.parametrize("rid,fail,p", SCROLL_CASES)
def test_scroll_pass(rid, fail, p): assert rid not in _r(p)

# animation-duration-too-long check_regex still active
DUR_CASES = [
    ("animation-duration-too-long",
     ".modal { animation-duration: 2s; }",
     ".modal { animation-duration: 0.2s; }"),
]
@pytest.mark.parametrize("rid,fail,p", DUR_CASES)
def test_dur_fail(rid, fail, p): assert rid in _r(fail)
@pytest.mark.parametrize("rid,fail,p", DUR_CASES)
def test_dur_pass(rid, fail, p): assert rid not in _r(p)

ALL_RULES = ["js-scroll-animation","no-prefers-reduced-motion","layout-thrashing-animation",
             "no-will-change","no-compositor-only","giant-gsap-bundle","no-lottie-alt",
             "animation-duration-too-long","no-exit-animation","infinite-animation-no-pause",
             "no-stagger-delay","opacity-zero-hidden"]
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("web-animation")["rules"]}
    for rid in ALL_RULES: assert rid in ids, f"{rid} missing"
def test_examples():
    for rule in harness.load_syllabus("web-animation")["rules"]:
        assert any(k.startswith("framework_") for k in rule), f"{rule['id']} missing examples"
def test_count():
    s = harness.load_syllabus("web-animation")
    assert s["class"]["rule_count"] == len(s["rules"])
