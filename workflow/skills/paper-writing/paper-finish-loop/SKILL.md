---
name: paper-finish-loop
description: "Build, finish, or check one named paper candidate. Use build mode to materialize and compile, finish mode to repair a bounded package issue, or submission-check mode for a read-only blocker assessment; no mode requires an independent review or promotes the candidate."
---

# Paper Finish Loop

## Role

Operate on the paper candidate that would actually be built or submitted. Run
one requested mode and stop when its direct acceptance criterion passes.

## Modes

- **build**: materialize missing requested package content, compile, and record
  current build status.
- **finish**: repair named source, bibliography, figure, formatting, or package
  problems, then rebuild and verify those changes.
- **submission-check**: perform a read-only check of the exact named candidate.

## Consume

- Exact `<paper-dir>/`, source entry point, bibliography, figures, venue files,
  build instructions, and `<paper-dir>/INVARIANTS.md`.
- Current result or claim evidence only when claim wording or displayed numbers
  are in scope.
- Venue rules and deadline constraints in submission-check mode.

## Produce

- Build or finish mode:
  - `<paper-dir>/` updates within the requested scope;
  - `<paper-dir>/tex-profile.json` when environment probing is needed;
  - `<paper-dir>/finish-report.md`;
  - optional `latex-sanity.txt` or `pdf-packaging-report.json` only when the
    corresponding check ran.
- Submission-check mode: `<paper-dir>/submission-checklist.md`.

## Workflow

1. Resolve the exact named candidate and mode. Never infer permission to
   replace a canonical paper.
2. Inspect current sources, assets, bibliography, invariants, and relevant
   evidence. Preserve unrelated user edits.
3. In **build** or **finish** mode:
   - make only requested or directly necessary package changes;
   - run focused source checks for structure, labels, assets, anonymity, and
     references;
   - compile using the documented project command;
   - inspect the current log and only the rendered pages needed to assess named
     layout, figure, table, blank-page, or packaging concerns;
   - record commands, page count, warnings, blockers, and remaining work in one
     finish report.
4. In **submission-check** mode:
   - keep the package read-only and build in a temporary location;
   - check claim scope, displayed numbers, method details, citations, page
     limit, anonymity, references, figures, fonts, margins, required files, and
     supplements against their direct sources;
   - list blockers, warnings, and the smallest next action in one checklist;
   - end with `no blocker found`, `blockers found`, or `not assessable`. This is
     advice, not a promotion gate.
5. Stop when the selected mode is verified or one concrete external or user
   decision is required. Do not start a scientific review or another mode.

## Quality Bar

- Reports describe a fresh build or current named candidate, not old logs.
- Blockers and warnings are distinct and have exact locators.
- Claims and numbers remain within their named evidence and units.
- Visual claims are based on targeted inspection of the actual render.

## Boundaries

- Do not promote or replace a paper.
- Do not rewrite the scientific story merely to make compilation pass.
- Do not create claim ledgers, content identifiers, review states, acceptance
  handshakes, or a review-fix-review loop.
- Do not edit the package in submission-check mode.

## Open References Only As Needed

- Review `references/compile-gates.md` for build commands.
- Review `../../_shared/writing-constraint-layer.md` for claim-safe edits.
- Review `../../_shared/templates/submission-checklist-template.md` only in
  submission-check mode.
