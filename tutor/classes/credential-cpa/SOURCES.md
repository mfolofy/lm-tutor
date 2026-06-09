# SOURCES — credential-cpa (Accounting & Finance Professional Standards)

All rules in `class.yaml` derive from US accounting, auditing, and financial
regulatory standards. Every rule cites the specific standard or code section
it codifies. No rule exists without a source.

## Primary Standards

### GAAP — Generally Accepted Accounting Principles
- **ASC Codification** (Accounting Standards Codification) — FASB's authoritative
  source of US GAAP. <https://asc.fasb.org/>
  - ASC 606 — Revenue from Contracts with Customers (supersedes ASC 605, ASC 340-40)
  - ASC 842 — Leases (supersedes ASC 840)
  - ASC 326 — Financial Instruments — Credit Losses (CECL)
  - ASC 740 — Income Taxes
  - ASC 235 — Notes to Financial Statements (disclosure of accounting policies)
  - ASC 250 — Accounting Changes and Error Corrections
- **SAB 99** — SEC Staff Accounting Bulletin No. 99: Materiality
- **SAB 108** — SEC Staff Accounting Bulletin No. 108: Quantifying Misstatements

### GAAS — Generally Accepted Auditing Standards
- **AICPA Auditing Standards Board** — Statements on Auditing Standards (SAS)
  - AU-C 300 — Planning an Audit
  - AU-C 315 — Understanding the Entity and Its Environment and Assessing Risks
  - AU-C 320 — Materiality in Planning and Performing an Audit
  - AU-C 330 — Responding to Assessed Risks
  - AU-C 500 — Audit Evidence
  - AU-C 230 — Audit Documentation
  - AU-C 700 — Forming an Opinion and Reporting on Financial Statements
- **PCAOB Auditing Standards** (for public company audits)
  - AS 2105 — Consideration of Materiality
  - AS 2201 — An Audit of Internal Control Over Financial Reporting
  - AS 2415 — Consideration of an Entity's Ability to Continue as a Going Concern
- Source: <https://www.aicpa.org/standards>

### AICPA Code of Professional Conduct
- **ET Section 1.700.001** — Confidential Client Information
- **ET Section 1.200.001** — Conceptual Framework for Independence
- **ET Section 1.210.001** — Independence (in fact and appearance)
- ET Section 1.100.001 — Integrity and Objectivity
- ET Section 1.400.001 — Acts Discreditable
- Source: <https://pub.aicpa.org/codeofconduct/>

### Sarbanes-Oxley Act of 2002
- **SOX Sec. 302** — Corporate Responsibility for Financial Reports (CEO/CFO certification)
- **SOX Sec. 404** — Management Assessment of Internal Controls (ICFR)
- **SOX Sec. 201** — Services Outside the Scope of Practice of Auditors (non-audit services prohibited)
- **SOX Sec. 802** — Criminal Penalties for Altering Documents (7-year retention, 10-year imprisonment)
- **SOX Sec. 101** — Public Company Accounting Oversight Board (PCAOB) establishment
- Public Law 107-204, 116 Stat. 745 (2002)

### Circular 230 — Treasury Department Regulations
- **31 CFR Part 10** — Practice Before the Internal Revenue Service
  - Sec. 10.34 — Standards for Tax Returns and Documents (reasonable basis, disclosure)
  - Sec. 10.35 — Tax Shelters (more likely than not standard)
  - Sec. 10.51 — Incompetence and Disreputable Conduct
  - Sec. 10.28 — Return of Client Records
  - Sec. 10.29 — Conflicting Interests
- **IRC Sec. 6662** — Accuracy-Related Penalty
- **IRC Sec. 6694** — Understatement of Taxpayer Liability by Tax Return Preparer
- **IRC Sec. 6695** — Other Assessable Penalties with Respect to the Preparation of Tax Returns
- **IRC Sec. 6001** — Recordkeeping Requirements

### SEC Rules
- **SEC Rule 10b-5** — Employment of Manipulative and Deceptive Devices (anti-fraud)
- **SEC Regulation S-K** — Standard Instructions for Filing Forms
- **SEC Regulation S-X** — Form and Content of Financial Statements
- Source: <https://www.sec.gov/rules>

### FINRA Rules
- **FINRA Rule 2210** — Communications with the Public (fair, balanced, not misleading)
- **FINRA Rule 2241** — Research Analysts and Research Reports
- **FINRA Rule 2111** — Suitability
- Source: <https://www.finra.org/rules-guidance>

### BSA/AML — Bank Secrecy Act / Anti-Money Laundering
- **31 USC 5311 et seq.** — Bank Secrecy Act (Currency and Foreign Transactions Reporting Act)
- **31 USC 5318(g)(2)** — SAR filing prohibition on tipping off
- **31 CFR 1020.220** — Customer Identification Program (CIP)
- **31 CFR 1010.230** — Beneficial Ownership Requirements for Legal Entity Customers (CDD Rule)
- **FinCEN** — Financial Crimes Enforcement Network guidance
- Source: <https://www.fincen.gov/resources/statutes-regulations>

### ERISA — Employee Retirement Income Security Act of 1974
- **ERISA Sec. 404** — Fiduciary Duties (sole interest, prudent person, diversification, plan documents)
- **Uniform Prudent Investor Act (UPIA)** — adopted by 45+ states

### Other Standards
- **Uniform Prudent Investor Act** (1994) — diversification, risk-return analysis, delegation
- **AICPA Code 1.700.001** — Client confidentiality in member practice
- **SEC Rule 17a-4** — Recordkeeping and retention for broker-dealers

## Per-Rule Source Map

| Rule ID | Primary Source(s) | Type |
|---------|------------------|------|
| `cpa-credential-claim` | AICPA ET Sec. 1.100.001 (Integrity and Objectivity) | check_regex |
| `past-performance-guarantee` | SEC Rule 10b-5, FINRA Rule 2210 | check_regex |
| `unaudited-statement-claim` | GAAS AU-C 700, PCAOB AS 3101 | check_regex |
| `independence-claim-conflict` | AICPA ET Sec. 1.200.001 (conceptual framework), ET Sec. 1.210.001 | check_regex |
| `aml-tipping-off` | 31 USC 5318(g)(2), FinCEN guidance | check_regex |
| `guaranteed-returns` | SEC Rule 10b-5, FINRA Rule 2210, FINRA Rule 2111 | check_regex |
| `scope-of-practice` | AICPA ET Sec. 1.100.001, Circular 230 Sec. 10.51 | teaching-only |
| `gaap-compliance` | ASC Codification (606, 842, 326, 740, 235) | teaching-only |
| `gaas-audit-standards` | GAAS AU-C 300-700 series, PCAOB AS | teaching-only |
| `fiduciary-duty` | ERISA Sec. 404, Uniform Prudent Investor Act | teaching-only |
| `confidentiality` | AICPA ET Sec. 1.700.001 | teaching-only |
| `sarbanes-oxley` | SOX Sec. 302, 404, 201, 802, 101 | teaching-only |
| `tax-standards` | Circular 230 Sec. 10.34, IRC Sec. 6662, 6694, 6695 | teaching-only |
| `record-retention` | SOX Sec. 802, IRC Sec. 6001, SEC Rule 17a-4 | teaching-only |
| `materiality` | SAB 99, PCAOB AS 2105, ASC 250 | teaching-only |
| `kyc-obligation` | 31 CFR 1020.220, 31 CFR 1010.230, FinCEN CDD Rule | teaching-only |

## Coverage Honesty

**Layer 1 (check_regex) rules** cover codifiable violations with high precision:
model credential claims, financial disclaimer patterns, audit opinion assertions,
independence disclosures, and SAR tipping-off. They do **not** cover nuanced
judgments (materiality assessment, GAAP application, fiduciary analysis) —
those are deferred to the LLM judge (Layer 2, Phase 1).

The honest coverage boundary for credential-cpa:
- ~35% of accounting/finance standards are codifiable at Layer 1
  (clear pattern violations like credential claims, missing disclaimers)
- ~65% need LLM or human judgment (GAAP compliance, GAAS auditing,
  materiality, fiduciary analysis)

## Verification

Each rule with a `check_regex` is FAIL/PASS tested in `tests/test_credential_cpa.py`.
Teaching-only rules (no checker) are tested for content presence only.
A rule cannot ship without its test pair — see CONTRIBUTING.md.
