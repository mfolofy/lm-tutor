"""``tutor prefix`` — compose multiple classes into a single injection prefix.

Phase 1.5: building outward. Takes one or more classes, deduplicates rules by
ID (first wins), and prints a unified ``[RULE]`` prefix to stdout — the same
format ``tutor learn`` produces for a single class, but composable.

Usage::

    tutor prefix --lang python,javascript          # shorthand for best-practices
    tutor prefix --classes brushes,security,test    # explicit class IDs
    tutor prefix --lang python,typescript --classes security  # mixed

The output is a single token-efficient prefix (~120 tokens per class) that
injects all rules into the model's attention window at generation time. Pipe
it directly into a model prompt or prepend it to a code-generation task.
"""

import sys

from tutor.eval.harness import load_syllabus

# Language → class-ID mapping for the ``--lang`` shorthand.
_LANG_TO_CLASS: dict[str, str] = {
    "python": "python-best-practices",
    "javascript": "javascript-best-practices",
    "js": "javascript-best-practices",
    "typescript": "typescript-best-practices",
    "ts": "typescript-best-practices",
    "html": "brushes",
    "accessibility": "brushes",
    "a11y": "brushes",
    "security": "security",
    "test": "test",
    "perf": "perf",
    "devops": "devops",
    "api": "api-design",
    "code-review": "code-review",
    "review": "code-review",
    "architecture": "architect",
    "defense": "defense",
    # Reserved — classes that don't exist yet but feel natural to map:
    # "sql": "sql-best-practices",
    # "css": "css-best-practices",
    # "go": "go-best-practices",
    # "rust": "rust-best-practices",
}

# ── Helpers ─────────────────────────────────────────────────────────────


def _resolve_classes(class_ids: list[str], lang_ids: list[str]) -> list[str]:
    """Resolve explicit class IDs and ``--lang`` shorthands into a
    deduplicated, ordered list of class IDs. Explicit ``--classes`` come
    first (caller-specified priority), then ``--lang`` shorthands in order.
    """
    seen: set[str] = set()
    resolved: list[str] = []

    for cid in class_ids:
        if cid not in seen:
            resolved.append(cid)
            seen.add(cid)

    for lang in lang_ids:
        cid = _LANG_TO_CLASS.get(lang)
        if cid is None:
            print(
                f"[tutor prefix] Warning: unknown language '{lang}'. "
                f"Use --classes for explicit class IDs.",
                file=sys.stderr,
            )
            continue
        if cid not in seen:
            resolved.append(cid)
            seen.add(cid)

    return resolved


def _dedup_rules(classes: list[dict]) -> list[dict]:
    """Merge rules from multiple classes into one ordered list.

    Rules with duplicate ``id`` are collapsed — first occurrence wins.
    Rules without an ``id`` are always included (appended at the end).
    """
    seen: set[str] = set()
    merged: list[dict] = []
    for cls in classes:
        rules = cls.get("rules", []) or []
        for rule in rules:
            rid = rule.get("id")
            if rid is None:
                merged.append(rule)  # no id — always include
            elif rid not in seen:
                merged.append(rule)
                seen.add(rid)
    return merged


def compose_prefix(classes: list[dict]) -> str:
    """Render a unified ``[RULE]`` injection prefix from multiple classes.

    Matches the output format of ``tutor learn`` — rule landmarks only,
    no framework examples (those are teaching-only, not injection).
    The title is the combined class titles joined by " + ".
    """
    titles = []
    for cls in classes:
        meta = cls.get("class", {})
        titles.append(meta.get("title", meta.get("id", "?")))

    rules = _dedup_rules(classes)
    lines = [
        f"# {' + '.join(titles)}",
        "Apply these rules:",
    ]
    for rule in rules:
        lines.append(f"  [RULE {rule.get('id', '?')}] {rule.get('rule', '')}")

    return "\n".join(lines)


def run(args) -> int:
    load_syllabus  # force import of the eval harness at module level

    raw_classes = getattr(args, "classes", "") or ""
    raw_lang = getattr(args, "lang", "") or ""
    class_ids = [c.strip() for c in raw_classes.split(",") if c.strip()]
    lang_ids = [l.strip() for l in raw_lang.split(",") if l.strip()]

    # At least one source required.
    if not class_ids and not lang_ids:
        print(
            "Usage: tutor prefix --classes <id1,id2,...> | --lang <python,javascript,...>",
            file=sys.stderr,
        )
        return 1

    resolved = _resolve_classes(class_ids, lang_ids)

    if not resolved:
        print("[tutor prefix] No valid classes to compose.", file=sys.stderr)
        return 2

    # Load all syllabuses.
    loaded: list[dict] = []
    errors: list[str] = []
    for cid in resolved:
        try:
            loaded.append(load_syllabus(cid))
        except FileNotFoundError:
            errors.append(cid)

    if errors:
        for cid in errors:
            print(
                f"[tutor prefix] Error: class '{cid}' not found. "
                f"Run `tutor list` to see available classes.",
                file=sys.stderr,
            )
        return 3

    # Render the composed prefix.
    print(compose_prefix(loaded))

    # Print composition metadata to stderr (doesn't pollute stdout).
    total_rules = sum(len(cls.get("rules", []) or []) for cls in loaded)
    deduped = len(_dedup_rules(loaded))
    print(
        f"[tutor prefix] {len(resolved)} class(es) composed: "
        f"{', '.join(resolved)}. "
        f"{total_rules} rules → {deduped} after dedup. "
        f"~{deduped * 12} token est.",
        file=sys.stderr,
    )

    return 0
