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

### Commit hooks

Search queries, instance URLs and captured output used in tests can carry private names, hostnames and paths into a commit. `scripts/hooks` holds a pre-commit and a commit-msg hook that refuse a commit when a staged line or the commit message matches a private identifier. The identifiers live in a file outside the repository, because listing them here would publish the very strings the hooks exist to keep out. Set it up once per clone:

```bash
git config core.hooksPath scripts/hooks
git config hooks.forbiddenPatternsFile ~/.config/git/forbidden-patterns.txt  # any path outside the repo
```

The file holds one extended regex per line, matched case-insensitively; blank lines and `#` comments are ignored. Until `hooks.forbiddenPatternsFile` points at a file with at least one pattern, both hooks refuse every commit and print how to fix it. The hooks check only the lines a commit adds.

## License

MIT
