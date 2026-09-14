# Retraction — benchmark numbers (2026-09-14)

An independent code review of this repository found two defects in the graders that produced lm-tutor's published
benchmark numbers. Each defect was reproduced by a second reviewer. **Every violation count and reduction percentage
published in this repository is withdrawn** until the benchmark is re-run against corrected graders. The numbers are
left in place in the documents as the record of what was claimed; this note is what is currently true.

## 1. The WCAG (`brushes`) grader did not check label association

7 of the 8 label-related rules in the `brushes` class treated a form control as "labelled" whenever it had an `id`
attribute. They never checked that a matching `<label for="...">`, an enclosing `<label>`, or a non-empty
`aria-label` / `aria-labelledby` actually existed.

Example: grading `<form><input type="text" id="username"></form>` with `brushes` reported **0 violations** for a form
control with no label at all. The same grader scored both the raw and the injected arm of every run.

**Withdrawn:** every WCAG result and every percentage derived from it — including the 55–93% headline, the per-model
table (68%, 83%, 100%, 63%, 12%), the 64–83% range, the placebo comparisons and their multiples, and the
difficulty-ladder figures. Unlabelled controls went uncounted in both arms, so the true effect size could be higher or
lower; the review does not show the steering effect is absent, only that it was measured with a broken instrument.

## 2. The defense (OWASP) cross-class row graded output the rules could not match

The `defense` class's checkable rules target backend and configuration patterns (SQL string construction, secrets in
config files, cookie flags). The benchmark's task output is a static HTML page, so none of those patterns could appear.
Grading that HTML with `defense` reported 0 violations in both arms, which was read as a 100% reduction.

**Withdrawn:** the "defense (OWASP) 1.0 → 0.0, 100%" row, its "zero variance" claim, and the conclusion that injection
is more effective for security-reasoning code. There was no security task and no security signal.

## 3. What is not affected

- `python-best-practices` (0%, at ceiling) is not implicated, but it was never a positive result.
- The mechanism claim is untested by this review, not refuted.

## 4. Status

Both grader defects have been fixed in the development tree: label association is now checked properly, and a grade
with no applicable rules is reported as not applicable rather than as zero violations. The fixes and a re-run of the
benchmark will be published here. Until then, please do not quote any reduction percentage from this project.
