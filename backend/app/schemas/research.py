from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    query: str = Field(
        min_length=5,
        max_length=1000,
        description="Research question to investigate",
    )

    depth: Literal["quick", "standard", "deep"] = "standard"


class ResearchResponse(BaseModel):
    research_id: UUID
    status: str