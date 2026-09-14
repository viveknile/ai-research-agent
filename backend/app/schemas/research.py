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
    id: str
    title: str
    url: str
    snippet: str
    content: str | None = None
    published_date: str | None = None
    domain: str


class WebDocument(BaseModel):
    source_id: str
    url: str
    title: str
    content: str
    domain: str

class Evidence(BaseModel):
    id: str
    source_id: str
    claim: str
    evidence_text: str
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )


class Finding(BaseModel):
    id: str
    statement: str
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )
    supporting_evidence_ids: list[str]