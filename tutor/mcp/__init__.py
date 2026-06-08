"""MCP server package — thin wrapper around the tutor SDK.

  * server.py  — ~50-line FastMCP server exposing enroll/eval/list/health tools
  * logging.py — NDJSON to stderr ONLY (stdout would corrupt MCP stdio)
  * health.py  — HTTP health on :9090, also exposed as an MCP tool
  * metrics.py — in-memory counters + latency histograms (p99)
"""
