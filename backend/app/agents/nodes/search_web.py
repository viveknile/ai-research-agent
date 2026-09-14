from app.agents.state import ResearchState
from app.tools.search import TavilySearchProvider


tavily_provider = TavilySearchProvider()


async def search_web(state: ResearchState) -> ResearchState:
    search_queries = state["search_queries"]

    all_sources = []

    for query in search_queries:
        results = await tavily_provider.search(
            query=query,
            max_results=5,
        )

        all_sources.extend(
            result.model_dump()
            for result in results
        )

    return {
        **state,
        "sources": all_sources,
    }