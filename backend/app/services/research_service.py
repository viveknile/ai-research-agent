from uuid import UUID, uuid4

from app.agents.graph import research_graph
from app.schemas.research import (
    ResearchRequest,
    ResearchResponse,
)


research_results: dict[str, dict] = {}


NODE_PROGRESS = {
    "analyze_query": {
        "progress": 10,
        "step": 1,
        "label": "Understanding your question",
        "description": "Analyzing the research objective",
    },
    "generate_queries": {
        "progress": 20,
        "step": 2,
        "label": "Creating research plan",
        "description": "Breaking the question into research topics",
    },
    "search_web": {
        "progress": 35,
        "step": 3,
        "label": "Searching the web",
        "description": "Finding relevant sources",
    },
    "fetch_sources": {
        "progress": 45,
        "step": 4,
        "label": "Analyzing sources",
        "description": "Reading and processing source material",
    },
    "extract_evidence": {
        "progress": 60,
        "step": 5,
        "label": "Extracting evidence",
        "description": "Identifying useful evidence and claims",
    },
    "analyze_findings": {
        "progress": 70,
        "step": 6,
        "label": "Checking research gaps",
        "description": "Analyzing findings and evidence",
    },
    "check_gaps": {
        "progress": 78,
        "step": 6,
        "label": "Checking research gaps",
        "description": "Determining whether more research is needed",
    },
    "synthesize_report": {
        "progress": 90,
        "step": 7,
        "label": "Preparing report",
        "description": "Synthesizing the research findings",
    },
    "generate_report": {
        "progress": 98,
        "step": 7,
        "label": "Preparing report",
        "description": "Generating the final cited report",
    },
}


class ResearchService:

    async def create_research(
        self,
        request: ResearchRequest,
    ) -> ResearchResponse:

        research_id = uuid4()
        research_id_str = str(research_id)

        research_results[research_id_str] = {
            "research_id": research_id_str,
            "query": request.query,
            "depth": request.depth,
            "status": "running",
            "progress": 0,
            "step": 1,
            "current_step": "Understanding your question",
            "current_description": (
                "Analyzing the research objective"
            ),
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

        # Run the research in the background.
        import asyncio

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

        print(
            "[ResearchPilot] Research started: "
            f"{research_id}"
        )

        accumulated_state = dict(initial_state)

        try:
            async for chunk in research_graph.astream(
                initial_state,
                stream_mode="updates",
            ):

                if not isinstance(chunk, dict):
                    continue

                for node_name, node_update in chunk.items():

                    if node_name not in NODE_PROGRESS:
                        continue

                    if not isinstance(node_update, dict):
                        continue

                    accumulated_state.update(
                        node_update
                    )

                    progress_info = NODE_PROGRESS[
                        node_name
                    ]

                    current_progress = research_results[
                        research_id
                    ].get("progress", 0)

                    progress = max(
                        current_progress,
                        progress_info["progress"],
                    )

                    current_step = (
                        progress_info["label"]
                    )

                    current_description = (
                        progress_info["description"]
                    )

                    # If gap checking says more research is
                    # required, the next active stage is web search.
                    if node_name == "check_gaps":

                        gaps = node_update.get(
                            "research_gaps",
                            [],
                        )

                        iteration = accumulated_state.get(
                            "iteration",
                            1,
                        )

                        max_iterations = (
                            accumulated_state.get(
                                "max_iterations",
                                2,
                            )
                        )

                        if (
                            gaps
                            and iteration < max_iterations
                        ):
                            current_step = (
                                "Searching the web"
                            )
                            current_description = (
                                "Researching the remaining gaps"
                            )

                        else:
                            current_step = (
                                "Preparing report"
                            )
                            current_description = (
                                "Synthesizing the research findings"
                            )

                    research_results[
                        research_id
                    ].update(
                        {
                            "status": "running",
                            "progress": progress,
                            "step": progress_info["step"],
                            "current_step": current_step,
                            "current_description": (
                                current_description
                            ),
                        }
                    )

                    print(
                        "[ResearchPilot] Node completed: "
                        f"{node_name} "
                        f"({progress}%)"
                    )

            # The graph has completed.
            research_results[
                research_id
            ].update(
                {
                    "status": "completed",
                    "progress": 100,
                    "step": 7,
                    "current_step": "Research complete",
                    "current_description": (
                        "Your cited research report is ready"
                    ),
                    "result": accumulated_state,
                    "error": None,
                }
            )

            print(
                "[ResearchPilot] Research completed: "
                f"{research_id}"
            )

        except Exception as exc:

            error_message = str(exc)

            print(
                "[ResearchPilot] Research failed: "
                f"{error_message}"
            )

            research_results[
                research_id
            ].update(
                {
                    "status": "failed",
                    "progress": 0,
                    "current_step": "Research failed",
                    "current_description": (
                        "Research could not be completed"
                    ),
                    "result": None,
                    "error": error_message,
                }
            )

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