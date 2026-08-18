---
name: paper-metadata-normalizer
description: "Extract and normalize paper metadata into a stable `meta.yaml` file. Use when Codex needs to capture or repair title, authors, year, venue, DOI, arXiv ID, or a citation key for a single paper before downstream reading, citation, or writing tasks."
---

# Paper Metadata Normalizer

## Overview
Create one canonical metadata record for a paper so every later skill reads the same identifiers and citation facts.

## Consume
- `<topic-root>/papers/<paper-id>/source.pdf`, the first page, or any existing
  metadata snippet.
- Optional existing `<topic-root>/papers/<paper-id>/meta.yaml` or `refs.bib`
  entry for cross-checking.
- Optional filename or folder naming conventions from the local project.

## Produce
- `<topic-root>/papers/<paper-id>/meta.yaml`

## Workflow
1. Resolve the selected `<topic-root>/papers/<paper-id>/` workspace before
   writing. Do not create metadata at the idea root.
2. Extract title, authors, year, venue, DOI, and arXiv ID from the strongest available source, preferring the paper itself over filenames.
3. Normalize author order, venue naming, and identifier formatting without losing the raw identifiers.
4. Record uncertainty explicitly when a field cannot be confirmed from the available inputs.
5. Write a stable `meta.yaml` in the selected paper workspace.

## Quality Bar
- Keep confirmed values separate from guessed or low-confidence values.
- Preserve all stable identifiers exactly, including DOI and arXiv formatting.
- Produce a clean machine-readable file rather than prose notes.

## Boundaries
- Do not write or merge `refs.bib`; leave bibliography maintenance to `$citation-library-maintainer`.
- Do not summarize the paper body or method.
- Do not invent venue or year from memory when the source is ambiguous.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
