# SOURCES — credential-paramedic (Paramedic / EMS Professional Standards)

All rules in `class.yaml` derive from paramedic professional standards, federal
regulations, and patient safety guidelines. Every rule cites its specific
source. No rule exists without a source.

## Primary standards

### NREMT Paramedic National Standards
- **National Registry of Emergency Medical Technicians (NREMT), Paramedic
  National Standards / Paramedic Certification Renewal.**
  <https://www.nremt.org>
- Covers: paramedic scope of practice, national EMS education standards,
  psychomotor competency requirements, cognitive exam domains (airway,
  cardiology, trauma, medical, obstetrics/gynecology, pediatrics, EMS
  operations).
- Rules cited: `scope-of-practice`, `airway-management`, `cardiac-care`,
  `patient-assessment`, `triage-communications`, `continuing-education`.

### State EMS Protocols
- **Individual state EMS authority (e.g., state department of health, EMS
  bureau). Varies by jurisdiction.**
- State-specific protocols covering: scope of practice for EMR, EMT, AEMT,
  and paramedic levels; treatment algorithms; drug formularies; medical
  direction requirements; transport destination guidelines; refusal of care
  standards; and mandatory continuing education.
- Rules cited: `protocol-adherence`, `scope-of-practice`, `medical-direction`,
  `controlled-substances`, `refusal-transport`, `spinal-motion-restriction`.

### NHTSA EMS Agenda for the Future (2008)
- **National Highway Traffic Safety Administration, EMS Agenda for the Future
  (2008) and EMS Education Agenda for the Future (2008).**
  <https://www.ems.gov>
- Vision for EMS as a community-based health management system integrated
  with other healthcare providers and public health agencies.
- 14 attributes: integration of health services, EMS research, legislation and
  regulation, system finance, human resources, medical direction, education
  systems, public education, prevention, public access, communication systems,
  clinical care, information systems, and evaluation.
- Rules cited: `continuing-education`, `triage-communications`,
  `medical-direction`.

### HIPAA Privacy Rule
- **Health Insurance Portability and Accountability Act of 1996.**
  Privacy Rule at 45 CFR 164.500-534.
  <https://www.hhs.gov/hipaa/for-professionals/privacy/index.html>
- Protected health information (PHI) in the healthcare setting: patient
  identifiers, medical records, treatment information, insurance data.
- Minimum necessary standard.
- Prehospital-specific considerations: radio and verbal reporting must also
  comply with HIPAA; incident location and time can be identifying.
- Rules cited: `patient-confidentiality`, `documentation-quality`.

### DEA Regulations (21 CFR 1300)
- **Drug Enforcement Administration, Controlled Substances Act Regulations.**
  <https://www.deadiversion.usdoj.gov>
- Registration requirements, recordkeeping, security requirements for
  controlled substances.
- Inventory and biennial inventory requirements.
- Disposal and wastage requirements: witnessed destruction, documentation.
- Rules cited: `controlled-substances`.

### Local Medical Director Protocols
- **EMS agency medical director — written patient care protocols, policies,
  and standing orders.**
- Specific to each EMS agency. Establishes the medical-legal standard of care
  for providers in that system.
- Medical director determines: drug formulary, protocol content, online
  medical direction procedures, QI/QA processes, provider credentialing,
  skill maintenance requirements, and scope deviations.
- Rules cited: `protocol-adherence`, `medical-direction`, `controlled-
  substances`, `refusal-transport`, `equipment-readiness`.

### AHA Guidelines for CPR and ECC
- **American Heart Association, Guidelines for CPR and Emergency
  Cardiovascular Care.**
  <https://cpr.heart.org>
- Updated every 5 years. Covers: high-quality CPR metrics, cardiac arrest
  algorithms (VF/VT, PEA/asystole), post-arrest care, acute coronary
  syndromes, stroke, and special resuscitation situations.
- Rules cited: `cardiac-care`, `airway-management`.

## Supporting standards

| Standard | Coverage |
|----------|----------|
| National EMS Scope of Practice Model (2019) | Defines four levels: EMR, EMT, AEMT, paramedic; sets national scope boundaries |
| NREMT Paramedic Psychomotor Competency Portfolio | Airway, cardiology, trauma, medical, obstetrics, pediatrics, EMS operations skill sheets |
| CDC National Violent Death Reporting System (NVDRS) | Mandatory reporting of violent injury patterns |
| OSHA Bloodborne Pathogens Standard (29 CFR 1910.1030) | BSI, standard precautions, PPE, needlestick prevention |
| START / JumpSTART Triage Systems | Pediatric and adult mass casualty triage algorithms |
| NEXUS Criteria (N Engl J Med 2000) | Clinical decision rule for cervical spine imaging after trauma |
| Canadian C-Spine Rule (JAMA 2001) | Clinical decision rule for c-spine imaging in alert, stable trauma patients |
| CDC Guidelines for Field Triage of Injured Patients | Trauma center transport decision guidelines (physiologic, anatomic, mechanism, special considerations) |
| ISBAR Communication Tool | Standardized handoff communication framework (Identify, Situation, Background, Assessment, Recommendation) |
| NAEMT EMS Medicine | Evidence-based clinical practice updates for paramedics |
| National EMS Quality Alliance (NEMSQA) Measures | Quality measure set for EMS system performance |
| EMS Research Network (EMSARN) / NHTSA Office of EMS | Research and evidence translation into EMS practice |
| Federal EMS Funding (DOT HS 811 723) | EMS system funding and legislative framework |
| The Joint Commission Sentinel Event Policy | Root cause analysis, reporting, disclosure |
| HHS National CLAS Standards | Culturally and linguistically appropriate services — applicable to prehospital care |
| State mandatory reporting laws (vary by jurisdiction) | Child abuse, elder abuse, domestic violence, infectious disease reporting |

## Per-rule citation table

| Rule id | Primary Authority | Secondary Authority | Notes |
|---------|------------------|---------------------|-------|
| `scope-of-practice` | NREMT Paramedic Standards, State NPA | National Scope of Practice Model (2019) | AI cannot possess EMS certification; must disclose AI status; cannot assess/treat; cannot replace paramedic/EMT |
| `patient-confidentiality` | HIPAA 45 CFR 164 | State privacy laws, ANA Code of Ethics | PHI protection; minimum necessary; de-identification; prehospital-specific identity risks |
| `documentation-quality` | State EMS protocols, NREMT standards | HIPAA, Joint Commission CAMH | PCR as legal document; no placeholder brackets; complete documentation required |
| `controlled-substances` | DEA 21 CFR 1300 | State EMS protocols, local medical director | Narcotic accountability; witnessed wasting; controlled substance logs; end-of-shift counts |
| `refusal-transport` | State EMS protocols, NREMT standards | Local medical director protocols, legal precedent | Capacity assessment; informed refusal; risks explained; online medical consult; documentation |
| `equipment-readiness` | State EMS protocols, local medical director | NHTSA EMS Operations, OSHA regulations | Daily truck check; expiration verification; restock after each call; documentation of equipment checks |
| `protocol-adherence` | State EMS protocols, local medical director | NREMT standards, National Scope of Practice Model | Standing orders; protocol limits; paramedic discretion; online medical direction for deviations |
| `patient-assessment` | NREMT Paramedic Standards | State EMS protocols, NHTSA | ABCDE primary survey; SAMPLE/OPQRST; vital signs; continuous reassessment |
| `airway-management` | NREMT Paramedic Standards | AHA Guidelines, National Scope of Practice Model | Basic and advanced airway; OPA/NPA/BVM; ET intubation; supraglottic airway; capnography |
| `cardiac-care` | AHA Guidelines for CPR and ECC | NREMT standards, State protocols | High-quality CPR; 12-lead ECG interpretation; cardiac arrest algorithms; Hs and Ts; post-arrest care |
| `medical-direction` | State EMS protocols, local medical director | NHTSA EMS Agenda, NREMT standards | Online vs offline medical direction; standing orders; paramedic discretion; documentation of physician orders |
| `mandatory-reporting` | State mandatory reporting laws | CDC NVDRS, NREMT standards | Child/elder abuse; violent injuries; communicable disease; good-faith immunity |
| `scene-safety` | NREMT standards, OSHA 29 CFR 1910.1030 | State protocols, NFPA standards | BSI; situational awareness; violence potential; hazmat; law enforcement coordination; staging |
| `spinal-motion-restriction` | NEXUS Criteria / Canadian C-Spine Rule | State protocols, NREMT standards | Clinical decision rules; appropriate immobilization; risks of prolonged immobilization; reassessment |
| `triage-communications` | NHTSA EMS Agenda, NREMT standards | ISBAR; START/JumpSTART; State protocols | Radio report structure; ISBAR handoff; mass casualty triage; professional communication |
| `continuing-education` | NREMT Recertification Requirements | State relicensure, NHTSA EMS Agenda, AHA updates | CE documentation; protocol currency; AHA guideline updates; equipment training; knowledge limitations of AI |

## Key research and commentary

| Source | Relevance |
|--------|-----------|
| *Prehospital Emergency Care* (NAEMSP journal) | EMS research, clinical practice updates, system design |
| *Journal of Emergency Medical Services* (JEMS) | Current EMS news, case reviews, protocol updates |
| *Annals of Emergency Medicine* | Emergency medicine research informing prehospital care |
| *Resuscitation* | Cardiac arrest research, CPR quality studies, post-arrest care |
| NREMT Practice Analysis (updated every 5 years) | National scope-of-practice task analysis for all certification levels |
| *EMS World* | EMS operations, continuing education, equipment reviews |
| NAEMT Position Papers | Ethical issues, safety culture, violence against EMS, fatigue management |
| *Prehospital and Disaster Medicine* (WADEM) | Mass casualty, disaster response, triage research |
| Institute of Medicine, *EMS at the Crossroads* (2006) | Foundational report on EMS system design, workforce, and patient safety |
| FEMA / DHS National Incident Management System (NIMS) | Incident command system (ICS) for multi-agency response |
| NHTSA National EMS Education Standards (2021) | Curriculum content for EMT and paramedic initial education |
| NAEMSP / ACEP Clinical Guidelines | Evidence-based prehospital treatment guidelines |
| *Western Journal of Emergency Medicine* | Emergency and EMS research, protocol outcomes |
| "AI in Emergency Medical Services: Opportunities and Ethical Considerations" (2025) | AI applications in dispatch, decision support, documentation in the prehospital setting |
| AHRQ Patient Safety Network — EMS Safety | Safety culture, fatigue, ambulance crashes, patient handling injuries |

## Coverage honesty

**Checkable rules (6):** `scope-of-practice`, `patient-confidentiality`,
`documentation-quality`, `controlled-substances`, `refusal-transport`,
`equipment-readiness`.

These are codifiable as regex patterns that detect specific text-based
violations: claiming paramedic/EMT credentials, exposing PHI with patient
identifiers, using placeholder brackets in PCR documentation, improper
controlled substance disposal/wasting, pressuring a patient into signing a
refusal without proper capacity assessment, and recommending skipping
equipment checks.

They are high precision but narrow — they detect specific known-bad text
patterns but do not evaluate whether the AI's overall clinical reasoning is
sound.

**Teaching-only rules (10):** Protocol adherence, patient assessment, airway
management, cardiac care, medical direction, mandatory reporting, scene
safety, spinal motion restriction, triage communications, and continuing
education. These require contextual or compositional clinical judgment and
are evaluated by the LLM judge (Layer 2) or the Socratic fix step.

**What is NOT covered:** Full paramedic/EMS practice requires knowledge of
state-specific protocols, local medical director policies, institutional
operating procedures, real-time protocol updates, clinical expertise for
complex multi-system patient presentations, and professional judgment on
ethical and operational questions. This class teaches an LLM to recognize the
most common paramedic professional standards and to follow them at generation
time. It does not certify the AI to practice as a paramedic or replace a
licensed EMS provider's clinical judgment.

## Verification

Each rule with `check_regex` is FAIL/PASS tested in
`tests/test_credential_paramedic.py`. Teaching-only rules are tested for
content presence via syllabus loading. A rule cannot ship without its test
pair.
