import math
from typing import List, Set


def recall_at_k(retrieved_ids: List[str], gold_ids: Set[str], k: int) -> float:
    if not gold_ids:
        return 1.0
    top_k = set(retrieved_ids[:k])
    hits = len(top_k.intersection(gold_ids))
    return hits / len(gold_ids)


def precision_at_k(retrieved_ids: List[str], gold_ids: Set[str], k: int) -> float:
    if k == 0:
        return 0.0
    top_k = retrieved_ids[:k]
    hits = sum(1 for item in top_k if item in gold_ids)
    return hits / k


def mrr_at_k(retrieved_ids: List[str], gold_ids: Set[str], k: int) -> float:
    for rank, item in enumerate(retrieved_ids[:k], start=1):
        if item in gold_ids:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(retrieved_ids: List[str], gold_ids: Set[str], k: int) -> float:
    if not gold_ids:
        return 1.0

    dcg = 0.0
    for rank, item in enumerate(retrieved_ids[:k], start=1):
        if item in gold_ids:
            dcg += 1.0 / math.log2(rank + 1)

    idcg = sum(1.0 / math.log2(r + 1) for r in range(1, min(len(gold_ids), k) + 1))
    return dcg / idcg if idcg > 0 else 0.0
