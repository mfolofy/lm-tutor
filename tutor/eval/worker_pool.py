"""Persistent worker pool for the eval harness.

Process isolation without the per-call cold-start tax. Workers are forked
(POSIX) / spawned (Windows) ONCE at ``start()`` and kept alive, each
pre-importing the harness and looping on a task queue.

This is used by the **benchmark** and **MCP server** paths, where many
evaluations are amortised over a long-lived process. The one-shot
``tutor eval`` CLI does NOT use the pool — it calls
``tutor.eval.harness.grade`` directly in-process, which is both faster and
deterministic for a single grade (important on Windows/3.14 where spawn
re-imports the main module).

Worker target ``_worker_loop`` is importable at module level so spawn can
pickle it; do not nest it inside another function.
"""

import multiprocessing
import os

DEFAULT_POOL_SIZE = 2
TASK_TIMEOUT = 60  # seconds


def _worker_loop(task_queue: "multiprocessing.Queue", result_queue: "multiprocessing.Queue") -> None:
    """Child-process loop. Pre-imports the harness once, then grades on demand.

    Tasks are ``(seq, submission, syllabus)``. Results are
    ``(seq, result_dict_or_error)``. A ``None`` task is the shutdown sentinel.
    """
    from tutor.eval.harness import grade  # heavy import, once per worker

    while True:
        task = task_queue.get()
        if task is None:
            break
        seq, submission, syllabus = task
        try:
            result = grade(submission, syllabus)
            result_queue.put((seq, {"ok": True, "result": result.model_dump()}))
        except Exception as exc:  # never let a worker die on a bad submission
            result_queue.put((seq, {"ok": False, "error": str(exc)}))


class EvalTimeout(Exception):
    pass


class PoolManager:
    """Manages a pool of forked/spawned worker processes."""

    def __init__(self, pool_size: int | None = None):
        self._pool_size = pool_size or int(
            os.environ.get("TUTOR_EVAL_POOL_SIZE", DEFAULT_POOL_SIZE)
        )
        self._ctx = multiprocessing.get_context()
        self._queue: multiprocessing.Queue | None = None
        self._result_queue: multiprocessing.Queue | None = None
        self._workers: list[multiprocessing.Process] = []
        self._seq = 0

    def start(self) -> None:
        """Fork/spawn the worker pool. Call once at process start."""
        self._queue = self._ctx.Queue()
        self._result_queue = self._ctx.Queue()
        self._workers = []
        for _ in range(self._pool_size):
            p = self._ctx.Process(
                target=_worker_loop,
                args=(self._queue, self._result_queue),
                daemon=True,
            )
            p.start()
            self._workers.append(p)

    def grade(self, submission: str, syllabus: str = "brushes", timeout: float = TASK_TIMEOUT) -> dict:
        """Send one grade task to the pool and block for its result."""
        if self._queue is None or self._result_queue is None:
            raise RuntimeError("PoolManager.start() not called")
        self._seq += 1
        my_seq = self._seq
        self._queue.put((my_seq, submission, syllabus))
        try:
            seq, payload = self._result_queue.get(timeout=timeout)
        except Exception as exc:
            raise EvalTimeout(f"eval exceeded {timeout}s") from exc
        return payload

    @property
    def workers_alive(self) -> int:
        return sum(1 for w in self._workers if w.is_alive())

    def shutdown(self, wait: bool = True) -> None:
        """Send the sentinel to every worker, then optionally join."""
        if self._queue is None:
            return
        for _ in self._workers:
            self._queue.put(None)
        if wait:
            for w in self._workers:
                w.join(timeout=10)
