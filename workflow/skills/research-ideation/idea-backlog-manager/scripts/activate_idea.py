#!/usr/bin/env python3
"""Activate one registered research idea without overwriting scientific state."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import sys
import uuid

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    yaml = None


IDEA_ID_RE = re.compile(r"^i\d{3,}$")
TERMINAL_STATUSES = {"archived", "retired"}


class LifecycleError(RuntimeError):
    """Raised when activation would violate the idea lifecycle contract."""


def _within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _one_line(value: str) -> str:
    return " ".join(value.split()).strip()


def _atomic_write(path: Path, text: str) -> None:
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _load_registry(path: Path) -> tuple[str, dict[str, object]]:
    if yaml is None:
        raise LifecycleError("PyYAML is required to activate an idea")
    try:
        original = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise LifecycleError(f"cannot read registry {path}: {exc}") from exc
    try:
        payload = yaml.safe_load(original)
    except yaml.YAMLError as exc:
        raise LifecycleError(f"invalid registry YAML in {path}: {exc}") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("ideas"), list):
        raise LifecycleError(f"{path} must contain a mapping with an ideas list")
    return original, payload


def _registry_entry(payload: dict[str, object], idea_id: str) -> dict[str, object]:
    matches = [
        entry
        for entry in payload["ideas"]
        if isinstance(entry, dict) and entry.get("id") == idea_id
    ]
    if len(matches) != 1:
        raise LifecycleError(
            f"registry must contain exactly one entry for {idea_id}; found {len(matches)}"
        )
    return matches[0]


def _replace_root_scalar(text: str, key: str, value: str) -> str:
    rendered = f"{key}: {json.dumps(value, ensure_ascii=False)}"
    pattern = re.compile(rf"^{re.escape(key)}\s*:.*$", flags=re.MULTILINE)
    if pattern.search(text):
        return pattern.sub(rendered, text, count=1)
    ideas_match = re.search(r"^ideas\s*:", text, flags=re.MULTILINE)
    if ideas_match:
        return text[: ideas_match.start()] + rendered + "\n" + text[ideas_match.start() :]
    return rendered + "\n" + text


def _replace_entry_status(text: str, idea_id: str) -> str:
    id_pattern = re.compile(
        rf"^(?P<indent>\s*)-\s+id\s*:\s*[\"']?{re.escape(idea_id)}[\"']?\s*$",
        flags=re.MULTILINE,
    )
    match = id_pattern.search(text)
    if not match:
        raise LifecycleError(f"cannot locate textual registry entry for {idea_id}")
    indent = match.group("indent")
    next_entry = re.search(rf"^{re.escape(indent)}-\s+id\s*:", text[match.end() :], re.MULTILINE)
    end = match.end() + (next_entry.start() if next_entry else len(text[match.end() :]))
    block = text[match.start() : end]
    status_pattern = re.compile(rf"^{re.escape(indent)}  status\s*:.*$", re.MULTILINE)
    if status_pattern.search(block):
        updated = status_pattern.sub(f"{indent}  status: active", block, count=1)
    else:
        line_end = block.find("\n")
        insertion = len(block) if line_end < 0 else line_end + 1
        updated = block[:insertion] + f"{indent}  status: active\n" + block[insertion:]
    return text[: match.start()] + updated + text[end:]


def _render_registry(
    original: str, payload: dict[str, object], idea_id: str, canonical_dir: str
) -> str:
    updated = _replace_root_scalar(original, "active_id", idea_id)
    updated = _replace_root_scalar(updated, "active_entry", canonical_dir)
    updated = _replace_entry_status(updated, idea_id)
    if not updated.endswith("\n"):
        updated += "\n"
    try:
        parsed = yaml.safe_load(updated)
    except yaml.YAMLError as exc:  # pragma: no cover - defensive
        raise LifecycleError(f"rendered registry is invalid YAML: {exc}") from exc
    entry = _registry_entry(parsed, idea_id)
    if (
        parsed.get("active_id") != idea_id
        or parsed.get("active_entry") != canonical_dir
        or entry.get("status") != "active"
    ):
        raise LifecycleError("rendered registry failed its activation self-check")
    return updated


def _current_text(args: argparse.Namespace) -> str:
    return "\n".join(
        (
            f"phase: {_one_line(args.phase)}",
            f"active_artifact: {_one_line(args.active_artifact)}",
            f"current_result: {_one_line(args.current_result)}",
            f"open_blockers: {_one_line(args.open_blockers)}",
            f"next_action: {_one_line(args.next_action)}",
            f"last_updated: {_one_line(args.last_updated)}",
            "",
        )
    )


def _project_state_text(
    *, idea_id: str, title: str, args: argparse.Namespace
) -> str:
    return f"""# Project State

## Current Question

- Active idea: {idea_id} — {title}
- Current phase: {_one_line(args.phase)}
- Active artifact: `{_one_line(args.active_artifact)}`

## Evidence

- Strongest result: {_one_line(args.current_result)}
- Evidence path: `{_one_line(args.active_artifact)}`
- Remaining uncertainty: {_one_line(args.open_blockers)}

## Interpretation

- Supported conclusion: No broader scientific conclusion is recorded by activation alone.
- Boundary: Activation creates resume state; it does not promote evidence or paper claims.

## Risks and Blockers

- Risk or blocker: {_one_line(args.open_blockers)}

## Next Scientific Decision

- Next action: {_one_line(args.next_action)}
- Stop condition: Record before launching the first nontrivial experiment.

## Decision Log

### {_one_line(args.last_updated)} — Idea activated

- Decision: Activate {idea_id} and establish canonical resume state.
- Evidence: Explicit user direction and the registered `idea.md`.
- Consequence: Future active work resumes from `notes/CURRENT.md`.
"""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic-root", required=True)
    parser.add_argument("--idea-id", required=True)
    parser.add_argument("--next-action", required=True)
    parser.add_argument("--phase", default="ideation")
    parser.add_argument("--active-artifact", default="idea.md")
    parser.add_argument(
        "--current-result", default="Idea activated; no scientific result recorded yet."
    )
    parser.add_argument("--open-blockers", default="none recorded")
    parser.add_argument(
        "--last-updated", default=datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def activate(args: argparse.Namespace) -> dict[str, object]:
    topic_root = Path(args.topic_root).expanduser().resolve(strict=True)
    if not IDEA_ID_RE.fullmatch(args.idea_id):
        raise LifecycleError(f"invalid idea ID {args.idea_id!r}; expected iNNN")
    if not (topic_root / "synthesis").is_dir() or not (topic_root / "ideas").is_dir():
        raise LifecycleError("topic root must contain both synthesis/ and ideas/")

    registry_path = topic_root / "ideas" / "registry.yaml"
    original_registry, payload = _load_registry(registry_path)
    entry = _registry_entry(payload, args.idea_id)
    status = str(entry.get("status", "")).strip().lower()
    if status in TERMINAL_STATUSES:
        raise LifecycleError(f"cannot activate {args.idea_id} from terminal status {status!r}")
    current_active = payload.get("active_id")
    if current_active not in (None, args.idea_id):
        raise LifecycleError(
            f"topic already has active_id {current_active!r}; explicit deactivation or switch is required"
        )
    active_status_ids = {
        str(candidate.get("id", ""))
        for candidate in payload["ideas"]
        if isinstance(candidate, dict)
        and str(candidate.get("status", "")).strip().lower() == "active"
    }
    if current_active is None and active_status_ids:
        raise LifecycleError(
            "registry has status 'active' entries while active_id is null; "
            "repair the lifecycle pointers before activation"
        )
    if current_active == args.idea_id and active_status_ids != {args.idea_id}:
        raise LifecycleError(
            "registry status 'active' entries do not match active_id; "
            "repair the lifecycle pointers before activation"
        )

    canonical_value = entry.get("canonical_dir")
    if not isinstance(canonical_value, str) or not canonical_value.strip():
        raise LifecycleError(f"registry entry {args.idea_id} has no canonical_dir")
    canonical_path = (topic_root / canonical_value).resolve(strict=True)
    if not _within(canonical_path, topic_root):
        raise LifecycleError(f"canonical_dir escapes topic root: {canonical_value}")
    if not (canonical_path / "idea.md").is_file():
        raise LifecycleError(f"missing canonical idea.md: {canonical_path / 'idea.md'}")

    notes = canonical_path / "notes"
    current = notes / "CURRENT.md"
    project_state = notes / "project-state.md"
    state_exists = (current.exists(), project_state.exists())
    if state_exists[0] != state_exists[1]:
        raise LifecycleError(
            "activation refuses one-sided resume state; repair CURRENT.md/project-state.md first"
        )
    if state_exists[0] and (
        not current.read_text(encoding="utf-8").strip()
        or not project_state.read_text(encoding="utf-8").strip()
    ):
        raise LifecycleError("activation refuses empty existing resume state")

    title = str(entry.get("title") or args.idea_id)
    rendered_registry = _render_registry(
        original_registry, payload, args.idea_id, canonical_value
    )
    plan = {
        "idea_id": args.idea_id,
        "canonical_dir": canonical_value,
        "create_resume_state": not state_exists[0],
        "set_active_id": args.idea_id,
        "set_active_entry": canonical_value,
        "set_status": "active",
    }
    if args.dry_run:
        return plan

    notes_created = False
    created_files: list[Path] = []
    try:
        if not state_exists[0]:
            if not notes.exists():
                notes.mkdir(parents=True)
                notes_created = True
            _atomic_write(current, _current_text(args))
            created_files.append(current)
            _atomic_write(
                project_state,
                _project_state_text(idea_id=args.idea_id, title=title, args=args),
            )
            created_files.append(project_state)
        _atomic_write(registry_path, rendered_registry)
    except Exception:
        for path in reversed(created_files):
            if path.exists():
                path.unlink()
        if notes_created and notes.exists() and not any(notes.iterdir()):
            notes.rmdir()
        if registry_path.read_text(encoding="utf-8") != original_registry:
            _atomic_write(registry_path, original_registry)
        raise
    return plan


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        plan = activate(args)
    except (LifecycleError, OSError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    print(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
