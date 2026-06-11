"""`tutor eval` — grade a submission read from stdin (Layer 1 rules engine).

The guarantee:  ``echo "<div>" | tutor eval``  returns a valid result with zero
additional arguments. The syllabus is inferred from the content when ``--class``
is not given. Result JSON goes to **stdout**; nothing else is printed there.

When ``--model`` is given, the result is also saved to the eval history
(``~/.tutor/evals/<model_id>.jsonl``) for later profiling.

Exit code is 0 on a successful grade regardless of pass/fail (violations found
= a successful grade, not an error). A non-zero exit means the grade itself
could not be performed.
"""

import json
import logging
import sys
from pathlib import Path

_CLASSES_DIR = Path(__file__).parent.parent / "classes"

_LANG_TO_CLASS: dict[str, str] = {
    "python": "python-best-practices",
    "javascript": "javascript-best-practices",
    "js": "javascript-best-practices",
    "typescript": "typescript-best-practices",
    "ts": "typescript-best-practices",
    "html": "brushes",
    "accessibility": "brushes",
    "a11y": "brushes",
    "security": "security",
    "test": "test",
    "perf": "perf",
    "code-review": "code-review",
}


def infer_syllabus(submission: str) -> str:
    """Heuristic syllabus inference. Never errors — always returns a class name.

    HTML-ish content -> brushes (the broadest default and the only Phase 0
    class). Python -> code-review, markdown -> prompt-design, JSON/YAML ->
    audit. If a guessed class is not installed in this build, fall back to
    brushes so the happy path always grades against a real syllabus.
    """
    content = submission.strip()
    lower = content.lower()

    guess = "brushes"
    if any(tag in lower for tag in (
        "<html", "<div", "<span", "<body", "<!doctype", "<head", "<table",
        "<form", "<input", "<button", "<nav", "<header", "<img", "<a ",
        "aria-", "role=", "class=", "style=",
    )):
        guess = "brushes"
    elif any(kw in content for kw in (
        "def ", "class ", "import ", "from ", "async def", "if __name__",
        "lambda ", "yield ",
    )):
        guess = "code-review"
    elif content.startswith("#") or content.startswith("---"):
        guess = "prompt-design"
    elif content.startswith("{") or content.startswith("["):
        guess = "audit"

    if not (_CLASSES_DIR / guess / "class.yaml").exists():
        guess = "brushes"
    return guess


def list_classes() -> list[dict]:
    """Return metadata for every installed class (used by `tutor list` + MCP)."""
    import yaml

    out: list[dict] = []
    if not _CLASSES_DIR.exists():
        return out
    for path in sorted(_CLASSES_DIR.glob("*/class.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        cls = data.get("class", {})
        out.append({
            "id": cls.get("id", path.parent.name),
            "title": cls.get("title", path.parent.name),
            "version": cls.get("version", "?"),
            "sources": cls.get("sources", []),
            "rules": len(data.get("rules", []) or []),
            "estimated_cost_tokens": cls.get("estimated_cost_tokens"),
        })
    return out


def _resolve_syllabuses(raw_classes: str, raw_lang: str) -> list[str]:
    seen: set[str] = set()
    resolved: list[str] = []
    for cid in [c.strip() for c in raw_classes.split(",") if c.strip()]:
        if cid not in seen:
            resolved.append(cid)
            seen.add(cid)
    for lang in [l.strip() for l in raw_lang.split(",") if l.strip()]:
        cid = _LANG_TO_CLASS.get(lang)
        if cid and cid not in seen:
            resolved.append(cid)
            seen.add(cid)
    return resolved


def run(args) -> int:
    from tutor.eval import grade, grade_multi
    from tutor.registrar.evals import EvalHistory

    submission = sys.stdin.read()

    raw_classes = getattr(args, "classes", "") or ""
    raw_lang = getattr(args, "lang", "") or ""
    syllabuses = _resolve_syllabuses(raw_classes, raw_lang)

    if syllabuses:
        multi = grade_multi(submission, syllabuses)
        payload = multi.model_dump()
        print(json.dumps(payload, indent=2, default=str))

        model_id = getattr(args, "model", None)
        if model_id:
            try:
                history = EvalHistory()
                history.record(model_id, {**payload, "syllabus": "+".join(syllabuses)})
            except Exception:
                logging.warning("eval: failed to record eval history: %s", sys.exc_info()[1])  # FIX: log instead of silent swallow

        return 0

    syllabus = getattr(args, "class_name", None) or infer_syllabus(submission)
    result = grade(submission, syllabus)

    payload = result.model_dump()
    if not getattr(args, "class_name", None):
        payload["syllabus"] = f"{result.syllabus} (auto-detected)"
    if result.error:
        payload["hint"] = result.hint or "Run with --class <name> to specify a syllabus."

    print(json.dumps(payload, indent=2, default=str))

    model_id = getattr(args, "model", None)
    if model_id and result.error is None:
        try:
            history = EvalHistory()
            history.record(model_id, payload)
        except Exception:
            logging.warning("eval: failed to record eval history: %s", sys.exc_info()[1])  # FIX: log instead of silent swallow

    return 0 if result.error is None else 2
