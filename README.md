# searxngcli

A command-line interface for [SearXNG](https://docs.searxng.org/) — a free, privacy-respecting metasearch engine.

## Features

- Search with filters (categories, engines, language, time range, safe search)
- JSON output for scripting and piping
- List available engines and categories from your instance
- Rich formatted terminal output
- Simple YAML configuration

## Installation

```bash
git clone https://github.com/fprochazka/searxngcli.git
cd searxngcli
uv tool install -e .
```

## Configuration

Create `~/.config/searxngcli/config.yml` with the URL of your SearXNG instance:

```yaml
base_url: https://searxng.example.com
```

Or use the CLI:

```bash
searxng config set base_url https://searxng.example.com
```

## Usage

```bash
# Basic search
searxng search "python asyncio"

# Filter by category
searxng search "breaking news" -c news

# Filter by engines
searxng search "rust" -e google,duckduckgo

# Limit results and paginate
searxng search "test" -n 5 -p 2

# Filter by time range
searxng search "latest updates" -t week

# JSON output (for scripting)
searxng search "test" --json

# List available engines
searxng engines

# List available categories
searxng categories

# Show current configuration
searxng config show
```

## Claude Code

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill is available for this project, allowing Claude to use the `searxng` CLI autonomously. See [searxngcli skill](https://github.com/fprochazka/claude-code-plugins/tree/master/plugins/searxngcli) for installation and usage instructions.

## Development

```bash
git clone https://github.com/fprochazka/searxngcli.git
cd searxngcli
uv sync

# Run from source
uv run searxng search "test"

# Lint
uv run ruff check src/

# Test
uv run pytest
```

## License

MIT
