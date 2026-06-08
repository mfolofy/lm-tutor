"""Crash-recovery state store.

Atomic-write JSON to ``~/.tutor/track_state.json`` (override the directory with
``TUTOR_STATE_DIR``). Each save writes a temp file then ``os.replace`` over the
target — atomic on POSIX, near-atomic on NTFS — so a crash mid-write never
leaves a partial state file.

Phase 0: single-process only. Concurrent writes from multiple tutor processes
on the same machine are not protected against (documented limitation).
"""

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_STATE_DIR = Path.home() / ".tutor"


class TrackStateStore:
    """Persists enrollment and class progress to a JSON file, keyed by model id."""

    def __init__(self, state_dir: Path | None = None):
        if state_dir is not None:
            self._state_dir = Path(state_dir)
        else:
            self._state_dir = Path(
                os.environ.get("TUTOR_STATE_DIR", str(DEFAULT_STATE_DIR))
            )
        self._state_dir.mkdir(parents=True, exist_ok=True)
        self._state_file = self._state_dir / "track_state.json"
        self._lock = threading.Lock()

    @property
    def state_file(self) -> Path:
        return self._state_file

    def save(self, model_id: str, state: dict) -> None:
        """Atomically persist ``state`` for ``model_id`` with a fresh timestamp."""
        with self._lock:
            all_states = self._load_all_unlocked()
            all_states[model_id] = {
                **state,
                "last_updated": datetime.now(timezone.utc).isoformat(),
            }
            tmp = self._state_file.with_suffix(".json.tmp")
            tmp.write_text(
                json.dumps(all_states, indent=2, default=str),
                encoding="utf-8",
            )
            os.replace(tmp, self._state_file)  # atomic swap

    def load(self, model_id: str) -> dict | None:
        """Return the last checkpoint for ``model_id``, or None."""
        with self._lock:
            return self._load_all_unlocked().get(model_id)

    def load_all(self) -> dict:
        with self._lock:
            return self._load_all_unlocked()

    def _load_all_unlocked(self) -> dict:
        if self._state_file.exists():
            try:
                return json.loads(self._state_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                # Corrupt or unreadable state — start fresh rather than crash.
                return {}
        return {}
