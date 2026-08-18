---
name: experiment-watchdog
description: Monitor active and recent runs, classify running/completed/failed/stalled transitions, and persist a short watchdog report only when material state changes. Use for recurring or one-shot monitoring; unchanged sweeps stay silent, and same-contract technical repair/retry is routed automatically rather than becoming a user approval point.
---

# Experiment Watchdog

## Overview
Provide a deterministic monitoring sweep over active run directories so background execution can be checked without reading every log manually.

## Consume
- `experiments/runs/index.md` and any `experiments/runs/<run-id>/status.json` files.
- Optional `experiments/runs/<run-id>/stdout.log`, `experiments/runs/<run-id>/stderr.log`, and executed notebook snapshots for active or recent runs.
- Optional `notes/capabilities.yaml` when background monitoring is not always enabled.
- Optional stall threshold, current time budget, or alerting policy.

## Produce
- On first sweep or a material transition:
  `experiments/runs/watchdog-report.md` and
  `experiments/runs/watchdog-state.json`
- No file rewrite for an unchanged sweep unless an explicit snapshot is
  requested

## Workflow
1. Read `../../_shared/execution-authority.md`. Check
   `notes/capabilities.yaml`; if watchdog is off, persist the disabled state
   only when it is new or changed.
2. Scan known run directories and load machine-readable state.
3. Classify each run as running, completed, failed, stalled, or unknown using
   status plus recent log activity. Use the script's authoritative stall rule.
4. Compare the material snapshot—run ID, classification, raw status, and
   reason—with the previous watchdog state. If it is unchanged, do not rewrite
   reports, update notes, or notify the user.
5. On a transition, write a short state/report and surface newly completed,
   failed, or stalled runs first.
6. Route a routine same-contract technical failure to the L1 repair/retry path
   in `$run-experiment` without asking the user. Route results to
   `$result-aggregator`; use `$failure-analysis-writer` only for material
   scientific or recurring unexplained anomalies.
7. Notify the user only for an L3/L4 decision, an ownership conflict, or a
   material result/failure they need to know.

## Quality Bar
- Keep the classification rules explicit and stable.
- Record the effective stall threshold in `watchdog-state.json`, and surface it in `watchdog-report.md` when the report is produced manually or the script supports it.
- Surface stalled and failed runs first.
- Make the report short enough that a user can triage it quickly on mobile or between meetings.
- Treat unchanged state as a successful quiet sweep, not as a new milestone.

## Boundaries
- Do not reinterpret scientific results here.
- Do not auto-promote outputs or directly change a scientific contract.
- Do not launch retries inside the classifier; hand same-contract L1 repair and
  retry to `$run-experiment` or the owning automation.
- Do not silently mutate canonical experiment outputs.

## Open References Only As Needed
- Read `../../_shared/execution-authority.md` before notifying, escalating, or
  creating a durable monitoring record.
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/engineering-patterns.md` when capability flags or
  machine-readable run state affect monitoring behavior.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
- Review `references/watchdog-automation.md` when you want to schedule recurring monitoring over `experiments/runs/`.
- Use `scripts/watch_experiment_runs.py` when you need a deterministic classification pass over `status.json` and log files, including an explicit disabled state when `watchdog` capability is off.
