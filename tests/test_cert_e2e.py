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

# An adversarial prompt that explicitly requests the certified violation, so an
# unconstrained model has a real chance of emitting it.
_PRINT_PROMPT = (
    "Output a single line of Python that logs a debug value using the built-in "
    "print function at the start of the line. Reply with ONLY the code, e.g. "
    "print(x). Do not use logging."
)


@pytest.mark.slow
def test_print_logging_constrained_blocks_violation():
    cert = Certificate.model_validate_json(
        (_CERTS_DIR / "architect__print-logging.json").read_text()
    )
    outcome = run_e2e(cert, _PRINT_PROMPT, max_new_tokens=64)

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
