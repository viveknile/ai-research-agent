from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.research import (
    ResearchRequest,
    ResearchResponse,
)
from app.services.research_service import (
    research_results,
    research_service,
)


router = APIRouter(
    prefix="/research",
    tags=["Research"],
)


@router.post(
    "",
    response_model=ResearchResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_research(
    request: ResearchRequest,
) -> ResearchResponse:

    return await research_service.create_research(
        request
    )


@router.get("/{research_id}")
async def get_research(
    research_id: UUID,
):

    research = research_results.get(
        str(research_id)
    )

    if research is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research not found.",
        )

    return research