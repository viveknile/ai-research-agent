from app.agents.state import ResearchState
from app.ai.provider import get_ai_provider
from app.schemas.research import ReportDraft


ai_provider = get_ai_provider()


async def synthesize_report(
    state: ResearchState,
) -> dict:

    query = state["query"]

    findings = state.get(
        "findings",
        [],
    )

    evidence = state.get(
        "evidence",
        [],
    )

    sources = state.get(
        "sources",
        [],
    )

    print(
        "[ResearchPilot] Starting report synthesis..."
    )

    if not findings:
        print(
            "[ResearchPilot] No findings available "
            "for report synthesis."
        )

    findings_text = "\n".join(
        (
            f"FINDING ID: {finding['id']}\n"
            f"STATEMENT: {finding['statement']}\n"
            f"CONFIDENCE: {finding['confidence']}"
        )
        for finding in findings
    )

    evidence_text = "\n".join(
        (
            f"EVIDENCE ID: {item['id']}\n"
            f"SOURCE ID: {item['source_id']}\n"
            f"CLAIM: {item['claim']}\n"
            f"EVIDENCE TEXT: {item['evidence_text']}\n"
            f"CONFIDENCE: {item['confidence']}"
        )
        for item in evidence
    )

    sources_text = "\n".join(
        (
            f"SOURCE ID: {source['id']}\n"
            f"TITLE: {source['title']}\n"
            f"DOMAIN: {source['domain']}\n"
            f"URL: {source['url']}"
        )
        for source in sources
    )

    prompt = f"""
You are the final report synthesis assistant for ResearchPilot.

Your task is to create a concise research report based ONLY on
the supplied research findings and evidence.

ORIGINAL RESEARCH QUESTION:

{query}


RESEARCH FINDINGS:

{findings_text}


RESEARCH EVIDENCE:

{evidence_text}


RESEARCH SOURCES:

{sources_text}


IMPORTANT OUTPUT RULES:

Return ONLY valid JSON data.

Do NOT return markdown.

Do NOT explain your reasoning.

Do NOT describe the schema.

Do NOT return the JSON schema.

Do NOT wrap any field inside another object.

The "findings" field MUST be an array.

Every finding MUST have exactly these fields:

"statement"
"confidence"
"evidence_ids"

The "statement" field MUST be a plain string.

CORRECT:

{{
  "statement": "LangGraph supports stateful workflows.",
  "confidence": 0.9,
  "evidence_ids": ["evidence-id-1"]
}}

INCORRECT:

{{
  "statement": {{
    "title": "LangGraph supports stateful workflows."
  }},
  "confidence": 0.9,
  "evidence_ids": ["evidence-id-1"]
}}

The statement must NEVER be an object.

Requirements:

1. Create a clear descriptive report title.
2. Write an executive summary that directly addresses
   the research question.
3. Select the most important findings.
4. Every finding must be supported by supplied evidence.
5. Use exact EVIDENCE ID values.
6. Do not invent facts.
7. Do not use information outside the supplied research.
8. Keep the report concise.
9. If evidence is insufficient for a claim, do not make that claim.
10. Use plain strings for every finding statement.
11. Return actual JSON data only.
"""

    print(
        "[ResearchPilot] Sending report synthesis "
        "request to OpenRouter..."
    )

    try:

        draft = await ai_provider.generate_structured(
            prompt,
            ReportDraft,
        )

        print(
            "[ResearchPilot] Report synthesis completed."
        )

        return {
            "report_draft": draft.model_dump()
        }

    except Exception as exc:

        print(
            "[ResearchPilot] Report synthesis failed: "
            f"{exc}"
        )

        raise