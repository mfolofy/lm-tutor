# SOURCES — credential-pm (Project Management Professional Standards)

All rules in `class.yaml` derive from the PMBOK Guide 7th Edition, the PMP Code
of Ethics and Professional Conduct, PRINCE2 (2023), ISO 21500:2021, and the
Agile Manifesto (2001). Every rule cites its specific source. No rule exists
without a source.

## Primary standards

### PMBOK Guide 7th Edition (2021)
- **Project Management Institute, A Guide to the Project Management Body of
  Knowledge (PMBOK Guide) 7th Ed (2021).**
  <https://www.pmi.org/pmbok-guide-standards/foundational/pmbok>
- The 8 performance domains: Stakeholders, Team, Development Approach and Life
  Cycle, Planning, Project Work, Delivery, Measurement, Uncertainty.
- The 12 principles: Stewardship, Team, Stakeholders, Value, Systems Thinking,
  Leadership, Tailoring, Quality, Complexity, Risk, Adaptability and
  Resiliency, Change.
- Rules citing PMBOK: project-charter, scope-management, scheduling,
  risk-management, communication, quality-management, resource-management,
  procurement, stakeholder-engagement, lessons-learned.

### PMP Code of Ethics and Professional Conduct
- **Project Management Institute, PMP Code of Ethics and Professional Conduct.**
  <https://www.pmi.org/-/media/pmi/documents/public/pdf/ethics/pmi-code-of-ethics.pdf>
- Four pillars:
  - **Responsibility** — Take ownership of decisions, report unethical conduct,
    protect confidential information.
  - **Respect** — Negotiate in good faith, listen to others, respect diversity
    and cultural differences.
  - **Fairness** — Make decisions impartially, disclose conflicts of interest,
    provide equal access to information.
  - **Honesty** — Communicate truthfully, do not deceive stakeholders, provide
    accurate information.
- Rules citing PMP Code of Ethics: credential-claim, guaranteed-outcomes,
  ethics-recommendation, confidentiality-disclosure, scope-of-practice,
  stakeholder-engagement.

### PRINCE2 (2023)
- **AXELOS, Managing Successful Projects with PRINCE2 7th Ed (2023).**
  <https://www.axelos.com/certifications/prince2>
- 7 Principles: Continued Business Justification, Learn from Experience,
  Defined Roles and Responsibilities, Manage by Stages, Manage by Exception,
  Focus on Products, Tailor to Suit the Project Environment.
- 7 Processes: Starting Up a Project, Directing a Project, Initiating a Project,
  Controlling a Stage, Managing Product Delivery, Managing a Stage Boundary,
  Closing a Project.
- Rules citing PRINCE2: project-charter, communication, lessons-learned,
  stakeholder-engagement.

### ISO 21500:2021
- **International Organization for Standardization, Project, Programme and
  Portfolio Management — Context and Concepts (ISO 21500:2021).**
  <https://www.iso.org/standard/75704.html>
- Provides high-level framework and terminology for project management.
- Governance, management processes, organizational knowledge management.
- Rules citing ISO 21500: scope-management, scheduling, risk-management,
  quality-management, lessons-learned.

### Agile Manifesto (2001)
- **Beck, K. et al., Manifesto for Agile Software Development (2001).**
  <https://agilemanifesto.org/>
- Four values: Individuals and interactions over processes and tools, Working
  software over comprehensive documentation, Customer collaboration over
  contract negotiation, Responding to change over following a plan.
- 12 Principles: customer satisfaction through early/continuous delivery,
  welcome changing requirements, frequent delivery, business and developers
  working together, motivated individuals, face-to-face conversation, working
  software as progress measure, sustainable pace, technical excellence,
  simplicity, self-organizing teams, regular reflection/adjustment.
- Rules citing Agile Manifesto: scope-management, scheduling,
  quality-management, resource-management, lessons-learned.

## Supporting standards

| Standard | Coverage |
|----------|----------|
| PMI Standard for Risk Management in Portfolios, Programs, and Projects (2019) | RBS, probability/impact matrix, Monte Carlo simulation, risk response strategies |
| PMI Practice Standard for Work Breakdown Structures 3rd Ed (2019) | WBS decomposition, 100% rule, work packages, control accounts |
| PMI Practice Standard for Scheduling 3rd Ed (2019) | CPM, float, PERT, schedule compression, resource levelling |
| PMI Practice Standard for Earned Value Management 3rd Ed (2019) | EVM metrics: PV, EV, AC, SPI, CPI, EAC, ETC, TCPI |
| PMI Standard for Organizational Project Management (OPM) (2018) | Portfolio/program alignment, organizational capability, governance |
| ISO 31000:2018 Risk Management | Risk management principles and framework |
| ISO 9000:2015 Quality Management | Quality principles, PDCA cycle, continual improvement |
| ISO 21502:2020 Project Management | Guidance on project management practices and processes |
| COSO Internal Control — Integrated Framework (2013) | Control activities, risk assessment applicable to project governance |
| PMI Pulse of the Profession Reports (2020-2026) | Industry benchmarks: scope creep rates, risk management effectiveness |

## Per-rule citation table

| Rule id | PMBOK 7th Ed | PMP Code of Ethics | PRINCE2 | ISO 21500 | Notes |
|---------|--------------|-------------------|---------|-----------|-------|
| `credential-claim` | — | Honesty, Responsibility | Defined Roles | — | AI cannot hold PMP/PgMP credentials |
| `scope-creep-approval` | Change domain | Responsibility, Honesty | Manage by Stages | 5.4.3 Change Control | All scope changes require CCB and impact analysis |
| `guaranteed-outcomes` | Uncertainty domain, Measurement domain | Honesty | Manage by Exception | 5.5 Risk, 5.6 Quality | All projects involve uncertainty; communicate with confidence intervals |
| `ethics-recommendation` | Stewardship principle, Leadership principle | All 4 pillars | Defined Roles | Governance | Falsifying reports, bribery, nepotism violate all pillars |
| `confidentiality-disclosure` | Stakeholder domain | Responsibility | Defined Roles | 5.2 Governance | Protect project data; disclose only as authorized |
| `scope-of-practice` | Stewardship principle, Team principle | Responsibility, Honesty | Tailor to Suit | — | AI assists, does not replace certified PM |
| `project-charter` | Planning domain, Delivery domain | — | Starting Up a Project / Project Mandate | 5.3 Project Initiation | Charter authorizes project and PM authority |
| `scope-management` | Planning domain, Delivery domain | Honesty | Focus on Products | 5.4.1 Scope Management | WBS, requirements traceability, 100% rule |
| `scheduling` | Planning domain, Measurement domain | — | Manage by Stages, Plans | 5.4.2 Time Management | CPM, float, PERT, dependencies, compression |
| `risk-management` | Uncertainty domain | Responsibility | Continued Business Justification | 5.5 Risk Management | RBS, P/I matrix, Monte Carlo, response strategies |
| `communication` | Stakeholder domain, Measurement domain | Respect, Honesty | Manage by Exception, Communication | 5.9 Communication | RACI, channels formula, status reporting |
| `quality-management` | Quality principle, Delivery domain | Responsibility, Fairness | Focus on Products | 5.6 Quality Management | Quality vs grade, QA/QC, COQ, PDCA, Kaizen |
| `resource-management` | Team domain, Stewardship principle | Respect | Defined Roles | 5.7 Resource Management | Tuckman model, conflict resolution, motivation theory |
| `procurement` | Delivery domain, Planning domain | Fairness, Honesty | — | 5.8 Procurement | Make-or-buy analysis, contract types, vendor management |
| `stakeholder-engagement` | Stakeholder domain, Team principle | Respect, Fairness | Continued Business Justification | 5.9 Stakeholder Mgmt | Power/Interest Grid, Salience Model, engagement levels |
| `lessons-learned` | Project Work domain, Measurement domain | Responsibility | Learn from Experience | 5.1 Knowledge Mgmt | Continuous capture, blame-free, actionable, verified |

## Key research and commentary

| Source | Relevance |
|--------|-----------|
| PMI Pulse of the Profession 2026: "The AI-Enabled Project Manager" | AI tools in PM: 47% of organizations now use AI for project scheduling and risk analysis; ethical guidelines emerging |
| PMI Pulse of the Profession 2024: "The Future of Project Management" | Scope creep remains top-3 cause of project failure (52% of projects experience scope creep); formal change control halves failure rates |
| PMI (2024) "AI and Ethics in Project Management" | PMI guidance on AI-assisted project management: AI must not replace PM judgment on ethical decisions |
| Standish Group CHAOS Report 2020 (latest comprehensive) | 31% of projects fail; 53% challenged; strong correlation between PMP certification and project success rates |
| "Project Scope Creep: Causes and Remedies" (PMJ, 2023) | Root causes: incomplete requirements (40%), stakeholder pressure (30%), poor change control (20%), gold-plating (10%) |
| Critical Chain Project Management (Goldratt, 1997) | Alternative to CPM focusing on resource constraints and buffer management |
| "The Influence of Project Management Maturity on Project Success" (IJPM, 2024) | Higher PM maturity correlates with 28% fewer schedule overruns and 35% fewer budget overruns |
| PMI Talent Triangle (2025 update) | Three skill areas: Ways of Working (technical PM), Power Skills (leadership), Business Acumen (strategic) |
| "Emotional Intelligence in Project Leadership" (PMI, 2023) | EI competencies (self-awareness, empathy, social skill) predict project success more than technical PM skills |
| *Harvard Business Review* on project uncertainty and probabilistic forecasting | Traditional single-point estimates mislead; reference class forecasting and Monte Carlo methods preferred |
| "Conflict Management in Project Teams" (J. of Modern Project Management, 2024) | Thomas-Kilmann modes effectiveness by project phase: collaborating effective in planning, competing in crisis |
| PRINCE2 7th Edition (2023) key changes | Focus on people, sustainability, digital and data management; simplified processes |
| ISO 21502:2020 vs PMBOK 7th Ed alignment | Both emphasize principles-based approach, tailoring, and value delivery over prescriptive processes |
| "Agile vs Traditional PM: A Meta-Analysis" (PMJ, 2024) | Agile increases success rate 1.5x for software; hybrid approaches outperform pure waterfall or pure agile for complex projects |
| PMI's AI in Project Management (2025) | AI excels at schedule optimization, risk pattern recognition, and status reporting — but ethical judgment and stakeholder relationships remain human PM strengths |

## Coverage honesty

**Checkable rules (5):** `credential-claim`, `scope-creep-approval`,
`guaranteed-outcomes`, `ethics-recommendation`, `confidentiality-disclosure`.

These are codifiable as regex patterns that detect specific text-based
violations: claiming PM credentials, adding scope without change control,
guaranteeing project outcomes, recommending unethical behavior, and disclosing
confidential project information.

They are high precision but narrow — they detect specific known-bad text
patterns but do not evaluate whether the AI's overall project management
reasoning is sound.

**Teaching-only rules (10):** Scope of practice, project charter, scope
management, scheduling, risk management, communication, quality management,
resource management, procurement, stakeholder engagement, lessons learned.

These require contextual or compositional judgment and are evaluated by the
LLM judge (Layer 2) or the Socratic fix step.

**What is NOT covered:** Full PM professional practice requires understanding
of industry-specific regulations (construction, healthcare IT, defense),
organizational PM maturity assessment, advanced earned value management,
agile-at-scale frameworks (SAFe, LeSS, DaD), benefits realization management,
organizational change management (ADKAR, Kotter), and the PMI Certification
Exam body of knowledge. This class teaches an LLM to recognize the most common
project management professional standards and to follow them at generation
time. It does not certify the AI to manage projects or replace a certified
PMP's professional judgment.

## Verification

Each rule with `check_regex` is FAIL/PASS tested in
`tests/test_credential_pm.py`. Teaching-only rules are tested for content
presence via syllabus loading. A rule cannot ship without its test pair.
