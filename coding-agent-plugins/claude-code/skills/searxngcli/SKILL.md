---
name: searxngcli:searxngcli
description: This skill should be used when the user asks to "search the web", "look up online", "find recent information", "search for", "what's the latest on", or needs web search results. Provides access to a private SearXNG metasearch engine instance via the `searxng` CLI. Prefer this over WebSearch when available. Web searches are best run in a research subagent.
user-invocable: false
trigger-keywords: searxng, websearch, web search, search online, look up online, find online, google
allowed-tools: Bash(searxng:*)
---

# searxngcli

The `searxng` CLI searches the web through a private SearXNG instance, which merges the results of several search engines.

## Search

```bash
searxng search "python asyncio taskgroup"
```

The text output lists each result as a title, its URL on one line, a snippet, and its published date when the engines know it. Run one search per phrasing of the question; when the results miss, rephrase and search again. Pick results by their title and snippet before fetching any page.

## Narrow the search when it helps

- `--time-range day|week|month|year` for news, releases and other recent topics.
- Search operators inside the query, which the engines receive as they are: `"site:docs.python.org taskgroup"`, `"filetype:pdf postgresql locking"`.
- `--num 5` for a quick lookup. A larger `--num` does not fetch more results, because the CLI shows only the one page the instance returns.

## Pick fields with JSON

Pipe `--json` through `jq` to keep only the fields the task needs, for example the titles and URLs to scan many results, or `published_date` to judge how fresh each result is. Each result has `title`, `url`, `content`, `published_date` and `engines`; the top level also has `suggestions` and `corrections`.

```bash
searxng search "python asyncio taskgroup" --num 10 --json | jq -r '.results[] | "\(.title) \(.url)"'
```

## Mistakes to avoid

- Quote the whole query, so the shell passes it as one argument.
- Put the flags after `search`: `searxng search "query" --time-range week`, not `searxng --time-range week search "query"`.
- Leave `--categories`, `--engines` and `--language` out unless the user asks for them. The instance has good defaults.
- Pass `--num` with `--json` and filter the output with `jq`. Never read the raw JSON: it is more than twice as large as the text output for the same results.
- If the CLI reports that it is not configured, ask the user for the URL of their SearXNG instance.

Everything else: `searxng search --help`.
