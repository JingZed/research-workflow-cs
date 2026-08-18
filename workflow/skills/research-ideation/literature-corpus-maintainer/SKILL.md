---
name: literature-corpus-maintainer
description: "Maintain the topic-level literature-corpus.jsonl as the single source of truth for all papers in a topic. Use when adding new papers after discovery or triage, merging duplicates, updating read_status or summary_path, or rebuilding the corpus from scratch."
---

# Literature Corpus Maintainer

## Overview
Own and maintain `<topic-root>/synthesis/literature-corpus.jsonl` as the authoritative record of every paper in a topic. All downstream skills treat this file as the primary deduplication and status source.

## Consume
- Existing `<topic-root>/synthesis/literature-corpus.jsonl` when it already exists.
- New paper entries from `<topic-root>/synthesis/paper-leads.jsonl`,
  `<topic-root>/synthesis/reading-queue.md`, or triage output.
- Optional `<topic-root>/papers/<paper-id>/meta.yaml`, `summary.md`, or path
  updates when a paper transitions from unread to read.
- Optional user-specified `relevant_to` tags that associate a paper with one or
  more shared subtopics or promoted idea IDs.

## Produce
- `<topic-root>/synthesis/literature-corpus.jsonl`

## Record Schema

Each record in the JSONL file must include these fields:

```json
{
  "paper_id": "<canonical-id>",
  "arxiv_id": "<arXiv-id-if-exists-else-null>",
  "title": "<full paper title>",
  "authors": ["<last, first>"],
  "venue": "<venue or null>",
  "year": <year or null>,
  "relevant_to": ["<idea-id-or-tag>"],
  "summary_path": "<absolute-path-to-summary.md-or-null>",
  "read_status": "<unread|downloaded|summarized>",
  "read_basis": "<title/abstract only|partial read|full read|unknown|null>",
  "pdf_path": "<absolute-path-to-source.pdf-or-null>",
  "notes": "<short note or null>"
}
```

- `paper_id` is the stable canonical identifier. Prefer the arXiv ID when one exists; use DOI slug (e.g. `10.1609_aaai.v40i37.40403`) only when no arXiv ID is available.
- `arxiv_id` is a secondary lookup field. Populate it even when `paper_id` is already the arXiv ID, so downstream skills can always match on both fields.
- `relevant_to` may include promoted idea IDs (e.g. `i003`) and shared topic
  tags (e.g. `vla`, `world-model`, `evaluation`, `layer2`, or `background`).
  Reserve the `iNNN` shape for idea IDs. Use stable lowercase slugs for new
  shared tags, and preserve legacy tags verbatim rather than migrating them.
- `read_basis` is optional and backward-compatible. Use it when a summary or note states the reading basis; missing legacy values should be treated as `unknown`, not as a corpus repair blocker.

## Workflow
1. Resolve `<topic-root>` using the shared artifact contract. Stop for an
   explicit root if resolution fails.
2. Load the existing corpus when it exists. Parse line by line (JSONL, not JSON array).
3. For each incoming paper to add, match against existing records by `paper_id` and `arxiv_id`. If a match exists, update fields (merge `relevant_to`, update `read_status`, add `summary_path`, and preserve or update `read_basis` when provided) rather than duplicating. Treat shared topic tags and `iNNN` idea links as separate meanings inside the same list.
4. For entirely new papers, append a new record with all required fields populated. Use `null` for unknown optional fields rather than omitting them.
5. Deduplicate: if two records represent the same physical paper (same DOI, same arXiv ID, same title), merge them into one record — union their `relevant_to`, keep the more specific `paper_id`, and populate `arxiv_id` if known.
6. Write the updated corpus back to `<topic-root>/synthesis/literature-corpus.jsonl`, one JSON object per line, no trailing comma.
7. Report: number of records added, updated, merged, and total record count.

## Quality Bar
- Never create duplicate records for the same physical paper.
- Never drop a `relevant_to` tag when merging records.
- Keep new shared tags stable and reusable across the corpus; do not derive
  classification from paper folder placement.
- Always validate that the written file parses correctly as JSONL (one object per line).
- Prefer `paper_id` = arXiv ID when available; DOI slug is a fallback only.
- Preserve `read_basis` when it exists and avoid upgrading it unless a newer summary or note justifies the stronger basis.

## Boundaries
- Do not perform paper reading, summarization, or ranking inside this skill.
- Do not write to per-idea `literature-matrix.md` files; that is `literature-matrix-builder`'s domain.
- Do not require a one-time migration of old records just to add `read_basis`; missing legacy values remain valid and mean `unknown`.
- Do not add a parallel `topic_tags` field or rewrite legacy `relevant_to` tags
  merely to separate theme and idea semantics.
- Do not delete records without explicit user instruction.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
