"""Health endpoint — HTTP on :9090, also exposed as an MCP tool.

The HTTP server binds ONLY when ``start_health_server`` is called (from
``tutor mcp``). Importing this module has no side effects and opens no socket,
so ``tutor --help`` and ``tutor eval`` never touch the network.

A separate HTTP endpoint (not just an MCP tool) is deliberate: if the MCP
server is unresponsive you cannot call an MCP tool to check it, but Docker
HEALTHCHECK / K8s liveness probes can still hit ``GET /health``.
"""

import json
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from tutor import __version__
from tutor.mcp.metrics import metrics

_START = datetime.now(timezone.utc)
_REGISTRY_CACHE: dict | None = None
_REGISTRY_CACHE_TTL = 60  # seconds
_REGISTRY_CACHE_AT: float | None = None


def health_snapshot() -> dict:
    """Build the health document (used by both HTTP and the MCP tool).

    Registry read is cached with a 60-second TTL — avoids JSON re-parse on
    every Docker HEALTHCHECK (default 30s interval).
    """
    import time

    from tutor.booster.sandbox import sandbox_manager

    global _REGISTRY_CACHE, _REGISTRY_CACHE_AT

    now = time.monotonic()
    if _REGISTRY_CACHE is None or _REGISTRY_CACHE_AT is None or now - _REGISTRY_CACHE_AT > _REGISTRY_CACHE_TTL:
        try:
            from tutor.registry import load_registry
            _REGISTRY_CACHE = len([k for k in load_registry() if not k.startswith("_")])
        except Exception:
            _REGISTRY_CACHE = 0
        _REGISTRY_CACHE_AT = now

    registered = _REGISTRY_CACHE

    uptime = (datetime.now(timezone.utc) - _START).total_seconds()
    snap = metrics.snapshot()
    return {
        "status": "ok",
        "version": __version__,
        "uptime_seconds": round(uptime, 3),
        "registered_models": registered,
        "booster_sandbox": {
            "active_sessions": sandbox_manager.active_sessions,
            "max_concurrent": sandbox_manager.max_concurrent,
            "total_invocations": sandbox_manager.total_invocations,
            "total_timeouts": sandbox_manager.total_timeouts,
        },
        "metrics": snap,
    }


class _HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.rstrip("/") in ("", "/health"):
            body = json.dumps(health_snapshot(), default=str).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):  # silence stdlib stdout/stderr access logging
        pass


def start_health_server(port: int = 9090) -> ThreadingHTTPServer:
    """Start the health HTTP server on a daemon thread; return the server."""
    server = ThreadingHTTPServer(("0.0.0.0", port), _HealthHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server
