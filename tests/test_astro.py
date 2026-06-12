"""Tests for astro class."""
import pytest
from tutor.eval import grade, harness
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("astro")["rules"]}
    for rid in ["no-client-directives","all-js-by-default","no-content-collections","no-view-transitions-astro","no-image-optimization-astro","framework-island-overload","no-hybrid-rendering","no-island-interactivity","static-paths-only","no-middleware-edge"]:
        assert rid in ids, f"{rid} missing"
def test_count(): s = harness.load_syllabus("astro"); assert s["class"]["rule_count"] == len(s["rules"])
