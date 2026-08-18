---
name: baseline-checklist-builder
description: "List the baselines, controls, and sanity checks required for a credible experiment. Use when Codex needs to turn a hypothesis or reproduction target into a concrete checklist of comparisons that must be included before running or writing experiments."
---

# Baseline Checklist Builder

## Overview
Make the comparison set explicit so experiments do not drift into easy but unconvincing evaluations.

## Consume
- `hypothesis.md` or `experiments/plans/reproduction-plan.md`.
- `literature-matrix.md` and relevant `summary.md` files.
- Optional compute budget or time constraints.

## Produce
- `experiments/plans/baseline-checklist.md`

## Workflow
1. List must-have baselines, sanity checks, controls, and negative controls for the current question.
2. Assign each entry a stable `baseline_id`; set `role` to
   `runnable_control` or `reported_reference`; and record `source_locator`,
   `implementation_locator`, `implementation_version`, `task`, `dataset`,
   `dataset_version`, `split`, `preprocessing`, `metric`, `direction`,
   `reported_score`, `uncertainty`, `backbone_or_model`, `training_setting`,
   `evaluation_setting`, `tuning_setting`, `access`, and `license`. Preserve
   explicit `unknown` values rather than omitting fields. Describe sanity and
   negative-control purpose in the entry's justification rather than adding a
   third role state.
3. Record `availability` as `runnable_verified`, `runnable_unverified`,
   `citation_only`, or `inaccessible`; record `parity_status` as `comparable`,
   `partially_comparable`, `incompatible`, or `unknown`; and state both the
   `parity_blocker` and `allowed_use` as `primary_comparison`,
   `contextual_only`, or `excluded` for the entry.
4. Separate cheap early checks from expensive full baselines so execution can be staged.
5. Justify each baseline in terms of what criticism it prevents or what comparison it enables.
6. Flag missing code, data, or evaluation parity requirements that could invalidate the comparison.

## Quality Bar
- Include only baselines that materially affect the study's credibility.
- Keep the checklist aligned with the hypothesis and target setting.
- Make missing parity conditions explicit.
- Forbid `primary_comparison` as an `allowed_use` when `parity_status` is
  `incompatible` or `unknown`.
- Never describe a `citation_only` entry as runnable or reproduced.

## Boundaries
- Do not define the full command matrix here.
- Do not aggregate results or plot figures.
- Do not substitute a baseline list for a full experiment spec.
- Do not duplicate this ledger downstream; experiment plans and runbooks must
  reference the stable `baseline_id` values.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
