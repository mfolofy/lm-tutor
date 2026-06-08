"""`tutor mcp` — launch the MCP server (stdio) + HTTP health on :9090."""

import os


def run(args) -> int:
    from tutor.mcp.server import serve

    health_port = int(os.environ.get("TUTOR_MCP_HEALTH_PORT", "9090"))
    serve(enable_health=not getattr(args, "no_health", False), health_port=health_port)
    return 0
