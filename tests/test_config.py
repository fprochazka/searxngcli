"""Tests for configuration management."""

from pathlib import Path

import pytest

from searxngcli.config import Config, load_config, save_config


class TestConfig:
    def test_load_config(self, tmp_path: Path):
        config_file = tmp_path / "config.yml"
        config_file.write_text("base_url: https://searxng.example.com\n")

        config = load_config(config_file)
        assert config.base_url == "https://searxng.example.com"

    def test_load_config_strips_trailing_slash(self, tmp_path: Path):
        config_file = tmp_path / "config.yml"
        config_file.write_text("base_url: https://searxng.example.com/\n")

        config = load_config(config_file)
        assert config.base_url == "https://searxng.example.com"

    def test_load_config_missing_file(self, tmp_path: Path):
        config_file = tmp_path / "nonexistent.yml"
        with pytest.raises(FileNotFoundError):
            load_config(config_file)

    def test_load_config_missing_base_url(self, tmp_path: Path):
        config_file = tmp_path / "config.yml"
        config_file.write_text("something_else: value\n")
        with pytest.raises(ValueError):
            load_config(config_file)

    def test_save_and_load_config(self, tmp_path: Path):
        config_file = tmp_path / "config.yml"
        config = Config(base_url="https://searxng.example.com")
        save_config(config, config_file)

        loaded = load_config(config_file)
        assert loaded.base_url == "https://searxng.example.com"
