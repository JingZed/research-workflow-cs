#!/usr/bin/env python3
"""Resolve an existing writable paper directory without changing the filesystem."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


CURRENT_KEYS = ("active_paper_dir", "candidate", "active_artifact")
FILE_SUFFIXES = {
    ".bib",
    ".doc",
    ".docx",
    ".md",
    ".pdf",
    ".tex",
    ".typ",
}
PROTECTED_MARKERS = (
    "read-only",
    "protected",
    "prohibited",
    "do not write",
    "must not write",
    "never write",
)
READ_ONLY_DECLARATION_PATTERN = re.compile(
    r"\b(?:is|are|remain|remains|stay|stays|must remain|must stay)"
    r"\s+read only\b",
    re.IGNORECASE,
)
WRITABLE_MARKERS = (
    "writable",
    "write scope",
    "changes belong under",
    "changes go under",
    "changes must go under",
    "edits belong under",
    "edits go under",
    "edits must go under",
    "write only under",
)
ACTIVE_PATTERN = re.compile(
    r"(?:\bactive\b.*\b(?:paper|candidate|manuscript)\b|"
    r"\b(?:paper|candidate|manuscript)\b.*\bactive\b)",
    re.IGNORECASE,
)
STATE_LINE_PATTERN = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$"
)
CODE_SPAN_PATTERN = re.compile(r"`([^`\n]+)`")


class PaperDirResolutionError(RuntimeError):
    """Base class for deterministic resolver failures."""

    code = "paper_dir_resolution_error"

    def __init__(self, message: str, paths: Sequence[Path] = ()) -> None:
        super().__init__(message)
        self.paths = tuple(paths)

    def as_dict(self) -> dict[str, object]:
        return {
            "error": self.code,
            "message": str(self),
            "paths": [str(path) for path in self.paths],
        }


class StartPathError(PaperDirResolutionError):
    code = "invalid_start_path"


class NoPaperCandidateError(PaperDirResolutionError):
    code = "no_paper_candidate"


class MultiplePaperCandidatesError(PaperDirResolutionError):
    code = "multiple_paper_candidates"


class ConflictingPaperTargetError(PaperDirResolutionError):
    code = "conflicting_paper_targets"


class ProtectedPaperTargetError(PaperDirResolutionError):
    code = "protected_paper_target"


class DisallowedPaperTargetError(PaperDirResolutionError):
    code = "outside_writable_scope"


class MissingPaperTargetError(PaperDirResolutionError):
    code = "missing_paper_target"


class OutsideProjectTargetError(PaperDirResolutionError):
    code = "outside_project_root"


@dataclass(frozen=True)
class RulePolicy:
    rules_path: Path | None
    active_dirs: tuple[Path, ...]
    writable_dirs: tuple[Path, ...]
    protected_dirs: tuple[Path, ...]


@dataclass(frozen=True)
class Candidate:
    path: Path
    sources: tuple[str, ...]


@dataclass(frozen=True)
class PaperDirResolution:
    paper_dir: Path
    project_root: Path
    sources: tuple[str, ...]
    rules_path: Path | None
    current_path: Path | None
    writable_dirs: tuple[Path, ...]
    protected_dirs: tuple[Path, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "paper_dir": str(self.paper_dir),
            "project_root": str(self.project_root),
            "sources": list(self.sources),
            "rules_path": str(self.rules_path) if self.rules_path else None,
            "current_path": str(self.current_path) if self.current_path else None,
            "writable_dirs": [str(path) for path in self.writable_dirs],
            "protected_dirs": [str(path) for path in self.protected_dirs],
        }


def _unique_paths(paths: Sequence[Path]) -> tuple[Path, ...]:
    return tuple(dict.fromkeys(paths))


def _is_within(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def _start_directory(start: str | Path) -> Path:
    path = Path(start).expanduser().resolve(strict=False)
    if not path.exists():
        raise StartPathError(f"start path does not exist: {path}", (path,))
    return path if path.is_dir() else path.parent


def _find_nearest(start: Path, relative: Path) -> Path | None:
    for directory in (start, *start.parents):
        candidate = directory / relative
        if candidate.is_file():
            return candidate.resolve()
    return None


def _logical_units(text: str) -> tuple[str, ...]:
    blocks: list[str] = []
    current: list[str] = []

    def flush() -> None:
        if current:
            blocks.append(" ".join(current))
            current.clear()

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            flush()
            continue
        if re.match(r"^[-*]\s+", line):
            flush()
        current.append(line)
    flush()

    units: list[str] = []
    for block in blocks:
        units.extend(
            part.strip()
            for part in re.split(r"(?<=[.!?])\s+", block)
            if part.strip()
        )
    return tuple(units)


def _looks_like_path(token: str) -> bool:
    token = token.strip()
    if not token or token.startswith(("http://", "https://", "$", "<")):
        return False
    if "\n" in token:
        return False
    return "/" in token or Path(token.rstrip("/")).suffix.lower() in FILE_SUFFIXES


def _path_to_directory(raw_path: str, base: Path) -> Path:
    token = raw_path.strip().strip("\"'").rstrip(",;")
    trailing_slash = token.endswith("/")
    path = Path(token).expanduser()
    if not path.is_absolute():
        path = base / path
    path = path.resolve(strict=False)

    if trailing_slash or path.is_dir():
        return path
    if path.is_file() or path.suffix.lower() in FILE_SUFFIXES:
        return path.parent
    return path


def _paths_from_unit(unit: str, base: Path) -> tuple[Path, ...]:
    return _unique_paths(
        [
            _path_to_directory(token, base)
            for token in CODE_SPAN_PATTERN.findall(unit)
            if _looks_like_path(token)
        ]
    )


def parse_rule_policy(rules_path: Path | None) -> RulePolicy:
    if rules_path is None:
        return RulePolicy(None, (), (), ())

    active: list[Path] = []
    writable: list[Path] = []
    protected: list[Path] = []
    text = rules_path.read_text(encoding="utf-8")

    for unit in _logical_units(text):
        lower = unit.lower()
        is_protected = any(
            marker in lower for marker in PROTECTED_MARKERS
        ) or READ_ONLY_DECLARATION_PATTERN.search(unit) is not None
        is_writable = any(marker in lower for marker in WRITABLE_MARKERS)
        is_active = ACTIVE_PATTERN.search(unit) is not None
        if not (is_protected or is_writable or is_active):
            continue

        paths = _paths_from_unit(unit, rules_path.parent)
        if is_protected:
            protected.extend(paths)
        if is_writable:
            writable.extend(paths)
        if is_active:
            active.extend(paths)

    return RulePolicy(
        rules_path=rules_path,
        active_dirs=_unique_paths(active),
        writable_dirs=_unique_paths(writable),
        protected_dirs=_unique_paths(protected),
    )


def _read_current_fields(current_path: Path | None) -> dict[str, list[str]]:
    fields = {key: [] for key in CURRENT_KEYS}
    if current_path is None:
        return fields

    for line in current_path.read_text(encoding="utf-8").splitlines():
        match = STATE_LINE_PATTERN.match(line)
        if not match:
            continue
        key, value = match.groups()
        if key in fields and value.strip():
            fields[key].append(value.strip())
    return fields


def _clean_state_value(value: str) -> str:
    code_spans = CODE_SPAN_PATTERN.findall(value)
    if code_spans:
        return code_spans[0].strip()
    value = value.split(" #", 1)[0].strip()
    return value.strip("`\"'")


def _merge_candidates(entries: Sequence[Candidate]) -> tuple[Candidate, ...]:
    sources_by_path: dict[Path, list[str]] = {}
    for entry in entries:
        sources_by_path.setdefault(entry.path, []).extend(entry.sources)
    return tuple(
        Candidate(path, tuple(dict.fromkeys(sources)))
        for path, sources in sources_by_path.items()
    )


def _current_candidates(
    current_path: Path | None, project_root: Path
) -> tuple[Candidate, ...]:
    fields = _read_current_fields(current_path)
    active_values = fields["active_paper_dir"]
    if active_values:
        entries = [
            Candidate(
                _path_to_directory(_clean_state_value(value), project_root),
                ("current.active_paper_dir",),
            )
            for value in active_values
        ]
    else:
        entries = []
        for key in ("candidate", "active_artifact"):
            entries.extend(
                Candidate(
                    _path_to_directory(_clean_state_value(value), project_root),
                    (f"current.{key}",),
                )
                for value in fields[key]
            )

    candidates = _merge_candidates(entries)
    if len(candidates) > 1:
        raise MultiplePaperCandidatesError(
            "CURRENT names multiple paper candidates",
            tuple(candidate.path for candidate in candidates),
        )
    return candidates


def _rule_candidates(policy: RulePolicy) -> tuple[Candidate, ...]:
    candidates = _merge_candidates(
        [
            Candidate(path, ("rules.active_paper_dir",))
            for path in policy.active_dirs
        ]
    )
    if len(candidates) > 1:
        raise MultiplePaperCandidatesError(
            "nearest project rules name multiple active paper candidates",
            tuple(candidate.path for candidate in candidates),
        )
    return candidates


def _has_writable_override(
    target: Path, protected: Path, writable_dirs: Sequence[Path]
) -> bool:
    return any(
        writable != protected
        and protected in writable.parents
        and _is_within(target, writable)
        for writable in writable_dirs
    )


def _validate_candidate(
    candidate: Path, project_root: Path, policy: RulePolicy
) -> None:
    if not _is_within(candidate, project_root):
        raise OutsideProjectTargetError(
            f"paper candidate is outside the project root: {candidate}",
            (candidate, project_root),
        )

    for protected in policy.protected_dirs:
        if _is_within(candidate, protected) and not _has_writable_override(
            candidate, protected, policy.writable_dirs
        ):
            raise ProtectedPaperTargetError(
                f"paper candidate is protected by project rules: {candidate}",
                (candidate, protected),
            )

    if policy.writable_dirs and not any(
        _is_within(candidate, writable) for writable in policy.writable_dirs
    ):
        raise DisallowedPaperTargetError(
            f"paper candidate is outside the allowed write scope: {candidate}",
            (candidate, *policy.writable_dirs),
        )

    if not candidate.is_dir():
        raise MissingPaperTargetError(
            f"paper candidate directory does not exist: {candidate}",
            (candidate,),
        )


def resolve_paper_dir(
    start: str | Path,
    *,
    explicit_target: str | Path | None = None,
) -> PaperDirResolution:
    """Resolve one existing paper directory from nearest rules and CURRENT."""

    start_dir = _start_directory(start)
    current_path = _find_nearest(start_dir, Path("notes") / "CURRENT.md")
    rules_path = _find_nearest(start_dir, Path("AGENTS.md"))
    project_root = (
        current_path.parent.parent
        if current_path is not None
        else rules_path.parent
        if rules_path is not None
        else start_dir
    ).resolve()
    policy = parse_rule_policy(rules_path)

    candidates: list[Candidate] = []
    candidates.extend(_current_candidates(current_path, project_root))
    candidates.extend(_rule_candidates(policy))
    if explicit_target is not None:
        candidates.append(
            Candidate(
                _path_to_directory(str(explicit_target), project_root),
                ("explicit_target",),
            )
        )

    merged = _merge_candidates(candidates)
    if not merged:
        raise NoPaperCandidateError(
            "no paper candidate is named by CURRENT, project rules, or the user"
        )

    for candidate in merged:
        _validate_candidate(candidate.path, project_root, policy)

    if len(merged) > 1:
        details = ", ".join(
            f"{candidate.path} ({', '.join(candidate.sources)})"
            for candidate in merged
        )
        raise ConflictingPaperTargetError(
            f"paper target sources disagree: {details}",
            tuple(candidate.path for candidate in merged),
        )

    selected = merged[0]
    return PaperDirResolution(
        paper_dir=selected.path,
        project_root=project_root,
        sources=selected.sources,
        rules_path=rules_path,
        current_path=current_path,
        writable_dirs=policy.writable_dirs,
        protected_dirs=policy.protected_dirs,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--start",
        default=".",
        help="Path inside the project whose nearest rules and CURRENT are used.",
    )
    parser.add_argument(
        "--target",
        help="Optional user-named paper directory or artifact to reconcile.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        resolution = resolve_paper_dir(
            args.start,
            explicit_target=args.target,
        )
    except PaperDirResolutionError as exc:
        print(json.dumps(exc.as_dict(), sort_keys=True), file=sys.stderr)
        return 2

    print(json.dumps(resolution.as_dict(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
