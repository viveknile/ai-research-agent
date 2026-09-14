from abc import ABC, abstractmethod

from app.schemas.research import SearchResult


class SearchProvider(ABC):

    @abstractmethod
    async def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:
        """Search the web and return normalized search results."""
        raise NotImplementedError