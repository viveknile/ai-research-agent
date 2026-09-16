from app.agents.state import ResearchState
from app.ai.provider import get_ai_provider
from app.schemas.research import SearchQueries


ai_provider = get_ai_provider()

MAX_SEARCH_QUERIES = 8


async def generate_queries(state: ResearchState) -> dict:
    query = state["query"]
    research_plan = state.get("research_plan", {})
    research_gaps = state.get("research_gaps", [])
    iteration = state.get("iteration", 0)

    print(
        "[ResearchPilot] Generating search queries "
        f"(iteration {iteration + 1})..."
    )

    if research_gaps:
        gap_text = "\n".join(
            f"- {gap}"
            for gap in research_gaps
        )

        prompt = f"""
You are a research search-query generator.

The original research question is:

{query}

The research plan is:

{research_plan}

The current research round is:

{iteration + 1}

The previous research identified these gaps:

{gap_text}

Generate targeted follow-up web search queries that specifically
address these research gaps.

Requirements:

1. Generate no more than {MAX_SEARCH_QUERIES} queries.
2. Avoid duplicate queries.
3. Avoid repeating information already researched.
4. Focus on the most important missing information.
5. Prefer specific queries over broad queries.

Return only actual JSON data matching the requested schema.
Do not return the schema itself.
"""

    else:
        prompt = f"""
You are a research search-query generator.

The original research question is:

{query}

The research plan is:

{research_plan}

Generate focused web search queries that will help answer
the research question.

Requirements:

1. Generate no more than {MAX_SEARCH_QUERIES} queries.
2. Cover the most important concepts.
3. Cover important technologies or entities.
4. Include comparisons where relevant.
5. Include current information where relevant.
6. Include practical or real-world considerations.
7. Avoid duplicate queries.
8. Avoid overly broad queries.
9. Prioritize quality over quantity.

Return only actual JSON data matching the requested schema.
Do not return the schema itself.
"""

    result = await ai_provider.generate_structured(
        prompt,
        SearchQueries,
    )

    queries = []

    for query_item in result.queries:
        cleaned_query = query_item.strip()

        if not cleaned_query:
            continue

        if cleaned_query in queries:
            continue

        queries.append(cleaned_query)

        if len(queries) >= MAX_SEARCH_QUERIES:
            break

    print(
        "[ResearchPilot] Generated "
        f"{len(queries)} search queries."
    )

    return {
        "search_queries": queries,
        "iteration": iteration + 1,
    }