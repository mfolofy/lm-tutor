"""Socratic debug — Hypothesis -> Proof -> Fix cycle (Phase 0 stub).

When a submission fails, the Grading Board doesn't just report violations; it
walks the student through a structured debugging cycle:

  1. Hypothesis — what rule is most likely violated, and why?
  2. Proof      — the concrete evidence (the matched fragment from the harness).
  3. Fix        — the minimal corrective change, drawn from the rule's PASS
                  example for the relevant framework.

Phase 0 ships the data structure and the cycle skeleton. The LLM-driven
hypothesis generation lands in Phase 2 alongside the Grading Board.
"""

from dataclasses import dataclass, field

from tutor.eval.harness import load_syllabus
from tutor.grading.evaluate import evaluate_submission


@dataclass
class DebugStep:
    hypothesis: str
    proof: str
    fix: str


@dataclass
class SocraticSession:
    syllabus: str
    steps: list[DebugStep] = field(default_factory=list)
    resolved: bool = False


def _pass_example(rule: dict) -> str:
    """Extract a PASS snippet from a rule's framework examples, if present."""
    for key in ("framework_html", "framework_react", "framework_vue", "framework_vanilla"):
        block = rule.get(key)
        if block:
            # The block pairs FAIL/PASS minimally; return it whole.
            return block.strip()
    return "See the rule's PASS example."


def run_cycle(submission: str, syllabus: str = "brushes") -> SocraticSession:
    """Run one Hypothesis -> Proof -> Fix pass over a failing submission."""
    verdict = evaluate_submission(submission, syllabus)
    session = SocraticSession(syllabus=syllabus, resolved=verdict["pass"])
    if verdict["pass"] or verdict["error"]:
        return session

    try:
        cls = load_syllabus(syllabus)
    except FileNotFoundError:
        cls = {"rules": []}
    rules_by_id = {r.get("id"): r for r in cls.get("rules", []) or []}

    for v in verdict["violations"]:
        rule = rules_by_id.get(v["rule"], {})
        session.steps.append(DebugStep(
            hypothesis=f"Rule {v['rule']} likely violated: {v['message']}",
            proof=v.get("matched") or "matched by check_selector/check_regex",
            fix=_pass_example(rule),
        ))
    return session
