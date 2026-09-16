from typing import List, Optional

from qdrant_client.http import models as rest

from aegis.config.settings import get_settings
from aegis.models.evidence import RetrievedEvidence
from aegis.vector.client import VectorClient
from aegis.vector.embeddings import EmbeddingService


class VectorSearcher:
    def __init__(self, client_wrapper: VectorClient, embedding_service: EmbeddingService):
        self.client_wrapper = client_wrapper
        self.embedding_service = embedding_service
        self.settings = get_settings()

    def search_dense(
        self,
        query: str,
        filters: Optional[rest.Filter] = None,
        top_k: Optional[int] = None,
    ) -> List[RetrievedEvidence]:
        limit = top_k or self.settings.dense_top_k
        query_vector = self.embedding_service.embed_query(query)
        client = self.client_wrapper.get_client()

        response = client.query_points(
            collection_name=self.settings.qdrant_collection,
            query=query_vector,
            using="dense",
            query_filter=filters,
            limit=limit,
        )

        retrieved = []
        for rank, hit in enumerate(response.points, start=1):
            p = hit.payload or {}
            retrieved.append(
                RetrievedEvidence(
                    evidence_id=p.get("evidence_id", f"EV-{hit.id}"),
                    document_id=p.get("document_id", ""),
                    chunk_id=p.get("chunk_id", ""),
                    text=p.get("text", ""),
                    source_type=p.get("source_type", "unknown"),
                    score=float(hit.score),
                    rank=rank,
                    matched_by=["dense"],
                    provenance=p,
                )
            )
        return retrieved

    def search_sparse(
        self,
        query: str,
        filters: Optional[rest.Filter] = None,
        top_k: Optional[int] = None,
    ) -> List[RetrievedEvidence]:
        limit = top_k or self.settings.sparse_top_k
        sp_vec = self.embedding_service.embed_sparse_query(query)
        client = self.client_wrapper.get_client()

        sparse_query = rest.SparseVector(
            indices=sp_vec.indices.tolist(),
            values=sp_vec.values.tolist(),
        )

        response = client.query_points(
            collection_name=self.settings.qdrant_collection,
            query=sparse_query,
            using="sparse",
            query_filter=filters,
            limit=limit,
        )

        retrieved = []
        for rank, hit in enumerate(response.points, start=1):
            p = hit.payload or {}
            retrieved.append(
                RetrievedEvidence(
                    evidence_id=p.get("evidence_id", f"EV-{hit.id}"),
                    document_id=p.get("document_id", ""),
                    chunk_id=p.get("chunk_id", ""),
                    text=p.get("text", ""),
                    source_type=p.get("source_type", "unknown"),
                    score=float(hit.score),
                    rank=rank,
                    matched_by=["sparse"],
                    provenance=p,
                )
            )
        return retrieved
