# Compile Gates

Use this checklist when `paper-finish-loop` needs to decide whether the paper is merely drafted or actually package-ready.

## Core Gates

Run the gates in this order:

1. TeX environment gate: probe available TeX tooling and package support before compile.
2. LaTeX structural sanity gate: fail fast on structural `.tex` problems before `latexmk`.
3. Package currency check: detect stale packaged sections, missing figures,
   and bibliography drift.
4. Build gate: compile the paper end to end when the previous hard blockers are clear.
5. PDF packaging gate: check post-compile packaging artifacts without drifting into content review.
6. Limit gate: page, length, or venue packaging limits are not already violated without visibility.

Rationale:
- environment failures and structural LaTeX failures are hard blockers
- stale or incomplete package files remain visible as package blockers
- packaging checks happen after compile and should remain packaging-layer only

## Stale File Detection

When `paper/` mirrors content from `drafts/`, check whether:

- a packaged section is older than its draft source
- a referenced figure filename no longer exists
- a bibliography or asset file is missing from the package

If the package is stale, treat that as a blocker, not as a cosmetic warning.

Expected machine-readable output:
- `stale_sections`
- `missing_figures`
- `missing_bibliography`
- `status`

## PDF Packaging Checks

When a PDF exists, quickly check for:

- missing compiled PDF
- unresolved placeholders or TODO markers

In v1, keep this checker narrow and deterministic. It is a packaging-layer checker, not a general content-review step.
Do not pretend the paper is submission-ready just because `latexmk` returned success once.

## Bounded Improvement Loop

Fix the highest-leverage blocker, re-run the relevant gate, and stop to record state.

Avoid turning one finish pass into an uncontrolled rewrite loop or a batch “fix everything later” pass.
