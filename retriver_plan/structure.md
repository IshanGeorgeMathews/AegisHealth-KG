# AegisHealth-KG — Code Structure

## 1. Goal

This structure separates domain modeling, ingestion, graph storage, vector storage, retrieval, evaluation, and API concerns.

```text
src/aegis/
│
├── api/
│   ├── __init__.py
│   └── routes/
│       ├── __init__.py
│       └── retrieval.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── models/
│   ├── __init__.py
│   ├── domain.py
│   ├── evidence.py
│   ├── retrieval.py
│   └── requirements.py
│
├── extraction/
│   ├── __init__.py
│   ├── dispatcher.py
│   ├── json_parser.py
│   ├── markdown_parser.py
│   ├── pdf_parser.py
│   ├── normalization.py
│   ├── entities.py
│   └── provenance.py
│
├── graph/
│   ├── __init__.py
│   ├── client.py
│   ├── schema.py
│   ├── constraints.py
│   ├── indexes.py
│   ├── repository.py
│   ├── queries.py
│   └── traversal.py
│
├── vector/
│   ├── __init__.py
│   ├── client.py
│   ├── collections.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── indexing.py
│   ├── filtering.py
│   └── search.py
│
├── retrieval/
│   ├── __init__.py
│   ├── planner.py
│   ├── exact.py
│   ├── graph.py
│   ├── dense.py
│   ├── sparse.py
│   ├── fusion.py
│   ├── reranker.py
│   ├── expansion.py
│   └── service.py
│
├── evaluation/
│   ├── __init__.py
│   ├── golden_set.py
│   ├── metrics.py
│   ├── benchmark.py
│   └── regression.py
│
└── main.py
```

---

## 2. Responsibility Boundaries

### `models/`

Only define contracts and domain models.

Do not connect to databases here.

Important models:

```text
Patient
Claim
Procedure
Diagnosis
Policy
Requirement
ClinicalEvent
TherapyEpisode
EvidenceChunk
RetrievedEvidence
RetrievalResult
RequirementResult
```

### `extraction/`

Converts raw files into canonical intermediate structures.

Responsibilities:

- identify document type
- parse JSON/Markdown/PDF
- normalize fields
- create provenance
- extract candidate entities
- produce canonical documents

It should not perform graph queries or vector search.

### `graph/`

Neo4j-only layer.

Responsibilities:

- connections
- constraints
- indexes
- upsert operations
- case queries
- policy queries
- requirement queries
- graph expansion

No embedding logic.

### `vector/`

Qdrant-only layer.

Responsibilities:

- collection creation
- chunk creation
- embedding
- payload
- indexing
- filtering
- vector search

No business-rule evaluation.

### `retrieval/`

Orchestrates Neo4j + Qdrant.

Responsibilities:

- query planning
- graph lookup
- dense search
- sparse search
- fusion
- reranking
- graph expansion
- result normalization

This is the core retrieval subsystem.

### `evaluation/`

Measures retrieval quality against answer keys.

Must not mutate production retrieval data.

### `api/`

Exposes stable HTTP interfaces.

The API must not contain raw Cypher or Qdrant implementation details.

---

## 3. Recommended Public Interfaces

### Graph repository

```python
class GraphRepository:
    def get_patient_case(self, patient_id: str): ...
    def get_claim_context(self, claim_id: str): ...
    def get_applicable_policy(self, policy_id: str, service_date): ...
    def get_policy_requirements(self, policy_id: str): ...
    def get_requirement_context(self, requirement_id: str): ...
    def expand_evidence(self, evidence_ids: list[str]): ...
```

### Vector repository

```python
class VectorRepository:
    def upsert_evidence(self, evidence_items): ...
    def search_dense(self, query, filters, top_k): ...
    def search_sparse(self, query, filters, top_k): ...
    def search_hybrid(self, query, filters, top_k): ...
```

### Retrieval service

```python
class RetrievalService:
    def retrieve(
        self,
        query: str,
        patient_id: str | None = None,
        claim_id: str | None = None,
    ) -> RetrievalResult:
        ...
```

---

## 4. Dependency Direction

Preferred dependency flow:

```text
api
 ↓
retrieval
 ├── graph
 ├── vector
 ├── models
 └── evaluation utilities only when explicitly requested

graph → models/config
vector → models/config
extraction → models
models → standard library only where practical
```

Avoid:

```text
graph → retrieval
vector → retrieval
models → graph
models → qdrant
```

The lower layers should not depend on orchestration.

---

## 5. Ingestion Structure

```text
extraction/
       ↓
CanonicalDocument
       ↓
      / \
     /   \
    ▼     ▼
 graph   chunker
          ↓
       embedding
          ↓
       Qdrant
```

Canonical document example:

```python
class CanonicalDocument:
    document_id: str
    document_version: str
    content_hash: str
    source_type: str
    source_status: str
    scenario_id: int | None
    patient_id: str | None
    text: str
    metadata: dict
```

---

## 6. Chunker Design

Interface:

```python
class Chunker(Protocol):
    def chunk(self, document: CanonicalDocument) -> list[EvidenceChunk]:
        ...
```

Implement:

```text
ClinicalRecordChunker
PolicyChunker
DenialChunker
LegalChunker
PubMedChunker
FallbackChunker
```

Each chunk must retain:

```text
document_id
chunk_id
evidence_id
section
page if available
source_type
scenario_id
```

---

## 7. Graph Query Organization

Do not put all Cypher in repository methods.

Keep reusable queries in:

```text
graph/queries.py
```

Group them:

```text
PATIENT_CASE_QUERY
CLAIM_CONTEXT_QUERY
POLICY_REQUIREMENTS_QUERY
DENIAL_CONTEXT_QUERY
EVIDENCE_EXPANSION_QUERY
```

Repository methods supply parameters and map records into domain models.

---

## 8. Cypher Rules

Always parameterize:

```python
session.run(
    QUERY,
    patient_id=patient_id,
)
```

Never:

```python
f"MATCH (p:Patient {{patient_id: '{patient_id}'}})"
```

Avoid unbounded traversals such as:

```cypher
MATCH (p)-[*]-(x)
```

unless there is a strict depth and label/relationship constraint.

Prefer anchored traversal from an indexed identifier.

---

## 9. Qdrant Payload Rules

Payload fields are not an excuse to duplicate the entire graph.

Keep:

```text
filterable identifiers
+
provenance
+
retrieval text
```

Do not copy every patient scalar into every chunk.

Example:

```json
{
  "evidence_id": "EV-S2-PT-001",
  "patient_id": "SYN-PAT-002",
  "policy_id": "ACME-MRI-2024-002",
  "requirement_id": "REQ-PHYSIO-6WK",
  "source_type": "clinical_record",
  "text": "..."
}
```

---

## 10. Retrieval Pipeline Implementation

`retrieval/service.py` should be the only component responsible for the full flow:

```text
query
 ↓
planner
 ↓
graph anchor
 ↓
filters
 ↓
dense search
 +
sparse search
 ↓
fusion
 ↓
rerank
 ↓
graph expansion
 ↓
requirement evaluation
 ↓
EvidencePack
```

Individual retrievers should remain independently testable.

---

## 11. Logging

Production-style logs should contain:

```text
request_id
query_type
patient_id (synthetic/pseudonymous only)
candidate counts
final evidence IDs
latency
errors
```

Avoid logging:

```text
full clinical text
full patient JSON
secrets
database credentials
```

---

## 12. Configuration

Use `Pydantic Settings`.

Example categories:

```text
Neo4j
Qdrant
Embedding model
Reranker model
Collection names
Top-k values
RRF weights
Chunk limits
Feature flags
```

Example environment:

```text
NEO4J_URI=
NEO4J_USERNAME=
NEO4J_PASSWORD=

QDRANT_URL=
QDRANT_API_KEY=

EMBEDDING_MODEL=
RERANKER_MODEL=

QDRANT_COLLECTION=aegis_evidence
```

---

## 13. Testing Structure

Mirror source structure:

```text
tests/
├── unit/
│   ├── extraction/
│   ├── chunking/
│   ├── fusion/
│   ├── requirements/
│   └── normalization/
│
├── integration/
│   ├── test_neo4j_repository.py
│   ├── test_qdrant_repository.py
│   └── test_hybrid_retrieval.py
│
└── evaluation/
    ├── test_scenario_1.py
    ├── test_scenario_2.py
    └── test_scenario_3.py
```

---

## 14. Data Structure

Keep the supplied dataset unchanged.

```text
data/
└── synthetic/
    ├── answer_keys/
    ├── clinical_records/
    ├── code_references/
    ├── denial_letters/
    ├── eob/
    ├── legal_references/
    ├── patients/
    ├── policies/
    ├── prior_auth/
    └── pubmed_articles/
```

Add generated/derived artifacts outside the source corpus:

```text
data/derived/
data/index/
```

Never commit a generated vector database dump as if it were source data.

---

## 15. Team Ownership

Recommended ownership:

```text
Neo4j owner
→ graph/

Vector owner
→ vector/

Hybrid retrieval owner
→ retrieval/

Data ingestion owner
→ extraction/

Agent owner
→ agent/ or LangGraph layer

API owner
→ api/
```

Your role specifically should own:

```text
graph/
vector/
retrieval/
evaluation retrieval benchmarks
```

---

## 16. Definition of Done for Your Subsystem

Your subsystem is complete only when:

```text
[ ] all 3 scenarios can be ingested
[ ] all canonical IDs are stable
[ ] Neo4j constraints exist
[ ] Qdrant collection exists
[ ] chunks preserve provenance
[ ] dense retrieval works
[ ] sparse retrieval works
[ ] hybrid fusion works
[ ] reranking works
[ ] graph expansion works
[ ] requirement evaluation works
[ ] answer-key benchmark runs
[ ] retrieval metrics are reported
[ ] all integration tests pass
[ ] no answer-key content is retrieved in production search
```
