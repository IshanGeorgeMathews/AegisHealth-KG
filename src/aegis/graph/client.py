from typing import Any, Dict, List, Optional

from neo4j import Driver, GraphDatabase

from aegis.config.settings import get_settings


class Neo4jClient:
    def __init__(self, uri: Optional[str] = None, auth: Optional[tuple] = None):
        settings = get_settings()
        self.uri = uri or settings.neo4j_uri
        user = auth[0] if auth else settings.get_neo4j_username()
        password = auth[1] if auth else settings.neo4j_password
        self._driver: Optional[Driver] = None
        self._auth = (user, password)

    def connect(self) -> Driver:
        if not self._driver:
            self._driver = GraphDatabase.driver(self.uri, auth=self._auth)
        return self._driver

    def close(self):
        if self._driver:
            self._driver.close()
            self._driver = None

    def execute_query(
        self, query: str, parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        driver = self.connect()
        with driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def is_connected(self) -> bool:
        try:
            driver = self.connect()
            driver.verify_connectivity()
            return True
        except Exception:
            return False
