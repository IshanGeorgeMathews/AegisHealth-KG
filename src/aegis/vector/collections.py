from typing import Optional

from qdrant_client.http import models as rest

from aegis.config.settings import get_settings
from aegis.vector.client import VectorClient


def init_collection(client_wrapper: VectorClient, collection_name: Optional[str] = None):
    settings = get_settings()
    col_name = collection_name or settings.qdrant_collection
    client = client_wrapper.get_client()

    collections = [c.name for c in client.get_collections().collections]
    if col_name not in collections:
        client.create_collection(
            collection_name=col_name,
            vectors_config={
                "dense": rest.VectorParams(
                    size=384,
                    distance=rest.Distance.COSINE,
                )
            },
            sparse_vectors_config={
                "sparse": rest.SparseVectorParams(
                    index=rest.SparseIndexParams(
                        on_disk=False,
                    )
                )
            },
        )

        filter_fields = [
            "patient_id",
            "scenario_id",
            "policy_id",
            "requirement_id",
            "source_type",
            "document_id",
            "claim_id",
        ]
        for field in filter_fields:
            client.create_payload_index(
                collection_name=col_name,
                field_name=field,
                field_schema=rest.PayloadSchemaType.KEYWORD,
            )
