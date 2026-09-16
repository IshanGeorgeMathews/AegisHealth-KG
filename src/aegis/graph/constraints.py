from aegis.graph.client import Neo4jClient

CONSTRAINTS = [
    "CREATE CONSTRAINT patient_id_unique IF NOT EXISTS FOR (p:Patient) REQUIRE p.patient_id IS UNIQUE;",
    "CREATE CONSTRAINT claim_id_unique IF NOT EXISTS FOR (c:Claim) REQUIRE c.claim_id IS UNIQUE;",
    "CREATE CONSTRAINT policy_id_unique IF NOT EXISTS FOR (p:Policy) REQUIRE p.policy_id IS UNIQUE;",
    "CREATE CONSTRAINT requirement_id_unique IF NOT EXISTS FOR (r:Requirement) REQUIRE r.requirement_id IS UNIQUE;",
    "CREATE CONSTRAINT evidence_id_unique IF NOT EXISTS FOR (e:EvidenceChunk) REQUIRE e.evidence_id IS UNIQUE;",
    "CREATE CONSTRAINT document_id_unique IF NOT EXISTS FOR (d:Document) REQUIRE d.document_id IS UNIQUE;",
    "CREATE CONSTRAINT cpt_code_unique IF NOT EXISTS FOR (c:CPTCode) REQUIRE c.code IS UNIQUE;",
    "CREATE CONSTRAINT icd10_code_unique IF NOT EXISTS FOR (i:ICD10Code) REQUIRE i.code IS UNIQUE;",
    "CREATE CONSTRAINT denial_code_unique IF NOT EXISTS FOR (d:DenialCode) REQUIRE d.code IS UNIQUE;",
]

INDEXES = [
    "CREATE INDEX patient_member_id_idx IF NOT EXISTS FOR (p:Patient) ON (p.member_id);",
    "CREATE INDEX claim_patient_id_idx IF NOT EXISTS FOR (c:Claim) ON (c.patient_id);",
    "CREATE INDEX policy_version_idx IF NOT EXISTS FOR (p:Policy) ON (p.version);",
    "CREATE INDEX evidence_patient_id_idx IF NOT EXISTS FOR (e:EvidenceChunk) ON (e.patient_id);",
    "CREATE INDEX evidence_policy_id_idx IF NOT EXISTS FOR (e:EvidenceChunk) ON (e.policy_id);",
]


def apply_constraints_and_indexes(client: Neo4jClient):
    if not client.is_connected():
        return False

    for stmt in CONSTRAINTS + INDEXES:
        try:
            client.execute_query(stmt)
        except Exception as e:
            print(f"Warning executing schema statement: {e}")
    return True
