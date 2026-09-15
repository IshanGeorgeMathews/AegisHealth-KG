# AegisHealth-KG — Quality and Acceptance Plan

## 1. Purpose

This document defines objective quality gates for the Neo4j + Qdrant retrieval subsystem.

The goal is not merely that the LLM produces a plausible answer.

The system must retrieve the right evidence, preserve provenance, evaluate requirements correctly, and avoid unsupported conclusions.

---

## 2. Quality Dimensions

Evaluate five dimensions:

```text
1. Retrieval quality
2. Decision/evaluation correctness
3. Grounding and provenance
4. Isolation and safety
5. Performance and maintainability
```

---

## 3. Retrieval Quality

### 3.1 Metrics

Use:

```text
Recall@5
Recall@10
MRR@10
nDCG@10
Precision@5
```

Definitions:

```text
Recall@K
= fraction of required gold evidence retrieved within top K

MRR
= reciprocal rank of the first relevant result

nDCG
= ranking quality accounting for graded relevance
```

### 3.2 Initial Release Targets

For the small synthetic benchmark, set high targets because the corpus is intentionally controlled.

Recommended gates:

```text
Recall@10        >= 0.90
MRR@10           >= 0.80
nDCG@10          >= 0.80
Precision@5      >= 0.70
```

These are engineering acceptance targets, not claims about real-world medical retrieval performance.

If a metric misses the target, document:

```text
failure query
retriever stage
gold evidence
retrieved evidence
root cause
planned fix
```

---

## 4. Requirement Evaluation Quality

Requirement evaluation has stronger requirements than semantic retrieval.

For the supplied answer keys:

```text
Scenario 1:
3/3 requirements correct

Scenario 2:
3/3 requirements correct
2 missing
1 satisfied

Scenario 3:
2/2 requirements correct
0 missing
```

Acceptance:

```text
Requirement ID exact-match = 100%
Requirement count exact-match = 100%
Satisfied/missing classification exact-match = 100%
Required-vs-actual numeric facts = 100%
```

A single incorrect requirement result is a critical defect because the evaluator is deterministic.

---

## 5. Grounding Quality

Every final evidence item must have:

```text
evidence_id
document_id
chunk_id
source_type
source_status
text
```

Target:

```text
100% provenance coverage
```

Every requirement conclusion must reference:

```text
policy evidence
+
patient/case evidence
```

when both are needed.

Target:

```text
100% evidence-linked requirement conclusions
```

---

## 6. Hallucination/Unsupported Claim Gates

The system must never:

```text
invent a requirement
invent a policy ID
invent a claim
invent a diagnosis
invent a laboratory result
invent a CPT/ICD code
invent a legal citation
invent a PubMed article
invent a DOI
change an observed numeric value
```

Scenario-specific negative tests are mandatory.

Examples:

### Scenario 2

Bad:

```text
"Patient completed six weeks of physical therapy."
```

Correct:

```text
"Patient completed approximately 5.7 weeks and 5 sessions."
```

### Scenario 3

Bad:

```text
"MHPAEA guarantees eligibility."
```

Correct:

```text
"The retrieved parity material supports a parity analysis; it does not by itself establish eligibility."
```

### PubMed

Bad:

```text
fabricated PMID/DOI/article citation
```

Correct:

```text
only metadata present in the retrieved source
```

---

## 7. Cross-Patient Isolation

A retrieval request scoped to:

```text
patient_id = SYN-PAT-002
```

must not expose patient-specific evidence from:

```text
SYN-PAT-001
SYN-PAT-003
```

Acceptance:

```text
0 cross-patient evidence leaks
```

This is a critical gate even though the current corpus is synthetic.

---

## 8. Policy Isolation

A claim must use the policy applicable to its:

```text
policy_id
+
service date
+
version
```

Acceptance:

```text
0 policy-version selection errors
```

---

## 9. Exact Identifier Quality

For exact identifiers such as:

```text
CO-197
CO-167
CO-50

73721
95251
90837

M25.561
E11.9
F33.1

REQ-PRIOR-AUTH
REQ-PHYSIO-6WK
REQ-MH-MEDICAL-NECESSITY
```

the system should achieve:

```text
Recall@5 >= 0.95
```

on exact-lookup benchmark queries.

If exact lookup fails, the system should route through lexical/exact lookup before relying on dense retrieval.

---

## 10. Chunking Quality

Measure whether each gold evidence unit remains retrievable.

A chunk is high-quality when:

```text
contains a coherent fact/rule/event
has complete necessary context
has correct source metadata
does not mix unrelated patients
does not split critical rule conditions
```

Manual review sample:

```text
at least 20 representative chunks
```

per major source type before first release.

Check:

```text
clinical
policy
denial
legal
PubMed
```

---

## 11. Fusion Quality

Run an ablation:

```text
Dense only
Sparse only
Dense + Sparse
Dense + Sparse + Graph
Full Hybrid
```

Measure:

```text
Recall@10
MRR@10
nDCG@10
latency
```

The full hybrid system is accepted only if graph and fusion stages provide measurable value or a documented reason exists for their omission on a particular query class.

---

## 12. Reranker Quality

Compare:

```text
without reranker
vs
with reranker
```

Acceptance target:

```text
reranking must improve or preserve Recall@10
and improve ranking quality (MRR/nDCG)
on the benchmark set.
```

A reranker that increases latency without improving ranking quality should not be enabled by default.

---

## 13. Graph Expansion Quality

Graph expansion must:

```text
add connected evidence/facts
not introduce unrelated entities
respect patient and policy scope
preserve evidence IDs
```

Test:

```text
Qdrant evidence
→ Neo4j requirement
→ policy
→ patient/claim
```

Acceptance:

```text
0 unrelated-patient expansions
0 missing provenance links
```

---

## 14. Performance Targets

Because the dataset is small, absolute latency numbers are less important than architectural measurement.

Track:

```text
planner_ms
neo4j_ms
dense_ms
sparse_ms
fusion_ms
reranker_ms
graph_expansion_ms
total_ms
```

For local development, target a practical p95 for ordinary retrieval:

```text
p95 < 2 seconds
```

and for full deep retrieval with reranking:

```text
p95 < 5 seconds
```

These are engineering targets for this synthetic-scale project, not production healthcare SLAs.

If model inference is CPU-bound, report the actual latency and model details rather than hiding it.

---

## 15. Indexing Quality

After ingestion verify:

```text
source file count
canonical document count
Neo4j node counts
Neo4j relationship counts
Qdrant point count
duplicate evidence IDs
missing provenance
```

Acceptance:

```text
0 duplicate evidence IDs
0 missing required provenance
0 answer-key documents in production collection
```

---

## 16. Idempotency Quality

Run ingestion twice.

Expected:

```text
same document count
same node identity
same evidence IDs
same Qdrant point count
no duplicate relationships caused by ingestion
```

Modify one source file.

Expected:

```text
only affected document/chunks are reindexed
```

---

## 17. Failure Handling

### Neo4j unavailable

Retrieval should fail clearly.

Do not fabricate graph context.

### Qdrant unavailable

Exact/structured workflows may continue where possible, but semantic evidence retrieval must report degraded mode.

### Reranker unavailable

Fallback:

```text
use fused first-stage ranking
```

and mark:

```text
reranker_used = false
```

### Missing evidence

Return:

```text
INSUFFICIENT_EVIDENCE
```

rather than constructing a conclusion from missing data.

---

## 18. Observability

Every retrieval request should produce structured telemetry:

```json
{
  "request_id": "...",
  "intent": "requirement_evaluation",
  "patient_id": "SYN-PAT-002",
  "dense_count": 20,
  "sparse_count": 20,
  "fused_count": 32,
  "reranked_count": 10,
  "graph_entities": 12,
  "latency_ms": 0
}
```

Do not log full clinical text by default.

---

## 19. Versioning

Record:

```text
application version
Neo4j version
Qdrant version
embedding model
embedding model version
reranker model
chunker version
retrieval configuration version
```

A benchmark result is meaningful only when the retrieval configuration is reproducible.

---

## 20. Current Technology Baseline

Recommended baseline to benchmark:

```text
Neo4j
Qdrant
FastEmbed
BGE-small dense
sparse retrieval
WRRF
BGE reranker
```

Advanced experiments:

```text
BGE-M3
Qwen3-Embedding-0.6B
MedCPT
Qdrant multivector / late interaction
Neo4j native hybrid capabilities
```

Do not add an advanced component merely because it is newer.

Accept it only when it improves measured retrieval quality, grounding, latency, or maintainability.

---

## 21. Quality Gate Levels

### Gate A — Data correctness

```text
source inventory correct
IDs stable
provenance present
answer keys excluded
```

### Gate B — Graph correctness

```text
constraints pass
required relationships exist
policy versions resolve
case chains resolve
```

### Gate C — Vector correctness

```text
all required chunks indexed
filters work
exact identifiers retrievable
dense retrieval works
sparse retrieval works
```

### Gate D — Hybrid correctness

```text
fusion works
reranking works
graph expansion works
```

### Gate E — Decision correctness

```text
all requirement evaluations match answer keys
```

### Gate F — Grounding

```text
100% provenance
0 fabricated citations
0 invented requirements
```

### Gate G — Performance

```text
p95 targets met or documented
```

No production-style demo should be considered complete below Gate F.

---

## 22. Final Acceptance Checklist

```text
[ ] All supplied source files audited
[ ] Source IDs stable
[ ] Neo4j schema implemented
[ ] Neo4j constraints/indexes implemented
[ ] Policy versions handled
[ ] Requirement nodes canonicalized
[ ] EvidenceChunk bridge implemented
[ ] Typed chunking implemented
[ ] Qdrant collection implemented
[ ] Payload filters implemented
[ ] Dense retrieval implemented
[ ] Sparse retrieval implemented
[ ] WRRF implemented
[ ] Reranker implemented
[ ] Graph expansion implemented
[ ] Requirement evaluator implemented
[ ] Retrieval API implemented
[ ] Scenario 1 passes
[ ] Scenario 2 passes
[ ] Scenario 3 passes
[ ] Cross-patient leakage test passes
[ ] No answer keys in retrieval index
[ ] Provenance coverage = 100%
[ ] Requirement classification = 100%
[ ] Retrieval benchmark meets target
[ ] Latency benchmark recorded
[ ] Model/version configuration recorded
```

---

## 23. Quality Philosophy

The system should be optimized in this order:

```text
Correctness
   ↓
Grounding
   ↓
Recall
   ↓
Ranking quality
   ↓
Latency
   ↓
Complexity
```

Do not sacrifice evidence correctness to make the demo appear more sophisticated.

For AegisHealth-KG, a smaller transparent retrieval system that can prove why it selected evidence is preferable to a larger opaque GraphRAG stack.
