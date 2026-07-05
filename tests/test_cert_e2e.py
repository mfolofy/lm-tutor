"""Layer B e2e — DEMONSTRATION only, skipped unless the cert model deps are
installed (pip install -e '.[cert]'). Proves the mechanism on a real small
model: under the certificate's constraint the certified violation cannot be
emitted, while an unconstrained baseline on the SAME prompt/seed does emit it.

Mandatory honesty guard (per the build plan): if the unconstrained baseline
does NOT violate, the test is INCONCLUSIVE (xfail), never a silent pass — a
green result requires constrained==0 AND unconstrained>=1.
"""

from pathlib import Path

import pytest

pytest.importorskip("outlines", reason="Layer B model deps not installed ([cert] extra)")
pytest.importorskip("transformers", reason="Layer B model deps not installed ([cert] extra)")
pytest.importorskip("torch", reason="Layer B model deps not installed ([cert] extra)")

from tutor.cert.certificate import Certificate  # noqa: E402
from tutor.cert.decode import run_e2e  # noqa: E402

_CERTS_DIR = Path(__file__).parent.parent / "tutor" / "cert" / "certs"

# We demo on brushes/positive-tabindex: its constraint's distinguishing
# alphabet is small (~50 symbols), so the greenery->interegular translation is
# provably FAITHFUL (verified in decode.build_constraint_interegular_fsm) and
# Outlines' byte-level index is tractable. The \b/\w rules (print-logging,
# single-operator-mode) are certified EXACT at Layer A but their word-vs-
# non-word distinction spans ~130k Unicode chars that cannot compress into
# Outlines' compact alphabet — decode.py raises rather than demo a lossy
# constraint, so they are deliberately NOT used for the model demo.
_TABINDEX_PROMPT = (
    "Write one HTML div with a positive tabindex attribute of 3. "
    'Reply with ONLY the tag, e.g. <div tabindex="3">.'
)


@pytest.mark.slow
def test_tabindex_constrained_blocks_violation():
    cert = Certificate.model_validate_json(
        (_CERTS_DIR / "brushes__positive-tabindex.json").read_text()
    )
    outcome = run_e2e(cert, _TABINDEX_PROMPT, max_new_tokens=64)

    if outcome.unconstrained_violations < 1:
        pytest.xfail(
            "INCONCLUSIVE: unconstrained baseline did not emit the violation on this "
            f"prompt/seed (got text {outcome.unconstrained_text!r}); strengthen the "
            "prompt. NOT counted as a pass."
        )

    assert outcome.constrained_violations == 0, (
        f"certificate FAILED: constrained output still violated the rule: "
        f"{outcome.constrained_text!r}"
    )
    assert outcome.unconstrained_violations >= 1
