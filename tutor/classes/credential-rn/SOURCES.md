# SOURCES — credential-rn (Registered Nurse Professional Standards)

All rules in `class.yaml` derive from nursing professional standards, federal
regulations, and patient safety guidelines. Every rule cites its specific
source. No rule exists without a source.

## Primary standards

### ANA Code of Ethics for Nurses (2015)
- **American Nurses Association, Code of Ethics for Nurses with Interpretive
  Statements (2015).**
  <https://www.nursingworld.org/coe-view-only>
- Nine provisions covering: compassion and respect (Provision 1), primary
  commitment to the patient (Provision 2), patient advocacy (Provision 3),
  authority and accountability (Provision 4), duty to self (Provision 5),
  improvement of healthcare environments (Provision 6), advancement of the
  profession (Provision 7), collaboration (Provision 8), and social justice
  (Provision 9).
- Rules cited: `code-of-ethics`, `confidentiality-hipaa`, `informed-consent`,
  `mandatory-reporting`, `cultural-competence`, `evidence-based-practice`,
  `professional-boundaries`.

### State Nurse Practice Acts (NPA)
- **National Council of State Boards of Nursing (NCSBN), Model Nursing Practice
  Act and Model Administrative Rules.**
  <https://www.ncsbn.org/nursing-regulation>
- State-specific scope of practice for RNs, LPNs/LVNs, and UAP.
- Delegation authority: RN retains accountability for all delegated tasks.
- Definitions of nursing practice, licensure requirements, grounds for
  discipline.
- Rules cited: `scope-of-practice`, `delegation`, `medication-administration`.

### HIPAA Privacy Rule
- **Health Insurance Portability and Accountability Act of 1996.**
  Privacy Rule at 45 CFR § 164.500-534.
  <https://www.hhs.gov/hipaa/for-professionals/privacy/index.html>
- Protected health information (PHI) in the healthcare setting: patient
  identifiers, medical records, treatment information, insurance data.
- Minimum necessary standard.
- Rules cited: `confidentiality-hipaa`, `professional-boundaries`.

### NPSG (National Patient Safety Goals)
- **The Joint Commission, National Patient Safety Goals (2026).**
  <https://www.jointcommission.org/standards/national-patient-safety-goals/>
- Goal 1: Identify patients correctly (two patient identifiers).
- Goal 2: Improve staff communication (report critical results in a timely
  manner).
- Goal 3: Use medications safely (label all medications, reconcile medications,
  anticoagulation safety).
- Goal 7: Reduce the risk of healthcare-associated infections (hand hygiene,
  CLABSI, SSI, CAUTI).
- Goal 15: Prevent patient falls.
- Goal 16: Prevent pressure injuries.
- Rules cited: `patient-safety`, `medication-administration`, `documentation-
  quality`, `critical-reporting`.

### CDC Guidelines
- **Centers for Disease Control and Prevention.**
  <https://www.cdc.gov/infectioncontrol/guidelines/>
- Standard precautions: hand hygiene, PPE, safe injection practices,
  respiratory hygiene, environmental cleaning.
- Transmission-based precautions: contact, droplet, airborne.
- Healthcare-associated infection prevention guidelines.
- Rules cited: `infection-control`, `evidence-based-practice`.

### ANA Scope and Standards of Practice (2021)
- **American Nurses Association, Nursing: Scope and Standards of Practice
  (4th Edition, 2021).**
- 18 standards of practice and professional performance.
- Standards cover: assessment, diagnosis, outcomes identification, planning,
  implementation, coordination of care, health teaching and health promotion,
  evaluation, ethics, culturally congruent practice, communication,
  collaboration, leadership, education, evidence-based practice and research,
  quality of practice, professional practice evaluation, resource utilization,
  and environmental health.
- Rules cited: `documentation-standards`, `documentation-quality`,
  `patient-education`, `cultural-competence`, `evidence-based-practice`,
  `critical-reporting`.

### Joint Commission Hospital Standards
- **The Joint Commission, Comprehensive Accreditation Manual for Hospitals
  (CAMH) (2026).**
- Standards for: patient rights and organizational ethics, record of care
  (documentation), infection prevention and control, medication management,
  provision of care and treatment, and transplant safety.
- Informed consent requirements, patient education standards, restraint and
  seclusion standards.
- Rules cited: `informed-consent`, `patient-education`, `documentation-standards`.

### Supporting standards

| Standard | Coverage |
|----------|----------|
| OSHA Bloodborne Pathogens Standard (29 CFR 1910.1030) | Standard precautions, PPE, needlestick prevention |
| NCSBN National Guidelines for Nursing Delegation (2016) | Five rights of delegation, RN accountability, delegation decision tree |
| ANA Principles for Delegation (2019) | RN accountability, delegation vs assignment, supervision expectations |
| ISMP Medication Safety Guidelines | Five rights, high-alert medications, LASA drug safety |
| NPUAP/EPUAP Pressure Injury Prevention Guidelines | Braden Scale, repositioning schedules, support surfaces |
| CDC Clinical Practice Guideline for Prescribing Opioids | Pain assessment and management standards |
| HHS National CLAS Standards | Culturally and linguistically appropriate services, interpreter requirements |
| The Joint Commission Sentinel Event Policy | Root cause analysis, reporting, disclosure |
| WHO Surgical Safety Checklist | Pre-operative verification, site marking, time-out |
| ANA Position Statements (various) | Ethical considerations: end-of-life, social media, nurse fatigue, staffing |

## Per-rule citation table

| Rule id | Primary Authority | Secondary Authority | Notes |
|---------|------------------|---------------------|-------|
| `scope-of-practice` | State NPA, ANA Scope & Stds | NCSBN Model Act | AI cannot possess nursing license; must disclose AI status; cannot assess/diagnose/treat |
| `confidentiality-hipaa` | HIPAA 45 CFR 164 | ANA Code of Ethics Prov. 3 | PHI protection; minimum necessary; de-identification; duty survives discharge/death |
| `documentation-quality` | ANA Scope & Stds (Std 12) | Joint Commission CAMH | Complete entries; no placeholder brackets; specific clinical data required |
| `medication-administration` | State NPA, facility policy | ISMP, Joint Commission NPSG.03.04.01, NPSG.03.05.01 | Five Rights (Patient, Drug, Dose, Route, Time); two identifiers; MAR documentation |
| `infection-control` | CDC Guidelines | OSHA 29 CFR 1910.1030 | Standard + transmission-based precautions; hand hygiene; PPE; safe injection |
| `delegation` | State NPA, NCSBN Delegation Guidelines | ANA Principles for Delegation | Five Rights of Delegation; RN retains accountability; non-delegable tasks |
| `patient-safety` | Joint Commission NPSG (Goals 1,2,3,7,15,16) | ANA Code of Ethics Prov. 3 | Fall prevention; pressure injury prevention; two identifiers; med reconciliation |
| `informed-consent` | State law, Joint Commission | ANA Code of Ethics Prov. 1, 3 | Capacity; voluntary; risks/benefits/alternatives; right to refuse; RN witness role |
| `mandatory-reporting` | State mandatory reporting laws | ANA Code of Ethics Prov. 3 | Child/elder abuse; communicable disease; sentinel events; good-faith immunity |
| `patient-education` | ANA Scope & Stds (Std 13) | Joint Commission CAMH | Health literacy; teach-back method; plain language; readiness to learn |
| `cultural-competence` | ANA Code of Ethics Prov. 1; CLAS Standards | Joint Commission, ANA Scope & Stds | Professional interpreters; cultural humility; religious accommodations; modesty |
| `critical-reporting` | Joint Commission NPSG Goal 2 | ANA Scope & Stds (Std 11) | Critical lab values; ISBAR communication; rapid response activation |
| `documentation-standards` | ANA Scope & Stds (Std 12) | Joint Commission CAMH | Timely, accurate, complete, objective; proper error correction; no pre/back-charting |
| `evidence-based-practice` | ANA Code of Ethics Prov. 7 | ANA Scope & Stds (Std 15) | Research-based care; clinical practice guidelines; Cochrane/JBI; evaluate evidence strength |
| `professional-boundaries` | ANA Code of Ethics Prov. 2 | State NPA, NCSBN | Therapeutic relationship; dual relationships; social media; accessing records without need |
| `code-of-ethics` | ANA Code of Ethics (2015) — all 9 provisions | State NPA, facility ethics policies | Nine provisions; ethical decision-making framework; patient advocacy; integrity |

## Key research and commentary

| Source | Relevance |
|--------|-----------|
| *American Journal of Nursing* (AJN) | Nursing research, best practices, continuing education |
| *Journal of Nursing Regulation* (JONR) — NCSBN | Regulatory updates, scope of practice, delegation standards |
| *The Online Journal of Issues in Nursing* (OJIN) — ANA | Ethical issues, professional practice, health policy |
| NCSBN Environmental Scan (2026) | Regulatory trends, technology in nursing, workforce issues |
| "AI in Nursing: Opportunities and Ethical Considerations" (2025) | AI applications in clinical decision support, documentation, patient monitoring |
| "The Role of AI in Clinical Documentation" — *CIN: Computers, Informatics, Nursing* (2025) | AI-assisted charting, documentation quality, risk of automation bias |
| *Institute for Healthcare Improvement* (IHI) | Patient safety frameworks, quality improvement, SBAR communication |
| "Health Literacy Universal Precautions Toolkit" (AHRQ, 3rd Ed.) | Plain language, teach-back, patient education materials |
| ANA Social Media Best Practices for Nurses | Maintaining professional boundaries online; HIPAA in digital contexts |
| *Evidence-Based Practice in Nursing*, Melnyk & Fineout-Overholt | EBP process, PICOT questions, evidence hierarchy |
| Joint Commission Quick Safety Advisories | Current patient safety issues, sentinel event analyses |
| *Agency for Healthcare Research and Quality* (AHRQ) Patient Safety Network | Patient safety resources, culture of safety, teamwork and communication |
| *Sigma Theta Tau International* (Honor Society of Nursing) | Nursing research dissemination, evidence-based practice resources |
| Standards of Practice for Culturally Competent Nursing Care (2024) | CLAS standards implementation, interpreter services, cultural assessment |

## Coverage honesty

**Checkable rules (6):** `scope-of-practice`, `confidentiality-hipaa`,
`documentation-quality`, `medication-administration`, `infection-control`,
`delegation`.

These are codifiable as regex patterns that detect specific text-based
violations: claiming registered nurse credentials, exposing PHI with patient
identifiers, using placeholder brackets in clinical documentation, skipping
the five rights of medication administration, bypassing infection control
precautions, and delegating RN-level judgment tasks to unlicensed personnel
or LPNs.

They are high precision but narrow — they detect specific known-bad text
patterns but do not evaluate whether the AI's overall clinical reasoning is
sound.

**Teaching-only rules (10):** Patient safety, informed consent, mandatory
reporting, patient education, cultural competence, critical reporting,
documentation standards, evidence-based practice, professional boundaries,
and code of ethics. These require contextual or compositional clinical
judgment and are evaluated by the LLM judge (Layer 2) or the Socratic fix
step.

**What is NOT covered:** Full nursing practice requires knowledge of
state-specific scope-of-practice regulations, institutional policies, clinical
expertise for complex patient cases, and professional judgment on ethical
questions. This class teaches an LLM to recognize the most common registered
nurse professional standards and to follow them at generation time. It does
not certify the AI to practice nursing or replace a licensed registered
nurse's clinical judgment.

## Verification

Each rule with `check_regex` is FAIL/PASS tested in
`tests/test_credential_rn.py`. Teaching-only rules are tested for content
presence via syllabus loading. A rule cannot ship without its test pair.
