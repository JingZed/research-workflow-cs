---
name: paper-story-framer
description: "Frame a paper's evidence-backed story or contribution. Use story mode when the central reader question or narrative lens is unclear, and contribution mode when the story is stable but the novelty delta, contribution ladder, or field-level significance needs sharpening."
---

# Paper Story Framer

## Role

Turn current evidence into either a memorable narrative lens or a precise
contribution ladder. Run only the mode the request needs.

## Modes

- **story**: answer what problem the paper makes visible, what question it
  answers, and why the answer matters.
- **contribution**: answer what the paper changes or clarifies, compared with
  the closest prior work, at the strongest defensible scope.

If both are explicitly requested, settle story first in-session and then write
the two owned briefs. Do not create both files by default.

## Consume

- `hypothesis.md`, `claim-evidence-map.md`, and
  `experiments/results/summary.md` when present.
- Optional `literature-matrix.md`, current outline or manuscript, target venue,
  and `<paper-dir>/INVARIANTS.md`.
- Existing `drafts/story-brief.md` or `drafts/contribution-brief.md` when
  revising that mode.

## Produce

- Story mode: `drafts/story-brief.md`.
- Contribution mode: `drafts/contribution-brief.md`.

## Workflow

1. Select the mode from the requested outcome. Treat evidence, current
   invariants, and named claim boundaries as hard limits.
2. Build a compact in-session evidence map: major evidence block, comparison or
   control, result pattern, what it rules in or out, and remaining caveat. Do
   not save this scaffold as another artifact.
3. In **story mode**:
   - state the reader-facing problem, central question, evidence ladder,
     one-sentence answer, and overclaim risk;
   - when the story is unresolved, compare two or three genuinely different
     lenses; when the user supplies a direction, assess it plus at most one
     stronger alternative;
   - choose one primary story and verify every evidence-ladder rung directly.
4. In **contribution mode**:
   - use the settled story or infer a clearly labeled provisional one;
   - build three to five contribution rungs, each with a paper-facing claim,
     evidence anchor, nearest-prior contrast, scope boundary, and overclaim
     risk;
   - distinguish what was measured, what was found, and what readers should
     update; choose one strongest top-line contribution.
5. Write only the mode's brief. Include implications for title, abstract,
   introduction, figures, and discussion as concise guidance, not drafted
   sections or next-Skill routing.
6. If the requested mode cannot proceed because the other mode contains a
   material unresolved scientific choice, name that one decision and stop.

## Quality Bar

- The result is more than an experiment list.
- Every story rung or contribution claim has a current evidence anchor.
- Elevation comes from a sharper question, contrast, or implication, not wider
  claim scope.
- One sentence captures what the reader should remember or update.

## Boundaries

- Do not invent results, baselines, citations, mechanisms, or guarantees.
- Do not draft full manuscript sections or create a plan tree.
- Do not save internal scoring tables or automatically trigger outlining,
  figure work, critique, or prose revision.

## Open References Only As Needed

- Review `../../_shared/writing-constraint-layer.md` when framing could change
  claim scope.
- Review `../../_shared/artifact-contract.md` only when output ownership is
  unclear.
