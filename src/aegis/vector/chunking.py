import hashlib
import re
from typing import List, Protocol

from aegis.extraction.entities import CanonicalDocument
from aegis.models.evidence import EvidenceChunk


class Chunker(Protocol):
    def chunk(self, doc: CanonicalDocument) -> List[EvidenceChunk]:
        ...


def extract_codes_and_reqs(text: str):
    cpt_codes = list(set(re.findall(r"\b\d{5}\b", text)))
    icd10_codes = list(set(re.findall(r"\b[A-TV-Z][0-9][0-9A-Z](?:\.[0-9A-Z]{1,4})?\b", text)))
    denial_codes = list(set(re.findall(r"\b(?:CO|OA|PI|PR)-\d+\b", text, re.IGNORECASE)))
    req_ids = list(set(re.findall(r"\bREQ-[A-Z0-9-]+\b", text)))

    return cpt_codes, icd10_codes, denial_codes, req_ids


class ClinicalRecordChunker:
    def chunk(self, doc: CanonicalDocument) -> List[EvidenceChunk]:
        chunks = []
        text = doc.text

        sections = re.split(r"(?=\n#{1,3}\s+)", text)
        for idx, sec in enumerate(sections):
            sec_text = sec.strip()
            if not sec_text:
                continue

            sec_title_match = re.match(r"#{1,3}\s+(.+)", sec_text)
            section_title = sec_title_match.group(1).strip() if sec_title_match else f"Section-{idx+1}"

            cpt, icd10, denial, reqs = extract_codes_and_reqs(sec_text)
            chunk_id = f"{doc.document_id}::sec-{idx+1}"
            evidence_id = f"EV-{hashlib.sha256(chunk_id.encode('utf-8')).hexdigest()[:12]}"
            text_hash = hashlib.sha256(sec_text.encode("utf-8")).hexdigest()

            chunks.append(
                EvidenceChunk(
                    evidence_id=evidence_id,
                    document_id=doc.document_id,
                    chunk_id=chunk_id,
                    text_hash=text_hash,
                    source_type="clinical_record",
                    document_type="MarkdownClinical",
                    section=section_title,
                    scenario_id=doc.scenario_id,
                    patient_id=doc.patient_id,
                    claim_id=doc.claim_id,
                    policy_id=doc.policy_id,
                    requirement_id=reqs[0] if reqs else None,
                    cpt_codes=cpt,
                    icd10_codes=icd10,
                    denial_codes=denial,
                    text=sec_text,
                )
            )

        return chunks if chunks else FallbackChunker().chunk(doc)


class PolicyChunker:
    def chunk(self, doc: CanonicalDocument) -> List[EvidenceChunk]:
        chunks = []
        text = doc.text

        sections = re.split(r"(?=\n#{1,3}\s+)", text)
        for idx, sec in enumerate(sections):
            sec_text = sec.strip()
            if not sec_text:
                continue

            sec_title_match = re.match(r"#{1,3}\s+(.+)", sec_text)
            section_title = sec_title_match.group(1).strip() if sec_title_match else f"Section-{idx+1}"

            cpt, icd10, denial, reqs = extract_codes_and_reqs(sec_text)
            chunk_id = f"{doc.document_id}::sec-{idx+1}"
            evidence_id = f"EV-{hashlib.sha256(chunk_id.encode('utf-8')).hexdigest()[:12]}"
            text_hash = hashlib.sha256(sec_text.encode("utf-8")).hexdigest()

            chunks.append(
                EvidenceChunk(
                    evidence_id=evidence_id,
                    document_id=doc.document_id,
                    chunk_id=chunk_id,
                    text_hash=text_hash,
                    source_type="policy",
                    document_type="MarkdownPolicy",
                    section=section_title,
                    scenario_id=doc.scenario_id,
                    policy_id=doc.policy_id,
                    requirement_id=reqs[0] if reqs else None,
                    cpt_codes=cpt,
                    icd10_codes=icd10,
                    denial_codes=denial,
                    text=sec_text,
                )
            )

        return chunks if chunks else FallbackChunker().chunk(doc)


class DenialChunker:
    def chunk(self, doc: CanonicalDocument) -> List[EvidenceChunk]:
        chunks = []
        text = doc.text

        page_blocks = re.split(r"--- PAGE (\d+) ---", text)
        if len(page_blocks) > 1:
            for i in range(1, len(page_blocks), 2):
                page_num = int(page_blocks[i])
                page_content = page_blocks[i + 1].strip()
                if not page_content:
                    continue

                cpt, icd10, denial, reqs = extract_codes_and_reqs(page_content)
                chunk_id = f"{doc.document_id}::page-{page_num}"
                evidence_id = f"EV-{hashlib.sha256(chunk_id.encode('utf-8')).hexdigest()[:12]}"
                text_hash = hashlib.sha256(page_content.encode("utf-8")).hexdigest()

                chunks.append(
                    EvidenceChunk(
                        evidence_id=evidence_id,
                        document_id=doc.document_id,
                        chunk_id=chunk_id,
                        text_hash=text_hash,
                        source_type="denial_letter",
                        document_type="PdfDenial",
                        section=f"Page {page_num}",
                        page=page_num,
                        scenario_id=doc.scenario_id,
                        patient_id=doc.patient_id,
                        claim_id=doc.claim_id,
                        policy_id=doc.policy_id,
                        requirement_id=reqs[0] if reqs else None,
                        cpt_codes=cpt,
                        icd10_codes=icd10,
                        denial_codes=denial,
                        text=page_content,
                    )
                )
        else:
            return FallbackChunker().chunk(doc)

        return chunks


class LegalChunker:
    def chunk(self, doc: CanonicalDocument) -> List[EvidenceChunk]:
        chunks = []
        text = doc.text

        sections = re.split(r"(?=\n#{1,3}\s+)", text)
        for idx, sec in enumerate(sections):
            sec_text = sec.strip()
            if not sec_text:
                continue

            sec_title_match = re.match(r"#{1,3}\s+(.+)", sec_text)
            section_title = sec_title_match.group(1).strip() if sec_title_match else f"Section-{idx+1}"

            cpt, icd10, denial, reqs = extract_codes_and_reqs(sec_text)
            chunk_id = f"{doc.document_id}::sec-{idx+1}"
            evidence_id = f"EV-{hashlib.sha256(chunk_id.encode('utf-8')).hexdigest()[:12]}"
            text_hash = hashlib.sha256(sec_text.encode("utf-8")).hexdigest()

            chunks.append(
                EvidenceChunk(
                    evidence_id=evidence_id,
                    document_id=doc.document_id,
                    chunk_id=chunk_id,
                    text_hash=text_hash,
                    source_type="legal_reference",
                    document_type="MarkdownLegal",
                    section=section_title,
                    scenario_id=doc.scenario_id,
                    text=sec_text,
                )
            )

        return chunks if chunks else FallbackChunker().chunk(doc)


class PubMedChunker:
    def chunk(self, doc: CanonicalDocument) -> List[EvidenceChunk]:
        sec_text = doc.text.strip()
        cpt, icd10, denial, reqs = extract_codes_and_reqs(sec_text)
        chunk_id = f"{doc.document_id}::main"
        evidence_id = f"EV-{hashlib.sha256(chunk_id.encode('utf-8')).hexdigest()[:12]}"
        text_hash = hashlib.sha256(sec_text.encode("utf-8")).hexdigest()

        return [
            EvidenceChunk(
                evidence_id=evidence_id,
                document_id=doc.document_id,
                chunk_id=chunk_id,
                text_hash=text_hash,
                source_type="pubmed",
                document_type="PubMedArticle",
                section="Abstract",
                text=sec_text,
            )
        ]


class FallbackChunker:
    def chunk(self, doc: CanonicalDocument) -> List[EvidenceChunk]:
        sec_text = doc.text.strip()
        cpt, icd10, denial, reqs = extract_codes_and_reqs(sec_text)
        chunk_id = f"{doc.document_id}::full"
        evidence_id = f"EV-{hashlib.sha256(chunk_id.encode('utf-8')).hexdigest()[:12]}"
        text_hash = hashlib.sha256(sec_text.encode("utf-8")).hexdigest()

        return [
            EvidenceChunk(
                evidence_id=evidence_id,
                document_id=doc.document_id,
                chunk_id=chunk_id,
                text_hash=text_hash,
                source_type=doc.source_type,
                document_type="Fallback",
                scenario_id=doc.scenario_id,
                patient_id=doc.patient_id,
                claim_id=doc.claim_id,
                policy_id=doc.policy_id,
                requirement_id=reqs[0] if reqs else None,
                cpt_codes=cpt,
                icd10_codes=icd10,
                denial_codes=denial,
                text=sec_text,
            )
        ]


class TypedChunkerDispatcher:
    def __init__(self):
        self.clinical_chunker = ClinicalRecordChunker()
        self.policy_chunker = PolicyChunker()
        self.denial_chunker = DenialChunker()
        self.legal_chunker = LegalChunker()
        self.pubmed_chunker = PubMedChunker()
        self.fallback_chunker = FallbackChunker()

    def chunk_document(self, doc: CanonicalDocument) -> List[EvidenceChunk]:
        st = doc.source_type
        if st == "clinical_record":
            return self.clinical_chunker.chunk(doc)
        elif st in ("policy", "prior_auth"):
            return self.policy_chunker.chunk(doc)
        elif st == "denial_letter":
            return self.denial_chunker.chunk(doc)
        elif st == "legal_reference":
            return self.legal_chunker.chunk(doc)
        elif st == "pubmed":
            return self.pubmed_chunker.chunk(doc)
        else:
            return self.fallback_chunker.chunk(doc)
