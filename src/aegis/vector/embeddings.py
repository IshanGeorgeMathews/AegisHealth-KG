from typing import List, Optional

from fastembed import SparseTextEmbedding, TextEmbedding

from aegis.config.settings import get_settings


class EmbeddingService:
    def __init__(self, dense_model_name: Optional[str] = None):
        settings = get_settings()
        self.dense_model_name = dense_model_name or settings.embedding_model
        self._dense_model: Optional[TextEmbedding] = None
        self._sparse_model: Optional[SparseTextEmbedding] = None

    @property
    def dense_model(self) -> TextEmbedding:
        if self._dense_model is None:
            self._dense_model = TextEmbedding(model_name=self.dense_model_name)
        return self._dense_model

    @property
    def sparse_model(self) -> SparseTextEmbedding:
        if self._sparse_model is None:
            self._sparse_model = SparseTextEmbedding(model_name="Qdrant/bm25")
        return self._sparse_model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = list(self.dense_model.embed(texts))
        return [e.tolist() for e in embeddings]

    def embed_query(self, query: str) -> List[float]:
        embeddings = list(self.dense_model.embed([query]))
        return embeddings[0].tolist()

    def embed_sparse_documents(self, texts: List[str]):
        embeddings = list(self.sparse_model.embed(texts))
        return embeddings

    def embed_sparse_query(self, query: str):
        embeddings = list(self.sparse_model.embed([query]))
        return embeddings[0]
