#!/usr/bin/env python3
"""Validate the lightweight research workflow without modifying project files."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


CAPABILITY_VALUES = {"off", "on", "auto"}
ACTIVE_LIFECYCLE_STATUSES = {"active", "finishing"}
CURRENT_ALLOWED_FIELDS = (
    "phase",
    "active_artifact",
    "current_result",
    "open_blockers",
    "next_action",
    "last_updated",
)
CURRENT_REQUIRED_FIELDS = CURRENT_ALLOWED_FIELDS
CURRENT_MAX_NONEMPTY_LINES = 15
CURRENT_MAX_BYTES = 2 * 1024
ACTIVE_ARTIFACT_MAX_BYTES = 64 * 1024
PROJECT_STATE_MAX_LINES = 120
PROJECT_STATE_MAX_BYTES = 8 * 1024
TODO_MAX_NONEMPTY_LINES = 80
TODO_MAX_BYTES = 8 * 1024
CURRENT_FIELD_RE = re.compile(r"^(?P<key>[a-z][a-z0-9_]*):(?P<value>.*)$")
PROJECT_STATE_PHASE_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:current|当前)\s+phase\s*[:：]\s*`?([^`#]+?)`?\s*$",
    re.IGNORECASE,
)
LEGACY_SKILL_PATTERNS = {
    "ThirdSpace runtime": re.compile(r"\bthirdspace\b", re.IGNORECASE),
    "global freshness state": re.compile(
        r"freshness[-_ ]?(?:state|report|override)", re.IGNORECASE
    ),
    "approval sentinel": re.compile(
        r"(?:idea-approved|design-approved|story-approved|writing-ready)",
        re.IGNORECASE,
    ),
    "claim ledger": re.compile(r"claim[-_ ]snapshot", re.IGNORECASE),
    "revision ledger Skill": re.compile(
        r"(?:revision-quality-guardian|revision_quality_guardian)",
        re.IGNORECASE,
    ),
    "numbered workflow gate": re.compile(r"\bG[1-4]\b"),
}
PROJECT_STATE_PROCESS_PATTERNS = {
    "workflow-control heading": re.compile(
        r"^#{1,6}\s+.*(?:harness state repair|workflow (?:state )?reset|"
        r"workflow reset and resume rule|routing state|session state|"
        r"handoff state|audit trail)\s*$",
        re.IGNORECASE | re.MULTILINE,
    ),
    "runtime routing field": re.compile(
        r"^\s*(?:[-*]\s*)?(?:current routing|next skill|gate status|"
        r"gate_status|coordination_state|workflow_rule|approval_status)\s*[:：]",
        re.IGNORECASE | re.MULTILINE,
    ),
    "session manifest contract": re.compile(
        r"(?:session manifest|scientific_state_changed)", re.IGNORECASE
    ),
}
LEGACY_LIVE_FILE_PATTERNS = (
    re.compile(r"^(?:execution-entry|writing-entry)\.md$", re.IGNORECASE),
    re.compile(r"^review-state\.json$", re.IGNORECASE),
    re.compile(r"^promotion-gate-result(?:\..+)?$", re.IGNORECASE),
    re.compile(r"^research-pipeline(?: .*)?\.md$", re.IGNORECASE),
    re.compile(r"^(?:HANDOFF|plan-tree)\.md$", re.IGNORECASE),
    re.compile(r"^idea-spec(?:\.provenance\.json|\.md)$", re.IGNORECASE),
)
LEGACY_SCAN_EXCLUDED_DIRS = frozenset(
    {
        ".backup",
        ".ccb",
        ".git",
        ".worktrees",
        "archive",
        "archives",
        "artifacts",
        "backups",
        "ccb-requests",
        "history",
        "node_modules",
        "outputs",
        "records",
        "rescue_handoff",
        "runs",
        "tmp",
        "vendor",
        "worktrees",
    }
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--idea", required=True, help="Path to the active idea root")
    return parser.parse_args()


def validate_capabilities(idea_root: Path, errors: list[str]) -> None:
    path = idea_root / "notes" / "capabilities.yaml"
    if not path.exists():
        return
    if yaml is None:
        errors.append("PyYAML is required to validate notes/capabilities.yaml")
        return
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        errors.append(f"{path}: invalid YAML ({exc})")
        return
    if not isinstance(payload, dict):
        errors.append(f"{path}: expected a mapping")
        return
    capabilities = payload.get("capabilities", payload)
    if not isinstance(capabilities, dict):
        errors.append(f"{path}: capabilities must be a mapping")
        return
    for key, value in capabilities.items():
        if isinstance(value, bool):
            normalized = "on" if value else "off"
        else:
            normalized = str(value).strip().lower()
        if normalized not in CAPABILITY_VALUES:
            errors.append(
                f"{path}: {key} has invalid value {value!r}; "
                f"expected one of {sorted(CAPABILITY_VALUES)}"
            )


def _within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _parse_current(lines: list[str]) -> tuple[dict[str, str], list[str]]:
    fields: dict[str, str] = {}
    issues: list[str] = []
    active_field: str | None = None
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        if line[:1].isspace():
            if active_field is None:
                issues.append(
                    f"line {line_number}: indented continuation has no preceding field"
                )
                continue
            continuation = line.strip()
            fields[active_field] = " ".join(
                part for part in (fields[active_field], continuation) if part
            )
            continue

        match = CURRENT_FIELD_RE.fullmatch(line)
        if match is None:
            issues.append(
                f"line {line_number}: expected 'field: value' or an indented continuation"
            )
            active_field = None
            continue

        key = match.group("key")
        value = match.group("value").strip().strip("`\"'")
        if key in fields:
            issues.append(f"line {line_number}: duplicate field {key!r}")
            active_field = None
            continue
        fields[key] = value
        active_field = key
    return fields, issues


def _current_fields(lines: list[str]) -> dict[str, str]:
    fields, _ = _parse_current(lines)
    return fields


def validate_current_md(
    idea_root: Path,
    errors: list[str],
    warnings: list[str],
    *,
    required: bool = False,
    allowed_root: Path | None = None,
) -> None:
    path = idea_root / "notes" / "CURRENT.md"
    notes = path.parent
    competitors = []
    if notes.is_dir():
        competitors = sorted(
            candidate
            for candidate in notes.iterdir()
            if candidate.is_file()
            and candidate.suffix.lower() == ".md"
            and candidate.name.casefold().startswith("current")
            and candidate.name != "CURRENT.md"
        )
    for competitor in competitors:
        message = f"{competitor}: competing resume filename; keep only canonical CURRENT.md live"
        (errors if required else warnings).append(message)
    if not path.exists():
        if required:
            errors.append(f"{path}: missing canonical resume state")
        return
    text = path.read_text(encoding="utf-8")
    raw_lines = text.splitlines()
    nonempty_lines = [line for line in raw_lines if line.strip()]
    if not nonempty_lines:
        errors.append(f"{path}: empty resume file")
        return
    if len(nonempty_lines) > CURRENT_MAX_NONEMPTY_LINES:
        errors.append(
            f"{path}: {len(nonempty_lines)} non-empty lines; maximum is "
            f"{CURRENT_MAX_NONEMPTY_LINES}"
        )
    byte_count = len(text.encode("utf-8"))
    if byte_count > CURRENT_MAX_BYTES:
        errors.append(
            f"{path}: {byte_count} bytes; maximum is {CURRENT_MAX_BYTES} bytes"
        )

    fields, syntax_issues = _parse_current(raw_lines)
    errors.extend(f"{path}: {issue}" for issue in syntax_issues)
    for field in fields:
        if field not in CURRENT_ALLOWED_FIELDS:
            errors.append(f"{path}: unknown top-level field {field!r}")
    known_field_order = tuple(
        field for field in fields if field in CURRENT_ALLOWED_FIELDS
    )
    if known_field_order != CURRENT_ALLOWED_FIELDS:
        errors.append(
            f"{path}: top-level fields must appear exactly in this order: "
            + ", ".join(CURRENT_ALLOWED_FIELDS)
        )
    for field in CURRENT_REQUIRED_FIELDS:
        if not fields.get(field):
            errors.append(f"{path}: missing or empty required field {field!r}")

    raw_artifact = fields.get("active_artifact")
    if not raw_artifact:
        return
    artifact = Path(raw_artifact).expanduser()
    if not artifact.is_absolute():
        artifact = idea_root / artifact
    artifact = artifact.resolve(strict=False)
    if not artifact.exists():
        errors.append(
            f"{path}: active_artifact points to missing artifact {raw_artifact!r}"
        )
    elif not artifact.is_file():
        errors.append(
            f"{path}: active_artifact must point to one regular file, not "
            f"{raw_artifact!r}"
        )
    elif artifact.stat().st_size > ACTIVE_ARTIFACT_MAX_BYTES:
        errors.append(
            f"{path}: active_artifact is {artifact.stat().st_size} bytes; maximum "
            f"is {ACTIVE_ARTIFACT_MAX_BYTES} bytes"
        )
    if allowed_root is not None and not _within(artifact, allowed_root.resolve()):
        errors.append(
            f"{path}: active_artifact escapes the research workspace: {artifact}"
        )


def validate_project_state(
    idea_root: Path,
    errors: list[str],
    warnings: list[str],
    *,
    required: bool = False,
) -> None:
    path = idea_root / "notes" / "project-state.md"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            errors.append(f"{path}: empty project state")
            return
        line_count = len(text.splitlines())
        byte_count = len(text.encode("utf-8"))
        if line_count > PROJECT_STATE_MAX_LINES:
            errors.append(
                f"{path}: {line_count} lines; maximum is {PROJECT_STATE_MAX_LINES}"
            )
        if byte_count > PROJECT_STATE_MAX_BYTES:
            errors.append(
                f"{path}: {byte_count} bytes; maximum is {PROJECT_STATE_MAX_BYTES} bytes"
            )
        for label, pattern in PROJECT_STATE_PROCESS_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{path}: contains forbidden {label}")
        return

    if required:
        errors.append(f"{path}: missing detailed resume state for an active idea")
        return

    scientific_markers = (
        idea_root / "hypothesis.md",
        idea_root / "experiments" / "results" / "summary.md",
        idea_root / "drafts" / "outline.md",
    )
    if any(marker.exists() for marker in scientific_markers):
        warnings.append(
            f"{path}: missing detailed resume state for an active scientific project"
        )


def validate_todo(idea_root: Path, errors: list[str]) -> None:
    candidates = [idea_root / "TODO.md", idea_root / "notes" / "TODO.md"]
    live = [path for path in candidates if path.is_file()]
    if len(live) > 1:
        errors.append(
            f"{idea_root}: keep only one lightweight TODO.md; found "
            + ", ".join(str(path) for path in live)
        )
    for path in live:
        text = path.read_text(encoding="utf-8")
        nonempty = sum(1 for line in text.splitlines() if line.strip())
        size = len(text.encode("utf-8"))
        if nonempty > TODO_MAX_NONEMPTY_LINES:
            errors.append(
                f"{path}: {nonempty} non-empty lines; maximum is "
                f"{TODO_MAX_NONEMPTY_LINES}"
            )
        if size > TODO_MAX_BYTES:
            errors.append(
                f"{path}: {size} bytes; maximum is {TODO_MAX_BYTES} bytes"
            )


def validate_live_legacy_artifacts(idea_root: Path, errors: list[str]) -> None:
    """Reject retired workflow controllers outside explicitly historical trees."""

    for current, dirnames, filenames in os.walk(idea_root, followlinks=False):
        current_path = Path(current)
        dirnames[:] = sorted(
            name
            for name in dirnames
            if name not in LEGACY_SCAN_EXCLUDED_DIRS
            and not name.startswith(".ccb.retired-")
        )
        if "session-proposals" in dirnames:
            errors.append(
                f"{current_path / 'session-proposals'}: retired live workflow "
                "directory; move it under notes/history"
            )
            dirnames.remove("session-proposals")
        for filename in sorted(filenames):
            if any(pattern.fullmatch(filename) for pattern in LEGACY_LIVE_FILE_PATTERNS):
                path = current_path / filename
                errors.append(
                    f"{path}: retired live workflow artifact; move it under "
                    "notes/history"
                )


def validate_resume_semantics(idea_root: Path, warnings: list[str]) -> None:
    """Warn conservatively when both resume files expose conflicting phases."""

    current_path = idea_root / "notes" / "CURRENT.md"
    state_path = idea_root / "notes" / "project-state.md"
    if not current_path.is_file() or not state_path.is_file():
        return

    current_lines = current_path.read_text(encoding="utf-8").splitlines()
    current_phase = _current_fields(current_lines).get("phase")
    if not current_phase:
        return

    state_phase = None
    for line in state_path.read_text(encoding="utf-8").splitlines()[:100]:
        match = PROJECT_STATE_PHASE_RE.match(line)
        if match:
            state_phase = match.group(1).strip()
            break
    if not state_phase:
        return

    normalize = lambda value: re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if normalize(current_phase) != normalize(state_phase):
        warnings.append(
            f"{current_path}: phase {current_phase!r} conflicts with "
            f"{state_path.name} phase {state_phase!r}; resolve authority before resuming"
        )


def _topic_root_for_idea(idea_root: Path) -> Path | None:
    for candidate in (idea_root, *idea_root.parents):
        if (candidate / "ideas" / "registry.yaml").is_file():
            return candidate
    return None


def validate_registry_identity(
    idea_root: Path, errors: list[str], warnings: list[str]
) -> bool:
    """Validate scoped registry identity and return whether state is required."""

    topic_root = _topic_root_for_idea(idea_root)
    if topic_root is None:
        warnings.append(f"{idea_root}: no enclosing ideas/registry.yaml")
        return False
    if yaml is None:
        errors.append("PyYAML is required to validate ideas/registry.yaml")
        return False
    registry_path = topic_root / "ideas" / "registry.yaml"
    try:
        payload = yaml.safe_load(registry_path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"{registry_path}: invalid or unreadable registry ({exc})")
        return False
    entries = payload.get("ideas")
    if not isinstance(entries, list):
        errors.append(f"{registry_path}: ideas must be a list")
        return False

    active_status_ids = {
        str(entry.get("id", ""))
        for entry in entries
        if isinstance(entry, dict)
        and str(entry.get("status", "")).strip().lower() == "active"
    }
    active_pointer = payload.get("active_id")
    if active_pointer is None and active_status_ids:
        errors.append(
            f"{registry_path}: active_id is null but entries have status 'active': "
            f"{', '.join(sorted(active_status_ids))}"
        )
    elif active_pointer is not None and active_status_ids != {str(active_pointer)}:
        errors.append(
            f"{registry_path}: status 'active' must belong only to active_id "
            f"{active_pointer!r}; found {', '.join(sorted(active_status_ids)) or 'none'}"
        )

    matches: list[tuple[dict[str, object], str]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        canonical = entry.get("canonical_dir")
        if not isinstance(canonical, str) or not canonical:
            continue
        try:
            resolved = (topic_root / canonical).resolve(strict=True)
        except (FileNotFoundError, OSError):
            continue
        if resolved == idea_root.resolve():
            matches.append((entry, canonical))
    if len(matches) != 1:
        warnings.append(
            f"{idea_root}: expected one registry entry for canonical root; found {len(matches)}"
        )
        return False

    entry, canonical = matches[0]
    idea_id = str(entry.get("id", ""))
    if not re.fullmatch(r"i\d{3,}", idea_id):
        errors.append(f"{registry_path}: invalid registered idea ID {idea_id!r}")
    idea_md = idea_root / "idea.md"
    if not idea_md.is_file() or not idea_md.read_text(encoding="utf-8").strip():
        errors.append(f"{idea_md}: missing or empty registered idea definition")

    status = str(entry.get("status", "")).strip().lower()
    required = status in ACTIVE_LIFECYCLE_STATUSES
    if payload.get("active_id") == idea_id:
        required = True
        if payload.get("active_entry") != canonical:
            errors.append(
                f"{registry_path}: active_entry must mirror canonical_dir {canonical!r}"
            )
    return required


def _section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    parsed: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            parsed[key.strip()] = value.strip().strip("\"'")
    return parsed


def validate_skill_policy(repo_root: Path, errors: list[str]) -> None:
    skills_root = repo_root / "workflow" / "skills"
    for path in sorted(skills_root.glob("*/*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        metadata = _frontmatter(text)
        name = path.parent.name
        if metadata.get("name") != name:
            errors.append(f"{path}: frontmatter name must be {name!r}")
        if not metadata.get("description"):
            errors.append(f"{path}: missing frontmatter description")
        if not re.search(r"^## Produce\n", text, flags=re.MULTILINE):
            errors.append(f"{path}: missing ## Produce section")
        elif "`" not in _section(text, "Produce"):
            errors.append(f"{path}: ## Produce must name an artifact in backticks")

        agent_yaml = path.parent / "agents" / "openai.yaml"
        if not agent_yaml.exists():
            errors.append(f"{agent_yaml}: missing")
        else:
            agent_text = agent_yaml.read_text(encoding="utf-8")
            if f"${name}" not in agent_text:
                errors.append(f"{agent_yaml}: default prompt must reference ${name}")

        for label, pattern in LEGACY_SKILL_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{path}: contains retired {label}")


def main() -> int:
    args = parse_args()
    idea_root = Path(args.idea).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    errors: list[str] = []
    warnings: list[str] = []

    try:
        relative_parts = idea_root.relative_to(repo_root).parts
    except ValueError:
        relative_parts = ()
    required_state = (
        validate_registry_identity(idea_root, errors, warnings)
        if "ideas" in relative_parts
        else False
    )
    has_resume_state = any(
        (idea_root / "notes" / filename).is_file()
        for filename in ("CURRENT.md", "project-state.md")
    )
    strict_state = required_state or has_resume_state
    validate_capabilities(idea_root, errors)
    validate_current_md(
        idea_root,
        errors,
        warnings,
        required=strict_state,
        allowed_root=repo_root,
    )
    validate_project_state(
        idea_root, errors, warnings, required=strict_state
    )
    validate_todo(idea_root, errors)
    validate_live_legacy_artifacts(idea_root, errors)
    validate_resume_semantics(idea_root, warnings)
    validate_skill_policy(repo_root, errors)

    for warning in warnings:
        print(f"WARN {warning}")
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)

    if errors:
        return 1
    print("OK  lightweight research workflow validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
