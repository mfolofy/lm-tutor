r"""Rewrite a class.yaml ``check_regex`` into a plain, greenery-parseable
regex whose language is EXACTLY ``Σ*·R·Σ*`` under Python ``re.finditer``
semantics — i.e. "R matches somewhere in this string".

greenery's own parser (see tutor/cert/compile.py) understands a large
regular-expression subset (literals, ``[...]`` classes, ``\w`` ``\d`` ``\s``,
alternation, groups, quantifiers) but NOT: the ``(?i)`` inline flag, ``\b``
word-boundary anchors, or lookaround. Those three constructs are exactly
what several class.yaml rules use, so this module hand-expands them into
plain regex text before handing off to greenery — never guessing when a
construct falls outside what it can prove exact.

Design constraint (the honesty bar): Python's ``\w``/``\b`` are Unicode-aware
by default; greenery's built-in ``\w`` is ASCII-only. Any construct whose
correctness depends on word-boundary semantics is rewritten using the real
Python \\w codepoint ranges (tutor/cert/unicode_word_ranges.json, generated
by gen_unicode_word_ranges.py), not greenery's ASCII approximation — getting
this wrong would silently certify the wrong language.

Supported source syntax (anything else -> RewriteResult(ok=False, reason=...)):
  - an optional leading ``(?i)`` inline flag (ASCII-letter case-folding only;
    a bare unescaped letter inside a ``[...]`` class under ``(?i)`` is refused,
    not guessed)
  - an optional leading single-char-class negative lookbehind: ``(?<![...])``
  - a body of literal chars, escapes (``\s`` ``\d`` ``\w`` ``\.`` ``\(`` etc.),
    ``[...]`` classes, ``(?:...)`` groups, ``|`` ``?`` ``*`` ``+`` ``{m,n}``
  - an optional single trailing ``\b`` anchor

Anything else in the body (mid-pattern ``\b``, lookahead, capturing-group
backreferences, additional lookbehind, unbalanced brackets) -> NONE.
"""

from __future__ import annotations

import json
import re as _re
from dataclasses import dataclass
from pathlib import Path

_RANGES_PATH = Path(__file__).parent / "unicode_word_ranges.json"

# The "any single character" class, spanning the full Unicode scalar range.
# (Python str never contains lone surrogates, so this is exact.)
SIGMA_CLASS = "[" + chr(0) + "-" + chr(0x10FFFF) + "]"
SIGMA_STAR = SIGMA_CLASS + "*"

_UNSUPPORTED_BODY_RE = _re.compile(
    r"\\b|\(\?=|\(\?!|\(\?<=|\(\?<!|\\[1-9]"
)


@dataclass
class RewriteResult:
    ok: bool
    forbidden_pattern: str | None = None  # greenery-parseable, means Σ*RΣ*
    reason: str | None = None


def _ranges_to_inner(ranges: list[list[int]]) -> str:
    return "".join(chr(lo) if lo == hi else f"{chr(lo)}-{chr(hi)}" for lo, hi in ranges)


def _load_shorthand_inner_texts() -> dict[str, str]:
    """Return {'w': <inner-ranges-text>, 'd': ..., 's': ...} — the precise,
    Python-re-matching inner content for \\w \\d \\s bracket expressions.
    NEVER let greenery parse a bare \\w/\\d/\\s/\\W/\\D/\\S itself — its
    built-in versions of these are ASCII-only and a real, caught divergence
    (see module docstring) from Python's Unicode-aware default semantics."""
    data = json.loads(_RANGES_PATH.read_text(encoding="utf-8"))
    return {name: _ranges_to_inner(spec["ranges"]) for name, spec in data["classes"].items()}


_SHORTHAND_INNER = _load_shorthand_inner_texts()
WORD_CLASS = f"[{_SHORTHAND_INNER['w']}]"
NONWORD_CLASS = f"[^{_SHORTHAND_INNER['w']}]"

_CLASS_SHORTHAND = {"d", "D", "w", "W", "s", "S"}


def _normalize_class_inner(inner: str, casefold: bool) -> str | None:
    """Normalize the inside of a ``[...]`` block for greenery, which (unlike
    Python's ``re``) does not accept a backslash before an ordinary
    (non-shorthand) character inside a class — e.g. ``[\\']`` is rejected
    even though Python's ``re`` treats ``\\'`` there as a redundant, harmless
    escape of a literal ``'``. We strip exactly that class of *redundant*
    escape (backslash immediately followed by ASCII punctuation that is not
    one of the ``\\d \\w \\s \\D \\W \\S`` shorthands), which is semantically
    identical to Python's own treatment of it inside a class. Anything else
    unrecognized -> None (refuse rather than guess). If ``casefold`` and a
    bare unescaped ASCII letter is found, also -> None (class-level case
    folding is not implemented)."""
    out: list[str] = []
    k = 0
    n = len(inner)
    while k < n:
        ch = inner[k]
        if ch == "\\":
            if k + 1 >= n:
                return None
            nxt = inner[k + 1]
            if nxt.lower() in ("d", "w", "s"):
                if nxt.isupper():
                    # \D \W \S mixed into a wider class: negation-inside-a-
                    # union isn't expressible as a simple text splice here
                    # (would need De Morgan over the whole class) — refuse.
                    return None
                out.append(_SHORTHAND_INNER[nxt])  # precise Unicode ranges
            elif nxt.isascii() and not nxt.isalnum():
                # redundant escape of ordinary punctuation -> drop backslash
                out.append(nxt)
            else:
                return None
            k += 2
            continue
        if casefold and ch.isascii() and ch.isalpha():
            return None  # bare letter inside a class under (?i): refuse
        out.append(ch)
        k += 1
    return "".join(out)


def _case_fold_body(body: str, casefold: bool) -> str | None:
    """Walk ``body``, expanding bare ASCII letters into ``[Xx]`` classes when
    ``casefold`` is set, leaving escapes / [...] classes / regex-meta chars
    otherwise untouched (beyond the class-escape normalization every class
    always goes through — see _normalize_class_inner)."""
    out: list[str] = []
    i, n = 0, len(body)
    while i < n:
        c = body[i]
        if c == "\\":
            if i + 1 >= n:
                return None
            nxt = body[i + 1]
            if nxt.lower() in ("d", "w", "s"):
                # Never let greenery see a bare \w/\d/\s/\W/\D/\S — its
                # built-ins are ASCII-only; substitute precise Unicode text.
                inner = _SHORTHAND_INNER[nxt.lower()]
                out.append(f"[^{inner}]" if nxt.isupper() else f"[{inner}]")
            else:
                out.append(body[i : i + 2])
            i += 2
        elif c == "[":
            j = body.find("]", i + 1)
            if j == -1:
                return None
            inner = _normalize_class_inner(body[i + 1 : j], casefold)
            if inner is None:
                return None
            out.append(f"[{inner}]")
            i = j + 1
        elif casefold and c.isascii() and c.isalpha():
            lo, up = c.lower(), c.upper()
            out.append(f"[{lo}{up}]" if lo != up else c)
            i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def rewrite_to_forbidden_language(check_regex: str) -> RewriteResult:
    """Rewrite ``check_regex`` (as it appears verbatim in a class.yaml rule)
    into the exact forbidden-language regex text: the set of strings
    containing a match of ``check_regex`` anywhere, per Python re.finditer.
    """
    remainder = check_regex
    case_insensitive = False
    lookbehind_negset: str | None = None
    trailing_boundary = False

    if remainder.startswith("(?i)"):
        case_insensitive = True
        remainder = remainder[len("(?i)") :]

    m = _re.match(r"^\(\?<!(\[[^\]]*\])\)", remainder)
    if m:
        lookbehind_negset = m.group(1)
        remainder = remainder[m.end() :]

    if remainder.endswith("\\b") and not remainder.endswith("\\\\b"):
        trailing_boundary = True
        remainder = remainder[: -len("\\b")]

    if _UNSUPPORTED_BODY_RE.search(remainder):
        return RewriteResult(
            ok=False,
            reason=f"unsupported construct in body after stripping known anchors: {remainder!r}",
        )

    # Always normalize [...] classes (greenery rejects Python's redundant
    # backslash-escapes of ordinary punctuation inside a class, e.g. [\']),
    # and additionally case-fold bare letters when (?i) is present.
    normalized = _case_fold_body(remainder, casefold=case_insensitive)
    if normalized is None:
        reason = (
            "(?i) present but body has a letter inside a [...] class "
            "(class-level case folding not implemented — refusing rather than guessing)"
            if case_insensitive
            else "body contains a [...] class with an unsupported escape sequence"
        )
        return RewriteResult(ok=False, reason=reason)
    body = normalized

    # Sanity: the body itself must be non-empty and balanced enough for
    # greenery to parse later; we don't re-validate bracket/paren balance
    # here (compile.py's greenery.parse call is the real validator and will
    # raise if this rewrite produced something malformed).

    if lookbehind_negset is not None:
        # (?<![...])BODY  ==  BODY at start of string, OR BODY immediately
        # preceded by a char NOT in the lookbehind's negated set.
        # This is the exact Σ*RΣ* forbidden language for this pattern shape.
        negset_inner = _normalize_class_inner(lookbehind_negset[1:-1], casefold=False)
        if negset_inner is None:
            return RewriteResult(
                ok=False, reason="lookbehind class has an unsupported escape sequence"
            )
        not_negset = f"[^{negset_inner}]"
        core = f"(?:{body}|{SIGMA_STAR}{not_negset}{body})"
        forbidden = f"{core}{SIGMA_STAR}"
        return RewriteResult(ok=True, forbidden_pattern=forbidden)

    if trailing_boundary:
        # BODY\b  ==  BODY followed by a non-word char and then anything,
        # OR BODY occurring at the very end of the string (nothing after).
        forbidden = f"{SIGMA_STAR}(?:{body})(?:{NONWORD_CLASS}{SIGMA_STAR}|)"
        return RewriteResult(ok=True, forbidden_pattern=forbidden)

    # Plain case: no anchors at all.
    forbidden = f"{SIGMA_STAR}(?:{body}){SIGMA_STAR}"
    return RewriteResult(ok=True, forbidden_pattern=forbidden)
