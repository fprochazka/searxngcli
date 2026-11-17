"""Tests for the text output of search results and engines."""

import io

import pytest

from searxngcli import formatter
from searxngcli.logging import create_console
from searxngcli.models import EngineInfo, SearchResponse, SearchResult

LONG_URL = "https://stackoverflow.com/questions/42231161/asyncio-gather-vs-asyncio-wait-vs-asyncio-taskgroup-" + "x" * 9
LONG_CONTENT = "TaskGroup is created using an asynchronous context manager " * 5


def _response() -> SearchResponse:
    result = SearchResult(title="asyncio.gather vs asyncio.TaskGroup", url=LONG_URL, content=LONG_CONTENT)
    return SearchResponse(query="python asyncio taskgroup", results=[result], number_of_results=1)


def _use_console(monkeypatch: pytest.MonkeyPatch, **kwargs: object) -> io.StringIO:
    out = io.StringIO()
    monkeypatch.setattr(formatter, "console", create_console(file=out, **kwargs))
    return out


def test_piped_results_are_not_wrapped(monkeypatch: pytest.MonkeyPatch) -> None:
    out = _use_console(monkeypatch)

    formatter.print_results(_response())

    lines = out.getvalue().splitlines()
    assert f"   {LONG_URL}" in lines
    assert f"   {LONG_CONTENT}" in lines


def test_terminal_results_wrap_text_but_keep_url_whole(monkeypatch: pytest.MonkeyPatch) -> None:
    out = _use_console(monkeypatch, force_terminal=True, width=60, color_system=None)

    formatter.print_results(_response())

    lines = out.getvalue().splitlines()
    assert f"   {LONG_URL}" in lines
    assert f"   {LONG_CONTENT}" not in lines
    assert all(len(line) <= 60 for line in lines if LONG_URL not in line)


def test_piped_engines_table_is_not_wrapped(monkeypatch: pytest.MonkeyPatch) -> None:
    out = _use_console(monkeypatch)
    categories = ["general", "web", "news", "science", "it", "files", "social media", "videos"]

    formatter.print_engines([EngineInfo(name="a search engine with a long name", categories=categories)])

    assert any(", ".join(categories) in line for line in out.getvalue().splitlines())


def _scored_response() -> SearchResponse:
    result = SearchResult(
        title="TaskGroup",
        url="https://example.com",
        engines=["brave", "bing"],
        category="general",
        score=2.5,
        published_date="2025-07-30T00:00:00",
    )
    return SearchResponse(query="python asyncio taskgroup", results=[result], number_of_results=1)


def test_results_leave_out_engines_category_and_score(monkeypatch: pytest.MonkeyPatch) -> None:
    out = _use_console(monkeypatch)

    formatter.print_results(_scored_response())

    lines = out.getvalue().splitlines()
    assert "   date: 2025-07-30T00:00:00" in lines
    assert not any("engines:" in line or "category:" in line or "score:" in line for line in lines)


def test_verbose_results_show_engines_category_and_score(monkeypatch: pytest.MonkeyPatch) -> None:
    out = _use_console(monkeypatch)

    formatter.print_results(_scored_response(), verbose=True)

    assert (
        "   engines: brave, bing | category: general | score: 2.5 | date: 2025-07-30T00:00:00"
        in out.getvalue().splitlines()
    )
