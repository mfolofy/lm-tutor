"""CLI handler for ``tutor session`` — Session Book lifecycle.

Commands:
    tutor session start         — create a new session book
    tutor session checkpoint    — freeze a confirmed decision
    tutor session inject         — output the book as injection prefix
    tutor session adherence      — show EAW profile and drift events
    tutor session close          — archive the session
    tutor session list           — list active/closed sessions
    tutor session export         — export drift data as training pairs
"""

from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from tutor.session_book import (
    ActiveRule,
    AdherenceTracker,
    Decision,
    DriftEvent,
    EAWProfile,
    SessionBook,
    SessionBookStore,
    compose_injection,
)
from tutor.registrar.state import TrackStateStore


def run(args) -> int:
    """Dispatch to the appropriate session subcommand."""
    cmd = args.session_cmd

    if cmd is None:
        print("Session subcommand required: {start,checkpoint,inject,adherence,close,list,export}")
        return 1

    dispatch = {
        "start": _cmd_start,
        "checkpoint": _cmd_checkpoint,
        "inject": _cmd_inject,
        "adherence": _cmd_adherence,
        "close": _cmd_close,
        "list": _cmd_list,
        "export": _cmd_export,
    }
    handler = dispatch.get(cmd)
    if handler is None:
        print(f"Unknown session command: {cmd}")
        return 1
    return handler(args)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_store(args) -> tuple[SessionBookStore, str | None]:
    """Get the store and optionally a session_id from args or env."""
    store = SessionBookStore()
    session_id = args.session_id or None
    # Fallback to env var (set by fleetctl)
    if session_id is None:
        session_id = _get_env_session_id()
    return store, session_id


def _get_env_session_id() -> str | None:
    """Read session ID from FLEETCTL_SESSION_ID env var (set by fleetctl hooks)."""
    import os
    return os.environ.get("FLEETCTL_SESSION_ID") or os.environ.get("TUTOR_SESSION_ID")


def _load_or_die(store: SessionBookStore, session_id: str | None) -> SessionBook:
    """Load a session book or exit with error."""
    if session_id is None:
        print("Error: no session_id provided and TUTOR_SESSION_ID not set.", file=sys.stderr)
        print("Use: tutor session start or --session-id <id>", file=sys.stderr)
        sys.exit(1)
    book = store.load(session_id)
    if book is None:
        print(f"Error: session not found: {session_id}", file=sys.stderr)
        sys.exit(1)
    return book


def _resolve_model_id() -> str:
    """Resolve model ID from various sources."""
    import os
    env_model = (
        os.environ.get("FLEETCTL_MODEL")
        or os.environ.get("TUTOR_MODEL")
        or os.environ.get("CLAUDE_MODEL")
    )
    if env_model:
        return env_model
    return "unknown"


# ── Commands ──────────────────────────────────────────────────────────────────


def _cmd_start(args) -> int:
    """Start a new session book.

    A unique session_id is generated. The book is persisted immediately.
    The session_id is printed to stdout for piping into fleetctl.
    """
    store = SessionBookStore()
    session_id = args.session_id or f"sess-{uuid.uuid4().hex[:12]}"
    model_id = args.model or _resolve_model_id()

    # Load active tutors from track state
    track_store = TrackStateStore()
    track_state = track_store.load(model_id) or {}
    enrolled_classes = track_state.get("classes_enrolled", [])

    now = datetime.now(timezone.utc).isoformat()

    book = SessionBook(
        session_id=session_id,
        model_id=model_id,
        trip_type=args.trip_type or "local",
        task=args.task or "",
        started_at=now,
        last_activity_at=now,
        enrolled_classes=enrolled_classes,
    )

    # Pre-populate active rules from enrolled classes
    # (In Phase 1, rules are added via checkpoint. In Phase 2, auto-load from class definitions.)
    # TODO: auto-load rules from enrolled class syllabi

    store.save(book)

    if args.json:
        print(json.dumps({"session_id": session_id, "status": "started"}, indent=2))
    else:
        print(f"Session started: {session_id}")
        print(f"Model: {model_id} | Trip: {book.trip_type}")

    return 0


def _cmd_checkpoint(args) -> int:
    """Freeze a confirmed decision.

    Each checkpoint locks in a decision that the agent must follow.
    Decisions are the core unit of EAW measurement.
    """
    store, session_id = _get_store(args)
    book = _load_or_die(store, session_id)

    # Require decision text
    if not args.text:
        print("Error: --text is required for checkpoint", file=sys.stderr)
        return 1

    decision_id = args.id or f"d{len(book.decisions) + 1}"

    decision = Decision(
        id=decision_id,
        decision=args.text,
        rationale=args.rationale or "",
        confirmed_at=datetime.now(timezone.utc).isoformat(),
        confirmed_by=args.by or "auto",
        decision_type=args.type or "general",
    )
    book.decisions.append(decision)
    book.last_activity_at = datetime.now(timezone.utc).isoformat()
    store.save(book)

    if args.json:
        print(json.dumps({"session_id": session_id, "decision_id": decision_id, "status": "recorded"}))
    else:
        print(f"Decision recorded: [{decision_id}] {decision.decision}")
        print(f"  Type: {decision.decision_type} | By: {decision.confirmed_by}")

    return 0


def _cmd_inject(args) -> int:
    """Output the session book as an injection prefix.

    The output is designed to be piped into an agent's system prompt or
    injected via fleetctl's compaction recovery mechanism.

    Pipe: tutor session inject | cat > injection.txt
    """
    store, session_id = _get_store(args)
    book = _load_or_die(store, session_id)

    prefix = compose_injection(book)

    if args.json:
        print(json.dumps({"session_id": session_id, "injection": prefix}, indent=2))
    else:
        print(prefix)

    return 0


def _cmd_adherence(args) -> int:
    """Show EAW profile and drift events for this session.

    This is the measurement output. Use --json for machine-readable.
    """
    store, session_id = _get_store(args)
    book = _load_or_die(store, session_id)

    tracker = AdherenceTracker(book)
    profile = tracker.compute_eaw(task_type=args.task_type)

    if args.json:
        output = {
            "session_id": session_id,
            "profile": profile.to_dict(),
            "drift_events": [e.__dict__ for e in book.drift_events],
            "injection_events": [e.__dict__ for e in book.injection_events],
            "decisions": [
                {"id": d.id, "decision": d.decision, "status": d.status, "type": d.decision_type}
                for d in book.decisions
            ],
            "guardrail_violations": len(book.guardrail_violations),
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"╔══ Session Book — {session_id}")
        print(f"║ Model: {book.model_id}")
        print(f"║ Trip:  {book.trip_type}")
        print(f"║")
        print(f"║ EAW Overall:    {profile.eaw_overall} tokens")
        print(f"║ Drift Rate:     {profile.drift_rate:.2f} / 10K tokens")
        print(f"║ Drift Events:   {len(book.drift_events)}")
        print(f"║ Adherence:      {book.adherence_score:.2f}")
        print(f"║ Turns:          {book.turn_count}")
        print(f"║ Compactions:    {book.compactions}")
        print(f"║ Handoffs:       {book.handoffs}")
        print(f"║")
        print(f"║ EAW by Decision Type:")
        for dtype, eaw in sorted(profile.eaw_by_type.items()):
            print(f"║   {dtype:20s}  {eaw:>6} tokens")
        print(f"║")
        print(f"║ Injection Sensitivity:  {profile.injection_sensitivity:.2f}")
        print(f"║ Compaction Robustness:  {profile.compaction_robustness:.2f}")
        print(f"║ Recovery Rate:          {profile.recovery_rate:.2f}")
        print(f"║ Guardrail Violations:   {len(book.guardrail_violations)}")
        print(f"╚══")

    return 0


def _cmd_close(args) -> int:
    """Archive the session book.

    Closed sessions remain on disk — they become training data.
    Export them with ``tutor session export``.
    """
    store, session_id = _get_store(args)
    book = _load_or_die(store, session_id)

    # Final adherence computation
    tracker = AdherenceTracker(book)
    profile = tracker.compute_eaw()

    # Record close
    book.close()
    book.last_activity_at = datetime.now(timezone.utc).isoformat()
    store.save(book)

    if args.json:
        print(json.dumps({
            "session_id": session_id,
            "status": "closed",
            "eaw": profile.eaw_overall,
            "drifts": len(book.drift_events),
            "tokens": book.tokens_consumed,
        }, indent=2))
    else:
        print(f"Session closed: {session_id}")
        print(f"  EAW: {profile.eaw_overall} tokens")
        print(f"  Drift events: {len(book.drift_events)}")
        print(f"  Tokens consumed: {book.tokens_consumed}")
        print(f"  → Archived as training data")

    return 0


def _cmd_list(args) -> int:
    """List active and closed sessions."""
    store = SessionBookStore()

    active = store.list_active()
    closed = store.list_closed()

    if args.json:
        print(json.dumps({
            "active": [
                {
                    "session_id": b.session_id,
                    "model": b.model_id,
                    "task": b.task,
                    "turns": b.turn_count,
                    "tokens": b.tokens_consumed,
                    "adherence": b.adherence_score,
                }
                for b in active
            ],
            "closed": [
                {
                    "session_id": b.session_id,
                    "model": b.model_id,
                    "task": b.task,
                    "turns": b.turn_count,
                    "tokens": b.tokens_consumed,
                    "decisions": len(b.decisions),
                    "drifts": len(b.drift_events),
                }
                for b in closed
            ],
        }, indent=2))
    else:
        if active:
            print("Active Sessions:")
            print(f"  {'ID':32s} {'Model':20s} {'Turns':6s} {'Tokens':8s} {'Adherence':10s}")
            print(f"  {'-'*32} {'-'*20} {'-'*6} {'-'*8} {'-'*10}")
            for b in active:
                print(f"  {b.session_id:32s} {b.model_id:20s} {b.turn_count:6d} {b.tokens_consumed:8d} {b.adherence_score:.2f}")
        else:
            print("No active sessions.")

        if closed:
            print(f"\nClosed Sessions ({len(closed)}):")
            print(f"  {'ID':32s} {'Model':20s} {'Turns':6s} {'Decisions':10s} {'Drifts':8s}")
            print(f"  {'-'*32} {'-'*20} {'-'*6} {'-'*10} {'-'*8}")
            for b in closed[-10:]:  # show last 10
                print(f"  {b.session_id:32s} {b.model_id:20s} {b.turn_count:6d} {len(b.decisions):10d} {len(b.drift_events):8d}")
        else:
            print("\nNo closed sessions.")

    return 0


def _cmd_export(args) -> int:
    """Export drift data as training preference pairs.

    Each drift event becomes a negative example. The same context with
    the decision followed becomes a positive example.

    Output format: JSONL, one pair per line:
        {"prompt": "...", "chosen": "...", "rejected": "..."}

    This is the product model providers pay for — formatted training data
    from real agent drift events.
    """
    store = SessionBookStore()

    # Load sessions — default to all closed, or filter by --session-id
    sessions: list[SessionBook] = []
    if args.session_id:
        book = store.load(args.session_id)
        if book:
            sessions.append(book)
    else:
        sessions = store.list_closed()

    if not sessions:
        print("No sessions to export.", file=sys.stderr)
        return 1

    pairs: list[dict] = []
    for book in sessions:
        for event in book.drift_events:
            # Find the decision that was violated
            decision = next(
                (d for d in book.decisions if d.id == event.decision_id),
                None,
            )
            if not decision:
                continue

            pair = {
                "session_id": book.session_id,
                "model_id": book.model_id,
                "decision_id": decision.id,
                "decision_type": decision.decision_type,
                "context": event.context,
                "rejected": event.violation,
                "chosen": decision.decision,
                "rationale": decision.rationale,
                "tokens_at_drift": event.token,
                "turn_at_drift": event.turn,
                "guardrail": event.decision_id in [g.decision_id for g in book.guardrail_violations],
            }
            pairs.append(pair)

    # Output
    output_path = args.output
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            for pair in pairs:
                f.write(json.dumps(pair) + "\n")
        print(f"Exported {len(pairs)} training pairs to {output_path}")
    else:
        # stdout
        for pair in pairs:
            print(json.dumps(pair))

    return 0
