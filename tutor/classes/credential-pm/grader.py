"""
credential-pm grader — project management computation-heavy checks.

Layer 2 validations that require cross-text analysis beyond single-line regex.

Current graders:
  - change-control-process: Verifies that when scope changes are discussed, the
    formal change control process is referenced (cross-text check not
    expressible as a single check_regex).
  - raci-completeness: Confirms that RACI matrices in the text have proper
    R, A, C, I role assignments for each activity.
  - pm-disclaimer-presence: Verifies that model outputs containing project
    management recommendations include a proper scope-of-practice disclaimer.
  - risk-description-quality: Checks that risk entries include both a
    probability and impact assessment element (not just a label).

Usage (called by the Layer 1 harness after regex checks pass):
    from tutor.classes.credential_pm.grader import grade_credential_pm
    results = grade_credential_pm(submission_text, metadata={})
"""

from __future__ import annotations

import re
from typing import Any


# ── HELPER PATTERNS ──────────────────────────────────────────────────────────

_SCOPE_CHANGE_LANGUAGE = re.compile(
    r"(?i)\b(?:scope\s+change|change\s+request|add\s+(?:a\s+)?(?:new\s+)?(?:feature|requirement|scope)"
    r"|additional\s+(?:work|scope|requirement|feature)"
    r"|new\s+(?:requirement|feature|request|scope\s+item))"
    r"\b",
)

_CHANGE_CONTROL_LANGUAGE = re.compile(
    r"(?i)\b(?:change\s+control\s+(?:board|process|procedure|request|system)"
    r"|CCB\b|impact\s+analysis|change\s+request\s+(?:form|process)"
    r"|formal\s+(?:approval|review|change\s+process)"
    r"|change\s+management\s+(?:plan|process|procedure)"
    r")\b",
)

_RACI_PATTERN = re.compile(
    r"(?i)\bRACI\b",
)

_RACI_ENTRIES = re.compile(
    r"(?i)\b([^\n]*?)\s*[|:\t]\s*([RrAaCcIi])\s*[|:\t]\s*"
    r"([RrAaCcIi])\s*[|:\t]\s*([RrAaCcIi])\s*[|:\t]\s*([RrAaCcIi])\b",
)

_RACI_ROW = re.compile(
    r"(?i)\b(R|A|C|I)\b",
)

_PM_RECOMMENDATION_TRIGGERS = re.compile(
    r"(?i)\b(?:recommend|suggest|advise|should|best\s+practice|you\s+ought|consider"
    r"|project\s+(?:plan|schedule|budget|charter|scope|risk|stakeholder)"
    r"|PMBOK|project\s+management)\b",
)

_PM_DISCLAIMER_PHRASES = [
    r"(?i)\bnot\s+(?:a\s+)?(?:certified\s+)?(?:project\s+)?manager\b",
    r"(?i)\b(?:AI|assistant|not\s+a\s+human)\s+(?:is\s+not|cannot|does\s+not)\s+(?:replace|substitute\s+for)",
    r"(?i)\bconsult\s+(?:a\s+)?(?:certified\s+)?(?:PMP|project\s+management\s+professional|project\s+manager)\b",
    r"(?i)\bfor\s+(?:educational|informational)\s+purposes\s+(?:only|and)",
    r"(?i)\bprofessional\s+(?:judgment|advice)\s+(?:from\s+)?(?:a\s+)?(?:certified\s+)?(?:PMP|project\s+manager)\b",
]

_RISK_REGISTER_ENTRY = re.compile(
    r"(?i)\b(?:risk\s*(?::|register|log|entry|#|id|identifier)"
    r"|R-\d{3}|risk\s+identification|risk\s+analysis|risk\s+assessment)"
    r"\b",
)

_PROBABILITY_IMPACT_LANGUAGE = re.compile(
    r"(?i)\b(?:probab(?:ility|ilistic|ly)|P\d{2,3}|P-\w+|impact|severity"
    r"|likelihood|probability.{0,30}impact|risk\s+(?:score|rating|level)"
    r"|low\s+(?:probability|impact|risk)|medium\s+(?:probability|impact|risk)"
    r"|high\s+(?:probability|impact|risk)|quantitativ|qualitativ"
    r"|Monte\s+Carlo|decision\s+tree|sensitivity|tornado|expected\s+monetary\s+value|EMV"
    r")\b",
)


# ── INDIVIDUAL GRADERS ───────────────────────────────────────────────────────


def grade_change_control_process(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Verify that scope-change discussion references formal change control.

    When scope change language is detected, the text MUST also reference
    formal change control processes. Returns dict with ``pass`` (bool),
    ``reason`` (str), and ``matches`` (list).
    """
    matches: list[str] = []

    has_scope_change = bool(_SCOPE_CHANGE_LANGUAGE.search(text))
    has_change_control = bool(_CHANGE_CONTROL_LANGUAGE.search(text))

    if has_scope_change and not has_change_control:
        matches.append(
            "Scope change language detected without reference to formal change control process"
        )

    return {
        "pass": len(matches) == 0,
        "reason": "; ".join(matches)
        if matches
        else (
            "Change control process referenced alongside scope change language"
            if has_scope_change
            else "No scope change language to check"
        ),
        "matches": matches,
    }


def grade_raci_completeness(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Check that RACI matrices include proper Responsible, Accountable,
    Consulted, and Informed role assignments.

    When a RACI matrix is mentioned, ensure each activity row has at least
    one R and one A assignment. Returns dict with ``pass`` (bool),
    ``reason`` (str), and ``matches`` (list).
    """
    matches: list[str] = []

    has_raci = bool(_RACI_PATTERN.search(text))

    if not has_raci:
        return {
            "pass": True,
            "reason": "No RACI matrix found -- skipping format check",
            "matches": [],
        }

    # Find structured RACI entries (pipe or tab delimited with R/A/C/I)
    structured = _RACI_ENTRIES.findall(text)

    if structured:
        # We have structured data; validate that each row has one R and one A
        for row in structured:
            activity, *roles = row
            has_r = any(r.upper() == "R" for r in roles)
            has_a = any(r.upper() == "A" for r in roles)
            if not has_r:
                matches.append(f"RACI row '{activity.strip()[:50]}' missing Responsible (R)")
            if not has_a:
                matches.append(f"RACI row '{activity.strip()[:50]}' missing Accountable (A)")
    else:
        # Unstructured RACI mention -- check that R, A, C, I are defined
        role_mentions = set(m.upper() for m in _RACI_ROW.findall(text))
        missing_roles = [r for r in ("R", "A", "C", "I") if r not in role_mentions]
        if len(missing_roles) > 1:  # Allow one missing for brief mention
            matches.append(
                f"RACI matrix mentioned but role definitions incomplete: "
                f"missing {', '.join(sorted(missing_roles))}"
            )

    return {
        "pass": len(matches) == 0,
        "reason": "; ".join(matches) if matches else "RACI structure and assignments are complete",
        "matches": matches,
    }


def grade_pm_disclaimer_presence(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Check whether project management recommendations include a disclaimer.

    Returns dict with ``pass`` (bool), ``reason`` (str), and ``matches`` (list).
    """
    has_recommendation = bool(_PM_RECOMMENDATION_TRIGGERS.search(text))

    if not has_recommendation:
        return {
            "pass": True,
            "reason": "No PM recommendation language detected; disclaimer not required",
            "matches": [],
        }

    found_phrases: list[str] = []
    for phrase in _PM_DISCLAIMER_PHRASES:
        if re.search(phrase, text):
            found_phrases.append(phrase)

    if found_phrases:
        return {
            "pass": True,
            "reason": f"PM disclaimer present ({len(found_phrases)} component(s) matched)",
            "matches": found_phrases,
        }

    return {
        "pass": False,
        "reason": (
            "Project management recommendations detected without required "
            "scope-of-practice disclaimer. Include a statement that you are an AI "
            "assistant, not a certified PMP, and recommend consulting a certified "
            "project manager for formal project decisions."
        ),
        "matches": [],
    }


def grade_risk_description_quality(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Check that risk register entries include both probability and impact
    assessment elements (not just a label or name).

    Returns dict with ``pass`` (bool), ``reason`` (str), and ``matches`` (list).
    """
    matches: list[str] = []

    has_risk_entry = bool(_RISK_REGISTER_ENTRY.search(text))
    has_quality = bool(_PROBABILITY_IMPACT_LANGUAGE.search(text))

    if has_risk_entry and not has_quality:
        matches.append(
            "Risk register entry found without probability/impact assessment. "
            "Each risk should include probability, impact, and a risk score."
        )

    return {
        "pass": len(matches) == 0,
        "reason": "; ".join(matches)
        if matches
        else (
            "Risk entries include probability/impact assessments"
            if has_risk_entry
            else "No risk register entries to check"
        ),
        "matches": matches,
    }


# ── AGGREGATE GRADER ─────────────────────────────────────────────────────────


def grade_credential_pm(
    text: str, metadata: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    """Run all credential-pm graders and return results.

    Args:
        text: The submitted model response text.
        metadata: Optional dict with contextual info (e.g. {"context": "planning"}).

    Returns:
        List of result dicts, one per grader, each with:
            grader_id (str): unique identifier
            pass (bool): whether the check passed
            reason (str): explanation
            matches (list): matched items if applicable
    """
    graders: list[tuple[str, Any]] = [
        ("change-control-process", grade_change_control_process),
        ("raci-completeness", grade_raci_completeness),
        ("pm-disclaimer-presence", grade_pm_disclaimer_presence),
        ("risk-description-quality", grade_risk_description_quality),
    ]

    results: list[dict[str, Any]] = []
    for grader_id, grader_fn in graders:
        result = grader_fn(text, metadata)
        result["grader_id"] = grader_id
        results.append(result)

    return results
