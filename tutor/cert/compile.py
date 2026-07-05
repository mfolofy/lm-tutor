"""Corpus sweep: attempt complement compilation of every check_regex rule in
tutor/classes/*/class.yaml.

Run: python -m tutor.cert.compile

Tiers (measured, not assumed):
  A (compiles) — rewrite.rewrite_to_forbidden_language() succeeds AND
    greenery can parse+build an FSM for the resulting forbidden-language
    regex. This is necessary but not sufficient for a certified EXACT
    equivalence — the emptiness/fidelity/grader-in-the-loop proofs in
    certificate.py are what actually certify a rule (see build order step 4).
    A rule landing in tier A here is "certifiable"; whether it ends up
    EXACT or gets rejected is decided by those proofs.
  NONE (does not compile) — either rewrite.py refuses (unsupported
    construct: mid-pattern \\b, lookahead, extra lookbehind, backreference,
    letter-in-class-under-(?i), etc.) or greenery's parser itself rejects
    the rewritten text (a construct rewrite.py's "supported syntax" claim
    doesn't actually cover, e.g. non-greedy quantifiers, anchors other than
    \\b, inline comments, `{m,}` open-ended bounds if greenery can't do
    them, etc.). The per-rule reason is recorded for both failure modes.

This script prints ONLY what was actually measured — do not hand-copy a
count from a plan or prior commit message without rerunning it.
"""

import glob
import json
import signal

import greenery
import yaml

_COMPILE_TIMEOUT_SECONDS = 5


class _CompileTimeout(Exception):
    pass


def _alarm_handler(signum, frame):  # noqa: ARG001
    raise _CompileTimeout()

from tutor.cert.rewrite import rewrite_to_forbidden_language

CLASSES_GLOB = "tutor/classes/*/class.yaml"


def collect_regex_rules() -> list[dict]:
    rules = []
    for f in sorted(glob.glob(CLASSES_GLOB)):
        cls_name = f.split("/")[-2]
        doc = yaml.safe_load(open(f, encoding="utf-8"))
        for r in doc.get("rules", []) or []:
            rx = r.get("check_regex")
            if rx:
                rules.append({"class": cls_name, "id": r.get("id", "?"), "check_regex": rx})
    return rules


def attempt_compile(check_regex: str) -> dict:
    rw = rewrite_to_forbidden_language(check_regex)
    if not rw.ok:
        return {"tier": "NONE", "reason": f"rewrite refused: {rw.reason}"}

    # Some rewritten patterns (e.g. those whose source uses a wildcard-heavy
    # proximity check like `.{0,60}`, multiplied further by (?i) case-fold
    # expansion) cause a genuine FSM state explosion in greenery's
    # determinization — not a hang, just computationally intractable in
    # practice. Bound it with a hard wall-clock timeout and record it as a
    # measured NONE rather than let the sweep stall indefinitely.
    old_handler = signal.signal(signal.SIGALRM, _alarm_handler)
    signal.alarm(_COMPILE_TIMEOUT_SECONDS)
    try:
        fsm = greenery.parse(rw.forbidden_pattern).to_fsm()
    except _CompileTimeout:
        return {
            "tier": "NONE",
            "reason": f"greenery FSM build exceeded {_COMPILE_TIMEOUT_SECONDS}s "
            "(likely state explosion — not attempted further)",
        }
    except Exception as exc:  # noqa: BLE001 — recording the failure, not swallowing it
        return {"tier": "NONE", "reason": f"greenery could not parse/build FSM: {exc}"}
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)

    return {
        "tier": "A",
        "reason": None,
        "forbidden_pattern_len": len(rw.forbidden_pattern),
        "fsm_states": len(fsm.states),
        "fsm_alphabet_size": len(fsm.alphabet),
    }


def sweep(verbose: bool = False) -> dict:
    import sys
    import time

    rules = collect_regex_rules()
    results = []
    for idx, r in enumerate(rules):
        if verbose:
            t0 = time.time()
            print(f"[{idx + 1}/{len(rules)}] {r['class']}/{r['id']} ...", file=sys.stderr, flush=True)
        outcome = attempt_compile(r["check_regex"])
        results.append({**r, **outcome})
        if verbose:
            print(f"    -> {outcome['tier']} ({time.time() - t0:.2f}s)", file=sys.stderr, flush=True)

    tier_a = [r for r in results if r["tier"] == "A"]
    tier_none = [r for r in results if r["tier"] == "NONE"]

    return {
        "total_regex_rules": len(rules),
        "tier_A_compiles": len(tier_a),
        "tier_NONE_count": len(tier_none),
        "tier_A_ids": [f"{r['class']}/{r['id']}" for r in tier_a],
        "tier_NONE_details": [
            {"rule": f"{r['class']}/{r['id']}", "reason": r["reason"]} for r in tier_none
        ],
    }


if __name__ == "__main__":
    import sys

    report = sweep(verbose="--verbose" in sys.argv)
    print(
        json.dumps(
            {
                "total_regex_rules": report["total_regex_rules"],
                "tier_A_compiles": report["tier_A_compiles"],
                "tier_NONE_count": report["tier_NONE_count"],
            },
            indent=2,
        )
    )
    print("\n--- tier A (compiles) ---")
    for rid in report["tier_A_ids"]:
        print(" ", rid)
    print("\n--- tier NONE (does not compile), with reasons ---")
    for d in report["tier_NONE_details"]:
        print(" ", d["rule"], "->", d["reason"])
