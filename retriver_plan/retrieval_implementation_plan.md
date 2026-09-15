# AegisHealth-KG — Retrieval Implementation Plan

## 1. Objective

Implement a deterministic, provenance-aware hybrid retrieval subsystem that can answer questions over:

- patient facts
- claims and denials
- insurance policies
- authorization requirements
- clinical records
- legal/reference material
- synthetic PubMed-style abstracts

The implementation must support both:

```text
case-centric retrieval
```

and:

```text
evidence-centric retrieval
```

without requiring the LLM to reconstruct the complete case from raw text.

---

## 2. Implementation Order

Do not implement all components simultaneously.

Use this order:

```text
Phase 0  Data audit
Phase 1  Domain contracts
Phase 2  Neo4j schema
Phase 3  Typed extraction
Phase 4  Qdrant + chunking
Phase 5  Dense retrieval
Phase 6  Sparse retrieval
Phase 7  Hybrid fusion
Phase 8  Reranking
Phase 9  Graph expansion
Phase 10 Requirement evaluation
Phase 11 Retrieval API
Phase 12 Benchmark + quality gates
Phase 13 Model experiments
```

---

## 3. Phase 0 — Data Audit

Confirm all source categories:

```text
answer_keys/
clinical_records/
code_references/
denial_letters/
eob/
legal_references/
patients/
policies/
prior_auth/
pubmed_articles/
```

Build an audit table with:

```text
file
document_id
source_type
scenario_id
patient_id
content_hash
version
synthetic/external status
```

Expected source groups from the supplied archive:

```text
3 answer keys
3 patient records
3 clinical records
3 EOBs
3 denial letters
3 policies
1 prior authorization guideline
1 legal reference document
1 CPT/HCPCS reference file
1 ICD-10 reference file
1 PubMed abstract collection
```

The three answer keys remain evaluation-only.

---

## 4. Phase 1 — Domain Contracts

Create:

```text
models/domain.py
models/evidence.py
models/retrieval.py
models/requirements.py
```

Minimum concepts:

```python
Patient
Claim
ClaimLine
Procedure
Diagnosis
Medication
LabResult
ClinicalEvent
TherapyEpisode
Denial
Policy
Requirement
LegalReference
EvidenceChunk
RetrievedEvidence
RequirementResult
RetrievalResult
```

All models should validate identifiers and dates.

---

## 5. Phase 2 — Neo4j Schema

### 5.1 Create constraints

At minimum:

```cypher
CREATE CONSTRAINT patient_id_unique IF NOT EXISTS
FOR (p:Patient)
REQUIRE p.patient_id IS UNIQUE;
```

```cypher
CREATE CONSTRAINT claim_id_unique IF NOT EXISTS
FOR (c:Claim)
REQUIRE c.claim_id IS UNIQUE;
```

```cypher
CREATE CONSTRAINT policy_id_unique IF NOT EXISTS
FOR (p:Policy)
REQUIRE p.policy_id IS UNIQUE;
```

```cypher
CREATE CONSTRAINT requirement_id_unique IF NOT EXISTS
FOR (r:Requirement)
REQUIRE r.requirement_id IS UNIQUE;
```

```cypher
CREATE CONSTRAINT evidence_id_unique IF NOT EXISTS
FOR (e:EvidenceChunk)
REQUIRE e.evidence_id IS UNIQUE;
```

Also create constraints for:

```text
document_id
procedure/CPT code
ICD-10 code
denial code
```

where the data model guarantees uniqueness.

### 5.2 Load shared knowledge first

Order:

```text
CPT/HCPCS
ICD-10
Requirements
Legal references
Policies
```

Then case data:

```text
Patients
Providers
Claims
Clinical events
Therapy episodes
Denials
Evidence
```

This makes reference IDs available when case relationships are created.

---

## 6. Phase 3 — Typed Extraction

Implement:

```text
JsonPatientParser
JsonEobParser
MarkdownClinicalParser
MarkdownPolicyParser
MarkdownPriorAuthParser
MarkdownLegalParser
PdfDenialParser
PubMedParser
ReferenceCodeParser
```

Each parser emits canonical structures and provenance.

No parser should directly write to Neo4j or Qdrant.

---

## 7. Phase 4 — Typed Chunking

### 7.1 Clinical

Preferred unit:

```text
event / section / episode
```

Examples:

```text
medication trial
hypoglycemia log
lab-result block
endocrinology assessment
therapy-session summary
PHQ-9 series
treatment plan
clinical examination
```

### 7.2 Policies

Preferred unit:

```text
one meaningful rule/requirement
```

Example IDs:

```text
POLICY-001::coverage
POLICY-001::REQ-STEP-METFORMIN
POLICY-002::REQ-PRIOR-AUTH
POLICY-002::REQ-PHYSIO-6WK
POLICY-003::REQ-MH-MEDICAL-NECESSITY
```

### 7.3 Denials

Preferred unit:

```text
decision
reason
supporting rationale
appeal instructions
```

### 7.4 Legal

Preferred unit:

```text
one statute/regulation/reference section
```

### 7.5 PubMed

Preferred unit:

```text
one article = title + abstract + keywords + metadata
```

unless an abstract is exceptionally long.

---

## 8. Phase 5 — Dense Retrieval

Start with a CPU-friendly baseline such as FastEmbed + a small BGE model.

Current baseline candidate:

```text
BAAI/bge-small-en-v1.5
```

Required experiment:

```text
query → embedding → Qdrant dense search
```

Store:

```text
embedding model name
embedding dimension
model revision/version
```

in collection metadata/config.

Do not silently switch embedding models after indexing. A model change requires re-indexing.

---

## 9. Phase 6 — Sparse Retrieval

Add sparse retrieval for:

```text
CPT
ICD-10
CARC/denial codes
policy IDs
requirement IDs
legal citations
drug names
exact clinical terms
```

Candidate implementation:

```text
Qdrant sparse vectors
```

with a BM25-compatible FastEmbed model where appropriate.

The sparse result set must be ranked independently from dense results.

---

## 10. Phase 7 — Metadata Filtering

Before semantic retrieval, construct filters from graph/query understanding.

Example:

```json
{
  "patient_id": "SYN-PAT-002",
  "policy_id": "ACME-MRI-2024-002"
}
```

For requirement search:

```json
{
  "requirement_id": "REQ-PHYSIO-6WK"
}
```

For PubMed:

```json
{
  "source_type": "pubmed",
  "scenario_id": 3
}
```

Avoid searching the entire corpus when a reliable anchor is available.

---

## 11. Phase 8 — Fusion

Implement a standalone fusion module.

Input:

```python
dense_results
sparse_results
graph_results
```

Output:

```python
list[FusedCandidate]
```

Use Reciprocal Rank Fusion or Weighted Reciprocal Rank Fusion.

Example:

```python
def wrf(rank: int, weight: float, k: int = 60) -> float:
    return weight / (k + rank)
```

Initial experiment:

```text
dense  = 1.0
sparse = 0.9
graph  = 1.2
```

Do not consider these final values.

Tune them against answer-key retrieval performance.

Deduplicate by:

```text
evidence_id
```

not by text alone.

---

## 12. Phase 9 — Reranking

Input:

```text
query
+
20–50 fused candidates
```

Output:

```text
top 5–10
```

Initial candidate:

```text
BAAI/bge-reranker-v2-m3
```

Benchmark against alternatives later.

The reranker must receive the original user query, not an over-processed version that loses the user's intent.

Keep:

```text
first_stage_rank
fusion_score
reranker_score
final_rank
```

for observability.

---

## 13. Phase 10 — Graph Expansion

For final evidence IDs:

```text
Qdrant
  ↓
evidence_id
  ↓
Neo4j
  ↓
related Requirement / Policy / Patient / Claim / ClinicalEvent
```

Expansion should have controlled depth.

Recommended initial expansion:

```text
Evidence
→ 1-hop supporting entity
→ 1-hop parent policy/case
```

Only expand deeper when query intent requires it.

Avoid arbitrary graph walks.

---

## 14. Phase 11 — Query Planner

Implement an explicit planner.

Input:

```text
raw query
patient_id
claim_id
optional known entities
```

Output:

```python
class RetrievalPlan:
    intent: str
    patient_id: str | None
    claim_id: str | None
    policy_id: str | None
    requirement_ids: list[str]
    cpt_codes: list[str]
    icd10_codes: list[str]
    denial_codes: list[str]
    source_types: list[str]
    use_graph: bool
    use_dense: bool
    use_sparse: bool
    use_reranker: bool
```

Keep the planner deterministic where possible.

LLM assistance may be added later for intent/entity extraction, but the output must pass schema validation.

---

## 15. Phase 12 — Deterministic Requirement Evaluator

Implement:

```text
requirements/evaluator.py
```

or keep this under `retrieval/` until the domain grows.

Input:

```text
Requirement
+
Structured patient/claim facts
```

Output:

```json
{
  "requirement_id": "REQ-PHYSIO-6WK",
  "status": "NOT_SATISFIED",
  "required": {
    "duration_days": 42,
    "sessions": 6
  },
  "actual": {
    "duration_days": 39,
    "sessions": 5
  },
  "evidence_ids": ["EV-S2-PT-001"],
  "reason": "Both minimum duration and session count are below policy requirements."
}
```

The evaluator must never invent missing facts.

Possible statuses:

```text
SATISFIED
NOT_SATISFIED
INSUFFICIENT_EVIDENCE
NOT_APPLICABLE
```

Do not collapse `INSUFFICIENT_EVIDENCE` into failure.

---

## 16. Scenario-Specific Retrieval Plans

### Scenario 1 — CGM / Step Therapy

Question:

```text
Was step therapy actually completed?
```

Retrieval:

```text
patient
→ diabetes diagnosis
→ medication trials
→ lab results
→ hypoglycemia events
→ CGM policy
→ 3 requirements
```

Qdrant:

```text
metformin trial
glipizide trial
glucose log
current HbA1c
clinical rationale
policy requirements
```

Expected evaluation:

```text
REQ-STEP-METFORMIN = SATISFIED
REQ-STEP-SULFONYLUREA = SATISFIED
REQ-HYPO-LOG = SATISFIED
```

### Scenario 2 — MRI / Prior Authorization

Question:

```text
Why was the MRI denied?
```

Retrieval:

```text
Patient
→ claim
→ CPT 73721
→ M25.561
→ CO-197
→ ACME-MRI-2024-002
→ requirements
```

Required evidence:

```text
PA-200 submission status
PT duration
PT session count
clinical examination
denial reason
policy
legal reference
```

Expected evaluation:

```text
REQ-PRIOR-AUTH = NOT_SATISFIED
REQ-PHYSIO-6WK = NOT_SATISFIED
REQ-CLINICAL-EXAM = SATISFIED
```

### Scenario 3 — Psychotherapy / Medical Necessity

Question:

```text
Does the patient satisfy session-21 medical-necessity requirements?
```

Retrieval:

```text
Patient
→ F33.1
→ provider
→ policy
→ requirements
→ sessions 1–20
→ PHQ-9
→ treatment plan
→ progress
→ clinical rationale
```

Additional vector retrieval:

```text
PubMed:
CBT efficacy
psychotherapy duration
relapse/discontinuation
```

Expected evaluation:

```text
REQ-MH-BASELINE = SATISFIED
REQ-MH-MEDICAL-NECESSITY = SATISFIED
```

---

## 17. Exact Search Fast Path

The system should bypass expensive semantic retrieval for trivial exact queries.

Examples:

```text
"What is CO-197?"
"What is CPT 73721?"
"What requirement is REQ-PHYSIO-6WK?"
```

Pipeline:

```text
query normalization
→ exact code lookup
→ structured response
```

No reranker required.

---

## 18. Full Appeal Deep Path

```text
Query
 ↓
Planner
 ↓
Case lookup
 ↓
Policy lookup
 ↓
Requirements
 ↓
Structured evaluation
 ↓
Qdrant dense + sparse
 ↓
Fusion
 ↓
Reranker
 ↓
Graph expansion
 ↓
Evidence pack
 ↓
LangGraph
```

This should be the highest-cost retrieval mode.

---

## 19. Provenance Rules

Every final evidence item must expose:

```text
evidence_id
document_id
chunk_id
source_type
source_status
section
page if available
```

For every evaluated requirement:

```text
requirement_id
actual facts
policy rule
evidence IDs
```

If an evidence item cannot be traced to a source, it must not be presented as grounded evidence.

---

## 20. Idempotent Indexing

For each document compute:

```text
content_hash = SHA-256(raw canonical content)
```

Persist:

```text
document_id
document_version
content_hash
indexed_at
```

Behavior:

```text
same hash
→ skip

new hash
→ create new version
→ delete/replace affected chunks
```

No duplicate evidence IDs.

---

## 21. Qdrant Indexing Sequence

```text
create collection
 ↓
create payload indexes
 ↓
embed chunks
 ↓
build payload
 ↓
upsert points
 ↓
validate count
 ↓
sample search
 ↓
run benchmark
```

Do not declare indexing successful solely because `upsert()` returned without error.

---

## 22. Neo4j Validation Sequence

After ingestion:

```text
count patients
count claims
count policies
count requirements
count evidence
```

Then verify:

```text
patient → claim
claim → denial
claim → policy
policy → requirement
clinical event → evidence
requirement → evidence
```

Run scenario-level consistency queries.

---

## 23. Initial Parameters

Treat these as configurable defaults:

```text
dense_top_k = 20
sparse_top_k = 20
fusion_candidate_limit = 50
rerank_top_k = 10
graph_expansion_depth = 1 or controlled 2
rrf_k = 60

chunk_target_tokens ≈ 300–700
chunk_hard_limit ≈ 900
```

These are starting points, not quality guarantees.

---

## 24. Model Evaluation Roadmap

Benchmark:

```text
A: BGE-small dense
B: BGE-small dense + sparse
C: dense + sparse + WRRF
D: C + reranker
E: D + graph expansion
```

Then optionally:

```text
F: BGE-M3
G: Qwen3-Embedding-0.6B
H: MedCPT for PubMed subset
I: late-interaction / multivector
```

Keep architecture fixed while changing the model when benchmarking model quality.

---

## 25. Implementation Completion Gate

Do not proceed to agent integration until:

```text
[ ] Scenario 1 retrieval passes benchmark
[ ] Scenario 2 retrieval passes benchmark
[ ] Scenario 3 retrieval passes benchmark
[ ] requirement evaluator matches answer keys
[ ] provenance exists for every final evidence item
[ ] exact identifiers are reliably retrievable
[ ] dense+sparse hybrid outperforms the dense-only baseline or a justified exception is documented
[ ] reranking impact is measured
[ ] graph expansion impact is measured
```
