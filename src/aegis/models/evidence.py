from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EvidenceChunk(BaseModel):
    evidence_id: str
    document_id: str
    chunk_id: str
    text_hash: str
    source_type: str
    document_type: Optional[str] = None
    section: Optional[str] = None
    page: Optional[int] = None
    scenario_id: Optional[int] = None
    patient_id: Optional[str] = None
    claim_id: Optional[str] = None
    policy_id: Optional[str] = None
    requirement_id: Optional[str] = None
    cpt_codes: List[str] = Field(default_factory=list)
    icd10_codes: List[str] = Field(default_factory=list)
    denial_codes: List[str] = Field(default_factory=list)
    source_status: str = "synthetic"
    event_date: Optional[str] = None
    text: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class RetrievedEvidence(BaseModel):
    evidence_id: str
    document_id: str
    chunk_id: str
    text: str
    source_type: str
    score: float = 0.0
    rank: int = 0
    matched_by: List[str] = Field(default_factory=list)
    provenance: Dict[str, Any] = Field(default_factory=dict)
