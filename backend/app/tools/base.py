from abc import ABC, abstractmethod

from app.schemas.research import SearchResult, WebDocument


class SearchProvider(ABC):

    @abstractmethod
    async def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:
        """Search the web and return normalized search results."""
        raise NotImplementedError


class FetchProvider(ABC):

    @abstractmethod
    async def fetch(
        self,
        url: str,
        source_id: str,
    ) -> WebDocument:
        """Fetch and extract readable content from a webpage."""
        raise NotImplementedError