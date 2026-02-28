"""SearXNG HTTP client."""

import httpx

from .logging import get_logger
from .models import EngineInfo, SearchResponse

logger = get_logger(__name__)

DEFAULT_TIMEOUT = 30.0


class SearXNGClient:
    """Client for interacting with a SearXNG instance."""

    def __init__(self, base_url: str, timeout: float = DEFAULT_TIMEOUT) -> None:
        self.base_url = base_url
        self.timeout = timeout

    def search(
        self,
        query: str,
        categories: str | None = None,
        engines: str | None = None,
        language: str | None = None,
        page: int = 1,
        time_range: str | None = None,
        safe_search: int | None = None,
    ) -> SearchResponse:
        """Execute a search query."""
        params: dict[str, str | int] = {
            "q": query,
            "format": "json",
            "pageno": page,
        }

        if categories:
            params["categories"] = categories
        if engines:
            params["engines"] = engines
        if language:
            params["language"] = language
        if time_range:
            params["time_range"] = time_range
        if safe_search is not None:
            params["safesearch"] = safe_search

        logger.debug("Search params: %s", params)

        response = httpx.get(
            f"{self.base_url}/search",
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()

        data = response.json()
        logger.debug("Got %d results", len(data.get("results", [])))

        return SearchResponse.from_dict(data)

    def get_config(self) -> dict:
        """Get the SearXNG instance configuration."""
        response = httpx.get(
            f"{self.base_url}/config",
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_engines(self) -> list[EngineInfo]:
        """Get list of available engines."""
        config = self.get_config()
        engines = config.get("engines", [])
        return [EngineInfo.from_dict(e) for e in engines]

    def get_categories(self) -> list[str]:
        """Get list of available categories."""
        config = self.get_config()
        return config.get("categories", [])
