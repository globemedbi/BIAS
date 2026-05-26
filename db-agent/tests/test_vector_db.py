"""
Tests for Vector DB connector interface.
"""
import pytest

from db_agent.vector_db.vector_connector import VectorDBConnector


@pytest.mark.asyncio
async def test_upsert_raises_not_implemented():
    """upsert_document should raise NotImplementedError until implemented."""
    connector = VectorDBConnector()
    with pytest.raises(NotImplementedError):
        await connector.upsert_document("doc-1", [0.1, 0.2], {"key": "val"})


@pytest.mark.asyncio
async def test_search_raises_not_implemented():
    """search should raise NotImplementedError until implemented."""
    connector = VectorDBConnector()
    with pytest.raises(NotImplementedError):
        await connector.search([0.1, 0.2])
