from app.agents.state import ResearchState
from app.ai.provider import get_ai_provider
from app.schemas.research import ResearchPlan


ai_provider = get_ai_provider()


async def analyze_query(state: ResearchState) -> dict:
    query = state["query"]

    prompt = f"""
You are a research planning assistant.

Analyze the following research question and create a structured research plan.

Research question:
{query}

Create a plan that includes:

1. The main objective of the research.
2. The important research questions that should be answered.
3. The major topics that should be searched.

Make the research plan specific and useful for a web research agent.
"""

    plan = await ai_provider.generate_structured(
        prompt,
        ResearchPlan,
    )

    return {
        "research_plan": plan.model_dump(),
    }