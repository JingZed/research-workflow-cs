#!/usr/bin/env python3
"""Execute a notebook in a named conda environment and persist run state."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
from datetime import datetime, timezone


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a notebook via papermill or nbconvert inside a conda env."
    )
    parser.add_argument("--env", required=True, help="Conda environment name")
    parser.add_argument("--notebook", required=True, help="Path to input notebook")
    parser.add_argument("--outdir", required=True, help="Run directory for logs and state")
    parser.add_argument(
        "--cwd",
        help="Working directory for execution. Defaults to the notebook parent directory.",
    )
    parser.add_argument(
        "--engine",
        choices=("auto", "papermill", "nbconvert"),
        default="auto",
        help="Notebook execution engine",
    )
    parser.add_argument(
        "--staging-output-dir",
        help="Optional family-side staging output directory recorded in status.json",
    )
    parser.add_argument(
        "--param",
        action="append",
        default=[],
        help="Notebook parameter in name=value form. Repeat as needed.",
    )
    parser.add_argument(
        "--evidence-path",
        action="append",
        default=[],
        help="Relative file under --staging-output-dir or absolute path that counts as paper-facing evidence. Repeat as needed.",
    )
    return parser.parse_args()


def ensure_conda() -> str:
    conda = shutil.which("conda")
    if not conda:
        raise RuntimeError("conda executable not found in PATH")
    return conda


def parse_params(items: list[str]) -> dict[str, str]:
    params: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Invalid --param value: {item!r}. Expected name=value.")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Invalid --param key in: {item!r}")
        params[key] = value
    return params


def env_supports(conda: str, env_name: str, module: str) -> bool:
    cmd = [
        conda,
        "run",
        "-n",
        env_name,
        "python",
        "-c",
        f"import {module}",
    ]
    proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc.returncode == 0


def choose_engine(conda: str, env_name: str, requested: str, has_params: bool) -> str:
    if requested == "papermill":
        if not env_supports(conda, env_name, "papermill"):
            raise RuntimeError("papermill requested but unavailable in the conda environment")
        return "papermill"
    if requested == "nbconvert":
        if has_params:
            raise RuntimeError("nbconvert does not support --param; use papermill instead")
        if not env_supports(conda, env_name, "jupyter"):
            raise RuntimeError("nbconvert requested but jupyter is unavailable in the conda environment")
        return "nbconvert"

    if has_params and env_supports(conda, env_name, "papermill"):
        return "papermill"
    if env_supports(conda, env_name, "papermill"):
        return "papermill"
    if env_supports(conda, env_name, "jupyter"):
        return "nbconvert"
    raise RuntimeError("Neither papermill nor jupyter nbconvert is available in the conda environment")


def build_command(
    conda: str,
    env_name: str,
    engine: str,
    notebook: Path,
    executed_notebook: Path,
    params: dict[str, str],
) -> list[str]:
    prefix = [conda, "run", "-n", env_name, "python", "-m"]
    if engine == "papermill":
        cmd = prefix + ["papermill", str(notebook), str(executed_notebook)]
        for key, value in params.items():
            cmd.extend(["-p", key, value])
        return cmd

    cmd = prefix + [
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        str(notebook),
        "--output",
        executed_notebook.name,
        "--output-dir",
        str(executed_notebook.parent),
        "--ExecutePreprocessor.timeout=-1",
    ]
    return cmd


def write_status(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    conda = ensure_conda()

    notebook = Path(args.notebook).expanduser().resolve()
    if not notebook.exists():
        raise FileNotFoundError(f"Notebook not found: {notebook}")

    outdir = Path(args.outdir).expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    params = parse_params(args.param)
    cwd = Path(args.cwd).expanduser().resolve() if args.cwd else notebook.parent
    status_path = outdir / "status.json"
    stdout_path = outdir / "stdout.log"
    stderr_path = outdir / "stderr.log"
    executed_notebook = outdir / "executed.ipynb"
    run_id = outdir.name
    engine = choose_engine(conda, args.env, args.engine, bool(params))
    command = build_command(conda, args.env, engine, notebook, executed_notebook, params)
    evidence_paths = args.evidence_path

    status: dict[str, object] = {
        "run_id": run_id,
        "status": "running",
        "engine_requested": args.engine,
        "engine_used": engine,
        "env_name": args.env,
        "notebook_path": str(notebook),
        "working_directory": str(cwd),
        "staging_output_dir": args.staging_output_dir,
        "stdout_log": str(stdout_path),
        "stderr_log": str(stderr_path),
        "executed_notebook": str(executed_notebook),
        "parameters": params,
        "evidence_paths": evidence_paths,
        "command": shlex.join(command),
        "start_time": iso_now(),
        "end_time": None,
        "exit_code": None,
    }
    write_status(status_path, status)

    with stdout_path.open("w", encoding="utf-8") as stdout_handle, stderr_path.open(
        "w", encoding="utf-8"
    ) as stderr_handle:
        proc = subprocess.run(command, cwd=str(cwd), stdout=stdout_handle, stderr=stderr_handle)

    status["end_time"] = iso_now()
    status["exit_code"] = proc.returncode
    status["status"] = "completed" if proc.returncode == 0 else "failed"
    write_status(status_path, status)
    return proc.returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - best-effort failure persistence
        sys.stderr.write(f"{type(exc).__name__}: {exc}\n")
        raise
