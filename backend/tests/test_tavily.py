import pytest

from app.tools.search import TavilySearchProvider


@pytest.mark.asyncio
async def test_tavily_search():

    provider = TavilySearchProvider()

    results = await provider.search(
        "AI agent frameworks 2026",
        max_results=3,
    )

    assert results
    assert len(results) <= 3

    for result in results:
        assert result.id
        assert result.title
        assert result.url
        assert result.domain