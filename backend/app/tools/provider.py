from app.core.config import settings
from app.tools.base import SearchProvider
from app.tools.mock import MockSearchProvider
from app.tools.search import TavilySearchProvider


def get_search_provider() -> SearchProvider:
    """
    Return the appropriate search provider based on the research mode.

    mock:
        Uses MockSearchProvider.
        No Tavily API requests are made.

    real:
        Uses TavilySearchProvider.
        Real web searches are performed.
    """

    if settings.research_mode.lower() == "real":
        return TavilySearchProvider()

    return MockSearchProvider()