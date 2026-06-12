"""Tests for frontend-architecture class."""
import pytest
from tutor.eval import grade, harness

def _r(s): return {v.rule for v in grade(s, "frontend-architecture").violations}

# js-only-no-html and bundle-size-no-check have active check_regex
HTML_CASES = [
    ("js-only-no-html",
     '<body><div id="root"></div><script src="/bundle.js"></script></body>',
     '<body><header>...</header><main><article>...</article></main><script src="/app.js" type="module"></script></body>'),
]
BUNDLE_CASES = [
    ("bundle-size-no-check",
     "import { Chart } from 'chart.js';",
     "const Chart = await import('chart.js');"),
]
@pytest.mark.parametrize("rid,fail,p", HTML_CASES)
def test_html_fail(rid, fail, p): assert rid in _r(fail)
@pytest.mark.parametrize("rid,fail,p", HTML_CASES)
def test_html_pass(rid, fail, p): assert rid not in _r(p)
@pytest.mark.parametrize("rid,fail,p", BUNDLE_CASES)
def test_bundle_fail(rid, fail, p): assert rid in _r(fail)
@pytest.mark.parametrize("rid,fail,p", BUNDLE_CASES)
def test_bundle_pass(rid, fail, p): assert rid not in _r(p)

ALL_RULES = ["js-only-no-html","full-hydration-spa","no-signals-vdom","client-data-fetch-default",
             "no-streaming-ssr","mpa-spa-wrong-choice","no-progressive-enhancement",
             "no-islands-pattern","no-edge-rendering","bundle-size-no-check"]
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("frontend-architecture")["rules"]}
    for rid in ALL_RULES: assert rid in ids, f"{rid} missing"
def test_examples():
    for rule in harness.load_syllabus("frontend-architecture")["rules"]:
        assert any(k.startswith("framework_") for k in rule), f"{rule['id']} missing examples"
def test_count():
    s = harness.load_syllabus("frontend-architecture")
    assert s["class"]["rule_count"] == len(s["rules"])
