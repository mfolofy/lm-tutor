"""Per-class virtual environment manager.

Each class with non-core dependencies gets its own venv, created lazily on
first use, under ``TUTOR_CLASS_VENV_DIR`` (default ``~/.tutor/venvs``). This
keeps ``pip install -e .`` lightweight (3 core deps) and prevents class A
(e.g. pillow) and class B (e.g. numpy 2.x) from conflicting.

The deeper, library-dependent grading for a class runs inside its venv via
``run_in_class_venv``. The Layer 1 happy path (``tutor eval``) never touches
this — it is stdlib-only.
"""

import os
import subprocess
import venv
from pathlib import Path

DEFAULT_VENV_DIR = Path.home() / ".tutor" / "venvs"
_CLASSES_DIR = Path(__file__).parent / "classes"


def _bin_dir(venv_path: Path) -> Path:
    return venv_path / ("Scripts" if os.name == "nt" else "bin")


class ClassVenvManager:
    """Creates and runs code inside per-class virtual environments."""

    def __init__(self, venv_dir: Path | None = None):
        if venv_dir is not None:
            self._venv_dir = Path(venv_dir)
        else:
            self._venv_dir = Path(
                os.environ.get("TUTOR_CLASS_VENV_DIR", str(DEFAULT_VENV_DIR))
            )
        self._venv_dir.mkdir(parents=True, exist_ok=True)

    def _python_path(self, venv_path: Path) -> Path:
        return _bin_dir(venv_path) / ("python.exe" if os.name == "nt" else "python")

    def ensure_class_venv(self, class_name: str) -> Path:
        """Ensure the class venv exists with its deps installed.

        Returns the path to the venv's Python executable. Uses a lock file so
        two callers don't ``pip install`` into the same venv simultaneously.
        """
        venv_path = self._venv_dir / class_name
        python_path = self._python_path(venv_path)

        if venv_path.exists() and (venv_path / "pyvenv.cfg").exists():
            return python_path

        lock_file = self._venv_dir / f"{class_name}.lock"
        with _FileLock(lock_file):
            # Re-check after acquiring the lock.
            if venv_path.exists() and (venv_path / "pyvenv.cfg").exists():
                return python_path

            venv.create(venv_path, clear=True, with_pip=True)

            req = _CLASSES_DIR / class_name / "_requirements.txt"
            if req.exists() and req.read_text(encoding="utf-8").strip():
                pip = _bin_dir(venv_path) / ("pip.exe" if os.name == "nt" else "pip")
                subprocess.run(
                    [str(pip), "install", "-r", str(req)],
                    check=True, capture_output=True, timeout=300,
                )
        return python_path

    def run_in_class_venv(self, class_name: str, module: str, args: list[str] | None = None) -> str:
        """Run ``python -m module args...`` inside the class venv; return stdout."""
        python_path = self.ensure_class_venv(class_name)
        result = subprocess.run(
            [str(python_path), "-m", module] + (args or []),
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Class venv error ({class_name}): {result.stderr[:2000]}"
            )
        return result.stdout


class _FileLock:
    """Minimal advisory lock via exclusive file creation; spins until free."""

    def __init__(self, path: Path, timeout: float = 300.0):
        self._path = path
        self._timeout = timeout
        self._fd: int | None = None

    def __enter__(self):
        import time
        start = time.monotonic()
        while True:
            try:
                self._fd = os.open(self._path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                return self
            except FileExistsError:
                if time.monotonic() - start > self._timeout:
                    # Stale lock — break it rather than hang forever.
                    try:
                        self._path.unlink()
                    except OSError:
                        pass
                time.sleep(0.2)

    def __exit__(self, *exc):
        if self._fd is not None:
            os.close(self._fd)
        try:
            self._path.unlink()
        except OSError:
            pass
