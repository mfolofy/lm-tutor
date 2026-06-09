"""Profile-driven injection: inject only the rules the model failed last time.
Tests whether targeted injection outperforms blanket injection."""

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

cls = yaml.safe_load((Path(__file__).parent.parent / "tutor" / "classes" / "brushes" / "class.yaml").read_text(encoding="utf-8"))
all_rules = {r["id"]: r["rule"] for r in cls.get("rules", []) if r.get("rule")}

def build_injection(rules_subset: dict) -> str:
    lines = "\n".join(f"  [RULE {k}] {v}" for k, v in rules_subset.items())
    return f"Brushes - Web Accessibility (WCAG 2.2)\nApply these rules:\n{lines}\n\nTask: {TASK}"

# Cycle 1: full injection
failed_rules = set()
for run in range(3):
    prompt = build_injection(all_rules)
    output = call(prompt)
    graded = grade(output)
    # Track which rules failed
    for v in graded.get("violations", []):
        failed_rules.add(v.get("rule", "?"))

print("Cycle 1 (full injection) done.")
print(f"  Remaining failing rules: {failed_rules}")

# Cycle 2: only failed rules
if failed_rules:
    subset = {k: v for k, v in all_rules.items() if k in failed_rules}
    print(f"  Targeted injection: {len(subset)} rules")
    for run in range(3):
        prompt = build_injection(subset)
        output = call(prompt)
        graded = grade(output)
        v = len(graded.get("violations", []))
        print(f"  Targeted run {run}: {v} violations")

# Save
Path("tmp/benchmark_profile.json").write_text(json.dumps({
    "cycle1_failures": list(failed_rules),
}, indent=2))
