"""Tests for svelte-5 class."""
import pytest
from tutor.eval import harness
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("svelte-5")["rules"]}
    for rid in ["no-runes-legacy-store","no-effect-cleanup","no-let-reactivity"]:
        assert rid in ids, f"{rid} missing"
def test_count(): s = harness.load_syllabus("svelte-5"); assert s["class"]["rule_count"] == len(s["rules"])
