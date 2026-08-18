# Explicit Replacement Policy

Use this reference when notebook reruns stage outputs outside a family's
canonical `outputs/` bundle.

## Preconditions

- `status.json` says the run completed successfully.
- The staged directory exists and contains the exports expected by the runbook.
- The target family and canonical output directory are known.

## Preview Status

- `READY`: the exact path plan may be shown for current-task confirmation.
- `BLOCKED`: parity, completeness, or paper-role questions remain.
- `ARCHIVE_ONLY`: preserve the staged run but keep canonical outputs unchanged.

## Planning Rules

- Use exact root-relative file paths; reject globs, directories, absolute paths,
  parent traversal, duplicates, and symlinks.
- Record each source and destination path, existence state, byte size, and
  modification time, plus the deterministic source-to-destination map.
- Compare source and destination bytes directly where both exist. Any later
  path, existence, size, or modification-time change requires a fresh preview.
- State whether the run registry, parity notes, result summaries, plots, or
  paper claims would need refresh after an approved replacement.
- Do not archive or copy files in preview mode.

## Apply Boundary

The same `$promote-run-outputs` Skill may apply a `READY` plan only after the
user explicitly confirms its exact source, target, and file list in the current
task. Apply mode owns archives and `promotion-manifest.json`.
