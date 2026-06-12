"""Tests for web-components class."""
import pytest
from tutor.eval import grade, harness

def _r(s): return {v.rule for v in grade(s, "web-components").violations}

TEACH = ["div-framework-component", "no-shadow-dom-encapsulation", "no-slots",
         "named-slots-missing", "no-css-parts", "no-form-participation",
         "no-declarative-shadow-dom", "catalyst-no-observe", "no-aria-in-shadow",
         "no-elem-internals", "custom-element-no-lifecycle", "inline-styles-global-leak"]
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("web-components")["rules"]}
    for rid in TEACH: assert rid in ids
def test_count(): s = harness.load_syllabus("web-components"); assert s["class"]["rule_count"] == len(s["rules"])
