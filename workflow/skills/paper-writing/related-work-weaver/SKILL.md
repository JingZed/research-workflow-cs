---
name: related-work-weaver
description: "Turn a literature matrix into related work prose. Use when Codex needs to write `drafts/related-work.md`, cluster prior work into meaningful groups, and position the current paper against those groups without producing a laundry list of citations."
---

# Related Work Weaver

## Overview
Convert structured literature comparison into readable related work that actually positions the paper.

The target is paper-specific synthesis, not a broad field survey and not a
laundry list of citations.

## Consume
- Optional `<topic-root>/synthesis/literature-corpus.jsonl` when it exists — use it as the primary paper inventory before scanning individual summaries or notes.
- The active `literature-matrix.md`,
  `<topic-root>/synthesis/topic-map.md`, and `refs.bib`.
- Optional `claim-evidence-map.md` and `<paper-dir>/INVARIANTS.md` when the
  related work will revise the paper's novelty claim or contribution boundary.
- Optional `drafts/outline.md` or venue conventions for related work style.
- Optional `drafts/style-profile.md` when author, venue, or field style has
  been calibrated for this manuscript.
- Optional `drafts/contribution-brief.md` when positioning the paper's novelty
  delta and nearest-prior-work contrast against related clusters.
- Optional `po-workspace/drafts/intro_relwork.tex` and
  `po-workspace/comparison-notes.md` when a PO backend scaffold is being
  selectively transplanted or used as a comparison baseline. These are
  comparison artifacts only; do not treat them as canonical prose. Route from
  `$po-related-work-backend` only when an explicit PO comparison was requested.
- Optional summaries of the most important comparison papers.

## Produce
- `drafts/related-work.md`

## Workflow
1. Establish the evidence scope for every related-work drafting or revision
   pass: name the corpus (`<topic-root>/synthesis/literature-corpus.jsonl`
   when present, the active literature matrix, `refs.bib`, and any paper
   summaries actually inspected), the claim structure (`claim-evidence-map.md`
   or contribution brief when relevant), and the constraint registry
   (`<paper-dir>/INVARIANTS.md` when present). If the corpus or matrix is
   absent, state that absence rather than silently assuming unrestricted
   positioning. If a prior-work attribution, literature summary, or novelty
   contrast cannot be traced to the sealed corpus scope, report an explicit
   blocker or assumption in the task response instead of filling the gap from
   model memory or inserting workflow language into manuscript prose.
2. Before revising an existing novelty contrast or claimed gap, record the
   current claim, nearest comparison, and source anchors in the task. After the
   edit, compare the wording directly with the same sources and active
   invariants.
3. Group prior work into a few meaningful clusters that match the current paper's positioning.
4. Read each matrix row's `evidence_role` before using it in positioning. Use
   `direct_prior` for bounded nearest-work and same-field coverage comparisons.
   Use `transferable_inspiration` only for clearly labeled cross-setting
   mechanisms, questions, or measurement ideas. Treat missing legacy roles as
   `unresolved` until the matrix owner classifies them.
5. Before drafting each cluster paragraph, build an in-session positioning plan:
   cluster claim, nearest prior work or family, unresolved limitation or
   assumption, the current paper's delta, and why that contrast matters. Do not
   save this plan as a separate artifact.
6. Summarize each cluster by its core approach, tradeoffs, and failure mode rather than by one-paper-at-a-time narration.
7. Keep the related-work scope micro and technical: use the section to compare against the nearest relevant prior work, not to restate the introduction's broad motivation.
8. Place the current work relative to those clusters using explicit differentiators tied to the paper's actual delta, nearest comparison point, and contribution boundary.
9. Identify the nearest-neighbor prior work or method family for the paper's
   main delta. If no single nearest neighbor exists, name the closest cluster
   and explain why the comparison is distributed.
10. Express novelty contrasts positively: state the nearest prior capability,
   the setting or question left open, and the current paper's scoped delta. Do
   not use internal boundary language as paper-facing prose.
11. Follow the plain-language scope rule in
    `../../_shared/writing-constraint-layer.md`. Express each cluster contrast
    through what prior work establishes, what question remains, and what the
    current paper adds in its tested setting.
12. Keep citation density high enough for rigor but low enough for readability, and prefer narrower, better-integrated coverage over broad but unfocused citation volume.
13. When a sentence groups three or more citations, make the synthesis explicit: state the shared point, the relevant contrast, or the positioning reason for grouping them.
14. Preserve conflict evidence when the corpus contains contradictory findings, assumptions, or evaluation settings that matter for the paper's gap; do not smooth every cluster into consensus.
15. For disputed areas, consider the optional shape consensus -> disagreement -> limitations -> gap, but use it only when the literature actually has that structure.
16. Use papers' `Reading basis:` when available to scale claim strength during synthesis; `unknown` or `title/abstract only` papers can motivate coverage or follow-up reading, but should not carry strong synthesis claims by themselves.
17. Before finalizing the section, check the related work against six quality dimensions: coverage, relevance, synthesis, positioning, organization, and citation rigor.
18. Compare revised novelty claims with the pre-edit claim, nearest comparison,
    sources, and invariants. Fix unsupported widening or missing source anchors
    before handoff; no separate claim ledger is created.

## Quality Bar
- Prefer synthesis over a citation laundry list.
- Use the matrix to keep comparisons factual and consistent.
- Preserve the matrix evidence-role boundary: transferable inspiration is not
  same-field coverage, nearest-prior, SOTA, or novelty evidence, and unresolved
  rows cannot carry strong positioning claims.
- Keep the positioning claim proportional to the actual delta of the paper.
- Keep novelty positioning compatible with active paper-global invariants when
  they exist.
- Treat mostly descriptive cluster summaries as a quality failure, not as an acceptable first draft.
- Treat novelty or positioning claims without explicit comparison to the nearest relevant prior work as a quality failure, not as acceptable rhetorical framing.
- Treat sparse, inconsistent, or weakly integrated citations as a quality failure, not as an acceptable tradeoff for readability.
- Do not reward high citation count unless the citations are relevant, distributed across the needed clusters, and integrated into the argument.
- Treat citation stacking as a quality failure when three or more citations appear together without a synthesis, contrast, or positioning sentence.
- Each paragraph should advance the paper's positioning argument; it is not
  enough to show coverage of a literature area.
- Every important citation cluster should be followed by a synthesis, contrast,
  or positioning sentence that explains why the cluster matters here.
- The nearest-neighbor contrast should be explicit enough that a reviewer can
  see what the current paper adds beyond the closest prior work or method
  family.
- Preserve important disagreements or setting-dependent conflicts from the corpus as positioning evidence or boundary evidence instead of writing only the consensus view.
- Use the consensus -> disagreement -> limitations -> gap pattern only as an optional organization aid for genuinely disputed areas, not as a required template.
- Scale synthesis strength to the weakest relevant reading basis in a cluster; mark `unknown` or abstract-only papers as needing follow-up before they support strong related-work claims.
- Keep boundary language paper-specific: prefer condition-linked narrowing moves such as observed failure modes, setting-specific results, or evidence-linked scope over generic limitation boilerplate.
- Keep novelty boundaries positive and comparative. The section should say what
  the cited cluster establishes and what this paper adds or delimits, not what
  larger genre of paper the current work is not.
- Use phrases like "under this setting", "in our experiments", "for this benchmark", "these results suggest", or "this points to" only when they match the actual evidence and inference strength; they are narrowing moves, not templates.
- Use coverage as a completeness check, not as a volume target: foundational and recent work should both appear when they matter, but citation count alone cannot rescue weak synthesis or weak positioning.
- Use navigation sentences only when they carry a concrete comparison or positioning move; do not stack generic openings such as "prior work has explored" or "many works have studied" without a paper-local claim.

## Boundaries
- Do not rewrite the bibliography file here.
- Do not repeat the introduction problem framing word for word.
- Do not invent missing comparisons that are not represented in the corpus.
- Do not relabel transferable inspiration as direct prior work in prose, or use
  it to claim that a same-field capability, benchmark result, or gap is absent.
- Do not introduce prior-work attribution claims, literature summaries, or
  novelty contrasts that cannot be traced to the sealed corpus scope. If an
  outside paper is needed, route to literature discovery, corpus maintenance,
  or citation repair before using it as paper-facing evidence.
- Do not widen the paper's claimed gap or novelty contrast beyond the active
  claim scope while making related work sound sharper.
- Do not hide conflict evidence just because a cleaner consensus paragraph would be easier to write.
- Do not force the consensus -> disagreement -> limitations -> gap skeleton onto non-disputed literature.
- Do not turn low-basis papers into strong synthesis evidence; phrase abstract-only material as reported or needing follow-up rather than demonstrated fact.
- Do not fall back to generic phrases like "existing work has several limitations" when a concrete cluster-level comparison sentence is possible.
- Do not use "future work will ..." or empty "we do not claim ..." boilerplate as a substitute for specific positioning.
- Do not use defensive paper-positioning templates as novelty contrasts.
- Do not use generic limitation or transition boilerplate as a substitute for evidence-linked boundaries, nearest-neighbor comparison, or concrete positioning.
- Do not treat descriptive summary, vague novelty positioning, or sparse citation support as "good enough" if the section still lacks synthesis, nearest-neighbor comparison, or citation rigor.
- Do not use citation volume to hide a missing nearest-neighbor contrast.
- Do not copy PO backend labels or workflow language into canonical
  related-work prose.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/writing-constraint-layer.md` before revising novelty
  positioning, claimed gaps, or contribution boundaries.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
