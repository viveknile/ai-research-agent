from app.agents.state import ResearchState
from app.tools.search import TavilySearchProvider


tavily_provider = TavilySearchProvider()


async def search_web(state: ResearchState) -> ResearchState:
    search_queries = state.get("search_queries", [])
    existing_sources = state.get("sources", [])

    # Keep track of URLs we already have.
    existing_urls = {
        source["url"]
        for source in existing_sources
    }

    new_sources = []

    for query in search_queries:

        try:
            results = await tavily_provider.search(
                query=query,
                max_results=5,
            )

            for result in results:

                # Skip duplicate URLs.
                if result.url in existing_urls:
                    continue

                new_sources.append(
                    result.model_dump()
                )

                existing_urls.add(result.url)

        except Exception as exc:

            errors = list(
                state.get("errors", [])
            )

            errors.append(
                f"Web search failed for '{query}': {exc}"
            )

            print(
                f"Web search failed for '{query}': {exc}"
            )

            return {
                **state,
                "sources": existing_sources + new_sources,
                "errors": errors,
            }

    return {
        **state,
        "sources": existing_sources + new_sources,
    }