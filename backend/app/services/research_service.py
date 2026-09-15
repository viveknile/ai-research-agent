import asyncio
from uuid import UUID, uuid4

from app.agents.graph import research_graph
from app.schemas.research import (
    ResearchRequest,
    ResearchResponse,
)


# Temporary in-memory storage.
#
# Supabase/database persistence will be added later.
research_results: dict[str, dict] = {}


class ResearchService:

    async def create_research(
        self,
        request: ResearchRequest,
    ) -> ResearchResponse:

        research_id = uuid4()
        research_id_str = str(research_id)

        # Create the job immediately.
        research_results[research_id_str] = {
            "research_id": research_id_str,
            "query": request.query,
            "depth": request.depth,
            "status": "running",
            "result": None,
            "error": None,
        }

        initial_state = {
            "research_id": research_id_str,
            "query": request.query,
            "max_iterations": self._get_max_iterations(
                request.depth
            ),
        }

        asyncio.create_task(
            self._run_research(
                research_id_str,
                initial_state,
            )
        )

        return ResearchResponse(
            research_id=research_id,
            status="running",
        )

    async def _run_research(
        self,
        research_id: str,
        initial_state: dict,
    ) -> None:

        try:

            result = await research_graph.ainvoke(
                initial_state
            )

            research_results[research_id] = {
                "research_id": research_id,
                "query": initial_state["query"],
                "status": "completed",
                "result": result,
                "error": None,
            }

        except Exception as exc:

            error_message = str(exc)

            print(
                f"Research failed: {error_message}"
            )

            research_results[research_id] = {
                "research_id": research_id,
                "query": initial_state["query"],
                "status": "failed",
                "result": None,
                "error": error_message,
            }

    @staticmethod
    def _get_max_iterations(
        depth: str,
    ) -> int:

        if depth == "quick":
            return 1

        if depth == "deep":
            return 3

        return 2


research_service = ResearchService()