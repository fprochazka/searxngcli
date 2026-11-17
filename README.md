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

# Also show the engines, category and score of each result (and debug logs)
searxng search "python asyncio" -v

# JSON output (for scripting)
searxng search "test" --json

# List available engines
searxng engines

# List available categories
searxng categories

# Show current configuration
searxng config show
```

## Claude Code Plugin

This repository bundles a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) plugin with a skill that teaches Claude to search the web with the `searxng` CLI. Install and configure the CLI first, then add the marketplace and install the plugin:

```bash
claude plugin marketplace add fprochazka/searxngcli
claude plugin install searxngcli@fprochazka-searxngcli
```

To upgrade after a new version:

```bash
claude plugin marketplace update fprochazka-searxngcli
claude plugin update searxngcli@fprochazka-searxngcli
```

Claude loads the skill on its own when a task needs a web search. The skill auto-approves every `searxng` command.

## Development

```bash
git clone https://github.com/fprochazka/searxngcli.git
cd searxngcli
uv sync --dev

# Run from source
uv run searxng search "test"

# Lint, format check and type check
uv run ruff check .
uv run ruff format --check .
uv run mypy

# Test
uv run pytest
```

The project needs Python 3.12 or newer. CI runs the same checks, and the tests on Python 3.12 to 3.15. `uv run ruff format .` fixes the formatting.

### Plugin version

When you change the plugin, bump its version in both manifests, so that they stay in lockstep: `.claude-plugin/marketplace.json` and `coding-agent-plugins/claude-code/.claude-plugin/plugin.json`. Claude Code offers the update to installed plugins only when the version changes, and users get it once the commit lands on `master`.

### Commit hooks

Search queries, instance URLs and captured output used in tests can carry private names, hostnames and paths into a commit. `scripts/hooks` holds a pre-commit and a commit-msg hook that refuse a commit when a staged line or the commit message matches a private identifier. The identifiers live in a file outside the repository, because listing them here would publish the very strings the hooks exist to keep out. Set it up once per clone:

```bash
git config core.hooksPath scripts/hooks
git config hooks.forbiddenPatternsFile ~/.config/git/forbidden-patterns.txt  # any path outside the repo
```

The file holds one extended regex per line, matched case-insensitively; blank lines and `#` comments are ignored. Until `hooks.forbiddenPatternsFile` points at a file with at least one pattern, both hooks refuse every commit and print how to fix it. The hooks check only the lines a commit adds.

## License

MIT
