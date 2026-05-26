"""
Tests for OCR engine interface.
"""
import pytest

from file_management.ocr.ocr_engine import OCREngine


@pytest.mark.asyncio
async def test_extract_text_raises_not_implemented():
    """extract_text should raise NotImplementedError until implemented."""
    engine = OCREngine()
    with pytest.raises(NotImplementedError):
        await engine.extract_text("s3://bucket/file.pdf")
