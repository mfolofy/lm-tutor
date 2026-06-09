# Peer Review Test Plan — lm-tutor

The following tests are required before this thesis can be submitted for
peer review. Each test addresses a specific confound or gap that a reviewer
would flag.

---

## Test 1: Full 5-Run Pro Benchmark (P0)

**Why:** Current Pro result is a single run — not publishable.

**Protocol:** DeepSeek V4 Pro, HTML task, raw vs class, 5 runs each.

**Files:** `tmp/benchmark_pro.json`

**Cost:** ~$2

---

## Test 2: Explicit Follow-Up (P0)

**Why:** Opus critique: "If a single follow-up prompt recovers most of the gain,
your injection is just a reminder, not steering."

**Protocol:** 
1. Generate raw HTML (no injection)
2. Ask: "The output above has accessibility issues. Rewrite it following WCAG 2.2 rules."
3. Grade the follow-up output
4. Compare: does follow-up alone match `tutor learn` injection?

**Interpretation:**
- If follow-up ≈ class injection → injection is just a reminder. Thesis weakens.
- If follow-up ≪ class injection → injection is doing real steering. Thesis holds.

**Models:** V4 Flash, 5 runs each.

**Cost:** ~$0.50

---

## Test 3: Difficulty Ladder (P1)

**Why:** Does injection help more on complex tasks where there are more
opportunities for violations? Or does it only help on simple, checklist-style
tasks?

**Protocol:** 4 levels of HTML page complexity, V4 Flash, raw vs class, 5 runs.

| Level | Description | Elements |
|-------|-------------|---------|
| Simple | Single paragraph | 3-5 |
| Medium | Page with image, link, button | 6-10 |
| Complex | Full page with form, table, nav | 10-15 |
| SPA | Interactive component with state | 15-25 |

**Interpretation:** Effect should increase with complexity (more opportunities
for violations → more room for injection to work). If effect is flat, injection
only fixes surface-level omissions.

**Cost:** ~$1

---

## Test 4: Cross-Class Benchmark (P1)

**Why:** WCAG may be a uniquely easy case (checklist-like, shallow patterns).
Need to show the effect generalizes.

**Protocol:** V4 Flash, 3 classes × raw vs class × 5 runs = 30 evals.

| Class | Domain | Task Prompt |
|-------|--------|-------------|
| `defense` | OWASP security | "Write a Python Flask login endpoint" |
| `python-best-practices` | PEP 8 | "Write a data processing script" |
| `audit` | SOC2/HIPAA | "Generate a compliance config for a new service" |

**Cost:** ~$0.50

---

## Test 5: Optional Follow-Up as Injection (P1)

**Why:** Does combining `tutor learn` + explicit follow-up beat either alone?
Tests whether the two mechanisms are additive.

**Protocol:** V4 Flash, HTML task, 4 conditions × 5 runs:

| Condition | Description |
|-----------|-------------|
| Raw | No injection |
| Follow-up only | Raw → ask to fix |
| Class only | `tutor learn` injection |
| Class + follow-up | Inject then ask to fix |

**Cost:** ~$1

---

## Summary

| Test | Runs | Calls | Cost | Time |
|------|------|-------|------|------|
| 1. Pro 5-run | 10 | 10 | ~$2 | 3 min |
| 2. Explicit follow-up | 10 | 20 | ~$0.50 | 3 min |
| 3. Difficulty ladder | 40 | 40 | ~$1 | 6 min |
| 4. Cross-class | 30 | 30 | ~$0.50 | 5 min |
| 5. Follow-up additive | 20 | 40 | ~$1 | 6 min |
| **Total** | **110** | **140** | **~$5** | **~25 min** |

All tests can run in parallel. Total cost ~$5. Total wall time ~25 min.

---

## Execution Order

1. Run Test 2 (explicit follow-up) — most important for thesis validity
2. Run Test 1 (Pro 5-run) — weakest data point currently
3. Run Test 4 (cross-class) — tests generalization
4. Run Test 3 (difficulty ladder) — maps the benefit curve
5. Run Test 5 (follow-up additive) — if Tests 2 shows follow-up works
