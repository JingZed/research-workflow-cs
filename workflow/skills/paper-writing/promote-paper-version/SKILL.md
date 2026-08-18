---
name: promote-paper-version
description: "Preview or apply replacement of a named canonical paper when the user asks to consider or perform that replacement from one exact versioned candidate. A clear natural-language promotion request may trigger this Skill; never initiate promotion merely because a candidate is ready. Preview is read-only, while apply requires current-task confirmation of the exact plan."
---

# Promote Paper Version

## Overview

Own the complete canonical paper replacement in two modes. `preview` is
read-only and is the default when the user asks to inspect or consider a
replacement. `apply` is an L4 action: project-local rules may forbid it, and
the exact candidate, target, and file list require current-task confirmation.
Do not split these modes into a separate gate Skill.

The user does not need to name this Skill when the requested replacement is
clear. Never infer promotion intent from candidate readiness or build success.

## Consume

- In `preview` mode: the exact named candidate and canonical paper directories,
  source entry point, rendered PDF, figures, bibliography, build log,
  project-local replacement rules, and directly relevant invariants/evidence.
- In `apply` mode: `notes/promotion-plan.md` and
  `notes/promotion-plan.json` with current `READY` status, plus explicit
  current-task confirmation of the displayed source, target, relative file
  list, exclusions, and archive location.

## Produce

- `notes/promotion-plan.md` in `preview` mode.
- `notes/promotion-plan.json` only for a `READY` preview.
- `<canonical-paper-dir>/promotion-manifest.json`, the named canonical paper
  directory, and a timestamped archive of the previous package in apply mode.

## Workflow

1. Select the mode from the user's request. Without current-task confirmation
   of an already displayed exact plan, use `preview` and do not mutate.
2. In `preview`, confirm the user explicitly requested canonical replacement
   and local rules permit it. Resolve candidate and target roots exactly.
3. Build a source-only inventory using exact relative paths. Record existence,
   byte size, and modification time; reject globs, parent traversal,
   duplicates, undeclared files, and escaping symlinks.
4. Build and inspect the candidate. Check references, figures, page count,
   fonts, warnings, rendered output, anonymity, and required package files.
5. Check only the scientific facts affected by replacement against their named
   evidence. Route unresolved numeric conflicts to `$result-aggregator`.
6. Compare candidate and canonical files directly where useful. Record exact
   additions, replacements, exclusions, and planned archive location.
7. Set `READY` or `BLOCKED`, write the plan, present the exact roots and file
   list, and stop. Do not execute replacement in the preview pass.
8. In `apply`, abort unless the plan, current user confirmation, and project-local rules all
   name the same candidate, target, exact relative files, exclusions, and
   archive location.
9. Recheck every planned path, existence state, byte size, and modification
   time. Reject globs, parent traversal, duplicates, unexpected files, and
   escaping symlinks. Any change requires a fresh plan and confirmation.
10. Materialize the exact source-only copy plan in a temporary sibling
   directory. Compare each staged copy directly with its source.
11. Build and inspect the staged replacement before touching canonical state.
   Verify references, figures, page count, fonts, warnings, and rendered output.
12. Move the current canonical package to the confirmed timestamped archive. Do
   not delete it.
13. Move the already verified staged directory into the canonical location.
14. Compare every promoted source file directly with its canonical destination
   and rerun the focused package checks. Restore the archive if replacement or
   verification fails.
15. Write `promotion-manifest.json` with approval note, source, target, archive,
   exact file inventory, recorded and final sizes and modification times,
   direct-comparison results, commands, failure state, and rollback
   instructions.
16. Refresh project resume state only if the replacement changes a major
   milestone.

## Quality Bar

- The previous canonical package is recoverable.
- Preview mode is read-only and exposes every copied file and exclusion.
- Every promoted file directly matches the confirmed candidate.
- The manifest records the actual filesystem state and rollback path.

## Boundaries

- Do not apply without `READY` and current explicit confirmation.
- Do not accept a plan after source, target, inventory, or file-metadata change.
- Do not delete the archive or copy undeclared build outputs.
- Do not reinterpret scientific claims during the filesystem transaction.
- Do not create an independent reviewer vote, finding ledger, acceptance chain,
  or separate promotion gate.

## Open References Only As Needed

- Review `../../_shared/artifact-contract.md` for canonical path rules.
