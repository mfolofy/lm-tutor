# SOURCES — security (Secure Coding & System Security Controls)

All rules in `class.yaml` derive from NIST SP 800-53 Rev 5 (Security and Privacy
Controls for Information Systems and Organizations) and supporting standards.
Every rule cites its specific control family and number. No rule exists without
a source.

## Primary standard

### NIST SP 800-53 Rev 5 (2020)
- **NIST Special Publication 800-53 Revision 5** — Security and Privacy Controls
  for Information Systems and Organizations (September 2020).
- <https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final>
- 17 control families covering access control, identification and authentication,
  system and communications protection, system and information integrity, audit
  and accountability, configuration management, contingency planning, and
  incident response.

### Supporting sources

- **NIST SP 800-63B** — Digital Identity Guidelines: Authentication and Lifecycle
  Management. <https://pages.nist.gov/800-63-3/sp800-63b.html>
  Referenced for password policy minimums (IA-5 rule).
- **OWASP Top 10 (2021)** — <https://owasp.org/www-project-top-ten/>
  Referenced for injection (A03:2021), cryptographic failures (A02:2021), and
  security misconfiguration (A05:2021).
- **OWASP ASVS v4.0** — Application Security Verification Standard.
  Referenced for session management, access control, and input validation
  guidance.
- **CWE Top 25 (2023)** — <https://cwe.mitre.org/top25/>
  Referenced for SQL injection (CWE-89), OS command injection (CWE-78),
  insecure deserialization (CWE-502), and cross-origin issues (CWE-942).
- **CERT Secure Coding Standards** — SEI CERT C/C++, Java, and Perl Coding
  Standards. Referenced for input validation and injection prevention patterns.
- **Security Framework** — Reference implementation covering agent identity,
  access control, and audit logging integration.

## Per-rule citation table

| Rule id | NIST SP 800-53 | Supporting Source | Notes |
|---------|----------------|-------------------|-------|
| `ac-permissive-cors` | AC-3 (Access Enforcement), SC-7 (Boundary Protection) | OWASP A01:2021, CWE-942 | Permissive CORS exposes authenticated endpoints |
| `ac-debug-enabled` | AC-3 (Access Enforcement), CM-7 (Least Functionality) | OWASP A05:2021 | Debug mode leaks internals |
| `ac-least-privilege` | AC-6 (Least Privilege) | OWASP A01:2021 | Minimum permissions for every entity |
| `ac-separation-duties` | AC-5 (Separation of Duties) | NIST SP 800-53 AC-5 | No single entity controls conflicting operations |
| `ac-session-security` | AC-12 (Session Termination) | OWASP ASVS v4.0 V3 | Secure cookies, httpOnly, SameSite |
| `ia-weak-password-policy` | IA-5 (Authenticator Management) | NIST SP 800-63B, OWASP ASVS v4.0 V2 | Minimum 8 chars, complexity required |
| `ia-mfa` | IA-2 (Identification and Auth), IA-6 (Auth Feedback) | OWASP ASVS v4.0 V2 | MFA for privileged access |
| `ia-credential-lifecycle` | IA-5 (Authenticator Management) | NIST SP 800-63B | Rotation, expiry, revocation |
| `ia-session-timeout` | AC-12 (Session Termination), IA-5 | OWASP ASVS v4.0 V3 | Idle timeout and absolute max lifetime |
| `sc-encryption-transit` | SC-8 (Transmission Confidentiality), SC-13 (Cryptographic Protection) | OWASP A02:2021 | TLS 1.2+, HSTS enforcement |
| `sc-encryption-rest` | SC-28 (Protection of Information at Rest) | OWASP A02:2021 | AES-256 for sensitive data at rest |
| `si-sql-injection` | SI-10 (Information Input Validation) | OWASP A03:2021, CWE-89 | Parameterized queries only |
| `si-shell-injection` | SI-10 (Information Input Validation) | OWASP A03:2021, CWE-78 | No user input in shell commands |
| `si-insecure-deserialization` | SI-10 (Information Input Validation) | OWASP A08:2021, CWE-502 | Safe deserialization only |
| `si-dependency-scanning` | SI-2 (Flaw Remediation) | OWASP A06:2021 | CVE scanning, patch promptly |
| `si-input-validation` | SI-10 (Information Input Validation) | OWASP A03:2021 | Allowlist-based validation |
| `au-security-logging` | AU-3 (Audit Record Content), AU-6 (Audit Review) | OWASP A09:2021 | Security event audit trail |
| `cm-secure-config` | CM-6 (Configuration Settings), CM-7 (Least Functionality) | OWASP A05:2021 | Hardened baseline configuration |
| `cp-backup-recovery` | CP-9 (System Backup), CP-10 (System Recovery) | — | Automated backup, tested recovery |
| `ir-detection` | IR-4 (Incident Handling), IR-6 (Incident Reporting) | NIST SP 800-61 Rev 2 | Anomaly detection and alerting |

## Coverage honesty

**Checkable rules (6):** `ac-permissive-cors`, `ac-debug-enabled`,
`ia-weak-password-policy`, `si-sql-injection`, `si-shell-injection`,
`si-insecure-deserialization` — these are codifiable as regex patterns that
detect common code/config anti-patterns. They are high precision but narrow —
they detect known-bad patterns but do not prove overall security posture.

**Teaching-only rules (14):** Access control principles, authentication best
practices, session management, encryption, input validation strategy,
dependency management, audit logging, configuration hardening, backup planning,
and incident detection — these require judgement and contextual understanding.
They are evaluated by the LLM judge (Layer 2) or the Socratic fix step, not by
deterministic regex.

**What is NOT covered:** Full NIST SP 800-53 compliance requires hundreds of
controls across 17 families. This class teaches the LLM to recognize the most
common secure-coding anti-patterns and to architect systems with security
controls in mind. It does not replace a security engineer or a full compliance
audit. Specifically excluded for developer focus: physical/environmental (PE),
personnel security (PS), planning (PL), and system and services acquisition
(SA) control families — these are organizational, not code-level.

## Reference implementation

A security framework implementation demonstrates how NIST SP 800-53 controls are
applied: PKI for agent identity, WORM chain for audit integrity, dual-approval
for break-glass access, and rate-limited authentication.
