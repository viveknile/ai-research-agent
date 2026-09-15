from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI

from app.ai.base import AIProvider
from app.core.config import settings


class GeminiProvider(AIProvider):
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            google_api_key=settings.gemini_api_key,
        )

    async def generate(self, prompt: str) -> str:
        response = await self.model.ainvoke(prompt)

        if isinstance(response.content, str):
            return response.content

        if isinstance(response.content, list):
            text_parts = []

            for part in response.content:
                if isinstance(part, dict) and part.get("type") == "text":
                    text_parts.append(part.get("text", ""))

            return "".join(text_parts)

        return str(response.content)

    async def generate_structured(
        self,
        prompt: str,
        schema: type[BaseModel],
    ) -> BaseModel:
        structured_model = self.model.with_structured_output(schema)

        return await structured_model.ainvoke(prompt)