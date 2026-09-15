from app.agents.state import ResearchState
from app.ai.gemini import GeminiProvider
from app.schemas.research import ResearchGaps


gemini_provider = GeminiProvider()


async def check_gaps(
    state: ResearchState,
) -> ResearchState:

    findings = state.get("findings", [])

    if not findings:
        return {
            **state,
            "research_gaps": [
                "No research findings were produced."
            ],
        }

    findings_text = "\n\n".join(
        [
            (
                f"Finding ID: {finding['id']}\n"
                f"Statement: {finding['statement']}\n"
                f"Confidence: {finding['confidence']}\n"
                f"Supporting evidence: "
                f"{finding['supporting_evidence_ids']}"
            )
            for finding in findings
        ]
    )

    prompt = f"""
You are a research quality-control assistant.

Determine whether the research contains enough information
to answer the user's question.

Research question:
{state["query"]}

Research findings:

{findings_text}

Identify any important gaps in the research.

A gap means:
- An important part of the question is unanswered.
- Evidence is too weak to support an important conclusion.
- Important aspects of the research question have not been investigated.
- More sources are needed to increase confidence.

Do NOT create gaps for minor details.

If the research is sufficient, return an empty list.

Return only important research gaps.
"""

    try:

        result = await gemini_provider.generate_structured(
            prompt,
            ResearchGaps,
        )

        return {
            **state,
            "research_gaps": result.research_gaps,
        }

    except Exception as exc:

        errors = list(
            state.get("errors", [])
        )

        errors.append(
            f"Gap analysis failed: {exc}"
        )

        print(
            f"Gap analysis failed: {exc}"
        )

        return {
            **state,
            "research_gaps": [],
            "errors": errors,
        }