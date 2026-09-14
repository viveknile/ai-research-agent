from pydantic import BaseModel

from app.ai.base import AIProvider
from app.schemas.research import (
    Evidence,
    Finding,
    ResearchPlan,
    SearchQueries,
)


class MockAIProvider(AIProvider):

    async def generate(self, prompt: str) -> str:
        return "Mock AI response"

    async def generate_structured(
        self,
        prompt: str,
        schema: type[BaseModel],
    ) -> BaseModel:

        if schema is ResearchPlan:
            return ResearchPlan(
                objective="Compare AI agent frameworks in 2026.",
                research_questions=[
                    "What are the major AI agent frameworks?",
                    "What are their main features?",
                    "Which framework is suitable for a Python backend?",
                ],
                search_topics=[
                    "AI agent frameworks",
                    "Python AI agent frameworks",
                    "AI agent framework comparison",
                ],
            )

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

        if schema is Evidence:
            return Evidence(
                id="mock-evidence-1",
                source_id="mock-source",
                claim=(
                    "This webpage contains information "
                    "relevant to AI agent frameworks."
                ),
                evidence_text=(
                    "Mock evidence extracted from the webpage."
                ),
                confidence=0.9,
            )

        if schema is Finding:
            return Finding(
                id="mock-finding-1",
                statement=(
                    "AI agent frameworks provide structured "
                    "orchestration for building agent workflows."
                ),
                confidence=0.9,
                supporting_evidence_ids=[
                    "mock-evidence-1",
                ],
            )

        raise ValueError(
            f"Unsupported mock schema: {schema.__name__}"
        )