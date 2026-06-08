# Multi-stage build for lm-tutor (The School for LLMs).
# The package is NOT on PyPI; transitive deps (mcp, pydantic, pyyaml) resolve
# from PyPI at build time and are frozen into the image layer. For air-gapped
# installs, ship this image — it needs no further network access.

# ── Builder stage ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

COPY pyproject.toml requirements.txt README.md ./
COPY tutor/ tutor/

# Install pinned transitive deps from the committed lock file...
RUN pip install --no-cache-dir -r requirements.txt
# ...then the package itself with --no-deps (deps already satisfied above,
# so pip performs no PyPI lookup for them).
RUN pip install --no-cache-dir --no-deps .

# ── Runtime stage ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Copy the resolved site-packages and console script from the builder.
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/tutor /usr/local/bin/tutor

# Health endpoint (only bound when running `tutor mcp`).
EXPOSE 9090

# Docker HEALTHCHECK hits the HTTP health endpoint exposed by `tutor mcp`.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:9090/health', timeout=3).status==200 else 1)" || exit 1

# Default to the MCP server (stdio). Override CMD for CLI usage:
#   docker run --rm -i lm-tutor eval   (then pipe a submission on stdin)
ENTRYPOINT ["tutor"]
CMD ["mcp"]
