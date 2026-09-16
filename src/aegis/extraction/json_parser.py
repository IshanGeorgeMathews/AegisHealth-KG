import json
from pathlib import Path
from typing import List, Optional, Tuple

from aegis.extraction.entities import CanonicalDocument
from aegis.models.domain import (
    Claim,
    ClaimLine,
    Denial,
    InsurancePlan,
    LabResult,
    Medication,
    Patient,
    Provider,
)


class JsonPatientParser:
    def parse_file(self, filepath: str) -> Tuple[CanonicalDocument, Patient, Optional[Provider], Optional[InsurancePlan], List[Medication], List[LabResult], Optional[Claim]]:
        path = Path(filepath)
        content = path.read_text(encoding="utf-8")
        data = json.loads(content)

        patient_id = data.get("patient_id")
        scenario_id = data.get("scenario")
        demo = data.get("demographics", {})
        prov_data = data.get("provider")
        ins_data = data.get("insurance", {})
        clin_hist = data.get("clinical_history", {})
        claim_data = data.get("claim")

        doc_id = f"DOC-PATIENT-S{scenario_id}" if scenario_id else f"DOC-PATIENT-{patient_id}"
        content_hash = CanonicalDocument.compute_hash(content)

        doc = CanonicalDocument(
            document_id=doc_id,
            content_hash=content_hash,
            source_type="patient",
            source_path=filepath,
            scenario_id=scenario_id,
            patient_id=patient_id,
            claim_id=claim_data.get("claim_id") if claim_data else None,
            policy_id=ins_data.get("policy_id"),
            title=f"Patient Record - {demo.get('first_name', '')} {demo.get('last_name', '')}",
            text=content,
            metadata=data,
        )

        patient = Patient(
            patient_id=patient_id,
            first_name=demo.get("first_name"),
            last_name=demo.get("last_name"),
            date_of_birth=demo.get("date_of_birth"),
            gender=demo.get("gender"),
            member_id=demo.get("member_id"),
            insurance_policy_id=ins_data.get("policy_id"),
            metadata={"scenario": scenario_id, "group_number": demo.get("group_number")},
        )

        provider = None
        if prov_data:
            provider = Provider(
                provider_id=f"PROV-{prov_data.get('npi', 'UNKNOWN')}",
                npi=prov_data.get("npi"),
                name=prov_data.get("name"),
                specialty=prov_data.get("specialty"),
            )

        insurance = None
        if ins_data.get("policy_id"):
            insurance = InsurancePlan(
                plan_id=ins_data.get("policy_id"),
                plan_name=ins_data.get("plan_name", "AcmeCare"),
                payer_id=f"PAYER-{ins_data.get('payer', 'ACME').upper().replace(' ', '-')}",
                group_number=demo.get("group_number"),
            )

        medications = []
        for i, m in enumerate(clin_hist.get("medications", [])):
            med = Medication(
                medication_id=f"MED-{patient_id}-{i+1}",
                patient_id=patient_id,
                drug_name=m.get("name"),
                start_date=m.get("start_date"),
                end_date=m.get("end_date"),
                duration_days=m.get("duration_days"),
                outcome=m.get("outcome"),
            )
            medications.append(med)

        lab_results = []
        for i, l in enumerate(clin_hist.get("lab_results", [])):
            lab = LabResult(
                lab_id=f"LAB-{patient_id}-{i+1}",
                patient_id=patient_id,
                test_name=l.get("test"),
                test_date=l.get("date"),
                result_value=l.get("value"),
                reference_range=l.get("context"),
            )
            lab_results.append(lab)

        claim = None
        if claim_data:
            claim = Claim(
                claim_id=claim_data.get("claim_id"),
                patient_id=patient_id,
                claim_date=claim_data.get("date_of_service"),
                policy_id=ins_data.get("policy_id"),
            )

        return doc, patient, provider, insurance, medications, lab_results, claim


class JsonEobParser:
    def parse_file(self, filepath: str) -> Tuple[CanonicalDocument, Claim, Denial]:
        path = Path(filepath)
        content = path.read_text(encoding="utf-8")
        data = json.loads(content)

        claim_data = data.get("claim", {})
        patient_data = data.get("member", {})

        scenario_id = data.get("scenario")
        if not scenario_id:
            filename = path.name.lower()
            if "scenario_1" in filename or "s1" in filename:
                scenario_id = 1
            elif "scenario_2" in filename or "s2" in filename:
                scenario_id = 2
            elif "scenario_3" in filename or "s3" in filename:
                scenario_id = 3

        patient_id = claim_data.get("patient_id") or patient_data.get("patient_id")
        if not patient_id and scenario_id:
            patient_id = f"SYN-PAT-{scenario_id:03d}"

        claim_id = claim_data.get("claim_id") or claim_data.get("claim_number") or f"CLM-UNKNOWN-{scenario_id}"
        policy_id = claim_data.get("policy_id") or data.get("determination", {}).get("policy_reference")

        determination = data.get("determination", {})

        doc_id = f"DOC-EOB-S{scenario_id}" if scenario_id else f"DOC-EOB-{claim_id}"
        content_hash = CanonicalDocument.compute_hash(content)

        doc = CanonicalDocument(
            document_id=doc_id,
            content_hash=content_hash,
            source_type="eob",
            source_path=filepath,
            scenario_id=scenario_id,
            patient_id=patient_id,
            claim_id=claim_id,
            policy_id=policy_id,
            title=f"EOB - Claim {claim_id}",
            text=content,
            metadata=data,
        )

        lines = []
        for line_data in data.get("claim_lines", []) or claim_data.get("lines", []):
            lines.append(
                ClaimLine(
                    line_number=line_data.get("line_number", 1),
                    cpt_code=line_data.get("cpt_code", ""),
                    icd10_codes=line_data.get("icd10_codes", []),
                    service_date=claim_data.get("date_of_service"),
                    billed_amount=line_data.get("billed_amount"),
                    allowed_amount=line_data.get("allowed_amount"),
                )
            )

        denial_code = determination.get("denial_reason_code") or determination.get("denial_code", "UNKNOWN")
        denial = Denial(
            denial_id=f"DENIAL-{claim_id}",
            claim_id=claim_id,
            denial_code=denial_code,
            category=determination.get("denial_category"),
            reason=determination.get("denial_narrative") or determination.get("denial_reason", ""),
        )

        claim = Claim(
            claim_id=claim_id,
            patient_id=patient_id or "UNKNOWN",
            claim_date=claim_data.get("date_of_service", ""),
            policy_id=policy_id,
            lines=lines,
            denials=[denial],
        )

        return doc, claim, denial
