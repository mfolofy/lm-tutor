# SOURCES — audit (Audit & Compliance Evidence Standards)

All rules in `class.yaml` derive from the following compliance frameworks
and standards. Every rule cites its specific control or section. No rule
exists without a source.

## Primary standards

### SOC2 — AICPA Trust Services Criteria (2017)
- **AICPA Trust Services Criteria** (TSC 2017) — Security, Availability,
  Processing Integrity, Confidentiality, Privacy.
- <https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2>
- Controls cited: CC6.1, CC6.2, CC6.3, CC6.6, CC7.1, CC7.2, A1.2, C1.1

### HIPAA Security Rule — 45 CFR Part 164 Subpart C
- **HIPAA Security Rule** (2003, updated 2013 via Omnibus Rule).
- <https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-C>
- Controls cited: 164.312(a)(1), 164.312(a)(2)(iv), 164.312(b), 164.312(c)(1),
  164.312(d), 164.308(a)(1)(ii)(D)

### CMMC 2.0 — NIST SP 800-171 Rev 2 aligned
- **Cybersecurity Maturity Model Certification 2.0** (DoD, 2021).
- Level 2 aligns with NIST SP 800-171 (110 controls).
- <https://www.acq.osd.mil/cmmc/>
- Controls cited: AC.L2-3.1.1, AC.L2-3.1.2, AC.L2-3.1.5, AU.L2-3.3.1,
  AU.L2-3.3.8, IA.L2-3.5.1, SC.L2-3.13.11, SC.L2-3.13.15

### NIST SP 800-53 — Security and Privacy Controls
- **NIST Special Publication 800-53 Rev 5** (2020).
- <https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final>
- Overlaps with CMMC controls; referenced for access control (AC), audit and
  accountability (AU), and system and communications protection (SC) families.

### Supporting sources
- **ISO 27001:2022** — Annex A controls for ISMS. Referenced for segregation of
  duties (A.5.2), logging (A.8.15), and auditor access (A.5.9).
- **NIST CSF** — Cybersecurity Framework (2018, updated 2024). Referenced for
  evidence collection and incident response patterns.
- **Ghost Mesh Compliance Framework** — Reference implementation at
  `projects/ghost_mesh/compliance/` covering SOC2 (8 controls), HIPAA
  (6 controls), and CMMC 2.0 (8 controls) with automated checks and evidence
  export. See `frameworks.py`, `check.py`, `exporter.py`.

## Per-rule citation table

| Rule id | Framework | Control/Section | Notes |
|---------|-----------|-----------------|-------|
| `hardcoded-secrets` | SOC2, CMMC | CC6.1, AC.L2-3.1.1 | Secrets management as access control |
| `audit-logging-disabled` | SOC2, HIPAA, CMMC | CC7.1, 164.312(b), AU.L2-3.3.1 | Logging is foundational to all audit |
| `weak-crypto` | HIPAA, SOC2 | 164.312(a)(2)(iv), CC6.1 | Approved crypto per NIST SP 800-175B |
| `world-readable` | SOC2, CMMC | CC6.1, AC.L2-3.1.1 | File permissions as access control |
| `missing-encryption` | HIPAA, SOC2 | 164.312(a)(2)(iv), C1.1 | Encryption for confidentiality |
| `single-operator-mode` | SOC2, HIPAA, CMMC | CC6.6, 164.312(d), AC.L2-3.1.5 | Dual-control for break-glass |
| `chain-verification-off` | HIPAA, CMMC | 164.312(c)(1), AU.L2-3.3.8 | Integrity verification |
| `evidence-integrity` | SOC2, HIPAA, CMMC | CC5.2, 164.312(c)(1), AU.L2-3.3.8 | WORM storage + signing |
| `sod-violation` | SOC2, CMMC, ISO 27001 | CC6.1, AC.L2-3.1.5, A.5.2 | Segregation of duties |
| `chain-of-custody` | SOC2, HIPAA, NIST SP 800-53 | CC8.1, 164.312(b), AU-3 | Evidence provenance |
| `soc2-security` | SOC2 | CC6.1-6.3, CC7.1-7.2 | Security principle |
| `soc2-availability` | SOC2 | CC7.1, A1.2 | Availability principle |
| `soc2-confidentiality` | SOC2 | C1.1 | Confidentiality principle |
| `hipaa-audit-controls` | HIPAA | 164.312(b) | Audit controls for ePHI |
| `cmmc-level2` | CMMC 2.0 | Multiple (110 controls) | Level 2 audit requirements |
| `evidence-collection` | SOC2, HIPAA, CMMC | Cross-framework | Evidence bundle patterns |
| `retention-policy` | SOC2, HIPAA, CMMC | A1.2, 164.308(a)(1)(ii)(D) | Evidence retention |
| `common-audit-failures` | Cross-framework | — | Compiled from Ghost Mesh compliance audits |
| `auditor-role` | SOC2, ISO 27001, CMMC | CC6.1, A.5.9, AU.L2-3.3.8 | Read-only auditor access |

## Reference implementation

Ghost Mesh ships a complete compliance framework at `projects/ghost_mesh/compliance/`:

- **`frameworks.py`** — 22 control mappings across SOC2 (8), HIPAA (6), CMMC 2.0 (8)
- **`check.py`** — Automated compliance checks: `_check_agents_have_certs()`,
  `_check_heartbeats_recent()`, `_check_integrity()`, `_check_red_key_dual()`,
  `_check_baa_template()`, and others. Each returns `(status, detail)`.
- **`exporter.py`** — Evidence bundle ZIP generation with manifest, audit trail,
  control mapping, agent inventory, PKI summary, NTP logs, red key log, chain
  integrity report, and architecture overview.

The Ghost Mesh implementation demonstrates how the rules in this class are
applied: PKI enforcement for agent identity, WORM chain for audit integrity,
dual-approval for break-glass access, and evidence export for auditor review.

## Coverage honesty

**Checkable rules (8):** `hardcoded-secrets`, `audit-logging-disabled`,
`weak-crypto`, `world-readable`, `missing-encryption`, `single-operator-mode`,
`chain-verification-off` — these are codifiable as regex patterns that detect
common config/code anti-patterns. They are high precision but narrow — they
detect known-bad patterns but do not prove overall compliance.

**Teaching-only rules (11):** Evidence concepts, SOC2 principles, HIPAA audit
controls, CMMC requirements, chain of custody, segregation of duties — these
require judgement and contextual understanding. They are evaluated by the LLM
judge (Layer 2) or the Socratic fix step, not by deterministic regex.

**What is NOT covered:** Full compliance against any framework requires
thousands of controls. This class teaches the LLM to recognize the most common
anti-patterns and to structure evidence properly. It does not replace a
compliance officer or a full audit tool.
