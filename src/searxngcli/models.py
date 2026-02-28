"""Data models for SearXNG CLI."""

from dataclasses import dataclass, field


@dataclass
class SearchResult:
    """A single search result."""

    title: str = ""
    url: str = ""
    content: str = ""
    engine: str = ""
    engines: list[str] = field(default_factory=list)
    category: str = ""
    score: float = 0.0
    published_date: str = ""
    thumbnail: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "SearchResult":
        return cls(
            title=data.get("title", ""),
            url=data.get("url", ""),
            content=data.get("content", ""),
            engine=data.get("engine", ""),
            engines=data.get("engines", []),
            category=data.get("category", ""),
            score=data.get("score", 0.0),
            published_date=data.get("publishedDate", ""),
            thumbnail=data.get("thumbnail", ""),
        )


@dataclass
class SearchResponse:
    """Response from a search query."""

    query: str = ""
    number_of_results: int = 0
    results: list[SearchResult] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    corrections: list[str] = field(default_factory=list)
    unresponsive_engines: list[list[str]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "SearchResponse":
        return cls(
            query=data.get("query", ""),
            number_of_results=data.get("number_of_results", 0),
            results=[SearchResult.from_dict(r) for r in data.get("results", [])],
            suggestions=data.get("suggestions", []),
            corrections=data.get("corrections", []),
            unresponsive_engines=data.get("unresponsive_engines", []),
        )


@dataclass
class EngineInfo:
    """Information about a search engine."""

    name: str = ""
    categories: list[str] = field(default_factory=list)
    shortcut: str = ""
    enabled: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> "EngineInfo":
        return cls(
            name=data.get("name", ""),
            categories=data.get("categories", []),
            shortcut=data.get("shortcut", ""),
            enabled=data.get("enabled", True),
        )
