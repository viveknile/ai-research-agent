import uuid

from app.agents.state import ResearchState
from app.ai.gemini import GeminiProvider
from app.schemas.research import Evidence


gemini_provider = GeminiProvider()


async def extract_evidence(
    state: ResearchState,
) -> ResearchState:

    documents = state.get("documents", [])

    all_evidence = []
    errors = list(state.get("errors", []))

    for document in documents:

        prompt = f"""
You are a research evidence extraction assistant.

Read the following webpage and extract the most important
evidence relevant to this research question.

Research question:
{state["query"]}

Webpage title:
{document["title"]}

Webpage URL:
{document["url"]}

Webpage content:
{document["content"]}

Extract useful factual claims supported by this webpage.

For the evidence:
- Write a concise factual claim.
- Provide the supporting information from the webpage.
- Assign a confidence score from 0.0 to 1.0.
- Only extract information that is actually supported by the webpage.
"""

        try:

            evidence = await gemini_provider.generate_structured(
                prompt,
                Evidence,
            )

            evidence.id = str(uuid.uuid4())
            evidence.source_id = document["source_id"]

            all_evidence.append(
                evidence.model_dump()
            )

        except Exception as exc:

            error_message = (
                f"Evidence extraction failed for "
                f"{document['url']}: {exc}"
            )

            errors.append(error_message)

            print(error_message)

    return {
        **state,
        "evidence": all_evidence,
        "errors": errors,
    }