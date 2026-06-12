"""Tests for html-apis class."""
import pytest
from tutor.eval import grade, harness
def _r(s): return {v.rule for v in grade(s, "html-apis").violations}

CASES = [
    ("div-popover-not-native", '<div class="popover" style="display:none">Content</div>', '<div popover id="help">Content</div>'),
    ("div-modal-not-dialog", '<div role="dialog" aria-modal="true">Modal</div>', '<dialog><form method="dialog">OK</form></dialog>'),
    ("no-lazy-loading-native", '<img src="footer.jpg">', '<img src="footer.jpg" loading="lazy" decoding="async">'),
]
@pytest.mark.parametrize("rid,fail,p", CASES)
def test_fail(rid, fail, p): assert rid in _r(fail)
@pytest.mark.parametrize("rid,fail,p", CASES)
def test_pass(rid, fail, p): assert rid not in _r(p)

TEACH = ["no-inert-attribute","custom-select-not-selectmenu","details-summary-missed","no-fetchpriority","no-inputmode","no-enterkeyhint","custom-toggle-missed"]
def test_teaching():
    ids = {r["id"] for r in harness.load_syllabus("html-apis")["rules"]}
    for rid in TEACH: assert rid in ids
def test_count(): s = harness.load_syllabus("html-apis"); assert s["class"]["rule_count"] == len(s["rules"])
