#!/usr/bin/env python3
"""Classify experiment runs from status.json and recent log activity."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import re
import tempfile


def iso_now(now: datetime | None = None) -> str:
    current = now or datetime.now(timezone.utc)
    return current.astimezone(timezone.utc).replace(microsecond=0).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Watch experiment runs and classify their state.")
    parser.add_argument("--runs-dir", required=True, help="Directory containing run-id subdirectories")
    parser.add_argument("--report-path", required=True, help="Markdown report output path")
    parser.add_argument("--state-path", required=True, help="JSON state output path")
    parser.add_argument(
        "--idea-root",
        help="Optional active idea root used to resolve watchdog capability flags",
    )
    parser.add_argument(
        "--stall-hours",
        type=float,
        default=6.0,
        help="Mark running jobs as stalled if no log activity occurs within this many hours",
    )
    parser.add_argument(
        "--now",
        help="Optional ISO-8601 UTC time for reproducible checks and tests",
    )
    parser.add_argument(
        "--write-unchanged",
        action="store_true",
        help="Rewrite report and state even when the material snapshot is unchanged",
    )
    return parser.parse_args()


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp must include a timezone: {value!r}")
    return parsed.astimezone(timezone.utc)


def last_activity(run_dir: Path, status: dict[str, object]) -> datetime | None:
    candidates: list[datetime] = []
    for key in ("stdout_log", "stderr_log", "executed_notebook"):
        path_value = status.get(key)
        if isinstance(path_value, str):
            path = Path(path_value)
            if not path.is_absolute():
                path = run_dir / path
            if path.exists():
                candidates.append(datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc))
    started = parse_time(status.get("start_time")) if isinstance(status.get("start_time"), str) else None
    if started:
        candidates.append(started)
    return max(candidates) if candidates else None


def classify(
    run_dir: Path,
    stall_delta: timedelta,
    now: datetime | None = None,
) -> dict[str, object]:
    status_path = run_dir / "status.json"
    if not status_path.exists():
        return {"run_id": run_dir.name, "classification": "unknown", "reason": "missing status.json"}

    status = json.loads(status_path.read_text(encoding="utf-8"))
    if not isinstance(status, dict):
        raise ValueError(f"{status_path} must contain a JSON object")
    raw_status = status.get("status")
    activity = last_activity(run_dir, status)
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    classification = "unknown"
    reason = ""

    if raw_status == "completed":
        classification = "completed"
        reason = "status.json marks run as completed"
    elif raw_status == "failed":
        classification = "failed"
        reason = "status.json marks run as failed"
    elif raw_status == "running":
        if activity and current - activity > stall_delta:
            classification = "stalled"
            reason = f"no log activity for more than {stall_delta.total_seconds() / 3600:.1f} hours"
        else:
            classification = "running"
            reason = "run is active with recent log activity"
    else:
        classification = "unknown"
        reason = f"unrecognized status {raw_status!r}"

    return {
        "run_id": run_dir.name,
        "classification": classification,
        "reason": reason,
        "status_path": str(status_path),
        "last_activity": activity.replace(microsecond=0).isoformat() if activity else None,
        "raw_status": raw_status,
    }


def render_report(items: list[dict[str, object]], generated_at: str) -> str:
    grouped: dict[str, list[dict[str, object]]] = {}
    for item in items:
        grouped.setdefault(str(item["classification"]), []).append(item)

    lines = ["# Watchdog Report", "", f"- Generated at: `{generated_at}`", ""]
    for status in ("stalled", "failed", "running", "completed", "unknown"):
        runs = grouped.get(status, [])
        lines.append(f"## {status.title()}")
        if not runs:
            lines.append("- None")
        else:
            for run in runs:
                lines.append(
                    f"- `{run['run_id']}`: {run['reason']}"
                    + (f" (last activity: `{run['last_activity']}`)" if run.get("last_activity") else "")
                )
        lines.append("")
    return "\n".join(lines)


def render_disabled_report(generated_at: str, reason: str) -> str:
    return "\n".join(
        [
            "# Watchdog Report",
            "",
            f"- Generated at: `{generated_at}`",
            "- Status: `disabled`",
            f"- Reason: {reason}",
            "",
        ]
    )


def load_watchdog_capability(idea_root: Path, runs_dir: Path) -> dict[str, object]:
    """Resolve only the watchdog flag without depending on retired workflow code."""
    config_path = idea_root / "notes" / "capabilities.yaml"
    configured = "off"
    if config_path.exists():
        version: str | None = None
        in_capabilities = False
        watchdog_seen = False
        for lineno, raw_line in enumerate(
            config_path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            line = raw_line.split("#", 1)[0].rstrip()
            if not line.strip():
                continue
            if not in_capabilities:
                if line.startswith("version:"):
                    version = line.split(":", 1)[1].strip()
                    if version != "1":
                        raise ValueError(
                            f"{config_path}:{lineno}: unsupported version {version!r}"
                        )
                    continue
                if line.strip() == "capabilities:":
                    in_capabilities = True
                    continue
                raise ValueError(
                    f"{config_path}:{lineno}: expected `version:` or `capabilities:`"
                )
            if not raw_line.startswith("  "):
                raise ValueError(
                    f"{config_path}:{lineno}: capability entries need two-space indentation"
                )
            inner = raw_line[2:].split("#", 1)[0].rstrip()
            match = re.fullmatch(r"([a-z_]+):\s*(off|on|auto)", inner)
            if not match:
                raise ValueError(
                    f"{config_path}:{lineno}: expected `<capability>: off|on|auto`"
                )
            key, value = match.groups()
            if key == "watchdog":
                configured = value
                watchdog_seen = True
        if version is None or not in_capabilities:
            raise ValueError(f"{config_path}: missing version or capabilities block")
        if not watchdog_seen:
            raise ValueError(f"{config_path}: missing capability key 'watchdog'")

    available = runs_dir.exists()
    if configured == "off":
        enabled = False
        reason = "capability is set to off"
    elif configured == "on":
        enabled = available
        reason = (
            "watchdog is enabled"
            if available
            else "capability is forced on but experiments/runs does not exist"
        )
    else:
        enabled = available
        reason = (
            "watchdog auto-enabled because experiments/runs exists"
            if available
            else "watchdog auto-disabled because experiments/runs does not exist"
        )
    return {
        "configured": configured,
        "enabled": enabled,
        "available": available,
        "reason": reason,
        "config_path": str(config_path),
    }


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    )
    temp_path = Path(handle.name)
    try:
        with handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def material_snapshot(payload: dict[str, object]) -> dict[str, object]:
    """Remove timestamps and log activity that do not change run classification."""
    capability = payload.get("capability")
    capability_snapshot: dict[str, object] | None = None
    if isinstance(capability, dict):
        capability_snapshot = {
            key: capability.get(key)
            for key in ("configured", "enabled", "available", "reason")
        }

    run_snapshots: list[dict[str, object]] = []
    runs = payload.get("runs")
    if isinstance(runs, list):
        for run in runs:
            if isinstance(run, dict):
                run_snapshots.append(
                    {
                        key: run.get(key)
                        for key in (
                            "run_id",
                            "classification",
                            "raw_status",
                            "reason",
                        )
                    }
                )

    return {
        "status": payload.get("status"),
        "capability": capability_snapshot,
        "stall_hours": payload.get("stall_hours"),
        "runs": run_snapshots,
    }


def should_write_snapshot(
    state_path: Path,
    report_path: Path,
    payload: dict[str, object],
    write_unchanged: bool,
) -> bool:
    if write_unchanged or not state_path.exists() or not report_path.exists():
        return True
    try:
        previous = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return True
    if not isinstance(previous, dict):
        return True
    return material_snapshot(previous) != material_snapshot(payload)


def main() -> int:
    args = parse_args()
    runs_dir = Path(args.runs_dir).expanduser().resolve()
    report_path = Path(args.report_path).expanduser().resolve()
    state_path = Path(args.state_path).expanduser().resolve()
    if args.stall_hours <= 0:
        raise ValueError("--stall-hours must be positive")
    stall_delta = timedelta(hours=args.stall_hours)
    now = parse_time(args.now) if args.now else datetime.now(timezone.utc)
    assert now is not None
    generated_at = iso_now(now)
    capability_state: dict[str, object] | None = None

    if args.idea_root:
        idea_root = Path(args.idea_root).expanduser().resolve()
        capability_state = load_watchdog_capability(idea_root, runs_dir)
        if not capability_state["enabled"]:
            state_payload: dict[str, object] = {
                "generated_at": generated_at,
                "status": "disabled",
                "capability": capability_state,
                "stall_hours": args.stall_hours,
                "runs": [],
            }
            if not should_write_snapshot(
                state_path,
                report_path,
                state_payload,
                args.write_unchanged,
            ):
                return 0
            report_text = (
                render_disabled_report(generated_at, str(capability_state["reason"]))
                + "\n"
            )
            state_text = json.dumps(state_payload, indent=2) + "\n"
            atomic_write_text(report_path, report_text)
            atomic_write_text(state_path, state_text)
            return 0

    runs: list[dict[str, object]] = []
    if runs_dir.exists():
        for child in sorted(runs_dir.iterdir()):
            if child.is_dir():
                runs.append(classify(child, stall_delta, now))

    state_payload = {
        "generated_at": generated_at,
        "status": "active",
        "capability": capability_state,
        "stall_hours": args.stall_hours,
        "runs": runs,
    }
    if not should_write_snapshot(
        state_path,
        report_path,
        state_payload,
        args.write_unchanged,
    ):
        return 0
    report_text = render_report(runs, generated_at) + "\n"
    state_text = json.dumps(state_payload, indent=2) + "\n"
    atomic_write_text(report_path, report_text)
    atomic_write_text(state_path, state_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
