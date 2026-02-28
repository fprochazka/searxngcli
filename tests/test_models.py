"""Tests for data models."""

from searxngcli.models import EngineInfo, SearchResponse, SearchResult


class TestSearchResult:
    def test_from_dict_full(self):
        data = {
            "title": "Example",
            "url": "https://example.com",
            "content": "Some content",
            "engine": "google",
            "engines": ["google", "bing"],
            "category": "general",
            "score": 1.5,
            "publishedDate": "2025-01-01",
            "thumbnail": "https://example.com/thumb.jpg",
        }
        result = SearchResult.from_dict(data)
        assert result.title == "Example"
        assert result.url == "https://example.com"
        assert result.content == "Some content"
        assert result.engine == "google"
        assert result.engines == ["google", "bing"]
        assert result.category == "general"
        assert result.score == 1.5
        assert result.published_date == "2025-01-01"
        assert result.thumbnail == "https://example.com/thumb.jpg"

    def test_from_dict_minimal(self):
        result = SearchResult.from_dict({})
        assert result.title == ""
        assert result.url == ""
        assert result.engines == []
        assert result.score == 0.0


class TestSearchResponse:
    def test_from_dict(self):
        data = {
            "query": "test",
            "number_of_results": 100,
            "results": [
                {"title": "Result 1", "url": "https://example.com/1"},
                {"title": "Result 2", "url": "https://example.com/2"},
            ],
            "suggestions": ["test suggestion"],
            "corrections": [],
            "unresponsive_engines": [],
        }
        response = SearchResponse.from_dict(data)
        assert response.query == "test"
        assert response.number_of_results == 100
        assert len(response.results) == 2
        assert response.results[0].title == "Result 1"
        assert response.suggestions == ["test suggestion"]

    def test_from_dict_empty(self):
        response = SearchResponse.from_dict({})
        assert response.query == ""
        assert response.results == []


class TestEngineInfo:
    def test_from_dict(self):
        data = {
            "name": "google",
            "categories": ["general"],
            "shortcut": "g",
            "enabled": True,
        }
        engine = EngineInfo.from_dict(data)
        assert engine.name == "google"
        assert engine.categories == ["general"]
        assert engine.shortcut == "g"
        assert engine.enabled is True
