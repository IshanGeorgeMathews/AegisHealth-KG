from typing import List, Optional

from aegis.config.settings import get_settings
from aegis.models.evidence import RetrievedEvidence

try:
    from sentence_transformers import CrossEncoder
except ImportError:
    CrossEncoder = None


class CrossEncoderReranker:
    def __init__(self, model_name: Optional[str] = None):
        get_settings()
        self.model_name = model_name or "cross-encoder/ms-marco-MiniLM-L-6-v2"
        self._model = None

    @property
    def model(self):
        if self._model is None and CrossEncoder is not None:
            try:
                self._model = CrossEncoder(self.model_name)
            except Exception:
                self._model = False
        return self._model

    def rerank(
        self,
        query: str,
        candidates: List[RetrievedEvidence],
        top_k: Optional[int] = None,
    ) -> List[RetrievedEvidence]:
        if not candidates:
            return []

        limit = top_k or get_settings().rerank_top_k

        model = self.model
        if model:
            pairs = [(query, cand.text) for cand in candidates]
            scores = model.predict(pairs)
            scored = list(zip(scores, candidates))
            scored.sort(key=lambda x: float(x[0]), reverse=True)

            reranked = []
            for rank, (score, cand) in enumerate(scored[:limit], start=1):
                cand.score = float(score)
                cand.rank = rank
                reranked.append(cand)
            return reranked

        # Fallback to lexical + fusion score if neural cross encoder is unavailable
        query_words = set(query.lower().split())
        scored_candidates = []
        for cand in candidates:
            cand_words = set(cand.text.lower().split())
            overlap = len(query_words.intersection(cand_words))
            overlap_score = overlap / max(len(query_words), 1)
            rerank_score = cand.score + 0.5 * overlap_score
            scored_candidates.append((rerank_score, cand))

        scored_candidates.sort(key=lambda x: x[0], reverse=True)

        reranked = []
        for rank, (score, cand) in enumerate(scored_candidates[:limit], start=1):
            cand.score = float(score)
            cand.rank = rank
            reranked.append(cand)

        return reranked
