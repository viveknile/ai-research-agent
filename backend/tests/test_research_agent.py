import pytest

from app.agents.graph import research_graph


@pytest.mark.asyncio
async def test_research_graph():
    initial_state = {
        "query": "Compare AI agent frameworks in 2026",
    }

    result = await research_graph.ainvoke(initial_state)

    assert result["query"] == "Compare AI agent frameworks in 2026"

    research_plan = result["research_plan"]

    assert research_plan["objective"]
    assert research_plan["research_questions"]
    assert research_plan["search_topics"]

    search_queries = result["search_queries"]

    assert search_queries
    assert len(search_queries) >= 5

    sources = result["sources"]

    assert sources
    assert len(sources) > 0

    for source in sources:
        assert source["title"]
        assert source["url"]
        assert source["domain"]