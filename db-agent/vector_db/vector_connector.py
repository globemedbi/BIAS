"""
Vector DB connector — for semantic search over OCR-extracted documents.
"""
import os
from typing import Any, Dict, List

from shared.communication_layer.logger import get_logger

logger = get_logger("DB_AGENT")

VECTOR_DB_URL = os.getenv("VECTOR_DB_URL", "")
VECTOR_DB_API_KEY = os.getenv("VECTOR_DB_API_KEY", "")


class VectorDBConnector:
    """Handles all vector storage and search operations."""

    async def upsert_document(self, doc_id: str, vector: List[float], payload: Dict[str, Any]) -> bool:
        """Upserts a document vector into the vector store."""
        raise NotImplementedError

    async def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Returns the top-k most similar documents."""
        raise NotImplementedError
