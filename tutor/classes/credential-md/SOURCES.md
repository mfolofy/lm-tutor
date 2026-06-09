# SOURCES — credential-md (Physician Medical Standards)

All rules in `class.yaml` derive from federal regulations, the AMA Code of
Medical Ethics, and established medical-legal doctrines. Every rule cites its
specific source. No rule exists without a source.

## Primary sources

### HIPAA Privacy Rule
- **Health Insurance Portability and Accountability Act of 1996 (HIPAA)** —
  Privacy Rule, 45 CFR § 164.500–534.
- <https://www.hhs.gov/hipaa/for-professionals/privacy/index.html>
- **Key provisions:** Definition of PHI (§ 164.501), minimum necessary standard
  (§ 164.502(b)), permitted uses and disclosures (§ 164.506–508), authorization
  requirements (§ 164.508), de-identification standard (§ 164.514).
- **Enforcement:** HHS Office for Civil Rights (OCR). Civil penalties up to
  $50,000 per violation, tiered by culpability (42 U.S.C. § 1320d-5).

### AMA Code of Medical Ethics
- **American Medical Association Code of Medical Ethics** — Current edition.
- <https://www.ama-assn.org/delivering-care/ama-code-medical-ethics>
- **Key opinions cited:**
  - Opinion 1.1.1 — Patient-Physician Relationship
  - Opinion 1.1.3 — Patient Rights (includes second opinions)
  - Opinion 1.2.1 — Respect for Patient Beliefs, Culture, Values
  - Opinion 2.1.1 — Informed Consent
  - Opinion 2.1.3 — Withholding Information / Therapeutic Privilege
  - Opinion 2.2.1 — Truthful Communications / Medical Records
  - Opinion 3.1.1 — Physician Competency / Scope of Practice
  - Opinion 3.1.2 — Physician Responsibility to Refer
  - Opinion 8.1 — Confidentiality
  - Opinion 8.2 — Mandatory Reporting
  - Opinion 9.1 — Conflicts of Interest
  - Opinion 9.6 — Research Ethics
  - Opinion 11.2 — Telemedicine
  - Opinion 11.3 — Emergency Care

### EMTALA
- **Emergency Medical Treatment and Active Labor Act**, 42 U.S.C. § 1395dd.
- **CMS Regulations:** 42 CFR § 489.24 (Special responsibilities of Medicare
  hospitals in emergency cases).
- <https://www.cms.gov/medicare/regulations-guidance/legislation/emtala>
- **Key provisions:** Medical screening requirement (§ 1395dd(a)), stabilizing
  treatment requirement (§ 1395dd(b)), restrictions on transfer (§ 1395dd(c)),
  civil penalties (§ 1395dd(d)(1)(A)) — up to $100,000 per violation.

### Standard of Care Doctrine
- **Restatement (Third) of Torts § 41** — Duty of health care professional.
- **Landmark cases:**
  - *Helling v. Carey*, 83 Wn. 2d 514 (1974) — Standard of care may require
    practices beyond customary professional usage.
  - *Hall v. Hilbun*, 466 So. 2d 856 (Miss. 1985) — National standard of care
    for specialists.
- **Key concept:** The degree of care a reasonably competent physician in the
  same field would provide under similar circumstances. National standard for
  board-certified specialists.
- **Related:** Clinical practice guidelines from specialty societies (ACG, AHA,
  ASCO, etc.) as evidence of the standard.

### Informed Consent Requirements
- **Common law doctrine** — *Schloendorff v. Society of New York Hospital*,
  211 N.Y. 125 (1914) (Cardozo, J.: "Every human being of adult years and
  sound mind has a right to determine what shall be done with his own body").
- **Modern standard:** *Canterbury v. Spence*, 464 F.2d 772 (D.C. Cir. 1972) —
  Reasonable patient standard for disclosure.
- **Key elements:** (1) Diagnosis/condition, (2) proposed treatment/procedure,
  (3) material risks, (4) reasonable alternatives (including no treatment),
  (5) risks of alternatives, (6) prognosis without treatment.
- **Statutory:** Most states have codified informed consent requirements via
  state medical practice acts.

### Stark Law and Anti-Kickback Statute
- **Stark Law** (Physician Self-Referral Law), 42 U.S.C. § 1395nn — Prohibits
  physician referral of Medicare/Medicaid patients to entities with which the
  physician has a financial relationship, unless an exception applies.
- **Anti-Kickback Statute**, 42 U.S.C. § 1320a-7b — Criminal penalties for
  offering or receiving remuneration for patient referrals.
- **OIG Guidance:** <https://oig.hhs.gov/compliance/physician-education/>

### Ryan Haight Act
- **Ryan Haight Online Pharmacy Consumer Protection Act of 2008**, 21 U.S.C.
  § 802 — Requires at least one in-person medical evaluation before prescribing
  controlled substances via telemedicine.
- **DEA Regulations:** 21 CFR Part 1306.
- **Public Health Emergency waivers** (COVID-19) have temporarily modified
  in-person requirements; consult current DEA guidance.

### Research Ethics
- **Belmont Report** (1979) — Ethical principles for human subjects research:
  respect for persons, beneficence, justice.
- **Common Rule** (45 CFR § 46) — Federal policy for protection of human subjects.
- **Declaration of Helsinki** (WMA, current version) — Ethical principles for
  medical research involving human subjects.
- **ICMJE Recommendations** — Uniform requirements for manuscripts submitted to
  biomedical journals (authorship, data sharing, conflicts of interest).
- **Nuremberg Code** (1947) — Voluntary consent is absolutely essential.

### Cultural Competence
- **National Standards for Culturally and Linguistically Appropriate Services
  (CLAS)** — U.S. Department of Health and Human Services, Office of Minority
  Health. <https://thinkculturalhealth.hhs.gov/clas>
- **Joint Commission Standards** — Patient-centered communication, language
  access services, cultural competence requirements for hospital accreditation.

### Telemedicine Standards
- **Federation of State Medical Boards (FSMB)** — Model Policy for the
  Appropriate Use of Telemedicine Technologies in Medical Practice (current
  edition). <https://www.fsmb.org/>
- **AMA Opinion 11.2** — Telemedicine: same standard of care as in-person.
- **Interstate Medical Licensure Compact (IMLC)** — Streamlined multi-state
  licensing for telemedicine.

## Per-rule citation table

| Rule id | Primary Source(s) | Citations |
|---------|-------------------|-----------|
| `scope-of-practice` | AMA Code 1.1.1, FSMB Model Policy | Patient-physician relationship requires a real physician; AI must not pose as one |
| `patient-confidentiality` | HIPAA Privacy Rule 45 CFR § 164.500–534, AMA Code 8.1 | PHI definition § 164.501, minimum necessary § 164.502(b), de-identification § 164.514 |
| `prescribing-boundaries` | Ryan Haight Act, FSMB Telemedicine Policy, AMA Code 3.1.1 | No AI prescribing, verify dosage with pharmacist, competency limits |
| `medical-disclaimer` | FTC Health Breach Notification Rule, FSMB guidelines | Clear disclosure of AI status, educational purposes only |
| `documentation` | AMA Code 2.2.1, Joint Commission Records Standards | SOAP format, timely entries, no retroactive alteration, addendum protocol |
| `informed-consent` | *Canterbury v. Spence*, AMA Code 2.1.1, Common Law | Risks, benefits, alternatives, voluntary, documented; emergency exception |
| `standard-of-care` | Restatement (Third) Torts § 41, *Hall v. Hilbun*, Specialty Guidelines | Degree of care of reasonably competent physician; off-label disclosure |
| `mandatory-reporting` | State statutes, AMA Code 8.2, Tarasoff duty | Communicable diseases, abuse, credible threats override confidentiality |
| `referral-threshold` | AMA Code 3.1.2, FSMB Competency Guidelines | Refer when outside competency, document rationale and follow-up |
| `conflict-of-interest` | Stark Law 42 U.S.C. § 1395nn, Anti-Kickback Statute 42 U.S.C. § 1320a-7b, AMA Code 9.1 | Disclosure required, no kickbacks, Stark exceptions |
| `cultural-competence` | National CLAS Standards, Joint Commission, AMA Code 1.2.1 | Interpreters, religious accommodation, non-discrimination |
| `emergency-care` | EMTALA 42 U.S.C. § 1395dd, 42 CFR § 489.24 | Screening regardless of insurance, stabilize before transfer, penalties |
| `telemedicine-standards` | AMA Code 11.2, FSMB Telemedicine Policy, Ryan Haight Act | Same standard of care, identity verification, location, consent |
| `second-opinion-rights` | AMA Code 1.1.3, Common law patient rights | Right to second opinion, no retaliation, timely records transfer |
| `research-ethics` | 45 CFR § 46 (Common Rule), Belmont Report, Declaration of Helsinki, ICMJE | IRB approval, informed consent, withdrawal rights, adverse event reporting |

## Coverage honesty

**Checkable rules (6):** `scope-of-practice`, `patient-confidentiality`,
`prescribing-boundaries`, `medical-disclaimer`, `documentation`,
`informed-consent`.

These are codifiable as regex patterns that detect common output violations:
AI posing as a physician, exposure of PHI identifiers, specific medication
dosages, missing medical disclaimers, retroactive record alteration, and
bypassing informed consent. They are high precision but narrow — they detect
known-bad patterns but do not prove overall medical compliance.

**Teaching-only rules (9):** standard-of-care, mandatory-reporting,
referral-threshold, conflict-of-interest, cultural-competence, emergency-care,
telemedicine-standards, second-opinion-rights, research-ethics. These require
contextual judgement and are evaluated by the LLM judge (Layer 2) or the
Socratic fix step.

**What is NOT covered:** Full medical practice compliance requires state medical
board licensure, DEA registration, malpractice coverage, hospital credentialing,
and hundreds of regulatory requirements. This class teaches an LLM to recognize
the most common medical standard violations and to follow professional standards
at generation time. It does not replace a compliance officer, risk manager, or
licensed physician.

## Verification

Each rule with `check_regex` is FAIL/PASS tested in
`tests/test_credential_md.py`. Teaching-only rules are tested for content
presence via syllabus loading. A rule cannot ship without its test pair — see
CONTRIBUTING.md.
