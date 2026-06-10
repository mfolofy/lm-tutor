"""Tests for the Booster sandbox resource limits.

Regression coverage for the disk-quota bug: MAX_DISK_BYTES must bound what the
sandboxed script *writes*, not just the script source. The pre-run check alone
let a runaway fill the disk unbounded — the exact "excessive output" case the
limit exists to bound.

Run with: pytest tests/test_booster_sandbox.py
"""

import pytest

from tutor.booster.sandbox import (
    ScratchpadQuotaExceeded,
    ScratchpadSandbox,
)


def test_happy_path_returns_stdout() -> None:
    with ScratchpadSandbox() as sbx:
        out = sbx.run("print('hello from sandbox')")
    assert "hello from sandbox" in out


def test_runaway_disk_write_is_killed_by_quota() -> None:
    """A script that writes past MAX_DISK_BYTES must be killed mid-run, not
    allowed to fill the disk. This is the core regression."""
    script = (
        "with open('big.bin', 'wb') as f:\n"
        "    chunk = b'A' * (1024 * 1024)\n"
        "    while True:\n"
        "        f.write(chunk)\n"
        "        f.flush()\n"
    )
    with ScratchpadSandbox() as sbx:
        sbx.MAX_DISK_BYTES = 4 * 1024 * 1024  # tighten so the test is fast
        with pytest.raises(ScratchpadQuotaExceeded):
            sbx.run(script)


def test_oversized_script_source_rejected_before_run() -> None:
    with ScratchpadSandbox() as sbx:
        sbx.MAX_DISK_BYTES = 1024
        with pytest.raises(ScratchpadQuotaExceeded):
            sbx.run("# pad\n" + ("x = 1  # filler\n" * 500))
