# AcmeCare Health Insurance — Prior Authorization Requirements
# Utilization Management Guideline Reference

---

## Overview

This document defines AcmeCare's prior authorization (PA) requirements and medical
necessity criteria for services covered under the AcmeCare Preferred PPO plan. Providers
must satisfy all applicable requirements before services are rendered, unless an emergency
exception applies.

---

## General Prior Authorization Policy

### When Prior Authorization is Required

Prior authorization is required for the following service categories:

| Category | Examples | PA Required? |
|---|---|---|
| Advanced Diagnostic Imaging | MRI, CT, PET scan | **Yes** |
| Durable Medical Equipment (DME) | CGM devices, insulin pumps, orthotics | **Yes** |
| Behavioral Health (extended) | Psychotherapy sessions beyond annual limit | **Yes** |
| Surgical Procedures (elective) | Joint replacement, spinal surgery | **Yes** |
| Specialty Medications | Biologics, specialty injectables | **Yes** |
| Routine Office Visits | PCP visits, standard lab work | No |
| Emergency Services | ER visits, urgent care | No |

### How to Submit a Prior Authorization Request

1. **Complete Form PA-200** (AcmeCare Prior Authorization Request Form)
   - Available at: `acmecare-mock.example.com/forms/PA-200`
   - Must be completed in full with all required fields
2. **Attach supporting clinical documentation** as specified per service category
3. **Submit at least 5 business days** before the scheduled service date
4. **Submission methods:**
   - Fax: 1-800-555-2266 (Utilization Review Department)
   - Online: `acmecare-mock.example.com/providers/prior-auth`
   - Mail: AcmeCare UR Dept, P.O. Box 94300, Phoenix, AZ 85070-4300

> **Important:** Submission of clinical notes alone does NOT constitute a prior
> authorization request. The PA-200 form is required in all cases.

### Response Timelines

| Request Type | Decision Timeline |
|---|---|
| Standard prior authorization | 5 business days |
| Urgent/expedited prior authorization | 72 hours |
| Medical necessity review | 15 business days |
| Retrospective review (post-service) | 30 business days |

---

## Service-Specific Prior Authorization Criteria

### 1. Continuous Glucose Monitoring (CGM) — Policy ACME-CGM-2024-001

**Applicable CPT Codes:** 95249, 95250, 95251

**Prior Authorization Requirements:**

| Requirement ID | Description | Documentation Needed |
|---|---|---|
| `REQ-STEP-METFORMIN` | Trial of first-line oral medication (Metformin) for ≥90 days | Prescription records + clinical notes showing failure or contraindication |
| `REQ-STEP-SULFONYLUREA` | Trial of second-line oral medication (sulfonylurea) for ≥90 days | Prescription records + clinical notes showing failure or contraindication |
| `REQ-HYPO-LOG` | Documented glycemic instability | 3-month BG log showing ≥3 hypoglycemic events (<70 mg/dL) OR sustained HbA1c >8.0% |

**Step Therapy Sequence:** Metformin → Sulfonylurea → CGM (must be in order)

**Medical Necessity Standard:** CGM is considered medically necessary when:
- Patient has documented failure of or contraindication to both first-line and second-line oral hypoglycemic agents
- Patient demonstrates ongoing glycemic instability (recurrent hypoglycemia or persistent hyperglycemia)
- CGM would provide clinically meaningful improvement in glycemic management

---

### 2. Lower Extremity MRI — Policy ACME-MRI-2024-002

**Applicable CPT Codes:** 73718, 73720, 73721, 73722, 73723

**Prior Authorization Requirements:**

| Requirement ID | Description | Documentation Needed |
|---|---|---|
| `REQ-PRIOR-AUTH` | Prior Authorization Form PA-200 submitted | Completed PA-200 form ≥5 business days before imaging |
| `REQ-PHYSIO-6WK` | Conservative physical therapy trial for ≥6 weeks (42 days) | PT treatment notes showing: initial eval date, ≥6 sessions, exercises performed, progress assessment, therapist recommendation |
| `REQ-CLINICAL-EXAM` | Clinical examination within 30 days of MRI request | Office visit note with: ROM assessment, joint stability testing, pain assessment, clinical impression |

**Medical Necessity Standard:** Lower extremity MRI is considered medically necessary when:
- Patient has completed a minimum 6-week trial of conservative therapy without adequate clinical improvement
- Physical examination findings suggest internal derangement or structural pathology
- Prior authorization has been obtained through the PA-200 process

**Exceptions:**
- Emergency MRI (acute trauma, suspected fracture, vascular emergency) — PA not required but must be reported within 48 hours
- Patients with prior imaging showing progressive pathology on clinical re-evaluation

---

### 3. Outpatient Psychotherapy (Extended) — Policy ACME-MH-2024-003

**Applicable CPT Codes:** 90834, 90837, 90847

**Prior Authorization Requirements:**

| Requirement ID | Description | Documentation Needed |
|---|---|---|
| `REQ-MH-BASELINE` | Sessions 1–20: Active behavioral health diagnosis + in-network provider | Diagnosis on file, provider credentials verified |
| `REQ-MH-MEDICAL-NECESSITY` | Sessions 21+: Medical necessity justification | See Medical Necessity Criteria below |

**Medical Necessity Criteria for Extended Psychotherapy (Session 21+):**

The following documentation must be submitted and each criterion must be satisfied:

1. **Validated Symptom Severity Assessment**
   - PHQ-9 ≥ 10 (moderate or greater depression severity)
   - Assessment must be from within 30 days of the extension request
   - Serial scores showing treatment trajectory preferred

2. **Treatment Plan with Measurable Goals**
   - At least 2 measurable goals with target dates
   - Goals must be specific, achievable, and clinically relevant
   - Documentation of progress toward goals

3. **Progress Documentation**
   - Evidence that patient is engaged in and benefiting from therapy
   - Documentation of specific therapeutic interventions used
   - Assessment of treatment response over the course of sessions 1–20

4. **Clinical Rationale for Continuation**
   - Explanation of why discontinuation at session 20 would be clinically inappropriate
   - Risk assessment for regression if therapy is terminated
   - Estimated number of additional sessions needed

**MHPAEA Compliance Note:**
AcmeCare's clinical review process for behavioral health treatment extensions must apply
criteria that are comparable to and no more stringent than criteria applied to analogous
medical/surgical treatment extensions (e.g., physical therapy extensions beyond standard
authorization). The 20-session limit must be evaluated for compliance with the Mental Health
Parity and Addiction Equity Act (MHPAEA), 29 USC §1185a.

---

## Appeal Process for Prior Authorization Denials

If a prior authorization request is denied, the provider and/or member may appeal
the determination. See individual denial letters for specific appeal instructions.

### Appeal Submission

| Item | Detail |
|---|---|
| **Appeal deadline** | 180 calendar days from denial notice |
| **Submit to** | AcmeCare Appeals Department, P.O. Box 94200, Phoenix, AZ 85070-4200 |
| **Fax** | 1-800-555-2265 |
| **Email** | appeals@acmecare-mock.example.com |

### External Review

If the internal appeal is denied, members may request an independent external review
through their state's Department of Insurance or Department of Managed Health Care.

---

## Statutory and Regulatory References

| Reference | Description |
|---|---|
| State Insurance Code §4521.3 | Step Therapy Protocol Override Rights |
| State Insurance Code §3891.1 | Timely Prior Authorization Review Requirements |
| State Insurance Code §6200.7 | Mental Health Coverage Parity Provisions |
| 42 CFR §423.578 | Medicare Part D Coverage Determination |
| 42 CFR §438.210 | Prior Authorization of Services (Medicaid Managed Care) |
| 42 CFR §438.910 | Parity Requirements for Medicaid Managed Care |
| 29 USC §1185a | Mental Health Parity and Addiction Equity Act (MHPAEA) |
