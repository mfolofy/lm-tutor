# SOURCES — credential-psychiatry (Psychiatric / Mental Health Professional Standards)

All rules in `class.yaml` derive from the APA Principles of Medical Ethics with Annotations Especially Applicable to Psychiatry, the DSM-5-TR, the HIPAA Privacy Rule (45 CFR 164), APA/APM Clinical Practice Guidelines, and Tarasoff case law. Every rule cites its specific source. No rule exists without a source.

## Primary standards

### APA Principles of Medical Ethics with Annotations Especially Applicable to Psychiatry
- **American Psychiatric Association, The Principles of Medical Ethics with Annotations Especially Applicable to Psychiatry (2024 edition).**
  <https://www.psychiatry.org/psychiatrists/practice/ethics>
- Key sections cited:
  - Section 2 — Competence, honesty, and dignity of the profession
  - Section 4 — Privacy and confidentiality; post-treatment confidentiality survival; Tarasoff exception
  - Section 7 — Physician responsibility to provide services with compassion and respect; scope of practice
  - Section 9 — Physician responsibility to participate in community health efforts
  - Annotations on boundary violations, dual relationships, and informed consent

### DSM-5-TR
- **American Psychiatric Association, Diagnostic and Statistical Manual of Mental Disorders (5th Edition, Text Revision), 2022.**
  <https://dsm.psychiatryonline.org/>
- Key sections cited:
  - Cultural Formulation Interview (CFI) — Appendix
  - Cultural Concepts of Distress — Glossary
  - Section II: Diagnostic Criteria and Codes
- **Note on AI use:** The DSM-5-TR emphasizes that diagnosis requires clinical judgment based on a thorough evaluation. It is not designed for algorithmic or automated diagnosis.

### HIPAA Privacy Rule
- **Health Insurance Portability and Accountability Act of 1996**, Privacy Rule, 45 CFR 164.
- <https://www.hhs.gov/hipaa/for-professionals/privacy/index.html>
- Key provisions: Definition of PHI (164.501), psychotherapy notes special protections (164.508(a)(2)), minimum necessary standard (164.502(b)), permitted disclosures (164.506-508).
- **Mental health-specific guidance:** HHS OCR guidance on sharing mental health information: <https://www.hhs.gov/hipaa/for-professionals/special-topics/mental-health/index.html>

### APA / APM Clinical Practice Guidelines
- **American Psychiatric Association Clinical Practice Guidelines:**
  - Practice Guideline for the Treatment of Patients with Major Depressive Disorder (3rd Ed, 2010; supplemented 2024)
  - Practice Guideline for the Treatment of Patients with Panic Disorder (2nd Ed, 2009; supplemented 2024)
  - Practice Guideline for the Treatment of Patients with Schizophrenia (3rd Ed, 2020)
  - Practice Guideline for the Treatment of Patients with Bipolar Disorder (2nd Ed, 2002; supplemented 2024)
- **Academy of Psychosomatic Medicine (APM) Clinical Practice Guidelines** for psychiatric care in medical settings.
- <https://www.psychiatry.org/psychiatrists/practice/clinical-practice-guidelines>

### Tarasoff Duty to Protect
- **Tarasoff v. Regents of the University of California, 17 Cal. 3d 425 (1976).**
  Established the duty of mental health professionals to protect identifiable victims from credible threats of violence.
- **Tarasoff v. Regents, 131 Cal. Rptr. 14 (Cal. 1976)** (rehearing).
- **Subsequent developments:**
  - *Jablonski v. United States, 712 F.2d 391 (9th Cir. 1983)* — duty extends to warning about known dangerousness
  - *Emerich v. Philadelphia Center for Human Development, 720 A.2d 1032 (Pa. Super. 1998)* — duty extends to suicide prevention
  - State-by-state variation: approximately 30 states have codified a duty to protect; scope varies widely

## Supporting standards

| Standard | Coverage |
|----------|----------|
| AMA Code of Medical Ethics (2024) | Physician ethics foundation; cross-referenced for psychiatric annotations |
| APA Ethics Committee, "AI in Mental Health: Ethical Considerations" (2025) | AI ethics in psychiatric contexts; disclosure, consent, scope |
| SAMHSA TIP 42 — Substance Use Disorder Treatment | Co-occurring disorder evidence-based practices |
| SAMHSA TIP 59 — Improving Cultural Competence | Cultural competence in behavioral health services |
| 988 Suicide and Crisis Lifeline Standards | Crisis intervention protocols; <https://988lifeline.org/> |
| National Institute of Mental Health (NIMH) Research Domain Criteria (RDoC) | Alternative diagnostic framework; emerging evidence standards |
| FDA Digital Health Guidelines | AI/ML-based medical device regulation; clinical decision support distinction |
| ISMP (Institute for Safe Medication Practices) | Psychiatric medication safety guidelines |
| JCAHO Behavioral Health Standards | Accreditation standards for psychiatric facilities |
| APA Committee on Telepsychiatry | Telepsychiatry practice guidelines; state license requirements |
| WHO mhGAP (Mental Health Gap Action Programme) | Evidence-based protocols for mental health in low-resource settings |

## Per-rule citation table

| Rule id | Primary Source(s) | Notes |
|---------|-------------------|-------|
| `no-diagnosis-without-examination` | APA Principles Section 7, DSM-5-TR Introduction §I, AMA Code 1.1.1 | DSM-5-TR requires clinical evaluation; AI cannot evaluate |
| `crisis-protocol` | Tarasoff (1976), APA Section 4 Annotations, APA Telepsychiatry Guidelines, 988 Lifeline Standards | Safety overrides confidentiality; imminent harm = emergency services |
| `informed-consent` | APA Principles Section 4 Annotation 2, AMA Code 2.1.1, APA AI Ethics Guidelines (2025) | AI disclosure; limitations of platform; ongoing consent |
| `confidentiality-limits` | APA Principles Section 4, HIPAA 45 CFR 164.508(a)(2), Tarasoff | No equivalent of doctor-patient privilege; Tarasoff exceptions |
| `no-medication-recommendations` | APA Prescribing Guidelines, APA Section 7 (Competence), AMA Code 3.1.1 | Only licensed prescriber can recommend; AI cannot prescribe |
| `scope-boundaries` | APA Principles Section 7, State Medical Practice Acts, APA Professional Boundaries Guidelines | AI is not therapy; distinguish education from treatment |
| `cultural-competence` | DSM-5-TR CFI and Cultural Concepts of Distress, SAMHSA TIP 59, APA Section 9 | Cultural variation in symptom presentation; CFI framework |
| `evidence-level` | APA Clinical Practice Guidelines, APA Section 2, APA AI Ethics Guidelines | EBP levels; distinguish established from emerging; no pseudoscience |
| `professional-boundary` | APA Principles Section 2 Annotations, APA Boundary Violations Guidelines | No dual relationships; no personal relationships; jurisdiction limits |
| `documentation` | APA Section 7 (Documentation), HIPAA 45 CFR 164, APA AI Ethics Guidelines | AI role disclosure; clinician review required |

## Coverage honesty

**Checkable rules (5):** `no-diagnosis-without-examination`, `crisis-protocol`, `informed-consent`, `confidentiality-limits`, `no-medication-recommendations`.

These are codifiable as regex patterns that detect specific text-based violations: offering diagnostic labels, promising secrecy about harm, beginning clinical discussion without consent disclosure, implying full confidentiality protections, and recommending specific medications or dosages. They are high precision but narrow — they detect specific known-bad text patterns but do not evaluate whether the AI's overall clinical reasoning is sound.

**Teaching-only rules (5):** Scope boundaries, cultural competence, evidence-level, professional boundary, documentation. These require contextual or compositional judgment and are evaluated by the LLM judge (Layer 2) or the Socratic fix step.

**What is NOT covered:** Full psychiatric ethics requires understanding of state-specific licensing and scope regulations, nuanced differential diagnosis, psychopharmacology expertise, therapeutic relationship management, and professional judgment on complex ethical dilemmas. This class teaches an LLM to recognize the most common psychiatric professional standards and to follow them at generation time. It does not certify the AI to provide clinical services or replace a licensed psychiatrist's professional judgment.

## Verification

Each rule with `check_regex` is FAIL/PASS tested in `tests/test_credential_psychiatry.py`. Teaching-only rules are tested for content presence via syllabus loading. A rule cannot ship without its test pair.
