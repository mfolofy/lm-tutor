"""
credential-hr grader — computation-heavy checks for HR/employment law rules.

Layer 2 validations that require cross-text analysis beyond single-line regex.

Current graders:
  - disclaimer-presence: Verifies that model outputs containing HR
    recommendations include a scope-of-practice disclaimer (AI cannot replace
    HR professionals, cannot make hiring/firing decisions).
  - termination-process-review: Checks that termination discussions include
    references to proper process (documentation, notice, COBRA, final pay,
    unemployment eligibility).
  - accommodation-interactive-process: Verifies that ADA accommodation
    discussions reference the interactive process and individualized assessment.
  - discipline-progression: Confirms that discipline discussions reference
    progressive discipline or PIP before termination.
  - layoff-warn-check: Checks that mass layoff discussions (50+ employees)
    reference WARN Act 60-day notice requirements.

Usage (called by the Layer 1 harness after regex checks pass):
    from tutor.classes.credential_hr.grader import grade_credential_hr
    results = grade_credential_hr(submission_text, metadata={})
"""

from __future__ import annotations

import re
from typing import Any


# ── HELPER PATTERNS ──────────────────────────────────────────────────────────

_HR_ADVICE_TRIGGERS = re.compile(
    r"(?i)\b(?:hire|fire|terminate|discipline|suspend|promote|demote|recruit|"
    r"interview|background\s+check|performance\s+(?:review|improvement|plan|"
    r"evaluation)|lay\s+off|reduce\s+(?:workforce|headcount|staff)|"
    r"employee\s+(?:handbook|policy|relation|grievance)|"
    r"compensation|salary|wage|benefit|leave\s+of\s+absence|"
    r"accommodat(?:e|ion)|reasonable\s+accommodation|"
    r"investigat(?:e|ion|ing)\s+(?:complaint|harassment|grievance))\b",
)

_REQUIRED_DISCLAIMER_PHRASES = [
    r"(?i)\bnot\s+(?:a\s+)?(?:HR\s+)?(?:professional|representative|manager|practitioner|specialist)\b",
    r"(?i)\b(?:AI|assistant|I\s+am\s+an?\s+AI)\s+(?:cannot|is\s+not|does\s+not|should\s+not)\s+(?:replace|substitute\s+for)\b",
    r"(?i)\bconsult\s+(?:with\s+)?(?:your\s+)?(?:HR\s+)?(?:department|professional|representative|attorney|legal\s+counsel)\b",
    r"(?i)\bfor\s+(?:educational|informational)\s+purposes\s+(?:only|and\s+should)|\bnot\s+(?:legal|employment)\s+advice\b",
    r"(?i)\brecommend\s+(?:consulting|speaking\s+with)\s+(?:a|an|your)\s+(?:qualified|licensed|experienced)\s+(?:HR|employment\s+law|attorney)\b",
    r"(?i)\bfinal\s+(?:hiring|firing|employment)\s+(?:decisions?|authority)\s+(?:rest\w+\s+with|reside\w+\s+with|belong\w+\s+to)\s+(?:human\s+)?(?:management|leadership|HR|the\s+company)\b",
]

_TERMINATION_LANGUAGE = re.compile(
    r"(?i)\b(?:terminat(?:e|ion|ing)|fire|dismiss(?:al)?|let\s+(?:go|them\s+go)|"
    r"separat(?:e|ion|ing)|end\s+(?:employment|the\s+relationship)|"
    r"RIF|reduction\s+in\s+force|lay\s+off|downsize|right-?size)\b",
)

_TERMINATION_PROCESS_ELEMENTS = [
    r"(?i)\bdocument\w*\s+(?:the\s+)?(?:issue|performance|behavior|incident|concern)\b",
    r"(?i)\b(?:written\s+)?(?:warning|notice)\s+(?:period|of\s+termination|letter)\b",
    r"(?i)\bCOBRA\b",
    r"(?i)\bfinal\s+(?:pay(?:check)?|wage|salary|compensation)\b",
    r"(?i)\bunemployment\s+(?:insurance|compensation|benefits?|claim)\b",
    r"(?i)\b(?:exit\s+interview|return\s+(?:of\s+)?(?:company\s+)?property)\b",
]

_ACCOMMODATION_LANGUAGE = re.compile(
    r"(?i)\b(?:accommodat(?:e|ion|ing)|reasonable\s+accommodation|"
    r"disability\s+(?:accommodation|request)|modification|"
    r"accessible|assistive\s+(?:technology|device)|"
    r"ergonomic|workplace\s+adjustment|flexible\s+(?:schedule|work|arrangement)"
    r"|leave\s+as\s+(?:an?\s+)?(?:accommodation|ADA))\b",
)

_INTERACTIVE_PROCESS_LANGUAGE = re.compile(
    r"(?i)\b(?:interactive\s+process|individualized\s+(?:assessment|analysis|inquiry)|"
    r"engage\s+(?:in\s+)?(?:a\s+)?(?:good\s+)?(?:faith\s+)?(?:interactive\s+)?(?:process|"
    r"dialogue|discussion|conversation)|"
    r"explore\s+(?:potential|possible|reasonable)\s+accommodation|"
    r"discuss\s+(?:the\s+)?(?:employee'?s?\s+)?(?:limitation|need|restriction|functional\s+"
    r"limitation)|"
    r"consult\s+(?:with\s+)?(?:the\s+)?(?:employee|doctor|healthcare\s+provider))\b",
)

_UNDUE_HARDSHIP_LANGUAGE = re.compile(
    r"(?i)\b(?:undue\s+hardship|significant\s+(?:difficulty|expense|cost)|"
    r"accommodation\s+(?:would|may|might)\s+(?:pose|create|cause)\s+(?:an?\s+)?(?:undue|"
    r"significant)|"
    r"disruption\s+(?:to\s+)?(?:operations|business|workplace)|"
    r"direct\s+threat\s+(?:to\s+)?(?:safety|health))\b",
)

_DISCIPLINE_LANGUAGE = re.compile(
    r"(?i)\b(?:discipline|disciplinary\s+(?:action|process|procedure|policy|measure)|"
    r"write-?up|written\s+(?:warning|reprimand)|verbal\s+(?:warning|counseling)|"
    r"corrective\s+(?:action|counseling|measure|step)|"
    r"progressive\s+(?:discipline|disciplinary)\b|"
    r"performance\s+improvement\s+(?:plan|program|process))\b",
)

_PROGRESSIVE_DISCIPLINE_LANGUAGE = re.compile(
    r"(?i)\b(?:progressive\s+discipline|progressive\s+disciplinary\s+(?:process|action)|"
    r"step(?:s|ped|ping)\s+(?:of\s+)?(?:progressive\s+)?discipline|"
    r"verbal\s+(?:warning|counseling).{0,50}written\s+(?:warning|reprimand)|"
    r"written\s+(?:warning|reprimand).{0,50}suspen|"
    r"performance\s+improvement\s+(?:plan|program).{0,100}(?:terminat|fire|dismiss)|"
    r"escalat(?:e|ion|ing)\s+(?:discipline|disciplinary\s+(?:action|process)))\b",
)

_MASS_LAYOFF_TRIGGERS = re.compile(
    r"(?i)\b(?:mass\s+(?:layoff|firing|termination|reduction)|"
    r"plant\s+(?:closing|closure|shutdown)|"
    r"facility\s+(?:closure|closing|shutdown)|"
    r"lay\s+off\s+(?:\d+\s*\+?\s*|\d+\s*[-–]\s*\d+\s*)?(?:employee|worker|person|staff)"
    r"|reduce\s+(?:workforce|headcount|staff(?:ing)?)\s+(?:by\s+)?(?:\d+|"
    r"(?:almost|over|more\s+than|nearly|approximately|about)\s+\d+)"
    r"|eliminat(?:e|ion)\s+of\s+(?:\d+|many)\s+(?:position|job|role))\b",
)

_WARN_LANGUAGE = re.compile(
    r"(?i)\b(?:WARN\s+(?:Act|notice|requirements?|notification)|"
    r"Worker\s+Adjustment\s+and\s+Retraining\s+Notification|"
    r"60[-\s]day\s+(?:notice|advance\s+(?:notice|warning)|notification|period)|"
    r"advance\s+(?:notice|warning|notification)\s+of\s+(?:plant\s+)?(?:closing|"
    r"closure|layoff)|"
    r"(?:plant|facility)\s+(?:closing|closure).{0,100}(?:60|sixty)\s+day|"
    r"dislocated\s+worker|rapid\s+response\s+(?:team|service))\b",
)


# ── INDIVIDUAL GRADERS ───────────────────────────────────────────────────────


def grade_disclaimer_presence(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Grade whether HR recommendations include a scope-of-practice disclaimer.

    An AI assistant providing HR guidance must include a clear statement that
    it is not an HR professional, cannot make hiring/firing decisions, and
    recommends consulting qualified HR or legal counsel.

    Returns dict with ``pass`` (bool), ``reason`` (str), and ``matches`` (list).
    """
    has_advice = bool(_HR_ADVICE_TRIGGERS.search(text))

    if not has_advice:
        return {
            "pass": True,
            "reason": "No HR employment-relations language detected; disclaimer not required",
            "matches": [],
        }

    found_phrases: list[str] = []
    for phrase in _REQUIRED_DISCLAIMER_PHRASES:
        if re.search(phrase, text):
            found_phrases.append(phrase)

    if found_phrases:
        return {
            "pass": True,
            "reason": f"HR scope-of-practice disclaimer present ({len(found_phrases)} component(s) matched)",
            "matches": found_phrases,
        }

    return {
        "pass": False,
        "reason": (
            "HR employment-relations recommendations detected without required "
            "scope-of-practice disclaimer. Include a statement that you are an AI "
            "assistant, not an HR professional, cannot make hiring or firing decisions, "
            "and recommend consulting qualified HR professionals or employment counsel "
            "for binding personnel decisions."
        ),
        "matches": [],
    }


def grade_termination_process(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Check that termination discussions reference proper process elements.

    When an AI discusses termination, it should reference: documentation, notice,
    COBRA, final pay, unemployment eligibility, and property return.

    Returns dict with ``pass`` (bool), ``reason`` (str), ``matches`` (list).
    """
    matches: list[str] = []

    has_termination = bool(_TERMINATION_LANGUAGE.search(text))

    if not has_termination:
        return {
            "pass": True,
            "reason": "No termination language detected; process check not required",
            "matches": [],
        }

    found_elements: list[str] = []
    for element in _TERMINATION_PROCESS_ELEMENTS:
        if re.search(element, text):
            found_elements.append(element)

    if len(found_elements) < 2:
        matches.append(
            f"Termination discussion lacks sufficient process references "
            f"(found {len(found_elements)}/6 expected elements: documentation, "
            f"notice/warning, COBRA, final pay, unemployment, exit process)"
        )

    return {
        "pass": len(matches) == 0,
        "reason": "; ".join(matches)
        if matches
        else (
            f"Termination process includes {len(found_elements)} process element(s) "
            f"(COBRA, final pay, notice, documentation, etc.)"
        ),
        "matches": found_elements,
    }


def grade_accommodation_interactive_process(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Verify accommodation discussions reference the interactive process
    and individualized assessment.

    When an ADA accommodation is discussed, the text MUST reference:
    - The interactive process or individualized assessment
    - Undue hardship as a potential limitation (not an automatic denial)

    Returns dict with ``pass`` (bool), ``reason`` (str), and ``matches`` (list).
    """
    matches: list[str] = []

    has_accommodation = bool(_ACCOMMODATION_LANGUAGE.search(text))

    if not has_accommodation:
        return {
            "pass": True,
            "reason": "No accommodation language detected; interactive process check skipped",
            "matches": [],
        }

    has_interactive = bool(_INTERACTIVE_PROCESS_LANGUAGE.search(text))
    has_undue_hardship = bool(_UNDUE_HARDSHIP_LANGUAGE.search(text))

    if not has_interactive:
        matches.append(
            "Accommodation discussion missing reference to the ADA interactive process. "
            "Employers must engage in a good-faith interactive process with the employee "
            "to identify effective reasonable accommodations."
        )

    return {
        "pass": len(matches) == 0,
        "reason": "; ".join(matches)
        if matches
        else (
            "Interactive process referenced in accommodation discussion"
            + ("; undue hardship considerations noted" if has_undue_hardship else "")
        ),
        "matches": [],
    }


def grade_discipline_progression(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Check that discipline discussions follow progressive discipline before
    termination.

    When an AI discusses employee discipline, it should reference progressive
    discipline or PIP as steps before termination, not skip directly to firing.

    Returns dict with ``pass`` (bool), ``reason`` (str), and ``matches`` (list).
    """
    matches: list[str] = []

    has_discipline = bool(_DISCIPLINE_LANGUAGE.search(text))
    has_progressive = bool(_PROGRESSIVE_DISCIPLINE_LANGUAGE.search(text))

    if not has_discipline:
        return {
            "pass": True,
            "reason": "No discipline language detected; progression check not required",
            "matches": [],
        }

    if not has_progressive:
        matches.append(
            "Discipline discussion lacks reference to progressive discipline or a "
            "performance improvement plan. Standard practice is to follow progressive "
            "steps: verbal warning, written warning, suspension/PIP, then termination "
            "if improvement is not demonstrated."
        )

    return {
        "pass": len(matches) == 0,
        "reason": "; ".join(matches) if matches else "Progressive discipline or PIP referenced",
        "matches": [],
    }


def grade_layoff_warn(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Check that mass layoff discussions reference WARN Act 60-day notice
    requirements.

    When mass layoff or plant closing language is detected (50+ employees),
    the text MUST reference WARN Act advance notice obligations.

    Returns dict with ``pass`` (bool), ``reason`` (str), and ``matches`` (list).
    """
    matches: list[str] = []

    has_mass_layoff = bool(_MASS_LAYOFF_TRIGGERS.search(text))
    has_warn = bool(_WARN_LANGUAGE.search(text))

    if not has_mass_layoff:
        return {
            "pass": True,
            "reason": "No mass layoff / plant closing language detected; WARN check not required",
            "matches": [],
        }

    if not has_warn:
        matches.append(
            "Mass layoff or plant closing language detected without reference to the "
            "WARN Act. The Worker Adjustment and Retraining Notification Act requires "
            "60 calendar days advance written notice for plant closings and mass layoffs "
            "affecting 50+ employees (or 33% of workforce, minimum 50) at a single site."
        )

    return {
        "pass": len(matches) == 0,
        "reason": "; ".join(matches) if matches else "WARN Act requirements referenced",
        "matches": [],
    }


# ── AGGREGATE GRADER ─────────────────────────────────────────────────────────


def grade_credential_hr(
    text: str, metadata: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    """Run all credential-hr graders and return results.

    Args:
        text: The submitted model response text.
        metadata: Optional dict with contextual info (e.g. {"context": "termination"}).

    Returns:
        List of result dicts, one per grader, each with:
            grader_id (str): unique identifier
            pass (bool): whether the check passed
            reason (str): explanation
            matches (list): matched items if applicable
    """
    graders: list[tuple[str, Any]] = [
        ("disclaimer-presence", grade_disclaimer_presence),
        ("termination-process", grade_termination_process),
        ("accommodation-interactive-process", grade_accommodation_interactive_process),
        ("discipline-progression", grade_discipline_progression),
        ("layoff-warn-check", grade_layoff_warn),
    ]

    results: list[dict[str, Any]] = []
    for grader_id, grader_fn in graders:
        result = grader_fn(text, metadata)
        result["grader_id"] = grader_id
        results.append(result)

    return results
