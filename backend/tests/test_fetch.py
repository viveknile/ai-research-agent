import pytest

from app.tools.fetch import HTTPFetchProvider


@pytest.mark.asyncio
async def test_http_fetch():

    provider = HTTPFetchProvider()

    document = await provider.fetch(
        url="https://example.com",
        source_id="test-source",
    )

    assert document.source_id == "test-source"
    assert document.url == "https://example.com"
    assert document.title
    assert document.content
    assert document.domain == "example.com"