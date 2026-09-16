from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):
    objective: str
    research_questions: list[str]
    search_topics: list[str]


class SearchQueries(BaseModel):
    queries: list[str]


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

    # Some OpenRouter free models may omit this field.
    # Use a neutral fallback instead of failing the entire run.
    confidence: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
    )


class EvidenceExtraction(BaseModel):
    evidence: list[Evidence]


class Finding(BaseModel):
    id: str
    statement: str

    # Some OpenRouter free models may omit this field.
    confidence: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
    )

    supporting_evidence_ids: list[str]


class FindingAnalysis(BaseModel):
    findings: list[Finding]


class ResearchGaps(BaseModel):
    research_gaps: list[str]


# ============================================================
# Report Schemas
# ============================================================


class ReportFinding(BaseModel):
    statement: str

    # Some OpenRouter free models may omit this field.
    confidence: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
    )

    evidence_ids: list[str]


class ReportDraft(BaseModel):
    title: str
    executive_summary: str
    findings: list[ReportFinding]


class ReportCitation(BaseModel):
    citation_id: str
    source_id: str
    title: str
    url: str
    domain: str


class FinalReportFinding(BaseModel):
    statement: str

    confidence: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
    )

    citation_ids: list[str]


class ResearchReport(BaseModel):
    title: str
    executive_summary: str
    findings: list[FinalReportFinding]
    citations: list[ReportCitation]


# ============================================================
# API Schemas
# ============================================================


class ResearchRequest(BaseModel):
    query: str = Field(
        min_length=5,
        max_length=1000,
        description="Research question to investigate",
    )

    depth: Literal[
        "quick",
        "standard",
        "deep",
    ] = "standard"


class ResearchResponse(BaseModel):
    research_id: UUID
    status: str