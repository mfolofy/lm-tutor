"""Tests for track assignment and the Booster threshold."""

from tutor.registrar.enroll import (
    HONORS,
    REMEDIAL,
    STANDARD,
    assign_track,
    booster_active,
    enroll,
)


def test_unregistered_defaults_to_remedial():
    rec = enroll("totally-unknown-model")
    assert rec["registered"] is False
    assert rec["track"] == REMEDIAL
    assert rec["booster"] is True


def test_frontier_is_honors():
    assert enroll("claude-opus-4-8")["track"] == HONORS


def test_low_tool_reliability_is_remedial():
    # gemma4 has low tool reliability -> remedial regardless of context.
    assert enroll("gemma4:latest")["track"] == REMEDIAL


def test_sub_8k_context_is_remedial():
    entry = {"capabilities": {
        "context_window": 4096,
        "tool_calling": {"reliability": "high"},
        "code_generation": {"html": "high", "python": "high"},
        "reasoning": {"cot_reliable": True, "max_reliable_steps": 6},
    }}
    assert assign_track(entry) == REMEDIAL


def test_limited_reasoning_is_standard():
    entry = {"capabilities": {
        "context_window": 128000,
        "tool_calling": {"reliability": "high"},
        "code_generation": {"html": "high", "python": "high"},
        "reasoning": {"cot_reliable": True, "max_reliable_steps": 2},
    }}
    assert assign_track(entry) == STANDARD


def test_explicit_track_override_wins():
    assert assign_track({"track": "honors"}) == "honors"


def test_alias_resolution():
    # deepseek-chat is an alias of deepseek-v4-flash.
    rec = enroll("deepseek-chat")
    assert rec["registered"] is True
    assert rec["canonical_id"] == "deepseek-v4-flash"


def test_booster_threshold():
    small = {"capabilities": {
        "context_window": 8192, "param_count_b": 8,
        "tool_calling": {"reliability": "low"},
    }}
    big = {"capabilities": {
        "context_window": 200000, "param_count_b": 400,
        "tool_calling": {"reliability": "very_high"},
    }}
    assert booster_active(small) is True
    assert booster_active(big) is False
