# Notebook-First Execution

Use this reference when the runnable source of truth is a notebook rather than a stable CLI training script.

## Fit

- The experiment family keeps code under `code/` and exported artifacts under `outputs/`.
- The user normally runs notebooks through Cursor or Jupyter inside a conda environment.
- Paper-facing numbers are valid only after they are exported to files under a versioned output directory.

## Default Launch Pattern

1. Resolve the notebook path and conda environment name from the runbook or family README.
2. Create a fresh run directory under `experiments/runs/<run-id>/` for logs, machine state, and executed notebook snapshots.
3. Stage notebook-produced exports in a fresh family-side output directory first, such as:
   - `workspace/experiments/<family>/outputs/runs/<run-id>/`
   - or another explicitly versioned staging directory defined by the project
4. Execute with `papermill` first when parameterization or repeated reruns matter.
5. Fall back to `jupyter nbconvert --execute` when the notebook is not parameterized and `papermill` is unavailable.
6. Promote staged outputs into the family's canonical `outputs/` bundle only after parity checks or explicit user approval.

## Why Staging Matters

- Notebook reruns can silently overwrite files in `outputs/`.
- Paper-facing families may already be frozen or cited in the draft.
- A rerun often needs inspection before becoming the new canonical evidence.

## Execution Preferences

- Prefer `papermill` for repeatable reruns, parameter sweeps, and executed notebook capture.
- Prefer `nbconvert --execute` only for simple one-off notebook execution without parameters.
- Keep the notebook's working directory aligned with its family folder so relative data and output paths still resolve.

## Machine-Readable State

For notebook-first runs, write these files under `experiments/runs/<run-id>/`:

- `launch.md`
- `status.json`
- `stdout.log`
- `stderr.log`
- `executed.ipynb`

Recommended `status.json` fields:

- `run_id`
- `status`
- `engine_requested`
- `engine_used`
- `env_name`
- `notebook_path`
- `working_directory`
- `staging_output_dir`
- `evidence_paths`
- `stdout_log`
- `stderr_log`
- `executed_notebook`
- `start_time`
- `end_time`
- `exit_code`

## Current Workspace Pattern

In the `i002` workspace, these rules already exist and should be respected:

- `workspace/experiments/` is the run layer.
- family `outputs/` directories hold exported artifacts that can become paper-facing evidence.
- `workspace/results/RUN_REGISTRY.md` defines which output directories are canonical.
- values that exist only inside notebook cells are not canonical until exported to versioned files.
