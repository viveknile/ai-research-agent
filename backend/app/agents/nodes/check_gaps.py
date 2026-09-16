from app.agents.state import ResearchState
from app.ai.provider import get_ai_provider
from app.schemas.research import ResearchGaps


ai_provider = get_ai_provider()


async def check_gaps(state: ResearchState) -> dict:
    query = state["query"]
    research_plan = state.get("research_plan", {})
    findings = state.get("findings", [])
    evidence = state.get("evidence", [])
    iteration = state.get("iteration", 1)

    print(
        f"[ResearchPilot] Checking research gaps "
        f"(iteration {iteration})..."
    )

    findings_text = "\n".join(
        f"{index + 1}. {finding['statement']}"
        for index, finding in enumerate(findings)
    )

    evidence_text = "\n".join(
        (
            f"{index + 1}. "
            f"{item['claim']}: "
            f"{item['evidence_text']}"
        )
        for index, item in enumerate(evidence)
    )

    prompt = f"""
Determine whether the current research contains important gaps
that prevent confidently answering the original research question.

Original research question:

{query}

Research plan:

{research_plan}

Current research round:

{iteration}

Current findings:

{findings_text}

Current evidence:

{evidence_text}

Identify ONLY meaningful research gaps.

A meaningful gap is something important that is still missing,
such as:

- An important part of the question is unanswered.
- A major comparison is missing.
- Important evidence is insufficient.
- Important current information is missing.

If the research is already sufficient, return:

{{
    "research_gaps": []
}}

Return ONLY the actual JSON data.
"""

    print(
        "[ResearchPilot] Sending gap-check request "
        "to OpenRouter..."
    )

    result = await ai_provider.generate_structured(
        prompt,
        ResearchGaps,
    )

    print(
        "[ResearchPilot] Gap check completed. "
        f"Gaps found: {result.research_gaps}"
    )

    return {
        "research_gaps": result.research_gaps
    }