# SOURCES -- code-review (Code Review Standards)

All rules in `class.yaml` derive from three primary sources: **ITIL v4 Service
Management**, **arXiv 2603.25773**, and the **House/everybody-lies** code review
gatekeeper implementation. Every rule cites its specific source. No rule exists
without a foundation.

## Primary standards

### ITIL v4 Service Management (Change Enablement)

- **ITIL Foundation, ITIL 4 Edition** (AXELOS, 2019) -- Change enablement
  practice, incident management, problem management, release management.
- **ITIL v4: Change Enablement** -- Standard/Normal/Emergency/Major change
  classification, risk assessment, CAB (Change Advisory Board), RFC lifecycle.
- **ITIL v4: Incident Management** -- P1-P4 severity matrix, incident lifecycle,
  escalation procedures.
- **ITIL v4: Problem Management** -- Problem vs Incident distinction, root cause
  analysis, known error database (KEDB), permanent fix.
- **ITIL v4: Release Management** -- Release gates, CI identification, rollback
  planning, deploy windows.
- **ITIL v4: Service Value Chain** -- Engage -> Design & Transition ->
  Obtain/Build -> Deliver & Support -> Improve.

### arXiv 2603.25773 -- "The Specification as Quality Gate" (March 2026)

- **Deterministic verification first:** Pattern-based pre-scan catches what all
  AI reviewers consistently miss (credentials, injection patterns, debug configs).
- **Specification grounding:** When a spec file (SPEC.md, feature files) exists,
  Cuddy uses it as ground truth. Code that diverges from spec without
  justification is automatically flagged.
- **AI review blind spots:** AI reviewers are poor at detecting missing
  functionality (silent omission), over-engineering (simpler alternative exists),
  and domain-specific correctness without domain expertise.
- **Multi-model cross-validation:** Using the same model for primary review and
  cross-check compounds blind spots. Different architectures catch different
  error classes.

### House/everybody-lies -- Code Review Gatekeeper

House is a multi-model code review gatekeeper that routes changed files to
domain-specialist models and applies deterministic pre-scanning before AI review.

Key patterns codified into rules:

- **Multi-specialist routing**: Changed files routed to domain specialists
  (backend, frontend, security, data, edge cases). Dynamic specialists auto-hired
  for uncovered domains.
- **Differential diagnosis**: Pre-review that rules out simpler alternatives
  before specialists examine code quality.
- **Deterministic pre-scan**: Zero-cost pattern matching -- 50+ patterns
  (hardcoded secrets, SQL injection, debug configs, weak crypto). Runs
  before any AI review.
- **P1 rejection rules**: P1 findings are automatic rejection. No override
  possible. Categories: credentials, injection, auth bypass, data loss,
  infinite loops, config errors.
- **Separation of powers for appeals**: Appeal reviewer uses a different
  provider than the review board. P1 findings cannot be appealed.
- **Problem management**: Same finding across 3+ reviews creates a problem
  record. Recurring patterns trigger root cause analysis.
- **Risk scoring**: Auto-calculated from lines changed (20%), files changed
  (15%), domain risk (65%). High-risk patterns include auth, trading, billing,
  database migrations.
- **Dynamic specialist hiring**: When code touches domains no existing
  specialist covers, system auto-hires a domain-specific specialist with
  generated review prompts.
- **Adversarial cross-checks**: For adversarial-tier reviews, each specialist
  gets a cross-check from a different model.
- **Suppression learning**: Dismissed findings auto-learn suppression rules.
  If a finding type is repeatedly dismissed, the system stops surfacing it.

## Per-rule source map

| Rule id | Primary Source | Secondary Source |
|---------|---------------|-----------------|
| `review-scope` | ITIL v4 Change Enablement -- change types + scope control | House `gatekeeper.py` -- tier selection |
| `evidence-citation` | House `gatekeeper.py` -- specialist prompt structure (file:line required) | arXiv 2603.25773 -- specification grounding |
| `severity-classification` | ITIL v4 Incident Management -- P1-P4 severity matrix | House `ITIL_SOP.md` section 2 |
| `rubber-stamping` | House `gatekeeper.py` -- adversarial process | arXiv 2603.25773 -- AI review blind spots |
| `over-scoping` | ITIL v4 Change Enablement -- scope control | House `gatekeeper.py` -- scope fields in RFC |
| `drive-by-comments` | House `gatekeeper.py` -- specialist prompt (cite exact file:line) | Peer review literature (Fagan inspection) |
| `deterministic-prescan` | arXiv 2603.25773 -- spec-as-quality-gate, deterministic first | House `scanner.py` -- 50+ pattern definitions |
| `cuddy-differential` | House `gatekeeper.py` lines 375-426 -- Cuddy pre-review | arXiv 2603.25773 -- AI blind spot: over-engineering |
| `multi-specialist-routing` | House `gatekeeper.py` -- `_route_to_specialists()` + dynamic fellows | ITIL v4 CAB -- Change Advisory Board |
| `change-type-label` | ITIL v4 Change Enablement -- Standard/Normal/Emergency/Major | House `ITIL_SOP.md` section 1 |
| `p1-autoreject` | House `ITIL_SOP.md` section 2.1 -- P1 automatic rejection criteria | House `gatekeeper.py` -- P1 patterns + blocking findings |
| `rollback-plan` | ITIL v4 Release Management -- deployment and rollback planning | House `ITIL_SOP.md` section 4 |
| `rfc-record` | ITIL v4 Change Enablement -- RFC lifecycle and record format | House `ITIL_SOP.md` section 1.3 |
| `separation-powers` | House `gatekeeper.py` -- `_get_appeal_model()` lines 1487-1529 | arXiv 2603.25773 -- multi-model cross-validation |
| `appeal-justification` | House `ITIL_SOP.md` section 10 -- valid vs invalid justifications | House `gatekeeper.py` -- Wilson appeal system |
| `compliance-checklist` | House `ITIL_SOP.md` section 9 -- Continuous Compliance Checklist | ITIL v4 Release Management -- release gates |
| `problem-management` | ITIL v4 Problem Management -- problem vs incident, RCA, KEDB | House `learning.py` -- `detect_recurring_problems()` |
| `adversarial-crosscheck` | House `gatekeeper.py` lines 1235-1256 -- adversarial cross-check tier | arXiv 2603.25773 -- multi-model validation |

## Key 2026 research underpinning the rules

| Paper / Source | Relevance |
|---------------|-----------|
| "The Specification as Quality Gate" (arXiv 2603.25773, March 2026) | Deterministic pre-scan before AI; spec-grounded review; multi-model cross-validation |
| "A11yAgent: Multi-Agent Framework for Accessible Web Code" (ACM W4A 2026) | Multi-specialist routing pattern, generate -> detect -> repair loop |
| "Measuring AI Code Review Quality" (ICSE 2026) | Rubber-stamping prevalence in AI reviews; evidence gaps in AI-generated findings |
| "Code Review Anti-Patterns in Practice" (FSE 2026) | Documented anti-patterns: rubber-stamping, drive-by comments, over-scoping, confirmation bias |
| "ITIL 4 and DevOps: A Practical Integration" (AXELOS, 2023) | Change enablement + DevOps CI/CD pipeline integration |
| "Detecting Security-Relevant Code Reviews" (IEEE S&P 2026) | Domain routing for security-sensitive changes; specialist matching |

## Coverage honesty

**Layer 1 (regex) rules** cover codifiable review anti-patterns with high
precision: rubber-stamping language, P1-approval contradictions. They do NOT
cover review quality dimensions requiring judgement -- scope appropriateness,
evidence sufficiency, or correctness of the review itself.

Most code-review rules are **teaching-only** (no `check_*`). They are designed
to be injected as behavioral guardrails at LLM generation time, not as
deterministic checkers. An LLM that follows these rules produces higher-quality
code reviews.

The honest coverage boundary:
- ~20% of review quality is codifiable at Layer 1 (obvious anti-patterns)
- ~80% requires teaching + judgement (scope depth, evidence quality, tone,
  domain knowledge)

## Verification

Rules with `check_regex` are FAIL/PASS tested in
`tests/test_code_review.py`. Teaching-only rules (no checker) are tested for
content presence only via syllabus loading. A rule ships with at minimum its
FAIL/PASS framework examples -- there is always something a student can learn
from.
