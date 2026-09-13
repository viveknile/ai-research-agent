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

        return response.content

    async def generate_structured(
        self,
        prompt: str,
        schema: type[BaseModel],
    ) -> BaseModel:

        structured_model = self.model.with_structured_output(schema)

        return await structured_model.ainvoke(prompt)