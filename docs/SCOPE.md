# AegisHealth-KG — Prototype Scope Definition

## Project One-Liner

> A working proof-of-concept demonstrating hybrid Graph-RAG reasoning for insurance claim appeals across three representative clinical scenarios, using synthetic data only.

---

## Prototype Scope Boundaries

| Dimension | Bounded To |
|---|---|
| Procedures | 3 (CGM, MRI, Outpatient Therapy) |
| Diagnoses | 3 ICD-10 codes (E11.9, M25.561, F33.1) |
| Insurance Policies | 3 mock policies (one per scenario) |
| Denial Types | 3 CARC codes + 3 mock denial categories |
| Patient Records | 100% synthetic — zero real PHI |
| Payer APIs | Mock endpoints only (no live insurer connections) |

---

## CARC Code + Mock Denial Category Architecture

Real CARC (Claim Adjustment Reason Code) codes are standardized industry codes that describe
*why a payer adjusted a claim*. They do **not** encode the full policy logic behind the denial.

Our system pairs each CARC code with an explicit **mock denial category** that our policy
graph defines. The CARC tells us *what happened*; the mock category tells us *what policy
rule to reason about*.

```
Denial Letter
      │
      ├── CARC code (industry standard input signal)
      │
      └── Mock Denial Category (system routing label)
                         │
                         ↓
              Mock Policy Document (authoritative source of truth)
                         │
                         ↓
              Knowledge Graph Policy Rules
```

| CARC Code | Standard CARC Description | Mock Denial Category | Reasoning Pathway |
|---|---|---|---|
| `CO-167` | Diagnosis(es) is (are) not covered by this payer/contractor | `STEP_THERAPY_NOT_SATISFIED` | Graph: multi-hop prerequisite check |
| `CO-197` | Precertification/authorization/notification absent | `PRIOR_AUTH_MISSING` | Graph: documentation requirement check |
| `CO-50` | Non-covered services; not deemed a "medical necessity" | `MEDICAL_NECESSITY_NOT_ESTABLISHED` | Graph + Vector: policy evaluation + PubMed evidence + legal retrieval |

---

## The Three Scenarios

### Scenario 1 — Type 2 Diabetes → Continuous Glucose Monitoring (CGM)

| Element | Value |
|---|---|
| Diagnosis | `E11.9` — Type 2 Diabetes Mellitus without complications |
| Procedure | `CPT-95251` — Continuous Glucose Monitoring |
| CARC Code | `CO-167` |
| Mock Denial Category | `STEP_THERAPY_NOT_SATISFIED` |
| Mock Policy Rule | Patient must document failure of Metformin AND a sulfonylurea before CGM is approved |
| Tests | Multi-hop graph traversal — check 2 prerequisite drug failures |

### Scenario 2 — Knee Pain → MRI

| Element | Value |
|---|---|
| Diagnosis | `M25.561` — Pain in right knee |
| Procedure | `CPT-73721` — MRI of lower extremity joint |
| CARC Code | `CO-197` |
| Mock Denial Category | `PRIOR_AUTH_MISSING` |
| Mock Policy Rule | Requires 6 weeks of documented conservative physical therapy before imaging approval |
| Tests | Missing documentation path — graph-only retrieval |

### Scenario 3 — Major Depressive Disorder → Outpatient Therapy

| Element | Value |
|---|---|
| Diagnosis | `F33.1` — Major Depressive Disorder, recurrent, moderate |
| Procedure | `CPT-90837` — Psychotherapy, 60 minutes |
| CARC Code | `CO-50` |
| Mock Denial Category | `MEDICAL_NECESSITY_NOT_ESTABLISHED` |
| Mock Policy Rule | 20 sessions/year authorized without additional clinical review. Session 21+ requires documented medical necessity justification |
| Mock Denial Trigger | Session 21 denied under the session limit |
| Appeal Analysis | Evaluate whether the denial/application of the session limitation is consistent with the mock policy and applicable parity rules (MHPAEA) |
| Tests | Medical necessity + legal retrieval path — PubMed evidence + legal material |

---

## Synthetic Data Policy

**No real patient data (PHI) will be used at any point.** All patient records, clinical notes,
and denial letters are fabricated for demonstration purposes. Using synthetic data ensures
that the prototype does not process real PHI, avoiding the need to implement production
HIPAA safeguards for this academic prototype.

---

## Success Criteria

The prototype is "working" when, for each of the 3 scenarios, the following
input→output chain produces correct results:

```
Input: Synthetic denial letter (PDF)
   ↓
System processing
   ↓
Expected: Correct extraction, correct reasoning, grounded output
```

| Component | Metric | Pass Condition |
|---|---|---|
| ICD-10 Extraction | Extracted codes match denial letter | All expected codes extracted, no spurious codes |
| CPT Extraction | Extracted codes match denial letter | All expected codes extracted, no spurious codes |
| Denial Code Extraction | CARC code + mock category correctly identified | Exact match to synthetic denial |
| Graph Reasoning | Missing criteria / policy violations identified | All expected requirements identified — no invented requirements |
| Vector Retrieval | PubMed evidence relevance (Scenario 3) | Relevant evidence appears in Top-K results |
| Appeal Letter | Required sections present | Admin headers, clinical rebuttal, legal citations, bibliography |
| Citation Accuracy | All citations traceable to source data | Every citation must exist in the supplied source data |
| FHIR Payload | Schema validation | Passes FHIR R4 schema validation |

### Grounded Generation Requirement

**The system must not invent missing criteria, policy rules, medical evidence, or legal citations.**

| Source Data Says | System Must NOT Produce |
|---|---|
| Policy requires 6 weeks physical therapy | "12 weeks physical therapy" |
| PubMed abstract does not mention the treatment | LLM claims the abstract supports the treatment |
| Mock policy has 3 requirements | System reports 4 or 5 requirements |
| MHPAEA is retrieved as relevant legal material | System claims MHPAEA "guarantees" eligibility |

---

## Explicitly Out of Scope

- Real insurance payer API connections
- Real patient data / HIPAA compliance infrastructure
- Full ICD-10/CPT code coverage (~70,000 ICD-10 codes exist)
- Multi-language support
- User authentication / multi-tenancy
- Production deployment / scaling

---

## Synthetic Data File Structure

```
data/synthetic/
├── denial_letters/
│   ├── scenario_1_denial.pdf
│   ├── scenario_2_denial.pdf
│   └── scenario_3_denial.pdf
├── policies/
│   ├── scenario_1_policy.md
│   ├── scenario_2_policy.md
│   └── scenario_3_policy.md
├── patients/
│   ├── scenario_1_patient.json
│   ├── scenario_2_patient.json
│   └── scenario_3_patient.json
└── answer_keys/
    ├── scenario_1_expected.json
    ├── scenario_2_expected.json
    └── scenario_3_expected.json
```
