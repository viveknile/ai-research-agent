
from app.agents.state import ResearchState
from app.ai.gemini import GeminiProvider
from app.schemas.research import SearchQueries


gemini_provider = GeminiProvider()


async def generate_queries(state: ResearchState) -> ResearchState:
    research_plan = state["research_plan"]

    prompt = f"""
You are a web research query generation assistant.

Based on the following research plan, generate search queries
that will help us find reliable and diverse information on the web.

Research plan:

Objective:
{research_plan["objective"]}

Research questions:
{research_plan["research_questions"]}

Search topics:
{research_plan["search_topics"]}

Generate 5 to 8 focused search queries.

Requirements:
- Each query should investigate a useful aspect of the research.
- Avoid duplicate or nearly identical queries.
- Cover different aspects of the research.
- Prefer specific queries over vague queries.
- Do not include explanations, only the search queries.
"""

    search_queries = await gemini_provider.generate_structured(
        prompt,
        SearchQueries,
    )

    return {
        **state,
        "search_queries": search_queries.queries,
    }