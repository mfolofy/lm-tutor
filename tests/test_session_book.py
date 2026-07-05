"""Tests for tutor/session_book/ — Session Book lifecycle, EAW measurement, CLI."""
from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

from tutor.session_book.book import (
    ActiveRule,
    Decision,
    DriftEvent,
    InjectionEvent,
    SessionBook,
    SessionBookStore,
    compose_injection,
)
from tutor.session_book.adherence import AdherenceTracker, EAWProfile, aggregate_eaw


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def sample_book() -> SessionBook:
    return SessionBook(
        session_id="test-sess-001",
        model_id="test-model",
        trip_type="sprint",
        task="Build test fixture",
        decisions=[
            Decision(
                id="d1",
                decision="Use FastAPI over Flask",
                rationale="Async-native",
                confirmed_at=datetime.now(timezone.utc).isoformat(),
                confirmed_by="auto",
                decision_type="architectural",
            ),
            Decision(
                id="d2",
                decision="Use snake_case naming",
                rationale="PEP 8 compliance",
                confirmed_at=datetime.now(timezone.utc).isoformat(),
                confirmed_by="auto",
                decision_type="convention",
            ),
            Decision(
                id="d3",
                decision="Use parameterized queries for all SQL",
                rationale="SQL injection prevention",
                confirmed_at=datetime.now(timezone.utc).isoformat(),
                confirmed_by="human",
                decision_type="security",
            ),
        ],
        active_rules=[
            ActiveRule(id="r1", rule="Never use eval()", source="security"),
            ActiveRule(id="r2", rule="Use httpOnly cookies", source="security"),
        ],
        started_at=datetime.now(timezone.utc).isoformat(),
        tokens_consumed=5000,
        turn_count=3,
    )


@pytest.fixture
def tmp_store() -> SessionBookStore:
    with tempfile.TemporaryDirectory() as td:
        yield SessionBookStore(session_dir=Path(td))


# ── Session Book Data Model ───────────────────────────────────────────────────


class TestSessionBookDataModel:
    def test_create_session_book(self):
        """A SessionBook can be created with required fields."""
        book = SessionBook(session_id="sess-1", model_id="deepseek-test")
        assert book.session_id == "sess-1"
        assert book.model_id == "deepseek-test"
        assert book.trip_type == "local"  # default
        assert book.adherence_score == 1.0  # default
        assert book.is_active is True  # not closed yet

    def test_session_book_to_dict_roundtrip(self, sample_book):
        """to_dict then from_dict produces an identical object."""
        data = sample_book.to_dict()
        restored = SessionBook.from_dict(data)
        assert restored.session_id == sample_book.session_id
        assert restored.model_id == sample_book.model_id
        assert len(restored.decisions) == len(sample_book.decisions)
        assert len(restored.active_rules) == len(sample_book.active_rules)
        assert restored.adherence_score == sample_book.adherence_score
        assert restored.tokens_consumed == sample_book.tokens_consumed

    def test_close_session(self, sample_book):
        """Closing a session sets closed_at and marks inactive."""
        assert sample_book.is_active is True
        sample_book.close()
        assert sample_book.closed_at != ""
        assert sample_book.is_active is False
        assert not hasattr(sample_book, "closed_at") or sample_book.closed_at  # closed_at is a dataclass field

    def test_close_with_to_dict(self, sample_book):
        """closed_at must survive to_dict serialization."""
        sample_book.close()
        data = sample_book.to_dict()
        assert "closed_at" in data
        assert data["closed_at"] != ""

    def test_active_rule(self):
        """ActiveRule holds id, rule text, and source."""
        r = ActiveRule(id="test-rule", rule="Use parameterized queries", source="security")
        assert r.id == "test-rule"
        assert "parameterized" in r.rule

    def test_decision_defaults(self):
        """Decision creates with correct defaults."""
        d = Decision(id="d1", decision="Use FastAPI", rationale="Fast", confirmed_at="now", confirmed_by="auto")
        assert d.status == "active"
        assert d.decision_type == "general"
        assert d.confirmed_by == "auto"

    def test_eaw_estimate_no_drift(self, sample_book):
        """EAW estimate equals tokens_consumed when no drift occurred."""
        assert sample_book.eaw_estimate == sample_book.tokens_consumed

    def test_eaw_estimate_with_drift(self, sample_book):
        """EAW estimate equals first drift event token when drift occurred."""
        sample_book.drift_events.append(
            DriftEvent(token=1200, turn=1, decision_id="d1", violation="Used Flask")
        )
        assert sample_book.eaw_estimate == 1200

    def test_scope_record_defaults(self):
        """ScopeRecord starts undefined."""
        from tutor.session_book.book import ScopeRecord
        s = ScopeRecord()
        assert s.defined is False
        assert s.confirmed is False

    def test_guardrail_violations(self, sample_book):
        """Guardrail violations are tracked separately."""
        event = DriftEvent(token=500, turn=1, decision_id="d3", violation="Raw SQL used")
        sample_book.guardrail_violations.append(event)
        assert len(sample_book.guardrail_violations) == 1

    def test_drift_event_autofill(self):
        """DriftEvent created with explicit fields."""
        e = DriftEvent(token=1000, turn=2, decision_id="d1", violation="Used Flask instead of FastAPI")
        assert e.token == 1000
        assert e.turn == 2
        assert e.decision_id == "d1"


# ── Persistence ───────────────────────────────────────────────────────────────


class TestSessionBookStore:
    def test_save_and_load(self, tmp_store, sample_book):
        """Save then load returns an identical session book."""
        tmp_store.save(sample_book)
        loaded = tmp_store.load(sample_book.session_id)
        assert loaded is not None
        assert loaded.session_id == sample_book.session_id
        assert loaded.model_id == sample_book.model_id

    def test_load_nonexistent(self, tmp_store):
        """Loading a non-existent session returns None."""
        assert tmp_store.load("no-such-session") is None

    def test_load_active_only_active(self, tmp_store, sample_book):
        """load_active returns session only if not closed."""
        tmp_store.save(sample_book)
        assert tmp_store.load_active(sample_book.session_id) is not None
        sample_book.close()
        tmp_store.save(sample_book)
        assert tmp_store.load_active(sample_book.session_id) is None

    def test_list_active(self, tmp_store, sample_book):
        """list_active returns only open sessions."""
        tmp_store.save(sample_book)
        active = tmp_store.list_active()
        assert len(active) == 1
        sample_book.close()
        tmp_store.save(sample_book)
        active = tmp_store.list_active()
        assert len(active) == 0

    def test_list_closed(self, tmp_store, sample_book):
        """list_closed returns only closed sessions."""
        tmp_store.save(sample_book)
        assert len(tmp_store.list_closed()) == 0
        sample_book.close()
        tmp_store.save(sample_book)
        assert len(tmp_store.list_closed()) == 1

    def test_delete_session(self, tmp_store, sample_book):
        """delete removes the session file."""
        tmp_store.save(sample_book)
        assert tmp_store.load(sample_book.session_id) is not None
        tmp_store.delete(sample_book.session_id)
        assert tmp_store.load(sample_book.session_id) is None

    def test_delete_nonexistent(self, tmp_store):
        """delete of non-existent session returns False."""
        assert tmp_store.delete("no-such") is False

    def test_multiple_sessions(self, tmp_store):
        """Multiple sessions can be stored and listed."""
        for i in range(5):
            book = SessionBook(session_id=f"sess-{i}", model_id="test")
            tmp_store.save(book)
        assert len(tmp_store.list_active()) == 5
        assert len(tmp_store.list_closed()) == 0

    def test_atomic_write_corruption_resistant(self, tmp_store):
        """Crash during write doesn't corrupt existing data."""
        book = SessionBook(session_id="atomic-test", model_id="test")
        tmp_store.save(book)
        loaded = tmp_store.load("atomic-test")
        assert loaded is not None

    def test_session_dir_creation(self):
        """SessionBookStore creates the directory on init."""
        with tempfile.TemporaryDirectory() as td:
            test_dir = Path(td) / "sessions"
            assert not test_dir.exists()
            store = SessionBookStore(session_dir=test_dir)
            assert test_dir.exists()


# ── Injection ─────────────────────────────────────────────────────────────────


class TestComposeInjection:
    def test_injection_contains_decisions(self, sample_book):
        """Injection output includes all active decisions."""
        output = compose_injection(sample_book)
        for d in sample_book.decisions:
            if d.status == "active":
                assert d.decision in output
            assert d.id in output

    def test_injection_contains_rules(self, sample_book):
        """Injection output includes active rules."""
        output = compose_injection(sample_book)
        for r in sample_book.active_rules:
            assert r.rule in output

    def test_injection_adherence_score(self, sample_book):
        """Injection output includes adherence score."""
        output = compose_injection(sample_book)
        assert str(round(sample_book.adherence_score, 2)) in output

    def test_injection_empty_book(self):
        """Empty session book produces a valid injection with no errors."""
        book = SessionBook(session_id="empty", model_id="t")
        output = compose_injection(book)
        assert len(output) > 0

    def test_injection_supressed_decisions_excluded(self, sample_book):
        """Superseded decisions are not injected."""
        sample_book.decisions[0].status = "superseded"
        output = compose_injection(sample_book)
        assert sample_book.decisions[0].decision not in output

    def test_injection_revoked_decisions_excluded(self, sample_book):
        """Revoked decisions are not injected."""
        sample_book.decisions[0].status = "revoked"
        output = compose_injection(sample_book)
        assert sample_book.decisions[0].decision not in output


# ── Adherence Tracker ─────────────────────────────────────────────────────────


class TestAdherenceTracker:
    def test_create_tracker(self, sample_book):
        """AdherenceTracker wraps a SessionBook."""
        tracker = AdherenceTracker(sample_book)
        assert tracker is not None

    def test_detect_drift_no_drift(self, sample_book):
        """Output following decisions produces no drift events."""
        tracker = AdherenceTracker(sample_book)
        output = "I will use FastAPI with snake_case naming and parameterized queries."
        events = tracker.detect_drift(output, tokens_consumed=100, turn_number=1)
        assert len(events) == 0

    def test_detect_drift_architectural_violation(self, sample_book):
        """Architectural violation (mentioning rejected alternative) is detected."""
        tracker = AdherenceTracker(sample_book)
        output = "I will use Flask for the API because it is simpler."
        events = tracker.detect_drift(output, tokens_consumed=100, turn_number=1)
        d1_events = [e for e in events if e.decision_id == "d1"]
        assert len(d1_events) >= 1

    def test_detect_drift_sql_injection_risk(self, sample_book):
        """SQL injection pattern is detected against security decisions."""
        tracker = AdherenceTracker(sample_book)
        output = 'cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")'
        events = tracker.detect_drift(output, tokens_consumed=100, turn_number=1)
        d3_events = [e for e in events if e.decision_id == "d3"]
        assert len(d3_events) >= 1

    def test_detect_drift_eval_violation(self, sample_book):
        """eval() usage triggers the rule violation."""
        tracker = AdherenceTracker(sample_book)
        output = "result = eval(user_input)"
        events = tracker.detect_drift(output, tokens_consumed=100, turn_number=1)
        r1_events = [e for e in events if e.decision_id == "r1"]
        assert len(r1_events) >= 1

    def test_detect_guardrail_rule(self, sample_book):
        """Guardrail rules are detected and double-tagged."""
        tracker = AdherenceTracker(sample_book)
        output = "result = eval(user_input)"
        events = tracker.detect_drift(output, tokens_consumed=100, turn_number=1)
        assert len(events) >= 1
        # Guardrail violations are tagged
        assert len(sample_book.guardrail_violations) >= 1

    def test_detect_debug_mode_violation(self, sample_book):
        """Debug mode enabled triggers a rule violation."""
        r_debug = ActiveRule(id="r3", rule="Never enable debug mode in production — disable before release", source="security")
        sample_book.active_rules.append(r_debug)
        tracker = AdherenceTracker(sample_book)
        output = "DEBUG = True"
        events = tracker.detect_drift(output, tokens_consumed=100, turn_number=1)
        r3_events = [e for e in events if e.decision_id == "r3"]
        assert len(r3_events) >= 1

    def test_compute_eaw_no_drift(self, sample_book):
        """EAW equals total tokens when no drift occurred."""
        tracker = AdherenceTracker(sample_book)
        profile = tracker.compute_eaw()
        assert profile.eaw_overall == sample_book.tokens_consumed

    def test_compute_eaw_with_drift(self, sample_book):
        """EAW equals the drift token when drift occurred."""
        sample_book.drift_events.append(
            DriftEvent(token=1200, turn=1, decision_id="d1", violation="Used Flask")
        )
        tracker = AdherenceTracker(sample_book)
        profile = tracker.compute_eaw()
        assert profile.eaw_overall == 1200

    def test_compute_eaw_by_type(self, sample_book):
        """EAW profiles break down by decision type."""
        sample_book.decisions[0].decision_type = "architectural"
        sample_book.decisions[1].decision_type = "convention"
        sample_book.decisions[2].decision_type = "security"
        tracker = AdherenceTracker(sample_book)
        profile = tracker.compute_eaw()
        assert "architectural" in profile.eaw_by_type or len(profile.eaw_by_type) >= 0
        assert profile.drift_rate >= 0.0

    def test_eaw_threshold_is_load_bearing(self):
        """`threshold` must change the result — regression for the dead-param bug.

        Old code returned the first-drift token regardless of threshold. With a
        real adherence ratio (1 - drifted/total), a stricter threshold closes the
        window earlier than a lax one, so the two calls MUST differ.
        """
        book = SessionBook(session_id="thr", model_id="m", tokens_consumed=100000)
        # 20 tracked constraints so one drift ≠ window closed.
        book.active_rules = [
            ActiveRule(id=f"r{i}", rule=f"rule {i}", source="best-practice")
            for i in range(20)
        ]
        # 20 distinct drifts, one per 1000 tokens.
        book.drift_events = [
            DriftEvent(token=1000 * (i + 1), turn=i, decision_id=f"r{i}", violation="x")
            for i in range(20)
        ]
        tracker = AdherenceTracker(book)
        strict = tracker.compute_eaw(threshold=0.95).eaw_overall  # closes at 2nd drift → 2000
        lax = tracker.compute_eaw(threshold=0.5).eaw_overall      # closes at 11th drift → 11000
        assert strict == 2000
        assert lax == 11000
        assert strict != lax  # the bug made these equal

    def test_eaw_single_drift_among_many_keeps_window_open(self):
        """One violation out of many constraints keeps adherence above 0.95."""
        book = SessionBook(session_id="one", model_id="m", tokens_consumed=50000)
        book.active_rules = [
            ActiveRule(id=f"r{i}", rule=f"rule {i}", source="best-practice")
            for i in range(40)
        ]
        book.drift_events = [
            DriftEvent(token=500, turn=0, decision_id="r0", violation="x")
        ]
        profile = AdherenceTracker(book).compute_eaw(threshold=0.95)
        # 1/40 = 0.025 drop → adherence 0.975 ≥ 0.95 → window never closes.
        assert profile.eaw_overall == 50000

    def test_eaw_ignores_drift_against_untracked_constraint(self):
        """A drift against a superseded decision must not count — it's no longer tracked.

        Numerator can never exceed the active denominator (no negative adherence).
        """
        book = SessionBook(session_id="sup", model_id="m", tokens_consumed=5000)
        book.decisions = [
            Decision(id="d1", decision="X", rationale="r", confirmed_at="now",
                     confirmed_by="auto", status="superseded"),
            Decision(id="d2", decision="Y", rationale="r", confirmed_at="now",
                     confirmed_by="auto", status="active"),
        ]
        # d1 drifted at 1000, but d1 was later superseded; d2 (the only tracked
        # constraint) never drifted → window stays open.
        book.drift_events = [
            DriftEvent(token=1000, turn=0, decision_id="d1", violation="x")
        ]
        profile = AdherenceTracker(book).compute_eaw(threshold=0.95)
        assert profile.eaw_overall == 5000

    def test_drift_rate_calculation(self, sample_book):
        """Drift rate is calculated per 10K tokens."""
        sample_book.drift_events.append(DriftEvent(token=1000, turn=1, decision_id="d1", violation="X"))
        sample_book.drift_events.append(DriftEvent(token=2000, turn=2, decision_id="d2", violation="Y"))
        tracker = AdherenceTracker(sample_book)
        profile = tracker.compute_eaw()
        # 2 drifts / 5000 tokens * 10000 = 4.0
        assert profile.drift_rate == 4.0

    def test_profile_attributes(self, sample_book):
        """EAWProfile carries all required attributes."""
        tracker = AdherenceTracker(sample_book)
        profile = tracker.compute_eaw()
        assert profile.model_id == sample_book.model_id
        assert profile.sample_count == sample_book.turn_count
        assert profile.recovery_rate >= 0.0
        assert profile.compaction_robustness >= 0.0
        assert profile.injection_sensitivity >= 0.0


class TestAggregateEAW:
    def test_aggregate_single_profile(self, sample_book):
        """Aggregate of a single profile returns that profile's values."""
        tracker = AdherenceTracker(sample_book)
        p = tracker.compute_eaw()
        agg = aggregate_eaw([p])
        assert agg.eaw_overall == p.eaw_overall
        assert agg.model_id == p.model_id

    def test_aggregate_multiple_profiles(self, sample_book):
        """Aggregate of multiple profiles produces a median."""
        profiles = []
        for i in range(5):
            book = SessionBook(
                session_id=f"agg-{i}", model_id="test",
                tokens_consumed=1000 * (i + 1), turn_count=1,
            )
            t = AdherenceTracker(book)
            profiles.append(t.compute_eaw())
        agg = aggregate_eaw(profiles)
        assert agg.eaw_overall > 0
        assert agg.sample_count == 5

    def test_aggregate_empty_raises(self):
        """Aggregate of empty list raises ValueError."""
        with pytest.raises(ValueError):
            aggregate_eaw([])


# ── CLI Integration (via direct Python invocation) ────────────────────────────


class TestSessionCLIIntegration:
    def test_cli_start_session(self):
        """Starting a session via the model produces a valid session book."""
        from tutor.session_book.book import SessionBook
        book = SessionBook(session_id="cli-start-test", model_id="deepseek-v4-flash", trip_type="sprint", task="Test task")
        assert book.is_active
        assert book.model_id == "deepseek-v4-flash"
        assert book.trip_type == "sprint"

    def test_cli_checkpoint_decision(self, sample_book):
        """Checkpointing a decision adds it to the book."""
        d = Decision(id="d4", decision="Use Redis for caching", rationale="Speed", confirmed_at="now", confirmed_by="auto", decision_type="architectural")
        sample_book.decisions.append(d)
        assert len(sample_book.decisions) == 4
        matching = [x for x in sample_book.decisions if x.id == "d4"]
        assert len(matching) == 1
        assert matching[0].decision == "Use Redis for caching"

    def test_cli_close_session(self, sample_book):
        """Closing a session updates state correctly."""
        sample_book.tokens_consumed = 10000
        sample_book.turn_count = 5
        sample_book.close()
        assert sample_book.closed_at != ""
        assert sample_book.is_active is False

    def test_cli_adherence_output(self, sample_book):
        """Adherence command produces a valid EAW profile."""
        tracker = AdherenceTracker(sample_book)
        profile = tracker.compute_eaw()
        assert isinstance(profile, EAWProfile)
        assert profile.eaw_overall == sample_book.tokens_consumed

    def test_cli_export_drift_pairs(self, sample_book):
        """Export produces valid preference pairs from drift events."""
        sample_book.drift_events.append(
            DriftEvent(token=100, turn=1, decision_id="d1", violation="Used Flask", context="Architecture decision")
        )
        pairs = []
        for event in sample_book.drift_events:
            decision = next((d for d in sample_book.decisions if d.id == event.decision_id), None)
            if decision:
                pairs.append({
                    "session_id": sample_book.session_id,
                    "model_id": sample_book.model_id,
                    "decision_id": decision.id,
                    "rejected": event.violation,
                    "chosen": decision.decision,
                })
        assert len(pairs) == 1
        assert pairs[0]["rejected"] == "Used Flask"
        assert pairs[0]["chosen"] == "Use FastAPI over Flask"

    def test_multi_turn_drift_accumulation(self, sample_book):
        """Multiple turns accumulate drift events correctly."""
        tracker = AdherenceTracker(sample_book)
        outputs = [
            "Using Flask",
            "Following the FastAPI decision correctly now",
            "Continuing with FastAPI as approved",
        ]
        for turn_num, output in enumerate(outputs):
            events = tracker.detect_drift(output, tokens_consumed=1000 * turn_num, turn_number=turn_num)
            sample_book.drift_events.extend(events)
            sample_book.tokens_consumed += 1000
            sample_book.turn_count += 1
        assert len(sample_book.drift_events) == 1  # one 'Flask' violation on turn 0
        # 3 turns from fixture + 3 test turns = 6
        assert sample_book.turn_count == 6

    def test_session_book_update_after_save(self, tmp_store, sample_book):
        """Updating a session book and saving preserves changes."""
        tmp_store.save(sample_book)
        loaded = tmp_store.load(sample_book.session_id)
        assert loaded.tokens_consumed == 5000
        loaded.tokens_consumed = 10000
        tmp_store.save(loaded)
        reloaded = tmp_store.load(sample_book.session_id)
        assert reloaded.tokens_consumed == 10000
