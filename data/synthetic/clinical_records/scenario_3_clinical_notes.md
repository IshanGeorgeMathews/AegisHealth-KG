# Patient Clinical Records — Aisha Williams (Scenario 3)
# AegisHealth-KG Synthetic EHR Data

---

## Patient Demographics

| Field | Value |
|---|---|
| **Name** | Aisha Williams |
| **Date of Birth** | March 8, 1990 (Age 34) |
| **Gender** | Female |
| **MRN** | MRN-2022-78956 |
| **Insurance Member ID** | ACM-5567123-03 |

---

## Problem List (Active)

| # | Diagnosis | ICD-10 | Date Onset | Status |
|---|---|---|---|---|
| 1 | Major Depressive Disorder, recurrent episode, moderate | F33.1 | 2022-09-15 | Active |
| 2 | Generalized Anxiety Disorder | F41.1 | 2022-09-15 | Active, secondary |
| 3 | Insomnia, unspecified | G47.00 | 2023-01-10 | Active, improving |

---

## Medication List (Current as of 2024-09-10)

| Medication | Dosage | Route | Frequency | Start Date | Prescriber |
|---|---|---|---|---|---|
| Sertraline (Zoloft) | 100 mg | Oral | Once daily | 2023-01-15 | Dr. Rebecca Liu |
| Melatonin | 3 mg | Oral | Once at bedtime (PRN) | 2023-02-01 | Dr. Rebecca Liu |

---

## Psychiatric History

### Initial Psychiatric Evaluation — September 15, 2022

**Provider:** Dr. Rebecca Liu, MD (Psychiatry)
**NPI:** 5551234567
**Practice:** Manhattan Behavioral Health Associates

**Presenting Concerns:**
- Persistent depressed mood for >3 months
- Loss of interest in previously enjoyed activities (anhedonia)
- Difficulty concentrating at work leading to underperformance
- Social withdrawal from friends and family
- Insomnia — difficulty falling asleep and early morning awakening
- Fatigue and low energy throughout the day
- Feelings of worthlessness and excessive guilt
- No suicidal ideation, no self-harm behaviors

**Psychiatric History:**
- First depressive episode at age 24 (2014), treated with 6 months of therapy, resolved
- Second depressive episode at age 28 (2018), treated with 4 months of therapy + Fluoxetine 20 mg for 1 year, resolved
- Current episode (third) began approximately June 2022, worsening over 3 months

**Assessment:**
- **Diagnosis:** Major Depressive Disorder, recurrent episode, moderate (F33.1)
- **Comorbid:** Generalized Anxiety Disorder (F41.1)
- **PHQ-9 Score:** 17 (moderately severe)
- **GAD-7 Score:** 12 (moderate anxiety)
- **Columbia Suicide Severity Rating Scale:** No current suicidal ideation

**Plan:**
- Individual cognitive-behavioral therapy (CBT), weekly sessions
- Consider pharmacotherapy if insufficient response to therapy alone after 8 weeks
- Follow-up PHQ-9 assessment in 4 weeks

---

## PHQ-9 Serial Assessments

| Date | Score | Severity | Context | Change from Baseline |
|---|---|---|---|---|
| 2022-09-15 | 17 | Moderately severe | Initial evaluation | — |
| 2022-11-15 | 15 | Moderately severe | After 8 weeks CBT | -2 (minimal) |
| 2023-01-09 | 18 | Moderately severe | Start of calendar year 2024 sessions — holiday relapse | +1 (worsened) |
| 2023-03-15 | 14 | Moderate | After adding Sertraline 50 mg | -4 |
| 2024-01-09 | 18 | Moderately severe | **CY2024 Baseline** — seasonal exacerbation | Reset baseline |
| 2024-04-16 | 14 | Moderate | After 3 months weekly CBT (2024) | -4 |
| 2024-06-25 | 13 | Moderate | After 5 months — steady decline | -5 |
| 2024-08-27 | **12** | **Moderate** | After 8 months — approaching mild threshold | **-6** |

> **Trajectory:** Consistent downward trend from 18 → 12 over 8 months of CBT in 2024. Score of 12 remains in the "moderate" range (10–14). Patient has NOT yet reached the treatment goal of PHQ-9 < 10 (mild range).

---

## GAD-7 Serial Assessments

| Date | Score | Severity | Context |
|---|---|---|---|
| 2022-09-15 | 12 | Moderate | Initial evaluation |
| 2024-01-09 | 10 | Moderate | CY2024 baseline |
| 2024-08-27 | 7 | Mild | Improvement with CBT — anxiety responding well |

---

## Therapy Session Log (Calendar Year 2024)

| Session # | Date | Duration | Type | Key Themes | PHQ-9 |
|---|---|---|---|---|---|
| 1 | 2024-01-09 | 60 min | CBT — individual | Baseline assessment, goal setting, seasonal mood exacerbation | 18 |
| 2 | 2024-01-16 | 55 min | CBT — individual | Cognitive distortion identification, thought records initiated | — |
| 3 | 2024-01-23 | 58 min | CBT — individual | Behavioral activation — scheduling pleasant activities | — |
| 4 | 2024-01-30 | 60 min | CBT — individual | Sleep hygiene, addressing insomnia-depression cycle | — |
| 5 | 2024-02-06 | 55 min | CBT — individual | Cognitive restructuring — core beliefs about worthlessness | — |
| 6 | 2024-02-20 | 60 min | CBT — individual | Behavioral experiments — workplace performance anxiety | — |
| 7 | 2024-03-05 | 55 min | CBT — individual | Relationship patterns, interpersonal effectiveness | — |
| 8 | 2024-03-19 | 60 min | CBT — individual | Intermediate beliefs, reviewing thought record progress | — |
| 9 | 2024-04-02 | 55 min | CBT — individual | Relapse prevention concepts introduced early | — |
| 10 | 2024-04-16 | 60 min | CBT — individual | Mid-treatment assessment | 14 |
| 11 | 2024-04-30 | 55 min | CBT — individual | Return-to-work planning, occupational functioning | — |
| 12 | 2024-05-14 | 60 min | CBT — individual | Coping skills for workplace stress, assertiveness training | — |
| 13 | 2024-05-28 | 55 min | CBT — individual | Processing transition to part-time work (started June) | — |
| 14 | 2024-06-11 | 60 min | CBT — individual | Adjustment to part-time work, social reengagement | — |
| 15 | 2024-06-25 | 55 min | CBT — individual | Interim assessment | 13 |
| 16 | 2024-07-09 | 60 min | CBT — individual | Advanced cognitive restructuring, schema work | — |
| 17 | 2024-07-23 | 55 min | CBT — individual | Stress inoculation for anticipated full-time return | — |
| 18 | 2024-08-06 | 60 min | CBT — individual | Consolidation of CBT skills, independent practice review | — |
| 19 | 2024-08-20 | 55 min | CBT — individual | Skills generalization, relapse signature identification | — |
| 20 | 2024-08-27 | 60 min | CBT — individual | **End of standard authorization.** Assessment + continuation planning | 12 |
| **21** | **2024-09-10** | **60 min** | **CBT — individual** | **Session 21 — DENIED by AcmeCare.** Treatment extension request submitted. | — |

---

## Treatment Plan (Updated August 27, 2024)

**Provider:** Dr. Rebecca Liu, MD
**Date:** August 27, 2024

### Treatment Goals

| # | Goal | Metric | Status | Target Date |
|---|---|---|---|---|
| 1 | Achieve remission (PHQ-9 < 10) | PHQ-9 score | **In progress** — decreased from 18 to 12, not yet < 10 | December 31, 2024 |
| 2 | Return to full-time employment | Occupational functioning | **In progress** — returned to part-time June 2024 | March 1, 2025 |
| 3 | Develop independent coping strategies | Consistent use of CBT techniques without therapist support | **In progress** — improved but inconsistent under stress | June 1, 2025 |

### Clinical Rationale for Continuation (Sessions 21–32)

Patient Aisha Williams has demonstrated consistent, measurable improvement across 20 sessions of individual CBT in calendar year 2024. PHQ-9 scores have decreased from 18 (moderately severe) to 12 (moderate), representing a 33% reduction in symptom severity. However, she has **not yet achieved the treatment goal of PHQ-9 < 10** (mild range) and continues to meet full diagnostic criteria for Major Depressive Disorder, recurrent, moderate (F33.1).

**Evidence supporting continuation:**
1. **Measurable but incomplete response:** The consistent downward PHQ-9 trajectory (18 → 14 → 13 → 12) indicates active treatment response, but the patient has not yet achieved the minimally adequate response threshold of 50% reduction (target: 9 or below from baseline of 18).
2. **Recurrent episode pattern:** This is the patient's third depressive episode (F33.1 — recurrent). Research consistently demonstrates that patients with recurrent MDD have higher relapse rates and benefit from extended treatment courses to consolidate gains and develop durable coping strategies.
3. **Functional goals not yet met:** Patient returned to part-time work in June 2024 but has not yet achieved the goal of full-time employment. Premature termination could jeopardize functional gains.
4. **CBT skill consolidation:** Evidence-based CBT protocols for depression typically recommend 16–20 sessions for acute phase treatment plus 8–12 sessions for consolidation/relapse prevention. Patient is at the transition from acute to consolidation phase.
5. **Risk of regression:** Abrupt discontinuation at session 20 — when the patient is still symptomatic (PHQ-9 = 12) and in the process of consolidating skills — carries significant risk of symptom regression, particularly given the recurrent episode pattern.

**Requested:** Authorization for sessions 21–32 (12 additional sessions, biweekly) to complete consolidation phase of CBT and achieve treatment goals.

---

## Progress Note — Session 21 (Treatment Extension Request)

**Date:** September 10, 2024
**Provider:** Dr. Rebecca Liu, MD (Psychiatry)
**Type:** Treatment Extension Request / Session 21

**Note:**
Patient Aisha Williams, 34-year-old female with recurrent Major Depressive Disorder, moderate (F33.1), presents for session 21 of individual CBT. Patient has completed 20 sessions in CY2024 (January 9 – August 27). This session exceeds the standard 20-session annual authorization under AcmeCare Policy ACME-MH-2024-003.

**Clinical Update:**
- Patient reports continued mood improvement but notes increased stress related to upcoming full-time work transition planned for October 2024
- Sleep has improved (6.5 hours/night, up from 4–5 hours at baseline)
- Appetite and energy levels improved but not fully restored
- Patient applying CBT techniques (thought records, behavioral activation) with moderate consistency — breaks down under high stress
- No suicidal ideation, no self-harm

**Medical Necessity Justification Submitted:**
The following documentation was submitted to AcmeCare on September 10, 2024:
1. PHQ-9 serial scores (3 assessments: 18 → 14 → 12)
2. Treatment plan with 3 measurable goals and target dates
3. Progress notes summary for sessions 1–20
4. Clinical rationale for continuation (see Treatment Plan above)

**Signed:** Dr. Rebecca Liu, MD — September 10, 2024, 17:15 EST

---

## Allergies

| Allergen | Reaction | Severity |
|---|---|---|
| Fluoxetine (Prozac) | Serotonin syndrome symptoms (agitation, tremor, tachycardia) at 40 mg | Moderate — drug switched to Sertraline |
| No other known drug allergies | — | — |

---

## Immunization Record

| Vaccine | Date | Status |
|---|---|---|
| Influenza | 2023-11-01 | Current |
| COVID-19 (updated booster) | 2023-10-15 | Current |
| Tdap | 2020-09-10 | Current |
| HPV series | Completed 2012 | Complete |

---

## Social History

- **Occupation:** Graphic designer — part-time since June 2024 (previously full-time, reduced hours due to depression-related functional impairment)
- **Living situation:** Lives alone in a studio apartment in Harlem, NYC
- **Tobacco:** Never smoker
- **Alcohol:** Rare — 1–2 drinks/month (reduced from prior social drinking)
- **Substance use:** Denies illicit drug use
- **Support system:** Close friend group (3–4 friends, social contact improving), parents live in Brooklyn (supportive but not locally involved in care)
- **Exercise:** Walking 15–20 minutes daily (restarted in April 2024 as behavioral activation intervention)

---

## Family History

- **Mother:** History of depression (treated with medication, stable)
- **Father:** No psychiatric history; hypertension
- **Maternal grandmother:** Depression, possible bipolar disorder (untreated, per family report)
- **No family history of:** completed suicide, schizophrenia, substance use disorders
