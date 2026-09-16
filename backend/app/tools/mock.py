from hashlib import md5

from app.schemas.research import SearchResult, WebDocument
from app.tools.base import FetchProvider, SearchProvider


class MockSearchProvider(SearchProvider):
    """Mock web search provider used for tests and local development."""

    async def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:
        results: list[SearchResult] = []

        safe_query = (
            query.lower()
            .replace(" ", "-")
            .replace("/", "-")
        )

        # Create a unique hash for each query.
        # This prevents duplicate source IDs when
        # multiple search queries are executed.
        query_hash = md5(
            query.encode("utf-8")
        ).hexdigest()[:8]

        # Generate up to 3 mock results.
        for index in range(min(max_results, 3)):
            source_id = (
                f"mock-source-{query_hash}-{index}"
            )

            results.append(
                SearchResult(
                    id=source_id,
                    title=f"Mock result {index + 1}",
                    url=(
                        f"https://example.com/research/"
                        f"{safe_query}/{index}"
                    ),
                    snippet=(
                        f"Mock search result for {query}"
                    ),
                    content=(
                        f"Mock content related to {query}"
                    ),
                    domain="example.com",
                )
            )

        return results


class MockFetchProvider(FetchProvider):
    """Mock webpage fetcher used for tests and local development."""

    async def fetch(
        self,
        url: str,
        source_id: str,
    ) -> WebDocument:
        return WebDocument(
            source_id=source_id,
            url=url,
            title="Mock Research Source",
            content=(
                "Mock webpage content containing useful "
                "information about AI agent frameworks, "
                "orchestration, and Python backend development."
            ),
            domain="example.com",
        )