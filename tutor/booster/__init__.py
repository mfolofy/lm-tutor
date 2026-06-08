"""The 8B Booster Protocol — remedial-track externalised reasoning.

Four tools (see ``tools.py``):
  * write_to_scratchpad      — run reasoning code in a sandbox (subprocess)
  * self_consistency_check   — validate assumptions as assertions in a sandbox
  * inject_few_shot          — static prompt construction (no sandbox)
  * downstream_lookahead     — static analysis (no sandbox)

Sandbox layer 1 (Phase 0): tempdir + subprocess + 30s timeout + 50MB disk
quota + semaphore (max 3 concurrent). Documented limitations: no network
isolation, no memory cap, same OS user. When the sandbox is unavailable the
sandbox-backed tools degrade to static injection with explicit logging.
"""
