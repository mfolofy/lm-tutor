"""Step-2 unit tests for tutor.cert.rewrite — the (?i)/\\b/lookbehind rewriter.

Each transform gets its own targeted assertion plus a differential fuzz
against Python's real `re` engine (the harness's own matcher), with
explicit adversarial cases for string start/end boundaries, characters
adjacent to \\b, Unicode word characters, and the empty string — per the
zero-tolerance rule: any divergence must FAIL the test, never be silently
absorbed.
"""

import random
import re

import greenery
import pytest

from tutor.cert.rewrite import rewrite_to_forbidden_language

# The three rules this certificate targets, verbatim from class.yaml.
TABINDEX_RE = r'tabindex\s*=\s*"\s*[1-9][0-9]*\s*"'
SINGLE_OPERATOR_RE = r'(?i)single_operator(?:_mode)?\s*[:=]\s*["\']?(?:true|yes|1)\b'
PRINT_LOGGING_RE = r"(?<![.\w])print\("


def _assert_exact(check_regex: str, samples: list[str]) -> None:
    res = rewrite_to_forbidden_language(check_regex)
    assert res.ok, res.reason
    fsm = greenery.parse(res.forbidden_pattern).to_fsm()
    pyre = re.compile(check_regex)
    mismatches = [
        (s, bool(pyre.search(s)), fsm.accepts(s))
        for s in samples
        if bool(pyre.search(s)) != fsm.accepts(s)
    ]
    assert mismatches == [], f"divergence(s) from Python re: {mismatches}"


# ─────────────────────────── plain case (no anchors) ───────────────────────

def test_plain_no_anchors_exact():
    _assert_exact(
        TABINDEX_RE,
        [
            "",
            "tabindex=\"3\"",
            "tabindex=\"0\"",
            "tabindex = \"12\"",
            "tabindex=\"-1\"",
            "TABINDEX=\"3\"",  # wrong case entirely, no (?i) here -> no match
            "x tabindex=\"7\" y",
        ],
    )


# ───────────────────────────── (?i) expansion ───────────────────────────────

def test_case_insensitive_expansion_basic():
    res = rewrite_to_forbidden_language(SINGLE_OPERATOR_RE)
    assert res.ok
    # every expanded literal letter must be a 2-member class
    assert "[sS]" in res.forbidden_pattern
    assert "[Tt]" not in res.forbidden_pattern  # order is lower,upper: [tT]... check both orders present
    assert "[tT]" in res.forbidden_pattern


def test_case_insensitive_refuses_letter_inside_class():
    # A synthetic rule with a letter inside a class under (?i) — must refuse,
    # not silently produce a wrong (non-case-folded) certificate.
    res = rewrite_to_forbidden_language(r"(?i)[abc]x")
    assert not res.ok
    assert "class" in res.reason


# ──────────────────────────────── trailing \b ───────────────────────────────

def test_trailing_boundary_exact_at_string_end():
    # \b after "true" etc — string ending exactly at the match (no char follows).
    _assert_exact(SINGLE_OPERATOR_RE, ["single_operator=true", "single_operator_mode:true"])


def test_trailing_boundary_exact_word_char_after():
    # A word char immediately after should NOT be a boundary -> NOT a violation.
    _assert_exact(SINGLE_OPERATOR_RE, ["single_operator=true9", "single_operator=true_", "single_operator=trueX"])


def test_trailing_boundary_exact_unicode_word_char_after():
    # The bug this fuzz is designed to catch: a Unicode word char (not ASCII)
    # immediately after the match must still fail the boundary (no violation),
    # matching Python's Unicode-aware \b/\w exactly.
    _assert_exact(SINGLE_OPERATOR_RE, ["single_operator=trueé", "single_operator=trueΩ"])  # é, Ω


def test_trailing_boundary_exact_nonword_char_after():
    _assert_exact(SINGLE_OPERATOR_RE, ["single_operator=true ", "single_operator=true!", "single_operator=true\n"])


def test_trailing_boundary_case_insensitive_and_boundary_combined():
    _assert_exact(
        SINGLE_OPERATOR_RE,
        ["SINGLE_OPERATOR=YES", "Single_Operator_Mode: TRUE", "single_operator=1", "single_operator=10"],
    )


# ─────────────────────────── char-class lookbehind ──────────────────────────

def test_lookbehind_start_of_string():
    # print( at position 0 -- lookbehind vacuously succeeds -> violation.
    _assert_exact(PRINT_LOGGING_RE, ["print(", "print(x)"])


def test_lookbehind_preceded_by_dot_or_word_char_not_a_violation():
    _assert_exact(PRINT_LOGGING_RE, ["x.print(", "self.print(", "xprint(", "_print(", "9print("])


def test_lookbehind_preceded_by_nonword_nondot_is_a_violation():
    _assert_exact(PRINT_LOGGING_RE, [" print(", "\nprint(", "=print(", ";print(", ")print("])


def test_lookbehind_unicode_word_char_before_not_a_violation():
    # The exact case the differential fuzz first caught as a real bug: a
    # Unicode word character (é) before "print(" must NOT be a violation,
    # since Python's \w in the lookbehind is Unicode-aware.
    _assert_exact(PRINT_LOGGING_RE, ["éprint(", "Ωprint(", "中print("])  # é, Ω, 中


# ─────────────────────────────── empty string ───────────────────────────────

def test_empty_string_never_a_violation():
    for rx in (TABINDEX_RE, SINGLE_OPERATOR_RE, PRINT_LOGGING_RE):
        _assert_exact(rx, [""])


# ──────────────────────────── randomized fuzz sweep ─────────────────────────

@pytest.mark.parametrize("check_regex", [TABINDEX_RE, SINGLE_OPERATOR_RE, PRINT_LOGGING_RE])
def test_random_fuzz_sweep(check_regex):
    random.seed(1234)
    vocab_common = list(
        "tabindex=\"'0123456789 \t\n:single_operator_modeTRUEtrueyes1print(). "
    )
    vocab_unicode = ["é", "Ω", "_", "9", "中", "a", "A", " ", " ", "٠"]
    samples = [""]
    for _ in range(1500):
        length = random.randint(0, 20)
        chars = [
            random.choice(vocab_common) if random.random() < 0.7 else random.choice(vocab_unicode)
            for _ in range(length)
        ]
        samples.append("".join(chars))
    _assert_exact(check_regex, samples)


# ───────────────────────────── unsupported constructs ───────────────────────

@pytest.mark.parametrize(
    "bad_regex",
    [
        r"foo\bbar\b",  # \b not at the very end
        r"(?=foo)bar",  # lookahead
        r"(?!foo)bar",  # negative lookahead
        r"(?<=foo)bar",  # lookbehind (not the single-char-class negative form)
        r"(\w+)\1",  # backreference
    ],
)
def test_unsupported_constructs_return_none(bad_regex):
    res = rewrite_to_forbidden_language(bad_regex)
    assert not res.ok
    assert res.reason
