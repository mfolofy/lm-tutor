"""Benchmark runner for lm-tutor.

Evaluates models on standard tasks with and without lm-tutor injection,
correlating results with known external benchmark scores.

Usage:
    python -m tutor.benchmark --model deepseek-chat --task html --runs 3
    python -m tutor.benchmark --model deepseek-chat --all-tasks --runs 20
"""

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

from tutor.eval import grade
from tutor.eval.harness import load_syllabus
from tutor.cli.eval import infer_syllabus
from tutor.registrar.evals import EvalHistory

# ── Task prompts ─────────────────────────────────────────────────────────────

TASKS = {
    "html": "Generate a complete HTML page with header, nav, main content, and footer. Include an image, a button, a link, a form with a text input, and a table.",
    "react": "Write a React component for a user profile card with an avatar image, name, bio, and a contact button. Use Tailwind CSS classes.",
    "json": "Generate a JSON response for a user endpoint including name, email, roles (array), and metadata (object with created_at, updated_at, last_login).",
    "svg": "Create an SVG icon for a settings gear. Make it a simple, clean 24x24 icon.",
    "markdown": "Write a README section describing how to install and configure a Python CLI tool called 'example-tool'.",
}


# ── Model API client ─────────────────────────────────────────────────────────

def _api_key() -> str:
    key = os.environ.get("DEEPSEEK_API_KEY")
    if key:
        return key
    # Fall back to secrets file
    secrets_path = Path(__file__).parent.parent.parent / "secrets" / "house-api-keys.json"
    if secrets_path.exists():
        with open(secrets_path) as f:
            return json.load(f).get("DEEPSEEK_API_KEY", "")
    return ""


def _generate_deepseek(prompt: str, temperature: float = 0.7, max_retries: int = 3) -> str | None:
    """Call DeepSeek API with the given prompt. Returns text or None."""
    import urllib.request
    import urllib.error

    key = _api_key()
    if not key:
        print("  [ERROR] No DeepSeek API key found", file=sys.stderr)
        return None

    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": 4096,
        "seed": None,  # set per cell
    }).encode()

    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )

    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode())
                return data["choices"][0]["message"]["content"]
        except (urllib.error.URLError, urllib.error.HTTPError, OSError, json.JSONDecodeError) as exc:
            print(f"  [RETRY {attempt + 1}/{max_retries}] API error: {exc}", file=sys.stderr)
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    return None


# ── Conditions ───────────────────────────────────────────────────────────────

def _build_prompt(task: str, condition: str) -> str:
    """Build the full prompt for a task + condition combination."""
    if condition == "raw":
        return task

    if condition == "prompt":
        return (
            "You are a senior web developer following WCAG 2.2 accessibility "
            "standards. Apply these rules:\n"
            "  [RULE img-alt] Every <img> must have non-empty alt text or aria-label.\n"
            "  [RULE button-name] Every <button> must have an accessible name.\n"
            "  [RULE link-name] Every <a> needs accessible name.\n"
            "  [RULE label-for-input] Every <input> needs a <label> or aria-label.\n"
            "  [RULE html-lang] <html> must have a lang attribute.\n"
            "  [RULE title-required] <title> must be non-empty.\n"
            "  [RULE positive-tabindex] Avoid positive tabindex values.\n"
            "\n"
            f"Task: {task}"
        )

    if condition == "placebo":
        # Same [RULE] format as the real class, but irrelevant domain (gardening).
        # If this produces similar reduction to the real class, the effect is
        # from structured prompting alone, not correct-pattern steering.
        # Placebo rules are chosen to be totally orthogonal to HTML/WCAG.
        placebo_rules = [
            ("water-frequency", "Water plants at the base, not the leaves, to prevent fungal disease."),
            ("soil-drainage", "Ensure soil drains well; standing water causes root rot."),
            ("pruning-timing", "Prune flowering shrubs immediately after blooming, not before."),
            ("fertilizer-npk", "Apply a balanced N-P-K fertilizer during active growing season."),
            ("companion-plant", "Plant marigolds near tomatoes to deter aphids naturally."),
            ("mulch-depth", "Apply mulch 2-3 inches deep; deeper mulch can suffocate roots."),
            ("seed-spacing", "Follow packet spacing — crowded seeds compete for nutrients."),
            ("ph-level", "Test soil pH yearly; most vegetables prefer 6.0-7.0."),
            ("deadheading", "Remove spent blooms to encourage continued flowering."),
            ("watering-time", "Water early morning so foliage dries before nightfall."),
        ]
        rules_text = "\n".join(
            f"  [RULE {rid}] {rule}"
            for rid, rule in placebo_rules
        )
        return (
            "# Gardening Best Practices\n"
            "Apply these rules:\n"
            f"{rules_text}\n\n"
            f"Task: {task}"
        )

    if condition == "class":
        cls = load_syllabus("brushes")
        rules_text = "\n".join(
            f"  [RULE {r['id']}] {r['rule']}"
            for r in cls.get("rules", [])
            if r.get("rule")
        )
        return (
            f"# {cls.get('class', {}).get('title', 'brushes')}\n"
            "Apply these rules:\n"
            f"{rules_text}\n\n"
            f"Task: {task}"
        )

    # booster = class + scratchpad hint
    cls = load_syllabus("brushes")
    rules_text = "\n".join(
        f"  [RULE {r['id']}] {r['rule']}"
        for r in cls.get("rules", [])
        if r.get("rule")
    )
    return (
        f"# {cls.get('class', {}).get('title', 'brushes')}\n"
        "Apply these rules:\n"
        f"{rules_text}\n\n"
        "Before generating, use your scratchpad to reason about each rule.\n"
        f"Task: {task}"
    )


# ── Seed ─────────────────────────────────────────────────────────────────────

def _seed_for(model: str, task: str) -> int:
    """Deterministic seed per model+task pair."""
    return int(hashlib.sha256(f"{model}:{task}".encode()).hexdigest()[:8], 16) % (2 ** 32)


# ── Main benchmark loop ──────────────────────────────────────────────────────

def run_benchmark(
    model: str,
    task: str,
    condition: str,
    runs: int = 5,
    temperature: float = 0.7,
) -> list[dict]:
    """Run N generations of a model+task+condition cell. Returns results list."""
    seed = _seed_for(model, task)
    history = EvalHistory()

    print(f"\n  Model: {model}  |  Task: {task}  |  Condition: {condition}  |  Runs: {runs}")
    results = []

    for i in range(runs):
        prompt = _build_prompt(TASKS[task], condition)
        cell_seed = seed + i

        # Inject seed into prompt for reproducibility
        seeded_prompt = f"[seed={cell_seed}]\n{prompt}"

        output = _generate_deepseek(seeded_prompt, temperature=temperature)
        if output is None:
            print(f"  [{i + 1}/{runs}] SKIP (API error)")
            continue

        # Grade it
        syllabus = infer_syllabus(output)
        result = grade(output, syllabus)
        result_dict = result.model_dump()
        result_dict["model"] = model
        result_dict["task"] = task
        result_dict["condition"] = condition
        result_dict["run"] = i
        result_dict["seed"] = cell_seed
        result_dict["temperature"] = temperature

        # Save to eval history
        try:
            history.record(model, result)
        except Exception:
            pass

        violation_count = len(result.violations)
        status = "PASS" if result.passed else f"FAIL ({violation_count} violations)"
        print(f"  [{i + 1}/{runs}] {status}")

        results.append(result_dict)

    return results


def main():
    parser = argparse.ArgumentParser(description="lm-tutor benchmark runner")
    parser.add_argument("--model", default="deepseek-chat", help="Model ID")
    parser.add_argument("--task", choices=list(TASKS.keys()) + ["all"], default="html")
    parser.add_argument("--condition", choices=["raw", "prompt", "placebo", "class", "booster", "all"], default="raw")
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--output", default=None, help="Output JSON path")
    args = parser.parse_args()

    tasks = list(TASKS.keys()) if args.task == "all" else [args.task]
    conditions = ["raw", "prompt", "placebo", "class", "booster"] if args.condition == "all" else [args.condition]

    all_results = []
    for task in tasks:
        for condition in conditions:
            results = run_benchmark(args.model, task, condition, args.runs, args.temperature)
            all_results.extend(results)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    by_condition: dict[str, list[int]] = {}
    for r in all_results:
        c = r["condition"]
        if c not in by_condition:
            by_condition[c] = []
        by_condition[c].append(len(r.get("violations", [])))

    for cond, counts in sorted(by_condition.items()):
        avg = sum(counts) / len(counts) if counts else 0
        passed = sum(1 for r in all_results if r["condition"] == cond and r["passed"])
        total = sum(1 for r in all_results if r["condition"] == cond)
        print(f"  {cond:10s}: avg {avg:.1f} violations — {passed}/{total} passed")

    # Save
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(all_results, indent=2, default=str))
        print(f"\nResults saved to {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
