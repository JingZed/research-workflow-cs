#!/usr/bin/env python3
"""Plan or initialize a minimal, domain-neutral research workspace."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys


WORKSPACE_DIRS = ("synthesis", "ideas", "papers")
REGISTRY_TEXT = "active_id: null\nactive_entry: null\nideas: []\n"


class WorkspaceInitError(RuntimeError):
    """Raised when initialization would be ambiguous or unsafe."""


@dataclass(frozen=True)
class WorkspacePlan:
    root: Path
    directories: tuple[Path, ...]
    files: tuple[Path, ...]


def _resolve_root(raw_root: str) -> Path:
    value = raw_root.strip()
    if not value:
        raise WorkspaceInitError("workspace root must not be empty")

    root = Path(value).expanduser()
    if not root.is_absolute():
        root = Path.cwd() / root
    # Inspect the lexical target before resolving it; otherwise a symlinked
    # root would disappear and the initializer could mutate its target.
    root = root.absolute()
    if root.is_symlink():
        raise WorkspaceInitError(f"workspace root must not be a symlink: {root}")
    root = root.resolve()

    forbidden = {Path("/").resolve(), Path.home().resolve(), Path.cwd().resolve()}
    if root in forbidden:
        raise WorkspaceInitError(
            "refusing to initialize a broad or current directory; provide an "
            "explicit child workspace path"
        )
    return root


def _validate_existing_root(root: Path) -> None:
    if root.is_symlink():
        raise WorkspaceInitError(f"workspace root must not be a symlink: {root}")
    if root.exists() and not root.is_dir():
        raise WorkspaceInitError(f"workspace root is not a directory: {root}")
    if not root.exists():
        return

    allowed = set(WORKSPACE_DIRS)
    unexpected = sorted(
        child.name for child in root.iterdir() if child.name not in allowed
    )
    if unexpected:
        rendered = ", ".join(unexpected[:8])
        if len(unexpected) > 8:
            rendered += ", ..."
        raise WorkspaceInitError(
            "refusing a directory with unrelated top-level entries: " + rendered
        )


def plan_workspace(raw_root: str) -> WorkspacePlan:
    root = _resolve_root(raw_root)
    _validate_existing_root(root)

    directories: list[Path] = []
    for name in WORKSPACE_DIRS:
        path = root / name
        if path.is_symlink():
            raise WorkspaceInitError(f"workspace path must not be a symlink: {path}")
        if path.exists() and not path.is_dir():
            raise WorkspaceInitError(f"workspace path is not a directory: {path}")
        if not path.exists():
            directories.append(path)

    registry = root / "ideas" / "registry.yaml"
    if registry.is_symlink():
        raise WorkspaceInitError(f"registry path must not be a symlink: {registry}")
    if registry.exists() and not registry.is_file():
        raise WorkspaceInitError(f"registry path is not a file: {registry}")
    files = () if registry.exists() else (registry,)
    return WorkspacePlan(root, tuple(directories), files)


def _relative(path: Path, root: Path) -> str:
    if path == root:
        return "."
    return path.relative_to(root).as_posix()


def render_plan(plan: WorkspacePlan, *, apply: bool) -> str:
    mode = "apply" if apply else "preview"
    lines = [f"workspace: {plan.root}", f"mode: {mode}"]
    if not plan.directories and not plan.files:
        lines.append("status: already_initialized")
        return "\n".join(lines)

    lines.append("create:")
    for path in (*plan.directories, *plan.files):
        kind = "directory" if path in plan.directories else "file"
        lines.append(f"- {kind}: {_relative(path, plan.root)}")
    return "\n".join(lines)


def initialize(raw_root: str, *, apply: bool) -> WorkspacePlan:
    plan = plan_workspace(raw_root)
    if not apply:
        return plan

    try:
        plan.root.mkdir(parents=True, exist_ok=True)
        for path in plan.directories:
            path.mkdir(parents=True, exist_ok=True)
        for path in plan.files:
            try:
                with path.open("x", encoding="utf-8") as handle:
                    handle.write(REGISTRY_TEXT)
            except FileExistsError:
                # A concurrent initializer won the race; never overwrite it.
                pass
    except OSError as exc:
        raise WorkspaceInitError(f"could not initialize workspace: {exc}") from exc

    final = plan_workspace(raw_root)
    if final.directories or final.files:
        raise WorkspaceInitError("workspace initialization did not reach a stable state")
    return plan


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Exact workspace directory to create")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create the minimal workspace; without this flag, only preview the plan",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        plan = initialize(args.root, apply=args.apply)
    except WorkspaceInitError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(render_plan(plan, apply=args.apply))
    if not args.apply and (plan.directories or plan.files):
        print("preview only; rerun with --apply to create these paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
