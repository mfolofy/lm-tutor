# SOURCES — credential-finra (Financial Advisor/Broker Professional Standards)

All rules in `class.yaml` derive from federal securities laws, FINRA rules, SEC
regulations, and anti-money laundering statutes. Every rule cites its specific
source. No rule exists without a source.

## Primary standards

### Federal Securities Laws
- **Investment Advisers Act of 1940** (15 USC 80b-1 et seq.) — Registration and
  regulation of investment advisers; fiduciary duty; Form ADV disclosure
  requirements.
- **Securities Act of 1933** (15 USC 77a et seq.) — Registration of securities;
  anti-fraud provisions; prospectus delivery requirements.
- **Securities Exchange Act of 1934** (15 USC 78a et seq.) — Regulation of
  securities markets; broker-dealer registration; Section 10(b) and Rule 10b-5
  (anti-fraud and insider trading); Section 15(c) (broker-dealer regulation).

### FINRA Rules
- **FINRA Rule 1250** — Continuing education requirements for registered persons.
- **FINRA Rule 2020** — Prohibition against using manipulative, deceptive, or
  other fraudulent devices; churning prohibition.
- **FINRA Rule 2111** — Suitability: reasonable-basis, customer-specific, and
  quantitative suitability obligations.
- **FINRA Rule 2210** — Communications with the public: standards for fair,
  balanced, and not misleading communications.
- **FINRA Rule 3110** — Supervision: written supervisory procedures, branch
  office inspections, communication review.
- **FINRA Rule 3210** — Anti-selling competition: prior written consent to
  recruit another firm's registered personnel.
- **FINRA Rule 3220** — Limitations on gifts, gratuities, and business
  entertainment.
- **FINRA Rule 5310** — Best execution obligation.

### SEC Regulations
- **SEC Rule 10b-5** (Exchange Act) — Employment of manipulative and deceptive
  devices; insider trading prohibition.
- **SEC Rule 204-2** (Advisers Act) — Books and records requirements for
  investment advisers; 5-year retention.
- **SEC Rule 204-3** (Advisers Act) — Form ADV Part 2 delivery requirements.
- **SEC Rule 606** (Exchange Act) — Disclosure of order routing practices.
- **SEC Rule 17a-4** (Exchange Act) — Record retention for broker-dealers;
  WORM format requirements.
- **Regulation S-P** (17 CFR Part 248) — Privacy of consumer financial
  information under Gramm-Leach-Bliley; safeguard requirements.
- **Regulation FD** (17 CFR Part 243) — Fair disclosure: selective disclosure
  of material non-public information prohibited.
- **Regulation Best Interest** (17 CFR 240.15l-1) — Standard of conduct for
  broker-dealers making recommendations.

### AML/BSA Statutes
- **Bank Secrecy Act** (31 USC 5311 et seq.) — Anti-money laundering program
  requirements.
- **USA PATRIOT Act** (2001) — Section 326: Customer Identification Program
  (CIP); enhanced due diligence; SAR filing obligations.
- **31 CFR 1020.220** — CIP requirements for financial institutions.
- **31 USC 5318(g)(2)** — Tipping off prohibition regarding SAR filings.
- **OFAC Sanctions** — Office of Foreign Assets Control: economic sanctions
  screening requirements.

### Other Standards
- **Gramm-Leach-Bliley Act** (15 USC 6801-6809) — Financial privacy;
  Safeguards Rule.
- **Uniform Prudent Investor Act** — Fiduciary standards for trust investments.

## Per-rule citation table

| Rule id | Primary Source | Supporting Authority | Key Cases / Releases | Notes |
|---------|---------------|---------------------|----------------------|-------|
| `credential-claim` | Securities Exchange Act of 1934 § 15(a) | State blue sky laws | | AI cannot hold FINRA/SEC registrations |
| `scope-of-practice` | Investment Advisers Act of 1940 § 203 | § 202(a)(11) definition | *SEC v. Capital Gains Bureau* (1963) | Personalized advice requires registration |
| `fiduciary-duty` | Investment Advisers Act of 1940 § 206 | SEC Interpretation (2019) | *SEC v. Capital Gains Bureau* (1963); Standard of Care Release | Duty of loyalty + duty of care |
| `suitability` | FINRA Rule 2111 | NASD Rule 2310 (predecessor) | FINRA Regulatory Notice 11-02, 12-25 | Three components: reasonable-basis, customer-specific, quantitative |
| `disclosure` | Advisers Act § 204, Rule 204-3 | Form ADV instructions | SEC Release IA-5240 (2023) | Form ADV Part 2 must be delivered |
| `conflicts-of-interest` | Investment Advisers Act § 206(1)-(2) | SEC Release IA-5240 (2023) | | Some conflicts cannot be cured by disclosure alone |
| `best-execution` | Exchange Act § 11(a) | FINRA Rule 5310 | SEC Release 34-37678A | Venue analysis; not lowest commission |
| `recordkeeping` | Advisers Act Rule 204-2 | Exchange Act Rule 17a-4 | SEC No-Action Letters | 5 years (first 2 on-site); WORM for broker-dealers |
| `advertising-marketing` | FINRA Rule 2210 | Securities Act of 1933 § 17 | FINRA Regulatory Notices 17-07, 21-31 | Past performance, testimonials, projections |
| `privacy-breach` | Regulation S-P (17 CFR 248) | Gramm-Leach-Bliley Act (15 USC 6801-6809) | Safeguards Rule (SEC 2023) | NPI protection; privacy notice; opt-out |
| `aml-tipping-off` | 31 USC 5318(g)(2) | USA PATRIOT Act § 326 | 31 CFR 1020.220 | SAR confidentiality; criminal penalties for tipping |
| `churning` | FINRA Rule 2020 | Exchange Act § 15(c) | *Mihara v. Dean Witter* (9th Cir.); cost-to-equity ratio analysis | Turnover ratio, in-and-out trading |
| `continuing-education` | FINRA Rule 1250 | Exchange Act § 15A(g)(3) | FINRA Regulatory Notice 22-10 | Regulatory element + firm element |
| `insider-trading` | Exchange Act § 10(b), Rule 10b-5 | Regulation FD | *SEC v. Dirks* (1983); *United States v. O'Hagan* (1997) | MNPI; tipper/tippee liability |
| `gifts-gratuities` | FINRA Rule 3220 | FINRA Rule 3210 (anti-selling competition) | FINRA Regulatory Notice 24-03 | $100 annual limit; business entertainment exemption |
| `communication-supervision` | FINRA Rule 3110 | Exchange Act Rule 17a-4 | FINRA Regulatory Notices 10-06, 11-39 | WSPs; branch inspections; social media supervision |

## Key research and commentary

| Source | Relevance |
|--------|-----------|
| SEC Standard of Conduct Release (2019) — Interpretation of fiduciary duty under Advisers Act | Fiduciary duty: loyalty, care, and full disclosure |
| SEC Regulation Best Interest (2020) — Standard of conduct for broker-dealers | Best interest obligation when making recommendations |
| "AI and the Investment Advisers Act" (SEC Division of Examinations, 2024) | AI use in advisory services: compliance considerations |
| FINRA Regulatory Notice 24-03 (2024) — Gift rule update | $100 limit adjusted for inflation |
| FINRA 2026 Regulatory Oversight Report | Current examination priorities and trends |
| SEC Examination Priorities (2026) | Focus areas: fiduciary obligations, AML programs, cybersecurity, AI governance |
| *SEC v. Capital Gains Bureau* (1963) | Foundational fiduciary duty case for investment advisers |
| *SEC v. Dirks*, 463 U.S. 646 (1983) | Insider trading: tipper must receive personal benefit |
| *United States v. O'Hagan*, 521 U.S. 642 (1997) | Misappropriation theory of insider trading |
| "Gramm-Leach-Bliley Act: A Practical Guide" (PLI) | Privacy notice requirements; opt-out mechanics |
| 31 CFR 1020.220 — CIP Rule Compliance Guide (FinCEN) | Customer identification program requirements |
| FINRA Rule 3110 — Supervision (2022 consolidated rulebook) | WSP content requirements; branch inspection cycles |
| "Artificial Intelligence in Investment Advisory" (SEC Investor Bulletin, 2024) | AI-generated advice and disclosure requirements |
| SEC Cybersecurity Guidance (2024) | Safeguards Rule compliance; incident response |
| Soft Dollar Arrangements (SEC Inspection Report) | Safe harbor under Section 28(e); disclosure requirements |

## Coverage honesty

**Checkable rules (6):** `credential-claim`, `advertising-marketing`, `churning`,
`aml-tipping-off`, `privacy-breach`, `insider-trading`.

These are codifiable as regex patterns that detect specific text-based violations:
claiming professional credentials, promising future returns based on past performance,
recommending excessive trading for commissions, disclosing SAR filings, sharing NPI
without consent, and proposing trades based on inside information.

They are high precision but narrow — they detect specific known-bad text patterns
but do not evaluate whether the AI's overall financial reasoning is sound.

**Teaching-only rules (10):** Scope of practice, fiduciary duty, suitability,
disclosure, conflicts of interest, best execution, recordkeeping, continuing
education, gifts/gratuities, and communication supervision. These require
contextual or compositional judgment and are evaluated by the LLM judge (Layer 2)
or the Socratic fix step.

**What is NOT covered:** Comprehensive financial regulation includes understanding
of per-investor suitability determinations, complex regulatory filing requirements,
state-specific securities laws (blue sky laws), tax implications of investment
strategies, exchange-specific trading rules, and professional judgment on complex
regulatory questions. This class teaches an LLM to recognize the most common
financial advisor/broker professional standards and to follow them at generation
time. It does not certify the AI to provide financial advice or replace a
registered professional's judgment.

## Verification

Each rule with `check_regex` is FAIL/PASS tested in
`tests/test_credential_finra.py`. Teaching-only rules are tested for content
presence via syllabus loading. A rule cannot ship without its test pair.
