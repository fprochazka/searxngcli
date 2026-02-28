"""Rich output formatting for SearXNG CLI."""

from rich.table import Table

from .logging import console
from .models import EngineInfo, SearchResponse


def print_results(response: SearchResponse, num: int = 10) -> None:
    """Print formatted search results."""
    if not response.results:
        console.print("[yellow]No results found.[/yellow]")
        return

    results = response.results[:num]

    for i, result in enumerate(results, 1):
        console.print(f"\n[bold]{i}. {result.title}[/bold]")
        console.print(f"   [dim]{result.url}[/dim]")
        if result.content:
            console.print(f"   {result.content}")
        engines_str = ", ".join(result.engines) if result.engines else result.engine
        meta_parts = []
        if engines_str:
            meta_parts.append(f"engines: {engines_str}")
        if result.category:
            meta_parts.append(f"category: {result.category}")
        if result.score:
            meta_parts.append(f"score: {result.score:.1f}")
        if result.published_date:
            meta_parts.append(f"date: {result.published_date}")
        if meta_parts:
            console.print(f"   [dim italic]{' | '.join(meta_parts)}[/dim italic]")

    console.print(f"\n[dim]Showing {len(results)} of {response.number_of_results} results[/dim]")

    if response.suggestions:
        console.print(f"[dim]Suggestions: {', '.join(response.suggestions)}[/dim]")

    if response.corrections:
        console.print(f"[dim]Corrections: {', '.join(response.corrections)}[/dim]")

    if response.unresponsive_engines:
        names = [e[0] if isinstance(e, list) and e else str(e) for e in response.unresponsive_engines]
        console.print(f"[yellow]Unresponsive engines: {', '.join(names)}[/yellow]")


def print_engines(engines: list[EngineInfo]) -> None:
    """Print a table of available engines."""
    table = Table(title="Available Engines")
    table.add_column("Name", style="bold")
    table.add_column("Shortcut", style="dim")
    table.add_column("Categories")
    table.add_column("Enabled")

    for engine in sorted(engines, key=lambda e: e.name):
        table.add_row(
            engine.name,
            engine.shortcut,
            ", ".join(engine.categories),
            "[green]yes[/green]" if engine.enabled else "[red]no[/red]",
        )

    console.print(table)


def print_categories(categories: list[str]) -> None:
    """Print available categories."""
    console.print("[bold]Available Categories:[/bold]")
    for cat in sorted(categories):
        console.print(f"  • {cat}")
