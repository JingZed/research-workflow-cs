# Engineering Patterns

Use only the patterns relevant to the current task.

## Resume State

- `notes/CURRENT.md` is the short resume card and normally stays within 10–15
  lines.
- `notes/project-state.md` records scientific state and major milestones.
- Do not update either file merely to record routine workflow activity.

## Optional Capabilities

`notes/capabilities.yaml` may describe optional infrastructure such as external
reviewers, remote execution, background monitoring, paper conversion, or TeX
build support. If the file is absent, inspect the environment directly and
state any limitation that changes the requested task.

Do not turn capability metadata into a prerequisite for work that can be
completed locally.

## Long-Running Experiments

Each launched run should have a stable run ID and a directory under
`experiments/runs/`. Record:

```text
command
working directory
config or parameters
start time
process, scheduler, or remote job identifier
status and last checked time
stdout and stderr
checkpoint and expected outputs
resume or recovery command
```

Monitoring may update run status and logs. It must not silently reinterpret
results or promote staged outputs.

## Task-Specific Validation

Choose checks from the failure modes of the task:

- experiment changes: configuration, command, smoke test, logs, outputs, and
  metric parity;
- result changes: input run set, aggregation logic, uncertainty, baselines,
  and claim scope;
- manuscript changes: compile, page count, references, fonts, warnings,
  figures, and rendered PDF;
- figure changes: source integrity, geometry, legibility, export, and placement;
- Skill changes: direct validation, registry rebuild, runtime-link validation,
  and catalog synchronization.

Unrelated files elsewhere in the workspace do not block a bounded task.

## Review Before Edit

A review, audit, scan, or critique is read-only by default:

1. inspect the named artifact;
2. report ranked findings with evidence;
3. propose the smallest fix package;
4. wait for the user’s decision;
5. apply only approved edits;
6. rerun affected checks.

## Promotion and Recovery

For canonical experiment or paper changes:

- compare exact source and target file sets;
- archive every overwritten file;
- avoid wildcard copying;
- record exact paths, sizes, modification times, and direct comparison results;
- rebuild or rerun the smallest relevant verification;
- keep a rollback command or file map.

An explicit replacement preflight may assess readiness. The user authorizes
the exact source, target, and file list in the current task.

## Safe File Operations

- Resolve paths before moving, replacing, or deleting.
- Prefer recoverable moves to permanent deletion.
- Preserve unrelated dirty-worktree changes.
- Never use a broad recursive target for cleanup.
- Do not modify a protected canonical artifact through an isolated candidate
  workflow.
