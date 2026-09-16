from typing import Any, Dict, List

from aegis.graph.repository import GraphRepository
from aegis.models.evidence import RetrievedEvidence


class GraphExpansion:
    def __init__(self, repository: GraphRepository):
        self.repo = repository

    def expand(self, retrieved_items: List[RetrievedEvidence]) -> List[Dict[str, Any]]:
        evidence_ids = [item.evidence_id for item in retrieved_items]
        if not evidence_ids:
            return []

        return self.repo.expand_evidence(evidence_ids)
