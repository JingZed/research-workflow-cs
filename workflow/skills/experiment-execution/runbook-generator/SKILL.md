---
name: runbook-generator
description: Translate an experiment plan into either a compact exploratory runbook or a full long-run/confirmatory runbook. Use when Codex needs copy-runnable commands, environment and output routing, a smoke check, and READY or BLOCKED status; require heartbeat, checkpoint, and stall machinery only for genuinely long, costly, distributed, or opaque work.
---

# Runbook Generator

## Overview
Bridge experiment design to execution without making a short diagnostic carry
the ceremony of a long confirmatory campaign.

## Consume
- `experiments/plans/experiment-plan.md`, `hypothesis.md`,
  and `experiments/plans/baseline-checklist.md`.
- Optional `experiments/failures/failure-analysis.md` when the experiment plan
  includes an anomaly-dependent adjustment.
- Optional environment constraints, compute queue rules, or codebase naming conventions.
- Optional reproduction-specific requirements from `experiments/plans/reproduction-plan.md`.

## Produce
- `experiments/runbooks/runbook.md`

## Workflow
1. Read `../../_shared/execution-authority.md` and inherit the plan's
   `exploratory` or `confirmatory` lane.
2. For a compact exploratory runbook, record the six-field run card plus the
   entrypoint, working directory, environment, copy-runnable command, focused
   smoke check, expected output, success/failure signal, and stop condition.
3. For a confirmatory, multi-stage, distributed, costly, or opaque runbook,
   additionally resolve prediction/baseline IDs, dependency order, naming,
   checkpoints, logs, evidence exports, uncertainty requirements, progress
   signal, heartbeat expectation, and stall condition.
4. Treat same-contract operational repairs as L1 and express retries as
   `attempt-N`. Do not require a scientific adjustment decision or user
   approval for Git, package, environment, download, scheduler, logging, or
   resume fixes. Require L3 only for a result-aware confirmatory-contract
   change or another shared-policy trigger.
5. Separate must-run experiments from optional or stretch experiments when the
   distinction matters. A one-run diagnostic does not need an artificial
   milestone tree.
6. Mark the runbook `READY` when every field needed for its selected lane is
   executable as written. Block only on a real command, environment, data,
   resource, permission, or scientific-contract gap; name the exact gap.
7. Make failure signals and stop rules visible. Only for genuinely long,
   costly, distributed, or opaque work, keep a compact operational milestone
   table in this same runbook with: step, prerequisite, success signal,
   fallback, and exit condition. Do not create a separate milestone artifact.

## Quality Bar
- Preserve clear dependency order between runs.
- Keep logging and naming conventions stable enough for later aggregation.
- Make long-running steps observable before execution starts. Keep a short
  exploratory runbook readable in one screen.
- Make every required command copy-runnable; do not block on metadata that is
  irrelevant to the selected lane.
- Treat `READY` only as execution readiness; it does not establish
  preregistration or confirmatory eligibility.
- Record exact input and output paths. Research runbooks do not compute
  file-content identifiers; use direct comparison for sensitive transfers.

## Boundaries
- Do not execute commands or mutate the codebase here.
- Do not aggregate results; that belongs to `$result-aggregator`.
- Do not hide optional runs among required runs.
- Do not write runbooks that launch long-running experiments silently and only inspect final artifacts hours later.
- Do not invent prediction or baseline IDs, override baseline parity, approve
  an anomaly-dependent adjustment, or grant preregistration from this Skill.
- Do not turn an evidence check, technical retry, or manager self-check into a
  user approval point.

## Open References Only As Needed
- Read `../../_shared/execution-authority.md` before selecting runbook depth or
  requiring a user decision.
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
- Review `../../_shared/templates/runbook-template.md` when you need the specific structure, template, or integration note for this skill.
- Review `references/notebook-family-runbooks.md` when the project keeps runnable notebooks under experiment-family `code/` folders and paper-facing exports under `outputs/`.
