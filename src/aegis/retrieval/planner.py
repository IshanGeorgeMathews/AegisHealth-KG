import re
from typing import Optional

from aegis.models.retrieval import RetrievalPlan


class QueryPlanner:
    def plan(
        self,
        query: str,
        patient_id: Optional[str] = None,
        claim_id: Optional[str] = None,
        policy_id: Optional[str] = None,
    ) -> RetrievalPlan:
        q_lower = query.lower()

        cpt_codes = list(set(re.findall(r"\b\d{5}\b", query)))
        icd10_codes = list(set(re.findall(r"\b[A-TV-Z][0-9][0-9A-Z](?:\.[0-9A-Z]{1,4})?\b", query)))
        denial_codes = list(set(re.findall(r"\b(?:CO|OA|PI|PR)-\d+\b", query, re.IGNORECASE)))
        req_ids = list(set(re.findall(r"\bREQ-[A-Z0-9-]+\b", query)))

        intent = "FULL_APPEAL_ANALYSIS"
        if len(query.strip().split()) <= 4 and (cpt_codes or icd10_codes or denial_codes or req_ids):
            intent = "EXACT_LOOKUP"
        elif "policy" in q_lower and not ("deni" in q_lower or "appeal" in q_lower):
            intent = "POLICY_LOOKUP"
        elif "req-" in q_lower or "satisfy" in q_lower or "requirement" in q_lower:
            intent = "REQUIREMENT_EVALUATION"
        elif "cbt" in q_lower or "efficacy" in q_lower or "literature" in q_lower or "pubmed" in q_lower:
            intent = "LITERATURE_SEARCH"

        return RetrievalPlan(
            intent=intent,
            patient_id=patient_id,
            claim_id=claim_id,
            policy_id=policy_id,
            requirement_ids=req_ids,
            cpt_codes=cpt_codes,
            icd10_codes=icd10_codes,
            denial_codes=denial_codes,
            source_types=["pubmed"] if intent == "LITERATURE_SEARCH" else [],
            use_graph=True,
            use_dense=intent != "EXACT_LOOKUP",
            use_sparse=True,
            use_reranker=intent != "EXACT_LOOKUP",
        )
