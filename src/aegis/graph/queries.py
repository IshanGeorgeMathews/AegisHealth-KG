PATIENT_CASE_QUERY = """
MATCH (p:Patient {patient_id: $patient_id})
OPTIONAL MATCH (p)-[:HAS_CLAIM]->(c:Claim)
OPTIONAL MATCH (c)-[:HAS_DENIAL]->(d:Denial)
OPTIONAL MATCH (c)-[:HAS_POLICY]->(pol:Policy)
OPTIONAL MATCH (p)-[:UNDERWENT]->(te:TherapyEpisode)
OPTIONAL MATCH (p)-[:TAKES]->(m:Medication)
OPTIONAL MATCH (p)-[:HAS_LAB_RESULT]->(l:LabResult)
OPTIONAL MATCH (p)-[:HAS_CLINICAL_EVENT]->(ce:ClinicalEvent)
RETURN p, collect(distinct c) as claims, collect(distinct d) as denials,
       collect(distinct pol) as policies, collect(distinct te) as therapy_episodes,
       collect(distinct m) as medications, collect(distinct l) as lab_results,
       collect(distinct ce) as clinical_events
"""

CLAIM_CONTEXT_QUERY = """
MATCH (c:Claim {claim_id: $claim_id})
OPTIONAL MATCH (c)<-[:HAS_CLAIM]-(p:Patient)
OPTIONAL MATCH (c)-[:HAS_DENIAL]->(d:Denial)
OPTIONAL MATCH (d)-[:HAS_DENIAL_CODE]->(dc:DenialCode)
OPTIONAL MATCH (c)-[:HAS_LINE]->(cl:ClaimLine)
OPTIONAL MATCH (cl)-[:FOR_PROCEDURE]->(proc:Procedure)-[:HAS_CPT_CODE]->(cpt:CPTCode)
OPTIONAL MATCH (cl)-[:HAS_DIAGNOSIS]->(diag:Diagnosis)-[:HAS_ICD10_CODE]->(icd:ICD10Code)
OPTIONAL MATCH (c)-[:HAS_POLICY]->(pol:Policy)
RETURN c, p, d, dc, collect(distinct cl) as lines, collect(distinct proc) as procedures,
       collect(distinct diag) as diagnoses, pol
"""

POLICY_REQUIREMENTS_QUERY = """
MATCH (pol:Policy {policy_id: $policy_id})
OPTIONAL MATCH (pol)-[:HAS_REQUIREMENT]->(r:Requirement)
OPTIONAL MATCH (pol)-[:REFERENCES]->(l:LegalReference)
RETURN pol, collect(distinct r) as requirements, collect(distinct l) as legal_references
"""

EVIDENCE_EXPANSION_QUERY = """
MATCH (e:EvidenceChunk) WHERE e.evidence_id IN $evidence_ids
OPTIONAL MATCH (r:Requirement)-[:SUPPORTED_BY]->(e)
OPTIONAL MATCH (pol:Policy)-[:SUPPORTED_BY]->(e)
OPTIONAL MATCH (ce:ClinicalEvent)-[:SUPPORTED_BY]->(e)
OPTIONAL MATCH (te:TherapyEpisode)-[:SUPPORTED_BY]->(e)
OPTIONAL MATCH (d:Denial)-[:SUPPORTED_BY]->(e)
OPTIONAL MATCH (p:Patient)-[:UNDERWENT|HAS_CLINICAL_EVENT]->(x) WHERE x = te OR x = ce
RETURN e, collect(distinct r) as requirements, collect(distinct pol) as policies,
       collect(distinct ce) as clinical_events, collect(distinct te) as therapy_episodes,
       collect(distinct d) as denials, collect(distinct p) as patients
"""
