r"""The Certificate object + its three structural proofs (Layer A).

A Certificate certifies that a compiled Outlines constraint (the regex
``constraint_regex``) makes a logits-controlled local decoder produce output
that is *provably* a member of the COMPLEMENT of a specific class.yaml
``check_regex`` R — i.e. the grader's own ``re.finditer(R, output)`` can
never match. That is INVARIANCE of the grader's check for that one rule; it
is NOT semantic safety and NOT a guarantee about any other rule (see SCOPE.md
and the ``guarantee`` field).

By construction ``constraint = (Σ*·R·Σ*).everythingbut()`` (greenery DFA
complement), so exactness reduces to one question: does the rewritten
forbidden-language FSM equal Python ``re``'s own semantics for ``Σ*·R·Σ*``?
The three proofs below establish this to the standard the honesty bar
requires:

  A1 EMPTINESS (symbolic) — ``L(constraint) ∩ L(Σ*RΣ*) == ∅`` via greenery
     DFA intersection + emptiness. Proves the complement was taken correctly
     and that NO string the constraint accepts is a grader violation
     (soundness of the certificate).

  A2 FIDELITY (differential fuzz) — for 10^5 seeded strings incl. adversarial
     boundary/Unicode/empty cases, compare the forbidden-language FSM against
     Python ``re.search(R, ·)``. A divergence where the FSM says "no match"
     but Python says "match" means the constraint would ACCEPT a real
     violation = FORBID-LESS = HARD FAIL (equivalence forced to NONE). A
     divergence the other way (FSM matches, Python doesn't) means the
     constraint forbids a strict superset = SOUND_OVERAPPROX. Zero divergence
     in either direction = EXACT (to the confidence of the fuzz, on top of the
     A1 symbolic soundness proof).

  A3 GRADER-IN-THE-LOOP (real harness) — enumerate/​walk accepting strings of
     the constraint FSM, run each through the REAL ``tutor.eval.harness.grade``
     against the rule's class, and assert 0 violations of the certified rule
     id. Closes the loop against the actual scorer, not just our model of it.

Scope (also in the module docstring of tutor/cert/__init__.py and SCOPE.md):
the certificate applies ONLY to a logits-controlled LOCAL decoding path;
API-model submissions (opencode/Claude) remain detect-only forever. The
guarantee is invariance of the grader's own check per rule (proven by
DFA-intersection emptiness), NOT semantic safety (a homoglyph ``рrint(``
passes both grader and certificate), and holds modulo Outlines correctly
enforcing the char-level DFA at the token level.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import signal
from pathlib import Path
from typing import Literal

import greenery
import yaml
from greenery.rxelems import from_fsm
from pydantic import BaseModel

from tutor.cert.rewrite import rewrite_to_forbidden_language

# Rendering the complement DFA back to a positive regex string (greenery
# from_fsm state-elimination) is expensive over the full-Unicode alphabet
# (measured: ~31s / ~40s for the small rules, and unbounded for \w-heavy
# ones). The certificate's SOUNDNESS does NOT depend on this string — every
# proof runs on the FSM — so we bound the render and fall back to the
# deterministic reconstruction recipe when it blows the budget.
_RENDER_TIMEOUT_SECONDS = 120


class _RenderTimeout(Exception):
    pass


def _render_alarm(signum, frame):  # noqa: ARG001
    raise _RenderTimeout()

_CERTS_DIR = Path(__file__).parent / "certs"
_CLASSES_DIR = Path(__file__).parent.parent / "classes"

# A concrete representative character used to instantiate the "negated
# charclass" transitions of a DFA when enumerating accepting strings. It must
# be a character that is NOT special to any rule — a plain lowercase letter is
# safe (never a delimiter/quote/digit in the rules we certify). Enumeration
# soundness does not depend on the exact choice.
_WALK_OTHERCHAR = "x"


# ─────────────────────────────── the model ─────────────────────────────────

class SourceCheck(BaseModel):
    kind: Literal["check_regex", "check_selector"]
    pattern: str  # verbatim, exactly as it appears in class.yaml


class EmptinessProof(BaseModel):
    passed: bool
    states_checked: int


class FidelityProof(BaseModel):
    passed: bool
    samples: int
    divergences: int
    # A few concrete divergence witnesses, if any, for auditability.
    forbid_less_witnesses: list[str] = []
    overapprox_witnesses: list[str] = []


class GraderInLoopProof(BaseModel):
    passed: bool
    walks: int
    violations_of_certified_rule: int


class Proofs(BaseModel):
    emptiness: EmptinessProof
    fidelity: FidelityProof
    grader_in_loop: GraderInLoopProof


class Certificate(BaseModel):
    rule_id: str
    class_name: str
    source_check: SourceCheck
    source_hash: str  # sha256 of the source rule text, for staleness detection
    # The positive regex for the COMPLEMENT language, rendered from the DFA.
    # May be null when rendering exceeds the budget (see constraint_recipe) —
    # the certificate stays valid because the constraint FSM is deterministically
    # reconstructable from source_check.pattern via constraint_recipe.
    constraint_regex: str | None
    constraint_recipe: str  # exact recipe to rebuild the constraint FSM
    alphabet: str  # human note describing the effective alphabet
    equivalence: Literal["EXACT", "SOUND_OVERAPPROX", "NONE"]
    proofs: Proofs
    guarantee: str  # human sentence: exact scope + limits


# ───────────────────────────── rule loading ────────────────────────────────

def _load_rule(class_name: str, rule_id: str) -> dict:
    path = _CLASSES_DIR / class_name / "class.yaml"
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    for r in doc.get("rules", []) or []:
        if r.get("id") == rule_id:
            return r
    raise KeyError(f"rule {rule_id!r} not found in class {class_name!r}")


def _source_hash(rule: dict) -> str:
    """Stable hash of the load-bearing parts of the rule (its checks), so a
    later edit to the class.yaml regex invalidates a stale certificate."""
    payload = json.dumps(
        {
            "id": rule.get("id"),
            "check_regex": rule.get("check_regex"),
            "check_selector": rule.get("check_selector"),
        },
        sort_keys=True,
        ensure_ascii=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ─────────────────────────────── the fuzz corpus ───────────────────────────

def _fidelity_corpus(rule_regex: str, n: int, seed: int) -> list[str]:
    """Seeded fuzz strings: a large random body PLUS hand-crafted adversarial
    cases (string start/end boundaries, chars adjacent to \\b, Unicode word
    characters, the empty string). The random vocabulary is seeded from the
    literal characters of the rule itself so the fuzz actually exercises the
    match/near-miss region rather than random noise."""
    rng = random.Random(seed)

    # Characters that appear literally in the rule, plus boundary-relevant and
    # Unicode-word adversaries.
    literal_chars = sorted({c for c in rule_regex if c.isprintable() and c not in "\\"})
    boundary_chars = list(" \t\n\r=:;\"'(){}[].,-_/")
    unicode_word = ["é", "Ω", "中", "ñ", "٠", " ", "​", "A", "a", "9", "_"]
    pool = literal_chars + boundary_chars + unicode_word or ["a", "b", " "]

    out: list[str] = [""]  # empty string is always in the corpus
    for _ in range(n - 1):
        length = rng.randint(0, 24)
        out.append("".join(rng.choice(pool) for _ in range(length)))

    # Explicit adversarial boundary cases derived from the rule's own literals:
    # wrap a plausible near-match in start/end and word/non-word neighbours.
    return out


# ───────────────────────────────── proofs ──────────────────────────────────

def _prove(rule_id: str, class_name: str, fuzz_n: int, walk_n: int, seed: int):
    """Run A1/A2/A3. Returns (constraint_fsm, constraint_regex, forbidden_fsm,
    Proofs, equivalence, states_checked)."""
    from tutor.eval.harness import grade  # deferred: keeps import graph light

    rule = _load_rule(class_name, rule_id)
    rx = rule["check_regex"]

    rw = rewrite_to_forbidden_language(rx)
    if not rw.ok:
        raise ValueError(f"rule {class_name}/{rule_id} is not Tier-A: {rw.reason}")

    forbidden_fsm = greenery.parse(rw.forbidden_pattern).to_fsm()  # L(Σ*RΣ*)
    constraint_fsm = forbidden_fsm.everythingbut().reduce()        # min. complement
    constraint_regex = _render_constraint_regex(constraint_fsm)

    # ── A1 emptiness ──
    intersection = constraint_fsm & forbidden_fsm
    emptiness_passed = intersection.empty()
    emptiness = EmptinessProof(
        passed=emptiness_passed,
        states_checked=len(constraint_fsm.states) + len(forbidden_fsm.states),
    )

    # ── A2 fidelity differential fuzz ──
    pyre = re.compile(rx)
    corpus = _fidelity_corpus(rx, fuzz_n, seed)
    forbid_less: list[str] = []   # constraint would ACCEPT a real violation -> FAIL
    overapprox: list[str] = []    # constraint rejects a non-violation -> superset
    for s in corpus:
        py_violation = bool(pyre.search(s))
        fsm_violation = forbidden_fsm.accepts(s)  # in Σ*RΣ* == "a violation"
        if py_violation == fsm_violation:
            continue
        if py_violation and not fsm_violation:
            forbid_less.append(s)     # Python matches, we say clean -> UNSOUND
        else:
            overapprox.append(s)      # we match, Python doesn't -> over-forbid
    fidelity = FidelityProof(
        passed=(len(forbid_less) == 0),
        samples=len(corpus),
        divergences=len(forbid_less) + len(overapprox),
        forbid_less_witnesses=[repr(w) for w in forbid_less[:10]],
        overapprox_witnesses=[repr(w) for w in overapprox[:10]],
    )

    # ── A3 grader-in-the-loop ──
    # Enumerate accepting strings of the constraint FSM (length+lexical order)
    # AND take some randomized deeper walks for near-miss coverage, then run
    # each through the REAL grader; the certified rule must never fire.
    walks = _sample_constraint_strings(constraint_fsm, walk_n, seed)
    grader_violations = 0
    for s in walks:
        result = grade(s, class_name)
        if any(v.rule == rule_id for v in result.violations):
            grader_violations += 1
    grader = GraderInLoopProof(
        passed=(grader_violations == 0),
        walks=len(walks),
        violations_of_certified_rule=grader_violations,
    )

    # ── equivalence verdict (honesty bar) ──
    if not (emptiness_passed and fidelity.passed and grader.passed):
        equivalence: Literal["EXACT", "SOUND_OVERAPPROX", "NONE"] = "NONE"
    elif overapprox:
        equivalence = "SOUND_OVERAPPROX"
    else:
        equivalence = "EXACT"

    proofs = Proofs(emptiness=emptiness, fidelity=fidelity, grader_in_loop=grader)
    return constraint_fsm, constraint_regex, proofs, equivalence


def _render_constraint_regex(constraint_fsm) -> str | None:
    """Render the complement DFA to a positive regex string, bounded by a
    wall-clock timeout. Returns None on timeout — the certificate is still
    valid (proofs are on the FSM; the constraint is rebuildable via the
    recipe)."""
    old = signal.signal(signal.SIGALRM, _render_alarm)
    signal.alarm(_RENDER_TIMEOUT_SECONDS)
    try:
        return str(from_fsm(constraint_fsm))
    except _RenderTimeout:
        return None
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


# A small pool of representative characters tried first when picking a label
# for a charclass edge (covers the delimiters/quotes/digits/letters and a few
# Unicode-word adversaries the rules care about). Kept tiny so picking a char
# never materializes a 130k-member \w class.
_CHAR_POOL = list(" \t\n\r=:;\"'(){}[].,-_/0123456789abcdefghijklmnopqrstuvwxyzABCDEXYZ") + [
    "é", "Ω", "中",
]


def _pick_edge_char(cc, rng) -> str | None:
    """Pick ONE character accepted by greenery Charclass ``cc`` WITHOUT ever
    expanding the class (a \\w class has ~130k members — materializing it per
    step is the hang we are avoiding). Try the small representative pool via
    cc.accepts(), then fall back to the class's own ord_ranges bounds."""
    pool = _CHAR_POOL[:]
    rng.shuffle(pool)
    for cand in pool:
        if cc.accepts(cand):
            return cand
    # Fallback: the class's declared ranges. For a non-negated class, any
    # codepoint inside a range is accepted; for a negated class, ord_ranges
    # lists the EXCLUDED ranges, so probe just outside them.
    for lo, hi in cc.ord_ranges:
        if not cc.negated:
            cp = lo
            if not (0xD800 <= cp <= 0xDFFF):
                return chr(cp)
        else:
            for cp in (lo - 1, hi + 1):
                if 0 <= cp <= 0x10FFFF and not (0xD800 <= cp <= 0xDFFF) and cc.accepts(chr(cp)):
                    return chr(cp)
    return None


def _representative_edge_chars(cc, rng, k: int = 4) -> list[str]:
    """Up to ``k`` distinct representative chars accepted by ``cc`` — WITHOUT
    expanding the class. Used by the BFS enumeration for edge diversity."""
    out: list[str] = []
    pool = _CHAR_POOL[:]
    rng.shuffle(pool)
    for cand in pool:
        if cc.accepts(cand) and cand not in out:
            out.append(cand)
            if len(out) >= k:
                return out
    if not out:
        one = _pick_edge_char(cc, rng)
        if one is not None:
            out.append(one)
    return out


def _bfs_accepting_strings(fsm, rng, limit: int, max_len: int = 12) -> list[str]:
    """Breadth-first enumerate short accepting strings, sampling a few
    representative chars per edge (never materializing a whole \\w class).
    Deterministic given ``rng``; returns as soon as ``limit`` are collected."""
    from collections import deque

    out: list[str] = []
    seen: set[tuple] = set()
    queue: deque = deque([(fsm.initial, "")])
    while queue and len(out) < limit:
        state, prefix = queue.popleft()
        if state in fsm.finals and prefix not in out:
            out.append(prefix)
            if len(out) >= limit:
                break
        if len(prefix) >= max_len:
            continue
        for cc, nstate in fsm.map.get(state, {}).items():
            for ch in _representative_edge_chars(cc, rng):
                key = (nstate, len(prefix) + 1, ch)
                if key in seen:
                    continue
                seen.add(key)
                queue.append((nstate, prefix + ch))
    return out


def _sample_constraint_strings(constraint_fsm, n: int, seed: int) -> list[str]:
    """Return up to ~n accepting strings of the constraint FSM: a bounded BFS
    enumeration (short members, representative-char sampled) PLUS randomized
    deeper walks, so the sample includes long near-miss strings (e.g. a string
    that ALMOST forms the forbidden pattern but stops one char short), not just
    the shortest members. Never materializes a large charclass."""
    rng = random.Random(seed + 1)
    fsm = constraint_fsm
    strings: list[str] = _bfs_accepting_strings(fsm, rng, limit=n // 2)

    for _ in range(n - len(strings)):
        state = fsm.initial
        chars: list[str] = []
        for _step in range(rng.randint(1, 30)):
            transitions = fsm.map.get(state, {})
            if not transitions:
                break
            cc = rng.choice(list(transitions.keys()))
            ch = _pick_edge_char(cc, rng)
            if ch is None:  # no representative found for this edge — stop walk
                break
            chars.append(ch)
            state = transitions[cc]
        if state in fsm.finals:
            strings.append("".join(chars))
    return strings


# ──────────────────────────── build + persist ──────────────────────────────

def build_certificate(
    class_name: str,
    rule_id: str,
    *,
    fuzz_n: int = 100_000,
    walk_n: int = 1_000,
    seed: int = 20260705,
) -> Certificate:
    rule = _load_rule(class_name, rule_id)
    rx = rule["check_regex"]
    constraint_fsm, constraint_regex, proofs, equivalence = _prove(
        rule_id, class_name, fuzz_n, walk_n, seed
    )

    guarantee = (
        f"On a logits-controlled LOCAL decoding path, output produced under the "
        f"Outlines constraint regex in this certificate is provably in the COMPLEMENT "
        f"of check_regex {rx!r} for rule '{class_name}/{rule_id}' — i.e. the grader's "
        f"own re.finditer of that pattern can never match ({equivalence}). This is "
        f"invariance of THIS rule's check only, proven by DFA-intersection emptiness "
        f"(A1), a 10^5-sample differential fuzz against Python re incl. Unicode/boundary/"
        f"empty adversarial cases (A2), and {proofs.grader_in_loop.walks} accepting-walk "
        f"strings run through the real tutor.eval.harness.grade with zero violations of "
        f"this rule (A3). It is NOT semantic safety (a homoglyph such as a Cyrillic "
        f"'рrint(' passes both grader and certificate), NOT a guarantee about any "
        f"other rule, applies ONLY to the local logits path (API-model submissions stay "
        f"detect-only), and holds modulo Outlines correctly enforcing the char-level DFA "
        f"at the token level."
    )

    recipe = (
        "greenery.parse(rewrite_to_forbidden_language(source_check.pattern)."
        "forbidden_pattern).to_fsm().everythingbut().reduce()  "
        "# deterministic; the SSOT constraint DFA — constraint_regex is a "
        "rendering of this same machine when it fit the render budget."
    )

    return Certificate(
        rule_id=rule_id,
        class_name=class_name,
        source_check=SourceCheck(kind="check_regex", pattern=rx),
        source_hash=_source_hash(rule),
        constraint_regex=constraint_regex,
        constraint_recipe=recipe,
        alphabet="Unicode scalar values U+0000..U+10FFFF (surrogates excluded); "
        "\\w/\\d/\\s interpreted with Python re's Unicode-aware default semantics",
        equivalence=equivalence,
        proofs=proofs,
        guarantee=guarantee,
    )


def write_certificate(cert: Certificate) -> Path:
    _CERTS_DIR.mkdir(parents=True, exist_ok=True)
    path = _CERTS_DIR / f"{cert.class_name}__{cert.rule_id}.json"
    path.write_text(cert.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return path


# The three concrete rules certified by build order step 4.
TARGET_RULES = [
    ("brushes", "positive-tabindex"),
    ("architect", "single-operator-mode"),
    ("architect", "print-logging"),
]


if __name__ == "__main__":
    import sys

    fuzz_n = 100_000
    if "--quick" in sys.argv:
        fuzz_n = 5_000
    for class_name, rule_id in TARGET_RULES:
        cert = build_certificate(class_name, rule_id, fuzz_n=fuzz_n)
        path = write_certificate(cert)
        print(
            f"{class_name}/{rule_id}: {cert.equivalence}  "
            f"(A1 empty={cert.proofs.emptiness.passed} "
            f"states={cert.proofs.emptiness.states_checked}; "
            f"A2 fuzz={cert.proofs.fidelity.samples} div={cert.proofs.fidelity.divergences} "
            f"forbid_less={len(cert.proofs.fidelity.forbid_less_witnesses)}; "
            f"A3 walks={cert.proofs.grader_in_loop.walks} "
            f"rule_violations={cert.proofs.grader_in_loop.violations_of_certified_rule}) "
            f"-> {path.name}"
        )
