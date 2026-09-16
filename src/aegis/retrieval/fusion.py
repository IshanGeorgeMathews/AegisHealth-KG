from typing import Dict, List

from aegis.config.settings import get_settings
from aegis.models.evidence import RetrievedEvidence


def wrf(rank: int, weight: float, k: int = 60) -> float:
    return weight / (k + rank)


class CandidateFusion:
    def __init__(
        self,
        dense_weight: float = None,
        sparse_weight: float = None,
        graph_weight: float = None,
        k: int = None,
    ):
        settings = get_settings()
        self.dense_weight = dense_weight if dense_weight is not None else settings.dense_weight
        self.sparse_weight = sparse_weight if sparse_weight is not None else settings.sparse_weight
        self.graph_weight = graph_weight if graph_weight is not None else settings.graph_weight
        self.k = k if k is not None else settings.rrf_k

    def fuse(
        self,
        dense_candidates: List[RetrievedEvidence],
        sparse_candidates: List[RetrievedEvidence],
        graph_candidates: List[RetrievedEvidence] = None,
        limit: int = 50,
    ) -> List[RetrievedEvidence]:
        fused_map: Dict[str, RetrievedEvidence] = {}
        scores_map: Dict[str, float] = {}

        for cand in dense_candidates:
            eid = cand.evidence_id
            fused_map[eid] = cand
            score = wrf(cand.rank, self.dense_weight, self.k)
            scores_map[eid] = scores_map.get(eid, 0.0) + score

        for cand in sparse_candidates:
            eid = cand.evidence_id
            if eid in fused_map:
                if "sparse" not in fused_map[eid].matched_by:
                    fused_map[eid].matched_by.append("sparse")
            else:
                fused_map[eid] = cand

            score = wrf(cand.rank, self.sparse_weight, self.k)
            scores_map[eid] = scores_map.get(eid, 0.0) + score

        if graph_candidates:
            for cand in graph_candidates:
                eid = cand.evidence_id
                if eid in fused_map:
                    if "graph" not in fused_map[eid].matched_by:
                        fused_map[eid].matched_by.append("graph")
                else:
                    fused_map[eid] = cand

                score = wrf(cand.rank, self.graph_weight, self.k)
                scores_map[eid] = scores_map.get(eid, 0.0) + score

        sorted_eids = sorted(scores_map.keys(), key=lambda x: scores_map[x], reverse=True)

        final_candidates = []
        for rank, eid in enumerate(sorted_eids[:limit], start=1):
            item = fused_map[eid]
            item.score = scores_map[eid]
            item.rank = rank
            final_candidates.append(item)

        return final_candidates
