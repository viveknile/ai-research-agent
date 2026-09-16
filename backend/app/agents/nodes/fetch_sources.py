import asyncio

from app.agents.state import ResearchState
from app.tools.fetch_provider import get_fetch_provider


fetch_provider = get_fetch_provider()

MAX_CONCURRENT_FETCHES = 5
MAX_TOTAL_DOCUMENTS = 12


async def _fetch_single_source(
    source: dict,
):
    source_id = source["id"]
    url = source["url"]

    try:
        document = await fetch_provider.fetch(
            url=url,
            source_id=source_id,
        )

        return document

    except Exception as exc:
        print(
            "[ResearchPilot] Source fetch failed: "
            f"{url} -> {exc}"
        )

        return None


async def fetch_sources(state: ResearchState) -> dict:
    sources = state.get("sources", [])
    errors = list(state.get("errors", []))

    print(
        "[ResearchPilot] Starting source fetching for "
        f"{len(sources)} sources..."
    )

    unique_sources = []
    seen_source_ids = set()

    for source in sources:
        source_id = source["id"]

        if source_id in seen_source_ids:
            continue

        seen_source_ids.add(source_id)
        unique_sources.append(source)

        if len(unique_sources) >= MAX_TOTAL_DOCUMENTS:
            break

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_FETCHES
    )

    async def limited_fetch(source: dict):
        async with semaphore:
            return await _fetch_single_source(source)

    documents = await asyncio.gather(
        *[
            limited_fetch(source)
            for source in unique_sources
        ]
    )

    valid_documents = [
        document
        for document in documents
        if document is not None
    ]

    print(
        "[ResearchPilot] Source fetching completed. "
        f"Fetched {len(valid_documents)} documents."
    )

    return {
        "documents": [
            document.model_dump()
            for document in valid_documents
        ],
        "errors": errors,
    }