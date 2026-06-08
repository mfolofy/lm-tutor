"""`tutor learn` — take a class.

Phase 0 renders the class.yaml into its token-efficient injection prefix (the
[RULE ...] landmarks the model attends to at generation time) and prints it,
plus the enrollment record so the caller knows the track and whether the
Booster is active. Progress is checkpointed to the crash-recovery state store.

When the Booster is active (remedial-track small models), the injection is
augmented with concrete FAIL/PASS examples from the class syllabus so the
model has both the rule and a worked example in context.
"""

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


def run(args) -> int:
    from tutor.registrar.enroll import enroll
    from tutor.registrar.state import TrackStateStore

    record = enroll(args.model)
    class_name = getattr(args, "class_name", None)

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

    # Print enrollment info to stderr (doesn't pollute the injection output).
    print(record, file=sys.stderr)

    # Print the injection (this is what the model reads).
    print(_render_injection(cls, booster=booster_active))

    # If Booster is active, remind the model about available tools.
    if booster_active:
        print(
            "\n[BOOSTER] Sandbox tools available: `tutor booster scratchpad` "
            "(reason before code), `tutor booster verify` (check assumptions), "
            "`tutor booster exemplars` (few-shot examples), "
            "`tutor booster foresee` (edge-case prediction).",
            file=sys.stderr,
        )

    return 0
