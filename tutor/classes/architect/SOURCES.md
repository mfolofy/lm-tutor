# SOURCES — architect (System Architecture Design Patterns)

All rules in `class.yaml` derive from established software architecture
literature, industry standards, and the Ghost Mesh governance model. Every
rule cites its architectural principle or source standard. No rule exists
without a source.

## Primary references

### Software architecture literature

- **Fowler, Martin.** *Patterns of Enterprise Application Architecture*.
  Addison-Wesley, 2002. — Layered architecture, domain model, service layer,
  repository, unit of work.
- **Richards, Mark & Neal Ford.** *Fundamentals of Software Architecture*.
  O'Reilly, 2020. — Architecture styles, component identification, coupling
  and cohesion, architectural fitness functions.
- **Hohpe, Gregor & Bobby Woolf.** *Enterprise Integration Patterns*.
  Addison-Wesley, 2003. — Messaging patterns, event-driven architecture,
  idempotent receiver, competing consumers.
- **Newman, Sam.** *Building Microservices*. 2nd ed. O'Reilly, 2021. —
  Bounded contexts, service decomposition, integration patterns, observability.
- **Nygard, Michael.** *Release It! Design and Deploy Production-Ready
  Software*. 2nd ed. Pragmatic Bookshelf, 2018. — Circuit breakers, bulkheads,
  stability patterns, graceful degradation.
- **Rozanski, Nick & Eoin Woods.** *Software Systems Architecture*. 2nd ed.
  Addison-Wesley, 2011. — Viewpoints and perspectives, architectural decisions.

### Security and compliance standards

- **AICPA.** *SOC 2 Trust Services Criteria* (TSC 2017). — CC6.1 (logical
  access controls), CC6.2 (segregation of duties), CC7.1-7.2 (monitoring).
- **NIST.** *SP 800-53 Rev. 5: Security and Privacy Controls for Information
  Systems and Organizations*. — AC-1 to AC-6 (access control), AU-1 to AU-12
  (audit and accountability).
- **NIST.** *SP 800-171 Rev. 2: Protecting Controlled Unclassified Information
  in Nonfederal Systems and Organizations*. — CMMC 2.0 compliance basis.
- **CMMC 2.0.** Cybersecurity Maturity Model Certification. — AC.L2-3.1.5
  (separation of duties), AU.L2-3.3.1 (audit logs), AU.L2-3.3.8 (audit
  protection).
- **45 CFR 164 — HIPAA Security Rule.** — 164.312(a)(2)(iv) (encryption),
  164.312(b) (audit controls), 164.312(d) (integrity controls).

### PKI and cryptography standards

- **RFC 5280.** *Internet X.509 Public Key Infrastructure Certificate and
  Certificate Revocation List (CRL) Profile*.
- **RFC 3647.** *Internet X.509 PKI Certificate Policy and Certification
  Practices Framework*.
- **NIST.** *SP 800-57 Part 1 Rev. 5: Recommendation for Key Management*.
- **Ryan, Mark D.** "Enhanced Certificate Transparency for End-Entity
  Certificates." *IEEE S&P*, 2024. — Short-lived certs as alternative to CRLs.

### Cloud and resilience patterns

- **AWS Well-Architected Framework.** *Reliability Pillar*. — Circuit
  breakers, retry with backoff, statelessness, bulkheads.
- **Google SRE Books.** *Site Reliability Engineering* (O'Reilly, 2016). —
  Service level objectives, error budgets, monitoring, incident response.
- **Microsoft.** *Azure Well-Architected Framework: Reliability*. — Retry
  pattern, circuit breaker pattern, health endpoint monitoring.

### API design references

- **Fielding, Roy T.** *Architectural Styles and the Design of Network-based
  Software Architectures* (dissertation, UC Irvine, 2000). — REST
  architectural constraints.
- **Google.** *API Design Guide*. — Resource-oriented design, HTTP methods,
  versioning, pagination, idempotency.
- **Microsoft.** *REST API Guidelines*. — Versioning strategies, error
  responses, pagination standards.

## Ghost Mesh source material (internal references)

- `docs/ghost-mesh/SOD_ARCHITECTURE.md` — Segregation of duties: 4-role model,
  dual approval matrix, enforcement points.
- `docs/ghost-mesh/CP_CPS.md` — Certificate policy and certification practice
  statement: two-tier CA hierarchy, certificate profiles, CRL distribution.
- `projects/ghost_mesh/governance/aegis_gate.py` — Pre-execution policy gate:
  protected resources, change request queue, approval workflow.
- `projects/ghost_mesh/governance/risk_policy.py` — Risk evaluation engine:
  4-level risk schema, resource-to-risk mapping, mtime-cached policy loading.

## Rule-to-source mapping

| Rule ID | Primary Sources | Architectural Principle |
|---------|----------------|------------------------|
| `single-responsibility` | Fowler (PoEAA), Richards & Ford | High cohesion, single reason to change |
| `bounded-context` | Fowler, Newman (Microservices) | Domain-driven design, context mapping |
| `layer-isolation` | Fowler (PoEAA), Rozanski & Woods | Strict layering, dependency inversion |
| `api-no-version` | Google API Design Guide, Fielding (REST) | Backward compatibility, contract evolution |
| `cqrs-separation` | Fowler (CQRS), Microsoft Azure | Command-query separation, read/write optimization |
| `api-idempotency` | Google API Design Guide, Microsoft REST | Safe retry, exactly-once semantics |
| `no-single-point-of-failure` | AWS Well-Architected, Nygard (Release It!) | Redundancy, fault tolerance |
| `defense-in-depth` | NIST SP 800-53, NIST SP 800-171 | Layered security, mutually independent controls |
| `credential-injection` | OWASP, SOC2 CC6.1 | Secret management, credential hygiene |
| `trust-boundary` | NIST SP 800-53 (AC-4), Zero Trust | Validate at every boundary, never trust implicitly |
| `sod-four-role` | Ghost Mesh SOD_ARCHITECTURE.md, SOC2 CC6.2 | Segregation of duties, no single control |
| `dual-approval` | Ghost Mesh SOD_ARCHITECTURE.md, HIPAA 164.312(d) | Two-person integrity, break-glass controls |
| `risk-classification` | Ghost Mesh risk_policy.py, NIST SP 800-53 | Risk-based approval, context-aware gating |
| `structured-observability` | Google SRE, AWS Well-Architected | Logs + metrics + traces, structured data |
| `print-logging` | Google SRE, 12 Factor App | Structured logging, log as event stream |
| `circuit-breaker` | Nygard (Release It!), AWS Well-Architected | Fail fast, graceful degradation, resilience |
| `stateless-design` | AWS Well-Architected, 12 Factor App | Horizontal scalability, ephemeral instances |
| `audit-chain-integrity` | NIST SP 800-53 (AU-9), Ghost Mesh | Tamper-evident logging, WORM storage |
| `event-driven-async` | Hohpe & Woolf (EIP), Fowler | Loose coupling, independent deployability |
| `idempotent-consumer` | Hohpe & Woolf (EIP), Microsoft Azure | At-least-once safety, deduplication |
| `pki-hierarchy` | RFC 3647, Ghost Mesh CP_CPS.md, NIST SP 800-57 | Two-tier CA, offline root, short-lived certs |

## Coverage honesty

**Layer 1 (check_regex) rules** cover codifiable architecture anti-patterns
with high precision: API versioning omissions, hardcoded secrets, single-operator
mode, and print-based logging. These are patterns that deterministic string
matching can detect reliably across code and config files.

**Teaching-only rules** cover architectural principles that require semantic
understanding of the system: separation of concerns, bounded context design,
defense-in-depth layering, event-driven integration, and PKI hierarchy. These
are deferred to the LLM judge (Layer 2, Phase 1) or human review.

The honest coverage boundary for the architect class:
- ~20% of architectural patterns are codifiable at Layer 1 (string-level anti-patterns)
- ~80% require system-level semantic understanding (component boundaries, dependency
  direction, risk classification appropriateness)

## Verification

Each rule with a `check_regex` is FAIL/PASS tested in
`tests/test_architect.py`. Teaching-only rules (no checker) are tested for
content presence only. A rule cannot ship without its test pair — see
CONTRIBUTING.md.
