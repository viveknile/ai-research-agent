import pytest

from app.ai.openrouter import OpenRouterProvider
from app.schemas.research import ResearchPlan


@pytest.mark.integration
@pytest.mark.asyncio
async def test_openrouter_structured_output():
    provider = OpenRouterProvider()

    prompt = """
You are a research planning assistant.

Research question:

Compare AI agent frameworks for Python development.

Create a research plan with:

1. The main objective.
2. Three important research questions.
3. Three search topics.
"""

    result = await provider.generate_structured(
        prompt,
        ResearchPlan,
    )

    assert isinstance(result, ResearchPlan)

    assert result.objective
    assert len(result.research_questions) >= 3
    assert len(result.search_topics) >= 3