"""Eval history logger — append-only JSONL per model.

Every ``tutor eval`` call appends a record to
``~/.tutor/evals/<model_id>.jsonl`` so we can track per-model pass rates
over time, identify weak rules, and feed the profile command.

Format (one JSON object per line):

  {"timestamp": ISO-8601, "model": str, "class": str,
   "passed": bool, "rules_checked": int, "violations": [{"rule": str, ...}],
   "syllabus": str}

Thread-safe via per-model file locking (Lock per model_id).
"""

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tutor.eval.harness import EvalResult

DEFAULT_STATE_DIR = Path.home() / ".tutor"


class EvalHistory:
    """Append-only JSONL eval history, one file per model."""

    def __init__(self, state_dir: Path | None = None):
        if state_dir is not None:
            self._state_dir = Path(state_dir)
        else:
            self._state_dir = Path(
                os.environ.get("TUTOR_STATE_DIR", str(DEFAULT_STATE_DIR))
            )
        self._evals_dir = self._state_dir / "evals"
        self._evals_dir.mkdir(parents=True, exist_ok=True)
        self._locks: dict[str, threading.Lock] = {}
        self._locks_lock = threading.Lock()

    def _lock_for(self, model_id: str) -> threading.Lock:
        with self._locks_lock:
            if model_id not in self._locks:
                self._locks[model_id] = threading.Lock()
            return self._locks[model_id]

    def _path_for(self, model_id: str) -> Path:
        safe = model_id.replace("/", "_").replace(":", "_")
        return self._evals_dir / f"{safe}.jsonl"

    def record(self, model_id: str, result: EvalResult | dict) -> None:
        """Append one eval result to the model's history file."""
        if isinstance(result, EvalResult):
            result = result.model_dump()

        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": model_id,
            "class": result.get("syllabus", result.get("class", "?")),
            "passed": result.get("passed", False),
            "rules_checked": result.get("rules_checked", 0),
            "violation_count": len(result.get("violations", [])),
            "violations": [
                {
                    "rule": v.get("rule", "?"),
                    "severity": v.get("severity", "fundamental"),
                }
                for v in (result.get("violations") or [])
            ],
            "error": result.get("error"),
        }

        path = self._path_for(model_id)
        lock = self._lock_for(model_id)
        with lock:
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, default=str) + "\n")

    def load(self, model_id: str) -> list[dict]:
        """Return all eval history records for a model, oldest first."""
        path = self._path_for(model_id)
        if not path.exists():
            return []
        records: list[dict] = []
        lock = self._lock_for(model_id)
        with lock:
            for line in path.read_text(encoding="utf-8").strip().split("\n"):
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return records

    def per_class_pass_rates(self, model_id: str) -> dict[str, dict]:
        """Aggregate pass rates per class.

        Returns {class_name: {"attempts": N, "passes": N, "pass_rate": float}}
        """
        records = self.load(model_id)
        counts: dict[str, dict] = {}
        for r in records:
            cls_name = r.get("class", "?")
            if cls_name not in counts:
                counts[cls_name] = {"attempts": 0, "passes": 0}
            counts[cls_name]["attempts"] += 1
            if r.get("passed"):
                counts[cls_name]["passes"] += 1

        for cls_name, data in counts.items():
            data["pass_rate"] = (
                round(data["passes"] / data["attempts"], 3)
                if data["attempts"] > 0
                else 0.0
            )
        return counts

    def weakest_rules(self, model_id: str, top_n: int = 5) -> list[dict]:
        """Return the N most-failed rules for a model, sorted by failure count."""
        records = self.load(model_id)
        counts: dict[str, dict] = {}
        for r in records:
            for v in (r.get("violations") or []):
                rule = v.get("rule", "?")
                if rule not in counts:
                    counts[rule] = {"failures": 0}
                counts[rule]["failures"] += 1

        sorted_rules = sorted(
            counts.items(), key=lambda x: x[1]["failures"], reverse=True
        )
        return [
            {"rule": rule, "failures": data["failures"]}
            for rule, data in sorted_rules[:top_n]
        ]

    def total_evals(self, model_id: str) -> int:
        """Total number of eval records for a model."""
        return len(self.load(model_id))
