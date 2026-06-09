"""
credential-socialworker grader — multi-line and contextual checks for social work rules.

Layer 2 validations that require cross-text analysis beyond single-line regex.

Current graders:
  - confidentiality-exception-present: After a match on confidentiality, verifies
    that the text also addresses at least one recognized exception (mandatory
    reporting, court order, etc.) — ensuring the model does not merely flag
    concerns but also teaches the exception framework.
  - client-voice-ratio: Checks that advocacy language centers client voice
    (client-directed phrasing) rather than practitioner-directed phrasing —
    addressing the "advocate with, not for" principle from NASW 6.01.
  - self-determination-documentation: When a limiting context (court order,
    child welfare mandate) is detected, verifies that the model explains the
    limits of self-determination rather than simply overriding it.

Usage (called by the Layer 1 harness after regex checks pass):
    from tutor.classes.credential_socialworker.grader import grade_credential_socialworker
    results = grade_credential_socialworker(submission_text, metadata={})
"""

from __future__ import annotations

import re
from typing import Any

# ── CONFIDENTIALITY EXCEPTION PATTERNS ──────────────────────────────────────

CONFIDENTIALITY_EXCEPTION_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?i)\b(?:exception|except|unless|however|but|limited|override)\b"),
    re.compile(r"(?i)\b(danger|harm|threat|abuse|neglect|imminent|safety)\b"),
    re.compile(r"(?i)\b(mandatory\s+report|child\s+abuse|elder\s+abuse|cps|aps)\b"),
    re.compile(r"(?i)\b(court\s+order|subpoena|legal\s+mandate|duty\s+to\s+protect)\b"),
    re.compile(r"(?i)\b(disclose\s+only\s+what|minimum\s+necessary|reasonably\s+necessary)\b"),
]

# ── CLIENT VOICE PATTERNS ───────────────────────────────────────────────────

# Phrases where the social worker centers their own authority
WORKER_DIRECTED_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?i)\bI\s+(?:will|am\s+going\s+to)\s+(?:advocate|speak|talk|file|call|arrange|set\s+up)\b"),
    re.compile(r"(?i)\blet\s+me\s+(?:handle|take\s+care\s+of|do\s+it|advocate)\b"),
    re.compile(r"(?i)\bI\s+(?:know|understand)\s+what\s+you\s+need\b"),
]

# Phrases where the social worker centers client choice/voice
CLIENT_DIRECTED_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?i)\bhow\s+would\s+you\s+like\s+to\s+proceed\b"),
    re.compile(r"(?i)\bwhat\s+(?:do\s+you|would\s+you|are\s+your)\b"),
    re.compile(r"(?i)\b(?:with\s+your\s+)?(?:consent|permission|input|direction|choice|decision)\b"),
    re.compile(r"(?i)\bI\s+can\s+(?:help\s+you|work\s+with\s+you|support\s+you|assist\s+you)\b"),
]

# ── SELF-DETERMINATION LIMITING CONTEXT ─────────────────────────────────────

LIMITING_CONTEXT_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?i)\b(court\s+order|judge\s+ordered|court\s+mandated|legal\s+requirement)\b"),
    re.compile(r"(?i)\b(child\s+welfare|foster\s+care|cps|protective\s+custody|safety\s+plan)\b"),
    re.compile(r"(?i)\b(mandatory|required\s+by\s+law|legal\s+obligation|non\s*-*negotiable)\b"),
]

EXPLANATION_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?i)\b(?:however|although|while|even\s+though|but)\s+(?:\w+\s+){0,5}(?:choice|self-determination|decision|input|decision-making)\b"),
    re.compile(r"(?i)\byou\s+(?:still|can\s+still|get\s+to|have\s+choices\s+within|have\s+a\s+voice)\b"),
    re.compile(r"(?i)\bI\s+will\s+(?:explain|clarify|discuss)\s+(?:what|how|the\s+limits|your\s+options|the\s+choices)\b"),
]


def grade_confidentiality_exceptions(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Grade whether confidentiality discussion includes exception language.

    When a submission discusses confidentiality, it should also reference at
    least one recognized exception framework — otherwise the model teaches
    absolute confidentiality, which is inaccurate in social work contexts.

    Returns a dict with ``pass`` (bool), ``reason`` (str), and ``exceptions``
    (list of matched exception references).
    """
    exceptions_found: list[str] = []

    for pattern in CONFIDENTIALITY_EXCEPTION_PATTERNS:
        m = pattern.search(text)
        if m:
            exceptions_found.append(m.group())

    if not exceptions_found:
        return {
            "pass": False,
            "reason": (
                "Confidentiality discussion lacks reference to exceptions. "
                "Must address at least one: mandatory reporting, danger to "
                "self/others, child/elder abuse, or court order."
            ),
            "exceptions": [],
        }

    return {
        "pass": True,
        "reason": f"Confidentiality exceptions referenced: {exceptions_found[:3]}",
        "exceptions": exceptions_found[:5],
    }


def grade_client_voice_ratio(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Grade whether advocacy language centers client voice.

    Compares worker-directed phrasing against client-directed phrasing.
    If worker-directed phrases exceed client-directed, the text may be
    advocating *for* rather than *with* the client, contravening NASW 6.01.

    Returns a dict with ``pass`` (bool), ``reason`` (str), and counts.
    """
    worker_count = sum(1 for p in WORKER_DIRECTED_PATTERNS if p.search(text))
    client_count = sum(1 for p in CLIENT_DIRECTED_PATTERNS if p.search(text))

    if worker_count > 0 and client_count == 0:
        return {
            "pass": False,
            "reason": (
                f"Advocacy language is worker-directed ({worker_count} patterns) "
                f"with no client-directed phrasing. Add language that centers "
                f"client choice: 'how would you like to proceed?', 'with your permission...'"
            ),
            "worker_directed": worker_count,
            "client_directed": client_count,
        }

    if worker_count > client_count + 1:
        return {
            "pass": False,
            "reason": (
                f"Advocacy language skews worker-directed ({worker_count} patterns) "
                f"vs. client-directed ({client_count}). Consider centering client "
                f"voice more."
            ),
            "worker_directed": worker_count,
            "client_directed": client_count,
        }

    return {
        "pass": True,
        "reason": (
            f"Client voice ratio acceptable: "
            f"{client_count} client-directed, {worker_count} worker-directed."
        ),
        "worker_directed": worker_count,
        "client_directed": client_count,
    }


def grade_self_determination_explanation(
    text: str, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Grade whether limited contexts (court order, child welfare mandate) include
    an explanation of remaining self-determination.

    When a text references legal mandates that limit client choice, the model
    should also explain what decisions remain within the client's authority.

    Returns a dict with ``pass`` (bool), ``reason`` (str), and details.
    """
    limiting_contexts = [
        m.group().lower() for p in LIMITING_CONTEXT_PATTERNS for m in p.finditer(text)
    ]

    if not limiting_contexts:
        return {
            "pass": True,
            "reason": "No limiting context detected; self-determination not tested.",
            "limiting_contexts": [],
            "explanations_found": [],
        }

    explanations_found = [
        m.group().lower() for p in EXPLANATION_PATTERNS for m in p.finditer(text)
    ]

    if not explanations_found:
        return {
            "pass": False,
            "reason": (
                f"Limiting context detected ({limiting_contexts[:3]}) but no "
                f"explanation of remaining client choices. When legal mandates "
                f"limit self-determination, explain what decisions remain in the "
                f"client's authority."
            ),
            "limiting_contexts": limiting_contexts[:5],
            "explanations_found": [],
        }

    return {
        "pass": True,
        "reason": (
            f"Self-determination limits acknowledged with explanation: "
            f"{explanations_found[:3]}"
        ),
        "limiting_contexts": limiting_contexts[:5],
        "explanations_found": explanations_found[:3],
    }


# ── AGGREGATE GRADER ──────────────────────────────────────────────────────


def grade_credential_socialworker(
    text: str, metadata: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    """Run all credential-socialworker graders and return results.

    Args:
        text: The submitted model response text.
        metadata: Optional dict with contextual info.

    Returns:
        List of result dicts, one per grader, each with:
            grader_id (str): unique identifier
            pass (bool): whether the check passed
            reason (str): explanation
            + grader-specific fields
    """
    results: list[dict[str, Any]] = []

    conf_result = grade_confidentiality_exceptions(text, metadata)
    conf_result["grader_id"] = "confidentiality-exception-present"
    results.append(conf_result)

    voice_result = grade_client_voice_ratio(text, metadata)
    voice_result["grader_id"] = "client-voice-ratio"
    results.append(voice_result)

    sd_result = grade_self_determination_explanation(text, metadata)
    sd_result["grader_id"] = "self-determination-explanation"
    results.append(sd_result)

    return results
