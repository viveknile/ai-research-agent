import uuid

from app.agents.state import ResearchState
from app.ai.gemini import GeminiProvider
from app.schemas.research import Finding


gemini_provider = GeminiProvider()


async def analyze_findings(
    state: ResearchState,
) -> ResearchState:

    evidence = state.get("evidence", [])

    if not evidence:
        return {
            **state,
            "findings": [],
        }

    evidence_text = "\n\n".join(
        [
            (
                f"Evidence ID: {item['id']}\n"
                f"Source ID: {item['source_id']}\n"
                f"Claim: {item['claim']}\n"
                f"Evidence: {item['evidence_text']}\n"
                f"Confidence: {item['confidence']}"
            )
            for item in evidence
        ]
    )

    prompt = f"""
You are a research analysis assistant.

Analyze the evidence collected for the following research question:

Research question:
{state["query"]}

Evidence:

{evidence_text}

Create a research finding by combining and comparing
the available evidence.

Requirements:
- The finding must be supported by the provided evidence.
- Do not introduce unsupported facts.
- Prefer conclusions supported by multiple pieces of evidence.
- If evidence is weak, keep the confidence lower.
- Identify which evidence IDs support the finding.
- Do not invent evidence IDs.
"""

    try:

        finding = await gemini_provider.generate_structured(
            prompt,
            Finding,
        )

        finding.id = str(uuid.uuid4())

        return {
            **state,
            "findings": [
                finding.model_dump()
            ],
        }

    except Exception as exc:

        errors = list(state.get("errors", []))

        errors.append(
            f"Finding analysis failed: {exc}"
        )

        print(
            f"Finding analysis failed: {exc}"
        )

        return {
            **state,
            "findings": [],
            "errors": errors,
        }