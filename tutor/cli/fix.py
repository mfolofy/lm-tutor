"""``tutor fix`` — eval -> fix -> re-eval correction loop.

Reads a submission from stdin, grades it, and if violations are found,
prints concrete fix suggestions (PASS examples from the class syllabus)
alongside each violation. The model can then fix the output and re-pipe.

With ``--auto``, the command loops: after printing fix suggestions it reads
the next submission from stdin and re-evals, continuing until the submission
passes or ``--max-iter`` rounds are exhausted. In auto mode each submission is
terminated by a line containing only ``---END---`` (or EOF) so a caller can
keep the pipe open between rounds — a plain ``read()`` to EOF would make a
second submission impossible.

Exit code is always 0 for a successful grade (pass or fail). Non-zero means
the grade itself failed (missing class, I/O error).
"""

import json
import sys
from pathlib import Path

from tutor.eval import grade
from tutor.cli.eval import infer_syllabus

_CLASSES_DIR = Path(__file__).parent.parent / "classes"


def _load_class(class_name: str) -> dict | None:
    """Load a class.yaml and return rules indexed by id."""
    import yaml

    path = _CLASSES_DIR / class_name / "class.yaml"
    if not path.exists():
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return None
    return data


def _build_fix_prompt(
    result: dict,
    class_data: dict | None,
) -> dict:
    """Build a fix-oriented response from eval results and class data.

    Returns a dict with:
      - verdict: the eval result
      - fix_suggestions: per-violation PASS examples from class.yaml
      - hint: instructions for the model to fix and re-submit
    """
    violations = result.get("violations", [])
    fix_suggestions: list[dict] = []

    if class_data:
        rules = {r.get("id"): r for r in (class_data.get("rules", []) or [])}

        for v in violations:
            rule_id = v.get("rule", "")
            rule = rules.get(rule_id)
            if not rule:
                fix_suggestions.append({
                    "rule": rule_id,
                    "suggestion": "No fix example available for this rule.",
                })
                continue

            suggestion: dict = {
                "rule": rule_id,
                "message": v.get("message", ""),
                "severity": v.get("severity", "fundamental"),
            }

            # Pick the most relevant framework example.
            for framework in ("html", "react", "vue", "vanilla"):
                ex = rule.get(f"framework_{framework}")
                if ex:
                    suggestion["fix_example"] = ex.strip()
                    suggestion["framework"] = framework
                    break

            if not suggestion.get("fix_example"):
                suggestion["fix_example"] = "Correct the violation per the rule."
                suggestion["framework"] = "general"

            fix_suggestions.append(suggestion)

    return {
        "verdict": {
            "syllabus": result.get("syllabus", "?"),
            "passed": result.get("passed", False),
            "rules_checked": result.get("rules_checked", 0),
            "violation_count": len(violations),
        },
        "violations": violations,
        "fix_suggestions": fix_suggestions,
        "hint": (
            "No violations found — well done."
            if result.get("passed")
            else "Fix each violation using the examples above, then re-pipe to `tutor fix`."
        ),
    }


def _run_fix_booster(submission: str, class_name: str | None) -> dict:
    """Run Booster tools to aid the fix loop for remedial models.

    Returns a dict with:
      - foresight: edge cases relevant to the class domain
      - scratchpad (optional): sandbox reasoning on the broken submission
    """
    from tutor.booster.tools import downstream_lookahead

    booster_output: dict = {}

    # Always run foresee on the class context — this is lightweight (static).
    foresee = downstream_lookahead(
        f"Fix {class_name or 'code'} violations",
        context=class_name or "",
    )
    if foresee:
        booster_output["foresight"] = foresee

    # Only run scratchpad if content looks like executable logic, not markup.
    # HTML/XML/markdown content would fail as Python code.
    stripped = submission.strip()
    if stripped and not stripped.startswith(("<", "#", "!")) and len(stripped) > 20:
        from tutor.booster.tools import write_to_scratchpad

        scratch = write_to_scratchpad(stripped)
        if scratch and isinstance(scratch, dict) and not scratch.get("error"):
            booster_output["scratchpad"] = scratch

    return booster_output


SUBMISSION_DELIMITER = "---END---"


def _read_submission() -> str:
    """Read one submission: lines until a '---END---' line or EOF.

    Unlike ``sys.stdin.read()`` this leaves the stream usable for the next
    round, so ``--auto`` can actually receive a resubmission over a pipe.
    """
    lines: list[str] = []
    for line in sys.stdin:
        if line.strip() == SUBMISSION_DELIMITER:
            break
        lines.append(line)
    return "".join(lines)


def run(args) -> int:
    class_name = getattr(args, "class_name", None)
    max_iter = getattr(args, "max_iter", 5)
    auto = getattr(args, "auto", False) and not getattr(args, "once", False)
    use_booster = getattr(args, "booster", False)

    submission = _read_submission() if auto else sys.stdin.read()

    # Phase 3: pre-run Booster for remedial-model fix context.
    booster_context = None
    if use_booster:
        booster_context = _run_fix_booster(submission, class_name)
        if booster_context:
            # Emit as a JSON comment on stderr so it doesn't pollute pipe output.
            import json as _json
            print(
                "fix:booster", _json.dumps(booster_context),
                file=sys.stderr,
            )

    for iteration in range(1, max_iter + 1):
        syllabus = class_name or infer_syllabus(submission)
        result_obj = grade(submission, syllabus)

        result = result_obj.model_dump()

        if result.get("error"):
            print(json.dumps({"error": result["error"], "hint": result.get("hint")}))
            return 2

        # Check if we should load class data for fix suggestions.
        class_data = None
        if not result.get("passed"):
            class_data = _load_class(result.get("syllabus", syllabus))

        response = _build_fix_prompt(result, class_data)
        response["iteration"] = iteration

        # Attach Booster context to first-iteration response.
        if iteration == 1 and booster_context:
            response["booster"] = booster_context

        # Always print the response.
        print(json.dumps(response, indent=2, default=str))

        if result.get("passed"):
            return 0

        if not auto or iteration >= max_iter:
            return 0

        # Auto mode: wait for the next submission on stdin.
        # Print a delimiter so the caller knows to send the next version.
        print("---FIX_AND_RESUBMIT---", flush=True)
        submission = _read_submission()
        if not submission.strip():
            print(json.dumps({"error": "Empty resubmission — stopping."}))
            return 1

    return 0
