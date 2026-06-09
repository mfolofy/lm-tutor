"""Compact benchmark: 5 tasks x 2 conditions x 3 runs = 30 evals."""

import json
import subprocess
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

import yaml

DEEPSEEK_KEY = sys.argv[1] if len(sys.argv) > 1 else ""

TASKS = {
    "html": "Generate a complete HTML page with header, nav, main content, footer. Include an image, a button, a link, a form with text input, and a table.",
    "react": "Write a React/Tailwind component for a user profile card with avatar image, name, bio, and contact button.",
    "json": "Generate a JSON response for a user endpoint with name, email, roles array, and metadata object.",
    "svg": "Create an SVG icon for a settings gear, 24x24.",
    "markdown": "Write a README section for a CLI tool called example-tool.",
}


def call(prompt: str) -> str:
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 4096,
    }).encode()
    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {DEEPSEEK_KEY}"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())["choices"][0]["message"]["content"]


def grade(text: str) -> dict:
    r = subprocess.run(
        [sys.executable, "-m", "tutor", "eval", "--model", "deepseek-chat"],
        input=text,
        capture_output=True,
        text=True,
        timeout=30,
        encoding="utf-8",
        cwd=Path(__file__).parent.parent,
    )
    return json.loads(r.stdout)


# Build injection prefix
cls = yaml.safe_load(
    (Path(__file__).parent.parent / "tutor" / "classes" / "brushes" / "class.yaml")
    .read_text(encoding="utf-8")
)
rule_lines = "\n".join(
    f"  [RULE {r['id']}] {r['rule']}"
    for r in cls.get("rules", [])
    if r.get("rule")
)
injection_prefix = f"{cls['class']['title']}\nApply these rules:\n{rule_lines}\n\nTask: "

results = []
for task_name, task_prompt in TASKS.items():
    for condition, prefix in [("raw", ""), ("class", injection_prefix)]:
        for run in range(3):
            prompt = prefix + task_prompt
            sys.stdout.write(f"  {task_name:10s} {condition:6s} run {run}... ")
            sys.stdout.flush()
            try:
                output = call(prompt)
                graded = grade(output)
                v = len(graded.get("violations", []))
                sys.stdout.write(f"{v} violations\n")
                results.append({
                    "task": task_name,
                    "condition": condition,
                    "run": run,
                    "violations": v,
                    "passed": graded.get("passed", False),
                    "rules_checked": graded.get("rules_checked", 0),
                })
            except Exception as e:
                sys.stdout.write(f"ERROR: {e}\n")

# Print results
print("\n" + "=" * 60)
print("BENCHMARK RESULTS — DeepSeek V4 Flash")
print("=" * 60)
by_cell = defaultdict(list)
for r in results:
    by_cell[(r["task"], r["condition"])].append(r["violations"])

for (t, c), vlist in sorted(by_cell.items()):
    avg = sum(vlist) / len(vlist)
    print(f"  {t:10s} {c:6s}: avg {avg:.1f} violations  per-run: {vlist}")

print()
cond_sums = defaultdict(list)
for r in results:
    cond_sums[r["condition"]].append(r["violations"])
for c in ["raw", "class"]:
    vs = cond_sums[c]
    avg = sum(vs) / len(vs)
    print(f"  {c:6s} overall: avg {avg:.1f} violations  ({len(vs)} evals)")

out_path = Path("tmp/benchmark_results.json")
out_path.write_text(json.dumps(results, indent=2))
print(f"\nSaved to {out_path}")
