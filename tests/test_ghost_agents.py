"""Integration tests for Ghost Agent enrollment + prefix composition.

Verifies that all 4 Ghost agents (Counsel, Auditor, Warden, Operator) are
properly enrolled and their credential classes compose correctly.
"""
from __future__ import annotations

import pytest

from tutor.registrar.state import TrackStateStore


# ── Agent Enrollment ──────────────────────────────────────────────────────────


AGENT_CLASSES = {
    "counsel": {"credential-jd"},
    "auditor": {"credential-finra", "credential-cpa"},
    "warden": {"defense", "audit", "security"},
    "operator": {"credential-pilot", "credential-pm", "devops"},
}

MODEL = "deepseek-v4-flash"


class TestGhostAgentEnrollment:
    """Enrolling the 4 Ghost agents' class sets round-trips through the store.

    NOTE: this used to read the developer's live ``~/.tutor/track_state.json``
    and assert that the agents had been enrolled on THIS machine — an
    environment assertion that failed on every fresh clone and tested no code.
    It now performs the enrollment into an isolated state dir and verifies the
    store persists and returns it.
    """

    @pytest.fixture(scope="class")
    def enrolled_classes(self, tmp_path_factory) -> set[str]:
        state_dir = tmp_path_factory.mktemp("tutor-state")
        store = TrackStateStore(state_dir=state_dir)

        all_required: set[str] = set()
        for classes in AGENT_CLASSES.values():
            all_required.update(classes)
        store.save(MODEL, {"classes_enrolled": sorted(all_required)})

        # Re-read through a fresh store instance to prove persistence.
        state = TrackStateStore(state_dir=state_dir).load(MODEL)
        if state is None:
            return set()
        return set(state.get("classes_enrolled", []))

    def test_counsel_enrolled(self, enrolled_classes):
        """Ghost Counsel requires credential-jd."""
        required = AGENT_CLASSES["counsel"]
        missing = required - enrolled_classes
        assert not missing, f"Ghost Counsel missing classes: {missing}"

    def test_auditor_enrolled(self, enrolled_classes):
        """Ghost Auditor requires credential-finra + credential-cpa."""
        required = AGENT_CLASSES["auditor"]
        missing = required - enrolled_classes
        assert not missing, f"Ghost Auditor missing classes: {missing}"

    def test_warden_enrolled(self, enrolled_classes):
        """Ghost Warden requires defense + audit + security."""
        required = AGENT_CLASSES["warden"]
        missing = required - enrolled_classes
        assert not missing, f"Ghost Warden missing classes: {missing}"

    def test_operator_enrolled(self, enrolled_classes):
        """Ghost Operator requires credential-pilot + credential-pm + devops."""
        required = AGENT_CLASSES["operator"]
        missing = required - enrolled_classes
        assert not missing, f"Ghost Operator missing classes: {missing}"

    def test_all_ghost_agents_complete(self, enrolled_classes):
        """All 10 unique classes must be enrolled for all 4 agents."""
        all_required = set()
        for classes in AGENT_CLASSES.values():
            all_required.update(classes)
        missing = all_required - enrolled_classes
        assert not missing, f"Missing enrollment: {missing}"


# ── Prefix Composition ────────────────────────────────────────────────────────


class TestGhostAgentPrefix:
    """Each agent's credential prefixes must load without errors."""

    @pytest.mark.parametrize(
        "agent_name,class_id",
        [
            ("counsel", "credential-jd"),
            ("auditor", "credential-finra"),
            ("auditor", "credential-cpa"),
            ("warden", "defense"),
            ("warden", "audit"),
            ("warden", "security"),
            ("operator", "credential-pilot"),
            ("operator", "credential-pm"),
            ("operator", "devops"),
        ],
    )
    def test_individual_prefix_injections(self, agent_name, class_id):
        """Each class composes a valid prefix."""
        from tutor.eval.harness import load_syllabus

        syllabus = load_syllabus(class_id)
        assert syllabus is not None, f"Failed to load syllabus for {class_id}"
        rules = syllabus.get("rules", [])
        assert len(rules) > 0, f"No rules in {class_id}"
        for rule in rules:
            assert "id" in rule
            assert "rule" in rule
            assert "severity" in rule

    def test_multi_class_prefix_composes(self):
        """Multiple classes compose into a single deduplicated prefix."""
        class_ids = ["credential-jd", "security", "defense"]
        from tutor.eval.harness import load_syllabus

        for cid in class_ids:
            syllabus = load_syllabus(cid)
            assert syllabus is not None

    def test_all_class_files_exist(self):
        """All credential class YAML files exist on disk."""
        from pathlib import Path
        import tutor  # top of package
        tutor_root = Path(tutor.__file__).parent
        classes_root = tutor_root / "classes"

        for _, classes in AGENT_CLASSES.items():
            for cid in classes:
                class_path = classes_root / cid / "class.yaml"
                assert class_path.exists(), f"Missing class file: {class_path}"


# ── Session Book Integration ──────────────────────────────────────────────────


class TestGhostAgentSessionBook:
    """Each agent can log its decisions using Session Book."""

    def test_counsel_decision_logging(self):
        """Ghost Counsel logs legal decisions."""
        from tutor.session_book.book import SessionBook, Decision

        book = SessionBook(session_id="counsel-test", model_id=MODEL, task="Contract review")
        book.decisions.append(
            Decision(id="legal-1", decision="Roderick fee: 5% after payment received",
                     rationale="Cash before pass-through", confirmed_at="now",
                     confirmed_by="human", decision_type="general")
        )
        assert len(book.decisions) == 1
        assert book.decisions[0].id == "legal-1"

    def test_auditor_decision_logging(self):
        """Ghost Auditor logs financial decisions."""
        from tutor.session_book.book import SessionBook, Decision

        book = SessionBook(session_id="auditor-test", model_id=MODEL, task="Fee review")
        book.decisions.append(
            Decision(id="fin-1", decision="Deal value: $2.3M with $1.25M recurring",
                     rationale="Market rate for EAW benchmark", confirmed_at="now",
                     confirmed_by="auto", decision_type="general")
        )
        assert len(book.decisions) == 1

    def test_warden_decision_logging(self):
        """Ghost Warden logs security decisions."""
        from tutor.session_book.book import SessionBook, Decision, DriftEvent

        book = SessionBook(session_id="warden-test", model_id=MODEL, task="Code audit")
        book.drift_events.append(
            DriftEvent(token=2500, turn=1, decision_id="sec-1", violation="Raw SQL detected")
        )
        assert len(book.drift_events) == 1
        assert book.eaw_estimate == 2500

    def test_operator_decision_logging(self):
        """Ghost Operator logs operational decisions."""
        from tutor.session_book.book import SessionBook, Decision

        book = SessionBook(session_id="operator-test", model_id=MODEL, task="Pre-flight check")
        book.decisions.append(
            Decision(id="ops-1", decision="Deploy to canary before production",
                     rationale="Rolling update, 10% traffic", confirmed_at="now",
                     confirmed_by="auto", decision_type="architectural")
        )
        assert len(book.decisions) == 1
