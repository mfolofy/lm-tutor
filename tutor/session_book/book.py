"""SessionBook — data model + atomic JSON persistence.

Design follows the ``TrackStateStore`` pattern in ``registrar/state.py``:
atomic writes via tmp → os.replace, thread-safe, crash-recovery safe.

Schema versioned at ``FORMAT_VERSION`` for forward compatibility of archived
session books used as training data.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ── Schema ────────────────────────────────────────────────────────────────────

FORMAT_VERSION = 1

SESSION_DIR_ENV = "TUTOR_SESSION_DIR"
DEFAULT_SESSION_DIR = Path.home() / ".tutor" / "sessions"


@dataclass
class Decision:
    """A confirmed decision that the agent must follow."""

    id: str
    decision: str                         # e.g. "Use FastAPI over Flask"
    rationale: str                        # why the decision was made
    confirmed_at: str                     # ISO-8601
    confirmed_by: str                     # "human" | "reviewer" | "auto"
    status: str = "active"                # "active" | "superseded" | "revoked"

    # Decision type classification for EAW measurement
    decision_type: str = "general"        # "architectural" | "convention" | "security" | "naming" | "general"


@dataclass
class ActiveRule:
    """A steering rule injected from a tutor class."""

    id: str
    rule: str                             # e.g. "Use parameterized queries only"
    source: str                           # class name, e.g. "security"


@dataclass
class DriftEvent:
    """A detected drift: the model violated a confirmed decision or rule."""

    token: int                            # cumulative token count at drift
    turn: int                             # turn number
    decision_id: str                      # which decision/rule was violated
    violation: str                        # what the model did instead
    context: str = ""                     # snippet of what triggered it
    detected_at: str = ""                 # ISO-8601, auto-filled


@dataclass
class InjectionEvent:
    """Record of a context injection event (compaction recovery or cadence)."""

    token: int
    turn: int
    injection_type: str                   # "compaction_recovery" | "cadence" | "manual"
    decisions_reinjected: list[str]       # decision IDs that were re-injected
    rules_reinjected: int = 0             # count of rules re-injected


@dataclass
class ScopeRecord:
    """Scope-of-work tracking from fleetctl."""

    defined: bool = False
    confirmed: bool = False
    artifact: str = ""
    task: str = ""


@dataclass
class SessionBook:
    """Per-session record of decisions, rules, drift, and adherence."""

    session_id: str
    model_id: str
    trip_type: str = "local"
    task: str = ""

    # Decisions locked in during this session
    decisions: list[Decision] = field(default_factory=list)
    active_rules: list[ActiveRule] = field(default_factory=list)
    enrolled_classes: list[str] = field(default_factory=list)

    # Scope
    scope: ScopeRecord = field(default_factory=ScopeRecord)

    # Session timing
    started_at: str = ""                  # ISO-8601
    last_activity_at: str = ""            # ISO-8601
    turn_count: int = 0
    tokens_consumed: int = 0
    wall_clock_minutes: int = 0

    # Compaction / handoff tracking
    compactions: int = 0
    handoffs: int = 0

    # Events
    drift_events: list[DriftEvent] = field(default_factory=list)
    injection_events: list[InjectionEvent] = field(default_factory=list)

    # Compliance
    adherence_score: float = 1.0          # running score [0, 1]
    deviation_count: int = 0
    escalation_stage: str = "normal"      # normal | warned | restricted | blocked

    # Metrics
    total_rules: int = 0
    rules_followed: int = 0
    rules_violated: int = 0

    # Schema
    format_version: int = FORMAT_VERSION
    closed_at: str = ""                   # ISO-8601, set on close()

    # Guardrail reinforcements captured
    guardrail_violations: list[DriftEvent] = field(default_factory=list)

    @property
    def eaw_estimate(self) -> int:
        """Rough EAW estimate: last drift token or tokens_consumed, whichever is lower."""
        if not self.drift_events:
            return self.tokens_consumed
        return min(e.token for e in self.drift_events)

    @property
    def is_active(self) -> bool:
        """Session is active if it has no close timestamp."""
        return not self.closed_at

    def close(self) -> None:
        """Mark session as closed. Persisted on next save()."""
        self.closed_at = datetime.now(timezone.utc).isoformat()
        self.last_activity_at = self.closed_at

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> SessionBook:
        decisions = [Decision(**dec) for dec in d.get("decisions", [])]
        active_rules = [ActiveRule(**r) for r in d.get("active_rules", [])]
        drift_events = [DriftEvent(**e) for e in d.get("drift_events", [])]
        injection_events = [InjectionEvent(**e) for e in d.get("injection_events", [])]
        guardrail_violations = [DriftEvent(**e) for e in d.get("guardrail_violations", [])]

        scope = ScopeRecord(**d.get("scope", {}))

        book = cls(
            session_id=d["session_id"],
            model_id=d.get("model_id", "unknown"),
            trip_type=d.get("trip_type", "local"),
            task=d.get("task", ""),
            decisions=decisions,
            active_rules=active_rules,
            enrolled_classes=d.get("enrolled_classes", []),
            scope=scope,
            started_at=d.get("started_at", ""),
            last_activity_at=d.get("last_activity_at", ""),
            turn_count=d.get("turn_count", 0),
            tokens_consumed=d.get("tokens_consumed", 0),
            wall_clock_minutes=d.get("wall_clock_minutes", 0),
            compactions=d.get("compactions", 0),
            handoffs=d.get("handoffs", 0),
            drift_events=drift_events,
            injection_events=injection_events,
            adherence_score=d.get("adherence_score", 1.0),
            deviation_count=d.get("deviation_count", 0),
            escalation_stage=d.get("escalation_stage", "normal"),
            total_rules=d.get("total_rules", 0),
            rules_followed=d.get("rules_followed", 0),
            rules_violated=d.get("rules_violated", 0),
            guardrail_violations=guardrail_violations,
        )
        if d.get("format_version"):
            book.format_version = d["format_version"]
        if d.get("closed_at"):
            book.closed_at = d["closed_at"]
        return book


# ── Persistence ───────────────────────────────────────────────────────────────


class SessionBookStore:
    """Atomic JSON persistence for Session Books.

    Each active session is stored at ``~/.tutor/sessions/{session_id}.json``.
    Closed sessions remain — they are the training data archive.

    Thread-safe (per-operation lock). Atomic writes via tmp → os.replace.
    """

    def __init__(self, session_dir: Path | None = None):
        if session_dir is not None:
            self._session_dir = Path(session_dir)
        else:
            self._session_dir = Path(
                os.environ.get(SESSION_DIR_ENV, str(DEFAULT_SESSION_DIR))
            )
        self._session_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    @property
    def session_dir(self) -> Path:
        return self._session_dir

    def save(self, book: SessionBook) -> None:
        """Atomically persist a session book."""
        with self._lock:
            path = self._session_dir / f"{book.session_id}.json"
            tmp = path.with_suffix(".json.tmp")
            tmp.write_text(
                json.dumps(book.to_dict(), indent=2, default=str),
                encoding="utf-8",
            )
            os.replace(tmp, path)

    def load(self, session_id: str) -> SessionBook | None:
        """Load a session book by ID, or None."""
        with self._lock:
            path = self._session_dir / f"{session_id}.json"
            if not path.exists():
                return None
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                return SessionBook.from_dict(data)
            except (json.JSONDecodeError, OSError, KeyError):
                return None

    def load_active(self, session_id: str) -> SessionBook | None:
        """Load the currently active session (checks if not closed)."""
        book = self.load(session_id)
        if book is None:
            return None
        if book.closed_at:
            return None
        return book

    def list_active(self) -> list[SessionBook]:
        """List all currently active session books."""
        books = []
        with self._lock:
            for path in self._session_dir.glob("*.json"):
                try:
                    data = json.loads(path.read_text(encoding="utf-8"))
                    if not data.get("closed_at"):
                        books.append(SessionBook.from_dict(data))
                except (json.JSONDecodeError, OSError, KeyError):
                    continue
        return books

    def list_closed(self) -> list[SessionBook]:
        """List all archived (closed) session books — usable as training data."""
        books = []
        with self._lock:
            for path in self._session_dir.glob("*.json"):
                try:
                    data = json.loads(path.read_text(encoding="utf-8"))
                    if data.get("closed_at"):
                        books.append(SessionBook.from_dict(data))
                except (json.JSONDecodeError, OSError, KeyError):
                    continue
        return books

    def delete(self, session_id: str) -> bool:
        """Remove a session book. Returns True if deleted."""
        with self._lock:
            path = self._session_dir / f"{session_id}.json"
            if path.exists():
                path.unlink()
                return True
            return False


# ── Injection ─────────────────────────────────────────────────────────────────


def compose_injection(book: SessionBook) -> str:
    """Format the session book as a prompt injection prefix.

    Re-injects active decisions + rules. Excludes drift events (those are
    measurement data, not steering).
    """
    lines: list[str] = []

    # Header
    lines.append(f"# Session Book — {book.session_id}")
    lines.append(f"Model: {book.model_id} | Trip: {book.trip_type}")
    if book.task:
        lines.append(f"Task: {book.task}")
    lines.append(f"Adherence: {book.adherence_score:.2f} | Turns: {book.turn_count}")
    lines.append("")

    # Active decisions
    active = [d for d in book.decisions if d.status == "active"]
    if active:
        lines.append("## Active Confirmed Decisions")
        for d in active:
            lines.append(f"  - [DECISION {d.id}] {d.decision}")
            lines.append(f"    Rationale: {d.rationale}")
            lines.append(f"    Confirmed by: {d.confirmed_by}")
        lines.append("")

    # Active rules
    if book.active_rules:
        lines.append("## Active Steering Rules")
        for r in book.active_rules:
            lines.append(f"  [RULE {r.id}] {r.rule}")
        lines.append("")

    # Scope reminder
    if book.scope.defined and not book.scope.confirmed:
        lines.append("## ⚠ Scope defined but not yet confirmed")
        lines.append(f"  Task: {book.scope.task}")
        lines.append("")

    # Adherence pulse
    lines.append(f"## Adherence: {book.adherence_score:.2f}")
    if book.drift_events:
        lines.append(f"  Drift events logged: {len(book.drift_events)}")
        lines.append(f"  EAW estimate: {book.eaw_estimate} tokens")
    if book.deviation_count > 0:
        lines.append(f"  Deviations: {book.deviation_count}")
    lines.append("")

    return "\n".join(lines)
