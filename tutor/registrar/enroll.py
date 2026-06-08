"""Enrollment: registry lookup + track assignment.

Track is a FUNCTION of the capability profile, never a stored field.

Rules (from SCOPE.md and the build spec):

  * Unregistered model                              -> remedial (conservative)
  * Unreliable tool calling OR context < 8K         -> remedial
  * Reliable multi-step reasoning (>= 4 steps)
        AND high code generation across languages   -> honors
  * Everything else                                 -> standard

An explicit ``track`` in overrides.json wins over the computed value (manual
escape hatch), but the default behaviour computes the track from capabilities.

The Booster activates on a multi-factor working-memory score:

    score = 0.4 * context_factor + 0.4 * param_factor + 0.2 * tool_factor

    context_factor = min(context_window, 32768) / 32768
    param_factor   = log2(param_count_b) / log2(400)   (clamped to [0, 1])
    tool_factor    = {very_high:1.0, high:0.8, medium:0.5, low:0.2}

Booster is active when score < BOOSTER_THRESHOLD (default 0.65).
"""

import math

from tutor.registry import resolve_model

REMEDIAL = "remedial"
STANDARD = "standard"
HONORS = "honors"

UNKNOWN_MODEL_TRACK = REMEDIAL
BOOSTER_THRESHOLD = 0.65

_TOOL_RELIABILITY_SCORE = {
    "very_high": 1.0,
    "high": 0.8,
    "medium": 0.5,
    "low": 0.2,
}
_UNRELIABLE_TOOL = {"low"}


def _code_gen_all_high(code_gen: dict) -> bool:
    levels = code_gen.values()
    return bool(levels) and all(level == "high" for level in levels)


def assign_track(entry: dict) -> str:
    """Compute the curriculum track from a capability profile.

    ``entry`` is a registry entry dict. If it carries an explicit ``track``
    field (from overrides), that wins.
    """
    if "track" in entry:
        return entry["track"]

    caps = entry.get("capabilities", {})
    reasoning = caps.get("reasoning", {})
    tool = caps.get("tool_calling", {})
    code_gen = caps.get("code_generation", {})

    context_window = caps.get("context_window", 0)
    tool_reliability = tool.get("reliability", "low")
    max_steps = reasoning.get("max_reliable_steps", 0)
    cot_reliable = reasoning.get("cot_reliable", False)

    # Remedial gate: unreliable tools OR sub-8K context.
    if tool_reliability in _UNRELIABLE_TOOL or context_window < 8192:
        return REMEDIAL

    # Honors gate: reliable 4+ step reasoning AND high code gen everywhere.
    if cot_reliable and max_steps >= 4 and _code_gen_all_high(code_gen):
        return HONORS

    return STANDARD


def working_memory_score(entry: dict) -> float:
    """Compute the Booster activation score in [0, 1]."""
    caps = entry.get("capabilities", {})
    context_window = caps.get("context_window", 0)
    param_count = caps.get("param_count_b", 0)
    tool_reliability = caps.get("tool_calling", {}).get("reliability", "low")

    context_factor = min(context_window, 32768) / 32768
    if param_count > 0:
        param_factor = min(math.log2(param_count) / math.log2(400), 1.0)
    else:
        param_factor = 0.0
    tool_factor = _TOOL_RELIABILITY_SCORE.get(tool_reliability, 0.2)

    return 0.4 * context_factor + 0.4 * param_factor + 0.2 * tool_factor


def booster_active(entry: dict, threshold: float = BOOSTER_THRESHOLD) -> bool:
    """True if the Booster should be active for this model."""
    return working_memory_score(entry) < threshold


def enroll(model_id: str) -> dict:
    """Enroll a model. Returns an enrollment record.

    {
      "model_id": "...",          # as supplied
      "canonical_id": "..." | None,
      "registered": bool,
      "tier": "...",
      "track": "remedial|standard|honors",
      "booster": bool,
      "working_memory_score": float,
    }
    """
    resolved = resolve_model(model_id)
    if resolved is None:
        return {
            "model_id": model_id,
            "canonical_id": None,
            "registered": False,
            "tier": "unknown",
            "track": UNKNOWN_MODEL_TRACK,
            "booster": True,  # remedial default => booster on
            "working_memory_score": 0.0,
        }

    canonical_id, entry = resolved
    track = assign_track(entry)
    score = working_memory_score(entry)
    # Booster only matters on remedial/standard; honors never uses it.
    booster = track != HONORS and booster_active(entry)
    return {
        "model_id": model_id,
        "canonical_id": canonical_id,
        "registered": True,
        "tier": entry.get("tier", "unknown"),
        "track": track,
        "booster": booster,
        "working_memory_score": round(score, 4),
    }
