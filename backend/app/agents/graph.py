from langgraph.graph import END, START, StateGraph

from app.agents.state import ResearchState
from app.agents.nodes.analyze_query import analyze_query
from app.agents.nodes.generate_queries import generate_queries
from app.agents.nodes.search_web import search_web


def build_research_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("analyze_query", analyze_query)
    graph.add_node("generate_queries", generate_queries)
    graph.add_node("search_web", search_web)

    graph.add_edge(START, "analyze_query")
    graph.add_edge("analyze_query", "generate_queries")
    graph.add_edge("generate_queries", "search_web")
    graph.add_edge("search_web", END)

    return graph.compile()


research_graph = build_research_graph()