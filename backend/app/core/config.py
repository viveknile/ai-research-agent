from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Research Agent"
    environment: str = "development"

    research_mode: str = "mock"

    # AI Provider
    ai_provider: str = "openrouter"

    # OpenRouter
    openrouter_api_key: str = ""
    openrouter_model: str = "openrouter/free"

    # Gemini
    gemini_api_key: str = ""

    # Tavily
    tavily_api_key: str = ""

    # Database - currently unused
    database_url: str = ""

    allowed_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()