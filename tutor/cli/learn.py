"""`tutor learn` — take a class.

Phase 0 renders the class.yaml into its token-efficient injection prefix (the
[RULE ...] landmarks the model attends to at generation time) and prints it,
plus the enrollment record so the caller knows the track and whether the
Booster is active. Progress is checkpointed to the crash-recovery state store.

Full generate -> validate -> repair loops land in Phase 2 (Grading Board).
"""

import sys

from tutor.eval.harness import load_syllabus


def _render_injection(cls: dict) -> str:
    meta = cls.get("class", {})
    lines = [f"# {meta.get('title', meta.get('id', 'class'))}", "Apply these rules:"]
    for rule in cls.get("rules", []) or []:
        lines.append(f"  [RULE {rule.get('id', '?')}] {rule.get('rule', '')}")
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

    # Checkpoint progress (crash recovery).
    store = TrackStateStore()
    store.save(record["model_id"], {
        "track": record["track"],
        "current_class": class_name,
        "booster": record["booster"],
    })

    print(_render_injection(cls))
    return 0
