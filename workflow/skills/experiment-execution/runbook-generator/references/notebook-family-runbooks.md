# Notebook-Family Runbooks

Use this reference when the experiment workspace follows a `family/code + family/outputs` pattern.

## Goals

- Keep a runbook concrete enough that `run-experiment` can execute it without reverse-engineering notebook cells.
- Preserve the distinction between staging reruns and paper-facing canonical outputs.
- Make promotion an explicit step rather than an implicit side effect of rerunning a notebook.

## Minimum Fields Per Run

- family identifier
- notebook or script path
- conda environment
- working directory
- execution engine (`papermill`, `nbconvert`, or script CLI)
- staging output directory
- canonical output directory
- expected exported files
- paper-facing evidence exports
- success and failure signals
- promotion decision rule

## Recommended Sections

1. Run Summary
2. Canonical Evidence Policy
3. Preflight Checks
4. Execution Order
5. Naming Rules
6. Per-Run Record
7. Promotion Checklist

## Current Workspace Fit

For `topics/llm-inconsistency/ideas/i002/workspace/experiments/`, each family README already defines:

- the family role
- the active notebook under `code/`
- the outputs directory that matters for paper-facing evidence

Use those README files and `workspace/results/RUN_REGISTRY.md` as the source of truth when filling the runbook.
