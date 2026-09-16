import re

from pydantic import BaseModel

from app.ai.base import AIProvider
from app.schemas.research import (
    Evidence,
    EvidenceExtraction,
    Finding,
    FindingAnalysis,
    ReportDraft,
    ReportFinding,
    ResearchGaps,
    ResearchPlan,
    SearchQueries,
)


class MockAIProvider(AIProvider):
    async def generate(
        self,
        prompt: str,
    ) -> str:
        return "Mock AI response"

    async def generate_structured(
        self,
        prompt: str,
        schema: type[BaseModel],
    ) -> BaseModel:

        # ====================================================
        # Research Plan
        # ====================================================

        if schema is ResearchPlan:
            return ResearchPlan(
                objective=(
                    "Compare major AI agent frameworks and "
                    "determine which is suitable for Python "
                    "development."
                ),
                research_questions=[
                    "What are the major AI agent frameworks?",
                    "What are their main features?",
                    "Which framework is suitable for Python?",
                ],
                search_topics=[
                    "AI agent frameworks",
                    "Python AI agent frameworks",
                    "AI agent framework comparison",
                ],
            )

        # ====================================================
        # Search Queries
        # ====================================================

        if schema is SearchQueries:
            return SearchQueries(
                queries=[
                    "AI agent frameworks 2026",
                    "Python AI agent frameworks 2026",
                    "LangGraph vs other agent frameworks 2026",
                    "AI agent framework comparison 2026",
                    "best AI agent framework Python 2026",
                ]
            )

        # ====================================================
        # Batch Evidence Extraction
        # ====================================================

        if schema is EvidenceExtraction:
            return EvidenceExtraction(
                evidence=[
                    Evidence(
                        id="mock-evidence-1",
                        source_id="mock-source",
                        claim=(
                            "AI agent frameworks provide "
                            "structured orchestration for "
                            "building agent workflows."
                        ),
                        evidence_text=(
                            "Mock evidence extracted from the "
                            "webpage showing that agent "
                            "frameworks support structured "
                            "workflows."
                        ),
                        confidence=0.9,
                    )
                ]
            )

        # ====================================================
        # Single Evidence
        # ====================================================

        if schema is Evidence:
            return Evidence(
                id="mock-evidence-1",
                source_id="mock-source",
                claim=(
                    "AI agent frameworks provide structured "
                    "orchestration for building agent "
                    "workflows."
                ),
                evidence_text=(
                    "Mock evidence extracted from the "
                    "webpage showing that agent frameworks "
                    "support structured workflows."
                ),
                confidence=0.9,
            )

        # ====================================================
        # Batch Finding Analysis
        # ====================================================

        if schema is FindingAnalysis:

            # The extract_evidence node creates the actual
            # evidence ID dynamically. Extract that ID from
            # the prompt so the mock finding references the
            # same ID.
            match = re.search(
                r"EVIDENCE ID:\s*([^\s]+)",
                prompt,
            )

            if match:
                evidence_id = match.group(1)
            else:
                evidence_id = "mock-evidence-1"

            return FindingAnalysis(
                findings=[
                    Finding(
                        id="mock-finding-1",
                        statement=(
                            "AI agent frameworks provide "
                            "structured orchestration for "
                            "building agent workflows."
                        ),
                        confidence=0.9,
                        supporting_evidence_ids=[
                            evidence_id,
                        ],
                    )
                ]
            )

        # ====================================================
        # Single Finding
        # ====================================================

        if schema is Finding:

            match = re.search(
                r"EVIDENCE ID:\s*([^\s]+)",
                prompt,
            )

            if match:
                evidence_id = match.group(1)
            else:
                evidence_id = "mock-evidence-1"

            return Finding(
                id="mock-finding-1",
                statement=(
                    "AI agent frameworks provide structured "
                    "orchestration for building agent "
                    "workflows."
                ),
                confidence=0.9,
                supporting_evidence_ids=[
                    evidence_id,
                ],
            )

        # ====================================================
        # Research Gap Check
        # ====================================================

        if schema is ResearchGaps:
            return ResearchGaps(
                research_gaps=[]
            )

        # ====================================================
        # Final Report Draft
        # ====================================================

        if schema is ReportDraft:

            match = re.search(
                r"EVIDENCE ID:\s*([^\s]+)",
                prompt,
            )

            if match:
                evidence_id = match.group(1)
            else:
                evidence_id = "mock-evidence-1"

            return ReportDraft(
                title=(
                    "AI Agent Frameworks for Python Development"
                ),
                executive_summary=(
                    "AI agent frameworks provide structured "
                    "orchestration for building agent "
                    "workflows. Choosing a framework should "
                    "depend on workflow requirements, Python "
                    "ecosystem support, and production needs."
                ),
                findings=[
                    ReportFinding(
                        statement=(
                            "AI agent frameworks provide "
                            "structured orchestration for "
                            "building agent workflows."
                        ),
                        confidence=0.9,
                        evidence_ids=[
                            evidence_id,
                        ],
                    ),
                    ReportFinding(
                        statement=(
                            "Python ecosystem support and "
                            "production requirements are "
                            "important factors when selecting "
                            "an AI agent framework."
                        ),
                        confidence=0.85,
                        evidence_ids=[
                            evidence_id,
                        ],
                    ),
                ],
            )

        # ====================================================
        # Unsupported Schema
        # ====================================================

        raise ValueError(
            f"Unsupported mock schema: {schema.__name__}"
        )