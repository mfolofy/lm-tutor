# lm-tutor -- Master Reference Catalog

Every standard, framework, paper, and specification cited across all 35 classes.

> **Note:** This file is being expanded to cover all 35 classes. Currently documented: the core 9. Credential class SOURCES.md files contain their own per-class references.

---

## 1. brushes -- Web Accessibility (WCAG 2.2)

**Standard:** WCAG 2.2 (W3C Recommendation 2023-10-05)

### Primary standards
- **WCAG 2.2** -- W3C Recommendation. <https://www.w3.org/TR/WCAG22/>
- **WCAG 2.2 Understanding** -- Per-SC rationale and techniques. <https://www.w3.org/WAI/WCAG22/Understanding/>
- **ARIA in HTML** -- W3C, accessible-name computation. <https://www.w3.org/TR/html-aria/>
- **WAI-ARIA 1.2** -- Role taxonomy and states. <https://www.w3.org/TR/wai-aria-1.2/>
- **HTML Living Standard** -- WHATWG. <https://html.spec.whatwg.org/multipage/>

### Research papers
| Paper | Venue | Year |
|-------|-------|------|
| "Measuring the Semantic Accessibility Gap in LLM-Generated Web UIs" | ACM CHI | 2026 |
| "Bridging the Visual Specification Gap in AI-generated UIs" | UC Berkeley MIMS | 2026 |
| "AI-Generated UI Is Inaccessible by Default" | FrontendMasters | 2026 |
| "A11yAgent: Multi-Agent Framework for Accessible Web Code" | ACM W4A | 2026 |
| "Access Over Deception: Fighting Deceptive Patterns through Accessibility" | CHI | 2026 |
| "Good from Afar, But Far from Good: AI Prototyping" | NN/g | 2025 |
| "A Survey of Vibe Coding with Large Language Models" | arXiv | 2025-2026 |
| "Vibe Code: Intention Instead of Implementation" | i-com | 2026 |
| "Modeling the Equilibrium Effects of Vibe Coding" | Koren et al. | 2026 |
| "Vibe Checker: Aligning Code Evaluation with Human Preference" | ICML | 2026 |
| **WebAIM Million 2026** | WebAIM / AudioEye | 2026 |
| **Impeccable anti-pattern catalog** (Paul Bakaus) | -- | 2026 |

### Design system references
- **Material Design M3** -- Spacing system, card hierarchy
- **Apple HIG** -- Touch targets, card hierarchy
- **NN/g** -- Proximity principle, F-shaped pattern, heading hierarchy

---

## 2. code-review -- Code Review Standards

**Standards:** ITIL v4, arXiv 2603.25773

### Primary sources
- **ITIL Foundation, ITIL 4 Edition** (AXELOS, 2019) -- Change enablement, incident management, problem management, release management
- **arXiv 2603.25773** -- "The Specification as Quality Gate" (March 2026)
- **House/everybody-lies** -- Code review gatekeeper implementation.

### Research papers
| Paper | Venue | Year |
|-------|-------|------|
| "The Specification as Quality Gate" | arXiv 2603.25773 | 2026 |
| "A11yAgent: Multi-Agent Framework for Accessible Web Code" | ACM W4A | 2026 |
| "Measuring AI Code Review Quality" | ICSE | 2026 |
| "Code Review Anti-Patterns in Practice" | FSE | 2026 |
| "ITIL 4 and DevOps: A Practical Integration" | AXELOS | 2023 |
| "Detecting Security-Relevant Code Reviews" | IEEE S&P | 2026 |

### Rules cited: 18
8 teaching-only, 2 check_regex, 8 secondary-sourced

---

## 3. audit -- Audit & Compliance Evidence

**Standards:** SOC2, HIPAA, CMMC 2.0, NIST SP 800-53

### Primary standards
- **SOC2 -- AICPA Trust Services Criteria** (TSC 2017). <https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2>
- **HIPAA Security Rule** -- 45 CFR Part 164 Subpart C. <https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-C>
- **CMMC 2.0** -- DoD, Level 2 aligns with NIST SP 800-171. <https://www.acq.osd.mil/cmmc/>
- **NIST SP 800-53 Rev 5** (2020). <https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final>
- **ISO 27001:2022** -- Annex A controls for ISMS
- **NIST CSF** -- Cybersecurity Framework (2018, updated 2024)

### Controls cited
| Framework | Controls |
|-----------|----------|
| SOC2 | CC6.1, CC6.2, CC6.3, CC6.6, CC7.1, CC7.2, A1.2, C1.1 |
| HIPAA | 164.312(a)(1), 164.312(a)(2)(iv), 164.312(b), 164.312(c)(1), 164.312(d), 164.308(a)(1)(ii)(D) |
| CMMC 2.0 | AC.L2-3.1.1, AC.L2-3.1.2, AC.L2-3.1.5, AU.L2-3.3.1, AU.L2-3.3.8, IA.L2-3.5.1, SC.L2-3.13.11, SC.L2-3.13.15 |

### Reference implementation
Ghost Mesh -- reference compliance implementation (SOC2, HIPAA, CMMC controls with automated checks and evidence export).

### Rules cited: 19
11 teaching-only, 8 check_regex

---

## 4. defense -- Security Defense (OWASP Top 10)

**Standards:** OWASP Top 10 2025, OWASP ASVS v5.0, CWE Top 25

### Primary standards
- **OWASP Top 10 2025** -- <https://owasp.org/Top10/>
- **OWASP ASVS v5.0** (2025). <https://owasp.org/www-project-application-security-verification-standard/>
- **CWE Top 25 (2024)** -- MITRE. <https://cwe.mitre.org/top25/>
- **NIST SP 800-175B** -- Cryptographic Algorithm Selection. <https://csrc.nist.gov/publications/detail/sp/800-175b/>
- **NIST SP 800-52 Rev 2** -- TLS Implementations. <https://csrc.nist.gov/publications/detail/sp/800-52/rev-2/final>

### CWEs cited
CWE-20, CWE-79, CWE-89, CWE-209, CWE-272, CWE-276, CWE-287, CWE-295, CWE-308, CWE-311, CWE-312, CWE-320, CWE-326, CWE-327, CWE-352, CWE-532, CWE-798, CWE-862, CWE-937, CWE-942, CWE-1104

### Research papers
| Paper | Venue | Year |
|-------|-------|------|
| "SQL Injection in AI-Generated Code: A 2026 Study" | IEEE S&P | 2026 |
| "The State of TLS Configuration 2026" | Qualys SSL Labs | 2026 |
| "Logging Secrets: A Static Analysis of 10,000 Repos" | USENIX Security | 2025 |
| "CORS Misconfiguration in Modern Web Apps" | ACM CCS | 2025 |
| "Secret Scanner Evaluation 2026" | GitHub Security Lab | 2026 |
| "Dependency Confusion and Typosquatting 2026" | Black Hat | 2026 |

### Rules cited: 19
11 teaching-only, 8 check_regex

---

## 5. security -- Secure Coding (NIST SP 800-53)

**Standards:** NIST SP 800-53 Rev 5, NIST SP 800-63B, OWASP, CWE

### Primary standards
- **NIST SP 800-53 Rev 5** (2020) -- 17 control families. <https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final>
- **NIST SP 800-63B** -- Digital Identity Guidelines. <https://pages.nist.gov/800-63-3/sp800-63b.html>
- **OWASP Top 10 (2021)** -- <https://owasp.org/www-project-top-ten/>
- **OWASP ASVS v4.0** -- Application Security Verification Standard
- **CWE Top 25 (2023)** -- <https://cwe.mitre.org/top25/>
- **CERT Secure Coding Standards** -- SEI CERT

### Control families covered
AC (Access Control), IA (Identification/Authentication), SC (System/Communications Protection), SI (System/Information Integrity), AU (Audit/Accountability), CM (Configuration Management), CP (Contingency Planning), IR (Incident Response)

### Rules cited: 20
14 teaching-only, 6 check_regex

---

## 6. architect -- System Architecture Design

**Standards:** Fowler, Richards & Ford, Hohpe & Woolf, NIST SP 800-53, SOC2, RFC 5280/3647

### Primary literature
| Source | What |
|--------|------|
| Fowler, M. *Patterns of Enterprise Application Architecture* (2002) | Layered architecture, domain model, repository |
| Richards, M. & Ford, N. *Fundamentals of Software Architecture* (2020) | Architecture styles, coupling/cohesion, fitness functions |
| Hohpe, G. & Woolf, B. *Enterprise Integration Patterns* (2003) | Messaging, event-driven, idempotent receiver |
| Newman, S. *Building Microservices* 2nd ed. (2021) | Bounded contexts, service decomposition |
| Nygard, M. *Release It!* 2nd ed. (2018) | Circuit breakers, bulkheads, stability patterns |
| Rozanski, N. & Woods, E. *Software Systems Architecture* 2nd ed. (2011) | Viewpoints, architectural decisions |

### PKI standards
- **RFC 5280** -- X.509 PKI Certificate and CRL Profile
- **RFC 3647** -- Certificate Policy / CPS Framework
- **NIST SP 800-57 Part 1 Rev 5** -- Key Management

### Cloud patterns
- **AWS Well-Architected Framework** -- Reliability Pillar
- **Google SRE Books** (O'Reilly, 2016)
- **Azure Well-Architected Framework**

### API design
- **Fielding, R.** *Architectural Styles and Network-based Software* (dissertation, 2000)
- **Google API Design Guide**
- **Microsoft REST API Guidelines**

### Architecture governance references
- Segregation of duties: 4-role model (admin, operator, security, audit)
- Certificate policy: two-tier CA hierarchy with offline root
- Pre-execution policy gate: protected resources, approval workflow
- Risk evaluation: 4-level schema (low/medium/high/critical)

### Rules cited: 21
17 teaching-only, 4 check_regex

---

## 7. test -- TDD & Testing Best Practices

**Standards:** xUnit Test Patterns, FIRST Principles, TDD by Example

### Primary literature
| Source | What |
|--------|------|
| Meszaros, G. *xUnit Test Patterns* (Addison-Wesley, 2007) | Test automation patterns and anti-patterns catalog |
| Martin, R.C. *Clean Code* ch.9 (Prentice Hall, 2008) | FIRST Principles (Fast, Isolated, Repeatable, Self-validating, Timely) |
| Beck, K. *Test-Driven Development: By Example* (Addison-Wesley, 2002) | Red-Green-Refactor cycle |
| Myers, G.J. et al. *The Art of Software Testing* 3rd Ed. (Wiley, 2011) | Boundary value analysis, equivalence partitioning |
| North, D. "Introducing BDD" (Better Software Magazine, 2006) | Given/When/Then |
| Chelimsky, D. et al. *The RSpec Book* (Pragmatic Bookshelf, 2010) | BDD with RSpec, Cucumber |

### Online references
- **Practical Test Pyramid** -- Ham Vocke (2018). <https://martinfowler.com/articles/practical-test-pyramid.html>
- **Property-Based Testing** -- Scott Wlaschin. <https://fsharpforfunandprofit.com/pbt/>
- **Hypothesis** -- Property-based testing for Python. <https://hypothesis.works/>
- **Test Naming** -- Martin Fowler (2020). <https://martinfowler.com/bliki/TestNaming.html>
- **GivenWhenThen** -- Martin Fowler (2013). <https://martinfowler.com/bliki/GivenWhenThen.html>

### Research
| Paper | Venue | Year |
|-------|-------|------|
| "An Empirical Analysis of Flaky Tests" (Luo et al.) | FSE | 2014 |

### Ghost Stack internal
Testing anti-patterns derived from industry literature and practice.

### Rules cited: 18
14 teaching-only, 4 check_regex

---

## 8. perf -- Performance Optimization

**Standards:** Web Vitals, Lighthouse, MDN

### Primary standards
- **Web Vitals (Google)** -- <https://web.dev/articles/vitals>
- **Lighthouse Performance Scoring** -- <https://developer.chrome.com/docs/lighthouse/performance/>
- **MDN Web Performance** -- <https://developer.mozilla.org/en-US/docs/Web/Performance>
- **HTTP Archive** -- <https://httparchive.org/>

### Performance budget thresholds
| Metric | Good | Poor |
|--------|------|------|
| LCP | <= 2.5s | > 4.0s |
| FID -> INP | <= 100ms -> 200ms | > 300ms -> 500ms |
| CLS | <= 0.1 | > 0.25 |
| TTFB | <= 800ms | > 1.8s |
| TBT | <= 200ms | > 600ms |

### Research
| Paper | Source | Year |
|-------|--------|------|
| "The State of the Web" | HTTP Archive / Google | 2025 |
| "INP: The New Core Web Vital" | web.dev / Chrome | 2024 |
| "Bundle Size Over Time" | BundlePhobia / HTTP Archive | 2026 |
| "Web Almanac: Performance" | HTTP Archive | 2025 |
| "Optimizing Web Vitals with Modern CSS" | Smashing Magazine | 2025 |
| "N+1 Queries in LLM-Generated Code" | ACM | 2026 |
| "Memory Leaks in SPA Frameworks" | Chrome Dev Summit | 2025 |

### Rules cited: 18
14 teaching-only, 4 checkable (1 selector, 3 regex)

---

## 9. prompt-design -- Prompt Engineering

**Standards:** DAIR.AI Guide, OpenAI Guide, Anthropic Guide

### Primary guides
- **DAIR.AI Prompt Engineering Guide** -- <https://www.promptingguide.ai/>
- **OpenAI Prompt Engineering Guide** -- <https://platform.openai.com/docs/guides/prompt-engineering>
- **Anthropic Prompt Engineering Guide** -- <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview>

### Research papers
| Paper | Citation | Key Finding |
|-------|----------|-------------|
| "Chain-of-Thought Prompting Elicits Reasoning" | Wei et al., arXiv 2201.11903 (2022) | +15-30% on multi-step reasoning |
| "Self-Consistency Improves Chain of Thought" | Wang et al., arXiv 2203.11171 (2022) | Multi-path voting beats single COT |
| "Tree of Thoughts" | Yao et al., arXiv 2305.10601 (2023) | Multi-branch reasoning exploration |
| "Meta-Prompting" | arXiv 2311.12055 | LLMs generate effective prompts with criteria |
| "Universal and Transferable Adversarial Attacks" | Zou et al., arXiv 2307.15043 (2023) | User input in system context enables injection |
| "Constitutional AI" | Anthropic, arXiv 2212.08073 | Rule-based constraints reduce harmful outputs |
| "Jailbreaking Black Box LLMs" | Chao et al., arXiv 2310.08419 | Injection vectors exist in well-guarded systems |
| "Lost in the Middle" | Liu et al. (2023) | Primacy + recency; middle context loss |
| "ReAct: Synergizing Reasoning and Acting" | Yao et al., arXiv 2210.03629 (2022) | Reasoning + action beats pure COT for tool use |
| "Language Models are Few-Shot Learners" | Brown et al., NeurIPS (2020) | 3-5 examples optimal for in-context learning |
| "The Unreliability of Explanations in Few-shot Prompting" | Zhou et al. (2022) | Instruction placement matters |
| "Graph of Thoughts" | Besta et al., arXiv 2308.09687 (2023) | Graph-based reasoning |

### Rules cited: 16
11 teaching-only, 5 check_regex

---

## Aggregate Statistics

| Metric | Count |
|--------|-------|
| Total classes | 35 |
| Total rules | 487+ |
| Total checkable rules (selector/regex) | 130+ |
| Total teaching-only rules | 350+ |
| Total tests | 1,255+ |
| Total unique standards/frameworks cited | 50+ |
| Total unique research papers cited | 45+ |
| Total unique RFCs/CWEs/controls | 50+ |


## Standards by Category

### Security (3 classes overlapping)
OWASP Top 10, OWASP ASVS, CWE Top 25, NIST SP 800-53, NIST SP 800-63B, NIST SP 800-175B, NIST SP 800-52, CERT Secure Coding

### Compliance (1 class)
SOC2 TSC, HIPAA Security Rule, CMMC 2.0, NIST SP 800-171, ISO 27001, NIST CSF

### Process/Methodology (1 class)
ITIL v4, Scrum, SAFe, LeSS, Kanban, CMMI (ITIL codified; others reference-only)

### Architecture/Design (1 class)
Fowler PoEAA, Richards & Ford, Hohpe & Woolf EIP, Newman Microservices, Nygard Release It!, Rozanski & Woods

### Testing (1 class)
xUnit Test Patterns, FIRST, TDD, BDD, property-based testing

### Performance (1 class)
Web Vitals, Lighthouse, RAIL model, HTTP Archive

### Prompt Engineering (1 class)
DAIR.AI, OpenAI, Anthropic, COT/ToT/GoT literature

### Accessibility (1 class)
WCAG 2.2, ARIA 1.2, Section 508, EN 301 549, Apple HIG, Material Design

### Infrastructure/Cloud (cross-cutting)
AWS Well-Architected, Google CAF/SRE, Azure CAF, 12-Factor App, CNCF

### Professional Credentials (18 classes)
ABA Model Rules, HIPAA, GAAP/GAAS/AICPA/SOX, NSPE Code, NASW/APA Codes, SPJ Code, FINRA/SEC, DEA/USP, AIA/IBC, ANA Code/NPA, FARs/FAA AIM, NAR Code/Fair Housing Act, PMBOK/PMP Code, ADA Code/CDC, NREMT/EMS, FLSA/FMLA/ADA/EEOC, ABA Judicial Code/FRE, AVMA Code/Animal Welfare Act

### PKI/Networking (cross-cutting)
RFC 5280, RFC 3647, TLS 1.2/1.3
