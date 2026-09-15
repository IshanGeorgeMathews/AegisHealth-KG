# AegisHealth-KG — Architecture Plan

## 1. Purpose

This document defines the production-oriented architecture for the AegisHealth-KG retrieval subsystem.

Scope:

- Canonical healthcare domain model
- Neo4j knowledge graph
- Qdrant evidence index
- Structure-aware chunking
- Dense + sparse retrieval
- Exact identifier lookup
- Graph retrieval and graph expansion
- Rank fusion and reranking
- Evidence provenance
- Requirement evaluation
- Retrieval API exposed to the LangGraph/agent layer
- Retrieval evaluation and operational quality

Out of scope:

- Final LLM prompt engineering
- Full appeal-document rendering
- Frontend implementation
- Real-world legal/medical validation of the synthetic corpus

The corpus is synthetic. Synthetic legal references and synthetic PubMed-style articles must never be presented by the system as real legal authority or real research.

---

## 2. Architectural Principle

Aegis must maintain three distinct representations of knowledge:

1. Structured facts and relationships → Neo4j
2. Searchable textual evidence → Qdrant
3. Decision/evaluation logic → deterministic Python services

The LLM is downstream of retrieval and evaluation. It is not the source of truth for basic facts, requirement satisfaction, dates, codes, or policy applicability.

Core principle:

```text
Facts       → Graph / structured records
Meaning     → Dense retrieval
Exact terms → Sparse/exact retrieval
Relations   → Graph traversal
Rules       → Deterministic evaluator
Explanation → LLM
```

---

## 3. High-Level Architecture

```text
                             ┌──────────────────┐
                             │     User Query   │
                             └────────┬─────────┘
                                      │
                                      ▼
                             ┌──────────────────┐
                             │  Query Planner   │
                             │ patient / claim  │
                             │ policy / codes   │
                             │ intent / dates   │
                             └────────┬─────────┘
                                      │
            ┌─────────────────────────┼─────────────────────────┐
            │                         │                         │
            ▼                         ▼                         ▼
     Exact Identifier           Neo4j Graph              Qdrant Search
        Lookup                  Retrieval                  │
            │                         │              ┌───────┴────────┐
            │                         │              ▼                ▼
            │                         │           Dense            Sparse
            │                         │              │                │
            │                         │              └──────┬─────────┘
            │                         │                     ▼
            │                         │                Candidate Set
            │                         │                     │
            │                         │                     ▼
            │                         │                 Reranker
            │                         │                     │
            └─────────────────────────┼─────────────────────┘
                                      ▼
                              Rank Fusion / Merge
                                      │
                                      ▼
                              Graph Evidence Expansion
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

The graph and vector database are connected through stable identifiers, especially:

- `document_id`
- `evidence_id`
- `chunk_id`
- `patient_id`
- `claim_id`
- `policy_id`
- `requirement_id`
- `cpt_code`
- `icd10_code`
- `denial_code`

---

## 4. Domain Data Classification

### 4.1 Patient JSON

Primary:

- Neo4j

Extract:

- Patient
- Provider
- Payer
- InsurancePlan
- Diagnosis
- Medication
- LabResult
- ClinicalEvent
- TherapyEpisode
- Claim
- ClaimLine
- Procedure

Optional textual summaries may be indexed, but scalar identifiers and values should remain structured.

### 4.2 EOB JSON

Primary:

- Neo4j

Extract:

- Claim
- ClaimLine
- Procedure
- Diagnosis
- Denial
- DenialCode
- Payer
- Policy reference

Narrative fields may also become Qdrant evidence if they contain useful explanatory text.

### 4.3 Clinical Markdown

Primary:

- Qdrant

Secondary:

- Neo4j extracted entities/events

Chunk by:

- clinical event
- treatment episode
- assessment
- lab/result block
- medication trial
- progress-note section

Do not use blind fixed-token chunking as the primary method.

### 4.4 Policy Markdown

Primary:

- Qdrant

Secondary:

- Neo4j

Chunk by rule/requirement:

```text
coverage
requirement
authorization
denial trigger
workflow
legal reference
```

Requirement IDs such as `REQ-PHYSIO-6WK` are canonical graph identifiers.

### 4.5 Denial PDF

Primary:

- Qdrant

Secondary:

- Neo4j

Extract:

- denial category
- denial code
- claim reference
- policy reference
- appeal instructions
- denial rationale

Each textual section/chunk must retain page/source provenance.

### 4.6 Prior Authorization Markdown

Primary:

- Qdrant

Secondary:

- Neo4j

Each `REQ-*` rule becomes a canonical `Requirement` node.

### 4.7 Legal References

Primary:

- Qdrant

Secondary:

- Neo4j `LegalReference`

Metadata must mark these sources as synthetic/mock where applicable.

### 4.8 CPT / HCPCS and ICD-10 references

Primary:

- Neo4j or another structured lookup layer

Do not embed every code definition by default.

Exact code matching should be authoritative for the synthetic corpus.

### 4.9 PubMed-style JSON

Primary:

- Qdrant

Secondary:

- Neo4j article metadata only if needed

Important:

The provided PubMed records are explicitly synthetic/fabricated. They may support retrieval demonstrations but must not be represented as real citations.

### 4.10 Answer keys

Never put answer keys into the production retrieval index.

They are an evaluation corpus only.

---

## 5. Canonical Neo4j Schema

### 5.1 Core node labels

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

### 5.2 Identity rules

Every domain node that can be referenced from another system needs a stable identifier.

Examples:

```text
Patient.patient_id
Claim.claim_id
Policy.policy_id
Requirement.requirement_id
Document.document_id
EvidenceChunk.evidence_id
```

Codes:

```text
CPTCode.code
ICD10Code.code
DenialCode.code
```

### 5.3 Core relationships

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

Do not create a relationship type merely because a sentence contains two entities. A relation must represent a domain relationship that the retrieval/decision system may need to traverse.

---

## 6. Event Modeling Rule

Do not flatten time-dependent evidence onto the Patient node.

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
  {
    start_date,
    end_date,
    duration_days,
    session_count,
    outcome
  }
```

This enables deterministic comparison against policy requirements.

The same principle applies to:

- medication trials
- lab observations
- psychiatric sessions
- clinical examinations
- authorization events

---

## 7. Temporal and Versioned Data

Policies must carry:

```text
policy_id
version
effective_from
effective_to
```

Claims should carry the service date.

A policy is applicable only when:

```text
effective_from <= claim_date
AND (
    effective_to IS NULL
    OR effective_to >= claim_date
)
```

This rule must be enforced before selecting a policy version for a claim.

Evidence may also contain:

```text
event_date
document_date
source_version
```

---

## 8. Evidence Model

`EvidenceChunk` is the bridge between Neo4j and Qdrant.

Recommended properties:

```text
evidence_id
document_id
chunk_id
text_hash
source_type
document_type
section
page
scenario_id
patient_id
claim_id
policy_id
requirement_id
cpt_codes
icd10_codes
denial_codes
source_status
created_at
```

Qdrant uses `evidence_id` as the stable point identity.

Graph nodes that require textual support point to the same `EvidenceChunk`.

---

## 9. Qdrant Collection

Initial collection:

```text
aegis_evidence
```

Recommended payload fields:

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

Development baseline:

```text
dense embedding
+
sparse retrieval
```

Optional later:

```text
late-interaction / multivector
```

Payload indexes should be created for high-value filter fields such as:

```text
patient_id
scenario_id
policy_id
requirement_id
source_type
document_id
```

---

## 10. Chunking Architecture

Use a typed chunker:

```text
Document
   │
   ├── clinical_record_chunker
   ├── policy_chunker
   ├── denial_chunker
   ├── legal_chunker
   ├── pubmed_chunker
   └── generic_fallback_chunker
```

### Clinical record

Chunk around:

- medication trial
- hypoglycemia event log
- lab block
- clinical assessment
- treatment plan
- therapy episode
- psychiatric assessment
- PHQ-9 block

### Policy

Chunk around:

- policy scope
- covered procedures
- covered diagnoses
- individual requirement
- denial trigger
- authorization workflow
- appeal process
- legal reference

### Denial

Chunk around:

- denial decision
- reason
- clinical rationale
- administrative reason
- appeal instructions

### Legal

Chunk around one statute/regulation/reference section.

### PubMed

For the supplied synthetic abstracts, one article can usually be one retrieval unit:

```text
title + abstract + keywords + metadata
```

---

## 11. Query Planning

Queries are routed into one or more retrieval modes.

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

"Why was James's MRI claim denied?"
→ case + policy + denial + evidence

"Did James satisfy REQ-PHYSIO-6WK?"
→ graph + deterministic evaluator + evidence

"Find evidence supporting continued CBT"
→ Qdrant + biomedical/text retrieval + reranker

"Generate an appeal for James"
→ full hybrid pipeline
```

---

## 12. Hybrid Retrieval

### Stage 1 — Anchor extraction

Extract:

```text
patient_id
claim_id
CPT
ICD-10
denial code
policy_id
requirement_id
dates
query intent
```

### Stage 2 — Graph retrieval

Resolve:

```text
patient
→ claim
→ denial
→ procedure
→ policy
→ requirements
```

### Stage 3 — Qdrant filters

Use graph-derived IDs to narrow vector search.

Example:

```text
patient_id = SYN-PAT-002
AND
policy_id = ACME-MRI-2024-002
```

or:

```text
requirement_id = REQ-PHYSIO-6WK
```

### Stage 4 — Dense + sparse retrieval

Retrieve candidate sets independently.

Suggested development values:

```text
dense top_k = 20
sparse top_k = 20
```

### Stage 5 — Rank fusion

Use RRF/WRRF.

Do not directly add cosine similarity to BM25 scores.

Example:

```python
rrf_score = weight / (k + rank)
```

Initial experimental weights:

```text
dense  = 1.0
sparse = 0.9
graph  = 1.2
```

These weights must be tuned against the evaluation set.

### Stage 6 — Reranking

Take approximately 20–50 fused candidates and rerank the best candidates using a cross encoder.

Initial target:

```text
top 5–10 final evidence chunks
```

### Stage 7 — Graph expansion

For the final evidence IDs:

```text
EvidenceChunk
→ Requirement
→ Policy
→ Patient
→ Claim
→ ClinicalEvent
```

This reconstructs the connected case context.

### Stage 8 — Requirement evaluation

Run deterministic calculations where applicable.

### Stage 9 — Evidence Pack

Return a normalized retrieval result to LangGraph.

---

## 13. Evidence Pack Contract

The agent should consume a stable structure:

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

Each evidence item:

```json
{
  "evidence_id": "...",
  "document_id": "...",
  "chunk_id": "...",
  "text": "...",
  "source_type": "...",
  "score": 0.0,
  "rank": 1,
  "matched_by": ["dense", "sparse"],
  "provenance": {}
}
```

---

## 14. Requirement Evaluation

Requirement evaluation is not a vector-search task.

Example:

```text
Requirement:
REQ-PHYSIO-6WK

Required:
duration >= 42 days
sessions >= 6

Observed:
duration = 39 days
sessions = 5

Result:
NOT_SATISFIED
```

For each requirement return:

```text
requirement_id
status
required_values
actual_values
reason
evidence_ids
```

This makes explanations traceable.

---

## 15. Retrieval API

Proposed endpoint:

```http
POST /retrieval/search
```

Request:

```json
{
  "query": "Why was James Chen's MRI claim denied?",
  "patient_id": "SYN-PAT-002"
}
```

Response:

```json
{
  "facts": [],
  "requirements": [],
  "evidence": [],
  "graph_context": [],
  "retrieval_metadata": {
    "dense_candidates": 20,
    "sparse_candidates": 20,
    "fused_candidates": 0,
    "reranked_candidates": 10,
    "latency_ms": 0
  }
}
```

The exact numerical fields must be populated from the execution rather than guessed.

---

## 16. Data Flow

```text
Raw Files
   ↓
Document Identification
   ↓
Canonical Parsing
   ├───────────────┐
   ▼               ▼
Structured Data   Text Evidence
   │               │
   ▼               ▼
Neo4j             Typed Chunking
                   ↓
                 Embedding
                   ↓
                 Qdrant
   │               │
   └──────┬────────┘
          ▼
     Stable IDs
```

Ingestion must be idempotent using a content hash.

---

## 17. Production-Oriented Operational Rules

1. Pin database/image versions.
2. Pin Python dependencies.
3. Use `.env` for secrets.
4. Never log full clinical text by default.
5. Use pseudonymous synthetic IDs in logs.
6. Parameterize all Cypher queries.
7. Treat ingestion as idempotent.
8. Store source hashes.
9. Retain provenance.
10. Keep evaluation data separate from retrieval data.
11. Make retrieval deterministic enough to debug.
12. Record retrieval metadata and latency.
13. Fail closed when provenance is missing for regulated evidence.
14. Mark synthetic/legal/reference status explicitly.

---

## 18. Technology Baseline and Research References

Current technologies worth evaluating:

- Neo4j GraphRAG Python: https://github.com/neo4j/neo4j-graphrag-python
- Qdrant: https://github.com/qdrant/qdrant
- Qdrant Python client: https://github.com/qdrant/qdrant-client
- FastEmbed: https://github.com/qdrant/fastembed
- FlagEmbedding/BGE: https://github.com/FlagOpen/FlagEmbedding
- Qwen3 Embedding: https://github.com/QwenLM/Qwen3-Embedding
- MedCPT: https://github.com/ncbi/MedCPT

Current ecosystem features particularly relevant to this design:

- Neo4j hybrid/vector/graph retrieval capabilities
- Qdrant dense+sparse hybrid search
- Qdrant multistage retrieval and reranking
- FastEmbed CPU-oriented inference
- BGE-M3 dense/sparse/multivector retrieval
- Biomedical-specific MedCPT retrieval/reranking

Use these as implementation options, not mandatory dependencies. The project's benchmark must determine whether the extra complexity is justified.

---

## 19. Architectural Decision

The default production-oriented Aegis design is:

```text
Neo4j
= structured decision graph

Qdrant
= searchable evidence store

FastEmbed/BGE baseline
= local CPU-friendly embeddings

Dense + sparse
= first retrieval stage

WRRF
= candidate fusion

Cross encoder
= reranking

Graph expansion
= connected context reconstruction

Python evaluator
= deterministic requirement checks

LangGraph
= workflow/orchestration

LLM
= final explanation/generation
```

This separation is the baseline unless benchmark results show a better alternative.
