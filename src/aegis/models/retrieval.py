from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from aegis.models.evidence import RetrievedEvidence
from aegis.models.requirements import RequirementResult


class RetrievalPlan(BaseModel):
    intent: str
    patient_id: Optional[str] = None
    claim_id: Optional[str] = None
    policy_id: Optional[str] = None
    requirement_ids: List[str] = Field(default_factory=list)
    cpt_codes: List[str] = Field(default_factory=list)
    icd10_codes: List[str] = Field(default_factory=list)
    denial_codes: List[str] = Field(default_factory=list)
    source_types: List[str] = Field(default_factory=list)
    use_graph: bool = True
    use_dense: bool = True
    use_sparse: bool = True
    use_reranker: bool = True


class EvidencePack(BaseModel):
    facts: List[Dict[str, Any]] = Field(default_factory=list)
    requirements: List[RequirementResult] = Field(default_factory=list)
    evidence: List[RetrievedEvidence] = Field(default_factory=list)
    graph_context: List[Dict[str, Any]] = Field(default_factory=list)
    provenance: List[Dict[str, Any]] = Field(default_factory=list)
    retrieval_metadata: Dict[str, Any] = Field(default_factory=dict)


class RetrievalRequest(BaseModel):
    query: str
    patient_id: Optional[str] = None
    claim_id: Optional[str] = None
    policy_id: Optional[str] = None


class RetrievalResult(BaseModel):
    evidence_pack: EvidencePack
    execution_time_ms: float = 0.0
