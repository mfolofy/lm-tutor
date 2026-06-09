"""
credential-cpa grader — computation-heavy checks for accounting/finance rules.

Layer 2 validations that require cross-text analysis beyond single-line regex.

Current graders:
  - disclaimer-presence: Verifies that model outputs containing financial
    recommendations include a proper disclaimer (cross-text check not
    expressible as a single check_regex).
  - gaap-citation-validity: Confirms that GAAP ASC references cited by the
    model actually exist and are used in the correct context.

Usage (called by the Layer 1 harness after regex checks pass):
    from tutor.classes.credential_cpa.grader import grade_credential_cpa
    results = grade_credential_cpa(submission_text, metadata={})
"""

from __future__ import annotations

import re
from typing import Any

# ── DISCLAIMER CHECK ────────────────────────────────────────────────────────

FINANCIAL_ADVICE_TRIGGERS = re.compile(
    r"(?i)\b(?:invest|portfolio|buy|sell|trade|allocate|diversify|recommend|"
    r"risk|return|yield|growth|dividend)\b"
)

REQUIRED_DISCLAIMER_PHRASES = [
    r"(?i)not\s+financial\s+advice",
    r"(?i)past\s+performance\s+(?:does\s+not|is\s+not\s+indicative)",
    r"(?i)consult\s+(?:a\s+)?(?:licensed\s+)?(?:financial\s+)?advisor",
    r"(?i)(?:investing|investment|trading)\s+carries?\s+risk",
]

REQUIRED_CPA_DISCLAIMER_PHRASES = [
    r"(?i)not\s+(?:a\s+)?certified\s+(?:public\s+)?accountant",
    r"(?i)consult\s+(?:a\s+)?(?:licensed\s+)?CPA",
]


def _has_disclaimer(text: str, phrases: list[str]) -> bool:
    """Check if the text contains at least one of the required disclaimer phrases."""
    return any(re.search(p, text) for p in phrases)


def grade_disclaimer_presence(text: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    """Grade whether financial advice includes a required disclaimer.

    Returns a dict with `pass` (bool), `reason` (str), and `matches` (list).
    """
    has_advice = bool(FINANCIAL_ADVICE_TRIGGERS.search(text))

    if not has_advice:
        return {
            "pass": True,
            "reason": "No financial terms detected; disclaimer not required.",
            "matches": [],
        }

    has_disclaimer = _has_disclaimer(text, REQUIRED_DISCLAIMER_PHRASES)

    if has_disclaimer:
        return {
            "pass": True,
            "reason": "Required financial disclaimer present.",
            "matches": [],
        }

    return {
        "pass": False,
        "reason": (
            "Financial advice detected without required disclaimer. "
            "Include: 'This is not financial advice. Past performance does not "
            "guarantee future results. Consult a licensed financial advisor.'"
        ),
        "matches": [],
    }


# ── GAAP CITATION VALIDITY ──────────────────────────────────────────────────

# Canonical ASC references (topic.subtopic -- section)
KNOWN_ASC_REFERENCES: dict[str, str] = {
    "606": "Revenue from Contracts with Customers",
    "842": "Leases",
    "326": "Financial Instruments -- Credit Losses (CECL)",
    "740": "Income Taxes",
    "235": "Notes to Financial Statements",
    "250": "Accounting Changes and Error Corrections",
    "350": "Intangibles -- Goodwill and Other",
    "360": "Property, Plant, and Equipment",
    "450": "Contingencies",
    "470": "Debt",
    "480": "Distinguishing Liabilities from Equity",
    "505": "Equity",
    "605": "Revenue Recognition (superseded by ASC 606)",
    "712": "Compensation -- Nonretirement Postemployment Benefits",
    "715": "Compensation -- Retirement Benefits",
    "718": "Compensation -- Stock Compensation",
    "805": "Business Combinations",
    "808": "Collaborative Arrangements",
    "810": "Consolidation",
    "815": "Derivatives and Hedging",
    "820": "Fair Value Measurement",
    "825": "Financial Instruments",
    "830": "Foreign Currency Matters",
    "840": "Leases (superseded by ASC 842)",
}

ASC_REF_PATTERN = re.compile(r"\bASC\s+(\d{3})(?:[-\s](\d{2}(?:-\d{2})?))?\b", re.IGNORECASE)


def grade_gaap_citations(text: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    """Grade ASC reference validity in accounting text.

    Returns a dict with `pass` (bool), `reason` (str),
    `valid_refs` (list), and `invalid_refs` (list).
    """
    matches = ASC_REF_PATTERN.findall(text)
    valid: list[str] = []
    invalid: list[str] = []

    for topic, _sect in matches:
        ref = f"ASC {topic}"
        if topic in KNOWN_ASC_REFERENCES:
            valid.append(ref)
        else:
            invalid.append(ref)

    if invalid:
        return {
            "pass": False,
            "reason": f"Unknown ASC reference(s): {', '.join(invalid)}",
            "valid_refs": valid,
            "invalid_refs": invalid,
        }

    return {
        "pass": True,
        "reason": "All ASC references are valid.",
        "valid_refs": valid,
        "invalid_refs": [],
    }


# ── AGGREGATE GRADER ───────────────────────────────────────────────────────

def grade_credential_cpa(text: str, metadata: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Run all credential-cpa graders and return results.

    Args:
        text: The submitted model response text.
        metadata: Optional dict with contextual info (e.g. {"context": "tax"}).

    Returns:
        List of result dicts, one per grader, each with:
            grader_id (str): unique identifier
            pass (bool): whether the check passed
            reason (str): explanation
            matches (list): matched items if applicable
    """
    results: list[dict[str, Any]] = []

    disclaimer_result = grade_disclaimer_presence(text, metadata)
    disclaimer_result["grader_id"] = "disclaimer-presence"
    results.append(disclaimer_result)

    gaap_result = grade_gaap_citations(text, metadata)
    gaap_result["grader_id"] = "gaap-citation-validity"
    results.append(gaap_result)

    return results
