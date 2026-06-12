"""Tests for build-tooling class."""
import pytest
from tutor.eval import grade, harness

def _r(s): return {v.rule for v in grade(s, "build-tooling").violations}

CASES = [
    ("tsc-for-linting", '"lint": "tsc --noEmit && eslint ."',
     '"lint": "biome lint ."'),
]

@pytest.mark.parametrize("rid,fail,p", CASES)
def test_fail(rid, fail, p): assert rid in _r(fail)
@pytest.mark.parametrize("rid,fail,p", CASES)
def test_pass(rid, fail, p): assert rid not in _r(p)

TEACH = ["eslint-legacy", "prettier-legacy", "postcss-over-lightning",
         "webpack-over-vite", "no-lint-autofix", "dual-eslint-biome",
         "all-lint-rules-on", "no-cache-in-ci", "js-tooling-default", "tsc-for-linting"]
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("build-tooling")["rules"]}
    for rid in TEACH: assert rid in ids
def test_count(): s = harness.load_syllabus("build-tooling"); assert s["class"]["rule_count"] == len(s["rules"])
