from pathlib import Path
from typing import Optional

from pypdf import PdfReader

from aegis.extraction.entities import CanonicalDocument


class PdfDenialParser:
    def parse_file(self, filepath: str) -> CanonicalDocument:
        path = Path(filepath)
        reader = PdfReader(filepath)
        pages_text = []
        for i, page in enumerate(reader.pages):
            txt = page.extract_text() or ""
            pages_text.append(f"--- PAGE {i+1} ---\n{txt}")

        full_text = "\n\n".join(pages_text)
        content_hash = CanonicalDocument.compute_hash(full_text)

        filename = path.name.lower()
        scenario_id: Optional[int] = None
        patient_id: Optional[str] = None
        claim_id: Optional[str] = None
        policy_id: Optional[str] = None

        if "scenario_1" in filename or "s1" in filename:
            scenario_id = 1
            patient_id = "SYN-PAT-001"
            claim_id = "CLM-2024-0815-001"
            policy_id = "ACME-CGM-2024-001"
        elif "scenario_2" in filename or "s2" in filename:
            scenario_id = 2
            patient_id = "SYN-PAT-002"
            claim_id = "CLM-2024-0715-002"
            policy_id = "ACME-MRI-2024-002"
        elif "scenario_3" in filename or "s3" in filename:
            scenario_id = 3
            patient_id = "SYN-PAT-003"
            claim_id = "CLM-2024-0901-003"
            policy_id = "ACME-MH-2024-003"

        doc_id = f"DOC-DENIAL-S{scenario_id}" if scenario_id else f"DOC-DENIAL-{path.stem}"

        return CanonicalDocument(
            document_id=doc_id,
            content_hash=content_hash,
            source_type="denial_letter",
            source_path=filepath,
            scenario_id=scenario_id,
            patient_id=patient_id,
            claim_id=claim_id,
            policy_id=policy_id,
            title=f"Denial Letter - Scenario {scenario_id}",
            text=full_text,
            metadata={"pages_count": len(reader.pages)},
        )
