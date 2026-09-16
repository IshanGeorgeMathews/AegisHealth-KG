from aegis.evaluation.golden_set import load_answer_keys
from aegis.evaluation.metrics import mrr_at_k, ndcg_at_k, precision_at_k, recall_at_k
from aegis.models import RetrievalRequest
from aegis.retrieval.service import RetrievalService


class BenchmarkHarness:
    def __init__(self, service: RetrievalService = None):
        self.service = service or RetrievalService()

    def run_benchmark(self) -> dict[str, float]:
        answer_keys = load_answer_keys()
        queries = [
            ("Why was Maria's CGM claim denied?", "SYN-PAT-001", 1),
            ("Why was James's MRI claim denied?", "SYN-PAT-002", 2),
            ("What evidence supports Aisha's psychotherapy medical necessity?", "SYN-PAT-003", 3),
        ]

        recalls, mrrs, ndcgs, precisions = [], [], [], []

        for q, pid, scenario in queries:
            req = RetrievalRequest(query=q, patient_id=pid)
            res = self.service.retrieve(req)
            retrieved_chunks = res.evidence_pack.evidence

            ak = answer_keys.get(scenario, {})
            expected_req_ids = [
                r.get("id") for r in ak.get("expected_requirements", []) if r.get("id")
            ]
            expected_policy_id = ak.get("expected_policy_id")

            gold_matched_indices = []
            for item in retrieved_chunks:
                txt = item.text + " " + str(item.provenance)
                if (expected_policy_id and expected_policy_id in txt) or any(
                    rid in txt for rid in expected_req_ids
                ):
                    gold_matched_indices.append(item.evidence_id)

            retrieved_ids = [e.evidence_id for e in retrieved_chunks]
            gold_ids = set(gold_matched_indices)

            recalls.append(recall_at_k(retrieved_ids, gold_ids, 10))
            mrrs.append(mrr_at_k(retrieved_ids, gold_ids, 10))
            ndcgs.append(ndcg_at_k(retrieved_ids, gold_ids, 10))
            precisions.append(precision_at_k(retrieved_ids, gold_ids, 5))

        return {
            "Recall@10": sum(recalls) / len(recalls) if recalls else 0.0,
            "MRR@10": sum(mrrs) / len(mrrs) if mrrs else 0.0,
            "nDCG@10": sum(ndcgs) / len(ndcgs) if ndcgs else 0.0,
            "Precision@5": sum(precisions) / len(precisions) if precisions else 0.0,
        }
