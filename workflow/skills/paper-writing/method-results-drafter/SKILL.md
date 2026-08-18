---
name: method-results-drafter
description: "Draft the methods and results sections from active idea artifacts. Use when Codex needs to turn experiment plans, result summaries, and plots into `drafts/method-results.md` that is specific, evidence-backed, and ready for later polishing."
---

# Method Results Drafter

## Overview
Translate experiment design and evidence into manuscript prose without detaching the text from the actual runs and figures.

Treat `experiments/results/summary.md` as a structured empirical source of
truth, not as a place to mine paper-style prose or figure/table numbering.

## Consume
- `experiments/plans/experiment-plan.md`, `experiments/results/summary.md`,
  `experiments/plots/index.md`, and `drafts/outline.md`.
- Optional `experiments/conceptual-figures/index.md` when methods/results prose
  needs to reference a framework figure, pipeline diagram, or method schematic.
- Optional `drafts/story-brief.md` when results prose should cash out the
  selected central question and evidence ladder.
- Optional `claim-evidence-map.md` and `<paper-dir>/INVARIANTS.md` when drafting
  or revising paper-facing result interpretations.
- Optional `experiments/failures/failure-analysis.md` for limitations or negative findings.
- Optional `refs.bib` when methods/results prose needs to mention prior work using existing citation keys.
- Optional `drafts/style-profile.md` when author, venue, or field style has
  been calibrated for this manuscript.
- Optional target venue style constraints.

## Produce
- `drafts/method-results.md`

## Workflow
1. Read the result summary, claim-evidence map, and active
   `<paper-dir>/INVARIANTS.md` before drafting paper-facing interpretations. If
   an expected source is absent, state the limitation instead of assuming a
   wider claim boundary.
2. Before revising a headline result, discussion bridge, or interpretation
   paragraph, record the current claim and its comparison, metric, condition,
   and evidence anchor in the task. Preserve that information in the revised
   text and compare the result directly with the evidence and invariants before
   handoff.
3. Before drafting results prose, map `drafts/story-brief.md` into an in-session
   result-family argument plan when it exists. For each major result family,
   name the claim it must support, the evidence anchor, the interpretation, the
   simpler alternative explanation it rules out, and the reader takeaway. Do
   not save this map as a file; use it as a paragraph-level drafting scaffold.
4. Describe the method, setup, and evaluation protocol at the level needed for reproducibility.
5. Draft the main results and ablations around the strongest tables and figures.
   Use conceptual figures only to explain framework, setup, or method logic; do
   not treat them as evidence for measured effects.
6. Separate observed results from stronger interpretive claims, and keep the latter proportional to the evidence.
7. Discuss limitations or failure cases only where the evidence supports them.
8. Follow the plain-language scope rule in
   `../../_shared/writing-constraint-layer.md`. Report failed controls,
   ruled-out alternatives, and measured null effects directly. Express claim
   boundaries by naming the tested condition and the role the evidence plays,
   rather than using generic defensive disclaimers.
9. Keep every substantive claim linked to a figure, table, or explicit experimental condition, ideally mirroring the claim-evidence structure already decided in `drafts/outline.md`.
10. Treat numbers, figure descriptions, and citations as evidence-integrity surfaces: every numeric claim should trace to current evidence artifacts, every figure/table description should stay faithful to the actual artifact, and every citation should resolve to an existing key in `refs.bib` when citations are used.
11. Use the result summary as a self-contained empirical record: pull raw numeric facts and qualitative observations from it without depending on manuscript-side figure numbers, table numbers, or section numbering.
12. For each results paragraph, make the comparison target, metric, condition, and interpretation boundary recoverable from the prose.
13. Make each result paragraph's topic sentence a claim that advances the
    paper's thesis, not a bare numeric observation. For each figure or table,
    ensure the caption or the adjacent prose states why the artifact matters,
    not only what it shows.
14. Compare every revised claim-facing paragraph with the pre-edit claim,
    evidence anchor, and active invariants. Fix unsupported widening or missing
    anchors before handoff; no separate claim ledger is created.

## Quality Bar
- Use concrete numbers and conditions, not vague praise.
- Keep the strongest result claim, secondary supporting claims, and caveats visibly distinct.
- Reference figures and tables consistently.
- Make each results paragraph do more than report a number: it should state what is compared, what metric or outcome matters, under which condition, and how far the interpretation can go.
- Make result paragraphs argumentative: the first sentence should be a thesis
  move supported by the paragraph, not the first number in a report.
- Explain why each figure or table matters in the caption or neighboring prose.
- Use experimental order only when that order itself serves the argument; do
  not let run order become manuscript structure by default.
- Build discussion bridges around what the result means or rules out, not only
  around what it does not prove.
- Keep interpretation boundaries paper-specific and evidence-linked: prefer condition-bound narrowing such as setting-specific scope, dataset coverage, or model dependence over generic disclaimer language.
- Use positive evidence-role language for scope boundaries. A result subsection
  may report what a test failed to show; it should not frame the paper's identity
  through generic negation.
- Keep result interpretations compatible with active paper-global invariants
  when they exist.
- Use only numbers that already exist in current evidence artifacts such as `experiments/results/summary.md` or the figure/table bundle derived from it.
- Describe figures and tables faithfully; do not infer visual trends or contrasts that the actual artifact does not support.
- When citing prior work in methods/results prose, use only citation keys that already exist in `refs.bib`.
- Keep raw numeric facts and qualitative observations distinguishable in the prose so later review can trace what was measured versus what was inferred.
- Treat superiority language as evidence-bound: only use "state-of-the-art", "best known", or equivalent wording when the experiments explicitly compare against a named published baseline on a public benchmark.
- Keep the draft close enough to the artifact contract that later updates stay manageable.

## Boundaries
- Do not generate titles or abstract variants here.
- Do not invent statistical or causal claims not supported by the experiments.
- Do not use mechanism-level or causal language when the current evidence only supports a descriptive comparison or partial result.
- Do not satisfy the interpretation-boundary requirement with generic hedging; the boundary must trace to a specific condition, scope, model, dataset, metric, or failure case from the experiments.
- Do not widen a headline result or interpretation paragraph beyond the active
  evidence and invariants.
- Do not introduce new numbers that are absent from the current evidence artifacts.
- Do not describe figures or tables in ways that are unsupported by the actual visual or tabular evidence.
- Do not invent or guess citation keys; only cite keys that already exist in `refs.bib`.
- Do not depend on manuscript-side references like "see Table 2" or "Figure 4 shows ..." inside the evidence source; treat the structured result summary itself as the source of truth.
- Do not write "state-of-the-art", "best known", or equivalent superiority claims unless the current evidence explicitly supports them with a named published-baseline comparison on a public benchmark.
- Do not hide weak results; frame them honestly.
- Do not use defensive paper-positioning templates. Concrete measured negative
  results stay allowed.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/writing-constraint-layer.md` before revising headline
  results, result interpretations, or discussion bridges.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
- Review `../paper-outline-builder/references/paper-plan-pattern.md` when you need to preserve the outline's claim-evidence matrix and hero-figure plan inside the prose draft.
