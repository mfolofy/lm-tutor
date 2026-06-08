"""MCP server — thin FastMCP wrapper around the tutor SDK (~50 lines of body).

Exposes the same SDK the CLI uses: enroll, eval, list_classes, health, and the
Booster tools. Logging goes to stderr (NDJSON); stdout is reserved for the
JSON-RPC protocol frames.
"""

import time

from mcp.server.fastmcp import FastMCP

from tutor.cli.eval import infer_syllabus, list_classes
from tutor.eval import grade
from tutor.mcp.health import health_snapshot
from tutor.mcp.logging import get_logger
from tutor.mcp.metrics import metrics
from tutor.registrar.enroll import enroll as _enroll

logger = get_logger("tutor.mcp")
mcp = FastMCP("lm-tutor")


@mcp.tool()
def enroll(model_id: str) -> dict:
    """Enroll a model by id; returns its curriculum track and Booster status."""
    metrics.incr("mcp.tools.enroll")
    metrics.incr("enroll.attempts")
    record = _enroll(model_id)
    if not record["registered"]:
        metrics.incr("enroll.unknown")
    logger.info("enroll", extra={"event": "enroll", "model_id": model_id, "track": record["track"]})
    return record


@mcp.tool()
def eval_submission(submission: str, class_name: str | None = None) -> dict:
    """Grade a submission with the Layer 1 rules engine. Syllabus auto-inferred."""
    metrics.incr("mcp.tools.eval_submission")
    metrics.incr("eval.tasks")
    syllabus = class_name or infer_syllabus(submission)
    start = time.monotonic()
    try:
        result = grade(submission, syllabus)
    except Exception as exc:
        metrics.incr("eval.error")
        logger.error("eval.error", extra={"event": "eval.error", "error": str(exc)})
        return {"error": str(exc)}
    metrics.record_latency("eval", time.monotonic() - start)
    metrics.incr("eval.passed" if result.passed else "eval.failed")
    return result.model_dump()


@mcp.tool()
def list_available_classes() -> list[dict]:
    """List the classes available in this tutor build."""
    metrics.incr("mcp.tools.list_available_classes")
    return list_classes()


@mcp.tool()
def health() -> dict:
    """Health snapshot: uptime, registered models, sandbox + eval metrics."""
    metrics.incr("mcp.tools.health")
    return health_snapshot()


def serve(enable_health: bool = True, health_port: int = 9090) -> None:
    """Run the MCP server over stdio, optionally with the HTTP health endpoint."""
    if enable_health:
        from tutor.mcp.health import start_health_server
        start_health_server(health_port)
        logger.info("health.start", extra={"event": "health.start", "port": health_port})
    logger.info("mcp.start", extra={"event": "mcp.start"})
    mcp.run()  # stdio transport
