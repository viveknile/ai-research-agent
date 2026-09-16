import pytest

from app.ai.openrouter import OpenRouterProvider


@pytest.mark.integration
@pytest.mark.asyncio
async def test_openrouter_real():
    provider = OpenRouterProvider()

    response = await provider.generate(
        "Reply with exactly: OpenRouter connection successful"
    )

    assert response.strip() == (
        "OpenRouter connection successful"
    )