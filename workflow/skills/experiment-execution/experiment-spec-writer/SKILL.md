---
name: experiment-spec-writer
description: Write either a compact exploratory run card or a full confirmatory experiment specification in `experiments/plans/experiment-plan.md`. Use when datasets, metrics, variables, seeds, budget, stop conditions, or the scientific contract must be fixed before execution; do not require the full confirmatory form for a reversible noncanonical diagnostic.
---

# Experiment Spec Writer

## Overview
Choose the lightest plan that makes the next run scientifically legible. Use a
compact exploratory card for noncanonical learning and a full specification
only for confirmatory or paper-facing evidence.

## Consume
- For exploratory mode, the research question and the directly relevant local
  evidence or prior run.
- For confirmatory mode, `hypothesis.md`,
  `experiments/plans/baseline-checklist.md`, and any relevant
  `experiments/plans/reproduction-plan.md`.
- Optional `experiments/failures/failure-analysis.md` when a prior anomaly
  motivates a result-changing adjustment.
- Optional resource constraints such as hardware, time, or advisor guidance.
- Optional target paper or benchmark conventions.

## Produce
- `experiments/plans/experiment-plan.md`

## Workflow
1. Read `../../_shared/execution-authority.md` and select the lane:
   - `exploratory` for reversible, noncanonical learning under L2;
   - `confirmatory` when the run is intended to support a frozen claim,
     paper-facing evidence, or canonical replacement.
2. In exploratory mode, write only the six-field run card: purpose; variables
   and fixed scientific inputs; owner and compute target; incremental paid
   budget; stop condition; and output path. Add a metric or comparison only
   when it is needed to answer the stated purpose.
3. In confirmatory mode, resolve stable `prediction_id` and `baseline_id`
   values, then define datasets, splits, metrics, baselines, ablations, seeds,
   uncertainty, budget, success/failure thresholds, and stop conditions.
4. Treat Git, package, environment, download, scheduler, logging, and resume
   repairs as L1 execution details, not experiment redesign. A noncanonical
   diagnostic for a scientific anomaly may remain exploratory under L2. A
   result-aware change to a confirmatory contract is L3 and needs a user
   decision.
5. Keep tradeoffs visible when time or hardware constrains the plan. Escalate
   paid cost only when it reaches the shared L3 threshold.
6. Only for a genuinely multi-stage, long, costly, or scientifically branching
   effort, add a compact `Stages and risks` section to this same file. Tie each
   stage to a concrete artifact or decision, name the major risk and fallback,
   reference stable prediction IDs where evidence changes the path, prewrite
   `supports`, `does_not_support`, `ambiguous`, and `technically_blocked`
   outcomes, and state an exit condition. Omit this section for a one-run
   diagnostic; never create a separate milestone plan.
7. End with `READY_FOR_RUNBOOK` or one concrete scientific blocker. Missing
   confirmatory metadata does not block an otherwise valid exploratory card.

## Quality Bar
- Make the selected lane explicit and keep the record proportional to it.
- Keep exploratory cards short enough to inspect in one screen.
- For confirmatory plans, keep success/failure thresholds explicit and require
  resolvable prediction and baseline IDs with compatible use.
- When staged decision branches are needed, keep them concrete, complete, and
  inside `experiment-plan.md`; do not add a second planning tree.
- Distinguish fixed scientific inputs from variables by exact path and versioned
  name. Research plans do not compute file-content identifiers.

## Boundaries
- Do not turn the plan into command-level execution details; use `$runbook-generator` next.
- Do not hide a material scientific choice under a placeholder.
- Do not write manuscript prose in this artifact.
- Do not copy the baseline ledger into the plan; reference its stable IDs and
  record only experiment-specific use.
- Do not claim preregistration, outcome blindness, or confirmatory eligibility
  from this planning artifact.
- Do not require user approval or independent acceptance for a ready L2
  exploratory card.

## Open References Only As Needed
- Read `../../_shared/execution-authority.md` before choosing exploratory or
  confirmatory depth and before requiring a user decision.
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
- Review `../../_shared/templates/experiment-spec-template.md` when you need the specific structure, template, or integration note for this skill.
