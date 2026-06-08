"""Structured NDJSON logging — stderr ONLY.

The MCP protocol speaks JSON-RPC over stdio. Any byte written to **stdout**
that is not a valid frame corrupts the protocol. Therefore every log line goes
to **stderr** as one newline-delimited JSON object. MCP hosts forward stderr to
their own logs; it never touches the protocol stream.
"""

import json
import logging
import sys
from datetime import datetime, timezone
from logging import LogRecord

# Reserved LogRecord attributes we never want to echo into the payload.
_RESERVED = set(vars(logging.makeLogRecord({})).keys()) | {"message", "asctime"}


class StderrJsonHandler(logging.Handler):
    """Emits structured NDJSON log lines to stderr. Never to stdout."""

    def emit(self, record: LogRecord) -> None:
        try:
            payload = {
                "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
            }
            # Promote any extra={...} fields the caller attached.
            for key, val in record.__dict__.items():
                if key not in _RESERVED and not key.startswith("_"):
                    payload[key] = val
            print(json.dumps(payload, default=str), file=sys.stderr, flush=True)
        except Exception:
            self.handleError(record)


_CONFIGURED = False


def get_logger(name: str = "tutor") -> logging.Logger:
    """Return a logger wired to the stderr NDJSON handler (idempotent)."""
    global _CONFIGURED
    logger = logging.getLogger(name)
    if not _CONFIGURED:
        root = logging.getLogger("tutor")
        root.handlers.clear()
        root.addHandler(StderrJsonHandler())
        root.setLevel(logging.INFO)
        root.propagate = False  # never bubble to the root stdout handler
        _CONFIGURED = True
    return logger
