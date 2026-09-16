from langgraph.graph import END, START, StateGraph

from app.agents.state import ResearchState
from app.agents.nodes.analyze_query import analyze_query
from app.agents.nodes.generate_queries import generate_queries
from app.agents.nodes.search_web import search_web
from app.agents.nodes.fetch_sources import fetch_sources
from app.agents.nodes.extract_evidence import extract_evidence
from app.agents.nodes.analyze_findings import analyze_findings
from app.agents.nodes.check_gaps import check_gaps
from app.agents.nodes.synthesize_report import synthesize_report
from app.agents.nodes.generate_report import generate_report


def route_after_gap_check(state: ResearchState) -> str:
    gaps = state.get("research_gaps", [])

    iteration = state.get(
        "iteration",
        1,
    )

    max_iterations = state.get(
        "max_iterations",
        3,
    )

    if gaps and iteration < max_iterations:
        return "research_more"

    return "finish"


def build_research_graph():
    graph = StateGraph(ResearchState)

    # --------------------------------------------------
    # Research phase
    # --------------------------------------------------

    graph.add_node(
        "analyze_query",
        analyze_query,
    )

    graph.add_node(
        "generate_queries",
        generate_queries,
    )

    graph.add_node(
        "search_web",
        search_web,
    )

    graph.add_node(
        "fetch_sources",
        fetch_sources,
    )

    graph.add_node(
        "extract_evidence",
        extract_evidence,
    )

    graph.add_node(
        "analyze_findings",
        analyze_findings,
    )

    graph.add_node(
        "check_gaps",
        check_gaps,
    )

    # --------------------------------------------------
    # Report phase
    # --------------------------------------------------

    graph.add_node(
        "synthesize_report",
        synthesize_report,
    )

    graph.add_node(
        "generate_report",
        generate_report,
    )

    # --------------------------------------------------
    # Initial flow
    # --------------------------------------------------

    graph.add_edge(
        START,
        "analyze_query",
    )

    graph.add_edge(
        "analyze_query",
        "generate_queries",
    )

    graph.add_edge(
        "generate_queries",
        "search_web",
    )

    graph.add_edge(
        "search_web",
        "fetch_sources",
    )

    graph.add_edge(
        "fetch_sources",
        "extract_evidence",
    )

    graph.add_edge(
        "extract_evidence",
        "analyze_findings",
    )

    graph.add_edge(
        "analyze_findings",
        "check_gaps",
    )

    # --------------------------------------------------
    # Research loop
    # --------------------------------------------------

    graph.add_conditional_edges(
        "check_gaps",
        route_after_gap_check,
        {
            "research_more": "generate_queries",
            "finish": "synthesize_report",
        },
    )

    # --------------------------------------------------
    # Report generation
    # --------------------------------------------------

    graph.add_edge(
        "synthesize_report",
        "generate_report",
    )

    graph.add_edge(
        "generate_report",
        END,
    )

    return graph.compile()


research_graph = build_research_graph()