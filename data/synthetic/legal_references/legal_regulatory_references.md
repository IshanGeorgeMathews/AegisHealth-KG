# Legal and Regulatory References
# AegisHealth-KG — Curated Legal Material for Appeal Reasoning

---

## Overview

This document contains curated summaries of legal statutes and regulations referenced in
AegisHealth-KG's appeal generation. The system's legal retrieval component retrieves
relevant material from this document for the LLM to reference when drafting appeals.

> **Important:** The system does NOT hard-code legal conclusions. It retrieves relevant
> legal material and presents it in the appeal for the reviewer's consideration. Citing
> a law does not automatically determine eligibility.

---

## Federal Statutes and Regulations

### Mental Health Parity and Addiction Equity Act (MHPAEA)

**Citation:** 29 USC §1185a; 42 USC §300gg-26

**Summary:**
The MHPAEA, originally enacted in 1996 and significantly expanded by the Paul Wellstone
and Pete Domenici Mental Health Parity and Addiction Equity Act of 2008, requires that
group health plans and health insurance issuers ensure that financial requirements
(deductibles, copayments, coinsurance, out-of-pocket limits) and treatment limitations
(day/visit limits, frequency limitations, prior authorization requirements) applicable
to mental health or substance use disorder (MH/SUD) benefits are no more restrictive
than the predominant financial requirements or treatment limitations applied to
substantially all medical/surgical benefits covered by the plan in the same classification.

**Key Provisions Relevant to AegisHealth-KG:**

1. **Quantitative Treatment Limits (QTLs):**
   - Session limits on outpatient psychotherapy are a form of QTL
   - If a plan limits outpatient psychotherapy to 20 sessions/year, it must apply
     comparable limits to substantially all outpatient medical/surgical benefits
     in the same classification
   - If outpatient physical therapy has no session limit (or a higher limit), a
     20-session psychotherapy limit may violate MHPAEA

2. **Non-Quantitative Treatment Limits (NQTLs):**
   - Medical necessity review criteria for mental health services must be comparable
     to and applied no more stringently than criteria for medical/surgical services
   - Prior authorization processes for MH/SUD must be comparable to those for
     medical/surgical services

3. **Disclosure Requirements:**
   - Plans must provide the criteria used for medical necessity determinations upon
     request
   - Plans must provide the reason for a denial, including clinical rationale

**Applicability:** Scenario 3 — The 20-session annual limit on psychotherapy may be
subject to MHPAEA parity analysis if comparable outpatient medical/surgical services
(e.g., physical therapy) do not have analogous session limits.

---

### 42 CFR §423.578 — Medicare Part D Coverage Determination

**Summary:**
This regulation governs the process by which Medicare Part D plan sponsors make coverage
determinations for prescription drug benefits and certain related services. Key provisions:

- Plan sponsors must have a process for making timely coverage determinations
- Enrollees have the right to request a coverage determination and receive a written
  decision
- If the initial determination is unfavorable, the enrollee has the right to appeal
- Step therapy protocols must include an exception process that allows for overrides
  when clinically appropriate

**Applicability:** Scenario 1 — Referenced as regulatory basis for step therapy override
rights in diabetes medication/device coverage.

---

### 42 CFR §438.210 — Prior Authorization of Services (Medicaid Managed Care)

**Summary:**
This regulation establishes requirements for prior authorization of services in Medicaid
managed care organizations (MCOs). Key provisions:

- MCOs must have written policies and procedures for processing prior authorization
  requests
- Standard authorization decisions must be made within 14 calendar days (with possible
  14-day extension)
- Expedited authorization decisions must be made within 72 hours
- MCOs must notify enrollees of the right to appeal adverse authorization decisions
- Authorization criteria must be based on valid clinical evidence and applied consistently

**Applicability:** Scenario 2 — Referenced as regulatory framework for prior authorization
requirements and timely review obligations.

---

### 42 CFR §438.910 — Parity Requirements for Medicaid Managed Care

**Summary:**
This regulation applies MHPAEA parity requirements to Medicaid managed care plans. It
requires that Medicaid MCOs:

- Apply the same standards used under MHPAEA for commercial insurance to Medicaid
  managed care beneficiaries
- Ensure that financial requirements and treatment limitations for MH/SUD benefits
  are no more restrictive than those for medical/surgical benefits
- Document and make available their parity compliance analyses

**Applicability:** Scenario 3 — Extends MHPAEA parity requirements to Medicaid managed
care context.

---

## State Insurance Codes (Mock)

> **Note:** These are mock state insurance code provisions created for the prototype.
> They are designed to be realistic but do not correspond to actual state statutes.

### State Insurance Code §4521.3 — Step Therapy Protocol Override Rights

**Summary:**
This provision establishes the right of enrollees and their providers to override step
therapy requirements under certain conditions:

- **Clinical exception:** The provider may request a step therapy override when the
  required step therapy drugs are contraindicated, have caused adverse reactions, or
  are clinically documented as ineffective for the patient
- **Documentation requirement:** The provider must submit clinical documentation
  demonstrating that the patient has already tried and failed (or is contraindicated
  for) the required step therapy agents
- **Timeline:** The insurer must respond to step therapy override requests within
  72 hours for urgent requests and 5 business days for standard requests
- **Appeal rights:** If the override is denied, the enrollee may appeal through the
  standard appeals process

**Applicability:** Scenario 1 — Patient has documented failure of both Metformin and
sulfonylurea, establishing grounds for step therapy override.

---

### State Insurance Code §3891.1 — Timely Prior Authorization Review Requirements

**Summary:**
This provision establishes timelines and procedures for prior authorization review:

- Insurers must provide clear, accessible information about prior authorization
  requirements to providers and enrollees
- Standard prior authorization decisions must be communicated within 5 business days
- Failure to respond within the required timeline constitutes constructive approval
- Retroactive denial for failure to obtain prior authorization may be overturned on
  appeal if the services would have been authorized had the prior authorization
  request been properly submitted
- Insurers must provide a clear process for retroactive authorization requests

**Applicability:** Scenario 2 — Relevant to the appeal argument that the MRI would
have been authorized had the PA-200 form been submitted (administrative error rather
than clinical determination).

---

### State Insurance Code §6200.7 — Mental Health Coverage Parity Provisions

**Summary:**
State-level parity provisions supplementing federal MHPAEA requirements:

- All health plans sold in the state must comply with MHPAEA requirements
- State enforcement authority may investigate and enforce parity compliance
- Insurers must submit annual parity compliance reports to the Department of Insurance
- Enrollees may file parity-related complaints with the Department of Insurance
- The Department may impose fines for documented parity violations

**Applicability:** Scenario 3 — Provides state-level enforcement mechanism for MHPAEA
parity analysis.

---

## How These References Are Used in the System

```
Denial Letter Entities (CARC code + denial category)
         │
         ↓
Knowledge Graph retrieval identifies applicable policy rules
         │
         ↓
Legal retrieval component matches relevant statutes/regulations
from this document based on:
  - Denial category (e.g., STEP_THERAPY → §4521.3)
  - Service type (e.g., behavioral health → MHPAEA)
  - Policy rule type (e.g., prior auth → §3891.1)
         │
         ↓
LLM references retrieved legal material in appeal letter
(LLM does NOT determine legal conclusions — it presents
the relevant legal context for human review)
```
