from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate a text response from the AI model."""
        raise NotImplementedError