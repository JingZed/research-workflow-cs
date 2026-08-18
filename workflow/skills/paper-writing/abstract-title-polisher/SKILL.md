---
name: abstract-title-polisher
description: "Polish the title, abstract, and one-sentence pitch for a paper. Use when Codex needs to generate `drafts/abstract.md`, multiple `drafts/title-options.md` candidates, or concise contribution framing after the full paper story is already stable."
---

# Abstract Title Polisher

## Overview
Compress the paper's story into its highest-leverage front-door text once the evidence and outline are stable.

## Consume
- `drafts/outline.md`, `drafts/intro.md`, and `drafts/method-results.md`.
- Optional `drafts/story-brief.md` and `drafts/contribution-brief.md` when the
  title or abstract should express an already-selected story or contribution
  ladder.
- Optional `<paper-dir>/INVARIANTS.md` from the active paper workspace. When
  present, it is a required constraint registry even though it lives outside
  `drafts/`.
- Optional `experiments/results/summary.md` when the abstract or title refers
  to empirical findings.
- Optional `drafts/style-profile.md` when author, venue, or field style has
  been calibrated for this manuscript.
- Optional target venue length limit or title style preference.
- Optional advisor or collaborator feedback on positioning.

## Produce
- `drafts/abstract.md`
- Optional `drafts/title-options.md` when the title is still unstable or the user wants multiple candidates

## Workflow
1. Read the outline, result summary, claim structure, and active
   `<paper-dir>/INVARIANTS.md`. If an expected source is absent, state the
   limitation instead of assuming a wider claim boundary.
2. Before editing an existing title or abstract, write down 3–5 current claims
   and their evidence anchors in the task. Keep them visible while revising.
3. Before drafting, build an in-session front-door argument arc:
   `problem -> tension/gap -> intervention or contrast -> evidence ->
   implication -> boundary`. Do not save this arc as a file; use it to keep the
   abstract from becoming a method sequence or contribution list.
4. Generate a few title options with distinct emphasis only when the title is still unstable or the user explicitly wants alternatives.
5. Write the abstract around the problem, stakes, method delta, evidence, and main takeaway in one clean arc. If `drafts/contribution-brief.md` exists, use its top-line contribution as the target claim, but do not rephrase the contribution bullets from the introduction; write a narrative that flows from problem to stakes to finding to implication.
6. Run a sentence-role check: each abstract sentence should have one primary
   job such as context, gap, method delta, evidence, takeaway, or boundary.
   Merge or remove sentences that only restate navigation without adding a role.
   Identify the central finding sentence -- the one carrying the paper's main
   empirical claim -- and confirm it occupies a clear main-clause position
   rather than being embedded as one item in an evidence list. If the central
   finding shares a sentence with secondary results, split it out.
7. Follow the plain-language scope rule in
   `../../_shared/writing-constraint-layer.md`. State what the evidence
   establishes and under which condition instead of using defensive
   boilerplate.
8. Run a cold-reader simulation after drafting: assume a reviewer who does not
   know the task sees only the abstract and first paragraph for 90 seconds.
   Check whether that reader can extract what was done, the main finding, and
   why it matters. If the abstract requires knowing the task setup or internal
   method labels before it becomes meaningful, revise the first 1-2 sentences
   toward public, field-level framing.
   Also check for LaTeX formatting tokens used as semantic labels in the
   abstract, such as `\texttt{speak}`, `\texttt{act}`,
   `\texttt{consistency\_label}`, or any `\texttt{}` / `\verb||` token naming
   an internal protocol field. Treat these as cold-reader blockers equivalent
   to method-local shorthand: replace them with natural English, or defer the
   formal label to Methods.
9. Produce a one-sentence pitch that remains faithful to the paper's strongest supported claim.
10. Discard wording that sounds exciting but weakens precision.
11. Compare the revised title and abstract with the pre-edit claims, evidence
    anchors, and invariants. Fix unsupported widening or missing anchors before
    handoff; no separate claim ledger is created.

## Quality Bar
- Keep the title specific enough to signal task and contribution.
- Use public, field-level vocabulary before relying on paper-internal names or section-local concepts; readers should understand the abstract before reading the method section.
- LaTeX-typeset protocol tokens such as `\texttt{fieldname}` or `\verb||`
  count as method-local shorthand under the cold-reader rule; in the abstract,
  they must be preceded by natural language or omitted.
- Make the abstract self-contained and claim-precise: every claim must be grounded in the paper's evidence, but prefer relational framing (A exceeds B, C remains below D) over bare metric values unless the magnitude itself is the contribution.
- Include a real stakes move after the phenomenon and before the technical
  method when the paper's motivation depends on why the phenomenon matters.
  The first one or two sentences should establish the public evaluation premise
  or assumption the paper challenges, not jump directly to the paper's setup.
- Give the central finding enough prominence that a cold reader can identify it
  without reconstructing the paper from a result sequence.
- Multi-modifier compound terms such as `simple global-control-axis
  interpretation` or other dense abstract-noun stacks count as cold-reader
  burden even when no internal label is used. Prefer one short phrase that names
  the role the evidence plays, such as `reusable control handle` or
  `general-purpose steering direction`, over stacked qualifiers.
- Multidimensional takeaway sentences are acceptable when each dimension maps to a distinct piece of evidence or finding.
- Navigation scaffolding such as "We then", "We interpret", or "Empirically" is acceptable when it leads into concrete evidence or a concrete argumentative move.
- The abstract must read as a front-door argument, not a contribution bullet
  list or a "we do X, then Y" method summary.
- The final one or two sentences must answer why the result matters beyond the
  local experiment while staying inside the evidence boundary.
- Ensure the one-sentence pitch survives without hype adjectives.
- A boundary sentence in the abstract must say what role the evidence plays,
  not what larger paper the work is not. Prefer `boundary stress test`,
  `label-proximal upper bound`, `condition-dependent apparent consistency`, or
  another paper-specific positive role over defensive negation.

## Boundaries
- Do not rewrite the whole paper from inside the abstract pass.
- Do not overfit to venue keyword trends at the expense of clarity.
- Do not claim broader impact that the paper does not establish.
- Do not widen title or abstract claim scope without a tested-setting qualifier
  traceable to the active `INVARIANTS.md`.
- Do not lead the abstract with internal experiment names, donor labels, or method-local shorthand before explaining the claim in common field terms.
- Do not use `\texttt{}`, `\verb||`, or typewriter-font markup as the primary
  name for a protocol field in abstract or title prose; introduce the concept
  in natural language first, and defer the formal typeset label to Methods.
- Do not compress the abstract into a contribution-bullet list or a sequence of method-local labels; the reader should get the paper's public claim before seeing internal shorthand.
- Do not over-hedge to the point of sounding like a disclaimer; the abstract should represent the paper's strongest defensible claim faithfully, neither inflated nor shrunk.
- Do not put defensive claim-boundary templates in the abstract or title,
  including `not a full ... study`, `rather than as a full ... study`,
  `we do not claim`, `should not be interpreted/read/treated as`, or `X is not
  mechanism discovery`. Translate those constraints into positive scoped
  contribution language.
- Do not let `drafts/style-profile.md`, venue keywords, or collaborator
  preference widen the title or abstract beyond the active evidence boundary.
- Do not include source attribution, provenance notes, workflow terms, or
  calibration references in title or abstract prose.

## Open References Only As Needed
- Review `../../_shared/writing-constraint-layer.md` before editing an existing
  title or abstract, or whenever an abstract/title pass may change claim scope.
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
