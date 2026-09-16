from app.ai.base import AIProvider
from app.ai.gemini import GeminiProvider
from app.ai.mock import MockAIProvider
from app.ai.openrouter import OpenRouterProvider
from app.core.config import settings


def get_ai_provider() -> AIProvider:
    # Development / testing mode
    if settings.research_mode.lower() != "real":
        return MockAIProvider()

    # Real AI provider
    provider = settings.ai_provider.lower()

    if provider == "openrouter":
        return OpenRouterProvider()

    if provider == "gemini":
        return GeminiProvider()

    raise ValueError(
        f"Unsupported AI provider: {settings.ai_provider}"
    )