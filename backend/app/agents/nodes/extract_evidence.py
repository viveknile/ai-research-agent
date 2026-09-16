from uuid import uuid4

from app.agents.state import ResearchState
from app.ai.provider import get_ai_provider
from app.schemas.research import EvidenceExtraction


ai_provider = get_ai_provider()

MAX_DOCUMENTS = 12
MAX_CONTENT_PER_DOCUMENT = 5000


async def extract_evidence(state: ResearchState) -> dict:
    documents = state.get("documents", [])
    errors = list(state.get("errors", []))

    print(
        "[ResearchPilot] Starting evidence extraction "
        f"for {len(documents)} documents..."
    )

    if not documents:
        print(
            "[ResearchPilot] No documents available "
            "for evidence extraction."
        )

        return {
            "evidence": [],
            "errors": errors,
        }

    documents = documents[:MAX_DOCUMENTS]

    documents_text_parts = []

    for document in documents:
        content = document.get("content", "")

        if len(content) > MAX_CONTENT_PER_DOCUMENT:
            content = content[:MAX_CONTENT_PER_DOCUMENT]

            content += (
                "\n\n[Document content truncated "
                "for research processing.]"
            )

        documents_text_parts.append(
            f"""
DOCUMENT ID: {document["source_id"]}
TITLE: {document["title"]}
URL: {document["url"]}
DOMAIN: {document["domain"]}

CONTENT:
{content}
"""
        )

    documents_text = "\n\n".join(
        documents_text_parts
    )

    prompt = f"""
You are an evidence extraction assistant for ResearchPilot.

Extract important factual evidence from the supplied research
documents.

Research question:

{state["query"]}

Research documents:

{documents_text}

Requirements:

1. Extract useful factual claims from the documents.
2. Every claim must be supported by the supplied document.
3. Use the exact DOCUMENT ID as the source_id.
4. Include supporting evidence text from the document.
5. Give every evidence item a confidence score between 0 and 1.
6. Do not invent information.
7. Ignore documents that contain no useful evidence.
8. Extract multiple evidence items when appropriate.
9. Keep evidence concise and factual.
10. Prefer a small number of high-quality evidence items over
    many repetitive items.

Return only actual JSON data matching the requested schema.
Do not return the JSON schema itself.
"""

    try:
        print(
            "[ResearchPilot] Sending evidence extraction "
            "request to OpenRouter..."
        )

        result = await ai_provider.generate_structured(
            prompt,
            EvidenceExtraction,
        )

        valid_source_ids = {
            document["source_id"]
            for document in documents
        }

        evidence = []

        for item in result.evidence:

            if item.source_id not in valid_source_ids:
                print(
                    "[ResearchPilot] Ignoring evidence with "
                    f"unknown source_id: {item.source_id}"
                )
                continue

            evidence.append(
                {
                    "id": str(uuid4()),
                    "source_id": item.source_id,
                    "claim": item.claim,
                    "evidence_text": item.evidence_text,
                    "confidence": item.confidence,
                }
            )

        print(
            "[ResearchPilot] Evidence extraction completed. "
            f"Extracted {len(evidence)} evidence items."
        )

        return {
            "evidence": evidence,
            "errors": errors,
        }

    except Exception as exc:
        error_message = (
            f"Evidence extraction failed: {exc}"
        )

        print(
            f"[ResearchPilot] {error_message}"
        )

        errors.append(error_message)

        raise