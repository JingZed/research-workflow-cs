---
name: idea-creator
description: "Generate and rank research ideas from a direction, including a bounded landscape scan, 8-12 candidates, feasibility/impact/novelty screening, minimum pilots, eliminated ideas, and pilot-aware reranking. Use for brainstorming, finding a research direction, a complete idea-discovery pass, or reassessing candidates after pilot results."
---

# Research Idea Creator

## Role

Turn a bounded research direction into a ranked, falsifiable candidate set. Keep
divergent generation, ruthless filtering, cheap pilot design, and evidence-based
reranking in one report without promoting or activating an idea.

## Modes

- **generate**: generate and filter candidates from supplied or local evidence.
- **discovery**: include a bounded landscape scan, current-work search, local
  novelty screen, and reviewer-style objections in the same report. This
  preserves the useful behavior of the retired `idea-discovery` entry without
  recreating a Skill router.
- **rerank**: reassess an existing candidate report using named pilot results,
  new literature, or changed constraints.

Use the mode named by the user. Infer `discovery` for “from zero,” “full idea
discovery,” or equivalent requests; otherwise use `generate`.

## Consume

- A research direction, problem statement, observation, or user-supplied scope.
- Existing `<topic-root>/synthesis/literature-corpus.jsonl`,
  `literature-matrix.md`, `topic-map.md`, `research-gaps.md`, and reading notes
  when available.
- Resource constraints: data, compute, time, implementation capacity, required
  venue or audience, privacy, licensing, and unavailable assets.
- In rerank mode, the prior candidate report and exact pilot or feasibility
  evidence.

## Produce

- `<topic-root>/synthesis/idea-candidates.md`

## Workflow

1. Resolve `<topic-root>`. If the direction is too broad to distinguish useful
   candidates and local context does not bound it, ask for the smallest missing
   choice. Otherwise state reasonable assumptions and continue.
2. Build a short landscape from the existing topic corpus first. In discovery
   mode, fill material gaps with current public literature search; distinguish
   verified papers from search leads and record the search date and scope.
3. Generate 8–12 meaningfully different candidates. Each candidate states:
   question, hypothesis, why the answer matters in either direction, expected
   contribution type, closest known work, and the non-obvious delta.
4. Give every candidate a minimum discriminating test with data or assets,
   baseline, metric, positive signal, informative negative signal, rough
   compute/time cost, and the main confound. A pilot is a design here, not
   authorization to launch.
5. Filter on feasibility, expected information value, impact, novelty risk, and
   dependency risk. Reject generic “apply X to Y” ideas unless the transfer
   exposes a new mechanism, diagnosis, or consequential finding.
6. Keep 4–6 survivors and identify the top 2–3 pilot candidates. For each
   elimination, preserve one concrete reason so the same dead end is not
   rediscovered.
7. In discovery mode, stress-test survivors with the strongest reviewer
   objection and a recent-work overlap check. Label local-only novelty evidence
   as provisional; do not turn it into a global novelty claim.
8. In rerank mode, compare pilot evidence against the prewritten signal and
   confounds. Reward informative negative results and execution realism, not
   merely positive metrics.
9. End with one recommended candidate, ranked backups, killed ideas, the
   smallest next decision, and any evidence that would change the ranking.

## Quality Bar

- Candidate diversity comes from different questions or mechanisms, not renamed
  variants of one idea.
- Every top idea can be falsified and has a cheap first discriminating test.
- Rankings expose evidence, assumptions, costs, and uncertainty.
- Negative or null outcomes remain useful when they resolve a meaningful claim.

## Boundaries

- Do not promote, activate, or scaffold an idea workspace.
- Do not launch pilots unless the user separately requested execution and the
  applicable execution-authority contract permits it.
- Do not claim definitive global novelty from a bounded scan.
- Do not invoke a chain of Skills or create routing, gate, handoff, or state
  artifacts.

## Open References Only As Needed

- Read `references/idea-evaluation-rubric.md` for the candidate table and pilot
  scorecard.
- Read `../../_shared/artifact-contract.md` when topic-root or output ownership
  is unclear.
