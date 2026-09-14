from app.agents.state import ResearchState
from app.ai.gemini import GeminiProvider
from app.schemas.research import ResearchPlan


gemini_provider = GeminiProvider()


async def analyze_query(
    state: ResearchState,
) -> ResearchState:

    query = state["query"]

    prompt = f"""
You are a research planning assistant.

Analyze the following research question:

{query}

Create a research plan.

The plan should:
1. Clearly identify the main objective.
2. Break the objective into useful research questions.
3. Identify search topics that should be investigated on the web.

Focus on producing a practical plan for a web research agent.
"""

    research_plan = await gemini_provider.generate_structured(
        prompt,
        ResearchPlan,
    )

    return {
        **state,
        "research_plan": research_plan.model_dump(),
    }