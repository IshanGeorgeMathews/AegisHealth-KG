# AegisHealth-KG — Test Cases and Retrieval Benchmark

## 1. Purpose

This document defines the test strategy for the Neo4j + Qdrant + hybrid retrieval subsystem.

The supplied `data/synthetic/answer_keys/` directory is the ground-truth evaluation source.

Production retrieval must never index answer keys.

---

## 2. Test Layers

```text
Unit
  ↓
Integration
  ↓
Scenario retrieval
  ↓
Requirement evaluation
  ↓
End-to-end evidence grounding
  ↓
Regression benchmark
```

---

## 3. Unit Tests

### U-001 — Stable document ID

Input:

```text
same source file
```

Expected:

```text
same document_id
same content_hash
```

unless source version intentionally changes.

### U-002 — Stable evidence ID

Same canonical chunk must produce the same:

```text
evidence_id
```

### U-003 — Chunk provenance

Every chunk must include:

```text
document_id
chunk_id
evidence_id
source_type
```

### U-004 — Requirement parsing

`REQ-*` identifiers must be preserved exactly.

### U-005 — Date parsing

Dates such as:

```text
2024-07-08
```

must become typed date values, not ambiguous strings during rule evaluation.

### U-006 — WRRF

Ranks:

```text
dense:  A B C
sparse: C A D
graph:  A C E
```

must produce A/C above documents appearing in only one weakly ranked list, subject to configured weights.

### U-007 — Deduplication

The same `evidence_id` returned by dense and sparse retrieval must appear once after fusion.

### U-008 — Missing evidence

If required evidence is absent, evaluator returns:

```text
INSUFFICIENT_EVIDENCE
```

not fabricated success/failure.

---

## 4. Neo4j Integration Tests

### N-001 — Patient lookup

```cypher
MATCH (p:Patient {patient_id: $patient_id})
RETURN p
```

Expected:

```text
SYN-PAT-001 → scenario 1
SYN-PAT-002 → scenario 2
SYN-PAT-003 → scenario 3
```

### N-002 — Scenario 2 claim chain

Expected traversable path:

```text
Patient
→ Claim
→ ClaimLine
→ Procedure
→ Denial
→ Policy
```

### N-003 — Policy requirements

Scenario 2 policy must return exactly:

```text
REQ-PRIOR-AUTH
REQ-PHYSIO-6WK
REQ-CLINICAL-EXAM
```

### N-004 — Scenario 1 policy

Return exactly:

```text
REQ-STEP-METFORMIN
REQ-STEP-SULFONYLUREA
REQ-HYPO-LOG
```

### N-005 — Scenario 3 policy

Return exactly:

```text
REQ-MH-BASELINE
REQ-MH-MEDICAL-NECESSITY
```

### N-006 — Evidence provenance

Every retrieved EvidenceChunk must have:

```text
document_id
source_type
```

and be traceable to a document.

---

## 5. Qdrant Integration Tests

### Q-001 — Collection exists

Expected:

```text
aegis_evidence
```

exists.

### Q-002 — Every point has an evidence ID

No indexed point may lack:

```text
evidence_id
```

### Q-003 — Patient filtering

A query filtered to:

```text
patient_id = SYN-PAT-002
```

must not return patient-specific chunks from scenarios 1 or 3.

### Q-004 — Policy filtering

A query filtered to:

```text
policy_id = ACME-MRI-2024-002
```

must not retrieve scenario 1 or 3 policy evidence.

### Q-005 — Exact code retrieval

Queries for:

```text
73721
M25.561
CO-197
```

should retrieve the corresponding scenario 2 evidence with lexical retrieval.

---

## 6. Scenario 1 Tests

### S1-Q1 — Requirement satisfaction

Query:

```text
Did the patient complete the required step therapy for CGM?
```

Expected:

```text
policy_id = ACME-CGM-2024-001

requirements:
REQ-STEP-METFORMIN
REQ-STEP-SULFONYLUREA
REQ-HYPO-LOG

missing = []
```

### S1-Q2 — Metformin evidence

Query:

```text
Was there a qualifying Metformin trial?
```

Required evidence:

```text
duration ≈ 198 days
inadequate control
GI adverse effects
failure/discontinuation
```

### S1-Q3 — Sulfonylurea evidence

Required:

```text
Glipizide
≈191 days
hypoglycemia
inadequate control
```

### S1-Q4 — Glucose log

Required:

```text
3 months
hypoglycemic events
hyperglycemic excursions
HbA1c evidence
```

### S1-Q5 — Grounding

Expected:

```text
no invented requirement
no invented evidence
all requirement IDs exactly match policy
```

---

## 7. Scenario 2 Tests

### S2-Q1 — Policy identification

Query:

```text
What policy applies to James's MRI claim?
```

Expected:

```text
ACME-MRI-2024-002
```

### S2-Q2 — Entity extraction

Expected:

```text
ICD-10 = M25.561
CPT = 73721
CARC = CO-197
```

### S2-Q3 — Requirement enumeration

Expected exactly three requirements:

```text
REQ-PRIOR-AUTH
REQ-PHYSIO-6WK
REQ-CLINICAL-EXAM
```

### S2-Q4 — Prior authorization

Expected:

```text
REQ-PRIOR-AUTH = NOT_SATISFIED
```

Reason must state that PA-200 was not submitted.

### S2-Q5 — PT requirement

Expected:

```text
REQ-PHYSIO-6WK = NOT_SATISFIED
```

Expected facts:

```text
actual duration ≈ 5.7 weeks
actual sessions = 5

required duration = 6 weeks / 42 days
required sessions = 6
```

Critical negative test:

```text
system must NOT claim that PT lasted 6 weeks
```

### S2-Q6 — Clinical examination

Expected:

```text
REQ-CLINICAL-EXAM = SATISFIED
```

Expected evidence:

```text
exam date = 2024-07-08
same day as MRI request
within 30 days
ROM
McMurray
stability
pain assessment
```

### S2-Q7 — Requirement count

Expected:

```text
total = 3
missing = 2
satisfied = 1
```

### S2-Q8 — Denial explanation

Expected:

```text
category = PRIOR_AUTH_MISSING
```

### S2-Q9 — Appeal evidence

Expected evidence classes:

```text
PA omission
PT duration/sessions
clinical exam
denial
policy
legal reference
```

---

## 8. Scenario 3 Tests

### S3-Q1 — Policy

Expected:

```text
ACME-MH-2024-003
```

### S3-Q2 — Requirements

Exactly:

```text
REQ-MH-BASELINE
REQ-MH-MEDICAL-NECESSITY
```

### S3-Q3 — Baseline requirement

Expected:

```text
active F33.1
in-network provider
```

### S3-Q4 — Medical necessity

Expected evidence:

```text
PHQ-9 latest score = 12
PHQ-9 >= 10
3 measurable treatment goals
progress notes
clinical rationale
```

### S3-Q5 — Result

Expected:

```text
REQ-MH-BASELINE = SATISFIED
REQ-MH-MEDICAL-NECESSITY = SATISFIED
missing = []
```

### S3-Q6 — PubMed retrieval

Query topics:

```text
CBT efficacy for recurrent MDD
optimal duration of psychotherapy for moderate depression
risk of relapse with premature therapy discontinuation
```

Expected:

```text
relevant PubMed-style synthetic abstracts are retrieved
```

Negative:

```text
system must not fabricate PMID/DOI/title/author
```

### S3-Q7 — MHPAEA

The system may retrieve and summarize the provided parity material.

Negative:

```text
must not say MHPAEA automatically guarantees eligibility
```

---

## 9. Cross-Scenario Isolation Tests

### ISO-001

Query:

```text
What evidence supports James's MRI claim?
```

Expected:

```text
no Maria-specific clinical evidence
no Aisha-specific psychotherapy evidence
```

### ISO-002

Filter:

```text
patient_id = SYN-PAT-001
```

Expected:

```text
only scenario 1 patient evidence
```

### ISO-003

Policy filter:

```text
policy_id = ACME-MH-2024-003
```

Expected:

```text
scenario 3 policy evidence only
```

---

## 10. Temporal Tests

### T-001

Claim date:

```text
2024-07-08
```

Policy effective range must include this date.

### T-002

A policy version outside the claim service date must not be selected as the active policy.

### T-003

Clinical exam window

Scenario 2:

```text
exam = 2024-07-08
MRI = 2024-07-08
```

Expected:

```text
within 30-day window
```

---

## 11. Retrieval Metric Tests

For each benchmark query, maintain:

```text
gold evidence IDs
```

Calculate:

```text
Recall@5
Recall@10
MRR@10
nDCG@10
Precision@5
```

### Required benchmark

Compare:

```text
Dense only
Dense + Sparse
Dense + Sparse + WRRF
Dense + Sparse + WRRF + Reranker
Full Hybrid + Graph Expansion
```

The final architecture should not be accepted based solely on subjective answer quality.

---

## 12. Regression Tests

Every code/model change must rerun:

```text
all unit tests
all integration tests
all scenario tests
all benchmark queries
```

Store previous metrics.

A regression is:

```text
material drop in Recall@10/MRR/nDCG
or
grounding failure
or
cross-patient leakage
or
new hallucinated evidence
```

---

## 13. Security/Privacy Tests

Even with synthetic data:

```text
T-SEC-001
logs must not include full document text

T-SEC-002
passwords must not appear in source code

T-SEC-003
Cypher must be parameterized

T-SEC-004
answer_keys are excluded from production indexing
```

---

## 14. Pass Criteria

A release candidate should satisfy:

```text
all critical unit tests pass
all integration tests pass
all 3 scenario requirement evaluations match answer keys
no cross-scenario leakage
no fabricated citations
all final evidence has provenance
retrieval benchmark meets quality thresholds in quality.md
```
