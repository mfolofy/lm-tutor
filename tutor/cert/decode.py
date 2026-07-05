"""Layer B — DEMONSTRATION that a real logits-controlled decoder, driven by a
certificate's constraint, cannot emit the certified violation.

This is NOT the certificate (Layer A is). It only shows the mechanism works
end to end on a real small model: same prompt, same seed, constrained vs
unconstrained, graded by the REAL harness.

Heavy deps (outlines, transformers, torch) are imported lazily so the core
test suite and Layer A never need them. Install with:  pip install -e '.[cert]'

The constraint fed to Outlines is built from the certificate's own recipe —
the greenery complement DFA — converted to an interegular FSM (Outlines'
native constraint form). We do NOT rely on the (possibly-null, possibly-huge)
rendered constraint_regex string; we rebuild the exact same DFA the proofs
used, directly from the rule's check_regex.
"""

from __future__ import annotations

from dataclasses import dataclass

import greenery

from tutor.cert.certificate import Certificate
from tutor.cert.rewrite import rewrite_to_forbidden_language


@dataclass
class DecodeOutcome:
    prompt: str
    constrained_text: str
    unconstrained_text: str
    constrained_violations: int
    unconstrained_violations: int


def build_constraint_interegular_fsm(cert: Certificate):
    """Rebuild the certified constraint DFA (¬(Σ*RΣ*)) and return it as an
    interegular FSM, ready for Outlines. Deterministic — matches the DFA the
    Layer-A proofs certified."""
    import interegular

    rw = rewrite_to_forbidden_language(cert.source_check.pattern)
    if not rw.ok:
        raise ValueError(f"cannot rebuild constraint: {rw.reason}")
    forbidden = greenery.parse(rw.forbidden_pattern).to_fsm()
    constraint = forbidden.everythingbut().reduce()

    # greenery.Fsm -> interegular.FSM. Both are explicit DFAs; we translate
    # the transition map, expanding greenery Charclasses into interegular's
    # symbol/partition model.
    return _greenery_to_interegular(constraint, interegular)


def _greenery_to_interegular(gfsm, interegular):
    """Translate a greenery Fsm into an interegular.FSM preserving the exact
    accepted language over the same alphabet."""
    # interegular represents transitions with a TransitionKey partition and an
    # anything_else symbol. We enumerate greenery's charclass edges directly.
    from interegular.fsm import FSM, anything_else

    # Assign each concrete char used on a non-negated edge its own symbol; all
    # negated ("everything else") edges share interegular's anything_else.
    states = list(gfsm.states)
    state_index = {s: i for i, s in enumerate(states)}

    alphabet_symbols: set = set()
    concrete_chars: set[str] = set()
    for _s, trans in gfsm.map.items():
        for cc in trans:
            if not cc.negated:
                concrete_chars.update(cc.get_chars())
    alphabet_symbols = set(concrete_chars) | {anything_else}

    # Build interegular alphabet mapping (symbol -> transition key).
    alphabet = interegular.fsm.Alphabet({sym: sym for sym in alphabet_symbols})

    imap: dict = {}
    for s, trans in gfsm.map.items():
        si = state_index[s]
        row: dict = {}
        for cc, nstate in trans.items():
            ni = state_index[nstate]
            if cc.negated:
                excluded = set(cc.get_chars())
                # anything_else plus every concrete char not excluded goes here
                row[anything_else] = ni
                for ch in concrete_chars:
                    if ch not in excluded:
                        row[ch] = ni
            else:
                for ch in cc.get_chars():
                    row[ch] = ni
        imap[si] = row

    return FSM(
        alphabet=alphabet,
        states=set(range(len(states))),
        initial=state_index[gfsm.initial],
        finals={state_index[s] for s in gfsm.finals},
        map=imap,
    )


def run_e2e(
    cert: Certificate,
    prompt: str,
    *,
    model_name: str = "Qwen/Qwen2.5-0.5B-Instruct",
    seed: int = 12345,
    max_new_tokens: int = 128,
) -> DecodeOutcome:
    """Generate constrained vs unconstrained on a real model and grade both.

    Returns violation counts of the CERTIFIED rule for each. The caller
    asserts constrained == 0 and unconstrained >= 1.
    """
    import outlines
    import torch  # noqa: F401 — imported for device/seed side effects
    from transformers import set_seed

    from tutor.eval.harness import grade

    set_seed(seed)
    model = outlines.models.transformers(model_name)

    constraint_fsm = build_constraint_interegular_fsm(cert)

    # Constrained generation via the certificate's DFA.
    constrained_gen = outlines.generate.fsm(model, constraint_fsm)
    set_seed(seed)
    constrained_text = constrained_gen(prompt, max_tokens=max_new_tokens)

    # Unconstrained baseline, same prompt/seed.
    free_gen = outlines.generate.text(model)
    set_seed(seed)
    unconstrained_text = free_gen(prompt, max_tokens=max_new_tokens)

    c_viol = sum(
        1 for v in grade(constrained_text, cert.class_name).violations if v.rule == cert.rule_id
    )
    u_viol = sum(
        1 for v in grade(unconstrained_text, cert.class_name).violations if v.rule == cert.rule_id
    )
    return DecodeOutcome(
        prompt=prompt,
        constrained_text=constrained_text,
        unconstrained_text=unconstrained_text,
        constrained_violations=c_viol,
        unconstrained_violations=u_viol,
    )
