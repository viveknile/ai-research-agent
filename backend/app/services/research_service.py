from uuid import UUID, uuid4

from app.schemas.research import ResearchRequest, ResearchResponse


class ResearchService:

    async def create_research(
        self,
        request: ResearchRequest,
    ) -> ResearchResponse:

        research_id: UUID = uuid4()

        # Agent/database integration will come later.
        # For now, we are creating the research session ID.

        return ResearchResponse(
            research_id=research_id,
            status="queued",
        )


research_service = ResearchService()