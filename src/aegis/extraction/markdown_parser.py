import re
from pathlib import Path
from typing import Optional

from aegis.extraction.entities import CanonicalDocument


class MarkdownParser:
    def parse_file(self, filepath: str, source_type: str) -> CanonicalDocument:
        path = Path(filepath)
        content = path.read_text(encoding="utf-8")
        content_hash = CanonicalDocument.compute_hash(content)

        filename = path.name.lower()
        scenario_id: Optional[int] = None
        if "scenario_1" in filename or "s1" in filename:
            scenario_id = 1
        elif "scenario_2" in filename or "s2" in filename:
            scenario_id = 2
        elif "scenario_3" in filename or "s3" in filename:
            scenario_id = 3

        patient_id: Optional[str] = None
        if scenario_id == 1:
            patient_id = "SYN-PAT-001"
        elif scenario_id == 2:
            patient_id = "SYN-PAT-002"
        elif scenario_id == 3:
            patient_id = "SYN-PAT-003"

        policy_id: Optional[str] = None
        m_pol = re.search(r"policy_id:\s*([A-Za-z0-9-]+)", content, re.IGNORECASE)
        if m_pol:
            policy_id = m_pol.group(1).strip()
        elif scenario_id == 1:
            policy_id = "ACME-CGM-2024-001"
        elif scenario_id == 2:
            policy_id = "ACME-MRI-2024-002"
        elif scenario_id == 3:
            policy_id = "ACME-MH-2024-003"

        doc_id = f"DOC-{source_type.upper()}-S{scenario_id}" if scenario_id else f"DOC-{source_type.upper()}-{path.stem}"

        title = path.stem.replace("_", " ").title()
        m_title = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if m_title:
            title = m_title.group(1).strip()

        return CanonicalDocument(
            document_id=doc_id,
            content_hash=content_hash,
            source_type=source_type,
            source_path=filepath,
            scenario_id=scenario_id,
            patient_id=patient_id,
            policy_id=policy_id,
            title=title,
            text=content,
        )
