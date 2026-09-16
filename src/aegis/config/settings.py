from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    api_host: str = "127.0.0.1"
    api_port: int = 8000
    environment: str = "development"

    # Neo4j Settings
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_username: Optional[str] = None
    neo4j_password: str = "password"

    # Qdrant Settings
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    qdrant_collection: str = "aegis_evidence"

    # Embedding & Reranking Models
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    reranker_model: str = "BAAI/bge-reranker-v2-m3"

    # Retrieval Limits & Weights
    dense_top_k: int = 20
    sparse_top_k: int = 20
    fusion_candidate_limit: int = 50
    rerank_top_k: int = 10
    rrf_k: int = 60
    dense_weight: float = 1.0
    sparse_weight: float = 0.9
    graph_weight: float = 1.2

    # Chunking Settings
    chunk_target_tokens: int = 400
    chunk_hard_limit: int = 900

    def get_neo4j_username(self) -> str:
        return self.neo4j_username or self.neo4j_user

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings()
