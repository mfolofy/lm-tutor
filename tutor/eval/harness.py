"""Layer 1 rules engine — deterministic, stdlib-only grading.

This is the authoritative scoring function for Phase 0. It runs on the core
dependency set only (stdlib + pydantic) so that

    echo "<div>" | tutor eval

works immediately after ``pip install -e .`` with no class venv created.

Each class.yaml rule may carry:

  * ``check_selector`` — a comma-separated list of simple CSS selectors. A
    *match* (element satisfying any selector) is a VIOLATION. Selectors are
    deliberately minimal: ``tag``, ``tag[attr]``, ``tag[attr="val"]``,
    ``tag[attr=""]``, ``tag:not([attr])``, ``tag:empty``, ``[attr]``. This
    covers the WCAG checks we ship without a full CSS engine or bs4.
  * ``check_regex`` — a Python regex. Any match is a VIOLATION.

Deeper, library-dependent grading (pillow/bs4 colour-contrast, AST checks)
lives in a per-class ``grader.py`` invoked through the class venv — NOT on this
happy path.
"""

import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel

_CLASSES_DIR = Path(__file__).parent.parent / "classes"


class Violation(BaseModel):
    rule: str
    severity: str = "fundamental"
    message: str
    wcag: str | None = None
    matched: str | None = None  # the offending fragment, when available


class EvalResult(BaseModel):
    syllabus: str
    passed: bool
    rules_checked: int
    violations: list[Violation] = []
    hint: str | None = None
    error: str | None = None


class MultiEvalResult(BaseModel):
    results: list[EvalResult]     # one per class
    total_violations: int
    total_rules_checked: int
    all_passed: bool              # true only if every class passes


# ─────────────────────────── HTML element model ────────────────────────────

class _Element:
    __slots__ = ("tag", "attrs", "has_children", "text", "raw")

    def __init__(self, tag: str, attrs: dict[str, str | None]):
        self.tag = tag
        self.attrs = attrs
        self.has_children = False
        self.text = ""
        self.raw = ""


class _Collector(HTMLParser):
    """Collects a flat list of elements with their attributes and emptiness."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements: list[_Element] = []
        self._stack: list[_Element] = []

    def handle_starttag(self, tag, attrs):
        el = _Element(tag, {k: v for k, v in attrs})
        if self._stack:
            self._stack[-1].has_children = True
        self.elements.append(el)
        self._stack.append(el)

    def handle_startendtag(self, tag, attrs):
        el = _Element(tag, {k: v for k, v in attrs})
        if self._stack:
            self._stack[-1].has_children = True
        self.elements.append(el)

    def handle_endtag(self, tag):
        while self._stack:
            top = self._stack.pop()
            if top.tag == tag:
                break

    def handle_data(self, data):
        if self._stack and data.strip():
            self._stack[-1].text += data
            self._stack[-1].has_children = True


def _parse_html(submission: str) -> list[_Element]:
    import logging

    parser = _Collector()
    try:
        parser.feed(submission)
        parser.close()
    except Exception as exc:
        # Malformed markup is common and non-fatal — grade what parsed.
        logging.getLogger("tutor.eval").debug(
            "HTML parse error (grading partial content): %s", exc
        )
    return parser.elements


# ───────────────────────────── selector engine ─────────────────────────────

# A single simple selector: optional tag, optional [attr], [attr="v"],
# [attr=""], :not([attr]), :empty.
_SEL_RE = re.compile(
    r"""^
    (?P<tag>[a-zA-Z][\w-]*|\*)?
    (?P<conds>(?:\[[^\]]*\]|:not\(\[[^\]]*\]\)|:empty)*)
    $""",
    re.VERBOSE,
)
_COND_ATTR = re.compile(r"\[\s*([\w-]+)\s*(?:([~|^$*]?=)\s*[\"']([^\"']*)[\"'])?\s*\]")
_COND_NOT_ATTR = re.compile(r":not\(\[\s*([\w-]+)\s*\]\)")


def _element_matches(el: _Element, selector: str) -> bool:
    selector = selector.strip()
    m = _SEL_RE.match(selector)
    if not m:
        return False
    tag = m.group("tag")
    if tag and tag != "*" and el.tag != tag.lower():
        return False

    conds = m.group("conds") or ""

    # :empty — no element/text children.
    if ":empty" in conds:
        if el.has_children:
            return False

    # :not([attr]) — attribute must be ABSENT.
    for not_attr in _COND_NOT_ATTR.findall(conds):
        if not_attr.lower() in {k.lower() for k in el.attrs}:
            return False

    # [attr] / [attr="val"] / [attr=""] — attribute must be present (and equal).
    # Strip the :not(...) groups first so we don't double-count their attrs.
    conds_wo_not = _COND_NOT_ATTR.sub("", conds)
    for attr, op, val in _COND_ATTR.findall(conds_wo_not):
        attr_l = attr.lower()
        present = {k.lower(): v for k, v in el.attrs.items()}
        if attr_l not in present:
            return False
        if op:  # an equality test was specified
            actual = present[attr_l] if present[attr_l] is not None else ""
            if actual != val:
                return False
    return True


def _check_selector(selector_group: str, elements: list[_Element]) -> list[_Element]:
    """Return elements matching any selector in a comma-separated group."""
    hits: list[_Element] = []
    for selector in selector_group.split(","):
        selector = selector.strip()
        if not selector:
            continue
        for el in elements:
            if _element_matches(el, selector) and el not in hits:
                hits.append(el)
    return hits


def _render(el: _Element) -> str:
    attr_str = "".join(
        f' {k}="{v}"' if v is not None else f" {k}" for k, v in el.attrs.items()
    )
    return f"<{el.tag}{attr_str}>"


# ──────────────────────────── syllabus loading ─────────────────────────────

def load_syllabus(class_name: str) -> dict[str, Any]:
    """Load a class.yaml by class name. Raises FileNotFoundError if missing."""
    path = _CLASSES_DIR / class_name / "class.yaml"
    if not path.exists():
        raise FileNotFoundError(f"No class.yaml for class '{class_name}' at {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


# ──────────────────────────────── grading ──────────────────────────────────

def grade(submission: str, syllabus: str = "brushes") -> EvalResult:
    """Grade ``submission`` against the named class syllabus (Layer 1)."""
    try:
        cls = load_syllabus(syllabus)
    except FileNotFoundError as exc:
        return EvalResult(
            syllabus=syllabus, passed=False, rules_checked=0,
            error=str(exc),
            hint="Run `tutor list` to see available classes.",
        )

    rules = cls.get("rules", []) or []
    elements = _parse_html(submission)
    violations: list[Violation] = []

    for rule in rules:
        rule_id = rule.get("id", "?")
        severity = rule.get("severity", "fundamental")
        message = rule.get("rule", "")
        wcag = rule.get("wcag")

        selector = rule.get("check_selector")
        if selector:
            for el in _check_selector(selector, elements):
                violations.append(Violation(
                    rule=rule_id, severity=severity, message=message,
                    wcag=str(wcag) if wcag is not None else None,
                    matched=_render(el),
                ))

        regex = rule.get("check_regex")
        if regex:
            try:
                pattern = re.compile(regex)
            except re.error:
                continue
            for m in pattern.finditer(submission):
                violations.append(Violation(
                    rule=rule_id, severity=severity, message=message,
                    wcag=str(wcag) if wcag is not None else None,
                    matched=m.group(0)[:120],
                ))

    return EvalResult(
        syllabus=syllabus,
        passed=len(violations) == 0,
        rules_checked=len(rules),
        violations=violations,
        hint=None if violations else "No fundamental violations found by Layer 1.",
    )


def grade_multi(submission: str, syllabuses: list[str]) -> MultiEvalResult:
    results: list[EvalResult] = []
    total_violations = 0
    total_rules_checked = 0
    all_passed = True

    for syllabus in syllabuses:
        result = grade(submission, syllabus)
        results.append(result)
        if result.error is None:
            total_violations += len(result.violations)
            total_rules_checked += result.rules_checked
        if not result.passed:
            all_passed = False

    return MultiEvalResult(
        results=results,
        total_violations=total_violations,
        total_rules_checked=total_rules_checked,
        all_passed=all_passed,
    )
