from app.agents.state import ResearchState
from app.ai.provider import get_ai_provider
from app.schemas.research import ReportDraft


ai_provider = get_ai_provider()


async def synthesize_report(state: ResearchState) -> dict:
    query = state["query"]

    findings = state.get("findings", [])
    evidence = state.get("evidence", [])
    sources = state.get("sources", [])

    findings_text = "\n".join(
        (
            f"- Finding ID: {finding['id']}\n"
            f"  Statement: {finding['statement']}\n"
            f"  Confidence: {finding['confidence']}"
        )
        for finding in findings
    )

    evidence_text = "\n".join(
        (
            f"- Evidence ID: {item['id']}\n"
            f"  Source ID: {item['source_id']}\n"
            f"  Claim: {item['claim']}\n"
            f"  Evidence: {item['evidence_text']}\n"
            f"  Confidence: {item['confidence']}"
        )
        for item in evidence
    )

    sources_text = "\n".join(
        (
            f"- Source ID: {source['id']}\n"
            f"  Title: {source['title']}\n"
            f"  Domain: {source['domain']}\n"
            f"  URL: {source['url']}"
        )
        for source in sources
    )

    prompt = f"""
You are the senior research analyst for ResearchPilot.

Create a concise research report based ONLY on the supplied research
findings and evidence.

Original research question:
{query}

Research findings:
{findings_text}

Research evidence:
{evidence_text}

Research sources:
{sources_text}

Requirements:

1. Create a clear and descriptive report title.
2. Write an executive summary that directly addresses the research
   question.
3. Select the most important findings.
4. Every finding must be supported by the supplied evidence.
5. Use the Evidence ID values when referencing supporting evidence.
6. Do not invent facts.
7. Do not use information that is not present in the supplied research.
8. Keep the report concise and useful.
9. If the evidence is insufficient for a claim, do not make that claim.
"""

    draft = await ai_provider.generate_structured(
        prompt,
        ReportDraft,
    )

    return {
        "report_draft": draft.model_dump(),
    }