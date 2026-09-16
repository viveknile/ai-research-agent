from uuid import uuid4

from app.agents.state import ResearchState
from app.ai.provider import get_ai_provider
from app.schemas.research import FindingAnalysis


ai_provider = get_ai_provider()


async def analyze_findings(state: ResearchState) -> dict:
    query = state["query"]

    evidence = state.get("evidence", [])

    errors = list(
        state.get("errors", [])
    )

    # --------------------------------------------------------
    # No evidence
    # --------------------------------------------------------

    if not evidence:
        return {
            "findings": [],
            "errors": errors,
        }

    # --------------------------------------------------------
    # Prepare evidence for one AI request
    # --------------------------------------------------------

    evidence_text = "\n\n".join(
        (
            f"EVIDENCE ID: {item['id']}\n"
            f"SOURCE ID: {item['source_id']}\n"
            f"CLAIM: {item['claim']}\n"
            f"EVIDENCE: {item['evidence_text']}\n"
            f"CONFIDENCE: {item['confidence']}"
        )
        for item in evidence
    )

    # --------------------------------------------------------
    # Prompt
    # --------------------------------------------------------

    prompt = f"""
You are a research analysis assistant for ResearchPilot.

Analyze the supplied evidence and produce research findings.

Original research question:

{query}

Research evidence:

{evidence_text}

Requirements:

1. Produce findings that directly contribute to answering
   the research question.
2. Every finding must be supported by supplied evidence.
3. Use the exact EVIDENCE ID values when identifying
   supporting evidence.
4. Do not invent facts.
5. Do not make claims that cannot be supported by the evidence.
6. Combine related evidence when appropriate.
7. Give every finding a confidence score between 0 and 1.
8. Keep findings clear and concise.

Return only structured findings.
"""

    # --------------------------------------------------------
    # AI call
    # --------------------------------------------------------

    try:
        result = await ai_provider.generate_structured(
            prompt,
            FindingAnalysis,
        )

        valid_evidence_ids = {
            item["id"]
            for item in evidence
        }

        findings: list[dict] = []

        for item in result.findings:

            supporting_ids = [
                evidence_id
                for evidence_id
                in item.supporting_evidence_ids
                if evidence_id in valid_evidence_ids
            ]

            # Ignore findings that have no valid evidence.
            if not supporting_ids:
                continue

            findings.append(
                {
                    "id": str(uuid4()),
                    "statement": item.statement,
                    "confidence": item.confidence,
                    "supporting_evidence_ids": supporting_ids,
                }
            )

        return {
            "findings": findings,
            "errors": errors,
        }

    except Exception as exc:
        errors.append(
            f"Finding analysis failed: {exc}"
        )

        return {
            "findings": [],
            "errors": errors,
        }