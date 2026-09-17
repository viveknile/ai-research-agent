import asyncio
import json
import re

from pydantic import BaseModel
from langchain_openai import ChatOpenAI

from app.ai.base import AIProvider
from app.core.config import settings


class OpenRouterProvider(AIProvider):
    def __init__(self):
        self.model = ChatOpenAI(
            model=settings.openrouter_model,
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=0,
            timeout=90,
            max_retries=0,
        )

    async def generate(self, prompt: str) -> str:
        print(
            "[ResearchPilot] OpenRouter: "
            "starting request..."
        )

        response = await self.model.ainvoke(prompt)

        print(
            "[ResearchPilot] OpenRouter: "
            "request completed."
        )

        return self._extract_text(response.content)

    async def generate_structured(
        self,
        prompt: str,
        schema: type[BaseModel],
    ) -> BaseModel:

        print(
            "[ResearchPilot] OpenRouter structured request "
            f"started: {schema.__name__}"
        )

        schema_json = json.dumps(
            schema.model_json_schema(),
            indent=2,
        )

        structured_prompt = self._build_structured_prompt(
            prompt=prompt,
            schema_json=schema_json,
        )

        first_content = "No response"
        retry_content = "No response"
        first_error: Exception | None = None

        # ====================================================
        # First attempt
        # ====================================================

        try:
            print(
                "[ResearchPilot] "
                f"{schema.__name__}: attempt 1/1"
            )

            response = await self.model.ainvoke(
                structured_prompt
            )

            first_content = self._extract_text(
                response.content
            )

            print(
                "[ResearchPilot] Raw structured response "
                f"for {schema.__name__}:"
            )
            print(first_content)

            data = self._parse_json(first_content)

            data = self._normalize_data(
                data,
                schema,
            )

            self._validate_not_schema(data)

            result = schema.model_validate(data)

            print(
                "[ResearchPilot] OpenRouter structured "
                f"request completed: {schema.__name__}"
            )

            return result

        except Exception as exc:
            first_error = exc

            print(
                "[ResearchPilot] Structured request failed "
                f"for {schema.__name__}: {exc}"
            )

        # ====================================================
        # Retry
        # ====================================================

        # Do not retry rate-limit errors.
        if self._is_rate_limit_error(first_error):
            print(
                "[ResearchPilot] Rate limit detected. "
                "Skipping retry."
            )

            raise ValueError(
                f"OpenRouter rate limit reached for "
                f"{schema.__name__}: {first_error}"
            ) from first_error

        print(
            "[ResearchPilot] Retrying structured request..."
        )

        retry_prompt = self._build_retry_prompt(
            prompt=prompt,
            schema_json=schema_json,
            error=str(first_error),
        )

        try:
            print(
                "[ResearchPilot] "
                f"{schema.__name__}: retry attempt 1/1"
            )

            response = await self.model.ainvoke(
                retry_prompt
            )

            retry_content = self._extract_text(
                response.content
            )

            print(
                "[ResearchPilot] Raw retry response "
                f"for {schema.__name__}:"
            )
            print(retry_content)

            retry_data = self._parse_json(
                retry_content
            )

            retry_data = self._normalize_data(
                retry_data,
                schema,
            )

            self._validate_not_schema(
                retry_data
            )

            result = schema.model_validate(
                retry_data
            )

            print(
                "[ResearchPilot] Retry successful: "
                f"{schema.__name__}"
            )

            return result

        except Exception as second_error:
            print(
                "[ResearchPilot] Retry failed for "
                f"{schema.__name__}: {second_error}"
            )

            raise ValueError(
                f"OpenRouter failed to generate valid "
                f"{schema.__name__} data.\n\n"
                f"First response:\n"
                f"{first_content}\n\n"
                f"Retry response:\n"
                f"{retry_content}"
            ) from second_error

    # ========================================================
    # Rate Limit Detection
    # ========================================================

    @staticmethod
    def _is_rate_limit_error(
        error: Exception | None,
    ) -> bool:

        if error is None:
            return False

        error_text = str(error).lower()

        rate_limit_indicators = [
            "429",
            "rate limit",
            "rate_limit",
            "too many requests",
            "free-models-per-day",
            "quota",
        ]

        return any(
            indicator in error_text
            for indicator in rate_limit_indicators
        )

    # ========================================================
    # Structured Prompt
    # ========================================================

    @staticmethod
    def _build_structured_prompt(
        prompt: str,
        schema_json: str,
    ) -> str:

        return f"""
You are a structured data extraction assistant.

TASK:

{prompt}

EXPECTED JSON STRUCTURE:

{schema_json}

IMPORTANT:

Return actual DATA matching the structure.

Do NOT return the JSON schema.

Do NOT return:
- properties
- definitions
- $defs
- required
- schema metadata

Return exactly ONE JSON object.

Do NOT return Markdown.

Do NOT use code fences.

Do NOT explain your reasoning.

Do NOT add text before the JSON.

Do NOT add text after the JSON.

Every required field must contain actual values.

Return the JSON object now.
"""

    # ========================================================
    # Retry Prompt
    # ========================================================

    @staticmethod
    def _build_retry_prompt(
        prompt: str,
        schema_json: str,
        error: str,
    ) -> str:

        return f"""
Return ONLY valid JSON DATA.

TASK:

{prompt}

EXPECTED JSON STRUCTURE:

{schema_json}

The previous attempt failed.

Previous error:

{error}

IMPORTANT:

Return actual values.

Do NOT return the schema.

Do NOT return:
- properties
- definitions
- $defs
- required
- type descriptions
- schema metadata

Do NOT explain anything.

Do NOT use Markdown.

Do NOT use code fences.

Do NOT return reasoning.

Return exactly ONE JSON object.

The response must begin with {{ and end with }}.

Return the JSON object now.
"""

    # ========================================================
    # Text Extraction
    # ========================================================

    @staticmethod
    def _extract_text(
        content,
    ) -> str:

        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):

            text_parts = []

            for part in content:

                if isinstance(part, dict):

                    if part.get("type") == "text":

                        text_parts.append(
                            part.get(
                                "text",
                                "",
                            )
                        )

            return "".join(
                text_parts
            ).strip()

        return str(content).strip()

    # ========================================================
    # JSON Parsing
    # ========================================================

    @staticmethod
    def _parse_json(
        content: str,
    ) -> dict:

        content = content.strip()

        if not content:
            raise ValueError(
                "OpenRouter returned an empty response."
            )

        # Remove Markdown code fences.
        content = re.sub(
            r"^```(?:json)?\s*",
            "",
            content,
            flags=re.IGNORECASE,
        )

        content = re.sub(
            r"\s*```$",
            "",
            content,
        )

        content = content.strip()

        # First try the entire response.
        try:

            data = json.loads(
                content
            )

            if not isinstance(data, dict):
                raise ValueError(
                    "OpenRouter returned JSON, "
                    "but it was not a JSON object."
                )

            return data

        except json.JSONDecodeError:
            pass

        # Try extracting the outer JSON object.
        start = content.find("{")
        end = content.rfind("}")

        if start != -1 and end != -1 and end > start:

            json_candidate = content[
                start : end + 1
            ]

            data = json.loads(
                json_candidate
            )

            if not isinstance(data, dict):
                raise ValueError(
                    "Extracted JSON is not an object."
                )

            return data

        raise ValueError(
            "Could not find a valid JSON object "
            "in the OpenRouter response."
        )

    # ========================================================
    # Schema Detection
    # ========================================================

    @staticmethod
    def _validate_not_schema(
        data: dict,
    ) -> None:

        if not isinstance(data, dict):
            return

        schema_keys = {
            "properties",
            "definitions",
            "$defs",
        }

        if schema_keys.intersection(
            data.keys()
        ):

            raise ValueError(
                "Model returned JSON schema "
                "instead of actual data."
            )

    # ========================================================
    # Model Output Normalization
    # ========================================================

    @staticmethod
    def _normalize_data(
        data: dict,
        schema: type[BaseModel],
    ) -> dict:

        if not isinstance(data, dict):
            return data

        # ----------------------------------------------------
        # ReportDraft normalization
        # ----------------------------------------------------

        if schema.__name__ == "ReportDraft":

            findings = data.get(
                "findings"
            )

            if isinstance(
                findings,
                list,
            ):

                normalized_findings = []

                for finding in findings:

                    if not isinstance(
                        finding,
                        dict,
                    ):
                        continue

                    statement = finding.get(
                        "statement"
                    )

                    if isinstance(
                        statement,
                        dict,
                    ):

                        title = statement.get(
                            "title"
                        )

                        if isinstance(
                            title,
                            str,
                        ):

                            finding = {
                                **finding,
                                "statement": title,
                            }

                    if (
                        "confidence"
                        not in finding
                    ):

                        finding = {
                            **finding,
                            "confidence": 0.8,
                        }

                    if (
                        "evidence_ids"
                        not in finding
                    ):

                        finding = {
                            **finding,
                            "evidence_ids": [],
                        }

                    normalized_findings.append(
                        finding
                    )

                data = {
                    **data,
                    "findings": normalized_findings,
                }

        return data