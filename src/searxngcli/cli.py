"""CLI entry point for SearXNG CLI."""

import json
import sys
from pathlib import Path
from typing import Annotated

import typer

from . import __version__
from .config import Config, get_config_path, load_config, save_config
from .context import get_context
from .logging import console, error_console, get_logger, setup_logging

app = typer.Typer(
    name="searxng",
    help="A command-line interface for SearXNG.",
    no_args_is_help=True,
    rich_markup_mode=None,
)

config_app = typer.Typer(
    name="config",
    help="Configuration management.",
    no_args_is_help=True,
    rich_markup_mode=None,
)
app.add_typer(config_app, name="config")

logger = get_logger(__name__)

_ctx = get_context()


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"searxng {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    config_path: Annotated[
        Path | None,
        typer.Option(
            "--config",
            "-c",
            help="Path to config file.",
            envvar="SEARXNG_CONFIG",
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Enable debug logging.",
            is_eager=True,
        ),
    ] = False,
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            "-V",
            help="Show version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    """SearXNG CLI - A command-line interface for SearXNG."""
    setup_logging(verbose=verbose)
    logger.debug("Debug logging enabled")

    _ctx.verbose = verbose

    if config_path:
        try:
            _ctx.config = load_config(config_path)
        except FileNotFoundError as e:
            error_console.print(f"[red]{e}[/red]")
            raise typer.Exit(1) from None


@app.command("search")
def search_command(
    query: Annotated[str, typer.Argument(help="Search query.")],
    categories: Annotated[
        str | None,
        typer.Option("--categories", "-c", help="Comma-separated categories (general, images, news, videos, etc.)."),
    ] = None,
    engines: Annotated[
        str | None,
        typer.Option("--engines", "-e", help="Comma-separated engines."),
    ] = None,
    language: Annotated[
        str | None,
        typer.Option("--language", "-l", help="Language code (en, de, cs, etc.)."),
    ] = None,
    num: Annotated[
        int,
        typer.Option("--num", "-n", help="Number of results to display."),
    ] = 10,
    page: Annotated[
        int,
        typer.Option("--page", "-p", help="Page number."),
    ] = 1,
    time_range: Annotated[
        str | None,
        typer.Option("--time-range", "-t", help="Time range: day, week, month, year."),
    ] = None,
    safe_search: Annotated[
        int | None,
        typer.Option("--safe-search", help="Safe search level: 0, 1, or 2."),
    ] = None,
    output_json: Annotated[
        bool,
        typer.Option("--json", help="Output raw JSON."),
    ] = False,
) -> None:
    """Search using SearXNG."""
    from .formatter import print_results

    client = _ctx.get_client()
    response = client.search(
        query=query,
        categories=categories,
        engines=engines,
        language=language,
        page=page,
        time_range=time_range,
        safe_search=safe_search,
    )

    if output_json:
        import json as json_mod

        console.print_json(
            json_mod.dumps(
                {
                    "query": response.query,
                    "number_of_results": response.number_of_results,
                    "results": [
                        {
                            "title": r.title,
                            "url": r.url,
                            "content": r.content,
                            "engine": r.engine,
                            "engines": r.engines,
                            "category": r.category,
                            "score": r.score,
                            "published_date": r.published_date,
                            "thumbnail": r.thumbnail,
                        }
                        for r in response.results
                    ],
                    "suggestions": response.suggestions,
                    "corrections": response.corrections,
                }
            )
        )
    else:
        print_results(response, num=num)


@app.command("engines")
def engines_command() -> None:
    """List available search engines."""
    from .formatter import print_engines

    client = _ctx.get_client()
    engines = client.get_engines()
    print_engines(engines)


@app.command("categories")
def categories_command() -> None:
    """List available search categories."""
    from .formatter import print_categories

    client = _ctx.get_client()
    categories = client.get_categories()
    print_categories(categories)


@config_app.command("show")
def config_show() -> None:
    """Show the current configuration."""
    config_path = get_config_path()

    if not config_path.exists():
        error_console.print(f"[yellow]Config file not found: {config_path}[/yellow]")
        raise typer.Exit(1)

    try:
        config = load_config()
    except Exception as e:
        error_console.print(f"[red]Error loading config: {e}[/red]")
        raise typer.Exit(1) from None

    console.print(json.dumps({"base_url": config.base_url}, indent=2))
    console.print(f"\n[dim]Config file: {config_path}[/dim]")


@config_app.command("set")
def config_set(
    key: Annotated[str, typer.Argument(help="Config key to set.")],
    value: Annotated[str, typer.Argument(help="Value to set.")],
) -> None:
    """Set a configuration value."""
    config_path = get_config_path()

    try:
        config = load_config()
    except FileNotFoundError:
        config = Config()

    if key == "base_url":
        config.base_url = value.rstrip("/")
    else:
        error_console.print(f"[red]Unknown config key: {key}[/red]")
        error_console.print("[dim]Available keys: base_url[/dim]")
        raise typer.Exit(1)

    save_config(config)
    console.print(f"[green]Set {key} = {value}[/green]")
    console.print(f"[dim]Config file: {config_path}[/dim]")


def _hoist_global_options(argv: list[str]) -> list[str]:
    """Move global options to before the first subcommand."""
    value_options = {"--config", "-c"}
    flag_options = {"--verbose", "-v", "--version", "-V"}

    hoisted: list[str] = []
    rest: list[str] = []

    i = 0
    while i < len(argv):
        arg = argv[i]

        if any(arg.startswith(f"{opt}=") for opt in value_options):
            hoisted.append(arg)
            i += 1
        elif arg in value_options:
            hoisted.append(arg)
            if i + 1 < len(argv):
                i += 1
                hoisted.append(argv[i])
            i += 1
        elif arg in flag_options:
            hoisted.append(arg)
            i += 1
        else:
            rest.append(arg)
            i += 1

    return hoisted + rest


def cli() -> None:
    """Main entry point for the CLI."""
    try:
        sys.argv[1:] = _hoist_global_options(sys.argv[1:])
        app()
    except Exception as e:
        error_console.print(f"[red]Error: {e}[/red]")
        if _ctx.verbose:
            error_console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    cli()
