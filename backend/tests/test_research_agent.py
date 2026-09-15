import pytest

from app.agents.graph import research_graph
from app.agents.nodes import analyze_query
from app.agents.nodes import generate_queries
from app.agents.nodes import extract_evidence
from app.agents.nodes import analyze_findings
from app.agents.nodes import check_gaps
from app.ai.mock import MockAIProvider


@pytest.mark.asyncio
async def test_research_graph(monkeypatch):

    mock_provider = MockAIProvider()

    # --------------------------------------------------
    # Replace Gemini with Mock AI
    # --------------------------------------------------

    monkeypatch.setattr(
        analyze_query,
        "gemini_provider",
        mock_provider,
    )

    monkeypatch.setattr(
        generate_queries,
        "gemini_provider",
        mock_provider,
    )

    monkeypatch.setattr(
        extract_evidence,
        "gemini_provider",
        mock_provider,
    )

    monkeypatch.setattr(
        analyze_findings,
        "gemini_provider",
        mock_provider,
    )

    monkeypatch.setattr(
        check_gaps,
        "gemini_provider",
        mock_provider,
    )

    # --------------------------------------------------
    # Initial Research State
    # --------------------------------------------------

    initial_state = {
        "query": "Compare AI agent frameworks in 2026",
    }

    # --------------------------------------------------
    # Run Research Graph
    # --------------------------------------------------

    result = await research_graph.ainvoke(
        initial_state
    )

    # --------------------------------------------------
    # Query
    # --------------------------------------------------

    assert (
        result["query"]
        == "Compare AI agent frameworks in 2026"
    )

    # --------------------------------------------------
    # Research Plan
    # --------------------------------------------------

    research_plan = result["research_plan"]

    assert research_plan["objective"]
    assert research_plan["research_questions"]
    assert research_plan["search_topics"]

    # --------------------------------------------------
    # Search Queries
    # --------------------------------------------------

    search_queries = result["search_queries"]

    assert search_queries
    assert len(search_queries) >= 5

    # --------------------------------------------------
    # Search Results
    # --------------------------------------------------

    sources = result["sources"]

    assert sources
    assert len(sources) > 0

    for source in sources:

        assert source["id"]
        assert source["title"]
        assert source["url"]
        assert source["domain"]

    # --------------------------------------------------
    # Fetched Documents
    # --------------------------------------------------

    documents = result["documents"]

    assert documents
    assert len(documents) > 0

    for document in documents:

        assert document["source_id"]
        assert document["url"]
        assert document["title"]
        assert document["content"]
        assert document["domain"]

    # --------------------------------------------------
    # Evidence
    # --------------------------------------------------

    evidence = result["evidence"]

    assert evidence
    assert len(evidence) > 0

    for item in evidence:

        assert item["id"]
        assert item["source_id"]
        assert item["claim"]
        assert item["evidence_text"]

        assert (
            0.0
            <= item["confidence"]
            <= 1.0
        )

    # --------------------------------------------------
    # Findings
    # --------------------------------------------------

    findings = result["findings"]

    assert findings
    assert len(findings) > 0

    for finding in findings:

        assert finding["id"]
        assert finding["statement"]

        assert (
            0.0
            <= finding["confidence"]
            <= 1.0
        )

        assert finding[
            "supporting_evidence_ids"
        ]

    # --------------------------------------------------
    # Research Gaps
    # --------------------------------------------------

    research_gaps = result["research_gaps"]

    assert isinstance(
        research_gaps,
        list,
    )