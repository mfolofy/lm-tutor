"""Tests for three-js class."""
import pytest
from tutor.eval import grade, harness
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("three-js")["rules"]}
    for rid in ["no-r3f-for-react","no-webgpu-backend","no-instanced-mesh","no-glb-compression","no-frustum-culling","no-dispose-cleanup","no-a11y-3d","no-fallback-2d","no-responsive-canvas","no-lod"]:
        assert rid in ids, f"{rid} missing"
def test_count(): s = harness.load_syllabus("three-js"); assert s["class"]["rule_count"] == len(s["rules"])
