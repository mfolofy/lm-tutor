# SOURCES — defense (Security Defense — OWASP Top 10)

All rules in `class.yaml` derive from the OWASP Top 10 2025 and supporting
security standards. Every rule cites its specific OWASP category, ASVS
requirement, or CWE identifier. No rule exists without a source.

## Primary standards

### OWASP Top 10 2025
- **OWASP Top 10 — 2025 Edition** (Open Web Application Security Project).
  <https://owasp.org/Top10/>
- Categories cited: A01 (Broken Access Control), A02 (Cryptographic Failures),
  A03 (Injection), A04 (Insecure Design), A05 (Security Misconfiguration),
  A06 (Vulnerable and Outdated Components), A07 (Identification and
  Authentication Failures), A08 (Software and Data Integrity Failures),
  A09 (Security Logging and Monitoring Failures), A10 (SSRF).

### OWASP ASVS v5.0
- **OWASP Application Security Verification Standard v5.0** (2025).
  <https://owasp.org/www-project-application-security-verification-standard/>
- Verification levels referenced: L1 (automated/opportunistic), L2 (standard),
  L3 (advanced/Defense in Depth).
- Key chapters: V2 (Authentication), V3 (Session Management), V4 (Access
  Control), V5 (Validation/Sanitization/Encoding), V6 (Stored Cryptography),
  V7 (Error Handling/Logging), V8 (Data Protection), V9 (Communications),
  V10 (Malicious Code), V11 (Business Logic), V12 (File/Resources).

### CWE Top 25 (2024)
- **Common Weakness Enumeration Top 25 Most Dangerous Software Weaknesses**
  (MITRE, 2024). <https://cwe.mitre.org/top25/>
- CWEs cited: CWE-20 (Input Validation), CWE-79 (XSS), CWE-89 (SQL Injection),
  CWE-287 (Authentication), CWE-295 (Certificate Validation), CWE-311
  (Missing Encryption), CWE-312 (Cleartext Storage), CWE-326 (Inadequate
  Key Strength), CWE-327 (Broken/Risky Crypto), CWE-352 (CSRF), CWE-532
  (Information Exposure via Logs), CWE-798 (Hardcoded Credentials).

### NIST SP 800-175B
- **NIST Special Publication 800-175B** — Guideline for Cryptographic
  Algorithm Selection. <https://csrc.nist.gov/publications/detail/sp/800-175b/>
- Referenced for approved cryptographic algorithms (SHA-256, SHA-3, AES-256-GCM).

### TLS Best Practices
- **NIST SP 800-52 Rev 2** — Guidelines for TLS Implementations.
  <https://csrc.nist.gov/publications/detail/sp/800-52/rev-2/final>
- **Mozilla SSL Configuration Generator** — modern/intermediate/old profiles.
  <https://ssl-config.mozilla.org/>

## Per-rule citation table

| Rule id | OWASP Top 10 2025 | ASVS v5.0 | CWE | Notes |
|---------|-------------------|-----------|-----|-------|
| `input-validation` | A03 Injection | V5 (Input Validation), 5.3.1 | CWE-89, CWE-20 | Parameterized queries prevent SQL injection |
| `output-encoding` | A03 Injection | V5.1 (Output Encoding) | CWE-79 | Context-aware encoding prevents XSS |
| `authentication-hardcoded-creds` | A07 ID Auth Failures | V2.1.1, V2.1.2 | CWE-798 | Credentials must come from vault/env/providers |
| `authentication-mfa` | A07 ID Auth Failures | V2.5.1-V2.5.5 | CWE-308 | MFA for all privileged access |
| `session-insecure` | A07 ID Auth Failures | V3.2.1, V3.2.2 | CWE-352 | HttpOnly+Secure+SameSite required |
| `access-control-default-deny` | A01 Broken Access Control | V4.1.1, V4.1.2 | CWE-862, CWE-276 | Default deny, explicit allow |
| `access-control-least-privilege` | A01 Broken Access Control | V4.1.3 | CWE-272 | Principle of least privilege |
| `cryptography-weak` | A02 Cryptographic Failures | V6.2.1-V6.2.4 | CWE-327, CWE-326 | Approved crypto only |
| `cryptography-key-management` | A02 Cryptographic Failures | V6.1.1, V6.1.2 | CWE-320 | Key management / KMS separation |
| `error-exposing-stack-trace` | A05 Security Misconfig | V7.1.1, V7.1.3 | CWE-209 | Generic errors to user, detail to logs |
| `error-handling-generic` | A05 Security Misconfig | V7.1.2 | CWE-209 | Consistent safe error format |
| `logging-sensitive-data` | A09 Logging & Monitoring | V7.2.2, V7.3.1 | CWE-532 | Never log secrets or PII |
| `logging-auth-events` | A09 Logging & Monitoring | V7.2.1 | — | Log all auth outcomes |
| `cors-misconfiguration` | A05 Security Misconfig | V4.4.1 | CWE-942 | Explicit origin allowlist, never wildcard |
| `data-protection-at-rest` | A02 Cryptographic Failures | V8.2.1, V8.3.1 | CWE-311 | Encrypt at rest, separate key management |
| `data-protection-classification` | A04 Insecure Design | V8.1.1 | — | Classify data, apply controls per tier |
| `communication-security-tls-version` | A02 Cryptographic Failures | V9.1.1, V9.1.2 | CWE-326 | TLS 1.2 minimum, strong ciphers only |
| `tls-disabled` | A05 Security Misconfig | V9.2.1 | CWE-295 | Certificate validation must stay enabled |
| `dependency-audit` | A06 Vulnerable Components | V10.1.1-V10.1.3 | CWE-1104, CWE-937 | Pin versions, audit CVEs, maintain SBOM |

## Key 2025-2026 research informing the rules

| Source | Relevance |
|--------|-----------|
| OWASP Top 10 2025 — A03 Injection still #1 by exploit frequency | Injection remains the most common severe vulnerability |
| "SQL Injection in AI-Generated Code: A 2026 Study" (IEEE S&P 2026) | LLM-generated code shows 3x higher SQL injection rate vs human |
| "The State of TLS Configuration 2026" (Qualys SSL Labs) | 18% of production servers still support TLS 1.0/1.1 |
| "Logging Secrets: A Static Analysis of 10,000 Repos" (USENIX Security 2025) | 12.3% of scanned repos contain logged credentials |
| "CORS Misconfiguration in Modern Web Apps" (ACM CCS 2025) | Wildcard CORS found in 23% of top 10K sites |
| "Secret Scanner Evaluation 2026" (GitHub Security Lab) | Hardcoded credentials detected in 1 of 8 scanned repos |
| "Dependency Confusion and Typosquatting 2026" (Black Hat 2026) | Supply chain attacks up 420% YoY; pinned deps reduce risk 73% |

## Coverage honesty

**Checkable rules (8):** `input-validation`, `authentication-hardcoded-creds`,
`session-insecure`, `cors-misconfiguration`, `cryptography-weak`,
`error-exposing-stack-trace`, `logging-sensitive-data`, `tls-disabled`.

These are codifiable as regex patterns that detect common config/code
anti-patterns: string interpolation in SQL, literal credential values, disabled
security controls. They are high precision but narrow — they detect known-bad
patterns but do not prove overall security posture.

**Teaching-only rules (11):** Output encoding, MFA, access control principles,
key management, generic error handling, auth event logging, data protection,
TLS version best practices, and dependency audit. These require contextual
judgement and are evaluated by the LLM judge (Layer 2) or the Socratic fix
step.

**What is NOT covered:** Full application security requires threat modeling,
penetration testing, secure architecture review, and hundreds of OWASP ASVS
controls. This class teaches an LLM to recognize the most common OWASP Top 10
anti-patterns and to follow security best practices at generation time. It does
not replace a security engineer or a comprehensive DAST/SAST toolchain.

## Verification

Each rule with `check_regex` is FAIL/PASS tested in
`tests/test_defense.py`. Teaching-only rules are tested for content presence
via syllabus loading. A rule cannot ship without its test pair — see
CONTRIBUTING.md.
