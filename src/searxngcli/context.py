"""CLI context management for SearXNG CLI."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import SearXNGClient
    from .config import Config


@dataclass
class Context:
    """CLI context passed to all commands."""

    config: "Config | None" = None
    verbose: bool = False

    def get_config(self) -> "Config":
        """Get config, loading if needed."""
        from .config import load_config

        if self.config is None:
            self.config = load_config()
        return self.config

    def get_client(self) -> "SearXNGClient":
        """Create a SearXNGClient from config."""
        from .client import SearXNGClient

        config = self.get_config()
        return SearXNGClient(base_url=config.base_url)


_ctx = Context()


def get_context() -> Context:
    """Get the current CLI context."""
    return _ctx
