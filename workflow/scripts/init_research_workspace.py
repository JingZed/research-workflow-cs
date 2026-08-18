#!/usr/bin/env python3
"""Plan or initialize a minimal, domain-neutral Research workspace."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys


ROOT_DIRECTORIES = (
    Path("workflow"),
    Path("workflow/skills"),
    Path("workflow/scripts"),
    Path("topics"),
)
TOPIC_DIRECTORIES = ("synthesis", "ideas", "papers")
REGISTRY_TEXT = "active_id: null\nactive_entry: null\nideas: []\n"
ALLOWED_ROOT_PROJECTIONS = {Path("workflow/skills")}


class WorkspaceInitError(RuntimeError):
    """Raised when initialization would be ambiguous or unsafe."""


@dataclass(frozen=True)
class WorkspacePlan:
    root: Path
    topic: str | None
    directories: tuple[Path, ...]
    files: tuple[Path, ...]


def _resolve_root(raw_root: str) -> Path:
    value = raw_root.strip()
    if not value:
        raise WorkspaceInitError("research root must not be empty")

    root = Path(value).expanduser()
    if not root.is_absolute():
        root = Path.cwd() / root
    # Inspect the lexical target before resolving it; otherwise a symlinked
    # root would disappear and the initializer could mutate its target.
    root = root.absolute()
    if root.is_symlink():
        raise WorkspaceInitError(f"research root must not be a symlink: {root}")
    root = root.resolve()

    forbidden = {Path("/").resolve(), Path.home().resolve(), Path.cwd().resolve()}
    if root in forbidden:
        raise WorkspaceInitError(
            "refusing to initialize a broad or current directory; provide an "
            "explicit Research root path"
        )
    return root


def _validate_topic(raw_topic: str) -> str:
    topic = raw_topic.strip()
    if not topic:
        raise WorkspaceInitError("topic must not be empty")
    if "\x00" in topic or "/" in topic or "\\" in topic:
        raise WorkspaceInitError("topic must be one directory name, not a path")
    if topic in {".", ".."}:
        raise WorkspaceInitError("topic must not be '.' or '..'")
    return topic


def _validate_root(root: Path) -> None:
    if root.is_symlink():
        raise WorkspaceInitError(f"research root must not be a symlink: {root}")
    if root.exists() and not root.is_dir():
        raise WorkspaceInitError(f"research root is not a directory: {root}")
    if not root.exists() or not any(root.iterdir()):
        return

    # An existing workflow or topics directory is an explicit Research-root
    # marker. Other entries are preserved; initialization touches only the
    # exact missing paths in ROOT_DIRECTORIES and the selected topic.
    markers = {"workflow", "topics"}
    if not markers.intersection(child.name for child in root.iterdir()):
        raise WorkspaceInitError(
            "refusing a non-empty directory without a workflow/ or topics/ "
            "Research-root marker"
        )


def _validate_directory_path(path: Path, *, allow_projection: bool = False) -> bool:
    if path.is_symlink():
        if allow_projection:
            return True
        raise WorkspaceInitError(f"workspace path must not be a symlink: {path}")
    if path.exists() and not path.is_dir():
        raise WorkspaceInitError(f"workspace path is not a directory: {path}")
    return path.exists()


def _validate_topic_root(topic_root: Path) -> None:
    if topic_root.is_symlink():
        raise WorkspaceInitError(f"topic path must not be a symlink: {topic_root}")
    if topic_root.exists() and not topic_root.is_dir():
        raise WorkspaceInitError(f"topic path is not a directory: {topic_root}")
    if not topic_root.exists():
        return

    allowed = set(TOPIC_DIRECTORIES)
    unexpected = sorted(
        child.name for child in topic_root.iterdir() if child.name not in allowed
    )
    if unexpected:
        rendered = ", ".join(unexpected[:8])
        if len(unexpected) > 8:
            rendered += ", ..."
        raise WorkspaceInitError(
            "refusing a topic directory with unrelated top-level entries: "
            + rendered
        )


def plan_workspace(raw_root: str, *, topic: str | None = None) -> WorkspacePlan:
    root = _resolve_root(raw_root)
    _validate_root(root)
    normalized_topic = _validate_topic(topic) if topic is not None else None

    directories: list[Path] = []
    for relative in ROOT_DIRECTORIES:
        path = root / relative
        exists = _validate_directory_path(
            path, allow_projection=relative in ALLOWED_ROOT_PROJECTIONS
        )
        if not exists:
            directories.append(path)

    files: list[Path] = []
    if normalized_topic is not None:
        topics_root = root / "topics"
        _validate_directory_path(topics_root)
        topic_root = topics_root / normalized_topic
        _validate_topic_root(topic_root)

        for name in TOPIC_DIRECTORIES:
            path = topic_root / name
            if path.is_symlink():
                raise WorkspaceInitError(f"topic path must not be a symlink: {path}")
            if path.exists() and not path.is_dir():
                raise WorkspaceInitError(f"topic path is not a directory: {path}")
            if not path.exists():
                directories.append(path)

        registry = topic_root / "ideas" / "registry.yaml"
        if registry.is_symlink():
            raise WorkspaceInitError(f"registry path must not be a symlink: {registry}")
        if registry.exists() and not registry.is_file():
            raise WorkspaceInitError(f"registry path is not a file: {registry}")
        if not registry.exists():
            files.append(registry)

    return WorkspacePlan(root, normalized_topic, tuple(directories), tuple(files))


def _relative(path: Path, root: Path) -> str:
    if path == root:
        return "."
    return path.relative_to(root).as_posix()


def render_plan(plan: WorkspacePlan, *, apply: bool) -> str:
    mode = "apply" if apply else "preview"
    lines = [f"research_root: {plan.root}", f"mode: {mode}"]
    if plan.topic is not None:
        lines.append(f"topic: {plan.topic}")
    if not plan.directories and not plan.files:
        lines.append("status: already_initialized")
        return "\n".join(lines)

    lines.append("create:")
    for path in (*plan.directories, *plan.files):
        kind = "directory" if path in plan.directories else "file"
        lines.append(f"- {kind}: {_relative(path, plan.root)}")
    return "\n".join(lines)


def initialize(
    raw_root: str, *, topic: str | None = None, apply: bool
) -> WorkspacePlan:
    plan = plan_workspace(raw_root, topic=topic)
    if not apply:
        return plan

    try:
        plan.root.mkdir(parents=True, exist_ok=True)
        for path in plan.directories:
            path.mkdir(parents=True, exist_ok=True)
        for path in plan.files:
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("x", encoding="utf-8") as handle:
                    handle.write(REGISTRY_TEXT)
            except FileExistsError:
                # A concurrent initializer won the race; never overwrite it.
                pass
    except OSError as exc:
        raise WorkspaceInitError(f"could not initialize workspace: {exc}") from exc

    final = plan_workspace(raw_root, topic=topic)
    if final.directories or final.files:
        raise WorkspaceInitError("workspace initialization did not reach a stable state")
    return plan


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Exact Research root directory")
    parser.add_argument(
        "--topic",
        help="Optional single directory name under topics/; the user supplies this",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create the minimal workspace; without this flag, only preview the plan",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        plan = initialize(args.root, topic=args.topic, apply=args.apply)
    except WorkspaceInitError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(render_plan(plan, apply=args.apply))
    if not args.apply and (plan.directories or plan.files):
        print("preview only; rerun with --apply to create these paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
