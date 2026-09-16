from typing import Any, Dict, List

from pydantic import BaseModel, Field


class Requirement(BaseModel):
    requirement_id: str
    policy_id: str
    description: str
    requirement_type: str
    rule_parameters: Dict[str, Any] = Field(default_factory=dict)


class RequirementResult(BaseModel):
    requirement_id: str
    status: str
    required: Dict[str, Any] = Field(default_factory=dict)
    actual: Dict[str, Any] = Field(default_factory=dict)
    reason: str
    evidence_ids: List[str] = Field(default_factory=list)
