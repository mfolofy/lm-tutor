# Fable 5 — Self-Admitted Validation Protocol

> **Purpose:** First external-model validation of the lm-tutor thesis. Fable 5 (Claude)
> receives lm-tutor class rules, produces output, and self-evaluates via `tutor eval`.
> This eliminates training-set contamination risk — Fable 5 was NOT used in
> lm-tutor class creation.

---

## Why This Matters

All prior benchmarks were run on DeepSeek models that *could* have had lm-tutor
class content in their training data (since the repo is public). Fable 5 was NOT
involved in class creation, has NOT ingested lm-tutor class.yaml files during
training, and has NO prior exposure to the rule format.

If Fable 5's output shows measurable violation reduction under class injection,
the thesis is validated on a truly independent model.

---

## Protocol

### Model

- **Name:** Fable 5 (Claude Fable 5)
- **Platform:** Claude Code on the command line
- **Context window:** 200K tokens

### Run Steps

#### Step 1 — Baseline (no injection)

Run Fable 5 raw on a production task. Collect output.

```bash
# Example: generate an HTML page with no lm-tutor rules
# Run this in Claude Code
> "Create a sign-up form page with name, email, password, and submit button.
   Make it look professional."
```

Save output to `tmp/fable5-baseline-1.html`.

#### Step 2 — Evaluate baseline against class

```bash
# Pipe the output through tutor eval against the relevant class
cat tmp/fable5-baseline-1.html | python -m tutor eval --class brushes
```

Record the violation count, severity, and rule IDs triggered.

#### Step 3 — Class-injected generation

Run Fable 5 with the lm-tutor class rules injected into context.

```bash
# First, get the class prefix
python -m tutor prefix --class brushes

# Then give Fable 5 the same task WITH the brush rules in context:
# "Create a sign-up form page with name, email, password, and submit button.
#  Make it look professional.
#
#  Follow these rules:
#  [paste the tutor prefix output here]"
```

Save output to `tmp/fable5-injected-1.html`.

#### Step 4 — Evaluate injected output

```bash
cat tmp/fable5-injected-1.html | python -m tutor eval --class brushes
```

Record violation count and compare to baseline.

#### Step 5 — Repeat for 5 tasks (3 runs each = 15 total)

| Task | Class | Description |
|------|-------|-------------|
| 1. Sign-up form | brushes | HTML form with validation |
| 2. Navigation bar | brushes | Responsive nav with dropdowns |
| 3. Data table | brushes | Sortable table with semantic markup |
| 4. API endpoint | code-review | JSON API with error handling |
| 5. Login component | security | Auth form with session handling |

Each task: 2 runs (baseline + injected) × 5 tasks = 10 eval calls total.
For statistical rigor, run each task 3 times: 30 eval calls.

---

## Recording Results

```json
{
  "model": "claude-fable-5",
  "date": "2026-06-10",
  "task": "sign-up-form",
  "class": "brushes",
  "baseline": {
    "violations": 5,
    "violation_ids": ["BR-001", "BR-003", "BR-007", "BR-012", "BR-015"],
    "pass": false
  },
  "injected": {
    "violations": 2,
    "violation_ids": ["BR-003", "BR-012"],
    "pass": false
  },
  "reduction": "60%",
  "reduction_significant": true
}
```

---

## Pass Criteria

| Metric | Target |
|--------|--------|
| Mean violation reduction across all tasks | >= 20% |
| At least 3/5 tasks show reduction | >= 60% of tasks |
| No task shows increase of > 2 violations | No negative effect |

---

## How to Run in Claude Code

```bash
# 1. Get class rules for injection
cd P:\AI_Code\projects\lm-tutor
python -m tutor prefix --class brushes > tmp/brushes-rules.txt

# 2. Generate baseline in Claude Code (skip lm-tutor context)
#    Save to tmp/fable5-baseline-1.html

# 3. Evaluate baseline
type tmp\fable5-baseline-1.html | python -m tutor eval --class brushes

# 4. Generate injected in Claude Code (with brush rules pasted into prompt)
#    Save to tmp/fable5-injected-1.html

# 5. Evaluate injected
type tmp\fable5-injected-1.html | python -m tutor eval --class brushes

# 6. Record in tmp/fable5-results.json
```
