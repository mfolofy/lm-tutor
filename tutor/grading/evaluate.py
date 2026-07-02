"""evaluate_submission — wire a submission to its class syllabus.

Reads the ``check_selector`` / ``check_regex`` fields from class.yaml (via the
Layer 1 harness) and returns a structured verdict: pass/fail, the violations,
and a per-severity breakdown. This is the seam the Grading Board (Phase 2) and
the LLM-judge layers (Phase 1) plug into.
"""

from tutor.eval import grade


def evaluate_submission(submission: str, syllabus: str = "brushes") -> dict:
    """Grade ``submission`` against ``syllabus`` and return a verdict dict.

    {
      "syllabus": "...",
      "pass": bool,
      "rules_checked": int,
      "violations": [...],
      "by_severity": {"fundamental": n, "advanced": m, ...},
      "error": str | None,
    }
    """
    result = grade(submission, syllabus)

    by_severity: dict[str, int] = {}
    for v in result.violations:
        by_severity[v.severity] = by_severity.get(v.severity, 0) + 1

    return {
        "syllabus": result.syllabus,
        "pass": result.passed,
        "rules_checked": result.rules_checked,
        "rules_total": result.rules_total,
        "violations": [v.model_dump() for v in result.violations],
        "by_severity": by_severity,
        "error": result.error,
    }
