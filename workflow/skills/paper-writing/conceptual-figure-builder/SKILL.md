---
name: conceptual-figure-builder
description: "Specify, explore, build, revise, or explicitly critique one paper-facing conceptual or method figure. Use spec, explore, build, or critique mode for the requested action; build is the default when the content direction is settled, and no mode automatically triggers another."
---

# Conceptual Figure Builder

## Role

Own one figure from a concise specification through production without turning
its modes into mandatory phases. Run one requested mode at a time.

## Modes

- **spec**: settle scientific content, visible labels, relations, and delivery
  constraints before rendering.
- **explore**: explicitly requested comparison of one primary visual direction
  and at most one materially different alternative.
- **build**: produce or revise the figure and perform focused local QA. This is
  the default for a settled brief, reference, or existing figure.
- **critique**: explicitly requested read-only visual assessment.

## Consume

- Relevant story, contribution, outline, manuscript, evidence, or explicit
  user instruction.
- Optional `drafts/figures/<figure-id>.spec.md`, prior render, editable source,
  selected reference, or `<figure-id>.visual-direction.md`.
- `<paper-dir>/INVARIANTS.md` when wording affects a protected claim.

## Produce

- Spec mode: `drafts/figures/<figure-id>.spec.md`.
- Explore mode, only when requested:
  - `experiments/conceptual-figures/<figure-id>.candidate-board.md`;
  - optional `<figure-id>.visual-direction.md` and up to two candidate images.
- Build mode:
  - `experiments/conceptual-figures/<figure-id>.png`;
  - optional SVG, overlay, scaffold, prompt, or path manifest only when the
    production method needs it;
  - optional `<figure-id>.qa.md` or existing figure index update when the
    project already keeps that record or the user requests it.
- Critique mode: in-session findings by default; optional
  `experiments/conceptual-figures/<figure-id>.critique.md` when requested.

## Workflow

1. Select one mode from the request. Do not execute the other modes as gates.
2. Preserve the claim boundary, required labels, figure-versus-caption split,
   aspect ratio, intended insertion size, editability, and reference role.
3. Apply the matching mode:
   - **spec**: state the reader question, visual payoff, evidence anchors,
     required visible content, caption-only detail, minimum regions and
     meaningful relations, formats, and one unresolved material decision if
     present;
   - **explore**: compare no more than two structurally distinct directions on
     reading path, paper-native fit, text capacity, claim alignment, and
     production risk, then select one only when the evidence is clear;
   - **build**: choose the simplest suitable production method, build one
     primary figure, inspect the actual render at insertion size, and make at
     most one bounded correction pass;
   - **critique**: inspect the render first, report `pass`, `needs changes`, or
     `not assessable`, and give at most five evidence-linked observations plus
     the smallest fix package.
4. Return the result and stop. A later mode runs only on a new explicit request.

## Quality Bar

- The figure communicates one paper-relevant idea within the evidence boundary.
- Required labels and connector meanings are visible and legible.
- Hard aspect ratio and placement constraints are preserved.
- Optional files exist only because the selected mode needs them.

## Boundaries

- Do not create candidate matrices, reviewer states, salvage states, gate
  fields, next-owner ledgers, or automatic regeneration loops.
- Do not move required content into the caption or paraphrase locked labels to
  make them fit.
- Do not expose image-generation credentials.

## Open References Only As Needed

- `references/output-mode-selection.md` for production method choice.
- `references/hybrid-asset-pattern.md` or
  `references/raster-scaffold-overlay.md` for hybrid assets.
- `references/prompt-library.md` for image-generation prompts.
- `references/figure-qa-rubric.md` for focused visual QA.
- `../../_shared/templates/figure-spec-template.md` for a durable spec.
- `../../_shared/templates/figure-critique-template.md` for a requested report.
