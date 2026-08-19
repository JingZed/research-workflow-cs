---
name: novelty-sanity-check
description: "Run a fast local-only novelty screen against the current topic corpus and reading artifacts. Use to find nearest-neighbor papers, estimate overlap, expose obvious novelty risks, or decide whether a broader novelty-check is worth doing before experiment design."
---

# Novelty Sanity Check

## Role

Stress-test one candidate against evidence already in the workspace. This is a
cheap local screen with a durable, clearly bounded result when requested.

## Consume

- One candidate idea, backlog item, `idea.md`, or novelty claim.
- `<topic-root>/synthesis/literature-corpus.jsonl` as the primary local paper
  inventory when it exists.
- Relevant `literature-matrix.md`, `topic-map.md`, `research-gaps.md`,
  single-paper summaries, notes, and bibliography.

## Produce

- An in-session report by default.
- Optional `<target-dir>/novelty-sanity-check.md` when the user requests a
  durable local screen.

## Workflow

1. Resolve the candidate and local corpus boundary. Do not use network search in
   this Skill.
2. Decompose the idea into task/problem, method family, data or benchmark,
   operating setting, evaluation, and claimed delta.
3. Identify the closest local papers and compare them across those dimensions.
   Cite concrete papers and local evidence locators.
4. Assign local novelty risk:
   - **high**: a neighbor overlaps on task, method family, and setting/data, and
     the claimed delta is not uniquely identifiable;
   - **medium**: a neighbor overlaps on task + method or task + setting/data,
     while the delta appears plausible but needs a named paper or result check;
   - **low**: no neighbor overlaps on more than one major dimension, or the
     claimed finding/evaluation is empirically distinct despite partial overlap;
   - **unknown**: the local corpus is too thin or stale to support a useful
     judgment.
5. Separate `not locally differentiated`, `not yet verified`, and `locally
   distinct`. List the smallest external searches or paper reads that would
   resolve uncertainty.
6. End with `safe for hypothesis framing`, `run global novelty-check`, or
   `reframe before proceeding`. This is advice, not activation authority.

## Quality Bar

- Every risk judgment names its nearest neighbors and overlap dimensions.
- The report states corpus size, coverage, and freshness limitations.
- Missing evidence remains visible instead of being converted into low risk.

## Boundaries

- Do not claim a global novelty verdict.
- Do not search the web, create paper workspaces, or update the topic corpus.
- Do not write a hypothesis or full experiment plan.

## Open References Only As Needed

- Read `../../_shared/artifact-contract.md` when topic-root or durable output
  ownership is unclear.

