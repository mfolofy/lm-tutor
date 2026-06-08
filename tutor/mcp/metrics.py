"""In-memory metrics — counters + latency histograms with p99.

Thread-safe, reset on process restart. No Prometheus, no external deps. Good
enough for a single-process Phase 0 deployment; the interface is stable so a
Prometheus exporter can be bolted on in Phase 2 without changing call sites.

Tracked counters include: eval.tasks, eval.passed, eval.failed, eval.error,
booster.invocations, booster.timeouts, enroll.attempts, enroll.unknown, and
per-tool mcp.tools.<name>.
"""

import threading
from collections import Counter, defaultdict
from datetime import datetime, timezone


class MetricsCollector:
    def __init__(self):
        self._lock = threading.Lock()
        self._counters: Counter = Counter()
        self._latencies: dict[str, list[float]] = defaultdict(list)
        self._start_time = datetime.now(timezone.utc)

    def incr(self, metric: str, value: int = 1) -> None:
        with self._lock:
            self._counters[metric] += value

    def record_latency(self, operation: str, seconds: float) -> None:
        with self._lock:
            vals = self._latencies[operation]
            vals.append(seconds)
            if len(vals) > 1000:  # keep only the last 1000 samples per op
                del vals[:-1000]

    def count(self, metric: str) -> int:
        with self._lock:
            return self._counters.get(metric, 0)

    def snapshot(self) -> dict:
        with self._lock:
            now = datetime.now(timezone.utc)
            uptime = (now - self._start_time).total_seconds()
            latencies = {}
            for op, vals in self._latencies.items():
                if not vals:
                    continue
                ordered = sorted(vals)
                p99_idx = min(int(len(ordered) * 0.99), len(ordered) - 1)
                latencies[op] = {
                    "count": len(ordered),
                    "avg_ms": round(sum(ordered) / len(ordered) * 1000, 3),
                    "p99_ms": round(ordered[p99_idx] * 1000, 3),
                }
            return {
                "uptime_seconds": round(uptime, 3),
                "counters": dict(self._counters),
                "latencies": latencies,
            }


# Global instance shared across the process.
metrics = MetricsCollector()
