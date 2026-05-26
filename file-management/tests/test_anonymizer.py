"""
Tests for the anonymizer interface.
"""
import pytest

from file_management.anonymizer.anonymizer import Anonymizer


@pytest.mark.asyncio
async def test_anonymize_raises_not_implemented():
    """anonymize should raise NotImplementedError until implemented."""
    anon = Anonymizer()
    with pytest.raises(NotImplementedError):
        await anon.anonymize("some text with PII")
