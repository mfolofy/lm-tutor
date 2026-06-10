"""Eval harness — the authoritative scoring function.

Phase 0 ships **Layer 1 only**: a deterministic rules engine that runs on the
core dependency set (stdlib + pydantic). Layer 2 (LLM judge) and Layer 3
(adversarial verification) are Phase 1.

Public API:

    from tutor.eval import grade
    result = grade(submission_text, syllabus="brushes")   # -> EvalResult
"""

from tutor.eval.harness import EvalResult, Violation, grade, MultiEvalResult, grade_multi

__all__ = ["grade", "grade_multi", "EvalResult", "Violation", "MultiEvalResult"]
