"""Benchmark: python-best-practices class on V4 Flash.
5 tasks x 2 conditions (raw, class) x 3 runs = 30 evals.
Graded via tutor eval --class python-best-practices."""

import json
import subprocess
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

import yaml

DEEPSEEK_KEY = sys.argv[1] if len(sys.argv) > 1 else ""

TASKS = {
    "function": "Write a Python function that takes a list of dictionaries representing users (each with name, email, age, roles) and returns the average age of users who have the 'admin' role. Include proper type hints, a docstring, and error handling.",
    "class": "Write a Python class called DataProcessor that reads a CSV file, cleans the data (removes empty rows, converts types), and provides methods to filter, sort, and export the data. Use proper naming conventions and type hints.",
    "script": "Write a Python script that reads a JSON config file, connects to an API endpoint, paginates through results, saves them to a SQLite database, and logs each step. Include proper error handling and resource cleanup.",
    "data-structure": "Write a Python function that takes two lists and returns a dictionary mapping items from the first list to items from the second, handling the case where lists differ in length. Use comprehensions and proper comparison idioms.",
    "module": "Write a small Python module called 'text_utils' with 3-4 public functions for text processing (word count, unique words, sentiment keywords, truncation). Include proper imports, constants, module docstring, and __all__.",
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
        [sys.executable, "-m", "tutor", "eval", "--class", "python-best-practices", "--model", "deepseek-chat"],
        input=text,
        capture_output=True,
        text=True,
        timeout=30,
        encoding="utf-8",
        cwd=Path(__file__).parent.parent,
    )
    return json.loads(r.stdout)


# Build injection
cls = yaml.safe_load(
    (Path(__file__).parent.parent / "tutor" / "classes" / "python-best-practices" / "class.yaml")
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
            sys.stdout.write(f"  {task_name:12s} {condition:6s} run {run}... ")
            sys.stdout.flush()
            try:
                output = call(prompt)
                graded = grade(output)
                v = len(graded.get("violations", []))
                rc = graded.get("rules_checked", 0)
                sys.stdout.write(f"{v} violations ({rc} rules)\n")
                results.append({
                    "task": task_name,
                    "condition": condition,
                    "run": run,
                    "violations": v,
                    "rules_checked": rc,
                    "passed": graded.get("passed", False),
                })
            except Exception as e:
                sys.stdout.write(f"ERROR: {e}\n")

# Print
print("\n" + "=" * 60)
print("BENCHMARK — python-best-practices on DeepSeek V4 Flash")
print("=" * 60)
by_cell = defaultdict(list)
for r in results:
    by_cell[(r["task"], r["condition"])].append(r["violations"])

for (t, c), vlist in sorted(by_cell.items()):
    avg = sum(vlist) / len(vlist)
    print(f"  {t:12s} {c:6s}: avg {avg:.1f} violations  per-run: {vlist}")

print()
cond_sums = defaultdict(list)
for r in results:
    cond_sums[r["condition"]].append(r["violations"])
for c in ["raw", "class"]:
    vs = cond_sums[c]
    avg = sum(vs) / len(vs)
    print(f"  {c:6s} overall: avg {avg:.1f} violations  ({len(vs)} evals)")

if cond_sums["raw"] and cond_sums["class"]:
    raw_avg = sum(cond_sums["raw"]) / len(cond_sums["raw"])
    cls_avg = sum(cond_sums["class"]) / len(cond_sums["class"])
    pct = ((raw_avg - cls_avg) / max(raw_avg, 1)) * 100
    print(f"\n  OVERALL DELTA: {raw_avg:.1f} -> {cls_avg:.1f} ({pct:.0f}% reduction)")

out = Path("tmp/benchmark_python.json")
out.write_text(json.dumps(results, indent=2))
print(f"\nSaved to {out}")
