"""CLI entry point for lm-tutor.

One console script (``tutor``) with subcommands:

    tutor enroll            — identify a model, get its curriculum track
    tutor learn             — take a class (Phase 0: prints the injection prefix)
    tutor eval              — grade a submission read from stdin (Layer 1 rules engine)
    tutor fix               — eval → fix → re-eval correction loop
    tutor mcp               — launch the MCP server (stdio) + HTTP health on :9090
    tutor list              — list available classes
    tutor booster <sub>     — Booster tools for small models

Design note: each subcommand imports its own dependencies *inside* the handler,
not at module top level. This keeps ``tutor --help`` and ``tutor eval`` from
importing the MCP server, the HTTP health socket, or anything networked.
"""

import argparse
import sys


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tutor",
        description="The School for LLMs — structured AI education for any model.",
    )
    parser.add_argument(
        "--version", action="version", version=_version_string()
    )
    sub = parser.add_subparsers(dest="command", metavar="{enroll,learn,eval,fix,mcp,list,booster,curriculum,profile}")

    # tutor enroll
    p_enroll = sub.add_parser("enroll", help="Identify a model, get its track.")
    p_enroll.add_argument("--model", required=True, help="Model id, e.g. claude-opus-4-8")
    p_enroll.add_argument("--json", action="store_true", help="Emit JSON instead of text.")

    # tutor learn
    p_learn = sub.add_parser("learn", help="Take a class.")
    p_learn.add_argument("--model", required=True, help="Model id.")
    p_learn.add_argument("--class", dest="class_name", default=None, help="Class to take.")

    # tutor eval
    p_eval = sub.add_parser("eval", help="Grade a submission read from stdin.")
    p_eval.add_argument(
        "--class", dest="class_name", default=None,
        help="Syllabus to grade against. If omitted, inferred from content.",
    )
    p_eval.add_argument(
        "--model", default=None,
        help="Model id. When set, saves the result to eval history.",
    )

    # tutor fix
    p_fix = sub.add_parser("fix", help="Eval → fix → re-eval correction loop.")
    p_fix.add_argument(
        "--class", dest="class_name", default=None,
        help="Syllabus to grade against. If omitted, inferred from content.",
    )
    p_fix.add_argument(
        "--once", action="store_true",
        help="Single pass: print fix suggestions, exit. Do not auto-iterate.",
    )
    p_fix.add_argument(
        "--max-iter", type=int, default=5,
        help="Maximum auto-iteration rounds (default: 5).",
    )

    # tutor mcp
    p_mcp = sub.add_parser("mcp", help="Launch the MCP server (stdio).")
    p_mcp.add_argument(
        "--no-health", action="store_true",
        help="Do not bind the HTTP health endpoint.",
    )

    # tutor list
    sub.add_parser("list", help="List available classes.")

    # tutor curriculum
    p_curriculum = sub.add_parser("curriculum", help="Show ordered class list for a model's track.")
    p_curriculum.add_argument("--model", required=True, help="Model id.")
    p_curriculum.add_argument("--json", action="store_true", help="Emit JSON instead of text.")

    # tutor prefix
    p_prefix = sub.add_parser("prefix", help="Compose multiple classes into a single injection prefix.")
    p_prefix.add_argument(
        "--classes", default="", help="Comma-separated class IDs, e.g. brushes,security,test."
    )
    p_prefix.add_argument(
        "--lang", default="",
        help="Language shorthand, e.g. python,javascript,typescript. Resolves to best-practices classes.",
    )

    # tutor install-opencode
    p_install_oc = sub.add_parser("install-opencode", help="Inject lm-tutor rules into OpenCode sessions.")
    p_install_oc.add_argument(
        "--lang", default="",
        help="Language shorthand, e.g. python,javascript,typescript.",
    )
    p_install_oc.add_argument(
        "--classes", default="",
        help="Comma-separated class IDs, e.g. security,test,perf.",
    )
    p_install_oc.add_argument(
        "--config", default=None,
        help="Path to opencode.json (auto-detected if omitted).",
    )
    p_install_oc.add_argument(
        "--dry-run", action="store_true",
        help="Preview the injection without writing.",
    )
    p_install_oc.add_argument(
        "--uninstall", action="store_true",
        help="Remove tutor rules and restore backup.",
    )

    # tutor profile
    p_profile = sub.add_parser("profile", help="Show eval history and pass rates for a model.")
    p_profile.add_argument("--model", required=True, help="Model id.")
    p_profile.add_argument("--json", action="store_true", help="Emit JSON instead of text.")

    # tutor booster — 4 sub-tools
    p_booster = sub.add_parser("booster", help="Booster tools for small models.")
    booster_sub = p_booster.add_subparsers(
        dest="booster_cmd",
        metavar="{scratchpad,verify,exemplars,foresee}",
    )

    p_scratch = booster_sub.add_parser(
        "scratchpad", help="Run reasoning code in the sandbox. Reads from stdin."
    )

    p_verify = booster_sub.add_parser(
        "verify", help="Check assumptions as Python boolean expressions."
    )
    p_verify.add_argument(
        "assumptions", nargs="+",
        help="Assumptions to verify (each a Python bool expression).",
    )

    p_exemplars = booster_sub.add_parser(
        "exemplars", help="Build a few-shot prompt block from PASS/FAIL examples."
    )
    p_exemplars.add_argument("task", help="Task description.")
    p_exemplars.add_argument(
        "--examples", default=None,
        help="Path to JSON file with [{\"fail\": ..., \"pass\": ...}] array.",
    )

    p_foresee = booster_sub.add_parser(
        "foresee", help="Predict edge cases ~50 lines ahead from a choice."
    )
    p_foresee.add_argument("choice", help="The design choice to analyze.")
    p_foresee.add_argument(
        "--context", default="",
        help="Optional context surrounding the choice.",
    )

    return parser


def _version_string() -> str:
    from tutor import __version__
    return f"tutor {__version__}"


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    # Lazy dispatch — each handler imports only what it needs.
    if args.command == "enroll":
        from tutor.cli.enroll import run
        return run(args)
    if args.command == "learn":
        from tutor.cli.learn import run
        return run(args)
    if args.command == "eval":
        from tutor.cli.eval import run
        return run(args)
    if args.command == "fix":
        from tutor.cli.fix import run
        return run(args)
    if args.command == "mcp":
        from tutor.cli.mcp import run
        return run(args)
    if args.command == "list":
        from tutor.cli.list import run
        return run(args)
    if args.command == "curriculum":
        from tutor.cli.curriculum import run
        return run(args)
    if args.command == "booster":
        return _run_booster(args)
    if args.command == "profile":
        from tutor.cli.profile import run
        return run(args)
    if args.command == "prefix":
        from tutor.cli.prefix import run
        return run(args)
    if args.command == "install-opencode":
        from tutor.cli.install_opencode import run
        return run(args)

    parser.print_help()
    return 1


def _run_booster(args) -> int:
    """Dispatch booster subcommands."""
    if args.booster_cmd is None:
        print("Booster subcommand required: {scratchpad,verify,exemplars,foresee}")
        return 1

    if args.booster_cmd == "scratchpad":
        from tutor.cli.booster import run_scratchpad
        return run_scratchpad(args)
    if args.booster_cmd == "verify":
        from tutor.cli.booster import run_verify
        return run_verify(args)
    if args.booster_cmd == "exemplars":
        from tutor.cli.booster import run_exemplars
        return run_exemplars(args)
    if args.booster_cmd == "foresee":
        from tutor.cli.booster import run_foresee
        return run_foresee(args)

    print(f"Unknown booster command: {args.booster_cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
