#!/usr/bin/env python3
"""Lint skill-catalog.json against the actual SKILL.md files on disk.

Checks:
  E1 - Every skill directory in the selected skill root has a catalog entry.
  E2 - Every catalog entry has a SKILL.md at its stated path.
  E3 - Open References in SKILL.md point to existing relative files.
  E4 - Every catalog part field uses the controlled slug vocabulary.
  E5 - Retired workflow-state artifacts are absent from live Skills.
  E6 - Retired machine-routing fields, Handoff sections, and routing references
       are absent.
  W1 - skill-output-map.md artifact tokens drifted from SKILL.md Produce section
       (keyword check only — not a hard failure).
  W2 - SKILL.md contains known stale hardcoded paper workspace paths.

Usage:
  python3 lint_skill_catalog.py [--catalog PATH] [--skills-root PATH]
  python3 lint_skill_catalog.py --all
"""

import argparse
import json
import os
import re
import sys

SKILLS_BASE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "skills")
)
RESEARCH_ROOT = os.path.abspath(os.path.join(SKILLS_BASE, "..", ".."))
CATALOG_PATH = os.path.join(SKILLS_BASE, "_shared", "skill-catalog.json")
OUTPUT_MAP_PATH = os.path.join(SKILLS_BASE, "_shared", "skill-output-map.md")
PAPER_WRITING_DIR = os.path.join(SKILLS_BASE, "paper-writing")
FORBIDDEN_HARDCODED_PATHS = [
    ("paper/finish-report.md", "<paper-dir>/finish-report.md"),
    ("paper/review-log.md", "<paper-dir>/review-log.md"),
    ("paper/submission-checklist.md", "<paper-dir>/submission-checklist.md"),
    ("paper/tex-profile.json", "<paper-dir>/tex-profile.json"),
    ("paper/style-audit.md", "<paper-dir>/style-audit.md"),
    ("paper/INVARIANTS.md", "<paper-dir>/INVARIANTS.md"),
]
RETIRED_WORKFLOW_ARTIFACT_MARKERS = (
    "## handoff",
    "execution-entry.md",
    "handoff.md",
    "idea-spec.md",
    "idea-spec.provenance.json",
    "ideation-entry.md",
    "plan-tree.md",
    "promotion-gate-result",
    "research-pipeline",
    "review-state.json",
    "session-proposals",
    "writing-entry.md",
    "handoff-rules.md",
    "workflow-map.md",
)
VALID_PARTS = {"research-ideation", "experiment-execution", "paper-writing", "standalone"}


def load_catalog(path):
    with open(path) as f:
        return json.load(f)


def resolve_catalog_path(path):
    """Resolve absolute personal paths and portable checkout-relative paths."""
    if os.path.isabs(path):
        return os.path.normpath(path)
    return os.path.normpath(os.path.join(RESEARCH_ROOT, path))


def skill_dirs(root):
    """Return {name: skill_md_path} for every directory under root."""
    result = {}
    for entry in sorted(os.listdir(root)):
        full = os.path.join(root, entry)
        if os.path.isdir(full):
            skill_md = os.path.join(full, "SKILL.md")
            result[entry] = skill_md
    return result


def all_skill_roots():
    """Return all top-level skill part directories under workflow/skills/."""
    roots = []
    for entry in sorted(os.listdir(SKILLS_BASE)):
        full = os.path.join(SKILLS_BASE, entry)
        if entry.startswith("_") or not os.path.isdir(full):
            continue
        roots.append(full)
    return roots


def catalog_by_name(catalog):
    return {e["name"]: e for e in catalog}


def parse_frontmatter(skill_md_path):
    """Return frontmatter keys for a SKILL.md file, or {} when absent."""
    if not os.path.exists(skill_md_path):
        return {}
    with open(skill_md_path) as f:
        content = f.read()
    if not content.startswith("---\n"):
        return {}
    end = content.find("\n---\n", 4)
    if end == -1:
        return {}
    result = {}
    for line in content[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def extract_produce_artifacts(skill_md_path):
    """Return list of artifact path tokens from Produce section of a SKILL.md."""
    if not os.path.exists(skill_md_path):
        return []
    with open(skill_md_path) as f:
        content = f.read()
    m = re.search(r"## Produce\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    if not m:
        return []
    artifacts = []
    for line in m.group(1).splitlines():
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        token = stripped[2:].strip()
        # Strip "Optional " prefix (case-insensitive)
        token = re.sub(r"^[Oo]ptional\s+", "", token)
        # Strip mode labels used by skills with mutually exclusive output paths.
        token = re.sub(r"^Mode\s+[A-Z]:\s+", "", token)
        # Strip surrounding backticks
        token = token.strip("`")
        # Take text before description separators
        token = re.split(r"\s+[—–]\s+|\s+when\s+|\s+\(|\s+for\s+|\s+unless\s+", token)[0]
        token = token.strip().strip("`")
        # Keep only tokens that look like file paths (contain / or a file
        # extension). Directory paths may contain spaces (for example
        # `source md文档/`), but prose fragments with spaces should still be
        # filtered out.
        path_like = "/" in token or re.search(r"\.\w{1,5}$", token)
        space_safe = " " not in token or token.endswith("/")
        if path_like and space_safe:
            artifacts.append(token)
    return artifacts


def extract_open_reference_paths(skill_md_path):
    """Return checkable relative path refs from Open References section."""
    if not os.path.exists(skill_md_path):
        return []
    with open(skill_md_path) as f:
        content = f.read()
    m = re.search(
        r"## Open References Only As Needed\n(.*?)(?=\n## |\Z)",
        content,
        re.DOTALL,
    )
    if not m:
        return []
    refs = []
    for ref in re.findall(r"`([^`]+)`", m.group(1)):
        if ref.startswith("$") or "://" in ref or ref.startswith("<"):
            continue
        # Check concrete documentation/tool references. Ignore artifact names
        # like `status.json` or workspace placeholders like `outputs/`.
        if (
            ref.startswith(".")
            or ref.startswith("references/")
            or ref.startswith("scripts/")
        ):
            refs.append(ref)
    return refs


def hardcoded_path_hits(skill_md_path):
    """Return known stale hardcoded paper workspace path hits."""
    if not os.path.exists(skill_md_path):
        return []
    with open(skill_md_path) as f:
        lines = f.readlines()
    hits = []
    for lineno, line in enumerate(lines, 1):
        for stale, replacement in FORBIDDEN_HARDCODED_PATHS:
            if stale in line:
                hits.append((lineno, stale, replacement))
    return hits


def retired_workflow_artifact_hits(skill_md_path):
    """Return retired workflow-state artifact mentions in a live Skill."""
    if not os.path.exists(skill_md_path):
        return []
    with open(skill_md_path) as f:
        lines = f.readlines()
    hits = []
    for lineno, line in enumerate(lines, 1):
        normalized = line.casefold()
        for artifact in RETIRED_WORKFLOW_ARTIFACT_MARKERS:
            if artifact in normalized:
                hits.append((lineno, artifact))
    return hits


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", default=CATALOG_PATH)
    parser.add_argument("--skills-root", default=PAPER_WRITING_DIR)
    parser.add_argument(
        "--all",
        action="store_true",
        help="scan every top-level skill part under workflow/skills/",
    )
    args = parser.parse_args()

    catalog = load_catalog(args.catalog)
    by_name = catalog_by_name(catalog)
    scan_roots = all_skill_roots() if args.all else [args.skills_root]
    dirs = {}
    for root in scan_roots:
        dirs.update(skill_dirs(root))

    errors = []
    warnings = []

    # E1: every skill directory has a catalog entry
    for name in dirs:
        if name not in by_name:
            errors.append(f"E1  skill dir '{name}' has no catalog entry")

    # E2: every catalog entry path exists
    for entry in catalog:
        path = entry.get("path", "")
        resolved_path = resolve_catalog_path(path) if path else ""
        if path and not os.path.exists(resolved_path):
            errors.append(
                f"E2  catalog entry '{entry['name']}' path not found: {path}"
            )

    # E2b: every catalog entry carries the generated leaf-Skill metadata.
    required_fields = ("part", "category", "consumes", "produces")
    for entry in catalog:
        missing = [field for field in required_fields if field not in entry]
        if missing:
            errors.append(
                f"E2b  catalog entry '{entry['name']}' missing fields: {', '.join(missing)}"
            )

    # E2c: SKILL.md frontmatter should carry the stable generated identity.
    for name, skill_md in dirs.items():
        if not os.path.exists(skill_md):
            continue
        frontmatter = parse_frontmatter(skill_md)
        missing = [field for field in ("name", "description") if not frontmatter.get(field)]
        if missing:
            errors.append(
                f"E2c  '{name}' SKILL.md missing required frontmatter: {', '.join(missing)}"
            )

    # E5: catalog part values should be stable slugs, not display labels.
    for entry in catalog:
        part = entry.get("part")
        if part not in VALID_PARTS:
            errors.append(
                f"E5  catalog entry '{entry['name']}' has invalid part '{part}'; "
                f"expected one of: {', '.join(sorted(VALID_PARTS))}"
            )

    # E6: retired workflow-state and routing surfaces must not return.
    for name, skill_md in dirs.items():
        if name not in by_name:
            continue
        for lineno, artifact in retired_workflow_artifact_hits(skill_md):
            errors.append(
                f"E6  '{name}' line {lineno} uses retired workflow surface "
                f"'{artifact}'; remove it"
            )

    # E6: machine routing was retired; leaf Skills are triggered directly.
    for entry in catalog:
        for field in ("next_skills", "routes_to"):
            if field in entry:
                errors.append(
                    f"E6  catalog entry '{entry['name']}' uses retired router field '{field}'"
                )

    # E3: Open References should point to existing relative files.
    for name, skill_md in dirs.items():
        if name not in by_name:
            continue
        for ref in extract_open_reference_paths(skill_md):
            resolved = os.path.normpath(os.path.join(os.path.dirname(skill_md), ref))
            if not os.path.exists(resolved):
                errors.append(
                    f"E4  '{name}' Open References path not found: {ref} -> {resolved}"
                )

    # W1: Produce artifact tokens in SKILL.md not found in skill-output-map.md
    output_map_content = ""
    if os.path.exists(OUTPUT_MAP_PATH):
        with open(OUTPUT_MAP_PATH) as f:
            output_map_content = f.read()
    for name, skill_md in dirs.items():
        if name not in by_name:
            continue
        for artifact in extract_produce_artifacts(skill_md):
            if artifact not in output_map_content:
                warnings.append(
                    f"W1  '{name}' Produce artifact '{artifact}' not in skill-output-map.md"
                )

    # W2: known stale hardcoded paper workspace paths.
    for name, skill_md in dirs.items():
        if name not in by_name:
            continue
        for lineno, stale, replacement in hardcoded_path_hits(skill_md):
            warnings.append(
                f"W2  '{name}' line {lineno} uses '{stale}'; prefer '{replacement}'"
            )

    # Report
    ok = not errors and not warnings
    if errors:
        print("ERRORS")
        for e in errors:
            print(f"  {e}")
    if warnings:
        print("WARNINGS")
        for w in warnings:
            print(f"  {w}")
    if ok:
        print("OK  skill-catalog lint passed")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
