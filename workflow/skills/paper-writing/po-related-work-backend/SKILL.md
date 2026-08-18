---
name: po-related-work-backend
description: "Use when Codex needs to run PaperOrchestra only as an optional related-work backend, starting from native project state and literature corpus, to produce a PO-side draft scaffold without transferring canonical manuscript ownership."
---

# PO Related-Work Backend

## Overview
Run PaperOrchestra only for related-work candidate generation and draft scaffolding.

This skill is an optional backend, not a canonical writing path. It prepares or resumes a `po-workspace/`, runs the PO literature-review flow, and returns comparison artifacts to the native workflow.

## Consume
- `notes/project-state.md` as the project-local source of thesis framing and claim boundaries.
- `<topic-root>/synthesis/literature-corpus.jsonl` as the read-only topic corpus used for seed selection.
- Optional `drafts/outline.md` when the native manuscript already has a useful cluster structure.
- Optional existing `po-workspace/` when resuming a prior related-work-only trial.
- Optional `claim-evidence-map.md` or `experiments/results/summary.md` when the introduction framing needs a tighter bounded-claim anchor.

## Produce
- `po-workspace/seeded_candidates.json`
- `po-workspace/raw_candidates.json`
- `po-workspace/deduped_candidates.json`
- `po-workspace/cache/s2_cache.json`
- `po-workspace/raw_pool.json`
- `po-workspace/s2_verification_report.json`
- `po-workspace/citation_pool.json` (intermediate only; see Handoff)
- `po-workspace/refs.bib` (intermediate only; see Handoff)
- `po-workspace/drafts/intro_relwork.tex`
- Optional `po-workspace/comparison-notes.md`
- Optional `po-workspace/trial-summary.md`

## Workflow
1. Confirm the user directly asked for an explicit PO related-work comparison
   or scaffold run. Native related-work weakness alone is not a valid trigger;
   route back to `$related-work-weaver` in that case. Then start from
   `notes/project-state.md` and the topic-level corpus to scope the PO run.
2. Build or refresh `po-workspace/` without touching native canonical drafts.
3. Filter the topic corpus into a project-specific seed set and write `po-workspace/seeded_candidates.json`.
4. Use `workflow/scripts/seed_candidates_for_po.py` to merge the seed set into `po-workspace/raw_candidates.json`.
5. Run the narrow PO literature-review path only: pre-dedup, Semantic Scholar verification, pool assembly, BibTeX generation, and related-work draft generation.
6. Treat the resulting `po-workspace/drafts/intro_relwork.tex` as a comparison draft or scaffold, not as a canonical manuscript artifact.
7. Hand the PO draft back to the native flow for editorial judgment,
   comparison, or selective transplant.

## Quality Bar
- Keep the PO run scoped to related-work-only.
- Keep seed quality high enough that the PO draft is a meaningful comparison baseline rather than a noisy web-search dump.
- Preserve bounded-claim framing from the native project state so PO output does not drift into stronger claims than the evidence supports.
- Keep the distinction between intermediate PO artifacts and native handoff artifacts explicit.

## Boundaries
- Do not overwrite `drafts/related-work.md`.
- Do not write to `<topic-root>/synthesis/literature-corpus.jsonl`.
- Do not run PO section-writing, refinement, or full-pipeline orchestration here.
- Do not treat `po-workspace/citation_pool.json` or `po-workspace/refs.bib` as canonical bibliography artifacts.
- Do not promote PO output into the manuscript without native editorial review.
- Do not run this skill as a fallback when `$related-work-weaver` produces weak output; weakness of the native draft is an upstream fix, not a PO trigger.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership or canonical paths are unclear.
- Review `../../_shared/engineering-patterns.md` when capability flags,
  machine-readable state, or optional backend boundaries affect the route.
- Review `../../_shared/language-policy.md` when project notes mix Chinese working notes with English manuscript text.
- Review the workspace's PaperOrchestra integration policy when the current
  allowed scope is unclear. If no local policy or installation exists, treat
  the optional backend as unavailable.
