r"""Generate the cached Unicode \w / \d / \s range tables used by rewrite.py.

Python's ``re`` module's ``\w``, ``\d``, and ``\s`` are Unicode-aware by
default (e.g. \w matches 'é', \d matches Unicode decimal digits beyond
0-9, \s matches Unicode whitespace like U+00A0 NBSP). greenery's built-in
versions of these shorthands are ASCII-only. For an EXACT certificate we
cannot let greenery interpret \w/\d/\s itself — a rewritten pattern that
relies on greenery's ASCII notion of these classes can silently diverge
from the real check_regex's Python-re semantics (this was caught live by
the A2 differential fuzz: 'éprint(' — the real regex's `(?<![.\w])`
lookbehind correctly refuses to match there since 'é' is a Python \w char,
but a naive rewrite using greenery's ASCII \w said it should).

So rewrite.py never emits a bare \w/\d/\s/\W/\D/\S for greenery to parse;
it substitutes the precise bracket-expression text computed here instead.

This script walks every Unicode scalar value (surrogates excluded — never
valid ``str`` characters) and asks CPython's own ``re`` engine whether it
matches each of \w \d \s, then RLE-compresses each result into contiguous
[lo, hi] ranges. Run once; output committed as JSON so cert code never
recomputes this (~0.3s total) without provenance.

Run: python -m tutor.cert.gen_unicode_word_ranges
"""

import json
import re
from pathlib import Path

_OUT = Path(__file__).parent / "unicode_word_ranges.json"

_CLASSES = {"w": r"\w", "d": r"\d", "s": r"\s"}


def compute_ranges(shorthand_pattern: str) -> list[list[int]]:
    pat = re.compile(shorthand_pattern)
    ranges: list[list[int]] = []
    start = None
    for cp in range(0x110000):
        if 0xD800 <= cp <= 0xDFFF:
            is_match = False  # surrogate code points, never real str chars
        else:
            is_match = bool(pat.match(chr(cp)))
        if is_match:
            if start is None:
                start = cp
        else:
            if start is not None:
                ranges.append([start, cp - 1])
                start = None
    if start is not None:
        ranges.append([start, 0x10FFFF])
    return ranges


if __name__ == "__main__":
    out = {
        "generated_by": "tutor.cert.gen_unicode_word_ranges",
        "python_re_semantics": "Unicode, default flags",
        "classes": {},
    }
    for name, pattern in _CLASSES.items():
        ranges = compute_ranges(pattern)
        out["classes"][name] = {"pattern": pattern, "num_ranges": len(ranges), "ranges": ranges}
        print(f"{name} ({pattern}): {len(ranges)} ranges")
    _OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {_OUT}")
