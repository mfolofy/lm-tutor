"""``tutor install-opencode`` — inject lm-tutor rules into OpenCode sessions.

Generates a multi-class tutor prefix and inserts it into ``opencode.json``'s
``instructions`` block so every OpenCode session auto-injects best-practice
rules into the model's attention window at generation time.

Usage::

    tutor install-opencode                           # default lang + general classes
    tutor install-opencode --lang python,typescript  # specific languages only
    tutor install-opencode --classes security,test   # explicit classes only
    tutor install-opencode --dry-run                 # preview without writing
    tutor install-opencode --config ~/opencode.json  # custom config path
    tutor install-opencode --uninstall               # remove tutor rules, restore backup

The command reads ``opencode.json``, locates the ``instructions`` array, and
prepends the tutor prefix as the first instruction. A marker comment
(``# ═══ lm-tutor injected ═══``) bounds the injected block so it can be
replaced or removed on re-install / uninstall.

A backup of the original ``opencode.json`` is saved as ``opencode.json.tutor-backup``.
"""

import json
import sys
from pathlib import Path
from typing import Optional

from tutor.cli.prefix import compose_prefix, _resolve_classes, _dedup_rules
from tutor.eval.harness import load_syllabus

_TUTOR_MARKER = "# ═══ lm-tutor injected ═══"
_TUTOR_MARKER_END = "# ═══ end lm-tutor ═══"


def _default_opencode_path(config_arg: str | None = None) -> Path:
    """Resolve the path to ``opencode.json``.

    Priority: ``--config`` flag > ``OPENCODE_CONFIG`` env > ``$HOME/opencode.json``
    > ``P:/AI_Code/opencode.json`` (Windows default).
    """
    if config_arg:
        return Path(config_arg).expanduser().resolve()

    env = sys.platform == "win32" and "OPENCODE_CONFIG" in dict(__import__("os").environ)
    # Actually: OPENCODE_CONFIG isn't a standard env var.
    # Default locations:
    candidates = [
        Path.home() / "opencode.json",
        Path("P:/AI_Code/opencode.json"),
    ]
    for p in candidates:
        if p.exists():
            return p.resolve()

    # Fall back to the current directory — will error later if not found.
    return Path("opencode.json")


def _generate_prefix(class_ids: list[str], lang_ids: list[str]) -> str:
    """Generate the tutor injection prefix from class/lang specifications."""
    resolved = _resolve_classes(class_ids, lang_ids)
    if not resolved:
        return ""

    loaded: list[dict] = []
    for cid in resolved:
        try:
            loaded.append(load_syllabus(cid))
        except FileNotFoundError:
            print(
                f"[tutor install-opencode] Warning: class '{cid}' not found. Skipping.",
                file=sys.stderr,
            )
            continue

    if not loaded:
        return ""

    return compose_prefix(loaded)


def _build_injection_block(prefix: str) -> list[str]:
    """Wrap the prefix in marker comments so it's identifiable for uninstall."""
    lines = [_TUTOR_MARKER]
    for line in prefix.strip().split("\n"):
        lines.append(f"  {line}")
    lines.append(f"  {_TUTOR_MARKER_END}")
    return lines


def _strip_tutor_instructions(instructions: list[str]) -> list[str]:
    """Remove any existing tutor-injected block from instructions."""
    cleaned: list[str] = []
    inside_tutor_block = False
    for line in instructions:
        if line.strip() == _TUTOR_MARKER:
            inside_tutor_block = True
            continue
        if line.strip() == _TUTOR_MARKER_END:
            inside_tutor_block = False
            continue
        if not inside_tutor_block:
            cleaned.append(line)
    return cleaned


def _print_prefix(prefix: str) -> None:
    """Show the prefix with a box for --dry-run output."""
    width = 68
    print("+" + "-" * (width - 2) + "+")
    print("| Would inject into opencode.json instructions:".ljust(width - 1) + "|")
    print("|".ljust(width - 1) + "|")
    for line in prefix.strip().split("\n")[:30]:
        display = line[:width - 4]
        print(f"| {display}".ljust(width - 1) + "|")
    lines_count = len(prefix.strip().split("\n"))
    if lines_count > 30:
        print(f"| ... (truncated, {lines_count} lines total)".ljust(width - 1) + "|")
    print("+" + "-" * (width - 2) + "+")


def install(config_path: Path, class_ids: list[str], lang_ids: list[str],
            dry_run: bool = False, backup_path: Optional[Path] = None) -> int:
    """Install or update tutor rules in opencode.json."""

    # 1. Generate the prefix.
    prefix = _generate_prefix(class_ids, lang_ids)
    if not prefix:
        print(
            "[tutor install-opencode] Error: no classes loaded. "
            "Run `tutor list` to see available classes.",
            file=sys.stderr,
        )
        return 1

    if dry_run:
        print(f"[tutor install-opencode] DRY RUN — would write to: {config_path}")
        print()
        _print_prefix(prefix)
        print()
        total_rules = prefix.count("[RULE")
        print(f"[tutor install-opencode] {total_rules} rules, {len(class_ids) + len(lang_ids)} source(s), "
              f"~{total_rules * 12} token est.")
        return 0

    # 2. Load opencode.json.
    if not config_path.exists():
        print(
            f"[tutor install-opencode] Error: {config_path} not found. "
            f"Use --config to specify the path.",
            file=sys.stderr,
        )
        return 2

    try:
        raw = config_path.read_text(encoding="utf-8")
        config = json.loads(raw)
    except (json.JSONDecodeError, OSError) as e:
        print(f"[tutor install-opencode] Error reading {config_path}: {e}", file=sys.stderr)
        return 3

    # 3. Save backup.
    bp = backup_path or config_path.with_suffix(config_path.suffix + ".tutor-backup")
    bp.write_text(raw, encoding="utf-8")
    print(f"[tutor install-opencode] Backup saved: {bp}", file=sys.stderr)

    # 4. Inject tutor instructions.
    instructions: list[str] = config.get("instructions", [])
    if not isinstance(instructions, list):
        instructions = []

    # Strip any existing tutor block (idempotent).
    instructions = _strip_tutor_instructions(instructions)

    # Prepend the tutor injection as first instruction.
    injection = _build_injection_block(prefix)
    config["instructions"] = injection + instructions

    # Also update agent.build.prompt if present.
    agent = config.get("agent", {})
    if isinstance(agent, dict):
        build = agent.get("build", {})
        if isinstance(build, dict) and "prompt" in build:
            prompt = build["prompt"]
            # Strip any existing tutor block.
            lines = prompt.split("\n")
            cleaned_lines = _strip_tutor_instructions(lines)
            # Prepend tutor injection.
            injection_flat = [line.lstrip() for line in injection]
            build["prompt"] = "\n".join(injection_flat + cleaned_lines)
            config["agent"]["build"] = build

    # 5. Write.
    try:
        config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    except OSError as e:
        print(f"[tutor install-opencode] Error writing {config_path}: {e}", file=sys.stderr)
        return 4

    total_rules = prefix.count("[RULE")
    print(
        f"[tutor install-opencode] Installed: {total_rules} rules from "
        f"{len(class_ids) + len(lang_ids)} source(s) into {config_path.name}.",
    )
    print(f"  ~{total_rules * 12} tokens injected into every OpenCode session.")

    return 0


def uninstall(config_path: Path, backup_path: Optional[Path] = None) -> int:
    """Remove tutor rules from opencode.json and restore from backup."""

    bp = backup_path or config_path.with_suffix(config_path.suffix + ".tutor-backup")

    if bp.exists():
        # Restore from backup.
        try:
            config_path.write_text(bp.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"[tutor install-opencode] Restored from backup: {bp}")
            bp.unlink(missing_ok=True)
            return 0
        except OSError as e:
            print(f"[tutor install-opencode] Error restoring backup: {e}", file=sys.stderr)
            return 3

    # No backup — strip tutor instructions and save.
    if not config_path.exists():
        print("[tutor install-opencode] Nothing to uninstall — config not found.", file=sys.stderr)
        return 1

    try:
        raw = config_path.read_text(encoding="utf-8")
        config = json.loads(raw)
    except (json.JSONDecodeError, OSError) as e:
        print(f"[tutor install-opencode] Error reading {config_path}: {e}", file=sys.stderr)
        return 2

    instructions: list[str] = config.get("instructions", [])
    if isinstance(instructions, list):
        config["instructions"] = _strip_tutor_instructions(instructions)

    # Also strip from agent.build.prompt.
    agent = config.get("agent", {})
    if isinstance(agent, dict):
        build = agent.get("build", {})
        if isinstance(build, dict) and "prompt" in build:
            lines = build["prompt"].split("\n")
            build["prompt"] = "\n".join(_strip_tutor_instructions(lines))
            config["agent"]["build"] = build

    try:
        config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    except OSError as e:
        print(f"[tutor install-opencode] Error writing {config_path}: {e}", file=sys.stderr)
        return 4

    print("[tutor install-opencode] ✓ Tutor rules removed from instructions.")
    return 0


def run(args) -> int:
    raw_classes = getattr(args, "classes", "") or ""
    raw_lang = getattr(args, "lang", "") or ""
    dry_run = getattr(args, "dry_run", False)
    uninstall_flag = getattr(args, "uninstall", False)
    config_arg = getattr(args, "config", None) or None

    class_ids = [c.strip() for c in raw_classes.split(",") if c.strip()]
    lang_ids = [l.strip() for l in raw_lang.split(",") if l.strip()]

    config_path = _default_opencode_path(config_arg)

    if uninstall_flag:
        return uninstall(config_path)

    # Default classes when no flags given: best-practices for common languages
    # plus general engineering classes.
    if not class_ids and not lang_ids:
        lang_ids = ["python", "javascript", "typescript", "html"]
        class_ids = ["security", "test", "perf", "code-review"]

    return install(config_path, class_ids, lang_ids, dry_run=dry_run)
