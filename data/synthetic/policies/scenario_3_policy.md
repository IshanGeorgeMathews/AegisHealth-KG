# Mock Insurance Policy — Scenario 3
# AcmeCare Health Plan: Outpatient Psychotherapy Coverage

## Policy ID
`ACME-MH-2024-003`

## Payer
AcmeCare Health Insurance

## Effective Date
2024-01-01

## Policy Category
Behavioral Health — Outpatient Psychotherapy Services

---

## Covered Procedure
- **CPT Code:** 90837
- **Description:** Psychotherapy, 53 minutes or more with patient

## Covered Diagnoses
- **F33.1** — Major Depressive Disorder, recurrent episode, moderate
- **F33.0** — Major Depressive Disorder, recurrent episode, mild
- **F33.2** — Major Depressive Disorder, recurrent episode, severe without psychotic features

---

## Coverage Criteria

### Standard Authorization: Sessions 1–20
Outpatient psychotherapy sessions 1 through 20 per calendar year are authorized
**without additional clinical review**, provided:

- **Requirement ID:** `REQ-MH-BASELINE`
- The patient has an active behavioral health diagnosis on file
- The treating provider is an in-network licensed mental health professional
- Sessions are documented with standard progress notes

### Extended Authorization: Sessions 21+
Sessions beyond 20 per calendar year **require documented medical necessity
justification** submitted for clinical review.

- **Requirement ID:** `REQ-MH-MEDICAL-NECESSITY`
- **Evidence Required:**
  - Validated symptom severity assessment (e.g., PHQ-9 score ≥ 10, indicating
    moderate or greater depression severity)
  - Treatment plan with measurable goals demonstrating ongoing need
  - Documentation of treatment progress showing that the patient is engaged
    and benefiting from therapy but has not yet achieved treatment goals
  - Clinical rationale explaining why discontinuation at session 20 would be
    clinically inappropriate for this patient

### Session Limit Review
AcmeCare reviews session limit denials within **15 business days** of receiving
a medical necessity justification package.

---

## Important Legal Context

### Mental Health Parity and Addiction Equity Act (MHPAEA)
The MHPAEA requires that financial requirements and treatment limitations
applied to mental health and substance use disorder benefits are **no more
restrictive** than the predominant requirements or limitations applied to
substantially all medical/surgical benefits in the same classification.

**This policy's session limit must be evaluated for MHPAEA compliance:**
- If comparable medical/surgical outpatient services (e.g., physical therapy)
  do not have analogous session limits, the 20-session limit on psychotherapy
  may be subject to parity analysis.
- AcmeCare's clinical review process for sessions 21+ must apply criteria
  that are comparable to and no more stringent than criteria applied to
  analogous medical/surgical treatment extensions.

> **Note:** This mock policy includes the session limit to create a realistic
> appeal scenario. The appeal analysis should evaluate whether the application
> of this limit is consistent with MHPAEA principles, not assume that citing
> MHPAEA automatically overrides the limit.

---

## Authorization Workflow

```
Sessions 1–20: Auto-authorized (no additional review)
          │
          ↓ (session 21 requested)
Session 21+: Medical Necessity Review Required
          │
          ├── Justification package submitted → Clinical Review (15 business days)
          │         │
          │         ├── Approved → Sessions authorized
          │         └── Denied → CARC CO-50 / MEDICAL_NECESSITY_NOT_ESTABLISHED
          │
          └── No justification submitted → Automatic Denial
```

---

## Denial Triggers

| Condition | Result |
|---|---|
| Session 21+ without medical necessity justification | Denial: `MEDICAL_NECESSITY_NOT_ESTABLISHED` |
| PHQ-9 score < 10 (mild/minimal severity) | Denial: `MEDICAL_NECESSITY_NOT_ESTABLISHED` |
| No measurable treatment goals documented | Denial: `MEDICAL_NECESSITY_NOT_ESTABLISHED` |
| Adequate justification with PHQ-9 ≥ 10 + treatment plan | **Approved** |

---

## Statutory References
- Mental Health Parity and Addiction Equity Act (MHPAEA), 29 USC §1185a
- 42 CFR §438.910 — Parity Requirements for Medicaid Managed Care
- State Insurance Code §6200.7 — Mental Health Coverage Parity Provisions
