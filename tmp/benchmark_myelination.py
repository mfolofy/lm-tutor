"""Myelination test: does corrective feedback through the fix loop compound?
Cycle: inject -> generate -> eval -> fix suggestions -> inject again -> generate -> eval.
5 cycles, tracking violations per cycle. Does the effect compound?"""

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

def fix(submission: str, violations: list) -> str:
    """Build a fix prompt showing the model its violations and asking for correction."""
    fix_lines = ["Your previous output had these violations. Fix each one:\n"]
    for v in violations[:5]:
        fix_lines.append(f"- {v.get('rule', '?')}: {v.get('message', '')[:100]}")
        fix_lines.append(f"  (found at: {v.get('matched', '')[:60]})")
    fix_lines.append(f"\nGenerate a corrected version. Apply the [RULE] checklists carefully.\n\nTask: {TASK}")
    return "\n".join(fix_lines)

# Build injection
cls = yaml.safe_load((Path(__file__).parent.parent / "tutor" / "classes" / "brushes" / "class.yaml").read_text(encoding="utf-8"))
rule_lines = "\n".join(f"  [RULE {r['id']}] {r['rule']}" for r in cls.get("rules", []) if r.get("rule"))
injection = f"{cls['class']['title']}\nApply these rules:\n{rule_lines}\n\nTask: {TASK}"

print("=" * 60)
print("MYELINATION TEST — Corrective Feedback Loop")
print("=" * 60)

results = []
current_prompt = injection

for cycle in range(5):
    print(f"\n  Cycle {cycle + 1}...")
    sys.stdout.flush()

    output = call(current_prompt)
    graded = grade(output)
    v = len(graded.get("violations", []))
    passed = graded.get("passed", False)

    print(f"  Violations: {v}  Passed: {passed}")
    results.append({"cycle": cycle, "violations": v, "passed": passed})

    if v == 0:
        print("  → Clean pass. Stopping.")
        break

    # Build fix prompt for next cycle
    current_prompt = fix(output, graded.get("violations", []))
    # Prepend the rule injection to keep rules in context
    current_prompt = f"{cls['class']['title']}\nApply these rules:\n{rule_lines}\n\n{current_prompt}"

print("\n" + "=" * 60)
print("RESULTS")
print("=" * 60)
for r in results:
    print(f"  Cycle {r['cycle'] + 1}: {r['violations']} violations{' ✅' if r['passed'] else ''}")

if len(results) > 1:
    first = results[0]["violations"]
    last = results[-1]["violations"]
    if first > 0:
        print(f"\n  Total reduction: {first} -> {last} ({((first - last) / first) * 100:.0f}%)")
    print(f"  Cycles to clean: {len(results) if results[-1]['passed'] else 'did not converge'}")

Path("tmp/benchmark_myelination.json").write_text(json.dumps(results, indent=2))
print(f"\nSaved to tmp/benchmark_myelination.json")
