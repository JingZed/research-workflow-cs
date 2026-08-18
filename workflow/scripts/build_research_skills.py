#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


WORKFLOW_ROOT = Path(__file__).resolve().parent.parent
RESEARCH_ROOT = WORKFLOW_ROOT.parent
SKILLS_DIR = WORKFLOW_ROOT / "skills"
SHARED_DIR = SKILLS_DIR / "_shared"
CATALOG_PATH = SHARED_DIR / "skill-catalog.json"
OUTPUT_MAP_PATH = SHARED_DIR / "skill-output-map.md"
MAX_RESEARCH_SKILLS = 40
MAX_TOTAL_ARTIFACT_REFS = 128
MAX_SKILL_BYTES = 16 * 1024
MAX_SKILL_LINES = 240
MAX_TOTAL_SKILL_BYTES = 240 * 1024
MAX_DESCRIPTION_CHARS = 480
MAX_REFERENCE_FILES = 30
MAX_REFERENCE_FILE_BYTES = 16 * 1024
MAX_TOTAL_REFERENCE_BYTES = 160 * 1024
MAX_SHORT_DESCRIPTION_CHARS = 64
FORBIDDEN_SKILL_SUFFIXES = ("-entry", "-router", "-gate")
FORBIDDEN_SKILL_NAMES = frozenset(
    {
        "auto-review-loop",
        "experiment-logbook-maintainer",
        "figure-spec-writer",
        "paper-contribution-framer",
        "paper-figure-art-director",
        "paper-figure-critic",
        "paper-review-loop",
        "paper-structure-parser",
        "project-state-summarizer",
        "reading-note-linker",
        "reading-question-generator",
        "research-gap-finder",
        "research-pipeline",
        "submission-package-checker",
        "topic-map-builder",
    }
)
RETIRED_ROUTING_REFERENCES = ("handoff-rules.md", "workflow-map.md")
FORBIDDEN_SKILL_ARTIFACTS = frozenset(
    {
        "ideation-entry.md",
        "experiments/execution-entry.md",
        "drafts/writing-entry.md",
        "notes/research-pipeline.md",
        "experiments/plans/milestone-plan.md",
        "notes/weekly-review.md",
        "notes/deadline-plan.md",
        "TODO.md",
        "notes/TODO.md",
    }
)
FORBIDDEN_SKILL_ARTIFACT_BASENAMES = frozenset(
    {
        "handoff.md",
        "idea-spec.md",
        "idea-spec.provenance.json",
        "plan-tree.md",
        "review-state.json",
    }
)
NON_ARTIFACT_CODE_SPANS = frozenset(
    {"preview", "apply", "READY", "PASS", "BLOCKED", "INCOMPLETE"}
)
ARTIFACT_SUFFIX_RE = re.compile(
    r"\.(?:bib|csv|ipynb|jpeg|jpg|json|jsonl|log|md|pdf|png|pptx|py|svg|tex|"
    r"tsv|txt|yaml|yml|zip)$",
    re.IGNORECASE,
)
EXPLICIT_ONLY_DESCRIPTION_RE = re.compile(
    r"\bexplicit[- ]only\b|"
    r"\b(?:trigger|use|invoke)\s+only\s+when\s+the\s+user\s+explicitly\b",
    re.IGNORECASE,
)

PART_SLUG_TO_NAME = {
    "research-ideation": "Research Ideation",
    "experiment-execution": "Experiment Execution",
    "paper-writing": "Paper Writing",
    "standalone": "Standalone Utility Skills",
}

PART_ORDER = {
    "research-ideation": 0,
    "experiment-execution": 1,
    "paper-writing": 2,
    "standalone": 3,
}

VALID_CATEGORIES_BY_PART = {
    "research-ideation": {
        "Literature Discovery",
        "Literature Acquisition",
        "Literature Intake",
        "Single-Paper Reading",
        "Multi-Paper Synthesis",
        "Flow Support",
    },
    "experiment-execution": {
        "Study Design",
        "Execution and Results",
    },
    "paper-writing": {
        "Writing and Submission",
    },
    "standalone": {"Standalone Utility"},
}

SHARED_ARTIFACT_DESCRIPTIONS = {
    "notes/CURRENT.md": (
        "`idea-backlog-manager` at activation; thereafter the active artifact "
        "owner under the fixed resume contract"
    ),
    "notes/project-state.md": (
        "`idea-backlog-manager` at activation; thereafter the active artifact "
        "owner when scientific state materially changes"
    ),
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def catalog_skill_path(skill_md: Path) -> str:
    """Render an install-aware path for generated discovery metadata.

    The personal Research workspace projects the central source through a
    symlink, so its catalog keeps the resolved central path. A distributable
    checkout materializes ``workflow/skills`` and therefore uses a portable
    path relative to the checkout root.
    """
    if SKILLS_DIR.is_symlink():
        return str(skill_md.resolve())
    try:
        return skill_md.resolve().relative_to(RESEARCH_ROOT.resolve()).as_posix()
    except ValueError as exc:
        raise SystemExit(
            f"Skill path escapes the Research root: {skill_md.resolve()}"
        ) from exc


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        inner = value[1:-1]
        return inner.replace('\\"', '"').replace("\\'", "'").replace("\\\\", "\\")
    return value


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    frontmatter = text[4:end]
    result: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = unquote(value)
    return result


def section_lines(text: str, heading: str) -> list[str]:
    pattern = rf"^## {re.escape(heading)}\n"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        return []
    start = match.end()
    next_match = re.search(r"^## ", text[start:], flags=re.MULTILINE)
    end = start + next_match.start() if next_match else len(text)
    return text[start:end].strip().splitlines()


def parse_bullets(lines: list[str]) -> list[str]:
    items: list[str] = []
    current: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            if current:
                items.append(" ".join(current))
            current = [stripped[2:].strip()]
        elif current and stripped:
            current.append(stripped)
    if current:
        items.append(" ".join(current))
    return items


def extract_code_spans(text: str) -> list[str]:
    return re.findall(r"`([^`]+)`", text)


def unique_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def is_artifact_ref(value: str) -> bool:
    value = value.strip()
    if not value or value in NON_ARTIFACT_CODE_SPANS:
        return False
    return "/" in value or value.startswith(".") or bool(ARTIFACT_SUFFIX_RE.search(value))


def parse_artifact_refs(items: list[str]) -> list[str]:
    refs: list[str] = []
    for item in items:
        refs.extend(span for span in extract_code_spans(item) if is_artifact_ref(span))
    return unique_keep_order(refs)


def parse_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def description_requires_explicit_invocation(description: str) -> bool:
    return bool(EXPLICIT_ONLY_DESCRIPTION_RE.search(description))


def is_forbidden_artifact(ref: str) -> bool:
    if ref in FORBIDDEN_SKILL_ARTIFACTS:
        return True
    normalized = ref.rstrip("/")
    basename = normalized.rsplit("/", 1)[-1].casefold()
    if basename in FORBIDDEN_SKILL_ARTIFACT_BASENAMES:
        return True
    if "session-proposals" in normalized.casefold().split("/"):
        return True
    return bool(
        re.fullmatch(r"research-pipeline(?: .*)?\.md", basename, re.IGNORECASE)
        or re.fullmatch(r"promotion-gate-result(?:\..+)?", basename, re.IGNORECASE)
        or re.fullmatch(r"(?:ideation|execution|writing)-entry\.md", basename, re.IGNORECASE)
    )


def load_existing_catalog() -> tuple[dict[str, dict[str, object]], dict[str, int]]:
    if not CATALOG_PATH.exists():
        return {}, {}
    data = json.loads(read_text(CATALOG_PATH))
    by_name = {entry["name"]: entry for entry in data}
    order = {entry["name"]: idx for idx, entry in enumerate(data)}
    return by_name, order


def infer_category(name: str, part: str, existing: dict[str, object] | None) -> str:
    if part == "standalone":
        return "Standalone Utility"
    if existing and isinstance(existing.get("category"), str):
        existing_category = existing["category"]
        if existing_category in VALID_CATEGORIES_BY_PART[part]:
            return existing_category
    if part == "research-ideation":
        return "Flow Support"
    if part == "experiment-execution":
        return "Execution and Results"
    return "Writing and Submission"


def parse_skill(skill_md: Path, existing: dict[str, object] | None) -> dict[str, object]:
    text = read_text(skill_md)
    frontmatter = parse_frontmatter(text)
    name = frontmatter.get("name", skill_md.parent.name)
    description = frontmatter.get("description", "")
    slug = skill_md.parents[1].name
    part = slug
    title = parse_title(text, name.replace("-", " ").title())
    consumes = parse_bullets(section_lines(text, "Consume"))
    produces = parse_bullets(section_lines(text, "Produce"))
    routing_text = "\n".join(
        section_lines(text, "Workflow")
        + section_lines(text, "Stop Conditions")
        + section_lines(text, "Boundaries")
    )
    authority_text = "\n".join(
        section_lines(text, "Consume") + section_lines(text, "Workflow")
    )
    reference_files = sorted(
        path
        for path in (skill_md.parent / "references").glob("**/*")
        if path.is_file()
    )
    category = infer_category(name, part, existing)
    return {
        "part": part,
        "category": category,
        "name": name,
        "title": title,
        "description": description,
        "path": catalog_skill_path(skill_md),
        "consumes": consumes,
        "produces": produces,
        "consume_refs": parse_artifact_refs(consumes),
        "produce_refs": parse_artifact_refs(produces),
        "_text": text,
        "_skill_path": str(skill_md.resolve()),
        "_routing_text": routing_text,
        "_authority_text": authority_text,
        "_skill_bytes": len(text.encode("utf-8")),
        "_skill_lines": len(text.splitlines()),
        "_reference_files": [str(path) for path in reference_files],
        "_reference_bytes": sum(path.stat().st_size for path in reference_files),
    }


def discover_skills() -> list[dict[str, object]]:
    existing_by_name, existing_order = load_existing_catalog()
    discovered: list[dict[str, object]] = []
    for skill_md in sorted(SKILLS_DIR.glob("*/*/SKILL.md")):
        if skill_md.parent.parent.name == "_shared":
            continue
        existing = existing_by_name.get(skill_md.parent.name)
        discovered.append(parse_skill(skill_md, existing))

    def sort_key(entry: dict[str, object]) -> tuple[int, int, str]:
        name = entry["name"]
        return (
            PART_ORDER[entry["part"]],
            existing_order.get(name, 10_000),
            name,
        )

    discovered.sort(key=sort_key)
    return discovered


def skill_architecture_errors(skills: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    if len(skills) > MAX_RESEARCH_SKILLS:
        errors.append(
            f"Research Skill count is {len(skills)}, above the fixed budget "
            f"of {MAX_RESEARCH_SKILLS}"
        )

    total_artifact_refs = sum(len(skill.get("produce_refs", [])) for skill in skills)
    if total_artifact_refs > MAX_TOTAL_ARTIFACT_REFS:
        errors.append(
            f"Research Skill artifact outputs total {total_artifact_refs}, above "
            f"the fixed budget of {MAX_TOTAL_ARTIFACT_REFS}"
        )
    total_skill_bytes = sum(int(skill.get("_skill_bytes", 0)) for skill in skills)
    if total_skill_bytes > MAX_TOTAL_SKILL_BYTES:
        errors.append(
            f"Research SKILL.md text totals {total_skill_bytes} bytes, above the "
            f"fixed budget of {MAX_TOTAL_SKILL_BYTES}"
        )
    reference_files = [
        Path(path)
        for skill in skills
        for path in skill.get("_reference_files", [])
        if isinstance(path, str)
    ]
    if len(reference_files) > MAX_REFERENCE_FILES:
        errors.append(
            f"Research Skill references total {len(reference_files)} files, above "
            f"the fixed budget of {MAX_REFERENCE_FILES}"
        )
    total_reference_bytes = sum(path.stat().st_size for path in reference_files)
    if total_reference_bytes > MAX_TOTAL_REFERENCE_BYTES:
        errors.append(
            f"Research Skill references total {total_reference_bytes} bytes, above "
            f"the fixed budget of {MAX_TOTAL_REFERENCE_BYTES}"
        )

    for skill in skills:
        name = str(skill["name"])
        for router_field in ("next_skills", "routes_to"):
            if router_field in skill:
                errors.append(
                    f"{name}: retired router field {router_field!r}; trigger leaf "
                    "Skills directly instead of generating a route graph"
                )
        if name in FORBIDDEN_SKILL_NAMES or name.endswith(FORBIDDEN_SKILL_SUFFIXES):
            errors.append(
                f"{name}: meta-workflow Skill names are retired; extend a leaf "
                "Skill or AGENTS.md instead"
            )
        text = str(skill.get("_text", ""))
        if re.search(r"^## Handoff\s*$", text, flags=re.MULTILINE):
            errors.append(
                f"{name}: Handoff sections are retired; return the requested "
                "artifact and let the next task trigger its leaf Skill directly"
            )
        for reference in RETIRED_ROUTING_REFERENCES:
            if reference in text:
                errors.append(
                    f"{name}: retired routing reference {reference!r}; use the "
                    "nearest AGENTS.md and direct leaf-Skill triggers"
                )

        skill_bytes = int(skill.get("_skill_bytes", 0))
        skill_lines = int(skill.get("_skill_lines", 0))
        description = str(skill.get("description", ""))
        if skill_bytes > MAX_SKILL_BYTES:
            errors.append(
                f"{name}: SKILL.md is {skill_bytes} bytes; maximum is {MAX_SKILL_BYTES}"
            )
        if skill_lines > MAX_SKILL_LINES:
            errors.append(
                f"{name}: SKILL.md is {skill_lines} lines; maximum is {MAX_SKILL_LINES}"
            )
        if len(description) > MAX_DESCRIPTION_CHARS:
            errors.append(
                f"{name}: description is {len(description)} characters; maximum "
                f"is {MAX_DESCRIPTION_CHARS}"
            )
        for raw_path in skill.get("_reference_files", []):
            reference_path = Path(str(raw_path))
            if reference_path.stat().st_size > MAX_REFERENCE_FILE_BYTES:
                errors.append(
                    f"{name}: reference {reference_path.name} is "
                    f"{reference_path.stat().st_size} bytes; maximum is "
                    f"{MAX_REFERENCE_FILE_BYTES}"
                )

        for ref in list(skill.get("produce_refs", [])) + list(skill.get("consume_refs", [])):
            if is_forbidden_artifact(str(ref)):
                errors.append(
                    f"{name}: meta-state artifact {ref!r} must not be produced or "
                    "used as workflow authority"
                )
        authority_text = str(skill.get("_authority_text", ""))
        for ref in FORBIDDEN_SKILL_ARTIFACTS:
            if ref in authority_text:
                errors.append(
                    f"{name}: meta-state artifact {ref!r} appears in Consume/Workflow"
                )
        authority_lower = authority_text.casefold()
        for basename in FORBIDDEN_SKILL_ARTIFACT_BASENAMES:
            if basename in authority_lower:
                errors.append(
                    f"{name}: meta-state artifact {basename!r} appears in Consume/Workflow"
                )
        for ref in unique_keep_order(extract_code_spans(authority_text)):
            if is_forbidden_artifact(ref):
                errors.append(
                    f"{name}: meta-state artifact {ref!r} appears in Consume/Workflow"
                )
        for line in str(skill.get("_routing_text", "")).splitlines():
            if re.search(r"\b(?:re-?run|repeat)\s+this skill\b", line, re.IGNORECASE) and not re.search(
                r"\b(?:do not|never|without)\b", line, re.IGNORECASE
            ):
                errors.append(f"{name}: unbounded self-rerun instruction is forbidden")

    return errors


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def parse_agent_yaml(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    result: dict[str, str] = {}
    for raw_line in read_text(path).splitlines():
        line = raw_line.rstrip()
        if not line.startswith("  ") or ":" not in line:
            continue
        key, value = line.strip().split(":", 1)
        result[key] = unquote(value)
    return result


def render_agent_yaml(skill: dict[str, object], existing: dict[str, str] | None = None) -> str:
    existing = existing or {}
    default_prompt = existing.get("default_prompt", "")
    if f"${skill['name']}" not in default_prompt:
        default_prompt = f"Use ${skill['name']} to help with this task."
    short_description = existing.get("short_description") or str(skill["title"])
    lines = [
        "interface:",
        f"  display_name: {yaml_quote(str(skill['title']))}",
        f"  short_description: {yaml_quote(short_description)}",
        f"  default_prompt: {yaml_quote(default_prompt)}",
    ]
    allow_implicit_invocation = existing.get("allow_implicit_invocation")
    if allow_implicit_invocation in {"true", "false"}:
        lines.extend(
            [
                "policy:",
                f"  allow_implicit_invocation: {allow_implicit_invocation}",
            ]
        )
    lines.append("")
    return "\n".join(lines)


def write_agents_yaml(skill: dict[str, object]) -> None:
    agents_dir = Path(str(skill["_skill_path"])).parent / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    yaml_path = agents_dir / "openai.yaml"
    existing = parse_agent_yaml(yaml_path)
    content = render_agent_yaml(skill, existing)
    if not yaml_path.exists() or read_text(yaml_path) != content:
        yaml_path.write_text(content, encoding="utf-8")


def render_skill_catalog(skills: list[dict[str, object]]) -> str:
    payload = []
    for skill in skills:
        record = {
            key: value
            for key, value in skill.items()
            if key not in {"consume_refs", "produce_refs"} and not key.startswith("_")
        }
        agents_yaml = Path(str(skill["_skill_path"])).parent / "agents" / "openai.yaml"
        agent_meta = parse_agent_yaml(agents_yaml)
        record["short_description"] = agent_meta.get(
            "short_description", str(skill["title"])
        )
        payload.append(record)
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def write_skill_catalog(skills: list[dict[str, object]]) -> None:
    CATALOG_PATH.write_text(render_skill_catalog(skills), encoding="utf-8")


def validate_skills(skills: list[dict[str, object]]) -> dict[str, list[str]]:
    errors = skill_architecture_errors(skills)
    owners: dict[str, list[str]] = {}

    for skill in skills:
        name = str(skill["name"])
        produces = skill["produces"]
        produce_refs = skill["produce_refs"]
        if not produces:
            errors.append(f"{name}: missing `## Produce` bullets")
            continue
        if not produce_refs:
            errors.append(f"{name}: `## Produce` has no canonical artifact paths in backticks")
        agents_yaml = Path(str(skill["_skill_path"])).parent / "agents" / "openai.yaml"
        if agents_yaml.exists():
            parsed = parse_agent_yaml(agents_yaml)
            if parsed.get("display_name") != skill["title"]:
                errors.append(f"{name}: agents/openai.yaml display_name is stale")
            if f"${name}" not in parsed.get("default_prompt", ""):
                errors.append(f"{name}: agents/openai.yaml default_prompt does not reference the current skill name")
            short_description = parsed.get("short_description", "")
            if len(short_description) > MAX_SHORT_DESCRIPTION_CHARS:
                errors.append(
                    f"{name}: agents/openai.yaml short_description is "
                    f"{len(short_description)} characters; maximum is "
                    f"{MAX_SHORT_DESCRIPTION_CHARS}"
                )
            explicit_description = description_requires_explicit_invocation(
                str(skill.get("description", ""))
            )
            implicit_policy = parsed.get("allow_implicit_invocation")
            if explicit_description and implicit_policy != "false":
                errors.append(
                    f"{name}: description declares explicit-only invocation but "
                    "agents/openai.yaml does not set "
                    "allow_implicit_invocation: false"
                )
            if implicit_policy == "false" and not explicit_description:
                errors.append(
                    f"{name}: agents/openai.yaml disables implicit invocation but "
                    "the description does not declare an explicit-only trigger"
                )
        for ref in produce_refs:
            owners.setdefault(ref, []).append(name)

    for ref, ref_owners in sorted(owners.items()):
        if len(ref_owners) > 1:
            joined = ", ".join(sorted(ref_owners))
            if ref not in SHARED_ARTIFACT_DESCRIPTIONS:
                errors.append(f"{ref}: multiple owning skills ({joined})")

    if errors:
        details = "\n".join(f"- {error}" for error in errors)
        raise SystemExit(f"Skill validation failed:\n{details}")

    return owners


def render_output_map(
    skills: list[dict[str, object]], owners: dict[str, list[str]]
) -> str:
    lines = [
        "# Skill Output Map",
        "",
        "This file is generated from each skill's `## Produce` section. Use it as the owner map for what a skill may create and where it should write it.",
        "",
        "- Only create artifacts listed under the triggered skill's `## Produce` section.",
        "- `## Consume` entries are inputs, not a checklist of files to create.",
        "- Optional bullets stay optional unless their condition is true or the user requests that output.",
        "",
        "## By Skill",
        "",
    ]

    for part in ("research-ideation", "experiment-execution", "paper-writing", "standalone"):
        lines.append(f"### {PART_SLUG_TO_NAME[part]}")
        for skill in [skill for skill in skills if skill["part"] == part]:
            lines.append(f"- `{skill['name']}`")
            for item in skill["produces"]:
                lines.append(f"  - {item}")
        lines.append("")

    lines.extend(
        [
            "## By Artifact",
            "",
            "Note: `presentations/<deck-id>/...` paths are relative to the standalone output root selected by `paper-presentation-builder`; they are not a default idea-root contract.",
            "",
        ]
    )
    for ref in sorted(owners):
        if ref in SHARED_ARTIFACT_DESCRIPTIONS:
            lines.append(f"- `{ref}` -> {SHARED_ARTIFACT_DESCRIPTIONS[ref]}")
        else:
            owner = owners[ref][0]
            lines.append(f"- `{ref}` -> `{owner}`")

    return "\n".join(lines).rstrip() + "\n"


def write_output_map(skills: list[dict[str, object]], owners: dict[str, list[str]]) -> None:
    OUTPUT_MAP_PATH.write_text(render_output_map(skills, owners), encoding="utf-8")


def build() -> None:
    skills = discover_skills()
    for skill in skills:
        write_agents_yaml(skill)
    owners = validate_skills(skills)
    write_skill_catalog(skills)
    write_output_map(skills, owners)


if __name__ == "__main__":
    build()
