from langgraph.graph import END, START, StateGraph

from app.agents.state import ResearchState
from app.agents.nodes.analyze_query import analyze_query


def build_research_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("analyze_query", analyze_query)

    graph.add_edge(START, "analyze_query")
    graph.add_edge("analyze_query", END)

    return graph.compile()


research_graph = build_research_graph()