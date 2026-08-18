---
name: paper-inbox-triage
description: "Triage new papers, PDFs, and links into a deduplicated reading queue with a clear next-read decision. Use when Codex needs to process an inbox of unread papers, rank relevance, remove duplicates, or decide what to read first for a topic, project, or deadline."
---

# Paper Inbox Triage

## Overview
Turn a mixed inbox of new papers or links into a ranked queue that reflects topic fit, urgency, and expected value.

## Consume
- One or more new `<topic-root>/papers/<paper-id>/source.pdf` files, URLs, or
  raw paper titles.
- Optional `<topic-root>/synthesis/paper-leads.jsonl` or
  `<topic-root>/synthesis/search-report.md` from `$paper-discovery-fetcher`.
- Optional existing `<topic-root>/synthesis/reading-queue.md`,
  `<topic-root>/synthesis/idea-backlog.md`, or deadline context.
- Optional `<topic-root>/synthesis/literature-corpus.jsonl` when it exists — check it first before any other source to avoid re-queueing papers the project already has.
- Optional local paper workspaces, `refs.bib`, or existing summaries as secondary deduplication checks when the corpus file is absent.
- Optional topic keywords, target venue, or thesis chapter scope.

## Produce
- `<topic-root>/synthesis/reading-queue.md`

## Workflow
1. Resolve `<topic-root>` using the shared artifact contract before reading or
   writing intake artifacts. Stop for an explicit root if resolution fails.
2. Collect candidate papers, normalize the visible title or ID for each item, and collapse obvious duplicates before ranking.
3. Check `<topic-root>/synthesis/literature-corpus.jsonl` first when it exists — match on `paper_id` and `arxiv_id`. Only when the corpus is absent should you check local paper workspaces, bibliography entries, or prior summaries.
4. Score each item on topic fit, novelty signal, urgency, and expected leverage for the active topic or selected idea.
5. For each shortlisted item, inspect whether a usable local PDF already exists, whether acquisition is unresolved, or whether the paper is blocked by access.
6. Explain the ranking in short, concrete reasons so the queue stays auditable instead of becoming a black box.
7. If a paper is worth reading but its PDF is missing, keep it in the queue with an explicit `blocked-access` note instead of dropping it.
8. End with exactly one recommended next paper to read so the user can continue without context switching.

## Quality Bar
- Keep the ranking criteria explicit and stable across items.
- Flag low-confidence metadata or likely duplicates instead of silently merging them.
- Prefer a short actionable queue over exhaustive commentary.
- Surface `worth reading but PDF unavailable` items clearly so the user can intervene manually.

## Boundaries
- Do not write `meta.yaml` or `summary.md` for each paper; hand selected papers to downstream single-paper skills.
- Do not claim research gaps or novelty from titles alone.
- Do not expand into a survey; stay at inbox triage level.
- Do not attempt ad hoc download workarounds inside triage; route blocked papers to `$paper-pdf-fetcher`.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
- Review `../paper-discovery-fetcher/references/source-priority.md` when you need a stable rule for preferring local paper memory before treating an item as new inbox work.
