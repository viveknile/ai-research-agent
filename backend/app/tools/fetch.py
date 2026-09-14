from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from app.core.security import validate_url
from app.schemas.research import WebDocument
from app.tools.base import FetchProvider


class HTTPFetchProvider(FetchProvider):

    async def fetch(
        self,
        url: str,
        source_id: str,
    ) -> WebDocument:

        validate_url(url)

        async with httpx.AsyncClient(
            timeout=10.0,
            follow_redirects=True,
        ) as client:

            response = await client.get(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 "
                        "(KHTML, like Gecko) "
                        "Chrome/131.0 Safari/537.36"
                    ),
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

        # Try to extract the webpage title.
        title = ""

        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        # If <title> is unavailable, try the main heading.
        if not title:
            heading = soup.find("h1")

            if heading:
                title = heading.get_text(
                    separator=" ",
                    strip=True,
                )

        # Final fallback: use the hostname.
        if not title:
            title = urlparse(url).netloc

        content = soup.get_text(
            separator=" ",
            strip=True,
        )

        domain = urlparse(url).netloc

        return WebDocument(
            source_id=source_id,
            url=url,
            title=title,
            content=content,
            domain=domain,
        )