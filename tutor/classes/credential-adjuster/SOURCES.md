# SOURCES — credential-adjuster (Insurance Claims Adjuster Professional Standards)

All rules in `class.yaml` derive from U.S. insurance claims-handling regulations,
model acts, state codes, and common law bad faith standards. Every rule cites the
specific standard or code section it codifies. No rule exists without a source.

## Primary Standards

### NAIC Unfair Claims Settlement Practices Model Act (UCSPA)
- **NAIC Model Act #900** — Unfair Claims Settlement Practices Act (adopted by all 50 states in substance)
  - Section 4 — Specific Unfair Claims Settlement Practices (15 enumerated prohibited acts)
  - Section 4(D) — Failing to adopt and implement reasonable standards for prompt investigation
  - Section 4(E) — Refusing to pay claims without conducting a reasonable investigation
  - Section 4(G) — Compelling insureds to litigate to recover amounts due
  - Section 4(H) — Attempting to settle for less than a reasonable person would believe
  - Section 4(I) — Making threats or using language to force settlement
  - Source: <https://content.naic.org/sites/default/files/inline-files/MD-900.pdf>

### State Unfair Claims Settlement Practices Regulations
- **California Fair Claims Settlement Practices Regulations** (10 CCR 2695.1 - 2695.17)
  - 10 CCR 2695.5 — Standards for prompt, fair, and equitable settlement
  - 10 CCR 2695.7 — Standards for claim denial and communication
  - 10 CCR 2695.8 — Standards for settlement offers
  - Source: <https://govt.westlaw.com/calregs/Browse/Home/California/CaliforniaCodeofRegulations>
- **Texas Insurance Code Chapter 541** — Unfair Claim Settlement Practices
  - Sec. 541.060 — Unfair Settlement Practices (specific prohibitions)
  - Source: <https://statutes.capitol.texas.gov/Docs/IN/htm/IN.541.htm>
- **New York Insurance Law Sec. 2601** — Unfair Claims Settlement Practices
  - 11 NYCRR 216 (Regulation 64) — Fair Claim Settlement
  - Source: <https://www.dfs.ny.gov/system/files/documents/2020-06/11_216.pdf>
- **Florida Statutes Sec. 626.9541** — Unfair Insurance Trade Practices Act
  - Sec. 626.9541(i) — Unfair claim settlement practices
  - Source: <https://www.flsenate.gov/Laws/Statutes/2024/626.9541>
- **Florida Administrative Code 69B-220.201** — Standards for fair claim settlement
  - Source: <https://www.flrules.org/gateway/ruleNo.asp?ID=69B-220.201>

### Fair Claims Settlement Practices Acts (FCSPA)
- **California Fair Claims Settlement Practices Regulations** (10 CCR 2695.1-2695.17)
- **Cal. Ins. Code Sec. 790.03(h)** — Prohibited unfair acts (pre-Proposition 103), still relevant for common law standards
- **20+ other states** with specific fair claims practices regulations modeled on NAIC UCSPA
- Most state insurance departments enforce fair claims practices through administrative regulations

### Common Law Bad Faith
- **First-Party Bad Faith**: Duty of good faith and fair dealing implied in every insurance contract
  - *Gruenberg v. Aetna Insurance Co.* (Cal. 1973) 9 Cal.3d 566 — First-party bad faith
  - *Anderson v. Continental Insurance Co.* (Wis. 1983) 271 N.W.2d 368 — Bad faith standards
  - Elements: (1) absence of reasonable basis for denial, (2) knowledge or reckless disregard of lack of reasonable basis
  - Remedies: contract damages + extra-contractual (emotional distress, punitive)
- **Third-Party Bad Faith**: Duty to settle within policy limits when liability is clear
  - *Crisci v. Security Insurance Co.* (Cal. 1967) 66 Cal.2d 425 — Duty to settle
  - *State Farm Mutual Auto Insurance Co. v. Campbell* (U.S. 2003) 538 U.S. 408 — Punitive damages limits
  - *Stowers Furniture Co. v. American Indemnity Co.* (Tex. 1929) 15 S.W.2d 544 — Stowers doctrine
  - *Rova Farms Resort v. Investors Insurance Co. of America* (N.J. 1974) 323 A.2d 495 — Strict duty to settle
- **Bad Faith Remedies**: Extra-contractual damages, emotional distress, punitive damages, attorney's fees
- **Model Punitive Damages Standards**: *State Farm v. Campbell* (2003) — 1:1 compensatory/punitive ratio guidance

### Federal Fair Debt Collection Practices Act (FDCPA)
- **15 USC Sec. 1692 et seq.** — Fair Debt Collection Practices Act
  - Sec. 1692d — Harassment or abuse (no threats, profanity, excessive calls)
  - Sec. 1692e — False or misleading representations
  - Sec. 1692f — Unfair practices (no unauthorized charges, no postdated check threats)
  - Applies to third-party debt collectors, including third-party administrators collecting subrogation
  - Source: <https://www.ftc.gov/legal-library/browse/fair-debt-collection-practices-act>

### HIPAA Privacy Rule
- **45 CFR Part 164**, Subpart E — Privacy of Individually Identifiable Health Information
  - 45 CFR 164.502 — Uses and disclosures of PHI (minimum necessary standard)
  - 45 CFR 164.506 — Uses and disclosures for treatment, payment, and health care operations
  - 45 CFR 164.508 — Authorization required for certain uses
  - Source: <https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164>

### State Privacy Laws (Claims Context)
- **California Consumer Privacy Act (CCPA)** — Cal. Civ. Code Sec. 1798.100 et seq.
- **New York SHIELD Act** — N.Y. Gen. Bus. Law Sec. 899-aa
- **Illinois Biometric Information Privacy Act (BIPA)** — 740 ILCS 14
- Source: See state specific codes

### Prompt Payment Statutes
- All 50 states have prompt payment laws requiring payment within statutory timeframes
- Standard: 30-60 days after settlement agreement, with interest penalties for late payment
- Examples: Cal. Ins. Code Sec. 1503 (30 days), Tex. Ins. Code Sec. 542.058 (60 days, 18% interest)

### Appraisal and Mediation Provisions
- Standard insurance policy appraisal clause (ISO forms)
- State-specific appraisal statutes (e.g., Cal. Ins. Code Sec. 2071)
- Alternative dispute resolution provisions in UCSPA

### Anti-Fraud Standards
- **Coalition Against Insurance Fraud** — Model SIU guidelines
- **National Insurance Crime Bureau (NICB)** — Fraud indicator standards
- **State fraud bureaus** — Mandatory fraud reporting statutes
- Source: <https://insurancefraud.org/>, <https://www.nicb.org/>

## Per-Rule Source Map

| Rule ID | Primary Source(s) | Type |
|---------|------------------|------|
| `adjuster-credential-claim` | State adjuster licensing laws, NAIC Producer Licensing Model Act | check_regex |
| `bad-faith-coverage-denial` | NAIC UCSPA Sec. 4(E), *Gruenberg v. Aetna*, *Anderson v. Continental* | check_regex |
| `confidentiality-breach` | HIPAA 45 CFR 164, CCPA, New York SHIELD Act, state privacy laws | check_regex |
| `unfair-lowball-settlement` | NAIC UCSPA Sec. 4(H), 10 CCR 2695.8, Tex. Ins. Code 541.060 | check_regex |
| `fraud-allegation-without-evidence` | State fraud reporting statutes, NICB guidelines, bad faith common law | check_regex |
| `scope-of-practice` | State adjuster licensing laws, NAIC Licensing Model Act | teaching-only |
| `good-faith-handling` | *Gruenberg*, *Crisci*, *Anderson*, *State Farm v. Campbell*, implied covenant | teaching-only |
| `timely-response` | NAIC UCSPA Sec. 4(B), 10 CCR 2695.5, state prompt payment statutes | teaching-only |
| `documentation` | NAIC UCSPA Sec. 4(D), bad faith discovery standards, state DOI examinations | teaching-only |
| `investigation-standards` | NAIC UCSPA Sec. 4(C)(D), *Anderson v. Continental* | teaching-only |
| `coverage-analysis` | Policy interpretation per *Contra Proferentem*, state coverage law | teaching-only |
| `damage-estimation` | State appraisal statutes, ISO policy provisions, valuation standards | teaching-only |
| `settlement-negotiation` | *Stowers*, *Crisci*, *Rova Farms*, appraisal clauses, mediation statutes | teaching-only |
| `fraud-indicators` | NICB fraud indicator standards, state fraud bureaus, Coalition Against Fraud | teaching-only |
| `communication` | 10 CCR 2695.5, NAIC UCSPA Sec. 4(A)(B), fair claims regulations | teaching-only |
| `unfair-practices` | NAIC UCSPA Sec. 4 (full), state UCL/UPC codes | teaching-only |

## Coverage Honesty

**Layer 1 (check_regex) rules** cover codifiable violations with high precision:
model adjuster credential claims, unreasonable denial patterns, confidentiality
breaches, coercive settlement language, and baseless fraud allegations. They do
**not** cover nuanced judgments (good-faith analysis, investigation adequacy,
coverage interpretation, damage accuracy) — those are deferred to the LLM judge
(Layer 2, Phase 1).

The honest coverage boundary for credential-adjuster:
- ~30% of claims handling standards are codifiable at Layer 1
  (clear pattern violations like credential claims, threats, confidentiality)
- ~70% need LLM or human judgment (good faith, investigation adequacy,
  coverage analysis, damage estimation, fraud evaluation)

## Verification

Each rule with a `check_regex` is FAIL/PASS tested in `tests/test_credential_adjuster.py`.
Teaching-only rules (no checker) are tested for content presence only.
A rule cannot ship without its test pair — see CONTRIBUTING.md.
