from typing import Optional

from qdrant_client.http import models as rest


def build_qdrant_filter(
    patient_id: Optional[str] = None,
    scenario_id: Optional[int] = None,
    policy_id: Optional[str] = None,
    requirement_id: Optional[str] = None,
    claim_id: Optional[str] = None,
    source_type: Optional[str] = None,
) -> Optional[rest.Filter]:
    must_conditions = []

    if patient_id:
        must_conditions.append(
            rest.FieldCondition(key="patient_id", match=rest.MatchValue(value=patient_id))
        )
    if scenario_id:
        must_conditions.append(
            rest.FieldCondition(key="scenario_id", match=rest.MatchValue(value=scenario_id))
        )
    if policy_id:
        must_conditions.append(
            rest.FieldCondition(key="policy_id", match=rest.MatchValue(value=policy_id))
        )
    if requirement_id:
        must_conditions.append(
            rest.FieldCondition(key="requirement_id", match=rest.MatchValue(value=requirement_id))
        )
    if claim_id:
        must_conditions.append(
            rest.FieldCondition(key="claim_id", match=rest.MatchValue(value=claim_id))
        )
    if source_type:
        must_conditions.append(
            rest.FieldCondition(key="source_type", match=rest.MatchValue(value=source_type))
        )

    if not must_conditions:
        return None

    return rest.Filter(must=must_conditions)
