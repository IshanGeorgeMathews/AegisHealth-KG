import hashlib
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class CanonicalDocument(BaseModel):
    document_id: str
    document_version: str = "1.0"
    content_hash: str
    source_type: str
    source_path: str
    source_status: str = "synthetic"
    scenario_id: Optional[int] = None
    patient_id: Optional[str] = None
    claim_id: Optional[str] = None
    policy_id: Optional[str] = None
    title: Optional[str] = None
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @staticmethod
    def compute_hash(content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
