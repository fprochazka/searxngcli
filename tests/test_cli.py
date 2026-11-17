"""Tests for the search command."""

import io
import json
from typing import Any

import pytest
from typer.testing import CliRunner

from searxngcli import cli
from searxngcli.logging import create_console
from searxngcli.models import SearchResponse, SearchResult


class FakeClient:
    def __init__(self, response: SearchResponse) -> None:
        self.response = response

    def search(self, **kwargs: Any) -> SearchResponse:
        return self.response


def _search_json(monkeypatch: pytest.MonkeyPatch, *args: str) -> dict[str, Any]:
    results = [SearchResult(title=f"Result {i}", url=f"https://example.com/{i}") for i in range(1, 6)]
    response = SearchResponse(query="q", number_of_results=5, results=results, suggestions=["q tutorial"])
    monkeypatch.setattr(cli._ctx, "get_client", lambda: FakeClient(response))
    out = io.StringIO()
    monkeypatch.setattr(cli, "console", create_console(file=out))

    result = CliRunner().invoke(cli.app, ["search", "q", "--json", *args])

    assert result.exit_code == 0, result.output
    payload: dict[str, Any] = json.loads(out.getvalue())
    return payload


def test_json_output_keeps_only_num_results(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _search_json(monkeypatch, "--num", "2")

    assert [r["url"] for r in payload["results"]] == ["https://example.com/1", "https://example.com/2"]
    assert payload["number_of_results"] == 5
    assert payload["suggestions"] == ["q tutorial"]


def test_json_output_without_num_keeps_all_results(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _search_json(monkeypatch)

    assert len(payload["results"]) == 5
