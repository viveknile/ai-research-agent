from unittest.mock import AsyncMock, patch

import pytest

from app.ai.gemini import GeminiProvider


@pytest.mark.asyncio
async def test_gemini_provider():
    mock_response = type(
        "MockResponse",
        (),
        {
            "content": "Gemini connection successful",
        },
    )()

    with patch(
        "langchain_core.language_models.chat_models.BaseChatModel.ainvoke",
        new=AsyncMock(return_value=mock_response),
    ):
        provider = GeminiProvider()

        response = await provider.generate(
            "Reply with exactly: Gemini connection successful"
        )

    assert response == "Gemini connection successful"