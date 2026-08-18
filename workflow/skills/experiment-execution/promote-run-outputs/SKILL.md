---
name: promote-run-outputs
description: "Preview or apply replacement of named canonical experiment outputs when the user asks to consider or perform that replacement. A clear natural-language promotion request may trigger this Skill; never initiate promotion merely because a run completed. Preview is read-only, while apply requires current-task confirmation of the exact plan."
---

# Promote Run Outputs

## Overview

Own the complete explicit replacement operation in two modes. `preview` is
read-only and is the default whenever the user asks to inspect or consider a
replacement. `apply` performs the confirmed transaction. Do not split these
modes into separate Skills or add an independent acceptance step.

The user does not need to name this Skill when the requested replacement is
clear. Never infer promotion intent from run completion or result quality alone.

## Consume

- In `preview` mode: `experiments/runs/<run-id>/status.json`, logs, config,
  staged outputs, the runbook or launch record, current canonical outputs, and
  explicit user intent to consider replacement.
- In `apply` mode: `experiments/runs/<run-id>/promotion.md` with `READY`, its
  matching `promotion-plan.json`, and explicit current-task confirmation of the
  displayed source, target, and exact relative file list.

## Produce

- `experiments/runs/<run-id>/promotion.md` in `preview` mode.
- `experiments/runs/<run-id>/promotion-plan.json` only for a `READY` preview.
- `experiments/runs/<run-id>/promotion-manifest.json`, approved canonical
  files, and rollback copies under the plan's archive directory in apply mode.

## Workflow

1. Select the mode from the user's request. If current-task confirmation of an
   already displayed exact plan is absent, use `preview` and do not mutate.
2. In `preview`, confirm the run completed and resolve the staging directory,
   canonical directory, and intended exports as exact relative file paths.
3. Compare staged and canonical files and affected metrics directly. Record
   each path, existence state, byte size, modification time, and whether the
   current contents match. Do not derive file-content identifiers.
4. Set `READY`, `BLOCKED`, or `ARCHIVE_ONLY`. `READY` means the differences are
   understood and the exact plan may be shown for confirmation; `BLOCKED`
   names the smallest missing, unexplained, or ambiguous item;
   `ARCHIVE_ONLY` preserves the run without replacement.
5. For `READY`, create the exact-file plan:

```bash
python workflow/skills/experiment-execution/promote-run-outputs/scripts/promote_run_outputs.py plan \
  --run-dir experiments/runs/<run-id> \
  --staging-dir <staged-output-dir> \
  --canonical-dir <canonical-output-dir> \
  --include <exact-relative-file>
```

6. Write `promotion.md`, display the source, target, exact relative files,
   direct differences, planned archive, and downstream evidence affected, then
   stop. Do not apply during the preview pass.
7. In `apply`, re-read the preview and plan. Confirm they identify the same run,
   source, target, relative files, and recorded file metadata, and that the user
   approved that exact list in the current task.
8. Run the apply command with a short reference to that approval:

```bash
python workflow/skills/experiment-execution/promote-run-outputs/scripts/promote_run_outputs.py apply \
  --plan experiments/runs/<run-id>/promotion-plan.json \
  --approval-note "<short current-task approval reference>"
```

9. Let the script recheck every path, existence state, size, and modification
   time. Stop before mutation if anything changed.
10. Inspect `promotion-manifest.json`. Verify `status: promoted`, direct source
   and destination matches, archived copies for overwritten files, and rollback
   instructions.
11. Re-run only the downstream aggregation, plots, or paper checks affected by
   the promoted files.

## Quality Bar

- Accept only exact relative file paths. Reject globs, absolute paths, `..`,
  directories, duplicates, and symlinks.
- A preview must expose the complete copy scope and must not mutate files.
- Preserve every overwritten byte in the archive before replacing a target.
- Treat source drift, destination drift, or a symlinked path as requiring a
  fresh plan and current user confirmation.
- Roll back every changed destination if any copy or replace step fails.

## Boundaries

- Do not infer a file list from a directory.
- Do not change the plan after approval.
- Do not reinterpret results or choose among unresolved scientific values;
  route those questions to `$result-aggregator`.
- Do not update result summaries, plots, or manuscripts in the same action.
- Do not create a separate gate, reviewer vote, finding ledger, or approval
  chain around this two-mode operation.

## Script

Use `scripts/promote_run_outputs.py plan` in `preview` mode and its `apply`
subcommand only after current-task approval of the unchanged exact plan.

## Open References Only As Needed

- Review `references/promotion-policy.md` for family-specific conventions.
