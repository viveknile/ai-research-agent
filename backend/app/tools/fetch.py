import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from app.core.security import validate_url
from app.schemas.research import WebDocument
from app.tools.base import FetchProvider


class HTTPFetchProvider(FetchProvider):

    async def fetch(self, url: str) -> WebDocument:

        validate_url(url)

        async with httpx.AsyncClient(
            timeout=10.0,
            follow_redirects=True,
        ) as client:

            response = await client.get(
                url,
                headers={
                    "User-Agent": "ResearchPilot/0.1",
                },
            )

            response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        for element in soup(
            ["script", "style", "nav", "footer", "header"]
        ):
            element.decompose()

        title = soup.title.string.strip() if soup.title else ""

        content = soup.get_text(
            separator=" ",
            strip=True,
        )

        domain = urlparse(url).netloc

        return WebDocument(
            url=url,
            title=title,
            content=content,
            domain=domain,
        )