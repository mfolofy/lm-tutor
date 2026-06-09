# SOURCES — devops (DevOps, SRE, and CI/CD Standards)

All rules in `class.yaml` derive from foundational DevOps and SRE literature,
industry frameworks, and cloud provider best-practice guides. Every rule cites
specific standards or authoritative texts. No rule exists without a source.

## Primary standards

### Google SRE Books

- **Site Reliability Engineering** (Beyer, Jones, Petoff & Murphy, O'Reilly 2016).
  <https://sre.google/sre-book/table-of-contents/>
  - Chapter 3 — Embracing Risk (error budgets, SLO/SLI rationale)
  - Chapter 4 — Service Level Objectives (slo-sli rule)
  - Chapter 5 — Eliminating Toil (incident-response, runbook-documentation)
  - Chapter 6 — Monitoring Distributed Systems (monitoring-observability, alerting)
  - Chapter 9 — Simplicity (dependency-management)
  - Chapter 11 — Being On-Call (incident-response, alerting)
  - Chapter 12 — Effective Troubleshooting (runbook-documentation)
  - Chapter 13 — Emergency Response (incident-response)
  - Chapter 14 — Managing Incidents (incident-response)
  - Chapter 24 — Daily Cycle of Capacity Planning (capacity-planning)
  - Chapter 25 — Data Integrity (backup-disaster-recovery)
  - Chapter 29 — Design for a Container-Based Architecture (containerization)

- **The Site Reliability Workbook** (Beyer, Harvey, Murphy, Rensin, O'Reilly 2018).
  <https://sre.google/workbook/table-of-contents/>
  - Chapter 2 — Implementing SLOs (slo-sli)
  - Chapter 3 — Implementing Error Budgets (slo-sli)
  - Chapter 4 — Monitoring (monitoring-observability)
  - Chapter 5 — Alerting (alerting)
  - Chapter 14 — Incident Response (incident-response)
  - Chapter 17 — Capacity Planning (capacity-planning)

### DORA (Accelerate)

- **Forsgren, Humble, Kim — Accelerate: The Science of Lean Software and DevOps**
  (IT Revolution Press, 2018). <https://itrevolution.com/product/accelerate/>
  - Chapter 2 — Measuring Performance (dora-metrics)
  - Chapter 3 — Implementing Continuous Delivery (ci-pipeline-gates, cd-deployment)
  - Chapter 4 — Version Control (infrastructure-as-code)
  - Chapter 7 — Lean Management and Monitoring (monitoring-observability)
  - Chapter 8 — Test and Deploy Automation (ci-pipeline-gates, cd-deployment)
  - Chapter 9 — Change Management (change-management)

- **DORA State of DevOps Reports** (2014–2024).
  <https://cloud.google.com/devops/state-of-devops/>
  - 2018: Four key metrics defined and validated
  - 2019: SRE integration with DevOps practices
  - 2020: Evolution of deployment patterns
  - 2021: Security practices in CI/CD
  - 2022: Platform engineering and internal developer platforms
  - 2023: AI-assisted development impacts on DevOps

### ITIL 4

- **ITIL 4 Foundation** (AXELOS, 2019).
  <https://www.axelos.com/certifications/itil-service-management/>
  - Service Value Chain (change-management, incident-response)
  - Change Enablement Practice (change-management)
  - Incident Management Practice (incident-response)
  - Service Configuration Management (infrastructure-as-code)
  - Deployment Management (cd-deployment-patterns, feature-flags)
  - Capacity and Performance Management (capacity-planning)
  - Availability Management (backup-disaster-recovery, slo-sli)
  - IT Asset Management (cost-optimization)

### AWS Well-Architected Framework

- **AWS Well-Architected Framework** (aws.amazon.com/well-architected).
  - Operational Excellence Pillar
    - OPS 1 — Operations as Code (infrastructure-as-code)
    - OPS 2 — Changes with Documentation (change-management)
    - OPS 3 — Anticipate Failure (backup-disaster-recovery)
    - OPS 5 — Learn from Operations (incident-response)
  - Security Pillar — SEC 9 — Secrets Management (secrets-management)
  - Reliability Pillar
    - REL 1 — Foundations (backup-disaster-recovery)
    - REL 6 — Monitoring (monitoring-observability, alerting)
    - REL 9 — Planning for Disaster (backup-disaster-recovery)
  - Performance Efficiency Pillar
    - PERF 1 — Selection (capacity-planning)
    - PERF 5 — Tradeoffs (cost-optimization)
  - Cost Optimization Pillar
    - COST 1 — Practice Cloud Financial Management (cost-optimization)
    - COST 2 — Expenditure Awareness (cost-optimization)
    - COST 3 — Service Usage (cost-optimization)
    - COST 5 — Managed Services (cost-optimization)

### CNCF Trail Map

- **Cloud Native Trail Map** (cncf.io/trailmap).
  - Stage 1 — Containerization (containerization)
  - Stage 2 — CI/CD (ci-pipeline-gates, cd-deployment-patterns)
  - Stage 3 — Observability (monitoring-observability, alerting)
  - Stage 5 — Service Mesh, Secrets, and Configuration (secrets-management)
  - Stage 7 — Observability at Scale (slo-sli, dora-metrics)

### Twelve-Factor App

- **Wiggins — The Twelve-Factor App** (2011). <https://12factor.net/>
  - II — Dependencies (dependency-management)
  - III — Config (secrets-management)
  - IV — Backing Services (backup-disaster-recovery)
  - V — Build, Release, Run (ci-pipeline-gates, cd-deployment-patterns)
  - VI — Processes (containerization)
  - VII — Port Binding (containerization)
  - X — Dev/Prod Parity (infrastructure-as-code)
  - XI — Logs (monitoring-observability)
  - XII — Admin Processes (runbook-documentation)

## Complementary references

### Deployment Patterns

- **Fowler — BlueGreenDeployment** (martinfowler.com/bliki/BlueGreenDeployment.html)
  - Blue-green deployment pattern definition
  - Load balancer switching between environments
  - Zero-downtime deployment
- **Sato — CanaryRelease** (martinfowler.com/bliki/CanaryRelease.html)
  - Incremental traffic shifting pattern
  - Health-check gated promotion
  - Auto-rollback on failure

### Feature Flags

- **Hodson — Feature Toggles (aka Feature Flags)** (martinfowler.com/articles/feature-toggles.html, 2017)
  - Toggle types: release, experiment, ops, permissioning
  - Toggle best practices and anti-patterns
  - Toggle removal and technical debt

### Incident Management

- **VictorOps (Splunk) — Incident Management Process** guidance
  - SEV1-SEV4 severity definitions
  - War room best practices
  - Blameless postmortem culture
- **Atlassian — Incident Management Handbook** (<https://www.atlassian.com/incident-management>)
  - Incident severity matrix
  - Communication templates
  - Post-incident review process

## Per-rule sources

| Rule | Primary sources |
|------|----------------|
| dora-metrics | Accelerate Ch. 2; DORA State of DevOps Reports |
| ci-pipeline-gates | Accelerate Ch. 3, 8; 12 Factor V; CNCF Trail Map Stage 2 |
| cd-deployment-patterns | Accelerate Ch. 3, 8; ITIL 4 Deployment Mgmt; Fowler BlueGreenDeployment; Sato CanaryRelease |
| incident-response | SRE Book Ch. 11-14, SRE Workbook Ch. 14; ITIL 4 Incident Mgmt; Atlassian Incident Mgmt Handbook |
| monitoring-observability | SRE Book Ch. 6, SRE Workbook Ch. 4; Accelerate Ch. 7; CNCF Trail Map Stage 3, 7; 12 Factor XI |
| alerting | SRE Book Ch. 6, 11; SRE Workbook Ch. 5; AWS WA REL 6 |
| slo-sli | SRE Book Ch. 3-4, SRE Workbook Ch. 2-3; CNCF Trail Map Stage 7; AWS WA REL |
| infrastructure-as-code | Accelerate Ch. 4; 12 Factor X; AWS WA OPS 1; ITIL 4 Config Mgmt; CNCF Trail Map |
| containerization | SRE Book Ch. 29; 12 Factor VI, VII; CNCF Trail Map Stage 1; Docker Best Practices |
| secrets-management | AWS WA SEC 9; 12 Factor III; CNCF Trail Map Stage 5; OWASP Secrets Management |
| backup-disaster-recovery | SRE Book Ch. 25; AWS WA REL 1, 9; Wells Fargo AWS WA COST 5; 12 Factor IV |
| change-management | Accelerate Ch. 9; ITIL 4 Change Enablement; AWS WA OPS 2; SRE Book Ch. 13 |
| capacity-planning | SRE Book Ch. 24, SRE Workbook Ch. 17; AWS WA PERF 1; ITIL 4 Capacity Mgmt |
| cost-optimization | AWS WA COST 1-5; Wells Framework; FinOps Foundation Principles |
| dependency-management | 12 Factor II; OWASP Dependency Check; SRE Book Ch. 9 |
| feature-flags | Fowler Feature Toggles; ITIL 4 Deployment Mgmt; LaunchDarkly Best Practices |
| runbook-documentation | SRE Book Ch. 5, 12; SRE Workbook Ch. 14; ITIL 4 Service Value Chain |

## Anti-pattern sources

- **Google SRE — "Blameless Postmortems"** (sre.google/resources/postmortem)
- **Google SRE — "Alert Fatigue"** (sre.google/monitoring)
- **AWS — "Well-Architected Anti-Patterns"** (docs.aws.amazon.com/wellarchitected)
- **CNCF — "Cloud Native Anti-Patterns"** (tag-app-delivery.cncf.io)
- **Webb — "9 Anti-Patterns Every DevOps Practitioner Should Know"** (devops.com, 2023)
- **O'Reilly — "DevOps Anti-Patterns"** (2023, ISBN 978-1-098-13393-5)
