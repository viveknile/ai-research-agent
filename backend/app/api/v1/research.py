
from fastapi import APIRouter, status

from app.schemas.research import ResearchRequest, ResearchResponse
from app.services.research_service import research_service


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

    return await research_service.create_research(request)