from app.agents.state import ResearchState
from app.tools.fetch import HTTPFetchProvider


fetch_provider = HTTPFetchProvider()


async def fetch_sources(state: ResearchState) -> ResearchState:
    sources = state.get("sources", [])
    existing_documents = state.get("documents", [])

    # Keep track of sources that have already been fetched.
    fetched_source_ids = {
        document["source_id"]
        for document in existing_documents
    }

    new_documents = []
    errors = list(state.get("errors", []))

    for source in sources:

        source_id = source["id"]

        # Skip sources that were already fetched.
        if source_id in fetched_source_ids:
            continue

        try:
            document = await fetch_provider.fetch(
                url=source["url"],
                source_id=source_id,
            )

            new_documents.append(
                document.model_dump()
            )

            fetched_source_ids.add(source_id)

        except Exception as exc:

            error_message = (
                f"Failed to fetch "
                f"{source['url']}: {exc}"
            )

            errors.append(error_message)

            print(error_message)

    return {
        **state,
        "documents": existing_documents + new_documents,
        "errors": errors,
    }