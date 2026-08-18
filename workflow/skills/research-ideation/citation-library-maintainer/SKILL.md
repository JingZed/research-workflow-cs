---
name: citation-library-maintainer
description: "Maintain a stable local bibliography file with deduplicated, normalized BibTeX entries. Use when Codex needs to merge paper metadata into `refs.bib`, fix citation keys, remove duplicates, or repair inconsistent venue and identifier fields across multiple papers."
---

# Citation Library Maintainer

## Overview
Keep `refs.bib` clean, deduplicated, and predictable so writing skills can cite papers without repairing bibliography noise first.

## Consume
- One or more `<topic-root>/papers/<paper-id>/meta.yaml` files or raw BibTeX
  entries.
- Existing `refs.bib`.
- Optional project-specific citation key conventions.

## Produce
- `refs.bib`

## Workflow
1. Merge incoming entries into the existing bibliography while preserving the strongest confirmed identifiers.
2. Collapse duplicates by DOI, arXiv ID, or highly similar title-author combinations.
3. Normalize citation keys using one stable naming rule and keep that rule consistent across the project.
4. Prefer data preservation when entries conflict; keep the best canonical entry instead of silently dropping useful fields.
5. For each newly merged entry, preserve locator metadata when the source
   `meta.yaml` contains `locator`; otherwise mark locator side metadata as
   `locator_status: unverified` when the project has a notes or bibliography
   side-metadata convention. Do not add unsupported locator fields to
   `refs.bib` just to satisfy this step.

## Quality Bar
- Maintain one canonical entry per paper.
- Keep citation keys deterministic so manuscript citations stay stable across updates.
- Retain identifiers even if venue fields are uncertain.
- Apply citation locator discipline for new citations: record a locator in
  notes or supported bibliography side metadata when available (page,
  paragraph, section, or quoted/excerpted passage). Missing locator evidence
  should be marked `[UNVERIFIED-LOCATOR]` for downstream audit rather than
  filled in from inference.

## Boundaries
- Do not write related work prose or compare papers conceptually.
- Do not invent missing BibTeX fields that are not supported by the source metadata.
- Do not invent page numbers, paragraphs, quoted passages, or locator side
  metadata that are not supported by the source metadata or reading notes.
- Do not edit manuscript text while cleaning the bibliography.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
