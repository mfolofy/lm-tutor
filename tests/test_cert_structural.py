"""Layer A — the structural certificate is airtight, with NO model deps.

This suite re-verifies every committed certificate JSON from scratch against
the live class.yaml, using only core (stdlib + pydantic + pyyaml) plus
greenery/interegular. It does NOT trust the numbers baked into the JSON — it
rebuilds the constraint DFA from the rule's own check_regex via the recorded
recipe and re-runs A1 (emptiness), A2 (fidelity vs Python re) and A3
(grader-in-the-loop) itself.

Run: pytest tests/test_cert_structural.py
"""

import json
import re
from pathlib import Path

import greenery
import pytest

from tutor.cert.certificate import (
    Certificate,
    TARGET_RULES,
    _load_rule,
    _sample_constraint_strings,
    _source_hash,
    build_certificate,
)
from tutor.cert.rewrite import rewrite_to_forbidden_language
from tutor.eval.harness import grade

_CERTS_DIR = Path(__file__).parent.parent / "tutor" / "cert" / "certs"


def _cert_path(class_name: str, rule_id: str) -> Path:
    return _CERTS_DIR / f"{class_name}__{rule_id}.json"


@pytest.fixture(params=TARGET_RULES, ids=lambda t: f"{t[0]}/{t[1]}")
def target(request):
    return request.param


def test_certificate_file_exists_and_loads(target):
    class_name, rule_id = target
    path = _cert_path(class_name, rule_id)
    assert path.exists(), f"missing certificate {path}"
    cert = Certificate.model_validate_json(path.read_text())
    assert cert.rule_id == rule_id
    assert cert.class_name == class_name


def test_certificate_is_not_stale(target):
    class_name, rule_id = target
    cert = Certificate.model_validate_json(_cert_path(class_name, rule_id).read_text())
    rule = _load_rule(class_name, rule_id)
    assert cert.source_check.pattern == rule["check_regex"], "cert regex drifted from class.yaml"
    assert cert.source_hash == _source_hash(rule), "cert source_hash stale vs class.yaml"


def test_certificate_claims_exact(target):
    class_name, rule_id = target
    cert = Certificate.model_validate_json(_cert_path(class_name, rule_id).read_text())
    assert cert.equivalence == "EXACT", f"expected EXACT, got {cert.equivalence}"
    assert cert.proofs.emptiness.passed
    assert cert.proofs.fidelity.passed
    assert cert.proofs.fidelity.forbid_less_witnesses == []
    assert cert.proofs.grader_in_loop.passed
    assert cert.proofs.grader_in_loop.violations_of_certified_rule == 0


def _rebuild_fsms(class_name: str, rule_id: str):
    rule = _load_rule(class_name, rule_id)
    rx = rule["check_regex"]
    rw = rewrite_to_forbidden_language(rx)
    assert rw.ok, rw.reason
    forbidden = greenery.parse(rw.forbidden_pattern).to_fsm()
    constraint = forbidden.everythingbut().reduce()
    return rx, forbidden, constraint


def test_A1_emptiness_recomputed(target):
    # Rebuild independently: L(constraint) ∩ L(Σ*RΣ*) must be empty.
    class_name, rule_id = target
    _rx, forbidden, constraint = _rebuild_fsms(class_name, rule_id)
    assert (constraint & forbidden).empty()


def test_A2_fidelity_recomputed(target):
    # Independent 20k-sample differential fuzz (the committed cert used 10^5;
    # this is a fast re-check that still includes the adversarial cases).
    class_name, rule_id = target
    rx, forbidden, _constraint = _rebuild_fsms(class_name, rule_id)
    pyre = re.compile(rx)

    import random

    rng = random.Random(99)
    literal = sorted({c for c in rx if c.isprintable() and c != "\\"})
    pool = literal + list(" \t\n=:;\"'().-_/") + ["é", "Ω", "中", "_", "9", "a", "A", " "]
    forbid_less = []
    for _ in range(20_000):
        s = "".join(rng.choice(pool) for _ in range(rng.randint(0, 22)))
        if bool(pyre.search(s)) and not forbidden.accepts(s):
            forbid_less.append(s)
    # empty-string and explicit boundary cases
    for s in ["", "print(", "éprint(", "single_operator=true", "single_operator=trueé",
              'tabindex="3"', 'tabindex="0"']:
        if bool(pyre.search(s)) and not forbidden.accepts(s):
            forbid_less.append(s)
    assert forbid_less == [], f"FORBID-LESS divergences (false certificate!): {forbid_less[:5]}"


def test_A3_grader_in_the_loop_recomputed(target):
    # Independently walk the constraint FSM and confirm the REAL grader never
    # fires the certified rule on any accepting string.
    class_name, rule_id = target
    _rx, _forbidden, constraint = _rebuild_fsms(class_name, rule_id)
    walks = _sample_constraint_strings(constraint, 300, seed=7)
    fired = [s for s in walks if any(v.rule == rule_id for v in grade(s, class_name).violations)]
    assert fired == [], f"grader fired {rule_id} on {len(fired)} constraint-accepted strings"


def test_A2_detects_a_false_certificate():
    # Guard the guard: a deliberately-broken constraint that forbids LESS than
    # the grader MUST be caught by the forbid-less check. Here we use the
    # complement of a STRICT SUBSET language (only "tabindex=\"1\"") as a fake
    # constraint against the real, broader tabindex rule.
    rule = _load_rule("brushes", "positive-tabindex")
    rx = rule["check_regex"]
    pyre = re.compile(rx)
    # Fake forbidden language: matches ONLY the literal tabindex="1" (a strict
    # subset of what the real rule forbids) -> its complement wrongly ACCEPTS
    # tabindex="2".."9"+, which ARE real violations.
    from tutor.cert.rewrite import SIGMA_STAR

    fake_forbidden = greenery.parse(SIGMA_STAR + 'tabindex="1"' + SIGMA_STAR).to_fsm()
    witness = 'tabindex="7"'
    assert bool(pyre.search(witness))  # a real violation
    assert not fake_forbidden.accepts(witness)  # fake says "clean" -> forbid-less
    # i.e. our A2 forbid-less rule would flag this and force equivalence=NONE.


@pytest.mark.slow
def test_full_rebuild_matches_committed(target):
    # Heavier: fully rebuild the certificate (small fuzz) and confirm the
    # verdict matches the committed one. Marked slow (from_fsm render is ~30s+).
    class_name, rule_id = target
    committed = Certificate.model_validate_json(_cert_path(class_name, rule_id).read_text())
    rebuilt = build_certificate(class_name, rule_id, fuzz_n=5_000, walk_n=200)
    assert rebuilt.equivalence == committed.equivalence
