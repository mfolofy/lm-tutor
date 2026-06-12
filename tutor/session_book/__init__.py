"""Session Book — per-session decision freeze + adherence measurement.

Every autonomous agent session produces a Session Book: a snapshot of confirmed
decisions, active steering rules, and a running adherence score. The book is
re-injected on compaction to prevent drift. Drift events are captured as labeled
data for the training pipeline.

Public API:
    SessionBook        — core dataclass: decisions, rules, drift events, scores
    SessionBookStore   — atomic JSON persistence to ``~/.tutor/sessions/``
    AdherenceTracker   — compare decisions vs output, compute EAW
    compose_injection  — format the book as a prompt injection prefix
"""

from tutor.session_book.book import SessionBook, SessionBookStore, compose_injection, Decision, ActiveRule, DriftEvent
from tutor.session_book.adherence import AdherenceTracker, EAWProfile

__all__ = [
    "SessionBook",
    "SessionBookStore",
    "AdherenceTracker",
    "EAWProfile",
    "Decision",
    "ActiveRule",
    "DriftEvent",
    "compose_injection",
]
