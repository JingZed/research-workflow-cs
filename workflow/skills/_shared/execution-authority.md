# Research Execution Authority

Classify work by consequence, not by complexity, runtime, or the number of
steps. Default to forward progress and apply the lightest level that protects
the real risk.

## L0--L4

### L0: observe

Read, search, inspect, monitor, compare, and run non-mutating checks directly.
Do not create a durable report or notify the user when nothing material
changed.

### L1: routine reversible execution

Execute immediately and report only a useful milestone, failure, or blocker.
This includes focused tests and same-contract repairs for Git, packages,
environments, downloads, network transfers, schedulers, logging, and resume
mechanics. Preserve enough evidence to diagnose a first failure, then repair
and retry without asking the user.

Use `attempt-N` for a technical retry that preserves the scientific contract.
Reserve a fresh `rN` for a changed scientific contract or a distinct candidate
that may later be compared or promoted. Do not manufacture a new revision,
full failure report, or acceptance gate for each technical attempt.

### L2: autonomous noncanonical experiment

Write a compact run card, check it, and launch without waiting for user
approval. The run card contains only:

- purpose;
- variables and fixed scientific inputs;
- owner and compute target;
- incremental paid budget;
- stop condition;
- output path.

L2 covers reversible exploratory diagnostics, baselines, ablations, and
noncanonical comparisons across seeds, scenes, checkpoints, actions, or other
conditions. Keep them clearly labeled exploratory and do not silently replace
a confirmatory or paper-facing contract with them. One owner controls each
formal run cell, but ownership bookkeeping must not become an approval queue.

The standing paid-cost limits are less than USD 100 of incremental spend per
experiment and less than USD 300 per day. Existing prepaid, institution-owned,
or otherwise non-incrementally billed compute does not consume these limits.
Normal host policy, queue policy, and resource exclusivity still apply.

### L3: user decision

Ask the user before:

- canonical promotion or replacement of paper-facing evidence;
- a material research-direction choice or a result-aware change to a
  confirmatory contract;
- incremental paid spend at or above either L2 limit;
- work with unresolved licensing, privacy, security, or access-authority
  ambiguity.

Freeze only the affected branch while waiting. Independent work continues.
Ask one decision-complete question with the recommended option first.

### L4: exact-target confirmation

Immediately before a destructive, public, or effectively irreversible action,
show the exact source and target, expected effect, and recovery path, then get
explicit confirmation. L4 includes deleting or overwriting important data,
public submission or publication, sending an external message as the user, and
material permission or security changes.

## Two Execution Lanes

Use the exploratory lane by default for noncanonical learning:

```text
compact run card -> run -> change-only monitoring -> quick summary
```

Use the confirmatory lane only when results are intended to support a frozen
claim, paper-facing evidence, or canonical replacement:

```text
hypothesis -> full specification -> runbook -> run
-> rigorous aggregation -> explicit replacement plan only when the user asks
```

An evidence or quality check is a scientific branch condition, not a user
approval point. L0--L2 work does not require serial independent acceptance.

## Proportional Records and Verification

- Keep one compact status record for a short diagnostic. Require heartbeat,
  stall, checkpoint, and five-field milestone records only for genuinely long,
  costly, distributed, or opaque work.
- Record material decisions and scientific outcomes. Do not churn canonical
  notes for routine retries or unchanged monitoring sweeps.
- Do not compute, request, record, compare, or require hashes, checksums,
  digests, or tree fingerprints. Use exact paths, versioned names, direct file
  comparisons, semantic validation, byte sizes, modification times, and
  recoverable archives as appropriate.
- Preserve failed evidence without turning common network, package, download,
  scheduler, or environment failures into scientific anomaly reports.

## Literature Review Depth

Default remaining-paper work to a rapid structured pass over the converted
text and the sections that bear on relevance, methods, results, limitations,
and conflicts. Escalate to page-by-page PDF review only for a highly relevant
paper, key evidence, a material internal/source-conversion conflict, or an
explicit user request.

Routine papers do not require per-paper independent acceptance, reverse
provenance reconstruction, package-wide integrity ledgers, or page-by-page
visual checks.
