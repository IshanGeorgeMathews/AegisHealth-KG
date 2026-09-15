# Patient Clinical Records — Maria Gonzalez (Scenario 1)
# AegisHealth-KG Synthetic EHR Data

---

## Patient Demographics

| Field | Value |
|---|---|
| **Name** | Maria Gonzalez |
| **Date of Birth** | April 12, 1968 (Age 56) |
| **Gender** | Female |
| **MRN** | MRN-2019-44821 |
| **Insurance Member ID** | ACM-8827451-01 |

---

## Problem List (Active)

| # | Diagnosis | ICD-10 | Date Onset | Status |
|---|---|---|---|---|
| 1 | Type 2 Diabetes Mellitus without complications | E11.9 | 2019-06-15 | Active |
| 2 | Essential hypertension | I10 | 2017-03-22 | Active, controlled |
| 3 | Obesity, BMI 32.4 | E66.01 | 2015-01-10 | Active |

---

## Medication List (Current as of 2024-08-15)

| Medication | Dosage | Route | Frequency | Start Date | Prescriber |
|---|---|---|---|---|---|
| Lisinopril | 10 mg | Oral | Once daily | 2017-04-01 | Dr. Patel (PCP) |
| Atorvastatin | 20 mg | Oral | Once daily at bedtime | 2020-09-15 | Dr. Patel (PCP) |

> **Note:** Patient is currently on NO oral hypoglycemic agents. Metformin and Glipizide were both discontinued due to documented failures (see Medication History below).

---

## Medication History (Diabetes-Specific)

### Trial 1: Metformin

| Field | Detail |
|---|---|
| **Medication** | Metformin HCl |
| **Dosage** | 500 mg BID → titrated to 1000 mg BID |
| **Start Date** | July 1, 2019 |
| **End Date** | January 15, 2020 |
| **Duration** | 198 days (6.6 months) |
| **Prescriber** | Dr. Priya Sharma, MD (Endocrinology) |
| **Rationale for Initiation** | First-line therapy for newly diagnosed Type 2 DM per ADA Standards of Medical Care |
| **HbA1c at Start** | 9.1% (at diagnosis, June 2019) |
| **HbA1c After Trial** | 8.2% (January 10, 2020) — inadequate response |
| **Adverse Effects** | Persistent gastrointestinal side effects: nausea, diarrhea, abdominal cramping. Symptoms persisted despite slow titration and administration with meals. |
| **Reason for Discontinuation** | Inadequate glycemic control (HbA1c 8.2%, target <7.0%) AND intolerable GI side effects despite 6+ months of compliance |
| **Outcome** | **FAILURE — Documented inadequate control + adverse effects** |

### Trial 2: Glipizide (Sulfonylurea)

| Field | Detail |
|---|---|
| **Medication** | Glipizide (sulfonylurea class) |
| **Dosage** | 5 mg daily → titrated to 10 mg daily |
| **Start Date** | February 1, 2020 |
| **End Date** | August 10, 2020 |
| **Duration** | 191 days (6.4 months) |
| **Prescriber** | Dr. Priya Sharma, MD (Endocrinology) |
| **Rationale for Initiation** | Second-line therapy after documented Metformin failure |
| **HbA1c at Start of Trial** | 8.2% |
| **HbA1c After Trial** | 7.8% — marginal improvement but still above target |
| **Adverse Effects** | Recurrent hypoglycemic episodes (5 documented, see Hypoglycemia Log) |
| **Reason for Discontinuation** | Recurrent hypoglycemia including one severe episode requiring ER visit, with inadequate glycemic control (HbA1c 7.8%, target <7.0%) |
| **Outcome** | **FAILURE — Documented inadequate control + recurrent hypoglycemia** |

---

## Hypoglycemia Event Log

| Date | Time | Blood Glucose (mg/dL) | Symptoms | Intervention | Location |
|---|---|---|---|---|---|
| 2020-04-12 | 14:30 | 58 | Tremor, diaphoresis, confusion | Glucose tablets (15g), resolved in 20 min | Workplace |
| 2020-05-03 | 07:15 | 62 | Dizziness, sweating, palpitations | Orange juice + crackers | Home |
| 2020-06-18 | 02:40 | 54 | Nocturnal diaphoresis, awoken from sleep | Glucose gel, blood glucose rechecked at 89 mg/dL after 30 min | Home |
| 2020-07-01 | 17:00 | 65 | Lightheadedness, weakness | Glucose tablets post-exercise | Gym |
| 2020-07-29 | 11:20 | 51 | Near-syncope, severe diaphoresis, confusion, tremor | **ER visit** — IV dextrose, observed 4 hours, discharged stable | ER — Seton Medical Center |

> **Total documented events:** 5 episodes over 6 months, including 1 ER visit for severe hypoglycemia (BG 51 mg/dL with near-syncope).

---

## Laboratory Results

| Date | Test | Result | Reference Range | Context |
|---|---|---|---|---|
| 2019-06-15 | HbA1c | **9.1%** | <5.7% normal, 5.7–6.4% prediabetes, ≥6.5% diabetes | At diagnosis |
| 2019-06-15 | Fasting Glucose | 212 mg/dL | 70–100 mg/dL | At diagnosis |
| 2020-01-10 | HbA1c | **8.2%** | Target <7.0% | After 6 months Metformin — inadequate control |
| 2020-01-10 | Fasting Glucose | 178 mg/dL | 70–100 mg/dL | Persistent hyperglycemia |
| 2020-08-05 | HbA1c | **7.8%** | Target <7.0% | After 6 months Metformin + Glipizide — inadequate |
| 2020-08-05 | Fasting Glucose | 162 mg/dL | 70–100 mg/dL | Still elevated |
| 2024-01-15 | HbA1c | **8.3%** | Target <7.0% | Annual follow-up — worsening |
| 2024-07-20 | HbA1c | **8.5%** | Target <7.0% | Most recent — persistent hyperglycemia |
| 2024-07-20 | Fasting Glucose | 194 mg/dL | 70–100 mg/dL | Elevated |
| 2024-07-20 | Comprehensive Metabolic Panel | Within normal limits | — | Renal and hepatic function normal |
| 2024-07-20 | Lipid Panel | LDL 118, HDL 42, TG 188 | LDL <100, HDL >40, TG <150 | Dyslipidemia — on statin |

---

## Blood Glucose Self-Monitoring Log (3-Month Summary: May–July 2024)

| Month | Avg Fasting BG | Avg Post-Meal BG | Readings <70 mg/dL | Readings >250 mg/dL | Notes |
|---|---|---|---|---|---|
| May 2024 | 182 mg/dL | 234 mg/dL | 2 | 8 | Erratic patterns |
| June 2024 | 176 mg/dL | 241 mg/dL | 1 | 10 | Hyperglycemic excursions after meals |
| July 2024 | 188 mg/dL | 228 mg/dL | 3 | 7 | Both hypo and hyper events |

> **3-month log demonstrates:** Persistent glycemic instability with both hypoglycemic events (6 readings <70 mg/dL) and frequent hyperglycemic excursions (25 readings >250 mg/dL). Average fasting BG consistently above 170 mg/dL.

---

## Progress Notes

### Visit: August 15, 2024 — Endocrinology Follow-up

**Provider:** Dr. Priya Sharma, MD (Endocrinology)
**NPI:** 1234567890
**Practice:** Capital Endocrine Associates

**Chief Complaint:** Follow-up for Type 2 Diabetes, discussion of glucose monitoring options.

**History of Present Illness:**
Patient Maria Gonzalez is a 56-year-old female with Type 2 Diabetes Mellitus (E11.9) diagnosed in June 2019. She presents today for follow-up of her diabetes management. Patient has failed both first-line and second-line oral therapies over the past 4+ years:

1. **Metformin** — trialed for 198 days (July 2019 – January 2020). Discontinued due to persistent GI intolerance (nausea, diarrhea, cramping despite slow titration) and inadequate glycemic control (HbA1c decreased from 9.1% to 8.2% — still above 7.0% target).

2. **Glipizide (sulfonylurea)** — trialed for 191 days (February 2020 – August 2020). Discontinued due to recurrent hypoglycemic episodes (5 documented events including 1 ER visit for near-syncope with BG 51 mg/dL) and inadequate glycemic control (HbA1c 7.8% — still above target).

Patient has been without oral hypoglycemic therapy since August 2020 due to the documented failures and safety concerns. Current HbA1c is 8.5% (July 20, 2024), reflecting persistent hyperglycemia. Patient has maintained a 3-month blood glucose self-monitoring log (May–July 2024) demonstrating erratic glycemic patterns with both hypoglycemic and hyperglycemic excursions.

**Assessment:**
1. Type 2 Diabetes Mellitus without complications (E11.9) — poorly controlled
2. Documented failure of step therapy: Metformin (Step 1) and Glipizide/sulfonylurea (Step 2)
3. Current HbA1c 8.5% — significantly above ADA target of <7.0%
4. Glycemic instability documented over 3-month self-monitoring period

**Plan:**
1. Requesting authorization for **Continuous Glucose Monitoring (CPT 95251)** to enable real-time glucose trend tracking, pattern identification, and improved glycemic management.
2. CGM is medically necessary given:
   - Documented failure of both first-line (Metformin) and second-line (sulfonylurea) oral therapies
   - Ongoing glycemic instability with both hypo- and hyperglycemic events
   - Current HbA1c of 8.5% demonstrating persistent poor control
   - 3-month blood glucose log confirming erratic patterns
3. Prior authorization request submitted to AcmeCare under Policy ACME-CGM-2024-001.
4. Follow-up in 4 weeks to review authorization status and discuss CGM initiation.

**Electronically signed:** Dr. Priya Sharma, MD — August 15, 2024, 16:45 EST

---

### Visit: January 15, 2024 — Annual Diabetes Review

**Provider:** Dr. Priya Sharma, MD (Endocrinology)

**Brief Note:** Annual diabetes follow-up. HbA1c 8.3%, elevated from prior. Patient not on oral hypoglycemics due to prior documented failures. Discussed options including CGM, insulin, GLP-1 agonists. Patient expressed interest in CGM for real-time monitoring before considering injectable therapies. Ordered comprehensive metabolic panel and lipid panel. Continue current antihypertensive and statin. Return in 6 months.

---

### Visit: July 20, 2024 — Pre-Authorization Labs & Assessment

**Provider:** Dr. Priya Sharma, MD (Endocrinology)

**Brief Note:** Labs drawn in preparation for CGM authorization request. HbA1c 8.5% — worsening. Fasting glucose 194 mg/dL. Reviewed patient's 3-month blood glucose log: shows erratic patterns with avg fasting BG 180+ mg/dL, multiple hypo events (<70), and frequent post-meal spikes >250 mg/dL. Patient is highly motivated for CGM. CMP normal, lipid panel shows mild dyslipidemia on statin. Will compile authorization package for CGM request at next visit.

---

## Allergies

| Allergen | Reaction | Severity |
|---|---|---|
| Sulfonamides | Rash, urticaria | Moderate |
| No known drug allergies (NKDA) other than above | — | — |

---

## Immunization Record

| Vaccine | Date | Status |
|---|---|---|
| Influenza | 2023-10-15 | Current |
| COVID-19 (updated booster) | 2023-09-20 | Current |
| Tdap | 2019-06-15 | Current |

---

## Social History

- **Occupation:** Administrative assistant
- **Tobacco:** Never smoker
- **Alcohol:** Occasional social use (1–2 drinks/month)
- **Exercise:** Walks 20 minutes, 3x/week
- **Diet:** Follows general diabetic diet with guidance from nutritionist since 2019

---

## Family History

- **Father:** Type 2 Diabetes (diagnosed age 50), hypertension
- **Mother:** Hypertension, hyperlipidemia
- **Sibling (brother):** Type 2 Diabetes (diagnosed age 45)
