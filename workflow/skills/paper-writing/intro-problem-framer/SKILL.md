---
name: intro-problem-framer
description: "Draft the problem framing for a paper introduction. Use when Codex needs to write `drafts/intro.md` with the problem, stakes, gap, high-level approach, and contribution framing without collapsing into generic method-first writing."
---

# Intro Problem Framer

## Overview
Write the introduction around the problem and gap the work addresses, not around implementation details.

## Consume
- `drafts/outline.md`, optional `drafts/story-brief.md`,
  `drafts/contribution-brief.md`, and `research-gaps.md`.
- Optional `claim-evidence-map.md`, `experiments/results/summary.md`, and
  `<paper-dir>/INVARIANTS.md` when the introduction will state contribution
  boundaries or paper-facing claims.
- Optional `drafts/style-profile.md` when author, venue, or field style has
  been calibrated for this manuscript.
- Optional target venue or audience expectation.
- Supporting summaries for the most relevant prior work when available. If the
  topic has a shared literature corpus or idea-level literature matrix, inspect
  it before drafting the prior-work motivation bridge; do not assume Related
  Work will supply all literature context later.

## Produce
- `drafts/intro.md`

## Workflow
1. Read the result summary, claim structure, relevant literature, and active
   `<paper-dir>/INVARIANTS.md` before drafting or revising contribution
   framing. If an expected source is absent, state that absence rather than
   assuming a wider claim scope. If `drafts/story-brief.md` and
   `drafts/contribution-brief.md` both exist, verify that the story question is
   the question the contribution ladder answers. If they conflict, flag the
   mismatch before drafting instead of silently mixing them.
2. Before writing paragraphs, map `drafts/story-brief.md` into an in-session
   introduction argument plan when it exists. Use its central question, answer,
   evidence ladder, and overclaim boundary to decide what each paragraph must
   prove: which problem pressure it advances, which claim it establishes, how
   it moves the reader from field gap to thesis, and why it is not merely a
   method preview. Do not save this map as a file; it is a drafting scaffold.
   Verify that the Introduction will complete the six functional movements:
   (M1) problem pressure, (M2) gap/task, (M3) prior-work motivation bridge,
   (M4) why hard, (M5) this paper's principled approach, (M6) bounded thesis in
   one sentence, and (M7) optional contribution structure. The movements may be
   merged or split across
   paragraphs, but each must appear as a topic-sentence-level argument anchor,
   not be buried inside or replaced by procedural preview language such as
   `we first`, `we then`, or `we compare`.
3. Build a compact prior-work motivation bridge before the paper's own thesis.
   This bridge is not a Related Work section. It should identify a compact set
   of the most relevant prior-work clusters that make the paper's question
   natural, state the shared pressure or limitation in each line, and end with
   the specific gap the current paper tests. For a full conference paper this
   often means two to four clusters; shorter or tightly scoped papers may need
   fewer. Use concrete citation clusters when citation keys are available. If
   the relevant literature artifacts are missing or stale, write the
   introduction with an explicit blocker note rather than omitting the bridge.
   Treat a zero-citation, no-prior-work Introduction as a generation failure
   unless the user explicitly requests a citation-free draft.
4. Before revising an existing contribution summary or problem-gap claim,
   record the current claim, scope, and evidence anchors in the task. Preserve
   any sole comparison, metric, condition, or evidence phrase needed to ground
   the claim, then compare the revised text directly with the evidence and
   invariants.
5. Open with the real problem and why it matters in the target context. If
   `drafts/story-brief.md` exists, use its central question and reader-facing
   story as the preferred macro framing unless it conflicts with the outline or
   evidence.
6. Frame the gap in prior work using evidence from the current literature artifacts.
7. Introduce the high-level approach and contribution boundaries without overclaiming.
   When a boundary comes from internal constraints, translate it into a positive
   paper-facing role: what the paper tests, establishes, delimits, or conditions.
   Do not copy constraint wording as a defensive negative sentence.
8. Follow the plain-language scope rule in
   `../../_shared/writing-constraint-layer.md`. State what the paper tests,
   bounds, or shows in its setting instead of defining the contribution through
   defensive boilerplate.
9. End with contribution statements that match the results you actually have.
   If `drafts/contribution-brief.md` exists, use its contribution ladder as the
   preferred contribution ordering unless it conflicts with active evidence or
   constraints.
10. Compare revised contribution framing with the pre-edit claim, evidence
    anchors, and active invariants. Fix unsupported widening or missing anchors
    before handoff; no separate claim ledger is created.

## Quality Bar
- Keep the intro problem-led rather than method-led.
- Make the gap specific and evidence-backed.
- Include a prior-work motivation bridge that explains why the paper's question
  arises from existing work. The bridge should synthesize live literatures, not
  list citations, and should make clear what existing work leaves unanswered.
- Avoid generic claims that any paper in the area could say.
- Make each topic sentence an argumentative move, not a procedure summary or
  experiment itinerary.
- Do not let "we first / we then / we compare" substitute for the problem logic
  selected in `drafts/story-brief.md`.
- Make the contribution paragraph state the paper's thesis rather than listing
  result families.
- The contribution paragraph must state what the paper demonstrates in claim
  form, not what experiments were run or what results were found in
  result-list form.
- Express contribution boundaries as positive scoped claims. Paper-facing
  limitation language should name the evidence role or tested condition, not
  define the paper by what larger study it is not.
- Keep contribution scope aligned with active paper-global invariants when they
  exist.

## Boundaries
- Do not write the related work section inside the introduction draft.
- Do not outsource all prior-work positioning to Related Work. Introduction
  must still give enough literature context for a reader to understand why the
  paper's question is motivated and novel.
- Do not produce title or abstract variants here.
- Do not let unsupported claims leak into the contribution list.
- Do not allow `we first`, `we then`, `we compare`, or `the answer is` to
  substitute for problem/gap/necessity logic. These phrases are symptoms of
  preview structure when they appear before the Introduction has established
  the problem pressure, gap, and evaluation necessity.
- Do not widen contribution framing, problem-gap claims, or stakes claims beyond
  the tested setting and evidence boundaries recorded in active constraints.
- Do not use defensive paper-positioning templates in the Introduction,
  including `not a full ... study`, `rather than as a full ... study`, `we do
  not claim`, `should not be interpreted/read/treated as`, `X is not mechanism
  discovery`, or `not evidence of stronger ...`. Concrete empirical negative
  findings may remain when they report a measured result or ruled-out
  alternative.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/writing-constraint-layer.md` before revising an
  existing contribution summary or paper-facing problem-gap claim.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
