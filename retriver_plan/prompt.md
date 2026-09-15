# AegisHealth-KG Retrieval System — Master Implementation Prompt

You are implementing the **Neo4j Knowledge Graph + Qdrant Hybrid Retrieval subsystem** for the AegisHealth-KG project.

This is a college project using a synthetic healthcare/insurance dataset, but the implementation must be designed with **production-grade engineering principles** wherever practical.

The repository already contains the following documents under:

```text
/retriever_plan/
```

These documents are the authoritative project specification:

```text
architecture_plan.md
retrieval_implementation_plan.md
structure.md
test_case.md
quality.md
```

## 1. SOURCE OF TRUTH

Read all five documents before making implementation decisions.

Treat them in this order of authority:

```text
architecture_plan.md
        ↓
retrieval_implementation_plan.md
        ↓
structure.md
        ↓
test_case.md
        ↓
quality.md
```

Do not introduce an architectural decision that contradicts these documents without first identifying the conflict and explaining why the change is necessary.

Do not replace the planned architecture with a generic LangChain/LlamaIndex/GraphRAG implementation simply because such abstractions exist.

The implementation must remain understandable, testable, inspectable, and maintainable by a college project team.

---

# 2. PRIMARY OBJECTIVE

Build a provenance-aware hybrid retrieval subsystem with this architecture:

```text
                        USER QUERY
                            │
                            ▼
                     Query Planner
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
       Exact Lookup     Neo4j Graph      Qdrant
                        Retrieval         Retrieval
                                            │
                                      ┌─────┴─────┐
                                      ▼           ▼
                                    Dense       Sparse
                                      │           │
                                      └─────┬─────┘
                                            ▼
                                      Candidate Fusion
                                            │
                                            ▼
                                       Reranking
                                            │
                                            ▼
                                    Graph Expansion
                                            │
                                            ▼
                                Requirement Evaluation
                                            │
                                            ▼
                                      Evidence Pack
                                            │
                                            ▼
                                         LangGraph
                                            │
                                            ▼
                                            LLM
```

The system must distinguish between:

```text
Structured facts
Semantic evidence
Exact identifiers
Graph relationships
Deterministic rules
LLM-generated explanations
```

The LLM must not be treated as the source of truth for basic facts or deterministic requirement evaluation.

---

# 3. YOUR ROLE

You are acting as a senior backend/retrieval engineer.

You are responsible for:

```text
Neo4j schema and ingestion
Qdrant schema and ingestion
Document chunking
Embeddings
Sparse retrieval
Hybrid search
Graph retrieval
Graph expansion
Rank fusion
Reranking
Requirement evaluation
Provenance
Retrieval evaluation
Testing
Performance measurement
```

The implementation must fit into the existing AegisHealth-KG Python/FastAPI project.

Do not reorganize unrelated parts of the repository unless required for integration.

---

# 4. EXISTING PROJECT CONTEXT

The project already has a Python/FastAPI foundation using:

```text
pyproject.toml
.venv/
src/aegis/
```

Existing package areas include:

```text
api/
agent/
appeal/
config/
extraction/
fhir/
graph/
models/
retrieval/
vector/
```

Do not create a second application architecture.

Extend the existing structure according to:

```text
/retriever_plan/structure.md
```

---

# 5. DATASET CONTEXT

The supplied synthetic dataset contains three main healthcare scenarios plus shared reference material.

The corpus includes:

```text
patients
clinical records
EOBs
denial letters
insurance policies
prior authorization requirements
legal references
CPT/HCPCS reference data
ICD-10 reference data
PubMed-style articles
answer keys
```

The answer keys are evaluation data.

IMPORTANT:

```text
answer_keys/
```

must NEVER be indexed into Neo4j/Qdrant as production retrieval evidence.

They are used only to construct the retrieval benchmark and regression tests.

---

# 6. DATA REPRESENTATION RULE

Do not treat every file identically.

Use the following representation strategy:

```text
Patient JSON
→ Neo4j primarily

EOB JSON
→ Neo4j primarily
→ narrative fields may also become Qdrant evidence

Clinical records
→ Qdrant primarily
→ extracted entities/events into Neo4j

Insurance policies
→ Qdrant primarily
→ requirements/policy/entities into Neo4j

Denial letters
→ Qdrant primarily
→ denial facts into Neo4j

Prior authorization requirements
→ Qdrant evidence
→ canonical Requirement nodes in Neo4j

Legal references
→ Qdrant primarily
→ LegalReference nodes in Neo4j

CPT/HCPCS and ICD-10 references
→ structured lookup / Neo4j

PubMed-style abstracts
→ Qdrant primarily
→ optional article metadata in Neo4j

Answer keys
→ evaluation only
```

Do not embed every scalar field simply because it exists.

Identifiers and structured facts should remain structured.

---

# 7. NEO4J DOMAIN MODEL

Use these core node labels where applicable:

```text
Patient
Provider
Payer
InsurancePlan

Claim
ClaimLine
Denial
DenialCode

Procedure
CPTCode

Diagnosis
ICD10Code
Medication
LabResult

ClinicalEvent
TherapyEpisode

Policy
Requirement
LegalReference

Document
EvidenceChunk
PubMedArticle
```

Core relationships:

```text
Patient
  -[:HAS_CLAIM]-> Claim
  -[:HAS_DIAGNOSIS]-> Diagnosis
  -[:TAKES]-> Medication
  -[:HAS_LAB_RESULT]-> LabResult
  -[:HAS_CLINICAL_EVENT]-> ClinicalEvent
  -[:UNDERWENT]-> TherapyEpisode
  -[:TREATED_BY]-> Provider
  -[:COVERED_BY]-> InsurancePlan

Claim
  -[:HAS_LINE]-> ClaimLine
  -[:HAS_DENIAL]-> Denial
  -[:HAS_POLICY]-> Policy

ClaimLine
  -[:FOR_PROCEDURE]-> Procedure
  -[:HAS_DIAGNOSIS]-> Diagnosis

Procedure
  -[:HAS_CPT_CODE]-> CPTCode

Diagnosis
  -[:HAS_ICD10_CODE]-> ICD10Code

Denial
  -[:HAS_DENIAL_CODE]-> DenialCode

Policy
  -[:COVERS_PROCEDURE]-> Procedure
  -[:COVERS_DIAGNOSIS]-> Diagnosis
  -[:HAS_REQUIREMENT]-> Requirement
  -[:REFERENCES]-> LegalReference

ClinicalEvent
  -[:SUPPORTED_BY]-> EvidenceChunk

TherapyEpisode
  -[:SUPPORTED_BY]-> EvidenceChunk

Denial
  -[:SUPPORTED_BY]-> EvidenceChunk

Requirement
  -[:SUPPORTED_BY]-> EvidenceChunk

Policy
  -[:SUPPORTED_BY]-> EvidenceChunk

Document
  -[:CONTAINS]-> EvidenceChunk
```

Do not invent excessive relationship types.

A relationship should exist because it represents a meaningful domain relationship or required traversal path.

---

# 8. REQUIREMENT MODEL

Requirement IDs such as:

```text
REQ-STEP-METFORMIN
REQ-STEP-SULFONYLUREA
REQ-HYPO-LOG

REQ-PRIOR-AUTH
REQ-PHYSIO-6WK
REQ-CLINICAL-EXAM

REQ-MH-BASELINE
REQ-MH-MEDICAL-NECESSITY
```

are canonical identifiers.

Never rename them or create scenario-specific duplicates.

A Requirement should contain machine-usable rule metadata where appropriate.

For example:

```json
{
  "requirement_id": "REQ-PHYSIO-6WK",
  "requirement_type": "therapy_duration",
  "min_duration_days": 42,
  "min_sessions": 6
}
```

Rules that can be evaluated deterministically must be evaluated programmatically.

Do not ask the LLM to decide whether:

```text
39 days >= 42 days
```

or similar deterministic conditions.

---

# 9. EVENT MODELING

Do not flatten temporal evidence directly onto Patient.

Bad:

```text
Patient.pt_sessions = 5
Patient.pt_days = 39
```

Preferred:

```text
Patient
  -[:UNDERWENT]->
TherapyEpisode
```

with:

```text
start_date
end_date
duration_days
session_count
outcome
```

Use event entities for:

```text
therapy
medication trials
labs
clinical examinations
psychiatric sessions
other time-dependent clinical evidence
```

---

# 10. TIME AND POLICY VERSIONING

Policies must contain:

```text
policy_id
version
effective_from
effective_to
```

Policy applicability must respect claim/service date.

Conceptually:

```text
effective_from <= claim_date
AND
(
    effective_to IS NULL
    OR
    effective_to >= claim_date
)
```

Never select a policy version solely because it has the correct policy family/name.

---

# 11. EVIDENCE AS THE NEO4J/QDRANT BRIDGE

`EvidenceChunk` is the bridge between the systems.

Every evidence item should have:

```text
evidence_id
document_id
chunk_id
text_hash
source_type
document_type
section
page when available
scenario_id
patient_id when applicable
claim_id when applicable
policy_id when applicable
requirement_id when applicable
cpt_codes
icd10_codes
denial_codes
source_status
created_at
```

The Qdrant point ID should be the stable `evidence_id`.

This creates:

```text
Neo4j EvidenceChunk
        │
        └──────── same evidence_id ──────── Qdrant point
```

Never rely on filenames as cross-system identity.

---

# 12. DOCUMENT IDs

Create stable IDs such as:

```text
DOC-S1-CLINICAL
DOC-S1-PATIENT
DOC-S2-CLINICAL
DOC-S2-POLICY
```

The exact naming convention may be refined, but IDs must be:

```text
stable
deterministic
unique
independent of filename
```

Compute a canonical content hash for idempotent ingestion.

---

# 13. CHUNKING

Do NOT use a universal:

```text
split every 500 tokens
```

strategy.

Implement typed chunkers:

```text
ClinicalRecordChunker
PolicyChunker
DenialChunker
LegalChunker
PubMedChunker
FallbackChunker
```

### Clinical records

Chunk by:

```text
clinical event
assessment
treatment episode
medication trial
lab/result block
therapy-session block
PHQ-9 block
treatment plan
clinical examination
```

Preserve enough context for the chunk to remain meaningful.

### Policies

Chunk around semantic rules:

```text
coverage
eligibility
requirement
authorization
denial trigger
workflow
appeal procedure
legal reference
```

A policy requirement must not be split across unrelated chunks if doing so loses the rule conditions.

### Denial letters

Chunk around:

```text
denial decision
reason
clinical/administrative rationale
appeal instructions
```

### Legal

Chunk around a coherent reference/statute/regulation section.

### PubMed

For the current synthetic abstracts:

```text
title + abstract + metadata
```

is normally one retrieval unit.

---

# 14. QDRANT DESIGN

Initial collection:

```text
aegis_evidence
```

Payload should contain:

```text
evidence_id
document_id
chunk_id
scenario_id
patient_id
claim_id
policy_id
requirement_id

source_type
document_type
section
page

cpt_codes
icd10_codes
denial_codes

source_status
event_date

text
```

High-value payload indexes include:

```text
patient_id
scenario_id
policy_id
requirement_id
source_type
document_id
```

Do not index every field unnecessarily.

---

# 15. EMBEDDING STRATEGY

Start with a CPU-friendly baseline appropriate for development hardware.

Baseline:

```text
FastEmbed
+
BAAI/bge-small-en-v1.5
```

The system must make the embedding model configurable.

Persist model/configuration metadata.

Changing the embedding model requires a deliberate re-index operation.

Do not silently mix vectors generated by different models in the same vector space.

---

# 16. SPARSE RETRIEVAL

Implement sparse/lexical retrieval for:

```text
CPT codes
ICD-10 codes
denial codes
policy IDs
requirement IDs
legal citations
drug names
exact clinical terminology
```

The sparse result list must be ranked independently.

Do not assume dense embeddings will reliably retrieve identifiers.

---

# 17. HYBRID SEARCH

The primary hybrid mechanism is:

```text
dense retrieval
+
sparse retrieval
+
Neo4j graph retrieval
```

These are independent signals.

Do not directly add:

```text
cosine similarity
+
BM25 score
+
graph score
```

because their scales are not inherently comparable.

Use ranked fusion.

---

# 18. WRRF / RRF

Implement a standalone fusion module.

Example:

```python
def wrf(rank: int, weight: float, k: int = 60) -> float:
    return weight / (k + rank)
```

Initial experimental weights:

```text
dense  = 1.0
sparse = 0.9
graph  = 1.2
```

These are configurable experimental defaults.

Do not claim they are optimal.

The benchmark must determine whether they should change.

Deduplicate by:

```text
evidence_id
```

---

# 19. RETRIEVAL TOP-K

Initial defaults:

```text
dense_top_k = 20
sparse_top_k = 20
fusion_candidate_limit = 50
rerank_top_k = 10
```

These must be configurable.

The actual retrieved counts must be recorded in telemetry.

---

# 20. RERANKING

Use a cross-encoder reranker after first-stage retrieval.

Initial candidate:

```text
BAAI/bge-reranker-v2-m3
```

Pipeline:

```text
20 dense
+
20 sparse
+
graph candidates
        ↓
deduplicate/fuse
        ↓
20–50 candidates
        ↓
reranker
        ↓
5–10 final evidence items
```

Retain:

```text
first_stage_rank
fusion_score
reranker_score
final_rank
```

for observability and debugging.

---

# 21. GRAPH RETRIEVAL

Graph retrieval should be anchored on indexed/stable identifiers.

Examples:

```text
patient_id
claim_id
policy_id
requirement_id
CPT
ICD-10
denial_code
```

Avoid unbounded:

```cypher
MATCH (p)-[*]-(x)
```

queries.

Use explicit labels, relationships and bounded traversal.

Prefer several small, composable queries over one giant multi-hop Cypher query.

---

# 22. GRAPH RETRIEVAL FUNCTIONS

Implement repository methods conceptually equivalent to:

```python
get_patient_case(patient_id)

get_claim_context(claim_id)

get_applicable_policy(policy_id, service_date)

get_policy_requirements(policy_id)

get_requirement_context(requirement_id)

get_denial_context(claim_id)

expand_evidence(evidence_ids)
```

Keep Cypher statements in a dedicated query module.

Use parameterized Cypher only.

---

# 23. QUERY PLANNER

Implement a query planner that converts a user query plus known context into a retrieval plan.

The plan should contain:

```text
intent
patient_id
claim_id
policy_id
requirement_ids
cpt_codes
icd10_codes
denial_codes
source_types
use_graph
use_dense
use_sparse
use_reranker
```

Supported query classes:

```text
EXACT_LOOKUP
CASE_LOOKUP
POLICY_LOOKUP
REQUIREMENT_EVALUATION
EVIDENCE_SEARCH
LITERATURE_SEARCH
FULL_APPEAL_ANALYSIS
```

Examples:

```text
"What does CO-197 mean?"
→ exact lookup

"What policy applies to James's MRI claim?"
→ case + policy lookup

"Did James satisfy REQ-PHYSIO-6WK?"
→ graph + deterministic evaluator + evidence

"What evidence supports continued CBT?"
→ text/literature retrieval + reranking

"Why was James's MRI claim denied?"
→ full hybrid retrieval
```

The planner may use an LLM for entity/intent extraction later, but its final output must be schema-validated.

---

# 24. FAST PATH

Simple exact questions must not trigger the most expensive retrieval pipeline.

Example:

```text
What is CO-197?
```

Use:

```text
exact lookup
→ structured result
```

Avoid unnecessary:

```text
dense search
reranking
graph expansion
LLM
```

when they add no value.

---

# 25. DEEP PATH

For complex questions:

```text
Why was James Chen's MRI claim denied and what evidence supports an appeal?
```

use:

```text
planner
→ graph case lookup
→ policy lookup
→ requirements
→ deterministic evaluation
→ Qdrant metadata filtering
→ dense search
→ sparse search
→ WRRF
→ reranker
→ graph expansion
→ Evidence Pack
```

---

# 26. GRAPH-DRIVEN VECTOR SEARCH

Whenever possible, use Neo4j to establish search scope before Qdrant retrieval.

Example:

```text
user query
→ patient = SYN-PAT-002
→ claim = CLM...
→ procedure = 73721
→ policy = ACME-MRI-2024-002
→ requirements = [...]
```

Then build Qdrant filters using those identifiers.

This prevents retrieval across unrelated scenarios.

---

# 27. GRAPH EXPANSION

After Qdrant retrieves final evidence:

```text
Evidence ID
      ↓
Neo4j
      ↓
Requirement
Policy
Patient
Claim
ClinicalEvent
```

Use controlled traversal.

Initial depth should generally be:

```text
1-hop
```

or carefully bounded 2-hop.

Do not perform arbitrary graph walks.

---

# 28. REQUIREMENT EVALUATION

Create a deterministic evaluator.

Required statuses:

```text
SATISFIED
NOT_SATISFIED
INSUFFICIENT_EVIDENCE
NOT_APPLICABLE
```

Never convert:

```text
missing evidence
```

into:

```text
failure
```

unless the policy explicitly defines missing evidence as a failure.

Each evaluation must include:

```text
requirement_id
status
required_values
actual_values
reason
evidence_ids
```

---

# 29. SCENARIO 1 — CGM

The system must correctly retrieve and evaluate:

```text
REQ-STEP-METFORMIN
REQ-STEP-SULFONYLUREA
REQ-HYPO-LOG
```

Expected answer-key state:

```text
all required conditions satisfied
```

Relevant evidence includes:

```text
Metformin treatment trial
Glipizide treatment trial
hypoglycemia records
glucose/lab data
clinical rationale
CGM policy
```

---

# 30. SCENARIO 2 — MRI

Entities include:

```text
ICD-10 = M25.561
CPT = 73721
Denial = CO-197
Policy = ACME-MRI-2024-002
```

Requirements:

```text
REQ-PRIOR-AUTH
REQ-PHYSIO-6WK
REQ-CLINICAL-EXAM
```

Expected evaluation:

```text
REQ-PRIOR-AUTH = NOT_SATISFIED

REQ-PHYSIO-6WK = NOT_SATISFIED

REQ-CLINICAL-EXAM = SATISFIED
```

The PT requirement must preserve the actual values and compare them deterministically:

```text
required duration = 42 days
actual duration ≈ 39 days

required sessions = 6
actual sessions = 5
```

Never hallucinate that six weeks of PT were completed.

---

# 31. SCENARIO 3 — PSYCHOTHERAPY

Policy:

```text
ACME-MH-2024-003
```

Requirements:

```text
REQ-MH-BASELINE
REQ-MH-MEDICAL-NECESSITY
```

Expected:

```text
REQ-MH-BASELINE = SATISFIED
REQ-MH-MEDICAL-NECESSITY = SATISFIED
```

Retrieve:

```text
F33.1
provider/network information
PHQ-9
clinical progress
treatment goals
medical-necessity rationale
```

Optional PubMed retrieval may use biomedical-specialized models, but the supplied PubMed corpus is synthetic and must not be represented as genuine citations.

---

# 32. PROVENANCE

Every final evidence item must be traceable to:

```text
evidence_id
document_id
chunk_id
source_type
source_status
section
page if applicable
```

Every requirement decision must be traceable to:

```text
policy/rule
+
patient facts
+
evidence
```

No untraceable evidence may be presented as grounded evidence.

---

# 33. SYNTHETIC DATA STATUS

The project contains synthetic data.

Maintain explicit metadata such as:

```text
source_status = synthetic
```

when applicable.

Synthetic legal references and synthetic research records must not be presented as authoritative real-world law or real publications.

Do not fabricate:

```text
PMID
DOI
author
statute
case
policy authority
```

---

# 34. IDEMPOTENT INGESTION

Every canonical document should receive a content hash:

```text
SHA-256
```

Ingestion behavior:

```text
same document + same hash
→ no duplicate ingestion

changed document
→ new version / replacement of affected evidence
```

Repeated ingestion must not create:

```text
duplicate nodes
duplicate evidence
duplicate chunks
duplicate relationships
```

---

# 35. OBSERVABILITY

Record per retrieval request:

```text
request_id
query_type
patient_id where appropriate
dense_candidate_count
sparse_candidate_count
graph_candidate_count
fused_candidate_count
reranked_candidate_count

planner_ms
neo4j_ms
dense_ms
sparse_ms
fusion_ms
reranker_ms
graph_expansion_ms
total_ms
```

Do not log full clinical text by default.

Use synthetic/pseudonymous identifiers in operational logs.

---

# 36. DATABASE CONFIGURATION

Use configuration through existing Pydantic Settings.

Expected categories:

```text
Neo4j URI
Neo4j username
Neo4j password

Qdrant URL
Qdrant API key if applicable

embedding model
reranker model
collection name

top-k values
fusion weights
chunk settings
feature flags
```

Never hardcode secrets.

---

# 37. VERSION PINNING

Use explicit versions for:

```text
Neo4j
Qdrant
Python dependencies
embedding models
reranker models
```

Current research baseline may use:

```text
Neo4j 2026.08.1
Qdrant 1.19.1
```

but verify compatibility with the actual development environment before pinning.

Record model/version metadata for reproducibility.

---

# 38. OPTIONAL ADVANCED TECHNOLOGY

Potential experiments include:

```text
BGE-M3
Qwen3-Embedding-0.6B
MedCPT
Qdrant multivector / late interaction
Neo4j native vector/full-text retrieval
```

Do not add these simply because they are newer.

Benchmark them against the baseline.

Baseline:

```text
FastEmbed
BGE-small
dense + sparse
WRRF
BGE reranker
Neo4j graph traversal
```

Choose an advanced component only when it provides measurable value.

---

# 39. GRAPH RAG LIBRARY USAGE

The official Neo4j GraphRAG Python package may be used where it provides useful adapters or retrievers.

Useful functionality includes:

```text
Qdrant integration
hybrid retrieval
vector + Cypher retrieval
graph-augmented retrieval
```

However:

Do not hide the core project logic inside the framework.

The project must retain explicit control over:

```text
query planning
fusion
requirement evaluation
provenance
testing
```

Frameworks are implementation tools, not architectural substitutes.

---

# 40. TESTING

Use the test strategy defined in:

```text
test_case.md
```

Required levels:

```text
unit
integration
scenario
retrieval benchmark
regression
security/privacy
```

At minimum verify:

```text
stable IDs
provenance
Neo4j constraints
Qdrant filters
exact identifier retrieval
dense retrieval
sparse retrieval
fusion
reranking
graph expansion
requirement evaluation
cross-scenario isolation
```

---

# 41. RETRIEVAL BENCHMARK

Use the supplied answer keys to construct gold evidence sets.

Compare:

```text
A. Dense only
B. Sparse only
C. Dense + Sparse
D. Dense + Sparse + WRRF
E. D + Reranker
F. E + Graph Expansion
```

Measure:

```text
Recall@5
Recall@10
MRR@10
nDCG@10
Precision@5
latency
```

Do not claim improvement without benchmark evidence.

---

# 42. QUALITY TARGETS

Initial engineering targets:

```text
Recall@10 >= 0.90
MRR@10 >= 0.80
nDCG@10 >= 0.80
Precision@5 >= 0.70
```

For exact identifier retrieval:

```text
Recall@5 >= 0.95
```

For deterministic requirement evaluation:

```text
Requirement ID exact-match = 100%
Requirement status exact-match = 100%
Required/actual numeric values = 100%
```

For provenance:

```text
100% of final evidence has provenance
```

For isolation:

```text
0 cross-patient evidence leaks
```

For answer-key contamination:

```text
0 answer-key documents in production retrieval
```

Performance targets for this synthetic-scale system:

```text
ordinary retrieval p95 < 2 s

deep hybrid retrieval p95 < 5 s
```

These are project engineering targets, not healthcare production SLAs.

---

# 43. FAILURE HANDLING

If Neo4j is unavailable:

```text
fail clearly
do not fabricate graph context
```

If Qdrant is unavailable:

```text
structured workflows may degrade to graph/exact retrieval
semantic evidence retrieval must explicitly report degraded mode
```

If reranking fails:

```text
fallback to fused ranking
record reranker_used = false
```

If required evidence is missing:

```text
INSUFFICIENT_EVIDENCE
```

Never manufacture evidence.

---

# 44. CODE QUALITY

Follow repository standards:

```text
Ruff
Pre-commit
Pytest
Pydantic
type hints where practical
```

Prefer small, composable functions.

Avoid:

```text
giant service classes
giant Cypher queries
giant retrieval functions
global mutable state
hardcoded credentials
hardcoded patient IDs
hardcoded ranking outputs
```

---

# 45. IMPLEMENTATION RULE

Do not implement the entire system as one large change.

Implement in vertical, testable stages:

```text
1. domain models
2. Neo4j schema/constraints
3. canonical extraction
4. graph ingestion
5. evidence model
6. typed chunking
7. Qdrant collection
8. embedding/indexing
9. dense retrieval
10. sparse retrieval
11. fusion
12. reranking
13. graph expansion
14. requirement evaluator
15. retrieval service
16. API endpoint
17. evaluation benchmark
18. quality/regression checks
```

After each stage:

```text
run relevant tests
inspect outputs
fix defects
then proceed
```

Do not build everything and only test at the end.

---

# 46. EXPECTED FILES

Follow `/retriever_plan/structure.md`.

Expected important implementation areas:

```text
src/aegis/models/
src/aegis/extraction/
src/aegis/graph/
src/aegis/vector/
src/aegis/retrieval/
src/aegis/evaluation/
```

Suggested key modules:

```text
graph/client.py
graph/schema.py
graph/constraints.py
graph/indexes.py
graph/repository.py
graph/queries.py
graph/traversal.py

vector/client.py
vector/collections.py
vector/chunking.py
vector/embeddings.py
vector/indexing.py
vector/filtering.py
vector/search.py

retrieval/planner.py
retrieval/exact.py
retrieval/graph.py
retrieval/dense.py
retrieval/sparse.py
retrieval/fusion.py
retrieval/reranker.py
retrieval/expansion.py
retrieval/service.py

evaluation/golden_set.py
evaluation/metrics.py
evaluation/benchmark.py
evaluation/regression.py
```

Do not create files unnecessarily.

---

# 47. API CONTRACT

The retrieval subsystem should expose:

```http
POST /retrieval/search
```

Example request:

```json
{
  "query": "Why was James Chen's MRI claim denied?",
  "patient_id": "SYN-PAT-002"
}
```

Return a normalized Evidence Pack:

```json
{
  "facts": [],
  "requirements": [],
  "evidence": [],
  "graph_context": [],
  "provenance": [],
  "retrieval_metadata": {}
}
```

The LangGraph/agent layer must not need to know whether an item came from:

```text
Neo4j
Qdrant dense
Qdrant sparse
reranking
graph expansion
```

unless that information is intentionally included as metadata.

---

# 48. EVIDENCE PACK CONTRACT

Each evidence item should resemble:

```json
{
  "evidence_id": "EV-S2-PT-001",
  "document_id": "DOC-S2-CLINICAL",
  "chunk_id": "DOC-S2-CLINICAL::PT-SUMMARY",
  "text": "...",
  "source_type": "clinical_record",
  "score": 0.0,
  "rank": 1,
  "matched_by": ["dense", "sparse"],
  "provenance": {}
}
```

Requirement results should contain:

```json
{
  "requirement_id": "REQ-PHYSIO-6WK",
  "status": "NOT_SATISFIED",
  "required": {},
  "actual": {},
  "reason": "...",
  "evidence_ids": []
}
```

---

# 49. CRITICAL ANTI-PATTERNS

Do not:

```text
put entire PDFs into Neo4j as giant nodes
embed every scalar JSON property
use only cosine similarity
use only graph traversal
use one fixed chunk size for every document type
allow arbitrary LLM-generated Cypher as the normal path
hardcode patient IDs
hardcode policy decisions
compare raw BM25 and cosine scores directly
retrieve all scenarios for every question
index answer keys
invent missing evidence
treat synthetic legal/research data as authoritative
log complete patient records
```

---

# 50. REQUIRED ENGINEERING BEHAVIOR

Whenever you make a change:

1. Identify which architectural requirement it satisfies.
2. Keep the implementation consistent with the five planning documents.
3. Add or update tests.
4. Run the relevant test subset.
5. Report exact failures rather than hiding them.
6. Preserve provenance.
7. Avoid speculative abstractions.
8. Prefer a simple implementation when it achieves the same architectural requirement.
9. Measure retrieval quality before declaring an optimization successful.
10. Keep configuration explicit and reproducible.

---

# 51. DEFINITION OF DONE

The retrieval subsystem is not complete until:

```text
[ ] all source files audited
[ ] answer keys excluded from retrieval
[ ] canonical IDs implemented
[ ] document hashes implemented
[ ] Neo4j constraints implemented
[ ] Neo4j indexes implemented
[ ] domain graph populated
[ ] temporal policy applicability works
[ ] EvidenceChunk bridge exists
[ ] typed chunking works
[ ] Qdrant collection works
[ ] Qdrant payload filters work
[ ] dense retrieval works
[ ] sparse retrieval works
[ ] WRRF/RRF works
[ ] reranking works
[ ] graph expansion works
[ ] deterministic requirement evaluation works
[ ] retrieval planner works
[ ] Evidence Pack contract works
[ ] retrieval API works
[ ] Scenario 1 tests pass
[ ] Scenario 2 tests pass
[ ] Scenario 3 tests pass
[ ] cross-patient isolation passes
[ ] provenance coverage is 100%
[ ] answer-key contamination is zero
[ ] retrieval benchmark passes quality targets
[ ] latency benchmark recorded
[ ] model/configuration versions recorded
[ ] full test suite passes
```

---

# 52. FINAL PRINCIPLE

The system must answer:

```text
"What does the evidence say?"
```

and:

```text
"What facts and relationships are actually present?"
```

before asking:

```text
"How should the LLM explain this?"
```

The architecture must therefore preserve this separation:

```text
                    AegisHealth-KG
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
       Neo4j            Qdrant          Evaluator
       Facts            Evidence          Rules
       Relations        Meaning           Logic
          │               │                │
          └───────────────┼────────────────┘
                          ▼
                    Hybrid Retrieval
                          │
                          ▼
                     Evidence Pack
                          │
                          ▼
                       LangGraph
                          │
                          ▼
                          LLM
```

Build the subsystem so that a developer can inspect any final answer and determine:

```text
which facts were used
which policy was selected
which requirements were evaluated
which evidence chunks were retrieved
why those chunks ranked highly
where each chunk came from
what was deterministic
what was generated by the LLM
```

That traceability is a first-class requirement, not an optional feature.
