import hashlib
from urllib.parse import urlparse

from tavily import TavilyClient

from app.core.config import settings
from app.schemas.research import SearchResult
from app.tools.base import SearchProvider


class TavilySearchProvider(SearchProvider):

    def __init__(self):
        self.client = TavilyClient(
            api_key=settings.tavily_api_key
        )

    async def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:

        response = self.client.search(
            query=query,
            max_results=max_results,
        )

        results = []

        for item in response.get("results", []):
            url = item.get("url", "")

            domain = urlparse(url).netloc

            source_id = hashlib.sha256(
                url.encode("utf-8")
            ).hexdigest()[:16]

            results.append(
                SearchResult(
                    id=source_id,
                    title=item.get("title", ""),
                    url=url,
                    snippet=item.get("content", ""),
                    content=item.get("raw_content"),
                    published_date=item.get("published_date"),
                    domain=domain,
                )
            )

        return results