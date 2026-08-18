# Results To Claims Pattern

Use this pattern when `experiments/results/summary.md` should support writing and review without turning into manuscript prose.

## Recommended Output Shape

1. Input and ID reconciliation
2. Comparable, failed, blocked, and missing runs
3. Canonical result tuples
4. Allowed baseline deltas
5. Prediction and outcome-branch assessments
6. Anomalies, adjustments, and deviations
7. Observations
8. Bounded interpretations
9. Implications for current claims
10. Next checks

## Canonical Result Tuple

Give each paper-facing quantity a stable result ID and record its metric,
condition or comparison, value, unit, sign or direction, delta kind, baseline
ID, displayed precision, and exact source locator. A derived delta must state
whether it is absolute, relative, or percentage-point. If source values
conflict, keep the tuple blocked and route the conflict back to aggregation;
never choose the value that appears most often in prose or figures.

## Comparison Rule

Resolve baseline IDs against `experiments/plans/baseline-checklist.md`. A
baseline with `incompatible` or `unknown` parity cannot produce a primary gain.
A citation-only value is a reported reference, not a reproduced run. Keep such
numbers as context with their limitations rather than silently dropping them.

## Prediction Branch Rule

Resolve prediction IDs against `hypothesis.md`, then select one branch already
written for the relevant evidence question: `supports`, `does_not_support`,
`ambiguous`, or `technically_blocked`. Do not invent a favorable branch after
seeing the result. An unresolved ID, an indistinguishable rival, or a missing
planned branch leaves the assessment incomplete.

## Anomaly Adjustment Rule

When an anomaly led to deletion, exclusion, reseeding, transformation, test
replacement, or threshold change, link the exact adjustment to the canonical
failure analysis and its supported root-cause decision. Until that cause is
supported,
preserve the original analysis and label any diagnostic variant exploratory.

## Observation Rule

Observations should stay descriptive:

- what changed
- by how much
- under which setting
- compared with what baseline

Avoid slipping from "A beats B by 3.1" to "therefore the representation is causal" inside the same sentence.

## Bounded Interpretation Rule

Interpretations may say what the pattern suggests, but they must also carry their confidence limits:

- missing seeds
- missing variance estimates
- confounded settings
- low sample size
- broken or partial runs

If the evidence is not strong enough for a paper claim, say so directly.

## Implication Rule

After each main result cluster, ask:

- which draft claim does this support
- which draft claim is still under-supported
- which rival or null/artifact prediction remains viable
- what smallest next check would reduce uncertainty

That keeps the result summary connected to writing and review while staying non-rhetorical.
