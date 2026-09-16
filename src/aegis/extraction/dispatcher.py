import os
from pathlib import Path
from typing import List

from aegis.extraction.entities import CanonicalDocument
from aegis.extraction.json_parser import JsonEobParser, JsonPatientParser
from aegis.extraction.markdown_parser import MarkdownParser
from aegis.extraction.pdf_parser import PdfDenialParser
from aegis.extraction.pubmed_parser import PubMedParser


class ExtractionDispatcher:
    def __init__(self, root_data_dir: str = "data/synthetic"):
        self.root_data_dir = Path(root_data_dir)
        self.patient_parser = JsonPatientParser()
        self.eob_parser = JsonEobParser()
        self.markdown_parser = MarkdownParser()
        self.pdf_parser = PdfDenialParser()
        self.pubmed_parser = PubMedParser()

    def process_directory(self) -> List[CanonicalDocument]:
        canonical_docs = []

        for root, dirs, files in os.walk(self.root_data_dir):
            rel_root = Path(root).relative_to(self.root_data_dir)
            if "answer_keys" in rel_root.parts:
                continue

            for file in files:
                file_path = Path(root) / file
                str_path = str(file_path)

                if "answer_keys" in file_path.parts:
                    continue

                if file.endswith(".json"):
                    if "patients" in str_path:
                        doc, _, _, _, _, _, _ = self.patient_parser.parse_file(str_path)
                        canonical_docs.append(doc)
                    elif "eob" in str_path:
                        doc, _, _ = self.eob_parser.parse_file(str_path)
                        canonical_docs.append(doc)
                    elif "pubmed_articles" in str_path:
                        docs = self.pubmed_parser.parse_file(str_path)
                        canonical_docs.extend(docs)
                elif file.endswith(".md"):
                    if "clinical_records" in str_path:
                        doc = self.markdown_parser.parse_file(str_path, "clinical_record")
                        canonical_docs.append(doc)
                    elif "policies" in str_path:
                        doc = self.markdown_parser.parse_file(str_path, "policy")
                        canonical_docs.append(doc)
                    elif "prior_auth" in str_path:
                        doc = self.markdown_parser.parse_file(str_path, "prior_auth")
                        canonical_docs.append(doc)
                    elif "legal_references" in str_path:
                        doc = self.markdown_parser.parse_file(str_path, "legal_reference")
                        canonical_docs.append(doc)
                elif file.endswith(".pdf"):
                    if "denial_letters" in str_path:
                        doc = self.pdf_parser.parse_file(str_path)
                        canonical_docs.append(doc)

        return canonical_docs
