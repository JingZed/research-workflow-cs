---
name: failure-analysis-writer
description: Write a structured analysis for a material scientific anomaly, weak or negative result, result-changing data/code issue, or recurring unexplained failure. Do not use for routine network, package, download, scheduler, environment, logging, or resume failures that can be repaired under the same scientific contract.
---

# Failure Analysis Writer

## Overview
Preserve scientific negative evidence and investigate result-changing
anomalies without turning ordinary infrastructure trouble into paperwork.

## Consume
- `experiments/logs/experiment-log.md`, raw error notes, and `experiments/results/summary.md` when available.
- Optional `experiments/runbooks/runbook.md` and `experiments/plans/experiment-plan.md` for intended behavior.
- Optional user focus on one recurring failure mode.

## Produce
- `experiments/failures/failure-analysis.md`

## Workflow
1. Read `../../_shared/execution-authority.md` and triage the event. If it is a
   routine operational failure with an unchanged scientific contract, keep the
   evidence in run status/logs and route the smallest L1 repair and
   `attempt-N` retry to `$run-experiment`; do not create this artifact.
2. For a material scientific anomaly, result-changing code/data issue, weak
   result, or recurring unexplained failure, assign a stable
   `anomaly_id` and record it as a concrete observation.
3. Reproduce an important anomaly with the original data, command, seed, and
   analysis unchanged before proposing an adjustment; record whether it
   reproduces and link the raw evidence.
4. Inspect recent code, data, environment, and dependency changes, then trace
   the anomaly across the raw, cleaned, derived, and reported-result pipeline
   boundaries.
5. Classify the current cause as `bug`, `data`, `real_effect`, or `unknown`,
   keeping the classification separate from its supporting evidence.
6. Test one root-cause hypothesis at a time with the smallest discriminating
   test. Record `supported` or `rejected` before selecting another hypothesis;
   after three rejected branches, set the anomaly status to `BLOCKED_UNKNOWN`
   and stop result-changing adjustments.
7. Separate supported causes, rejected explanations, and still-untested hypotheses.
8. Group failures that point to the same underlying issue so the analysis stays actionable.
9. Record `adjustment_decision` as exactly one of `BUG_FIX_ALLOWED`,
   `DATA_CORRECTION_ALLOWED`, `PRESERVE_AS_REAL`, or `BLOCKED_UNKNOWN`, with
   the supporting hypothesis and test locators. A supported software cause may
   permit only its named bug fix; a supported data cause may permit only its
   named correction; a supported real effect must remain in the main analysis.
   End with the smallest useful next debugging branch when the state is
   `BLOCKED_UNKNOWN`. Require a user decision only when the resulting action is
   L3/L4; same-contract technical fixes remain L1.

## Quality Bar
- Keep observation and interpretation separate.
- Preserve failed evidence instead of rewriting history around successful runs only.
- Prefer a small number of high-value debugging branches over a generic brainstorm.
- Link every allowed adjustment to a supported root cause and its minimal test;
  an unexplained anomaly remains blocked rather than becoming a new analysis choice.
- Keep `anomaly_id`, reproduction status, change inventory, pipeline trace,
  cause class, hypothesis attempts, discriminating tests, and
  `adjustment_decision` visible as one auditable chain.
- Apply that full chain only to material anomalies; routine technical failures
  need only the run status, useful logs, repair, and next attempt.

## Boundaries
- Do not silently rewrite the experiment plan from inside this artifact.
- Do not convert this into a reviewer response unless the user asks.
- Do not blur confirmed root causes with guesses.
- Before a root cause is supported, do not delete observations, change seeds or
  statistical tests, transform the outcome, or change exclusion thresholds.
- Keep diagnostic transformations or exclusions in separately labeled
  exploratory outputs; never let them replace the original anomaly evidence.
- Do not create a failure-analysis artifact or file-content identifier solely
  to document a recoverable infrastructure failure.

## Open References Only As Needed
- Read `../../_shared/execution-authority.md` before deciding whether the event
  warrants a durable anomaly analysis or only an L1 retry.
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
