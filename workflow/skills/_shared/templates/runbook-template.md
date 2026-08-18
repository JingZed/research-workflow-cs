# Runbook Template

- Mode: `compact-exploratory` or `full-confirmatory`
- Source plan:
- Status: `READY` or `BLOCKED`
- Blocker, when blocked:

## Compact Runnable Core

- Purpose:
- Variables and fixed scientific inputs:
- Owner and compute target:
- Incremental paid budget:
- Stop condition:
- Output path:
- Entrypoint:
- Working directory:
- Environment:
- Copy-runnable command:
- Focused smoke check:
- Success signal:
- Failure signal:

This core is sufficient for a short, reversible, noncanonical L2 experiment.
Any placeholder in the entrypoint, working directory, environment, command, or
smoke check makes the run `BLOCKED`.

## Full-Run Extension

Complete only for confirmatory, multi-stage, long, costly, distributed, or
opaque work.

- Prediction IDs:
- Baseline IDs and intended use:
- Dependency and run order:
- Run ID and staging directory:
- Checkpoint policy:
- Standard output and error logs:
- Progress signal:
- Heartbeat expectation:
- Stall condition:
- Recovery or resume command:
- Expected exports:
- Paper-facing evidence exports:
- Aggregation handoff:

## Retry and Promotion Boundaries

- Record same-scientific-contract technical retries as `attempt-N`.
- Create a fresh `rN` only for a changed scientific contract or distinct
  candidate.
- Research workflows do not compute content identifiers for files. Record exact
  paths and use direct comparisons when transfer integrity matters.
- Prepare a canonical-replacement plan only when the user explicitly requests
  replacement of named outputs.
