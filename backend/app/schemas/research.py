from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):
    objective: str
    research_questions: list[str]
    search_topics: list[str]


class SearchQueries(BaseModel):
    queries: list[str]


class ResearchRequest(BaseModel):
    query: str = Field(
        min_length=5,
        max_length=1000,
        description="Research question to investigate",
    )
    depth: Literal["quick", "standard", "deep"] = "standard"

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    content: str | None = None
    published_date: str | None = None
    domain: str