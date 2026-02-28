"""Configuration management for SearXNG CLI."""

from dataclasses import dataclass
from pathlib import Path

import yaml

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "searxngcli" / "config.yml"


@dataclass
class Config:
    """Main configuration class."""

    base_url: str = ""


def load_config(config_path: Path | None = None) -> Config:
    """Load configuration from YAML file."""
    path = config_path or DEFAULT_CONFIG_PATH

    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found: {path}\n"
            f"Create it with your SearXNG instance URL. Example:\n\n"
            f"base_url: https://searxng.example.com"
        )

    with open(path) as f:
        data = yaml.safe_load(f) or {}

    base_url = data.get("base_url", "")
    if not base_url:
        raise ValueError(f"Missing 'base_url' in config file: {path}")

    return Config(base_url=base_url.rstrip("/"))


def save_config(config: Config, config_path: Path | None = None) -> None:
    """Save configuration to YAML file."""
    path = config_path or DEFAULT_CONFIG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {"base_url": config.base_url}
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)


def get_config_path() -> Path:
    """Get the default config file path."""
    return DEFAULT_CONFIG_PATH
