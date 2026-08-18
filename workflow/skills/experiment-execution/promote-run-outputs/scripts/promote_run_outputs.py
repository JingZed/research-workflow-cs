#!/usr/bin/env python3
"""Plan and apply exact experiment-output replacements without content IDs."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import filecmp
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tempfile
from typing import Any


PLAN_VERSION = 2
MANIFEST_VERSION = 2
GLOB_CHARS = frozenset("*?[]{}")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def absolute_path(raw: str) -> Path:
    return Path(os.path.abspath(os.path.expanduser(raw)))


def exact_relative_path(raw: str) -> PurePosixPath:
    if not raw or any(char in raw for char in GLOB_CHARS):
        raise ValueError(f"include must be an exact relative file path: {raw!r}")
    if raw.startswith(("/", "\\")):
        raise ValueError(f"absolute include is forbidden: {raw!r}")
    if "\\" in raw:
        raise ValueError(f"use POSIX separators in include paths: {raw!r}")
    raw_parts = raw.split("/")
    if any(part in {"", ".", ".."} for part in raw_parts):
        raise ValueError(
            f"include may not contain empty, dot, or parent segments: {raw!r}"
        )
    candidate = PurePosixPath(raw)
    if candidate.is_absolute():
        raise ValueError(f"absolute include is forbidden: {raw!r}")
    return candidate


def reject_symlink_root(path: Path, label: str) -> None:
    if path.is_symlink():
        raise ValueError(f"{label} may not be a symlink: {path}")


def reject_symlink_components(root: Path, relative: PurePosixPath) -> None:
    current = root
    reject_symlink_root(current, "root")
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"symlinked replacement path is forbidden: {current}")


def file_state(path: Path) -> dict[str, Any]:
    if path.is_symlink():
        raise ValueError(f"symlinked file is forbidden: {path}")
    if not path.exists():
        return {"exists": False, "size": None, "mtime_ns": None}
    if not path.is_file():
        raise ValueError(f"path is not a regular file: {path}")
    stat = path.stat()
    return {
        "exists": True,
        "size": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
    }


def normalized_state(raw: Any, label: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError(f"{label} state must be an object")
    if set(raw) != {"exists", "size", "mtime_ns"}:
        raise ValueError(f"{label} state has unexpected fields")
    exists = raw["exists"]
    if not isinstance(exists, bool):
        raise ValueError(f"{label} existence flag must be boolean")
    size = raw["size"]
    mtime_ns = raw["mtime_ns"]
    if exists:
        if not isinstance(size, int) or size < 0:
            raise ValueError(f"{label} size must be a nonnegative integer")
        if not isinstance(mtime_ns, int) or mtime_ns < 0:
            raise ValueError(f"{label} modification time must be nonnegative")
    elif size is not None or mtime_ns is not None:
        raise ValueError(f"{label} absent state must use null metadata")
    return {"exists": exists, "size": size, "mtime_ns": mtime_ns}


def require_state(path: Path, expected: Any, label: str) -> dict[str, Any]:
    recorded = normalized_state(expected, label)
    actual = file_state(path)
    if actual != recorded:
        raise ValueError(
            f"{label} changed since planning: expected {recorded}, found {actual}"
        )
    return actual


def direct_match(first: Path, second: Path) -> bool:
    if not first.is_file() or not second.is_file():
        return False
    return filecmp.cmp(first, second, shallow=False)


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
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
            json.dump(payload, handle, ensure_ascii=True, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def planned_archive_dir(
    canonical_dir: Path,
    run_id: str,
    created_at: str,
) -> Path:
    timestamp = created_at.replace(":", "").replace("+00:00", "Z")
    return (
        canonical_dir.parent
        / "archive_promotions"
        / canonical_dir.name
        / f"{timestamp}-{run_id}"
    )


def build_plan(
    *,
    run_dir: Path,
    staging_dir: Path,
    canonical_dir: Path,
    includes: list[str],
    created_at: str | None = None,
) -> dict[str, Any]:
    reject_symlink_root(run_dir, "run directory")
    reject_symlink_root(staging_dir, "staging directory")
    reject_symlink_root(canonical_dir, "canonical directory")
    if not run_dir.is_dir():
        raise FileNotFoundError(f"run directory not found: {run_dir}")
    if not staging_dir.is_dir():
        raise FileNotFoundError(f"staging directory not found: {staging_dir}")
    if canonical_dir.exists() and not canonical_dir.is_dir():
        raise ValueError(f"canonical path is not a directory: {canonical_dir}")
    if not includes:
        raise ValueError("at least one --include path is required")

    relative_paths = [exact_relative_path(item) for item in includes]
    normalized = [item.as_posix() for item in relative_paths]
    if len(set(normalized)) != len(normalized):
        raise ValueError("duplicate include paths are forbidden")

    timestamp = created_at or utc_now()
    archive_dir = planned_archive_dir(canonical_dir, run_dir.name, timestamp)
    files: list[dict[str, Any]] = []
    for relative in sorted(relative_paths, key=lambda item: item.as_posix()):
        reject_symlink_components(staging_dir, relative)
        reject_symlink_components(canonical_dir, relative)
        source = staging_dir.joinpath(*relative.parts)
        destination = canonical_dir.joinpath(*relative.parts)
        source_state = file_state(source)
        if not source_state["exists"]:
            raise FileNotFoundError(f"staged file not found: {source}")
        destination_state = file_state(destination)
        files.append(
            {
                "relative_path": relative.as_posix(),
                "source": str(source),
                "destination": str(destination),
                "archive": str(archive_dir.joinpath(*relative.parts)),
                "source_state": source_state,
                "destination_state": destination_state,
                "source_matches_destination": (
                    direct_match(source, destination)
                    if destination_state["exists"]
                    else None
                ),
            }
        )

    return {
        "version": PLAN_VERSION,
        "kind": "run-output-replacement-plan",
        "status": "awaiting-user-confirmation",
        "created_at": timestamp,
        "run_id": run_dir.name,
        "run_dir": str(run_dir),
        "staging_dir": str(staging_dir),
        "canonical_dir": str(canonical_dir),
        "archive_dir": str(archive_dir),
        "files": files,
    }


def load_plan(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("replacement plan must contain a JSON object")
    if payload.get("version") != PLAN_VERSION:
        raise ValueError(
            f"unsupported replacement plan version: {payload.get('version')!r}"
        )
    if payload.get("kind") != "run-output-replacement-plan":
        raise ValueError("not a run-output replacement plan")
    if payload.get("status") != "awaiting-user-confirmation":
        raise ValueError("replacement plan is not awaiting user confirmation")
    return payload


def verify_plan_files(plan: dict[str, Any]) -> list[dict[str, Any]]:
    run_dir = absolute_path(str(plan["run_dir"]))
    staging_dir = absolute_path(str(plan["staging_dir"]))
    canonical_dir = absolute_path(str(plan["canonical_dir"]))
    archive_dir = absolute_path(str(plan["archive_dir"]))
    reject_symlink_root(run_dir, "run directory")
    reject_symlink_root(staging_dir, "staging directory")
    reject_symlink_root(canonical_dir, "canonical directory")
    reject_symlink_root(archive_dir, "archive directory")
    if not run_dir.is_dir():
        raise FileNotFoundError(f"run directory not found: {run_dir}")
    if not staging_dir.is_dir():
        raise FileNotFoundError(f"staging directory not found: {staging_dir}")
    if canonical_dir.exists() and not canonical_dir.is_dir():
        raise ValueError(f"canonical path is not a directory: {canonical_dir}")

    run_id = str(plan.get("run_id", ""))
    created_at = str(plan.get("created_at", ""))
    if run_id != run_dir.name:
        raise ValueError("planned run ID does not match the run directory")
    expected_archive_dir = planned_archive_dir(canonical_dir, run_id, created_at)
    if archive_dir != expected_archive_dir:
        raise ValueError("planned archive directory does not match plan roots")

    raw_files = plan.get("files")
    if not isinstance(raw_files, list) or not raw_files:
        raise ValueError("replacement plan has no files")
    verified: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw_entry in raw_files:
        if not isinstance(raw_entry, dict):
            raise ValueError("replacement plan file entry must be an object")
        relative = exact_relative_path(str(raw_entry.get("relative_path", "")))
        rel_text = relative.as_posix()
        if rel_text in seen:
            raise ValueError(f"duplicate planned path: {rel_text}")
        seen.add(rel_text)
        reject_symlink_components(staging_dir, relative)
        reject_symlink_components(canonical_dir, relative)
        reject_symlink_components(archive_dir, relative)

        source = staging_dir.joinpath(*relative.parts)
        destination = canonical_dir.joinpath(*relative.parts)
        archive = archive_dir.joinpath(*relative.parts)
        if absolute_path(str(raw_entry.get("source", ""))) != source:
            raise ValueError(f"planned source does not match roots for {rel_text}")
        if absolute_path(str(raw_entry.get("destination", ""))) != destination:
            raise ValueError(
                f"planned destination does not match roots for {rel_text}"
            )
        if absolute_path(str(raw_entry.get("archive", ""))) != archive:
            raise ValueError(f"planned archive does not match roots for {rel_text}")

        source_state = require_state(
            source, raw_entry.get("source_state"), f"source {rel_text}"
        )
        destination_state = require_state(
            destination,
            raw_entry.get("destination_state"),
            f"destination {rel_text}",
        )
        recorded_relation = raw_entry.get("source_matches_destination")
        if destination_state["exists"]:
            if not isinstance(recorded_relation, bool):
                raise ValueError(
                    f"planned direct-comparison result is invalid for {rel_text}"
                )
            if direct_match(source, destination) != recorded_relation:
                raise ValueError(
                    f"source/destination relationship changed for {rel_text}"
                )
        elif recorded_relation is not None:
            raise ValueError(
                f"absent destination must have null comparison for {rel_text}"
            )

        verified.append(
            {
                **raw_entry,
                "_relative": relative,
                "_source": source,
                "_destination": destination,
                "_archive": archive,
                "_source_state": source_state,
                "_destination_state": destination_state,
            }
        )
    return verified


def copy_and_compare(source: Path, destination: Path) -> dict[str, Any]:
    before = file_state(source)
    if not before["exists"]:
        raise FileNotFoundError(f"copy source missing: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    if not direct_match(source, destination):
        raise OSError(f"direct comparison failed after copy: {source} -> {destination}")
    after = file_state(source)
    if after != before:
        raise OSError(f"copy source changed during copy: {source}")
    return file_state(destination)


def apply_plan(
    plan: dict[str, Any],
    *,
    approval_note: str,
    applied_at: str | None = None,
) -> dict[str, Any]:
    if not approval_note.strip():
        raise ValueError("approval note must identify the current-task confirmation")
    files = verify_plan_files(plan)
    run_dir = absolute_path(str(plan["run_dir"]))
    canonical_dir = absolute_path(str(plan["canonical_dir"]))
    archive_dir = absolute_path(str(plan["archive_dir"]))
    if archive_dir.exists():
        raise FileExistsError(
            f"planned archive already exists; create a fresh plan: {archive_dir}"
        )

    canonical_dir.parent.mkdir(parents=True, exist_ok=True)
    transaction_dir = Path(
        tempfile.mkdtemp(
            prefix=f".replacement-{plan['run_id']}-",
            dir=canonical_dir.parent,
        )
    )
    prepared_dir = transaction_dir / "prepared"
    changed: list[dict[str, Any]] = []
    result_files: list[dict[str, Any]] = []
    rollback_errors: list[str] = []
    status = "failed"
    failure: str | None = None

    try:
        for entry in files:
            relative = entry["_relative"]
            source = entry["_source"]
            destination = entry["_destination"]
            prepared = prepared_dir.joinpath(*relative.parts)
            require_state(source, entry["_source_state"], f"source {relative}")
            prepared_state = copy_and_compare(source, prepared)
            require_state(source, entry["_source_state"], f"source {relative}")
            entry["_prepared_state"] = prepared_state

            if entry["_destination_state"]["exists"]:
                require_state(
                    destination,
                    entry["_destination_state"],
                    f"destination {relative}",
                )
                archive_state = copy_and_compare(destination, entry["_archive"])
                require_state(
                    destination,
                    entry["_destination_state"],
                    f"destination {relative}",
                )
                entry["_archive_state"] = archive_state
            else:
                entry["_archive_state"] = None

        for entry in files:
            relative = entry["_relative"]
            source = entry["_source"]
            destination = entry["_destination"]
            prepared = prepared_dir.joinpath(*relative.parts)
            require_state(source, entry["_source_state"], f"source {relative}")
            require_state(
                destination,
                entry["_destination_state"],
                f"destination {relative}",
            )
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(prepared, destination)
            changed.append(entry)
            require_state(source, entry["_source_state"], f"source {relative}")
            if not direct_match(source, destination):
                raise OSError(
                    f"canonical destination differs from source: {relative.as_posix()}"
                )
            if entry["_archive_state"] is not None:
                require_state(
                    entry["_archive"],
                    entry["_archive_state"],
                    f"archive {relative}",
                )
            result_files.append(
                {
                    "relative_path": relative.as_posix(),
                    "source": str(source),
                    "destination": str(destination),
                    "archive": (
                        str(entry["_archive"])
                        if entry["_archive_state"] is not None
                        else None
                    ),
                    "source_state": entry["_source_state"],
                    "previous_destination_state": entry["_destination_state"],
                    "archive_state": entry["_archive_state"],
                    "final_destination_state": file_state(destination),
                    "source_matches_destination": True,
                    "archive_matches_previous_destination": (
                        True if entry["_archive_state"] is not None else None
                    ),
                }
            )
        status = "promoted"
    except Exception as exc:
        failure = f"{type(exc).__name__}: {exc}"
        for entry in reversed(changed):
            destination = entry["_destination"]
            relative = entry["_relative"]
            try:
                if destination.is_symlink():
                    raise OSError(f"refusing rollback through symlink: {destination}")
                if not entry["_destination_state"]["exists"]:
                    destination.unlink(missing_ok=True)
                    if destination.exists():
                        raise OSError(f"rollback could not remove: {destination}")
                else:
                    archive = entry["_archive"]
                    require_state(
                        archive,
                        entry["_archive_state"],
                        f"archive {relative}",
                    )
                    restore_temp = transaction_dir / "rollback" / relative
                    copy_and_compare(archive, restore_temp)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(restore_temp, destination)
                    require_state(
                        destination,
                        entry["_destination_state"],
                        f"restored destination {relative}",
                    )
                    if not direct_match(archive, destination):
                        raise OSError(
                            f"restored destination differs from archive: {destination}"
                        )
            except Exception as rollback_exc:
                rollback_errors.append(
                    f"{relative.as_posix()}: "
                    f"{type(rollback_exc).__name__}: {rollback_exc}"
                )
    finally:
        shutil.rmtree(transaction_dir, ignore_errors=True)

    if status != "promoted":
        result_files = []
        for entry in files:
            destination = entry["_destination"]
            archive = entry["_archive"]
            old_existed = entry["_destination_state"]["exists"]
            destination_state = file_state(destination)
            archive_state = file_state(archive)
            restored = (
                direct_match(archive, destination)
                and destination_state == entry["_destination_state"]
                if old_existed and archive_state["exists"]
                else not old_existed and not destination_state["exists"]
            )
            result_files.append(
                {
                    "relative_path": entry["_relative"].as_posix(),
                    "source": str(entry["_source"]),
                    "destination": str(destination),
                    "archive": str(archive) if archive_state["exists"] else None,
                    "source_state": entry["_source_state"],
                    "previous_destination_state": entry["_destination_state"],
                    "current_destination_state": destination_state,
                    "archive_state": archive_state,
                    "restored": restored,
                }
            )

    return {
        "version": MANIFEST_VERSION,
        "kind": "run-output-replacement-manifest",
        "status": status if not rollback_errors else "rollback-failed",
        "run_id": plan["run_id"],
        "plan_created_at": plan["created_at"],
        "approval_note": approval_note,
        "applied_at": applied_at or utc_now(),
        "canonical_dir": plan["canonical_dir"],
        "archive_dir": plan["archive_dir"],
        "files": result_files,
        "failure": failure,
        "rollback_errors": rollback_errors,
        "rollback": (
            "Restore each archived file to its named destination and remove each "
            "new destination whose previous_destination_state.exists is false."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plan or apply an exact run-output replacement."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser(
        "plan", help="Create a read-only replacement plan"
    )
    plan_parser.add_argument("--run-dir", required=True)
    plan_parser.add_argument("--staging-dir", required=True)
    plan_parser.add_argument("--canonical-dir", required=True)
    plan_parser.add_argument("--include", action="append", required=True)
    plan_parser.add_argument("--plan-path")

    apply_parser = subparsers.add_parser(
        "apply", help="Apply a user-confirmed replacement plan"
    )
    apply_parser.add_argument("--plan", required=True)
    apply_parser.add_argument("--approval-note", required=True)
    apply_parser.add_argument("--manifest-path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "plan":
        run_dir = absolute_path(args.run_dir)
        plan_path = (
            absolute_path(args.plan_path)
            if args.plan_path
            else run_dir / "promotion-plan.json"
        )
        plan = build_plan(
            run_dir=run_dir,
            staging_dir=absolute_path(args.staging_dir),
            canonical_dir=absolute_path(args.canonical_dir),
            includes=args.include,
        )
        atomic_write_json(plan_path, plan)
        print(plan_path)
        return 0

    plan_path = absolute_path(args.plan)
    plan = load_plan(plan_path)
    run_dir = absolute_path(str(plan["run_dir"]))
    manifest_path = (
        absolute_path(args.manifest_path)
        if args.manifest_path
        else run_dir / "promotion-manifest.json"
    )
    manifest = apply_plan(
        plan,
        approval_note=args.approval_note,
    )
    atomic_write_json(manifest_path, manifest)
    if manifest["status"] != "promoted":
        raise RuntimeError(
            f"replacement failed with status {manifest['status']}: "
            f"{manifest['failure']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
