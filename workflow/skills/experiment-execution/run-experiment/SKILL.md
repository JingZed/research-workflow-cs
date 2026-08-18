---
name: run-experiment
description: "Launch READY exploratory or confirmatory runs, make bounded same-contract technical repairs and retries, and preserve proportional run-local state. An optional explicit record mode can update a legacy experiment log without making append-only logging a required workflow step."
---

# Run Experiment

## Role

Turn a ready runbook into live execution with the smallest state needed to
recover. Keep execution facts beside the run instead of growing a parallel
workflow history.

## Modes

- **run** (default): prepare, launch, repair, retry, and report a run.
- **record**: explicitly requested compact update to an existing legacy
  experiment log; never a prerequisite for launch or aggregation.

## Consume

- `experiments/runbooks/runbook.md` and
  `experiments/plans/experiment-plan.md`.
- Optional environment notes, source, run registry, current run directories,
  and paper-facing evidence rules directly relevant to execution.
- `infrastructure/compute-hosts.md` plus a fresh host snapshot before GPU work.
- Optional existing `experiments/logs/experiment-log.md` only in record mode.

## Produce

- Run mode:
  - `experiments/runs/index.md` for named or multi-run work;
  - `experiments/runs/<run-id>/status.json`;
  - `experiments/runs/<run-id>/stdout.log` and `stderr.log` when applicable;
  - optional `launch.md` for long, costly, distributed, confirmatory, or
    otherwise non-obvious launches;
  - optional `attempt-N/` state for same-contract technical retries;
  - optional `executed.ipynb` for notebook-first execution;
  - only bounded code, configuration, entrypoint, logging, and focused test
    changes required by the existing scientific contract.
- Record mode: optional update to an existing
  `experiments/logs/experiment-log.md` when the user explicitly asks.

## Workflow

1. Select the mode. For run mode, read
   `../../_shared/execution-authority.md`, classify the action, proceed at
   L1/L2, and freeze only the affected L3/L4 branch.
2. In **run mode**:
   - inspect readiness and make the smallest same-contract implementation,
     environment, logging, or test repair needed;
   - resolve the execution target, refresh compute availability, and verify
     prerequisites;
   - prefer the stable notebook or CLI entry point already named by the runbook;
   - keep one `run-id` per scientific contract and use `attempt-N` for routine
     technical retries; create a new revision only for a material contract or
     candidate change;
   - stage outputs away from paper-facing bundles and match observability to
     duration, cost, distribution, and opacity;
   - launch ready L2 work without a serial approval queue;
   - record only exact command, target, start/status, output paths, and useful
     logs, adding recovery detail only when warranted;
   - on technical failure, preserve useful state, repair within the same
     contract, run focused checks, and retry as `attempt-N`.
3. In **record mode**:
   - read run-local status and logs rather than reconstructing shell history;
   - append one compact material run outcome, anomaly, or decision only when
     the existing project still uses `experiment-log.md`;
   - point to run paths instead of copying telemetry, and do not log unchanged
     monitoring or every attempt;
   - if the live log already exceeds 200 lines, compact repeated operational
     detail into run-path pointers only when no unique evidence would be lost.
4. Report only a material launch, transition, failure, or result with its run
   ID and inspection paths. Unchanged monitoring is silent.

## Quality Bar

- Commands are copy-runnable when the environment is known.
- Long runs expose a log path, progress signal, and stall condition.
- Staging and paper-facing outputs remain distinct.
- Later work can resume from run-local state without a separate audit dossier.

## Boundaries

- Do not silently change a confirmatory scientific contract.
- Do not aggregate or interpret results, claim success from launch alone, or
  treat notebook output as canonical evidence before export.
- Do not compute or store content hashes, checksums, digests, or fingerprints;
  use exact paths and direct comparison.
- Do not create a new revision, full failure analysis, independent acceptance
  step, or global log entry for a routine technical failure.

## Open References Only As Needed

- Read `../../_shared/execution-authority.md` before launch or retry decisions.
- Review `../../_shared/artifact-contract.md` only when output ownership is
  unclear.
- Review `references/notebook-first-execution.md` for notebook-first runs.
- Use `scripts/run_notebook_experiment.py` when its deterministic wrapper fits
  the named runbook.
