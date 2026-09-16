import pytest

from aegis.models import RetrievalRequest
from aegis.retrieval.service import RetrievalService


@pytest.fixture(scope="module")
def retrieval_service():
    return RetrievalService()


def test_scenario_1_cgm(retrieval_service):
    req = RetrievalRequest(
        query="Did Maria complete step therapy for CGM?", patient_id="SYN-PAT-001"
    )
    res = retrieval_service.retrieve(req)
    reqs = res.evidence_pack.requirements
    assert len(reqs) == 3
    assert all(r.status == "SATISFIED" for r in reqs)


def test_scenario_2_mri(retrieval_service):
    req = RetrievalRequest(
        query="Why was James's MRI claim denied?", patient_id="SYN-PAT-002"
    )
    res = retrieval_service.retrieve(req)
    reqs = res.evidence_pack.requirements
    status_map = {r.requirement_id: r.status for r in reqs}
    assert status_map["REQ-PRIOR-AUTH"] == "NOT_SATISFIED"
    assert status_map["REQ-PHYSIO-6WK"] == "NOT_SATISFIED"
    assert status_map["REQ-CLINICAL-EXAM"] == "SATISFIED"


def test_scenario_3_psychotherapy(retrieval_service):
    req = RetrievalRequest(
        query="Does Aisha meet medical necessity for session 21?", patient_id="SYN-PAT-003"
    )
    res = retrieval_service.retrieve(req)
    reqs = res.evidence_pack.requirements
    assert len(reqs) == 2
    assert all(r.status == "SATISFIED" for r in reqs)


def test_cross_patient_isolation(retrieval_service):
    req = RetrievalRequest(query="Show clinical evidence", patient_id="SYN-PAT-002")
    res = retrieval_service.retrieve(req)
    for item in res.evidence_pack.evidence:
        pid = item.provenance.get("patient_id")
        if pid:
            assert pid == "SYN-PAT-002"
