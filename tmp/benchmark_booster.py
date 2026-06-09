"""Compare raw vs class vs booster on V4 Flash HTML. 3 runs each."""

import json
import subprocess
import sys
import urllib.request
from pathlib import Path

import yaml

DEEPSEEK_KEY = sys.argv[1]

TASK = "Generate a complete HTML page with header, nav, main content, footer. Include an image, a button, a link, a form with text input, and a table."


def call(prompt: str) -> str:
    p = json.dumps({"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7, "max_tokens": 4096}).encode()
    req = urllib.request.Request("https://api.deepseek.com/chat/completions", data=p,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {DEEPSEEK_KEY}"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())["choices"][0]["message"]["content"]


def grade(text: str) -> dict:
    r = subprocess.run([sys.executable, "-m", "tutor", "eval", "--model", "deepseek-chat"], input=text,
        capture_output=True, text=True, timeout=30, encoding="utf-8", cwd=Path(__file__).parent.parent)
    return json.loads(r.stdout)


# Build conditions
cls = yaml.safe_load((Path(__file__).parent.parent / "tutor" / "classes" / "brushes" / "class.yaml").read_text(encoding="utf-8"))
rule_lines = "\n".join(f"  [RULE {r['id']}] {r['rule']}" for r in cls.get("rules", []) if r.get("rule"))

prompts = {
    "raw": TASK,
    "class": f"{cls['class']['title']}\nApply these rules:\n{rule_lines}\n\nTask: {TASK}",
    "booster": f"{cls['class']['title']}\nApply these rules:\n{rule_lines}\n\nBefore generating, reason step by step in your scratchpad about each rule and how it applies. Check your assumptions about accessibility requirements. Then generate the output.\n\nTask: {TASK}",
}

results = []
for condition in ["raw", "class", "booster"]:
    for run in range(5):  # 5 runs for better signal
        prompt = prompts[condition]
        sys.stdout.write(f"  {condition:7s} run {run}... ")
        sys.stdout.flush()
        try:
            output = call(prompt)
            graded = grade(output)
            v = len(graded.get("violations", []))
            sys.stdout.write(f"{v} violations\n")
            results.append({"condition": condition, "run": run, "violations": v, "passed": graded.get("passed")})
        except Exception as e:
            sys.stdout.write(f"ERROR: {e}\n")

print("\n" + "=" * 50)
print("BOOSTER TEST — V4 Flash HTML")
print("=" * 50)
from collections import defaultdict
by_cond = defaultdict(list)
for r in results:
    by_cond[r["condition"]].append(r["violations"])

for c in ["raw", "class", "booster"]:
    vs = by_cond.get(c, [])
    if vs:
        avg = sum(vs) / len(vs)
        print(f"  {c:7s}: avg {avg:.1f} violations  ({vs})")

if by_cond.get("class") and by_cond.get("booster"):
    ca = sum(by_cond["class"]) / len(by_cond["class"])
    ba = sum(by_cond["booster"]) / len(by_cond["booster"])
    ra = sum(by_cond["raw"]) / len(by_cond["raw"])
    print(f"\n  raw -> class:  {((ra - ca) / max(ra, 1)) * 100:.0f}%")
    print(f"  raw -> booster: {((ra - ba) / max(ra, 1)) * 100:.0f}%")
    if ca != ba:
        print(f"  booster vs class: {((ca - ba) / max(ca, 1)) * 100:.0f}% {'better' if ba < ca else 'worse'}")

Path("tmp/benchmark_booster.json").write_text(json.dumps(results, indent=2))
print(f"\nSaved to tmp/benchmark_booster.json")
