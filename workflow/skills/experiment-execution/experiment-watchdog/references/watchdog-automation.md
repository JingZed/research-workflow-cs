# Watchdog Automation

Use this reference when you want recurring monitoring over `experiments/runs/`.

## Recommended Frequency

- Every 2 hours is a good default for notebook-heavy runs.
- Use hourly only when many short jobs are active.

## What the Automation Should Do

1. Run the watchdog classification script over the current workspace.
2. Write `experiments/runs/watchdog-report.md` and `watchdog-state.json` only
   on the first sweep or a material state transition.
3. Return quietly when classifications and reasons are unchanged.
4. If a run is newly `completed`, `failed`, or `stalled`, route the transition
   to the appropriate owner. Same-contract technical repair/retry proceeds at
   L1; scientific interpretation goes to `$result-aggregator` or, for a
   material anomaly, `$failure-analysis-writer`.
5. Open an inbox item only for an L3/L4 decision, ownership conflict, or a
   material result/failure that needs human attention.

## What It Should Not Do Automatically

- promote outputs
- rewrite result summaries
- trigger paper-writing changes
- change a scientific contract

Keep classification deterministic. Let `$run-experiment` or the owning
automation perform a bounded same-contract L1 repair and `attempt-N` retry;
the watchdog itself does not mutate the run.
