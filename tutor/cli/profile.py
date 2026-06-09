"""``tutor profile --model <id>`` — eval history and pass rates.

Reads the per-model eval history from ``~/.tutor/evals/<model_id>.jsonl``
and prints a summary: total evals, per-class pass rates, weakest rules,
and a next-class suggestion based on actual performance.

Requires at least one ``tutor eval --model <id>`` run to have data.
"""

import json
import sys

from tutor.registrar.evals import EvalHistory
from tutor.cli.curriculum import _TRACK_CURRICULUM
from tutor.registrar.enroll import enroll


def run(args) -> int:
    model_id = args.model
    history = EvalHistory()
    records = history.load(model_id)
    total = len(records)

    if total == 0:
        print(f"No eval history for {model_id}.")
        print("Run `tutor eval --model <id> < submission` first.")
        return 1

    rates = history.per_class_pass_rates(model_id)
    weakest = history.weakest_rules(model_id, top_n=5)
    enrollment = enroll(model_id)

    if args.json:
        print(json.dumps({
            "model_id": model_id,
            "total_evals": total,
            "per_class": rates,
            "weakest_rules": weakest,
            "track": enrollment.get("track", "remedial"),
        }, indent=2))
        return 0

    # Text output
    print(f"Model:             {model_id}")
    print(f"Track:             {enrollment.get('track', 'remedial')}")
    print(f"Total evaluations: {total}")
    print()

    # Per-class pass rates
    print("Per-class pass rates:")
    if rates:
        for cls_name, data in sorted(rates.items()):
            pct = round(data["pass_rate"] * 100, 1)
            icon = "✅" if data["pass_rate"] >= 0.8 else "⚠️" if data["pass_rate"] >= 0.5 else "❌"
            print(f"  {icon} {cls_name:20s} — {data['passes']}/{data['attempts']} ({pct}%)")
    else:
        print("  (no class-specific data yet)")

    print()

    # Weakest rules
    if weakest:
        print("Weakest rules (most-failed):")
        for w in weakest:
            print(f"  • {w['rule']:30s} — failed {w['failures']}x")
        print()

    # Next-class suggestion
    track = enrollment.get("track", "remedial")
    curriculum = _TRACK_CURRICULUM.get(track, _TRACK_CURRICULUM["remedial"])
    print("Suggested next steps:")
    for cid, title in curriculum:
        cls_rates = rates.get(cid)
        if cls_rates is None:
            print(f"  ▶  tutor learn --model {model_id} --class {cid}  — {title} (not yet attempted)")
        elif cls_rates["pass_rate"] < 0.5:
            print(f"  ⚠️  tutor learn --model {model_id} --class {cid}  — {title} (retake recommended: {cls_rates['passes']}/{cls_rates['attempts']} passed)")
        elif cls_rates["pass_rate"] >= 0.8:
            print(f"  ✅ {cid:20s} — already passing ({cls_rates['passes']}/{cls_rates['attempts']})")
    print()
    print("Run `tutor learn --model <id> --class <name>` to take a class.")

    return 0
