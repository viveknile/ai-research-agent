import pytest

from app.ai.gemini import GeminiProvider


@pytest.mark.asyncio
async def test_gemini_provider():
    provider = GeminiProvider()

    response = await provider.generate(
        "Reply with exactly: Gemini connection successful"
    )

    assert response