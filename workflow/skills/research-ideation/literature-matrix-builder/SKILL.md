---
name: literature-matrix-builder
description: "Build one requested multi-paper synthesis view from the shared topic corpus. Supports matrix mode for comparable rows, map mode for clusters and bridge papers, and gaps mode for a small source-bounded gap shortlist; modes are independent and never auto-chain."
---

# Literature Matrix Builder

## Role

Turn the existing corpus and paper notes into one decision-useful synthesis
artifact. Run only the requested mode.

## Modes

- **matrix** (default): topic-level shared matrix or idea-specific derived view.
- **map**: textual clusters, bridges, and sparse regions.
- **gaps**: small evidence-backed gap shortlist.

## Consume

- `<topic-root>/synthesis/literature-corpus.jsonl` as the paper inventory when
  it exists.
- Relevant paper-local `summary.md`, `meta.yaml`, `notes.md`, and optional
  `claim-evidence-map.md`.
- Existing `<topic-root>/synthesis/literature-matrix.md` or
  `<topic-root>/synthesis/topic-map.md` only when the selected mode needs it.
- Optional exact idea ID, topic scope, comparison columns, or constraints.

## Produce

- Matrix mode:
  - `<topic-root>/synthesis/literature-matrix.md`, or
  - `<topic-root>/ideas/<id>/literature-matrix.md` for one explicit idea.
- Map mode: `<topic-root>/synthesis/topic-map.md`.
- Gaps mode: `<topic-root>/synthesis/research-gaps.md`.

Produce one mode's artifact unless the user explicitly asks for several.

## Workflow

1. Resolve `<topic-root>`, select the mode, and load the corpus before scanning
   paper workspaces. Do not reparse every paper from scratch.
2. In **matrix mode**:
   - choose topic-level or exact-idea scope;
   - keep one physical paper per row and show overlap with `Relevant To`;
   - use comparable columns and assign `direct_prior`,
     `transferable_inspiration`, or `unresolved` with a source-backed reason;
   - mark missing or incomparable cells explicitly.
3. In **map mode**:
   - choose one clustering axis that answers the current question;
   - name stable branches, bridge papers, and genuinely sparse regions;
   - keep the result textual and decision-oriented rather than drawing a
     generic mind map.
4. In **gaps mode**:
   - inspect missing combinations, contradictory results, weak controls,
     neglected constraints, and evaluation gaps;
   - ground each candidate in concrete `direct_prior` rows;
   - if support is only inspiration or unresolved, label the same-field gap
     `UNVERIFIED` and name the missing coverage rather than launching search;
   - rank only a small set by relevance and feasible leverage.
5. Return the selected view and stop. Do not automatically create another view,
   search, promote an idea, frame a hypothesis, or write related-work prose.

## Quality Bar

- Each nontrivial comparison is traceable to a paper artifact.
- Contextual evidence roles are not written back as global corpus facts.
- Sparse collection is not misreported as a globally novel gap.
- The artifact stays smaller than the source pile and directly supports the
  requested decision.

## Boundaries

- Do not duplicate papers across folders or rows.
- Do not promote `transferable_inspiration` or `unresolved` to direct evidence.
- Do not make global novelty or SOTA claims from local coverage.

## Open References Only As Needed

- Review `../../_shared/artifact-contract.md` for topic and idea path rules.
- Review `../../_shared/templates/literature-matrix-template.md` only in matrix
  mode when the exact structure is useful.
- Review `../../_shared/templates/topic-map-template.md` only in map mode.
