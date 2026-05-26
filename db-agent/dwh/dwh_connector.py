"""
Data Warehouse connector.
"""
import os
from typing import Any, Dict, List

from shared.communication_layer.logger import get_logger

logger = get_logger("DB_AGENT")

DWH_URL = os.getenv("DWH_URL", "")


class DWHConnector:
    """Handles queries to the Data Warehouse."""

    async def execute_query(self, sql: str, params: List[Any] = []) -> List[Dict[str, Any]]:
        """Executes a safe, pre-validated SELECT query against the DWH."""
        raise NotImplementedError
