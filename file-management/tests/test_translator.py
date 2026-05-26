"""
Tests for the translator interface.
"""
import pytest

from file_management.translator.translator import Translator


@pytest.mark.asyncio
async def test_translate_raises_not_implemented():
    """translate should raise NotImplementedError until implemented."""
    trans = Translator()
    with pytest.raises(NotImplementedError):
        await trans.translate("anonymized text", "fr")
