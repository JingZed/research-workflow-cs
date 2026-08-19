---
name: research-lit
description: "Search and synthesize literature across the Research corpus, connected reference libraries such as Zotero, connected or local note stores, local PDFs, and current scholarly web sources. Use for a library-first literature review, related-work search, or checking what the user already has before broader discovery."
---

# Research Literature Search

## Role

Provide one cross-source literature view while preserving where each item came
from. Missing integrations reduce coverage; they do not make the whole search
fail or justify pretending that a source was checked.

## Modes

- **all**: search every requested and available source.
- **library-only**: search the Research corpus, connected libraries, notes, and
  local papers without network discovery.
- **web-only**: search current public scholarly sources without reading private
  libraries or notes.
- **source-audit**: report source availability and coverage without a full
  synthesis.

## Consume

- Topic, question, paper title/URL, or explicit source selection.
- Optional `<topic-root>/synthesis/literature-corpus.jsonl` and paper
  workspaces.
- Optional connected Zotero or another reference manager, connected note store,
  authorized local note-vault path, and user-selected local PDF libraries.
- Optional freshness window, language, venue, paper-count, and download rules.

## Produce

- An in-session synthesis by default.
- Optional `<topic-root>/synthesis/library-search.md` when the user requests a
  durable cross-source report.

## Workflow

1. Resolve the topic and requested mode. If the user named sources, search only
   those sources and report unavailable ones explicitly.
2. Search in this order when allowed: topic corpus and existing paper
   workspaces; connected reference manager; connected/local research notes;
   authorized local PDFs or trustworthy Markdown; current scholarly web.
3. For connected libraries, retain collection, tags, annotations, highlights,
   citation metadata, and attachment status when relevant. User annotations are
   evidence of prior attention, not proof that a paper supports a claim.
4. For note stores, retain the note locator, user-authored interpretation, tags,
   and linked papers. Keep note interpretation separate from source-paper
   claims.
5. For local papers, inspect metadata and existing Markdown first. Escalate to
   structured PDF extraction only for relevant items whose text is otherwise
   unavailable; keep the scan bounded by the requested question.
6. For public search, use current scholarly sources and verify retained items
   against primary records. Distinguish peer-reviewed papers, preprints,
   workshop work, theses, and non-paper sources.
7. Deduplicate by DOI, arXiv ID, title/authors, and version relationship while
   preserving all source provenance. Do not silently merge distinct versions
   with materially different claims.
8. Analyze each retained paper by problem, method, evidence, limitation,
   relevance, and source. Then synthesize themes, disagreements, missing
   evidence, and the most useful next reads.
9. Report source coverage as `searched`, `unavailable`, `not requested`, or
   `blocked`. Include a citation-ready metadata or BibTeX section when available.
10. Write back to Zotero, a note store, or another external system only after an
    explicit request identifies the exact destination. Download or ingest a PDF
    only under the owning acquisition workflow.

## Quality Bar

- The user can distinguish papers already in their library from newly found
  work.
- Every paper has stable citation metadata and source provenance.
- Search coverage and unavailable integrations are visible.
- The synthesis separates source claims, user notes, and current interpretation.

## Boundaries

- Do not silently create or edit external library or note records.
- Do not treat search snippets, annotations, or notes as primary paper evidence.
- Do not duplicate the canonical literature corpus or paper workspace.
- Do not fail merely because an optional connector is absent.

## Open References Only As Needed

- Read `references/source-integration-pattern.md` for source-specific fields and
  graceful-degradation rules.
- Read `../../_shared/artifact-contract.md` for topic-root, corpus, and paper
  workspace ownership.
