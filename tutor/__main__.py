"""CLI entry point for lm-tutor.

One console script (``tutor``) with five subcommands:

    tutor enroll   — identify a model, get its curriculum track
    tutor learn    — take a class (Phase 0: prints the injection prefix)
    tutor eval     — grade a submission read from stdin (Layer 1 rules engine)
    tutor mcp      — launch the MCP server (stdio) + HTTP health on :9090
    tutor list     — list available classes

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
    sub = parser.add_subparsers(dest="command", metavar="{enroll,learn,eval,mcp,list}")

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

    # tutor mcp
    p_mcp = sub.add_parser("mcp", help="Launch the MCP server (stdio).")
    p_mcp.add_argument(
        "--no-health", action="store_true",
        help="Do not bind the HTTP health endpoint.",
    )

    # tutor list
    sub.add_parser("list", help="List available classes.")

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
    if args.command == "mcp":
        from tutor.cli.mcp import run
        return run(args)
    if args.command == "list":
        from tutor.cli.list import run
        return run(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
