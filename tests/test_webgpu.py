"""Tests for webgpu class."""
import pytest
from tutor.eval import harness
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("webgpu")["rules"]}
    for rid in ["no-webgpu-detection","webgl-over-webgpu","no-compute-shader","no-error-scoping"]:
        assert rid in ids, f"{rid} missing"
def test_count(): s = harness.load_syllabus("webgpu"); assert s["class"]["rule_count"] == len(s["rules"])
