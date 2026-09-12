# Mock Insurance Policy — Scenario 2
# AcmeCare Health Plan: Lower Extremity MRI Coverage

## Policy ID
`ACME-MRI-2024-002`

## Payer
AcmeCare Health Insurance

## Effective Date
2024-01-01

## Policy Category
Diagnostic Imaging — Magnetic Resonance Imaging (MRI)

---

## Covered Procedure
- **CPT Code:** 73721
- **Description:** Magnetic resonance imaging, any joint of lower extremity; without contrast material(s)

## Covered Diagnoses
- **M25.561** — Pain in right knee
- **M25.562** — Pain in left knee
- **M23.21** — Derangement of anterior horn of medial meniscus due to old tear or injury, right knee

---

## Coverage Criteria

### Prerequisite 1: Prior Authorization Required
All non-emergency lower extremity MRI requests **require prior authorization**
from AcmeCare Utilization Review before the imaging study is performed.

- **Requirement ID:** `REQ-PRIOR-AUTH`
- **Evidence Required:** Completed Prior Authorization Request Form (AcmeCare
  Form PA-200) submitted at least 5 business days before the scheduled imaging
  date.

### Prerequisite 2: Conservative Therapy Documentation
The patient **must** have documentation of a trial of conservative physical
therapy for the affected joint for a minimum of **6 weeks (42 days)** prior to
the MRI authorization request.

- **Requirement ID:** `REQ-PHYSIO-6WK`
- **Evidence Required:** Physical therapy treatment notes showing:
  - Date of initial PT evaluation
  - Minimum of 6 PT sessions over 6 weeks
  - Description of exercises/modalities performed
  - Assessment of patient progress/response to therapy
  - Therapist's recommendation regarding continued treatment or advanced imaging

### Prerequisite 3: Clinical Examination
The referring physician **must** have performed and documented a physical
examination of the affected joint within **30 days** of the MRI request.

- **Requirement ID:** `REQ-CLINICAL-EXAM`
- **Evidence Required:** Office visit note documenting:
  - Range of motion assessment
  - Joint stability testing (e.g., Lachman test, McMurray test for knee)
  - Pain assessment with validated scale
  - Clinical impression and rationale for imaging

---

## Authorization Workflow

```
Step 1: Clinical Examination (within 30 days)
          │
          ↓
Step 2: Conservative Physical Therapy (≥6 weeks, ≥6 sessions)
          │
          ↓
Step 3: Submit Prior Authorization Form PA-200
          │
          ↓
Step 4: Utilization Review Decision (within 5 business days)
          │
          ↓
Step 5: MRI Approved or Denied
```

**Prior Authorization must be obtained BEFORE the imaging study.**
Failure to obtain prior authorization results in denial under CARC code CO-197
with mock category `PRIOR_AUTH_MISSING`.

---

## Denial Triggers

| Condition | Result |
|---|---|
| No Prior Authorization Form PA-200 submitted | Denial: `PRIOR_AUTH_MISSING` |
| Physical therapy < 6 weeks documented | Denial: `PRIOR_AUTH_MISSING` |
| No clinical examination within 30 days | Denial: `PRIOR_AUTH_MISSING` |
| All prerequisites documented | **Approved** |

---

## Statutory References
- State Insurance Code §3891.1 — Timely Prior Authorization Review Requirements
- 42 CFR §438.210 — Prior Authorization of Services (Medicaid Managed Care)
