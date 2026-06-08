"""`tutor list` — list available classes."""


def run(args) -> int:
    from tutor.cli.eval import list_classes

    classes = list_classes()
    if not classes:
        print("No classes installed.")
        return 0

    print(f"Available classes ({len(classes)}):\n")
    for c in classes:
        sources = ", ".join(c["sources"]) if c["sources"] else "—"
        cost = c["estimated_cost_tokens"]
        cost_str = f"~{cost} tokens" if cost else "?"
        print(f"  {c['id']:<16} {c['title']}")
        print(f"  {'':<16} v{c['version']} · {c['rules']} rules · {cost_str} · sources: {sources}")
        print()
    return 0
