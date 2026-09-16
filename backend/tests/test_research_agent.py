import pytest

from app.agents.graph import research_graph
from app.agents.nodes import (
    analyze_findings,
    analyze_query,
    check_gaps,
    extract_evidence,
    fetch_sources,
    generate_queries,
    search_web,
)
from app.ai.mock import MockAIProvider
from app.tools.mock import (
    MockFetchProvider,
    MockSearchProvider,
)


@pytest.mark.asyncio
async def test_research_graph(monkeypatch):
    mock_ai_provider = MockAIProvider()
    mock_search_provider = MockSearchProvider()
    mock_fetch_provider = MockFetchProvider()

    # ==================================================
    # Mock AI
    # ==================================================

    monkeypatch.setattr(
        analyze_query,
        "ai_provider",
        mock_ai_provider,
    )

    monkeypatch.setattr(
        generate_queries,
        "ai_provider",
        mock_ai_provider,
    )

    monkeypatch.setattr(
        extract_evidence,
        "ai_provider",
        mock_ai_provider,
    )

    monkeypatch.setattr(
        analyze_findings,
        "ai_provider",
        mock_ai_provider,
    )

    monkeypatch.setattr(
        check_gaps,
        "ai_provider",
        mock_ai_provider,
    )

    # The report synthesis node also uses AI.
    #
    # Import it here so the test can replace its
    # module-level provider.

    from app.agents.nodes import synthesize_report

    monkeypatch.setattr(
        synthesize_report,
        "ai_provider",
        mock_ai_provider,
    )

    # ==================================================
    # Mock Search
    # ==================================================

    monkeypatch.setattr(
        search_web,
        "search_provider",
        mock_search_provider,
    )

    # ==================================================
    # Mock Fetch
    # ==================================================

    monkeypatch.setattr(
        fetch_sources,
        "fetch_provider",
        mock_fetch_provider,
    )

    # ==================================================
    # Initial state
    # ==================================================

    initial_state = {
        "research_id": "test-research-id",
        "query": (
            "Compare AI agent frameworks "
            "for Python development."
        ),
        "max_iterations": 2,
    }

    # ==================================================
    # Run complete graph
    # ==================================================

    result = await research_graph.ainvoke(
        initial_state
    )

    # ==================================================
    # Research assertions
    # ==================================================

    assert result["query"] == initial_state["query"]

    assert result["research_plan"]

    assert result["search_queries"]

    assert result["sources"]

    assert result["documents"]

    assert result["evidence"]

    assert result["findings"]

    assert "research_gaps" in result

    # ==================================================
    # Report assertions
    # ==================================================

    assert result["report_draft"]

    assert result["final_report"]

    final_report = result["final_report"]

    assert final_report["title"]

    assert final_report["executive_summary"]

    assert final_report["findings"]

    assert final_report["citations"]

    # ==================================================
    # Iteration
    # ==================================================

    assert result["iteration"] >= 1