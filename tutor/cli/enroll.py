"""`tutor enroll` — identify a model, print its curriculum track."""

import json


def run(args) -> int:
    from tutor.registrar.enroll import enroll

    record = enroll(args.model)

    if getattr(args, "json", False):
        print(json.dumps(record, indent=2))
        return 0

    status = "registered" if record["registered"] else "UNREGISTERED (defaulting to remedial)"
    booster = "ON" if record["booster"] else "off"
    print(f"Model:   {record['model_id']}")
    if record["canonical_id"] and record["canonical_id"] != record["model_id"]:
        print(f"Resolved: {record['canonical_id']}")
    print(f"Status:  {status}")
    print(f"Tier:    {record['tier']}")
    print(f"Track:   {record['track']}")
    print(f"Booster: {booster}  (working-memory score {record['working_memory_score']})")
    return 0
