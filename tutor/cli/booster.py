"""`tutor booster` — CLI access to the 4 Booster tools.

Booster tools are designed for small models (remedial track). They give the
model structured support: sandboxed reasoning, consistency verification,
few-shot exemplars, and downstream edge-case prediction.

Before Phase 1 this was Python-API only (``import tutor.booster.tools``).
These CLI wrappers let the model call them as subprocess tools.
"""

import json
import sys


def run_scratchpad(args) -> int:
    """``tutor booster scratchpad`` — run reasoning code in the sandbox.

    Reads the code from stdin (pipe-friendly). Returns the sandbox output
    as JSON on stdout.
    """
    from tutor.booster.tools import write_to_scratchpad

    code = sys.stdin.read()
    if not code.strip():
        print(json.dumps({"error": "No code provided. Pipe code to stdin."}))
        return 1

    result = write_to_scratchpad(code)
    print(json.dumps(result, indent=2, default=str))
    return 0


def run_verify(args) -> int:
    """``tutor booster verify <assumption> [<assumption> ...]``

    Each assumption must be a Python boolean expression. The sandbox runs
    them as assertions and returns per-assumption pass/fail.
    """
    from tutor.booster.tools import self_consistency_check

    if not args.assumptions:
        print(json.dumps({"error": "No assumptions given. Provide at least one."}))
        return 1

    result = self_consistency_check(args.assumptions)
    print(json.dumps(result, indent=2, default=str))
    return 0


def run_exemplars(args) -> int:
    """``tutor booster exemplars <task> [--examples <path>]``

    Constructs a few-shot prompt block from the class.yaml FAIL/PASS examples.
    If ``--examples`` is given, reads a JSON file with ``[{"fail": "...",
    "pass": "..."}, ...]``. Otherwise pulls from the target class's syllabus.
    """
    from tutor.booster.tools import inject_few_shot

    examples = None
    if args.examples:
        try:
            with open(args.examples, encoding="utf-8") as f:
                examples = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            print(json.dumps({"error": f"Failed to load examples: {exc}"}))
            return 2

    result = inject_few_shot(args.task, examples)
    print(json.dumps(result, indent=2, default=str))
    return 0


def run_foresee(args) -> int:
    """``tutor booster foresee <choice> [--context <text>]``

    Static analysis: predicts edge cases ~50 lines ahead from a design choice.
    Keyword-match heuristic — no code execution.
    """
    from tutor.booster.tools import downstream_lookahead

    result = downstream_lookahead(args.choice, args.context or "")
    print(json.dumps(result, indent=2, default=str))
    return 0
