"""``tutor curriculum`` — output ordered class list for a model's track.

Phase 1 defines the class ordering from the SCOPE. Tracks:

  * **remedial** — fundamentals only: brushes → defense → security → test
  * **standard** — full curriculum: all 9 classes
  * **honors** — same as standard (can skip classes after diagnostic)
"""

import json
import sys

# Phase 1 class ordering from SCOPE.md lines 348-352.
# Remedial gets fundamentals; standard/honors get the full path.
_TRACK_CURRICULUM = {
    "remedial": [
        ("brushes", "UI/UX accessibility — WCAG 2.2"),
        ("defense", "Security defense — OWASP top 10"),
        ("security", "Secure coding — NIST SP 800-53"),
        ("test", "Test-driven development — best practices"),
    ],
    "standard": [
        ("brushes", "UI/UX accessibility — WCAG 2.2"),
        ("python-best-practices", "Python coding standards — PEP 8/484"),
        ("javascript-best-practices", "JavaScript coding standards — ES2026 / idiomatic JS"),
        ("typescript-best-practices", "TypeScript coding standards — strict types, generics, idiomatic TS"),
        ("api-design", "API design — REST/GraphQL/gRPC standards"),
        ("devops", "DevOps/SRE — DORA, SRE, CI/CD, IaC"),
        ("code-review", "Code review patterns — House audit standards"),
        ("prompt-design", "Prompt engineering — Prompt Brush methodology"),
        ("audit", "Audit & compliance — evidence requirements"),
        ("architect", "Architecture — system design patterns"),
        ("defense", "Security defense — OWASP top 10"),
        ("perf", "Performance — optimization patterns"),
        ("test", "Test-driven development — best practices"),
        ("security", "Secure coding — NIST SP 800-53"),
    ],
    "honors": [
        ("brushes", "UI/UX accessibility — WCAG 2.2"),
        ("python-best-practices", "Python coding standards — PEP 8/484"),
        ("javascript-best-practices", "JavaScript coding standards — ES2026 / idiomatic JS"),
        ("typescript-best-practices", "TypeScript coding standards — strict types, generics, idiomatic TS"),
        ("api-design", "API design — REST/GraphQL/gRPC standards"),
        ("devops", "DevOps/SRE — DORA, SRE, CI/CD, IaC"),
        ("code-review", "Code review patterns — House audit standards"),
        ("prompt-design", "Prompt engineering — Prompt Brush methodology"),
        ("audit", "Audit & compliance — evidence requirements"),
        ("architect", "Architecture — system design patterns"),
        ("defense", "Security defense — OWASP top 10"),
        ("perf", "Performance — optimization patterns"),
        ("test", "Test-driven development — best practices"),
        ("security", "Secure coding — NIST SP 800-53"),
    ],
}


def run(args) -> int:
    from tutor.registrar.enroll import enroll

    model_id = args.model
    record = enroll(model_id)
    track = record["track"]
    curriculum = _TRACK_CURRICULUM.get(track, _TRACK_CURRICULUM["remedial"])

    output = {
        "model_id": model_id,
        "canonical_id": record.get("canonical_id"),
        "track": track,
        "booster": record.get("booster", False),
        "classes": [
            {"id": cid, "title": title, "order": i + 1}
            for i, (cid, title) in enumerate(curriculum)
        ],
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"Model:       {model_id}")
        print(f"Track:       {track}")
        print(f"Booster:     {'ACTIVE' if record.get('booster') else 'off'}")
        print()
        print("Curriculum:")
        for i, (cid, title) in enumerate(curriculum, 1):
            print(f"  {i}. {cid:20s} — {title}")
        print()
        print(f"Next class:  `tutor learn --model {model_id} --class {curriculum[0][0]}`")

    return 0
