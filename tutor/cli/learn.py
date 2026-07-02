"""`tutor learn` — take a class.

Phase 0 renders the class.yaml into its token-efficient injection prefix (the
[RULE ...] landmarks the model attends to at generation time) and prints it,
plus the enrollment record so the caller knows the track and whether the
Booster is active. Progress is checkpointed to the crash-recovery state store.

When the Booster is active (remedial-track small models), the injection is
augmented with concrete FAIL/PASS examples from the class syllabus so the
model has both the rule and a worked example in context.

With ``--auto`` (Phase 3), the Booster tools run automatically: the model
receives the injection prefix plus foresight (edge cases to watch for) and
exemplars (few-shot examples) in a single output — no manual tool chaining.
"""

import json
import sys

from tutor.eval.harness import load_syllabus


def _render_injection(cls: dict, booster: bool = False) -> str:
    """Render the token-efficient injection prefix.

    Without Booster: just the [RULE ...] landmarks (~120 tokens for brushes).
    With Booster: RULE landmarks + FAIL/PASS framework examples per rule.
    """
    meta = cls.get("class", {})
    lines = [f"# {meta.get('title', meta.get('id', 'class'))}", "Apply these rules:"]
    rules = cls.get("rules", []) or []

    for rule in rules:
        lines.append(f"  [RULE {rule.get('id', '?')}] {rule.get('rule', '')}")
        if booster:
            html_ex = rule.get("framework_html", "")
            if html_ex:
                lines.append(f"    \\-- {html_ex.strip()}")

    return "\n".join(lines)


_FAIL_MARK = "<!-- FAIL -->"
_PASS_MARK = "<!-- PASS -->"


def _syllabus_examples(cls: dict, limit: int = 3) -> list[dict]:
    """Extract FAIL/PASS example pairs from the class rules' framework blocks."""
    examples: list[dict] = []
    for rule in cls.get("rules", []) or []:
        block = rule.get("framework_html") or ""
        if _FAIL_MARK in block and _PASS_MARK in block:
            fail_part, _, pass_part = block.partition(_PASS_MARK)
            fail = fail_part.replace(_FAIL_MARK, "").strip()
            good = pass_part.strip()
            if fail and good:
                examples.append({"fail": fail, "pass": good})
        if len(examples) >= limit:
            break
    return examples


def _run_auto_booster(class_name: str, cls: dict) -> str:
    """Run Booster tools automatically for a remedial model.

    Returns a structured "booster pack" string with:
      - Foresight: edge cases the model should watch for
      - Exemplars: few-shot prompt block built from the class's FAIL/PASS
        examples (omitted when the class has none — an empty exemplar block
        would be injection theater)
    """
    from tutor.booster.tools import (
        downstream_lookahead,
        inject_few_shot,
    )

    meta = cls.get("class", {})
    cls_title = meta.get("title", meta.get("id", class_name))
    task_desc = f"Generate content compliant with {cls_title} rules"

    parts = []

    # Downstream lookahead: what edge cases does this class target?
    foresight = downstream_lookahead(task_desc, context=class_name)
    if foresight and isinstance(foresight, dict) and "edge_cases_to_handle" in foresight:
        parts.append("# Booster: Edge Cases to Watch For")
        for i, ec in enumerate(foresight["edge_cases_to_handle"], 1):
            parts.append(f"  {i}. {ec}")

    # Few-shot exemplars from the class syllabus (only when it has some).
    examples = _syllabus_examples(cls)
    if examples:
        exemplars = inject_few_shot(task_desc, examples=examples)
        if exemplars and isinstance(exemplars, dict) and "few_shot_prompt" in exemplars:
            parts.append("\n# Booster: Few-Shot Examples")
            parts.append(exemplars["few_shot_prompt"])

    return "\n".join(parts)


def run(args) -> int:
    from tutor.registrar.enroll import enroll
    from tutor.registrar.state import TrackStateStore

    record = enroll(args.model)
    class_name = getattr(args, "class_name", None)
    auto_mode = getattr(args, "auto", False)

    if class_name is None:
        print(f"Track for {record['model_id']}: {record['track']}", file=sys.stderr)
        print("Specify a class with --class <name>. See `tutor list`.", file=sys.stderr)
        return 1

    try:
        cls = load_syllabus(class_name)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    booster_active = record.get("booster", False)

    # Checkpoint progress (crash recovery).
    store = TrackStateStore()
    store.save(record["model_id"], {
        "track": record["track"],
        "current_class": class_name,
        "booster": booster_active,
    })

    # Print enrollment info to stderr.
    print(record, file=sys.stderr)

    # Print the injection prefix (always on stdout for piping).
    print(_render_injection(cls, booster=booster_active))

    # Phase 3: auto-Booster for remedial models.
    if booster_active and auto_mode:
        print("\n" + _run_auto_booster(class_name, cls))
        print(
            "\n# [BOOSTER] Auto-mode complete. "
            "Rules + foresight + exemplars injected above.",
            file=sys.stderr,
        )
    elif booster_active and not auto_mode:
        print(
            "\n[BOOSTER] Sandbox tools available: `tutor booster scratchpad` "
            "(reason before code), `tutor booster verify` (check assumptions), "
            "`tutor booster exemplars` (few-shot examples), "
            "`tutor booster foresee` (edge-case prediction). "
            "Use `--auto` to run them automatically.",
            file=sys.stderr,
        )

    return 0
