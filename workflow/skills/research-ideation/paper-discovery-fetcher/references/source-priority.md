# Source Priority

Use this ordering when discovery or triage should prefer what the project already knows before widening the search.

## Priority Order

1. `<topic-root>/synthesis/literature-corpus.jsonl`
2. `<topic-root>/papers/<paper-id>/` workspaces
3. `<topic-root>/synthesis/reading-queue.md`
4. Existing paper-local `summary.md`, `notes.md`, and other reading artifacts
5. `refs.bib` or other local bibliography records
6. An already-available structured scholarly API or search index
7. Broader web search

## Why This Order

This keeps the workflow from:

- rediscovering papers already processed
- queueing papers that already have summaries
- splitting the same paper across multiple local folders
- treating a bibliography entry as if it were a brand new lead

## Dedup Rule

Before adding a paper as new, check the strongest stable identifier available:

- DOI
- arXiv ID
- title plus first author
- semantic-scholar style paper URL when needed

If a local match already exists, update the status or queue position instead of creating a fresh duplicate lead.
