# Agent Dispatch Rules

Use these rules when a workflow skill dispatches subagents or external review
agents.

## Default Boundary

- Subagents are read-only by default. They may inspect allowed inputs and return
  a verdict, critique, or recommendation, but they must not create, edit, move,
  delete, or overwrite files unless the parent skill explicitly grants a narrow
  write scope.
- The coordinating controller owns canonical artifact writes, machine-readable
  state updates, final scores, promotion decisions, and submission-readiness
  decisions.
- Subagent outputs are evidence for the controller, not canonical workflow
  artifacts by themselves.

## Prompt Requirements

Every subagent prompt should state:

- allowed inputs
- forbidden inputs that must not be read before forming the verdict
- whether the task is read-only
- the exact output schema or verdict labels
- the maximum number of must-fix or blocker items when bounded output matters

## Synthesis Rules

- Preserve disagreement. Do not average conflicting verdicts into a false
  consensus.
- Merge duplicate criticisms by root cause, while recording which agent raised
  each issue in the controller-owned log.
- If the controller adds a finding not present in subagent outputs, label it
  `controller_added`.
- Do not copy subagent prose, provider names, prompts, attribution, or internal
  routing details into paper-facing manuscript text.

## Dispatch Paths

- Codex controller: use built-in `spawn_agent` / `wait_agent`.
- Claude controller: use Claude's `Agent` tool.
- Do not use `CCB ask codex` as a Codex subtask route in this workflow; it has
  been observed to hang.
