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

    # greenery.Fsm -> interegular.FSM with a COMPACT alphabet (so Outlines'
    # byte-level index is tractable). This compaction rides all "bulk" chars on
    # anything_else, which is LOSSY for a constraint that must distinguish two
    # large Unicode classes routing differently (e.g. word vs non-word for a
    # \b / \w-lookbehind rule — \w has ~130k members that cannot collapse).
    ifsm = _greenery_to_interegular(constraint, interegular)
    _assert_translation_faithful(constraint, ifsm, cert)
    return ifsm


def _assert_translation_faithful(gconstraint, ifsm, cert, samples: int = 4000, seed: int = 5) -> None:
    """Fuzz the interegular translation against the greenery constraint DFA;
    raise if the compact-alphabet translation is LOSSY for this rule (rather
    than let Layer B silently demonstrate a WRONG constraint). tabindex-style
    rules pass; \\b/\\w rules over the full Unicode alphabet do not."""
    import random

    rng = random.Random(seed)
    pool = list(' \t\n\r=:;"\'(){}[].,-_/0123456789abcdefgtruABX') + ["é", "Ω", "中", "print", "tabindex"]
    # Explicit adversarial boundary cases: a Unicode word char immediately
    # adjacent to the pattern is exactly where a \b/\w rule's compact-alphabet
    # translation goes wrong (word vs non-word can't both ride anything_else).
    adversarial = [
        "éprint(", "Ωprint(", "中print(", "_print(", "9print(", ".print(", " print(", "print(",
        "single_operator=trueé", "single_operator=trueΩ", "single_operator=true中",
        "single_operator=true_", "single_operator=true9", "single_operator=true ",
        'tabindex="3"', 'tabindex="0"', "",
    ]
    diverged = []
    for s in adversarial:
        if gconstraint.accepts(s) != ifsm.accepts(s):
            diverged.append(s)
    for _ in range(samples):
        parts = [rng.choice(pool) for _ in range(rng.randint(0, 10))]
        s = "".join(parts)
        if gconstraint.accepts(s) != ifsm.accepts(s):
            diverged.append(s)
        if len(diverged) >= 5:
            break
    if diverged:
        raise ValueError(
            f"compact interegular translation is LOSSY for {cert.class_name}/{cert.rule_id} "
            f"(diverges from the certified greenery DFA on e.g. {diverged[:3]!r}). This rule's "
            "constraint distinguishes two large Unicode classes (word vs non-word) that cannot "
            "ride a single anything_else. Layer A still certifies it EXACT; only this Outlines "
            "demo path is limited. Use a rule whose distinguishing alphabet is small (e.g. "
            "brushes/positive-tabindex)."
        )


def _distinguished_chars(gfsm) -> set[str]:
    """The (small) set of characters that any edge charclass in ``gfsm``
    treats specially — i.e. the boundary chars. A negated ("everything but")
    class distinguishes exactly the chars it EXCLUDES; a *small* non-negated
    class distinguishes the chars it INCLUDES. A *large* non-negated class
    (e.g. the full-Σ span used for ``Σ*`` or a ``\\w`` range) is NOT
    enumerated — its bulk is carried by ``anything_else`` and only its
    boundaries (already contributed by the other classes it is partitioned
    against) matter. This keeps the interegular alphabet tiny instead of
    exploding to ~1.1M full-Unicode entries."""
    big = 512  # a class whose SMALLER side exceeds this rides anything_else
    sigma_size = 0x110000 - 0x800  # scalar values, surrogates excluded
    out: set[str] = set()
    for _s, trans in gfsm.map.items():
        for cc in trans:
            accepted = cc.num_chars()  # cheap: from ord_ranges, no expansion
            if accepted == 0:
                continue  # dead edge — contributes nothing to the language
            if cc.negated:
                excluded = sigma_size - accepted
                if excluded <= big:
                    out.update(cc.get_chars())        # few EXCLUDED chars
                elif accepted <= big:
                    out.update((~cc).get_chars())     # few ACCEPTED chars
                # else both halves large -> boundary carried by other classes
            elif accepted <= big:
                out.update(cc.get_chars())            # small positive class
            # else large positive class -> bulk via anything_else
    return out


def _generic_other_char(distinguished: set[str]) -> str:
    """A character NOT in ``distinguished`` — the representative for
    ``anything_else`` routing."""
    for cp in range(0x21, 0x110000):
        if 0xD800 <= cp <= 0xDFFF:
            continue
        ch = chr(cp)
        if ch not in distinguished:
            return ch
    raise RuntimeError("no generic 'other' character available")  # unreachable


def _greenery_to_interegular(gfsm, interegular):
    """Translate a greenery Fsm into an interegular.FSM preserving the exact
    accepted language, with a COMPACT alphabet.

    interegular's model: ``alphabet`` maps each concrete char (and the special
    ``anything_else`` symbol) to an INTEGER transition key (chars sharing a key
    are indistinguishable); ``map`` is {state:{key:state}}. We assign a key to
    ``anything_else`` and to each *distinguished* char only (see
    _distinguished_chars) — large positive classes ride ``anything_else`` — so
    the alphabet stays small enough for Outlines' byte-level index.
    """
    from interegular.fsm import FSM, Alphabet, anything_else

    states = list(gfsm.states)
    state_index = {s: i for i, s in enumerate(states)}

    distinguished = _distinguished_chars(gfsm)
    other = _generic_other_char(distinguished)

    symbol_to_key: dict = {anything_else: 0}
    for i, ch in enumerate(sorted(distinguished), start=1):
        symbol_to_key[ch] = i
    alphabet = Alphabet(symbol_to_key)

    imap: dict = {}
    for s, trans in gfsm.map.items():
        si = state_index[s]
        row: dict = {}
        for cc, nstate in trans.items():
            ni = state_index[nstate]
            # anything_else routes here iff this class accepts a generic "other"
            if cc.accepts(other):
                row[0] = ni
            # each distinguished char routes per its own membership
            for ch, key in symbol_to_key.items():
                if ch is anything_else:
                    continue
                if cc.accepts(ch):
                    row[key] = ni
        imap[si] = row

    return FSM(
        alphabet=alphabet,
        states=set(range(len(states))),
        initial=state_index[gfsm.initial],
        finals={state_index[s] for s in gfsm.finals},
        map=imap,
        __no_validation__=True,
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
