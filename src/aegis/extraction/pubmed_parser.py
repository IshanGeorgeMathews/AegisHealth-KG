import json
from pathlib import Path
from typing import List

from aegis.extraction.entities import CanonicalDocument


class PubMedParser:
    def parse_file(self, filepath: str) -> List[CanonicalDocument]:
        path = Path(filepath)
        content = path.read_text(encoding="utf-8")
        data = json.loads(content)

        docs = []
        articles = data if isinstance(data, list) else data.get("articles", [])
        for article in articles:
            pmid = article.get("pmid") or article.get("id") or "UNKNOWN"
            title = article.get("title", "")
            abstract = article.get("abstract", "")
            text = f"Title: {title}\nAbstract: {abstract}"
            if "keywords" in article:
                text += f"\nKeywords: {', '.join(article['keywords'])}"

            content_hash = CanonicalDocument.compute_hash(text)
            doc_id = f"DOC-PUBMED-{pmid}"

            doc = CanonicalDocument(
                document_id=doc_id,
                content_hash=content_hash,
                source_type="pubmed",
                source_path=filepath,
                title=title,
                text=text,
                metadata=article,
            )
            docs.append(doc)

        return docs
