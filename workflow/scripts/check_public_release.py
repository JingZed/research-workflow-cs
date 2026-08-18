#!/usr/bin/env python3
"""Validate a materialized Research workflow release without mutating it."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = Path(__file__).resolve().parent
SKILLS_DIR = ROOT / "workflow" / "skills"
CATALOG_PATH = SKILLS_DIR / "_shared" / "skill-catalog.json"
OUTPUT_MAP_PATH = SKILLS_DIR / "_shared" / "skill-output-map.md"
AGENTS_PATH = ROOT / "AGENTS.md"
EXPECTED_SKILL_COUNT = 39
REQUIRED_LICENSE_FILES = (
    ROOT / "LICENSE",
    ROOT / "THIRD_PARTY_NOTICES.md",
    ROOT / "LICENSES" / "Auto-claude-code-research-in-sleep-MIT.txt",
)

PRIVATE_TEXT_PATTERNS = (
    "/" + "Users/",
    "Desktop/" + "research",
    "personal-" + "skills-src",
    "wang" + "jingzhe",
    "file:///" + "Users/",
    "C:\\" + "Users\\",
)
FORBIDDEN_NAMES = {
    ".DS_Store",
    ".env",
    "api_tokens.env",
    "mineru_api_token.txt",
    ".mineru_token",
}
FORBIDDEN_DIRS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
}
TEXT_SUFFIXES = {
    "",
    ".cfg",
    ".csv",
    ".env",
    ".ini",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".rst",
    ".toml",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}
SECRET_VALUE_RE = re.compile(
    r"(?im)^[A-Z][A-Z0-9_]*(?:API_KEY|TOKEN|SECRET|PASSWORD)\s*=\s*(.+?)\s*$"
)
TOKEN_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bgh[opusr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
)


def _within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _iter_release_files() -> Iterable[Path]:
    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts:
            continue
        yield path


def _is_placeholder(value: str) -> bool:
    normalized = value.strip().strip('"').strip("'")
    if not normalized:
        return True
    lowered = normalized.casefold()
    return (
        normalized.startswith("<") and normalized.endswith(">")
    ) or normalized.startswith("${") or any(
        marker in lowered
        for marker in ("replace-me", "your-key", "example", "placeholder")
    )


def scan_tree_errors() -> list[str]:
    errors: list[str] = []
    for path in _iter_release_files():
        relative = path.relative_to(ROOT).as_posix()
        if path.is_symlink():
            errors.append(f"symlink is forbidden in release: {relative}")
            continue
        if any(part in FORBIDDEN_DIRS for part in path.parts):
            errors.append(f"cache or dependency directory is forbidden: {relative}")
            continue
        if not path.is_file():
            continue
        if path.name in FORBIDDEN_NAMES or path.suffix == ".pyc":
            errors.append(f"credential or cache file is forbidden: {relative}")
            continue
        if path.suffix.casefold() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"declared text file is not UTF-8: {relative}")
            continue
        for pattern in PRIVATE_TEXT_PATTERNS:
            if pattern in text:
                errors.append(f"private path marker {pattern!r} in {relative}")
        for token_re in TOKEN_PATTERNS:
            if token_re.search(text):
                errors.append(f"credential-like token in {relative}")
        for match in SECRET_VALUE_RE.finditer(text):
            if not _is_placeholder(match.group(1)):
                errors.append(
                    f"non-placeholder secret assignment in {relative}: "
                    f"{match.group(0).split('=', 1)[0].strip()}"
                )
    return errors


def license_errors() -> list[str]:
    errors: list[str] = []
    for path in REQUIRED_LICENSE_FILES:
        if not path.is_file():
            errors.append(f"required license file is missing: {path.relative_to(ROOT)}")
    pending = sorted(ROOT.rglob("*_PENDING.md"))
    if pending:
        errors.append(
            "unresolved license marker remains: "
            + ", ".join(path.relative_to(ROOT).as_posix() for path in pending)
        )
    if errors:
        return errors

    project_license = (ROOT / "LICENSE").read_text(encoding="utf-8")
    for required in (
        "MIT License",
        "Copyright (c) 2026 Wang Jingzhe",
        "Permission is hereby granted",
    ):
        if required not in project_license:
            errors.append(f"project LICENSE is missing required text: {required}")

    upstream_license = REQUIRED_LICENSE_FILES[2].read_text(encoding="utf-8")
    for required in (
        "MIT License",
        "Copyright (c) 2026 wanshuiyin",
        "Permission is hereby granted",
    ):
        if required not in upstream_license:
            errors.append(f"upstream license is missing required text: {required}")

    notice = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    for required in (
        "workflow/scripts/arxiv_fetch.py",
        "wanshuiyin/Auto-claude-code-research-in-sleep",
        "LICENSES/Auto-claude-code-research-in-sleep-MIT.txt",
    ):
        if required not in notice:
            errors.append(f"third-party notice is missing required text: {required}")
    return errors


def load_build_module():
    module_path = SCRIPTS_DIR / "build_research_skills.py"
    spec = importlib.util.spec_from_file_location(
        "release_build_research_skills", module_path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def catalog_errors() -> list[str]:
    errors: list[str] = []
    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read generated catalog: {exc}"]
    if len(catalog) != EXPECTED_SKILL_COUNT:
        errors.append(
            f"catalog has {len(catalog)} Skills; release expects "
            f"{EXPECTED_SKILL_COUNT}"
        )
    names: set[str] = set()
    for entry in catalog:
        name = str(entry.get("name", ""))
        if not name:
            errors.append("catalog entry is missing name")
            continue
        if name in names:
            errors.append(f"duplicate catalog Skill name: {name}")
        names.add(name)
        raw_path = str(entry.get("path", ""))
        path = Path(raw_path)
        if not raw_path:
            errors.append(f"{name}: catalog path is empty")
            continue
        if path.is_absolute():
            errors.append(f"{name}: catalog path must be relative: {raw_path}")
            continue
        resolved = ROOT / path
        if not _within(resolved, ROOT):
            errors.append(f"{name}: catalog path escapes release root: {raw_path}")
        elif not resolved.is_file():
            errors.append(f"{name}: catalog path does not exist: {raw_path}")

    skill_files = sorted(SKILLS_DIR.glob("*/*/SKILL.md"))
    live_names = {path.parent.name for path in skill_files}
    if len(skill_files) != EXPECTED_SKILL_COUNT:
        errors.append(
            f"materialized tree has {len(skill_files)} Skills; release expects "
            f"{EXPECTED_SKILL_COUNT}"
        )
    if names != live_names:
        missing = sorted(live_names - names)
        extra = sorted(names - live_names)
        if missing:
            errors.append(f"catalog is missing live Skills: {', '.join(missing)}")
        if extra:
            errors.append(f"catalog has non-live Skills: {', '.join(extra)}")
    return errors


def generated_metadata_errors() -> list[str]:
    errors: list[str] = []
    try:
        module = load_build_module()
        skills = module.discover_skills()
        owners = module.validate_skills(skills)
    except (Exception, SystemExit) as exc:
        return [f"Skill architecture validation failed: {exc}"]

    expected_catalog = module.render_skill_catalog(skills)
    actual_catalog = CATALOG_PATH.read_text(encoding="utf-8")
    if actual_catalog != expected_catalog:
        errors.append("skill-catalog.json is out of date")

    expected_map = module.render_output_map(skills, owners)
    actual_map = OUTPUT_MAP_PATH.read_text(encoding="utf-8")
    if actual_map != expected_map:
        errors.append("skill-output-map.md is out of date")

    for skill in skills:
        skill_path = Path(str(skill["_skill_path"]))
        yaml_path = skill_path.parent / "agents" / "openai.yaml"
        existing = module.parse_agent_yaml(yaml_path)
        expected_yaml = module.render_agent_yaml(skill, existing)
        if not yaml_path.is_file() or yaml_path.read_text(encoding="utf-8") != expected_yaml:
            errors.append(f"{skill['name']}: agents/openai.yaml is out of date")
    return errors


def agents_catalog_errors() -> list[str]:
    errors: list[str] = []
    agents_text = AGENTS_PATH.read_text(encoding="utf-8")
    begin = "<!-- BEGIN AUTO-GENERATED SKILLS -->"
    end = "<!-- END AUTO-GENERATED SKILLS -->"
    if begin not in agents_text or end not in agents_text:
        return ["AGENTS.md is missing generated Skill markers"]
    block = agents_text.split(begin, 1)[1].split(end, 1)[0]
    agents_names = set(re.findall(r"(?m)^- ([a-z0-9-]+):", block))
    catalog_names = {
        str(entry["name"])
        for entry in json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    }
    if agents_names != catalog_names:
        errors.append("AGENTS.md Skill names do not match skill-catalog.json")
    return errors


def python_syntax_errors() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.py")):
        if any(part in FORBIDDEN_DIRS for part in path.parts):
            continue
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except (SyntaxError, UnicodeDecodeError) as exc:
            errors.append(f"Python syntax error in {path.relative_to(ROOT)}: {exc}")
    return errors


def command_errors() -> list[str]:
    errors: list[str] = []
    commands = (
        (
            "catalog lint",
            [sys.executable, "workflow/scripts/lint_skill_catalog.py", "--all"],
        ),
        (
            "AGENTS sync check",
            [sys.executable, "workflow/scripts/sync_agents_md.py", "--check"],
        ),
    )
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    for name, command in commands:
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        output = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
        if result.returncode != 0:
            errors.append(f"{name} failed: {output}")
        elif "WARNINGS" in result.stdout:
            errors.append(f"{name} produced warnings: {output}")
    return errors


def collect_errors(*, include_commands: bool = True) -> list[str]:
    errors: list[str] = []
    if SKILLS_DIR.is_symlink():
        errors.append("workflow/skills must be materialized, not a symlink")
    errors.extend(scan_tree_errors())
    errors.extend(license_errors())
    errors.extend(catalog_errors())
    errors.extend(generated_metadata_errors())
    errors.extend(agents_catalog_errors())
    errors.extend(python_syntax_errors())
    if include_commands:
        errors.extend(command_errors())
    return errors


def run_tests() -> int:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "workflow/scripts",
            "-p",
            "test_*.py",
        ],
        cwd=ROOT,
        env=env,
        check=False,
    )
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-tests",
        action="store_true",
        help="Run the packaged unittest suite after static release checks.",
    )
    args = parser.parse_args()

    errors = collect_errors()
    if errors:
        print("PUBLIC RELEASE CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"OK  public release checks passed for {EXPECTED_SKILL_COUNT} "
        "materialized Skills"
    )
    if args.run_tests:
        return run_tests()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
