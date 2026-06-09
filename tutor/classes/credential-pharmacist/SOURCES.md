# SOURCES — credential-pharmacist (Pharmacy Professional Standards)

All rules in `class.yaml` derive from federal regulations, USP standards, and
pharmacy practice guidelines. Every rule cites its specific source. No rule
exists without a source.

## Primary standards

### OBRA '90 (Omnibus Budget Reconciliation Act of 1990)
- **Omnibus Budget Reconciliation Act of 1990, Pub. L. 101-508, § 4401.**
  Codified at 42 U.S.C. § 1396r-8.
- Established prospective and retrospective DUR requirements for Medicaid
  (later adopted as standard of care across all payers).
- Requires offer to counsel each patient on new prescriptions.
- Rules cited: `patient-counseling`, `drug-interactions`, `dosage-verification`.

### HIPAA Privacy Rule
- **Health Insurance Portability and Accountability Act of 1996.**
  Privacy Rule at 45 CFR § 164.500–534.
  <https://www.hhs.gov/hipaa/for-professionals/privacy/index.html>
- Protected health information (PHI) in the pharmacy setting: medication
  records, patient health information, insurance data, patient identities.
- Minimum necessary standard.
- Rules cited: `confidentiality`.

### DEA Regulations (21 CFR 1300-1399)
- **Controlled Substances Act (21 U.S.C. § 801-971).**
  Implementing regulations at 21 CFR Parts 1300-1399.
  <https://www.deadiversion.usdoj.gov/21cfr/>
- Schedule definitions: C-II (no refills), C-III/C-IV (5 refills/6 months).
- DEA number verification (check-digit algorithm).
- Separate recordkeeping for C-II.
- Suspicious order reporting.
- Rules cited: `controlled-substances`, `prescription-verification`.

### USP 795 — Non-Sterile Compounding
- **United States Pharmacopeia General Chapter 795: Pharmaceutical
  Compounding — Non sterile Preparations.**
- Beyond-use dating based on water activity and stability data.
- Master formula records, compounding records.
- Labeling requirements for compounded preparations.
- Rules cited: `compounding`.

### USP 797 — Sterile Compounding
- **United States Pharmacopeia General Chapter 797: Pharmaceutical
  Compounding — Sterile Preparations.**
- ISO-classified compounding environments (ISO Class 5 primary engineering
  controls).
- Garbing, hand hygiene, surface decontamination.
- Environmental monitoring (viable and non-viable particle sampling).
- Personnel competency testing (gloved fingertip, media fill).
- Beyond-use dating by risk level (Category 1, 2, 3).
- Rules cited: `compounding`.

### FDA Guidelines
- **Food and Drug Administration.**
  <https://www.fda.gov/drugs>
- Drug labeling requirements (21 CFR 201).
- MedWatch adverse event reporting.
- Generic drug approval and therapeutic equivalence ratings (Orange Book).
- Rules cited: `label-accuracy`, `error-reporting`, `substitution-guidelines`.

### ISMP Guidelines
- **Institute for Safe Medication Practices.**
  <https://www.ismp.org/>
- Medication Error Reporting Program (MERP).
- High-alert medication lists.
- Look-alike, sound-alike (LASA) drug naming.
- Tall-man lettering recommendations.
- Non-punitive error reporting culture.
- Rules cited: `error-reporting`, `label-accuracy`.

### State Pharmacy Practice Acts
- **National Association of Boards of Pharmacy (NABP) Model State Pharmacy
  Act and Model Rules.**
- State-specific scope of practice for pharmacists.
- Pharmacist immunization authority (varies by state).
- Collaborative practice agreements.
- Pharmacy technician supervision ratios.
- Rules cited: `immunization`, `scope-of-practice`, `substitution-guidelines`.

### Supporting standards

| Standard | Coverage |
|----------|----------|
| CDC / ACIP Adult and Child Immunization Schedules | Vaccine eligibility, contraindication screening |
| The Joint Commission National Patient Safety Goals | Medication reconciliation (NPSG.03.06.01) |
| AMA / ASHP Guidelines on Medication Reconciliation | Transitions of care, discrepancy resolution |
| USP <1160> — Pharmacy Compounding of Sterile Preparations | Personnel training and competency |
| Orange Book (FDA Approved Drug Products with Therapeutic Equivalence) | AB ratings, generic substitution guidance |
| FDA MedWatch: The FDA Safety Information and Adverse Event Reporting Program | ADR and product problem reporting |
| Drug Enforcement Administration Pharmacist's Manual | DEA compliance for controlled substance dispensing |
| Pharmacy Times / Pharmacy Today | Continuing education, practice updates |
| ASHP Guidelines on Pharmacist-Conducted Patient Education and Counseling | Counseling standards and communication |

## Per-rule citation table

| Rule id | Primary Authority | Secondary Authority | Notes |
|---------|------------------|---------------------|-------|
| `pharmacist-disclaimer` | State Pharmacy Practice Acts | NABP Model Act | AI cannot hold pharmacy license; must disclose AI status |
| `scope-of-practice` | State Pharmacy Practice Acts | NABP Model Act | AI cannot dispense, prescribe, or replace pharmacist |
| `prescription-verification` | DEA 21 CFR 1306 | State pharmacy acts | Verify identity, drug, dose, prescriber, DEA number, date; check for forgeries |
| `drug-interactions` | OBRA '90 DUR requirements | FDA labeling, USP DI | CYP450, QTc, serotonin syndrome, pharmacodynamic interactions |
| `dosage-verification` | OBRA '90 DUR requirements | FDA labeling, Lexicomp/UpToDate | Renal/hepatic adjustments; age, weight, indication appropriateness |
| `controlled-substances` | DEA 21 CFR 1300-1399 | CSA (21 USC 801-971), DEA Pharmacist's Manual | C-II no refills, C-III/V 5 refills/6mo, DEA check-digit, suspicious orders |
| `patient-counseling` | OBRA '90 § 4401 | ASHP Counseling Guidelines | Offer to counsel each new Rx; discuss name, directions, side effects, storage |
| `allergy-screening` | State pharmacy practice acts, Standard of care | FDA labeling, AAAAI guidelines | True allergy vs intolerance vs side effect; cross-reactivity within drug classes |
| `label-accuracy` | FDA 21 CFR 201 | State pharmacy acts, USP <17> | Patient name, drug/strength, directions, prescriber, pharmacy, date, refills, warnings |
| `immunization` | State pharmacy practice acts | CDC/ACIP schedules, Public Readiness and Emergency Preparedness Act (PREP Act) | Patient eligibility, consent, VIS, observation, registry reporting |
| `compounding` | USP 795, USP 797 | FDA 503A/503B, state BOP rules | Non-sterile (795): BUD, batch records. Sterile (797): ISO 5, garb, monitoring |
| `confidentiality` | HIPAA Privacy Rule (45 CFR 164) | HHS OCR guidance | PHI protection, minimum necessary, patient authorization required |
| `error-reporting` | FDA MedWatch | ISMP MERP, The Joint Commission | Non-punitive culture, root cause analysis, system improvements |
| `medication-reconciliation` | The Joint Commission NPSG.03.06.01 | ASHP Guidelines | Transitions of care, discrepancy resolution, include OTC/herbals |
| `substitution-guidelines` | FDA Orange Book | State pharmacy acts, NABP | AB-rated generic substitution, NTI drugs, DAW codes, therapeutic interchange |

## Key research and commentary

| Source | Relevance |
|--------|-----------|
| *Pharmacy Times* (ongoing CE) | Continuing pharmacy education and practice updates |
| *Drug Topics* (ongoing) | Pharmacy news, regulatory changes, professional practice |
| ASHP Guidelines on Pharmacy Practice in Health Systems | Health-system pharmacy standards and medication-use process |
| "The Pharmacist's Role in Medication Safety" (ISMP, 2023) | Error prevention strategies, high-alert medications |
| "The Role of AI in Pharmacy" — *Journal of the American Pharmacists Association* (2025) | AI applications in pharmacy: DUR, counseling, interaction screening |
| "AI in Clinical Decision Support: Pharmacy Applications and Limitations" (2025) | Scope boundaries for AI-assisted pharmacy practice |
| NABP Survey of Pharmacy Law (2026) | State-by-state pharmacy practice variations |
| DEA Pharmacist's Manual (2025 edition) | CS dispensing, recordkeeping, diversion prevention |
| *Institute for Safe Medication Practices* quarterly Hazard Alerts | Emerging medication safety issues |
| FDA Drug Safety Communications | Active safety alerts and labeling changes |
| American Pharmacists Association (APhA) Immunization Certificate Program | Immunization training standards for pharmacists |
| Board of Pharmacy Specialties (BPS) | Specialty certification: pharmacotherapy, ambulatory care, critical care, etc. |
| *Pharmacotherapy: A Pathophysiologic Approach*, DiPiro et al. | Clinical pharmacy foundational text |

## Coverage honesty

**Checkable rules (5):** `pharmacist-disclaimer`, `confidentiality`,
`label-accuracy`, `prescription-verification`, `controlled-substances`.

These are codifiable as regex patterns that detect specific text-based
violations: claiming pharmacist credentials, exposing PHI with identifiers,
using placeholder brackets on labels, dispensing without verification, and
proposing illegal C-II refills or early fills of controlled substances.

They are high precision but narrow — they detect specific known-bad text
patterns but do not evaluate whether the AI's overall clinical reasoning is
sound.

**Teaching-only rules (10):** Scope of practice, drug interactions, dosage
verification, patient counseling, allergy screening, immunization, compounding,
error reporting, medication reconciliation, substitution guidelines. These
require contextual or compositional clinical judgment and are evaluated by the
LLM judge (Layer 2) or the Socratic fix step.

**What is NOT covered:** Full pharmacy practice requires knowledge of
state-specific regulations, institutional policies, clinical expertise for
complex patient cases, and professional judgment on clinical interventions.
This class teaches an LLM to recognize the most common pharmacy professional
standards and to follow them at generation time. It does not certify the AI to
practice pharmacy or replace a licensed pharmacist's clinical judgment.

## Verification

Each rule with `check_regex` is FAIL/PASS tested in
`tests/test_credential_pharmacist.py`. Teaching-only rules are tested for
content presence via syllabus loading. A rule cannot ship without its test pair.
