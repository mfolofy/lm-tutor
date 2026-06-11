"""The four Booster tools.

  * write_to_scratchpad(problem_code)   — sandbox-backed
  * self_consistency_check(assumptions) — sandbox-backed
  * inject_few_shot(task, examples)     — static prompt construction
  * downstream_lookahead(choice, context) — static analysis

The two sandbox-backed tools degrade gracefully when the sandbox is
unavailable (e.g. no usable interpreter): ``write_to_scratchpad`` falls back to
a static system-prompt instruction, and ``self_consistency_check`` reports that
it is unavailable. Every degradation is flagged in the returned payload so the
caller knows it happened (no silent failure).
"""

from tutor.booster.sandbox import (
    SECURITY_BOUNDARY,
    ScratchpadError,
    ScratchpadTimeout,
    sandbox_manager,
)


def write_to_scratchpad(problem_code: str) -> dict:
    """Run reasoning code in the sandbox before generating the real answer.

    Returns {"mode": "sandbox"|"static", "output"|"instruction": ...,
             "security_boundary": ...}.
    """
    try:
        output = sandbox_manager.run_in_sandbox(problem_code)
        return {
            "mode": "sandbox",
            "output": output,
            "security_boundary": SECURITY_BOUNDARY,
        }
    except (ScratchpadTimeout, ScratchpadError, OSError, ValueError) as exc:
        return {
            "mode": "static",
            "instruction": (
                "Sandbox unavailable — before generating code, write your "
                "reasoning step by step in a comment block, then verify each "
                "step against the rules."
            ),
            "reason": str(exc),
            "security_boundary": SECURITY_BOUNDARY,
        }


def self_consistency_check(assumptions: list[str]) -> dict:
    """Turn each assumption into an assertion and run them in the sandbox.

    Each assumption must be a Python boolean expression (e.g.
    ``"len('abc') == 3"``). Returns per-assumption pass/fail.
    """
    if not assumptions:
        return {"mode": "sandbox", "results": []}

    import json as _json
    lines = ["import json", "results = []"]
    for i, a in enumerate(assumptions):
        safe = _json.dumps(a)
        lines.append("try:")
        lines.append(f"    _ok = bool({a})")
        lines.append(f'    results.append({{"index": {i}, "assumption": {safe}, "passed": _ok}})')
        lines.append("except Exception as _e:")
        lines.append(f'    results.append({{"index": {i}, "assumption": {safe}, "passed": False, "error": str(_e)}})')
    lines.append("print(json.dumps(results))")
    script = "\n".join(lines)

    try:
        import json
        output = sandbox_manager.run_in_sandbox(script)
        return {"mode": "sandbox", "results": json.loads(output.strip() or "[]")}
    except (ScratchpadTimeout, ScratchpadError, OSError, ValueError) as exc:
        return {
            "mode": "unavailable",
            "reason": str(exc),
            "note": "self_consistency_check requires the sandbox; not available.",
        }


def inject_few_shot(task: str, examples: list[dict] | None = None) -> dict:
    """Static prompt construction — no sandbox.

    ``examples`` is a list of {"fail": "...", "pass": "..."} dicts. Returns a
    formatted few-shot block ready to prepend to a generation prompt.
    """
    examples = examples or []
    blocks = []
    for ex in examples:
        fail = ex.get("fail", "")
        good = ex.get("pass", "")
        blocks.append(f"// FAIL\n{fail}\n// PASS\n{good}")
    prompt = f"Task: {task}\n\nFollow these worked examples:\n\n" + "\n\n".join(blocks)
    return {"mode": "static", "few_shot_prompt": prompt, "example_count": len(examples)}


def downstream_lookahead(choice: str, context: str = "") -> dict:
    """Static analysis — predict edge cases ~50 lines ahead from a choice.

    Phase 0 is a heuristic stub: it surfaces a checklist of common downstream
    consequences keyed off the kind of choice. No code execution.
    """
    choice_l = choice.lower()
    considerations: list[str] = []
    if any(k in choice_l for k in ("loop", "for ", "while ", "iterate")):
        considerations.append("empty-collection case (zero iterations)")
        considerations.append("off-by-one on the final element")
    if any(k in choice_l for k in ("dict", "map", "lookup", "key", "[")):
        considerations.append("missing-key / KeyError path")
    if any(k in choice_l for k in ("await", "async", "promise", "fetch")):
        considerations.append("rejection / network-failure path")
    if any(k in choice_l for k in ("input", "form", "user", "param", "arg")):
        considerations.append("untrusted-input validation and escaping")
    if any(k in choice_l for k in ("button", "<a", "aria", "role", "img", "label")):
        considerations.append("accessibility: name, role, keyboard reachability")
    if not considerations:
        considerations.append("define the failure mode for this choice explicitly")
    return {
        "mode": "static",
        "choice": choice,
        "context_hint": context[:200],
        "edge_cases_to_handle": considerations,
    }
