"""Retry HTML task on Gemma 3 4B with delays to avoid rate limits."""

import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import yaml

OPENROUTER_KEY = sys.argv[1]
MODEL = "google/gemma-3-4b-it"
TASK = "Generate a complete HTML page with header, nav, main content, footer. Include an image, a button, a link, a form with text input, and a table."


def call(prompt: str, retries=5) -> str | None:
    for attempt in range(retries):
        payload = json.dumps({
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 4096,
        }).encode()
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=payload,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {OPENROUTER_KEY}"},
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read())["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 5 * (2 ** attempt)
                sys.stdout.write(f"  429, waiting {wait}s... ")
                sys.stdout.flush()
                time.sleep(wait)
            else:
                sys.stdout.write(f"ERROR {e.code}: ")
                sys.stdout.flush()
                return None
        except Exception as e:
            sys.stdout.write(f"ERROR: {e} ")
            sys.stdout.flush()
            return None
    return None


def grade(text: str) -> dict:
    r = subprocess.run(
        [sys.executable, "-m", "tutor", "eval", "--model", MODEL],
        input=text, capture_output=True, text=True, timeout=30,
        encoding="utf-8", cwd=Path(__file__).parent.parent,
    )
    return json.loads(r.stdout)


# Build injection
cls = yaml.safe_load(
    (Path(__file__).parent.parent / "tutor" / "classes" / "brushes" / "class.yaml")
    .read_text(encoding="utf-8")
)
rule_lines = "\n".join(f"  [RULE {r['id']}] {r['rule']}" for r in cls.get("rules", []) if r.get("rule"))
injection = f"{cls['class']['title']}\nApply these rules:\n{rule_lines}\n\nTask: "

results = []
for condition, prefix in [("raw", ""), ("class", injection)]:
    for run in range(3):
        prompt = prefix + TASK
        sys.stdout.write(f"\nhtml {condition} run {run}... ")
        sys.stdout.flush()
        output = call(prompt)
        if output is None:
            sys.stdout.write("FAILED\n")
            continue
        graded = grade(output)
        v = len(graded.get("violations", []))
        sys.stdout.write(f"{v} violations (passed: {graded.get('passed')})\n")
        results.append({"task": "html", "condition": condition, "run": run, "violations": v, "passed": graded.get("passed")})

print("\n" + "=" * 50)
print("HTML RESULTS — Gemma 3 4B")
print("=" * 50)
for r in results:
    print(f"  {r['condition']:6s} run {r['run']}: {r['violations']} violations")
if results:
    raw_v = [r["violations"] for r in results if r["condition"] == "raw"]
    cls_v = [r["violations"] for r in results if r["condition"] == "class"]
    raw_avg = sum(raw_v) / len(raw_v) if raw_v else 0
    cls_avg = sum(cls_v) / len(cls_v) if cls_v else 0
    print(f"\n  raw   avg: {raw_avg:.1f}")
    print(f"  class avg: {cls_avg:.1f}")
    if raw_avg > 0:
        print(f"  delta: {((raw_avg - cls_avg) / raw_avg) * 100:.0f}%")

Path("tmp/benchmark_gemma_html.json").write_text(json.dumps(results, indent=2))
print("\nSaved")
