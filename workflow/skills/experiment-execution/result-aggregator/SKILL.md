---
name: result-aggregator
description: "Aggregate selected experimental outputs into `experiments/results/summary.md` with traceable numbers, baseline deltas, uncertainty, bounded interpretations, and explicit limitations."
---

# Result Aggregator

## Overview

Create a self-contained empirical source of truth for one project or active
idea.

## Consume

- Raw metrics and structured outputs from explicitly selected runs.
- Run logs, configs, and the runbook.
- `hypothesis.md` and `experiments/plans/baseline-checklist.md` when those
  artifacts exist.
- `experiments/failures/failure-analysis.md` when an anomaly led to a proposed
  exclusion, seed change, transformation, test change, or data correction.
- Project-specific metric definitions and comparison rules.

## Produce

- `experiments/results/summary.md`

## Workflow

1. Confirm that every selected run belongs to one project and comparison
   family.
2. Record whether each input is staged or canonical. Explicitly selected staged
   outputs may be aggregated before promotion; promotion is required only to
   replace a paper-facing canonical bundle.
3. Resolve every used `prediction_id` against `hypothesis.md` and every used
   `baseline_id` against the canonical baseline checklist. Mark unresolved or
   ambiguous references `INCOMPLETE`; do not repair an upstream ledger here.
4. Separate complete comparable runs from failed, partial, or confounded runs.
   Keep failed, null, blocked, and missing evidence visible whenever it affects
   the comparison or interpretation.
5. Normalize metrics into a canonical result tuple containing a stable result
   ID, metric, condition or comparison, value, unit, sign or direction,
   `delta_kind` and `baseline_id` when applicable, displayed precision, and
   source locator. Use these tuples, not manuscript wording or a majority of repeated
   values, as the numeric source for downstream checks.
6. Compute a primary baseline delta only when the baseline ledger permits
   `primary_comparison` and its parity and availability support that use.
   `incompatible` or `unknown` parity and `citation_only` references may remain
   contextual but must not yield a primary gain claim.
7. Link every reported number to its run, config, seed, sample size, and
   canonical result tuple.
8. For each evaluated prewritten evidence question, record the referenced
   `prediction_id`
   values and select exactly one prewritten branch from `supports`,
   `does_not_support`, `ambiguous`, or `technically_blocked`. Base the selection
   on the observed evidence without rewriting the planned threshold or branch.
9. When an anomaly motivated a result-changing adjustment, require the linked
   failure analysis to authorize that exact adjustment with an applicable
   `BUG_FIX_ALLOWED` or `DATA_CORRECTION_ALLOWED` decision. A
   `PRESERVE_AS_REAL` or `BLOCKED_UNKNOWN` state cannot authorize replacement.
   Otherwise preserve the original result, label the adjusted analysis
   exploratory, and mark the paper-facing interpretation blocked.
10. Separate observation, bounded interpretation, implication, and next check.
11. For paper-facing findings, state the tested scope and whether the evidence
    is partial, negative, diagnostic, ambiguous, or technically blocked. Do not
    infer a stronger evidence status than an upstream plan supplies.

## Quality Bar

- Numbers are reproducible from named inputs.
- Comparisons use compatible settings and resolve to allowed baseline IDs.
- Every paper-facing value has one canonical result tuple; conflicting source
  values remain an explicit blocker rather than being reconciled by vote.
- Every prediction assessment names a resolvable prediction and one planned
  outcome branch.
- An anomaly-dependent adjustment is either authorized by a supported
  root-cause decision or kept exploratory and unable to replace the original.
- Uncertainty and missing support remain visible.
- The summary does not depend on manuscript figure or table numbering.

## Boundaries

- Do not merge unrelated projects.
- Do not turn specific results into universal or mechanistic claims.
- Do not upgrade prediction, baseline parity, or anomaly-adjustment states that
  belong to upstream owners.
- Do not omit an unfavorable run or switch a threshold, baseline, seed,
  exclusion, transformation, or statistical test because of its outcome.
- Do not choose plot aesthetics or silently discard failures.

## Open References Only As Needed

- Review `references/results-to-claims-pattern.md` for a stable summary shape.
- Review `../../_shared/artifact-contract.md` for ownership.
