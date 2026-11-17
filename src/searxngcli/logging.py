"""Logging configuration for SearXNG CLI."""

import logging
from typing import Any

from rich.console import Console
from rich.logging import RichHandler

# Width of output that does not go to a terminal: tables size to their content instead of wrapping cells.
UNLIMITED_WIDTH = 10_000


def create_console(**kwargs: Any) -> Console:
    """Create a console that wraps text only when it writes to a terminal.

    Rich wraps at 80 columns when it cannot measure a terminal, which splits long URLs in piped output across lines.
    """
    console = Console(**kwargs)
    if not console.is_terminal:
        console.soft_wrap = True
        console.width = UNLIMITED_WIDTH
    return console


console = create_console()
# Not created by create_console: the log handler renders each record as a table expanded to the console width.
error_console = Console(stderr=True)


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the CLI."""
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=error_console,
                rich_tracebacks=True,
                show_time=verbose,
                show_path=verbose,
            )
        ],
    )

    if not verbose:
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name."""
    return logging.getLogger(name)
