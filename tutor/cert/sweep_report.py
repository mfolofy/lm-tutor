"""One-off reconciliation script: 253 vs 254 checkable-rule counts.

Run: python -m tutor.cert.sweep_report

Finding (measured, not asserted):
  * harness.grade()'s own ``rules_checked`` counter increments once per RULE
    that carries check_selector and/or check_regex (an OR, deduplicated).
    Summed across every class.yaml this is 253.
  * A naive count that sums "rules with check_regex" + "rules with
    check_selector" separately gets 254, because exactly one rule carries
    BOTH keys (css-modern / js-tooltip) and gets counted twice.
  * There is no bug in the harness — 253 is the correct, harness-consistent
    figure. 254 is an artifact of a different (double-counting) counting
    method applied to the same corpus.
"""

import glob

import yaml

CLASSES_GLOB = "tutor/classes/*/class.yaml"


def reconcile() -> dict:
    total_rules = 0
    checkable_dedup = 0
    n_regex = 0
    n_sel = 0
    both: list[tuple[str, str]] = []

    for f in sorted(glob.glob(CLASSES_GLOB)):
        doc = yaml.safe_load(open(f, encoding="utf-8"))
        for r in (doc.get("rules", []) or []):
            total_rules += 1
            has_sel = bool(r.get("check_selector"))
            has_re = bool(r.get("check_regex"))
            if has_sel or has_re:
                checkable_dedup += 1
            if has_re:
                n_regex += 1
            if has_sel:
                n_sel += 1
            if has_sel and has_re:
                both.append((f, r.get("id", "?")))

    return {
        "total_rules": total_rules,
        "checkable_dedup_253": checkable_dedup,
        "n_regex": n_regex,
        "n_selector": n_sel,
        "naive_sum_254": n_regex + n_sel,
        "double_counted_rules": both,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(reconcile(), indent=2))
