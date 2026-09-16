import asyncio

from app.agents.state import ResearchState
from app.tools.provider import get_search_provider


search_provider = get_search_provider()

MAX_RESULTS_PER_QUERY = 3
MAX_TOTAL_SOURCES = 12
MAX_CONCURRENT_SEARCHES = 4


async def _search_single_query(
    query: str,
) -> tuple[str, list]:
    try:
        results = await search_provider.search(
            query=query,
            max_results=MAX_RESULTS_PER_QUERY,
        )

        return query, results

    except Exception as exc:
        print(
            "[ResearchPilot] Search failed for "
            f"'{query}': {exc}"
        )

        return query, []


async def search_web(state: ResearchState) -> dict:
    search_queries = state.get("search_queries", [])
    errors = list(state.get("errors", []))

    print(
        "[ResearchPilot] Starting web search for "
        f"{len(search_queries)} queries..."
    )

    seen_urls = {
        source["url"]
        for source in state.get("sources", [])
        if source.get("url")
    }

    sources: list[dict] = []

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_SEARCHES
    )

    async def limited_search(query: str):
        async with semaphore:
            return await _search_single_query(query)

    results_by_query = await asyncio.gather(
        *[
            limited_search(query)
            for query in search_queries
        ]
    )

    for query, results in results_by_query:
        print(
            "[ResearchPilot] Search completed: "
            f"'{query}' -> {len(results)} results"
        )

        for result in results:
            if result.url in seen_urls:
                continue

            seen_urls.add(result.url)
            sources.append(result.model_dump())

            if len(sources) >= MAX_TOTAL_SOURCES:
                break

        if len(sources) >= MAX_TOTAL_SOURCES:
            break

    print(
        "[ResearchPilot] Web search completed. "
        f"Collected {len(sources)} unique sources."
    )

    return {
        "sources": sources,
        "errors": errors,
    }