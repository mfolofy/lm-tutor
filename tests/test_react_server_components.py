"""Tests for react-server-components class."""
import pytest
from tutor.eval import harness

ALL_RULES = ["use-client-placement","use-server-only","no-hooks-in-server","serializable-props",
             "client-boundary-colocation","async-server-fetch","no-use-effect-fetch","no-bare-fetch",
             "use-hook-unwrap","server-actions-mutations","route-vs-action","cache-revalidation",
             "suspense-streaming","file-conventions","metadata-api","image-optimization",
             "env-public-prefix","server-imports-client-wrong"]
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("react-server-components")["rules"]}
    for rid in ALL_RULES: assert rid in ids, f"{rid} missing"
def test_examples():
    for rule in harness.load_syllabus("react-server-components")["rules"]:
        assert any(k.startswith("framework_") for k in rule), f"{rule['id']} missing examples"
def test_count():
    s = harness.load_syllabus("react-server-components")
    assert s["class"]["rule_count"] == len(s["rules"])
