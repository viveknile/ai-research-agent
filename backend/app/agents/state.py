from typing import TypedDict


class ResearchState(TypedDict, total=False):
    research_id: str

    query: str

    research_plan: dict

    search_queries: list[str]

    sources: list[dict]

    documents: list[dict]

    evidence: list[dict]

    findings: list[dict]

    research_gaps: list[str]

    iteration: int

    max_iterations: int

    final_report: dict

    errors: list[str]