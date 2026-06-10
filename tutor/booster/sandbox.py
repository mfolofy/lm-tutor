"""Booster sandbox — Layer 1 (tempdir + subprocess + resource limits).

SECURITY BOUNDARY (documented, surfaced verbatim in tool descriptions):
    This runs model-provided code in a subprocess with disk and timeout limits.
    It does NOT provide network isolation, memory limits, or container-level
    security. The subprocess runs as the same OS user as the tutor process.
    Do not execute untrusted code from unauthenticated sources. The threat
    model here is accidental infinite loops or excessive output, not
    adversarial escape.

Layers 2 (container per session) and 3 (Firecracker microVM) are designed in
docs/designs/devops-architecture.md but not built in Phase 0.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

SECURITY_BOUNDARY = (
    "Security boundary: runs code in a subprocess with disk and timeout "
    "limits only. No network isolation, no memory cap, same OS user. Not "
    "safe for untrusted code. Threat model: accidental infinite loops / "
    "excessive output, not adversarial escape."
)


class ScratchpadError(Exception):
    """Base sandbox error. ``code`` is a machine-parseable error identifier."""

    def __init__(self, message: str = "", code: str = "SANDBOX_ERROR"):
        self.code = code
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


class ScratchpadTimeout(ScratchpadError):
    def __init__(self, message: str = ""):
        super().__init__(message, code="SANDBOX_TIMEOUT")


class ScratchpadQuotaExceeded(ScratchpadError):
    def __init__(self, message: str = ""):
        super().__init__(message, code="SANDBOX_QUOTA_EXCEEDED")


class ScratchpadSandbox:
    """A single-use subprocess runner with a tempdir jail and resource limits."""

    MAX_DISK_BYTES = 50 * 1024 * 1024   # 50 MB
    MAX_DURATION_SECONDS = 30
    MAX_STDOUT_BYTES = 1 * 1024 * 1024  # 1 MB

    def __init__(self):
        self._tmpdir: Path | None = None
        self._start_time: float | None = None

    def __enter__(self) -> "ScratchpadSandbox":
        self._tmpdir = Path(tempfile.mkdtemp(prefix="tutor_booster_"))
        self._start_time = time.monotonic()
        return self

    def __exit__(self, *exc):
        if self._tmpdir and self._tmpdir.exists():
            shutil.rmtree(self._tmpdir, ignore_errors=True)
        self._tmpdir = None

    def _dir_size(self) -> int:
        """Bytes currently used by the tempdir jail."""
        if self._tmpdir is None:
            return 0
        return sum(
            f.stat().st_size for f in self._tmpdir.rglob("*") if f.is_file()
        )

    def run(self, script: str, interpreter: str | None = None) -> str:
        """Write ``script`` to the tempdir, run it, return stdout.

        Raises ScratchpadTimeout / ScratchpadQuotaExceeded / ScratchpadError.
        """
        if self._tmpdir is None:
            raise RuntimeError("Use 'with ScratchpadSandbox() as sbx:'")
        interpreter = interpreter or sys.executable

        script_path = self._tmpdir / "scratchpad_script.py"
        script_path.write_text(script, encoding="utf-8")

        if self._dir_size() > self.MAX_DISK_BYTES:
            raise ScratchpadQuotaExceeded(
                f"Scratchpad script exceeds {self.MAX_DISK_BYTES} bytes before run"
            )

        proc = subprocess.Popen(
            [interpreter, str(script_path)],
            cwd=self._tmpdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
        )

        # Enforce the disk quota *during* execution. The pre-run check only sees
        # the script source; without this a runaway that writes to its cwd blows
        # past MAX_DISK_BYTES unbounded — the exact "excessive output" case the
        # limit is meant to bound. Poll the jail and kill the process if it
        # exceeds the cap.
        quota_hit = threading.Event()

        def _watch() -> None:
            while proc.poll() is None:
                if self._dir_size() > self.MAX_DISK_BYTES:
                    quota_hit.set()
                    proc.kill()
                    return
                time.sleep(0.25)

        watcher = threading.Thread(target=_watch, daemon=True)
        watcher.start()

        try:
            stdout, stderr = proc.communicate(timeout=self.MAX_DURATION_SECONDS)
        except subprocess.TimeoutExpired:
            proc.kill()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pass
            raise ScratchpadTimeout(
                f"Scratchpad exceeded {self.MAX_DURATION_SECONDS}s limit"
            )
        finally:
            watcher.join(timeout=1)

        if quota_hit.is_set():
            raise ScratchpadQuotaExceeded(
                f"Scratchpad exceeded {self.MAX_DISK_BYTES} bytes during run"
            )

        if len(stdout) > self.MAX_STDOUT_BYTES:
            stdout = stdout[: self.MAX_STDOUT_BYTES] + b"\n... (truncated)"

        if proc.returncode != 0:
            raise ScratchpadError(
                f"Scratchpad exited code {proc.returncode}:\n"
                f"{stderr.decode('utf-8', errors='replace')[:2000]}"
            )
        return stdout.decode("utf-8", errors="replace")


class SandboxManager:
    """Bounds concurrent sandbox calls with a semaphore (default max 3)."""

    DEFAULT_MAX_CONCURRENT = 3
    QUEUE_TIMEOUT = 60

    def __init__(self):
        max_c = int(
            os.environ.get(
                "TUTOR_BOOSTER_MAX_CONCURRENT", self.DEFAULT_MAX_CONCURRENT
            )
        )
        self._semaphore = threading.Semaphore(max_c)
        self._max_concurrent = max_c
        self._active = 0
        self._lock = threading.Lock()
        self.total_invocations = 0
        self.total_timeouts = 0

    @property
    def active_sessions(self) -> int:
        return self._active

    @property
    def max_concurrent(self) -> int:
        return self._max_concurrent

    def run_in_sandbox(self, script: str) -> str:
        """Run ``script`` in a fresh sandbox, respecting the concurrency cap."""
        if not self._semaphore.acquire(timeout=self.QUEUE_TIMEOUT):
            raise ScratchpadError("All sandbox slots busy — try again later")
        with self._lock:
            self._active += 1
            self.total_invocations += 1
        try:
            with ScratchpadSandbox() as sbx:
                return sbx.run(script)
        except ScratchpadTimeout:
            with self._lock:
                self.total_timeouts += 1
            raise
        finally:
            with self._lock:
                self._active -= 1
            self._semaphore.release()


# Global instance shared by Booster tool handlers.
sandbox_manager = SandboxManager()
