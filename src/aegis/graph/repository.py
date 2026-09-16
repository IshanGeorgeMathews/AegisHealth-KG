from typing import Any, Dict, List, Optional

from aegis.graph import queries
from aegis.graph.client import Neo4jClient


class InMemGraphStore:
    def __init__(self):
        self.patients: Dict[str, Dict[str, Any]] = {}
        self.claims: Dict[str, Dict[str, Any]] = {}
        self.policies: Dict[str, Dict[str, Any]] = {}
        self.requirements: Dict[str, Dict[str, Any]] = {}
        self.evidence_chunks: Dict[str, Dict[str, Any]] = {}
        self.medications: Dict[str, List[Dict[str, Any]]] = {}
        self.therapy_episodes: Dict[str, List[Dict[str, Any]]] = {}
        self.lab_results: Dict[str, List[Dict[str, Any]]] = {}

    def add_patient(self, patient_data: Dict[str, Any]):
        pid = patient_data["patient_id"]
        self.patients[pid] = patient_data

    def add_claim(self, claim_data: Dict[str, Any]):
        cid = claim_data["claim_id"]
        self.claims[cid] = claim_data

    def add_policy(self, policy_data: Dict[str, Any]):
        pol_id = policy_data["policy_id"]
        self.policies[pol_id] = policy_data

    def add_requirement(self, req_data: Dict[str, Any]):
        rid = req_data["requirement_id"]
        self.requirements[rid] = req_data

    def add_evidence_chunk(self, chunk_data: Dict[str, Any]):
        eid = chunk_data["evidence_id"]
        self.evidence_chunks[eid] = chunk_data


class GraphRepository:
    def __init__(self, client: Optional[Neo4jClient] = None):
        self.client = client or Neo4jClient()
        self.in_mem_store = InMemGraphStore()

    def is_connected(self) -> bool:
        return self.client.is_connected()

    def get_patient_case(self, patient_id: str) -> Dict[str, Any]:
        if self.is_connected():
            res = self.client.execute_query(queries.PATIENT_CASE_QUERY, {"patient_id": patient_id})
            if res:
                return res[0]

        p = self.in_mem_store.patients.get(patient_id, {"patient_id": patient_id})
        claims = [c for c in self.in_mem_store.claims.values() if c.get("patient_id") == patient_id]
        policies = list(self.in_mem_store.policies.values())
        meds = self.in_mem_store.medications.get(patient_id, [])
        therapies = self.in_mem_store.therapy_episodes.get(patient_id, [])
        labs = self.in_mem_store.lab_results.get(patient_id, [])

        return {
            "p": p,
            "claims": claims,
            "policies": policies,
            "medications": meds,
            "therapy_episodes": therapies,
            "lab_results": labs,
        }

    def get_claim_context(self, claim_id: str) -> Dict[str, Any]:
        if self.is_connected():
            res = self.client.execute_query(queries.CLAIM_CONTEXT_QUERY, {"claim_id": claim_id})
            if res:
                return res[0]

        c = self.in_mem_store.claims.get(claim_id, {"claim_id": claim_id})
        pid = c.get("patient_id")
        p = self.in_mem_store.patients.get(pid, {}) if pid else {}
        pol_id = c.get("policy_id")
        pol = self.in_mem_store.policies.get(pol_id, {}) if pol_id else {}

        return {
            "c": c,
            "p": p,
            "pol": pol,
            "lines": c.get("lines", []),
            "denials": c.get("denials", []),
        }

    def get_policy_requirements(self, policy_id: str) -> List[Dict[str, Any]]:
        if self.is_connected():
            res = self.client.execute_query(
                queries.POLICY_REQUIREMENTS_QUERY, {"policy_id": policy_id}
            )
            if res and "requirements" in res[0]:
                return res[0]["requirements"]

        return [
            r for r in self.in_mem_store.requirements.values() if r.get("policy_id") == policy_id
        ]

    def expand_evidence(self, evidence_ids: List[str]) -> List[Dict[str, Any]]:
        if not evidence_ids:
            return []

        if self.is_connected():
            return self.client.execute_query(
                queries.EVIDENCE_EXPANSION_QUERY, {"evidence_ids": evidence_ids}
            )

        expansions = []
        for eid in evidence_ids:
            chunk = self.in_mem_store.evidence_chunks.get(eid)
            if chunk:
                req_id = chunk.get("requirement_id")
                req = self.in_mem_store.requirements.get(req_id) if req_id else None
                pol_id = chunk.get("policy_id")
                pol = self.in_mem_store.policies.get(pol_id) if pol_id else None
                expansions.append({
                    "e": chunk,
                    "requirements": [req] if req else [],
                    "policies": [pol] if pol else [],
                })
        return expansions
