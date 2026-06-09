"""
credential-adjuster grader — insurance claims handling computation-heavy checks.

Layer 2 validations that require cross-text analysis beyond single-line regex.

Current graders:
  - adjuster-disclaimer-presence: Verifies that model outputs containing claims
    handling guidance include a proper scope-of-practice disclaimer.
  - good-faith-balance: Checks that claim discussions reference both factual
    investigation and good-faith standards — not just adversarial tactics.
  - investigation-documentation-completeness: Verifies that when investigation
    steps are discussed, the text references documentation requirements.
  - coverage-analysis-completeness: Confirms that coverage discussions include
    both policy language analysis and factual findings.
  - settlement-reasonableness: Checks that settlement discussions frame offers
    in terms of documented damages and good-faith evaluation.

Usage (called by the Layer 1 harness after regex checks pass):
    from tutor.classes.credential_adjuster.grader import grade_credential_adjuster
    results = grade_credential_adjuster(submission_text, metadata={})
"""

from __future__ import annotations

import re
from typing import Any


# ── HELPER PATTERNS ──────────────────────────────────────────────────────────

_ADJUSTER_ADVICE_TRIGGERS = re.compile(
    r"(?i)\b(?:"
    r"claim(?:s)?\s+(?:handling|adjustment|process|file|investigation|evaluation|"
    r"settlement|resolution|management|decision|determination|denial|payment)"
    r"|coverage\s+(?:analysis|determination|decision|opinion|issue|question|dispute)"
    r"|insured[''']?s?\s+(?:claim|loss|damage|policy|right|obligation)"
    r"|adjust(?:er|ing)\s+the\s+(?:claim|loss)"
    r"|investigat(?:e|ion|ing)\s+(?:the\s+)?claim"
    r"|settlement\s+(?:offer|amount|agreement|negotiation|discuss|value)"
    r"|bad\s+faith|duty\s+to\s+(?:settle|defend|investigate)"
    r")\b",
)

_REQUIRED_DISCLAIMER_PHRASES = [
    r"(?i)\bnot\s+(?:a\s+)?(?:licensed\s+)?(?:claims\s+)?(?:adjuster|"
    r"insurance\s+(?:claims\s+)?professional|public\s+adjuster|"
    r"independent\s+adjuster)\b",
    r"(?i)\b(?:AI|assistant|I\s+am\s+an?\s+AI)\s+(?:is\s+not|cannot|does\s+not|"
    r"should\s+not)\s+(?:replace|substitute\s+for)\b",
    r"(?i)\bconsult\s+(?:a\s+)?(?:licensed\s+)?(?:claims\s+)?(?:adjuster|"
    r"insurance\s+professional|public\s+adjuster|attorney|legal\s+counsel)\b",
    r"(?i)\bfor\s+(?:educational|informational)\s+purposes\s+(?:only|and)",
    r"(?i)\bfinal\s+(?:coverage|settlement|claim)\s+(?:determination|decision|"
    r"authority)\s+(?:rest\w+\s+with|reside\w+\s+with|belong\w+\s+to)\s+"
    r"(?:a\s+)?(?:licensed\s+)?(?:adjuster|professional|insurer)\b",
]

_INVESTIGATION_LANGUAGE = re.compile(
    r"(?i)\b(?:"
    r"investigat(?:e|ion|ing|ed|or)"
    r"|inspect(?:ion|ed|ing|or)?"
    r"|examin(?:e|ation|ed|ing)"
    r"|interview"
    r"|site\s+(?:visit|inspection|examination)"
    r"|loss\s+(?:site|scene|location)"
    r"|photograph|diagram|measure"
    r"|document\s+(?:review|collection|gathering)"
    r"|recorded\s+statement"
    r"|examination\s+under\s+oath"
    r")\b",
)

_DOCUMENTATION_LANGUAGE = re.compile(
    r"(?i)\b(?:"
    r"document(?:ation|ed|ing|s)?"
    r"|claim\s+file"
    r"|file\s+(?:note|entry|record)"
    r"|contemporaneous"
    r"|written\s+record"
    r"|diary|log|chronology"
    r")\b",
)

_COVERAGE_LANGUAGE = re.compile(
    r"(?i)\b(?:"
    r"cover(?:age|ed|ing|s)?"
    r"|policy\s+(?:language|provision|exclusion|condition|limit|term|section)"
    r"|exclusion"
    r"|endorsement"
    r"|limit|sub.?\s*limit|deductible"
    r"|peril|risk"
    r")\b",
)

_FACTUAL_FINDING_LANGUAGE = re.compile(
    r"(?i)\b(?:"
    r"fact(?:ual|s|or)?"
    r"|finding|evidence|proof"
    r"|based\s+on\s+(?:the\s+)?(?:investigation|evidence|facts?|policy|documentation)"
    r"|according\s+to\s+the\s+(?:record|report|file|policy)"
    r"|investigation\s+(?:revealed|found|showed|indicated|determined)"
    r")\b",
)

_SETTLEMENT_LANGUAGE = re.compile(
    r"(?i)\b(?:"
    r"settle(?:ment|d)?"
    r"|offer"
    r"|negotiat(?:e|ion|ing|ed|or)"
    r"|demand"
    r"|engage\s+in"
    r")\b",
)

_DAMAGES_LANGUAGE = re.compile(
    r"(?i)\b(?:"
    r"damage(?:s|d)?"
    r"|evaluat(?:e|ion|ing|ed)"
    r"|estimate"
    r"|valuation|value|cost"
    r"|loss"
    r"|appraisal"
    r")\b",
)


# ── INDIVIDUAL GRADERS ───────────────────────────────────────────────────────


def grade_adjuster_disclaimer_presence(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Grade whether claims handling guidance includes a scope-of-practice disclaimer.

    An AI assistant providing claims handling information must include a clear
    statement that it is not a licensed adjuster, cannot make binding claim
    decisions, and recommends consulting a licensed professional.

    Returns dict with ``pass`` (bool), ``reason`` (str), and ``matches`` (list).
    """
    has_advice = bool(_ADJUSTER_ADVICE_TRIGGERS.search(text))

    if not has_advice:
        return {
            "pass": True,
            "reason": "No claims handling language detected; disclaimer not required",
            "matches": [],
        }

    found_phrases: list[str] = []
    for phrase in _REQUIRED_DISCLAIMER_PHRASES:
        if re.search(phrase, text):
            found_phrases.append(phrase)

    if found_phrases:
        return {
            "pass": True,
            "reason": (
                f"Adjuster scope-of-practice disclaimer present "
                f"({len(found_phrases)} component(s) matched)"
            ),
            "matches": found_phrases,
        }

    return {
        "pass": False,
        "reason": (
            "Claims handling guidance detected without required scope-of-practice "
            "disclaimer. Include a statement that you are an AI assistant, not a "
            "licensed claims adjuster, and recommend consulting a licensed "
            "adjuster or insurance professional for binding claim decisions."
        ),
        "matches": [],
    }


def grade_good_faith_balance(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Check that claim discussions reference good-faith standards.

    When claims handling language is detected, the text should reference
    good-faith standards or the duty of fair dealing -- not purely adversarial
    or cost-minimization framing.

    Returns dict with ``pass`` (bool), ``reason`` (str), and ``matches`` (list).
    """
    matches: list[str] = []

    has_advice = bool(_ADJUSTER_ADVICE_TRIGGERS.search(text))

    if not has_advice:
        return {
            "pass": True,
            "reason": "No claims handling language detected; good-faith check skipped",
            "matches": [],
        }

    # Look for good-faith language
    good_faith_language = re.compile(
        r"(?i)\b(?:"
        r"good\s+faith|good[-\s]faith"
        r"|fair\s+(?:dealing|settlement|treatment|and\s+equitable|claim)"
        r"|duty\s+of\s+(?:good\s+faith|fair\s+dealing)"
        r"|reasonab(?:le|ly)\s+(?:basis|investigation|decision|adjuster|person)"
        r"|implied\s+covenant"
        r"|fairly|equitably"
        r"|equal\s+consideration"
        r")\b",
    )

    has_good_faith = bool(good_faith_language.search(text))

    if not has_good_faith:
        matches.append(
            "Claims handling language detected without reference to good-faith "
            "standards or the duty of fair dealing"
        )

    return {
        "pass": len(matches) == 0,
        "reason": "; ".join(matches)
        if matches
        else "Good-faith standards referenced alongside claims handling language",
        "matches": matches,
    }


def grade_investigation_documentation(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Check that investigation discussions reference documentation requirements.

    When investigation language is detected, the text should also reference
    documentation of investigation steps.

    Returns dict with ``pass`` (bool), ``reason`` (str), and ``matches`` (list).
    """
    matches: list[str] = []

    has_investigation = bool(_INVESTIGATION_LANGUAGE.search(text))

    if not has_investigation:
        return {
            "pass": True,
            "reason": "No investigation language detected; documentation check skipped",
            "matches": [],
        }

    has_documentation = bool(_DOCUMENTATION_LANGUAGE.search(text))

    if not has_documentation:
        matches.append(
            "Investigation language detected without reference to documentation "
            "requirements. Investigation steps should be documented in the claim "
            "file with dates, findings, and conclusions."
        )

    return {
        "pass": len(matches) == 0,
        "reason": "; ".join(matches)
        if matches
        else (
            "Investigation steps include documentation references"
        ),
        "matches": matches,
    }


def grade_coverage_analysis_completeness(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Check that coverage discussions include both policy language analysis
    and factual findings.

    A complete coverage analysis references both the applicable policy language
    and the factual findings from the investigation.

    Returns dict with ``pass`` (bool), ``reason`` (str), and ``matches`` (list).
    """
    matches: list[str] = []

    has_coverage = bool(_COVERAGE_LANGUAGE.search(text))

    if not has_coverage:
        return {
            "pass": True,
            "reason": "No coverage language detected; completeness check skipped",
            "matches": [],
        }

    has_factual = bool(_FACTUAL_FINDING_LANGUAGE.search(text))

    if not has_factual:
        matches.append(
            "Coverage analysis language detected without reference to factual "
            "findings. A complete coverage analysis must apply policy language "
            "to specific factual findings from the investigation."
        )

    return {
        "pass": len(matches) == 0,
        "reason": "; ".join(matches)
        if matches
        else "Coverage analysis references both policy language and factual findings",
        "matches": matches,
    }


def grade_settlement_reasonableness(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Check that settlement discussions frame offers in terms of documented
    damages and good-faith evaluation.

    When settlement language is detected, the text should reference the
    basis for the offer (damage evaluation) rather than simply urging
    settlement without context.

    Returns dict with ``pass`` (bool), ``reason`` (str), and ``matches`` (list).
    """
    matches: list[str] = []

    has_settlement = bool(_SETTLEMENT_LANGUAGE.search(text))

    if not has_settlement:
        return {
            "pass": True,
            "reason": "No settlement language detected; reasonableness check skipped",
            "matches": [],
        }

    has_damages = bool(_DAMAGES_LANGUAGE.search(text))

    if not has_damages:
        matches.append(
            "Settlement discussion detected without reference to documented "
            "damages or damage evaluation. Settlement offers should be based "
            "on a good-faith evaluation of covered damages."
        )

    return {
        "pass": len(matches) == 0,
        "reason": "; ".join(matches)
        if matches
        else "Settlement discussion references documented damages or evaluation",
        "matches": matches,
    }


# ── AGGREGATE GRADER ─────────────────────────────────────────────────────────


def grade_credential_adjuster(
    text: str, metadata: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    """Run all credential-adjuster graders and return results.

    Args:
        text: The submitted model response text.
        metadata: Optional dict with contextual info (e.g. {"context": "coverage_analysis"}).

    Returns:
        List of result dicts, one per grader, each with:
            grader_id (str): unique identifier
            pass (bool): whether the check passed
            reason (str): explanation
            matches (list): matched items if applicable
    """
    graders: list[tuple[str, Any]] = [
        ("adjuster-disclaimer-presence", grade_adjuster_disclaimer_presence),
        ("good-faith-balance", grade_good_faith_balance),
        ("investigation-documentation", grade_investigation_documentation),
        ("coverage-analysis-completeness", grade_coverage_analysis_completeness),
        ("settlement-reasonableness", grade_settlement_reasonableness),
    ]

    results: list[dict[str, Any]] = []
    for grader_id, grader_fn in graders:
        result = grader_fn(text, metadata)
        result["grader_id"] = grader_id
        results.append(result)

    return results
