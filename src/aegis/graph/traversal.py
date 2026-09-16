from typing import Any, Dict, List, Optional

from aegis.graph.repository import GraphRepository


class GraphTraversal:
    def __init__(self, repository: GraphRepository):
        self.repo = repository

    def traverse_case_context(
        self, patient_id: str, claim_id: Optional[str] = None
    ) -> Dict[str, Any]:
        case_data = self.repo.get_patient_case(patient_id)
        claim_data = self.repo.get_claim_context(claim_id) if claim_id else {}

        return {
            "patient_case": case_data,
            "claim_context": claim_data,
        }

    def traverse_policy_rules(self, policy_id: str) -> List[Dict[str, Any]]:
        return self.repo.get_policy_requirements(policy_id)
