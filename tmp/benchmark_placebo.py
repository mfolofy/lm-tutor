"""Placebo control: irrelevant [RULE] injection vs real class vs raw.
If placebo also reduces violations, the thesis is wrong -- it's 'structured
prompting helps' not 'steering toward correct patterns'."""

import json
import subprocess
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

import yaml

DEEPSEEK_KEY = sys.argv[1] if len(sys.argv) > 1 else ""
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

# Build real class injection
cls = yaml.safe_load((Path(__file__).parent.parent / "tutor" / "classes" / "brushes" / "class.yaml").read_text(encoding="utf-8"))
real_rules = "\n".join(f"  [RULE {r['id']}] {r['rule']}" for r in cls.get("rules", []) if r.get("rule"))

# Build placebo injection (same format, wrong rules — gardening tips)
placebo_rules = """  [RULE soil-type] Choose soil that matches your plant's native habitat. Succulents need sandy, well-draining mix.
  [RULE watering] Water deeply but infrequently to encourage deep root growth. Morning watering prevents fungal disease.
  [RULE sunlight] Most vegetables need 6-8 hours of direct sunlight daily. Leafy greens tolerate partial shade.
  [RULE spacing] Space plants according to mature size, not seedling size. Overcrowding reduces yield and encourages disease.
  [RULE pruning] Remove dead or diseased branches at the collar. Never remove more than 1/3 of living tissue per season.
  [RULE fertilizer] Use balanced NPK for most plants. Nitrogen for leafy growth, phosphorus for blooms, potassium for roots.
  [RULE mulching] Apply 2-3 inches of organic mulch around plants. Keep mulch 2 inches from stems to prevent rot.
  [RULE composting] Maintain 3:1 brown-to-green ratio in compost. Turn pile weekly for optimal decomposition.
  [RULE pest-control] Introduce beneficial insects before pesticides. Neem oil treats most common garden pests.
  [RULE seasonality] Plant cool-season crops in early spring and fall. Warm-season crops after last frost date."""

prompts = {
    "raw": TASK,
    "class": f"Brushes - Web Accessibility (WCAG 2.2)\nApply these rules:\n{real_rules}\n\nTask: {TASK}",
    "placebo": f"Gardening - Plant Care Guidelines\nApply these rules:\n{placebo_rules}\n\nTask: {TASK}",
}

results = []
for condition in ["raw", "placebo", "class"]:
    for run in range(5):
        sys.stdout.write(f"  {condition:7s} run {run}... ")
        sys.stdout.flush()
        try:
            output = call(prompts[condition])
            graded = grade(output)
            v = len(graded.get("violations", []))
            sys.stdout.write(f"{v} violations\n")
            results.append({"condition": condition, "run": run, "violations": v, "passed": graded.get("passed")})
        except Exception as e:
            sys.stdout.write(f"ERROR: {e}\n")

print("\n" + "=" * 60)
print("PLACEBO CONTROL TEST")
print("=" * 60)
by_cond = defaultdict(list)
for r in results:
    by_cond[r["condition"]].append(r["violations"])

for c in ["raw", "placebo", "class"]:
    vs = by_cond.get(c, [])
    if vs:
        avg = sum(vs) / len(vs)
        print(f"  {c:7s}: avg {avg:.1f} violations  ({vs})")

if all(by_cond.get(c) for c in ["raw", "placebo", "class"]):
    ra = sum(by_cond["raw"]) / len(by_cond["raw"])
    pa = sum(by_cond["placebo"]) / len(by_cond["placebo"])
    ca = sum(by_cond["class"]) / len(by_cond["class"])
    print(f"\n  raw    -> class:   {((ra - ca) / max(ra, 1)) * 100:.0f}%")
    print(f"  raw    -> placebo: {((ra - pa) / max(ra, 1)) * 100:.0f}%")
    if pa < ra * 0.85:
        print("\n  *** PLACEBO EFFECT DETECTED ***")
        print("  Irrelevant rules also reduce violations. The 'steering' thesis is wrong.")
        print("  The effect is from structured prompting, not correct-pattern steering.")
    else:
        print("\n  *** NO PLACEBO EFFECT ***")
        print("  Irrelevant rules don't help. Violation reduction requires correct rules.")
        print("  The steering thesis holds.")

Path("tmp/benchmark_placebo.json").write_text(json.dumps(results, indent=2))
print(f"\nSaved to tmp/benchmark_placebo.json")
