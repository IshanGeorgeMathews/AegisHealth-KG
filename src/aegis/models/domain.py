from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Patient(BaseModel):
    patient_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    member_id: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    contact_info: Optional[Dict[str, Any]] = None
    insurance_policy_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Provider(BaseModel):
    provider_id: str
    npi: Optional[str] = None
    name: str
    specialty: Optional[str] = None
    network_status: Optional[str] = None


class Payer(BaseModel):
    payer_id: str
    name: str


class InsurancePlan(BaseModel):
    plan_id: str
    plan_name: str
    payer_id: str
    group_number: Optional[str] = None


class Procedure(BaseModel):
    procedure_id: str
    cpt_code: str
    description: Optional[str] = None


class Diagnosis(BaseModel):
    diagnosis_id: str
    icd10_code: str
    description: Optional[str] = None


class Medication(BaseModel):
    medication_id: str
    patient_id: str
    drug_name: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration_days: Optional[int] = None
    outcome: Optional[str] = None


class LabResult(BaseModel):
    lab_id: str
    patient_id: str
    test_name: str
    test_date: Optional[str] = None
    result_value: Optional[str] = None
    reference_range: Optional[str] = None


class ClinicalEvent(BaseModel):
    event_id: str
    patient_id: str
    event_type: str
    event_date: Optional[str] = None
    description: str
    supporting_evidence_ids: List[str] = Field(default_factory=list)


class TherapyEpisode(BaseModel):
    episode_id: str
    patient_id: str
    therapy_type: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration_days: Optional[int] = None
    session_count: Optional[int] = None
    outcome: Optional[str] = None
    supporting_evidence_ids: List[str] = Field(default_factory=list)


class ClaimLine(BaseModel):
    line_number: int
    cpt_code: str
    icd10_codes: List[str] = Field(default_factory=list)
    service_date: Optional[str] = None
    billed_amount: Optional[float] = None
    allowed_amount: Optional[float] = None


class Denial(BaseModel):
    denial_id: str
    claim_id: str
    denial_code: str
    category: Optional[str] = None
    reason: str
    supporting_evidence_ids: List[str] = Field(default_factory=list)


class Claim(BaseModel):
    claim_id: str
    patient_id: str
    claim_date: str
    policy_id: Optional[str] = None
    lines: List[ClaimLine] = Field(default_factory=list)
    denials: List[Denial] = Field(default_factory=list)


class Policy(BaseModel):
    policy_id: str
    title: str
    version: str
    effective_from: str
    effective_to: Optional[str] = None
    covered_procedures: List[str] = Field(default_factory=list)
    covered_diagnoses: List[str] = Field(default_factory=list)
    requirement_ids: List[str] = Field(default_factory=list)


class LegalReference(BaseModel):
    legal_ref_id: str
    title: str
    citation: str
    text: str
    source_status: str = "synthetic"
