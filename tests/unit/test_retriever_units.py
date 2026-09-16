from aegis.extraction.dispatcher import ExtractionDispatcher
from aegis.retrieval.evaluator import RequirementEvaluator
from aegis.retrieval.planner import QueryPlanner
from aegis.vector.chunking import TypedChunkerDispatcher


def test_answer_keys_excluded():
    dispatcher = ExtractionDispatcher()
    docs = dispatcher.process_directory()
    for d in docs:
        assert "answer_keys" not in d.source_path.lower()


def test_query_planner():
    planner = QueryPlanner()
    plan = planner.plan("Why was James's MRI claim denied?", patient_id="SYN-PAT-002")
    assert plan.intent == "FULL_APPEAL_ANALYSIS"
    assert plan.use_dense is True

    plan_exact = planner.plan("CO-197")
    assert plan_exact.intent == "EXACT_LOOKUP"


def test_chunking_provenance():
    docs = ExtractionDispatcher().process_directory()
    chunker = TypedChunkerDispatcher()
    for d in docs[:5]:
        chunks = chunker.chunk_document(d)
        for c in chunks:
            assert c.evidence_id.startswith("EV-")
            assert c.document_id == d.document_id


def test_requirement_evaluator_scenario_2():
    evaluator = RequirementEvaluator()
    results = evaluator.evaluate_scenario_2({
        "prior_auth_submitted": False,
        "pt_duration_days": 39,
        "pt_sessions": 5,
        "exam_days_prior": 0,
    })
    status_dict = {r.requirement_id: r.status for r in results}
    assert status_dict["REQ-PRIOR-AUTH"] == "NOT_SATISFIED"
    assert status_dict["REQ-PHYSIO-6WK"] == "NOT_SATISFIED"
    assert status_dict["REQ-CLINICAL-EXAM"] == "SATISFIED"
