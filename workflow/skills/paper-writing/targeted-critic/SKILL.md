---
name: targeted-critic
description: "Give a named artifact, evidence bundle, or manuscript one bounded read-only critique when the user requests it. A clear natural-language review or critique request may trigger this Skill; never run it as a prerequisite, automatic follow-up, or repeat review loop. Supports artifact, evidence, and paper modes."
---

# Targeted Critic

## Role

Give one current target a proportional second opinion. The user does not need
to name this Skill when the review intent and target are clear. This Skill never
runs as a prerequisite and never starts a review → fix → re-review cycle.

## Modes

- **artifact**: assess one artifact or section against one stated purpose.
- **evidence**: assess named results, claims, controls, or interpretation.
- **paper**: assess a scoped section or full named manuscript candidate.

Use the mode named by the user. Infer the narrowest fitting mode only when the
request is clear. Do not run several modes merely because their inputs exist.

## Consume

- The exact named target and requested scope.
- The single criterion or directly relevant evidence and invariants.
- In paper mode, the current source or trustworthy Markdown plus the rendered
  PDF only when layout is in scope.
- Prior findings only for an explicitly requested follow-up.

## Produce

- In-session findings by default.
- Optional user-requested durable report at one of:
  - `reviews/auto-review.md` for evidence mode;
  - `<paper-dir>/review-log.md` for paper mode;
  - a user-named `critique-output.md` for artifact mode.

Never create a durable report merely to prove the critique happened.

## Workflow

1. State the target, mode, criterion, and scope in one sentence.
2. Read the current target and only the evidence needed to judge it. Do not
   inherit an old verdict. When trustworthy text exists, do not render every
   PDF page; inspect only target pages needed for a named visual ambiguity.
3. Keep the pass read-only unless the current request explicitly includes
   edits. Do not dispatch another reviewer.
4. Apply the matching mode:
   - **artifact**: report `meets`, `needs changes`, or `not assessable`, with
     decisive evidence and at most three fixes;
   - **evidence**: check claim support, controls, uncertainty, alternatives,
     and interpretation, then rank only material fixes;
   - **paper**: check the requested scientific argument, claim-to-evidence
     alignment, method validity, limitations, clarity, and named layout issues.
5. Give each material finding an exact locator, why it matters, and the
   smallest useful fix. End with `no blocking issue found`, `revisions needed`,
   or `not assessable`; this is advice, not an acceptance state.
6. Stop after one pass. Write one compact report only when requested.

## Quality Bar

- Findings point to current text, values, figures, or source evidence.
- Depth matches the requested scope; a clean result is valid.
- Scientific scope is expressed through the actual evidence boundary.
- The fix package is short enough to act on directly.

## Boundaries

- Do not edit during a review-only request.
- Do not run automatically after writing, execution, build, or package checks.
- Do not create reviewer votes, coverage ledgers, content identifiers, gate
  records, approval states, routing fields, or per-finding state files.
- Do not require a durable report or a second round.

## Open References Only As Needed

- Review `../../_shared/writing-constraint-layer.md` for reader-facing prose.
- Review `../../_shared/artifact-contract.md` only when optional report
  ownership is unclear.
