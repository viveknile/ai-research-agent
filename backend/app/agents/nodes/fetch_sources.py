from app.agents.state import ResearchState
from app.tools.fetch import HTTPFetchProvider


fetch_provider = HTTPFetchProvider()


async def fetch_sources(state: ResearchState) -> ResearchState:
    sources = state.get("sources", [])

    documents = []

    for source in sources[:10]:
        try:
            document = await fetch_provider.fetch(
                source["url"]
            )

            documents.append(
                document.model_dump()
            )

        except Exception as exc:
            print(
                f"Failed to fetch {source['url']}: {exc}"
            )

    return {
        **state,
        "documents": documents,
    }