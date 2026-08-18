---
name: figure-table-extractor
description: "Extract figures, tables, and captions from a paper into a reusable index. Use when Codex needs to capture visual evidence from `source.pdf` or `paper.md`, build a `figures/` folder, or connect claims to the paper's visual artifacts."
---

# Figure Table Extractor

## Overview
Extract the paper's visual evidence into a stable `figures/` folder with an index that downstream skills can cite.

## Consume
- `<topic-root>/papers/<paper-id>/source.pdf` and, when helpful, paper-local
  `paper.md` for cross-checking numbering.
- Optional local extraction tools or existing image exports.
- Optional paper-local `summary.md` or `claim-evidence-map.md` if figure
  priority already exists.

## Produce
- `<topic-root>/papers/<paper-id>/figures/`
- `<topic-root>/papers/<paper-id>/figures/index.md`

## Workflow
1. Resolve the selected `<topic-root>/papers/<paper-id>/` workspace before
   writing.
2. Locate figures, tables, captions, and the surrounding section context in the source paper.
3. Export assets when tooling allows it; otherwise capture numbering, caption text, and the relevant page or section anchor.
4. Build `figures/index.md` with one entry per item, including what the figure or table is meant to show.
5. Highlight missing, low-resolution, or ambiguous assets instead of pretending the extraction is complete.

## Quality Bar
- Keep numbering consistent with the source paper.
- Retain enough caption information to reconnect the artifact to the main text.
- Mark whether an item is a figure, table, or equation block.

## Boundaries
- Do not redesign the plots or redraw figures.
- Do not write `summary.md` or manuscript captions.
- Do not infer unsupported takeaways from a figure alone.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
