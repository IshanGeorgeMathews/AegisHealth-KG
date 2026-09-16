import uuid
from typing import List

from qdrant_client.http import models as rest

from aegis.config.settings import get_settings
from aegis.models.evidence import EvidenceChunk
from aegis.vector.client import VectorClient
from aegis.vector.collections import init_collection
from aegis.vector.embeddings import EmbeddingService


class VectorIndexer:
    def __init__(self, client_wrapper: VectorClient, embedding_service: EmbeddingService):
        self.client_wrapper = client_wrapper
        self.embedding_service = embedding_service
        self.settings = get_settings()
        init_collection(self.client_wrapper, self.settings.qdrant_collection)

    def index_chunks(self, chunks: List[EvidenceChunk]):
        if not chunks:
            return

        texts = [c.text for c in chunks]
        dense_vectors = self.embedding_service.embed_documents(texts)
        sparse_vectors = self.embedding_service.embed_sparse_documents(texts)

        points = []
        for idx, c in enumerate(chunks):
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, c.evidence_id))
            payload = c.model_dump()

            sp_vec = sparse_vectors[idx]
            points.append(
                rest.PointStruct(
                    id=point_id,
                    vector={
                        "dense": dense_vectors[idx],
                        "sparse": rest.SparseVector(
                            indices=sp_vec.indices.tolist(),
                            values=sp_vec.values.tolist(),
                        ),
                    },
                    payload=payload,
                )
            )

        client = self.client_wrapper.get_client()
        client.upsert(
            collection_name=self.settings.qdrant_collection,
            points=points,
        )
