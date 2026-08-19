---
name: results-sufficiency-review
description: "Judge whether the current experimental evidence is sufficient for the planned paper claims. Use when the user asks whether results are enough, whether writing can begin, which claims are supported, or what minimum evidence is still missing."
---

# Results Sufficiency Review

## Role

Give a claims-driven readiness judgment without recomputing results, running
experiments, or turning the judgment into an approval gate.

## Consume

- `experiments/results/summary.md` as the primary empirical source.
- `hypothesis.md`, experiment plan, baseline checklist, runbook, and relevant
  failure analysis when they exist.
- Planned paper claims, scope boundaries, project invariants, and named venue or
  audience requirements when relevant.
- Exact raw or run artifacts only to resolve a material ambiguity in the
  summary, not to redo aggregation.

## Produce

- An in-session verdict by default.
- Optional `experiments/results/sufficiency-review.md` when the user requests a
  durable assessment.

## Workflow

1. Identify the exact claims the evidence is expected to support. If no claim
   set exists, derive a provisional set from the hypothesis and clearly label
   it.
2. Read the current result summary first. If it is missing, stale relative to
   named canonical runs, internally inconsistent, or lacks source locators,
   return `BLOCK` with the smallest repair needed.
3. Map every claim to named evidence and classify it as `supported`, `weak`,
   `missing`, `conflicting`, or `technically blocked`.
4. Check comparison validity: baseline parity, controls, sample/seed coverage,
   uncertainty, effect size and units, ablations, failure cases, negative
   results, exclusions or corrections, and the tested generalization scope.
5. Distinguish evidence needed for a central claim from evidence that is merely
   desirable. Do not require an idealized experiment package when the bounded
   claim is already supported.
6. Issue exactly one advisory verdict:
   - **SUFFICIENT**: current evidence supports the bounded planned claims well
     enough to draft from;
   - **NEEDS MORE**: the core direction remains viable, but one or more named
     claims require a specific additional experiment or analysis;
   - **BLOCK**: the result source is absent/unreliable, the comparison is
     fundamentally invalid, or the planned central claim is contradicted with
     no defensible narrower story.
7. For `NEEDS MORE` or `BLOCK`, give the minimum additional evidence package in
   priority order, with the claim it resolves and rough cost. For `SUFFICIENT`,
   state the exact claim boundary and limitations that must remain visible in
   writing.
8. End with one next scientific action. Do not mutate project state or start the
   action automatically.

## Quality Bar

- Every verdict is traceable to claim-evidence rows.
- Missing baselines, uncertainty, failures, and conflicting runs remain visible.
- The review does not silently strengthen a claim to match a positive result.
- “Enough to draft” is separated from “guaranteed to satisfy reviewers.”

## Boundaries

- Do not aggregate statistics, exclude runs, alter thresholds, or generate
  figures.
- Do not call the verdict a workflow gate or authorization for promotion,
  submission, or canonical replacement.
- Do not demand new experiments that do not change the bounded claim decision.

## Open References Only As Needed

- Read `references/sufficiency-rubric.md` for the claim-evidence table and
  minimum-evidence checklist.
- Read `../../_shared/artifact-contract.md` for result and review ownership.
