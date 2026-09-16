from app.core.config import settings
from app.tools.base import FetchProvider
from app.tools.fetch import HTTPFetchProvider
from app.tools.mock import MockFetchProvider


def get_fetch_provider() -> FetchProvider:
    """
    Return the appropriate fetch provider based on the research mode.

    mock:
        Uses MockFetchProvider.
        No real HTTP requests are made.

    real:
        Uses HTTPFetchProvider.
        Real webpages are fetched.
    """

    if settings.research_mode.lower() == "real":
        return HTTPFetchProvider()

    return MockFetchProvider()