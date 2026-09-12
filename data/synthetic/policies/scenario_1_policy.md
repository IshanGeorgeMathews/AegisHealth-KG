# Mock Insurance Policy — Scenario 1
# AcmeCare Health Plan: Continuous Glucose Monitoring (CGM) Coverage

## Policy ID
`ACME-CGM-2024-001`

## Payer
AcmeCare Health Insurance

## Effective Date
2024-01-01

## Policy Category
Durable Medical Equipment — Continuous Glucose Monitoring Systems

---

## Covered Procedure
- **CPT Code:** 95251
- **Description:** Ambulatory continuous glucose monitoring of interstitial tissue fluid via a subcutaneous sensor for a minimum of 72 hours; analysis, interpretation and report

## Covered Diagnoses
- **E11.9** — Type 2 Diabetes Mellitus without complications
- **E11.65** — Type 2 Diabetes Mellitus with hyperglycemia

---

## Coverage Criteria

### Prerequisite 1: Step Therapy — First-Line Oral Medication
The patient **must** have documentation of a trial of Metformin (or a clinically
documented contraindication to Metformin) for a minimum of **90 days** prior to
the CGM authorization request.

- **Requirement ID:** `REQ-STEP-METFORMIN`
- **Evidence Required:** Prescription records showing Metformin dispensation AND
  clinical notes documenting inadequate glycemic control (HbA1c > 7.0%)
  despite compliance, OR documented adverse reaction/contraindication.

### Prerequisite 2: Step Therapy — Second-Line Oral Medication
The patient **must** have documentation of a trial of a sulfonylurea agent
(e.g., Glipizide, Glyburide, Glimepiride) for a minimum of **90 days** prior
to the CGM authorization request.

- **Requirement ID:** `REQ-STEP-SULFONYLUREA`
- **Evidence Required:** Prescription records showing sulfonylurea dispensation
  AND clinical notes documenting inadequate glycemic control (HbA1c > 7.0%)
  despite compliance with both Metformin and the sulfonylurea, OR documented
  adverse reaction/contraindication.

### Prerequisite 3: Clinical Documentation
The patient **must** have a documented history of recurrent hypoglycemic events
OR persistent hyperglycemia despite dual oral therapy.

- **Requirement ID:** `REQ-HYPO-LOG`
- **Evidence Required:** A minimum 3-month log of blood glucose readings
  showing at least 3 documented hypoglycemic events (blood glucose < 70 mg/dL)
  OR sustained HbA1c > 8.0% on most recent lab work.

---

## Step Therapy Sequence (Mandatory Order)

```
Step 1: Trial of Metformin (≥90 days)
          │
          ↓ (documented failure or contraindication)
Step 2: Trial of Sulfonylurea (≥90 days)
          │
          ↓ (documented failure or contraindication)
Step 3: CGM Authorization Eligible
```

**All steps must be completed in order.** Skipping a step results in denial
under CARC code CO-167 with mock category `STEP_THERAPY_NOT_SATISFIED`.

---

## Denial Triggers

| Condition | Result |
|---|---|
| No documented Metformin trial | Denial: `STEP_THERAPY_NOT_SATISFIED` |
| No documented Sulfonylurea trial | Denial: `STEP_THERAPY_NOT_SATISFIED` |
| No 3-month glucose/hypoglycemia log | Denial: `STEP_THERAPY_NOT_SATISFIED` |
| All steps documented | **Approved** |

---

## Statutory References
- State Insurance Code §4521.3 — Step Therapy Protocol Override Rights
- 42 CFR §423.578 — Medicare Part D Coverage Determination
