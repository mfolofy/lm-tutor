#!/usr/bin/env python3
"""Phase 3 Benchmark: Compare classes alone vs booster+classes.

Usage:
    python scripts/benchmark_phase3.py                    # pipeline-only (no API)
    python scripts/benchmark_phase3.py --api-key <key>    # live model eval
    python scripts/benchmark_phase3.py --model deepseek/deepseek-v4-flash

Pipeline-only mode tests:
  - Booster tools generate valid foresight + exemplars
  - `tutor learn --auto` produces a booster pack
  - `tutor fix --booster` attaches booster context to fix output

Live model mode tests (requires DEEPSEEK_API_KEY):
  - Classes alone: model output injected with rules only
  - Booster + classes: model output injected with rules + booster pack
  - Compares violation counts between conditions

Output: tmp/benchmark-phase3-results.json
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TMP = REPO / "tmp"
TMP.mkdir(parents=True, exist_ok=True)


# ── Test tasks ─────────────────────────────────────────────────────────────────

TASKS = {
    "html": "Generate a complete HTML page with header, nav, main content, and footer. Include an image, a button, and a form with a text input.",
    "react": "Write a React component for a user profile card with an avatar image, name, bio, and contact button.",
}

CLASSES = ["brushes", "security"]

MOCK_OUTPUTS = {
    "brushes": '<html><body><img src="photo.jpg"><button></button><input type="text"></body></html>',
    "security": '{\n  "password": "admin123",\n  "query": "SELECT * FROM users WHERE id = " + user_id\n}',
}


# ── Pipeline tests ─────────────────────────────────────────────────────────────

def test_learn_auto() -> dict:
    """Test that `tutor learn --auto` produces valid booster artifacts."""
    results = {}
    for class_name in CLASSES:
        result = subprocess.run(
            [sys.executable, "-m", "tutor", "learn",
             "--model", "gemma4:latest", "--class", class_name, "--auto"],
            capture_output=True, encoding="utf-8", errors="replace", timeout=30,
        )
        stdout = result.stdout
        stderr = result.stderr
        results[class_name] = {
            "exit_code": result.returncode,
            "has_rules": "[RULE" in stdout,
            "has_edge_cases": "Edge Cases" in stdout,
            "has_exemplars": "Few-Shot" in stdout,
            "valid": result.returncode == 0 and "[RULE" in stdout,
        }
    return results


def test_fix_booster() -> dict:
    """Test that `tutor fix --booster` attaches booster context."""
    results = {}
    for class_name, output in MOCK_OUTPUTS.items():
        result = subprocess.run(
            [sys.executable, "-m", "tutor", "fix",
             "--class", class_name, "--once", "--booster"],
            input=output, capture_output=True, encoding="utf-8", errors="replace",
        )
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        has_booster_in_stderr = "fix:booster" in stderr
        has_violations = '"violations"' in stdout
        results[class_name] = {
            "exit_code": result.returncode,
            "has_booster": has_booster_in_stderr,
            "has_violations": has_violations,
            "valid": result.returncode == 0 and has_violations,
        }
    return results


def test_eval_live() -> dict:
    """Test that `tutor eval` works on mock outputs."""
    results = {}
    for class_name, output in MOCK_OUTPUTS.items():
        result = subprocess.run(
            [sys.executable, "-m", "tutor", "eval",
             "--class", class_name, "--model", "gemma4:latest"],
            input=output, capture_output=True, encoding="utf-8", errors="replace",
        )
        stdout = result.stdout or ""
        try:
            data = json.loads(result.stdout)
        except (json.JSONDecodeError, ValueError):
            data = {"parse_error": result.stdout[:200]}
        results[class_name] = {
            "exit_code": result.returncode,
            "violations": len(data.get("violations", [])),
            "passed": data.get("passed", False),
            "valid": result.returncode == 0,
        }
    return results


# ── Live model test (requires API key) ─────────────────────────────────────────

def live_model_test(api_key: str, model: str) -> dict:
    """Run the full Phase 3 benchmark against a live model."""
    from openai import OpenAI

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1",
    )

    results = {}
    for task_name, task_prompt in TASKS.items():
        for class_name in CLASSES:
            # --- Condition 1: Raw (no injection) ---
            raw_output = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": task_prompt}],
                temperature=0.7,
            ).choices[0].message.content or ""

            # Grade raw output
            raw_eval = subprocess.run(
                [sys.executable, "-m", "tutor", "eval", "--class", class_name],
                input=raw_output, capture_output=True, encoding="utf-8", errors="replace", timeout=30,
            )
            raw_violations = _count_violations(raw_eval.stdout)

            # --- Condition 2: Class injection only ---
            cls_result = subprocess.run(
                [sys.executable, "-m", "tutor", "learn",
                 "--model", model, "--class", class_name],
                capture_output=True, encoding="utf-8", errors="replace", timeout=30,
            )
            class_prefix = cls_result.stdout

            injected_output = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": class_prefix + "\n\n" + task_prompt},
                ],
                temperature=0.7,
            ).choices[0].message.content or ""

            injected_eval = subprocess.run(
                [sys.executable, "-m", "tutor", "eval", "--class", class_name],
                input=injected_output, capture_output=True, encoding="utf-8", errors="replace", timeout=30,
            )
            class_violations = _count_violations(injected_eval.stdout)

            # --- Condition 3: Class + Booster auto ---
            booster_result = subprocess.run(
                [sys.executable, "-m", "tutor", "learn",
                 "--model", model, "--class", class_name, "--auto"],
                capture_output=True, encoding="utf-8", errors="replace", timeout=30,
            )
            booster_prefix = booster_result.stdout

            booster_output = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": booster_prefix + "\n\n" + task_prompt},
                ],
                temperature=0.7,
            ).choices[0].message.content or ""

            booster_eval = subprocess.run(
                [sys.executable, "-m", "tutor", "eval", "--class", class_name],
                input=booster_output, capture_output=True, encoding="utf-8", errors="replace", timeout=30,
            )
            booster_violations = _count_violations(booster_eval.stdout)

            key = f"{task_name}/{class_name}"
            results[key] = {
                "raw_violations": raw_violations,
                "class_only_violations": class_violations,
                "booster_violations": booster_violations,
                "reduction_class": _pct(raw_violations, class_violations),
                "reduction_booster": _pct(raw_violations, booster_violations),
            }

    return results


def _count_violations(eval_stdout: str) -> int:
    try:
        data = json.loads(eval_stdout)
        return len(data.get("violations", []))
    except (json.JSONDecodeError, ValueError):
        return -1


def _pct(baseline: int, value: int) -> float | None:
    if baseline <= 0:
        return None
    return round((baseline - value) / baseline * 100, 1)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Phase 3 Benchmark")
    parser.add_argument("--api-key", help="DeepSeek API key for live model eval")
    parser.add_argument("--model", default="deepseek/deepseek-v4-flash", help="Model to test")
    args = parser.parse_args()

    print("=" * 60)
    print("Phase 3 Benchmark — lm-tutor")
    print("=" * 60)

    # Pipeline tests (always run, no API key needed)
    print("\n[1/3] Pipeline: tutor learn --auto ... ", end="", flush=True)
    learn_results = test_learn_auto()
    all_ok = all(r["valid"] for r in learn_results.values())
    print("PASS" if all_ok else "FAIL")
    for cls, r in learn_results.items():
        print(f"  {cls}: rules={r['has_rules']}, edges={r['has_edge_cases']}, exemplars={r['has_exemplars']}")

    print("\n[2/3] Pipeline: tutor fix --booster ... ", end="", flush=True)
    fix_results = test_fix_booster()
    all_ok = all(r["valid"] for r in fix_results.values())
    print("PASS" if all_ok else "FAIL")
    for cls, r in fix_results.items():
        print(f"  {cls}: booster={r['has_booster']}, violations={r['has_violations']}")

    print("\n[3/3] Pipeline: tutor eval ... ", end="", flush=True)
    eval_results = test_eval_live()
    all_ok = all(r["valid"] for r in eval_results.values())
    print("PASS" if all_ok else "FAIL")
    for cls, r in eval_results.items():
        print(f"  {cls}: {r['violations']} violations, passed={r['passed']}")

    # Live model test (API key required)
    live_results = {}
    if args.api_key:
        print("\n[Live] Model benchmark (3 conditions)... ", end="", flush=True)
        live_results = live_model_test(args.api_key, args.model)
        print("DONE")
        for key, r in live_results.items():
            print(f"  {key}: raw={r['raw_violations']}, class={r['class_only_violations']}, booster={r['booster_violations']}")
    else:
        print("\n[Live] Skipped (no --api-key). Run with DEEPSEEK_API_KEY or --api-key.")

    # Save results
    results = {
        "pipeline_learn": learn_results,
        "pipeline_fix": fix_results,
        "pipeline_eval": eval_results,
        "live": live_results,
        "pipeline_passed": all(
            r["valid"] for r in learn_results.values()
        ) and all(
            r["valid"] for r in fix_results.values()
        ) and all(
            r["valid"] for r in eval_results.values()
        ),
    }
    out_path = TMP / "benchmark-phase3-results.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nResults saved to {out_path}")

    return 0 if results["pipeline_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
