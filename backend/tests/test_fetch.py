import pytest

from app.tools.fetch import HTTPFetchProvider


@pytest.mark.asyncio
async def test_http_fetch():

    provider = HTTPFetchProvider()

    document = await provider.fetch(
        "https://example.com"
    )

    assert document.url == "https://example.com"
    assert document.title
    assert document.content
    assert document.domain == "example.com"