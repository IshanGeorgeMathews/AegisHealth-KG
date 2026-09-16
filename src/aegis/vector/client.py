from typing import Optional

from qdrant_client import QdrantClient

from aegis.config.settings import get_settings


class VectorClient:
    def __init__(
        self,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        in_memory: bool = False,
    ):
        settings = get_settings()
        if in_memory:
            self.client = QdrantClient(location=":memory:")
        else:
            self.url = url or settings.qdrant_url
            self.api_key = api_key or settings.qdrant_api_key
            try:
                self.client = QdrantClient(url=self.url, api_key=self.api_key, timeout=5)
            except Exception:
                self.client = QdrantClient(location=":memory:")

    def get_client(self) -> QdrantClient:
        return self.client
