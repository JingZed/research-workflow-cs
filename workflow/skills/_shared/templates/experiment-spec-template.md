# Experiment Spec Template

- Mode: `exploratory` or `confirmatory`
- Status: `READY_FOR_RUNBOOK` or `BLOCKED`
- Blocker, when blocked:

## Exploratory Run Card

For `exploratory` mode, this is the complete required plan:

- Purpose:
- Variables and fixed scientific inputs:
- Owner and compute target:
- Incremental paid budget:
- Stop condition:
- Output path:

Add a metric, comparison, or quick analysis only when it is necessary to answer
the purpose. L2 cards do not need independent acceptance or confirmatory
metadata.

## Confirmatory Extension

Complete this section only for `confirmatory` mode.

### Claim Contract

- Hypothesis artifact:
- Prediction IDs:
- Baseline checklist:
- Baseline IDs and permitted use:
- Success threshold:
- Failure threshold:

### Data and Variables

- Dataset and split:
- Independent variables:
- Controlled variables:
- Seeds:

### Evaluation

- Metrics:
- Planned analysis -> prediction IDs -> baseline IDs:
- Ablations:
- Uncertainty or interval requirement:

### Budget and Stop Conditions

- Compute and time:
- Incremental paid budget:
- Stop if:

### Result-Aware Adjustment, When Applicable

- Anomaly ID:
- Supported cause and evidence:
- Exact scientific-contract change:
- L3 user-decision locator:

Routine Git, package, environment, download, scheduler, logging, and resume
repairs stay outside this section as L1 same-contract execution work.
