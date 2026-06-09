# SOURCES — credential-pilot (Pilot Professional Standards)

All rules in `class.yaml` derive from US federal aviation regulations, FAA
advisory materials, and NTSB reporting requirements. Every rule cites its
specific source. No rule exists without a source.

## Primary Standards

### 14 CFR — Code of Federal Regulations, Title 14 (Aeronautics and Space)

#### Part 61 — Certification: Pilots, Flight Instructors, and Ground Instructors
- **14 CFR § 61.56** — Flight Review (every 24 calendar months)
- **14 CFR § 61.57** — Recent Flight Experience: Pilot in Command (currency)
  - § 61.57(b) — Night passenger-carrying: 3 takeoffs/landings in 90 days
  - § 61.57(c) — Instrument experience: 6 approaches, holds, intercepting/tracking in 6 months
  - § 61.57(d) — Instrument proficiency check after 12 months of non-compliance
- **14 CFR § 61.23** — Medical Certificates: First, Second, Third Class
- **14 CFR § 61.31** — Type rating, high-performance, complex, tailwheel endorsements
- **14 CFR § 61.133** — Commercial pilot privileges and limitations

#### Part 91 — General Operating and Flight Rules
- **14 CFR § 91.7** — Civil Aircraft Airworthiness (PIC responsibility)
- **14 CFR § 91.9** — Civil Aircraft Flight Manual, Marking, Placards (must operate within POH limitations)
- **14 CFR § 91.13** — Careless or Reckless Operation (includes operation while fatigued)
- **14 CFR § 91.17** — Alcohol and Drugs (0.04 BAC, 8 hours bottle-to-throttle)
- **14 CFR § 91.151** — Fuel Requirements for Flight in VFR Conditions (30 min day, 45 min night)
- **14 CFR § 91.155** — Basic VFR Weather Minimums (airspace-specific visibility and cloud clearance)
- **14 CFR § 91.167** — Fuel Requirements for Flight in IFR Conditions (45 min reserve)
- **14 CFR § 91.171** — VOR Equipment Check for IFR Flight (within 30 days)
- **14 CFR § 91.205** — Powered Civil Aircraft with Standard Category U.S. Airworthiness Certificate: Instrument and Equipment Requirements
- **14 CFR § 91.215** — ATC Transponder and Altitude Reporting Equipment
- **14 CFR § 91.225** — Automatic Dependent Surveillance-Broadcast (ADS-B) Out
- **14 CFR § 91.403** — General Maintenance (owner/operator responsible for airworthiness)
- **14 CFR § 91.409** — Inspections (annual, 100-hour)
- **14 CFR § 91.411** — Altimeter System and Altitude Reporting Equipment Tests (24 months)
- **14 CFR § 91.413** — ATC Transponder Tests and Inspections (24 months)

#### Part 71 — Designation of Class A, B, C, D, and E Airspace Areas
- **14 CFR Part 71** — Airspace classifications, dimensions, and requirements

#### Part 121 — Operating Requirements: Domestic, Flag, and Supplemental Operations
- **14 CFR § 121.542** — Flight Crewmember Duties (Sterile Cockpit Rule)
- **14 CFR § 121.543** — Flight Crewmember at Controls (required crew at duties)
- Subparts Q–Z — Maintenance, crew training, dispatch, operational control

#### Part 135 — Operating Requirements: Commuter and On-Demand Operations
- **14 CFR § 135.100** — Flight Crewmember Duties (Sterile Cockpit Rule, parallel to 121.542)
- **14 CFR § 135.267** — Flight Time Limitations and Rest Requirements

### FAA Aeronautical Information Manual (AIM)
- **AIM Chapter 4** — Air Traffic Control
  - Section 2 — Radio Communications Phraseology and Techniques
  - Section 3 — Airport Operations
  - Section 4 — ATC Clearances and Aircraft Separation
    - ¶ 4-4-6 — Readback / Hearback (full readback of runway/hold-short, altitude, heading)
- **AIM Chapter 5** — Air Traffic Procedures
  - Section 3 — Airport Traffic Patterns
  - Section 4 — VFR/IFR Operations
  - Section 5 — Instrument Approach Procedures
- **AIM Chapter 6** — Emergency Procedures
  - Section 1 — General
  - ¶ 6-1-2 — Emergency Declaration (Mayday, Pan-Pan, squawk 7700)
  - ¶ 6-3-1 — Distress and Urgency Procedures
- **AIM Chapter 7** — Safety of Flight
  - Section 2 — Aircraft Accident Reporting

### Advisory Circulars
- **AC 120-71** — Crew Resource Management (CRM) Training
  - Communication, situational awareness, problem-solving, decision-making, teamwork
  - Standardized challenge-and-response protocols
- **AC 60-22** — Aeronautical Decision Making (ADM)
  - PAVE checklist, DECIDE model, hazardous attitudes and antidotes
- **AC 91-92** — Pilot's Guide to a Preflight Briefing

### Pilot's Handbook of Aeronautical Knowledge (PHAK)
- **FAA-H-8083-25C** (PHAK)
  - Chapter 2 — Aircraft Structure (weight and balance)
  - Chapter 6 — Flight Controls
  - Chapter 8 — Flight Instruments
  - Chapter 9 — Flight Manuals and Other Documents (POH/W&B, MEL, checklists)
  - Chapter 10 — Weight and Balance
  - Chapter 11 — Aircraft Performance
  - Chapter 14 — Airport Operations
  - Chapter 15 — Airspace
  - Chapter 16 — Navigation
  - Chapter 17 — Aeronautical Decision-Making (ADM, PAVE, DECIDE, hazardous attitudes)
  - Chapter 18 — IFR Operations
  - Appendix A — Human Factors, IMSAFE

### NTSB — Notification and Reporting of Aircraft Accidents
- **49 CFR Part 830** — Notification and Reporting of Aircraft Accidents or Incidents and
  Overdue Aircraft, and Preservation of Aircraft Wreckage, Mail, Cargo, and Records
  - § 830.2 — Definitions (accident, incident, serious injury, substantial damage)
  - § 830.5 — Immediate Notification (2-hour requirement)
  - § 830.10 — Preservation of Aircraft Wreckage, Mail, Cargo, and Records

### Medical Standards
- **14 CFR Part 67** — Medical Standards and Certification
  - Subpart B — First-Class Airman Medical Certificate
  - Subpart C — Second-Class Airman Medical Certificate
  - Subpart D — Third-Class Airman Medical Certificate
  - Subpart E — Special Issuance
- **IMSAFE** — FAA-recommended personal health self-assessment (Illness, Medication, Stress, Alcohol, Fatigue, Emotion)

## Per-Rule Citation Table

| Rule ID | Primary Source(s) | Type |
|---------|------------------|------|
| `scope-of-practice` | 14 CFR Parts 61 & 91 (general operating rules), PHAK Ch. 9 | check_regex |
| `sterile-cockpit` | 14 CFR § 121.542, § 135.100, AIM ¶ 4-3-1 | check_regex |
| `weather-minimums` | 14 CFR § 91.155, PHAK Ch. 15 | check_regex |
| `fuel-management` | 14 CFR § 91.151, § 91.167, PHAK Ch. 11 | check_regex |
| `emergency-procedures` | AIM Ch. 6, ¶ 6-1-2, ¶ 6-3-1, PHAK Ch. 18 | check_regex |
| `medical-fitness` | 14 CFR Part 67, 14 CFR § 91.17, IMSAFE, PHAK App A | check_regex |
| `flight-checklists` | 14 CFR § 91.7, PHAK Ch. 9, NTSB accident data | teaching-only |
| `airspace-regulations` | 14 CFR Part 71, § 91.155, § 91.215, § 91.225, PHAK Ch. 15 | teaching-only |
| `communication-phraseology` | AIM Ch. 4, ¶ 4-2, ¶ 4-4-6 | teaching-only |
| `crew-resource-management` | AC 120-71, PHAK Ch. 17, NTSB CRM-related accident reports | teaching-only |
| `maintenance` | 14 CFR § 91.7, § 91.403, § 91.409, § 91.411, § 91.413 | teaching-only |
| `weight-balance` | 14 CFR § 91.9, PHAK Ch. 10, POH data | teaching-only |
| `currency-proficiency` | 14 CFR § 61.56, § 61.57, § 61.31 | teaching-only |
| `risk-management-adm` | AC 60-22, PHAK Ch. 17, PAVE checklist, DECIDE model | teaching-only |
| `fatigue-rest` | 14 CFR § 91.13, Part 117, FAA Fatigue Management Guide | teaching-only |
| `ntsb-reporting` | 49 CFR Part 830 (NTSB), AIM Ch. 7, § 7-2 | teaching-only |

## Coverage Honesty

**Layer 1 (check_regex) rules** cover codifiable violations with high precision:
AI credential claims (posing as pilot/captain), sterile cockpit violations,
weather-minimums violations, fuel-reserve violations, delayed emergency
declarations, and medical-fitness violations. They do **not** cover nuanced
judgments (CRM effectiveness, ADM quality, weight-and-balance arithmetic) —
those are deferred to the LLM judge (Layer 2, Phase 1).

The honest coverage boundary for credential-pilot:
- ~35% of pilot professional standards are codifiable at Layer 1
  (clear pattern violations like credential claims, checklist step-skipping,
  non-standard phraseology patterns, equipment-limit violations)
- ~65% need LLM or human judgment (CRM, ADM, aeronautical decision-making
  evaluation, nuanced situational awareness, checklist sequence analysis)

**What is NOT covered:** Full aeronautical knowledge requires understanding of
regional terrain, instrument procedure analysis, real-time weather interpretation,
specific aircraft POH performance calculations, and practical flying judgment.
This class teaches an LLM to recognize the most common pilot professional
standards and to follow them at generation time. It does not certify the AI to
act as a pilot-in-command or replace a certificated pilot's authority and
responsibility.

## Key Research and Commentary

| Source | Relevance |
|--------|-----------|
| FAA Airman Certification Standards (ACS) | Current standards for pilot testing; indicates regulatory emphasis areas |
| NTSB Safety Alerts (SA-081, SA-049) | Checklist non-use, fuel mismanagement, weather-related accident causality |
| FAA General Aviation Joint Steering Committee (GA JSC) | Safety enhancement focus areas: loss of control in flight, weather, fuel |
| "Sterile Cockpit" — NASA ASRS Directline, No. 4 | CRM case studies on sterile cockpit compliance |
| "The Five Hazardous Attitudes" — FAA Safety Briefing | ADM training; hazardous attitudes and their antidotes |
| IMSAFE Checklist — FAA Safety Team (FAASTeam) | Standardized health self-assessment for pilots |
| Part 117 Final Rule (2011) — Flightcrew Member Duty and Rest | Fatigue science; fatigue risk management systems |
| AC 120-72 — Fatigue Education and Awareness Training | Fatigue symptoms, mitigation strategies |

## Verification

Each rule with `check_regex` is FAIL/PASS tested in
`tests/test_credential_pilot.py`. Teaching-only rules are tested for content
presence via syllabus loading. A rule cannot ship without its test pair.
