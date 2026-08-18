#!/usr/bin/env python3
"""Sync AGENTS.md "### Available skills" section from skill-catalog.json.

Single source of truth: workflow/skills/_shared/skill-catalog.json (regenerated
by build_research_skills.py). This script rewrites the body of the
"### Available skills" section in AGENTS.md, keeping the section heading and
all surrounding hand-written content untouched.

Idempotent. Use --check to verify AGENTS.md is already in sync (exit 1 if not).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CATALOG_PATH = ROOT / "workflow" / "skills" / "_shared" / "skill-catalog.json"
AGENTS_PATH = ROOT / "AGENTS.md"

BEGIN_MARKER = "<!-- BEGIN AUTO-GENERATED SKILLS -->"
END_MARKER = "<!-- END AUTO-GENERATED SKILLS -->"
SECTION_HEADER = "### Available skills"

PART_ORDER = ["research-ideation", "experiment-execution", "paper-writing", "standalone"]
PART_HEADINGS = {
    "research-ideation": "Research Ideation",
    "experiment-execution": "Experiment Execution",
    "paper-writing": "Paper Writing",
    "standalone": "Standalone Utility Skills",
}


def render_block(skills: list[dict]) -> str:
    by_part: dict[str, list[dict]] = {p: [] for p in PART_ORDER}
    for s in skills:
        by_part.setdefault(s["part"], []).append(s)
    lines: list[str] = [BEGIN_MARKER]
    for part in PART_ORDER:
        items = by_part.get(part, [])
        if not items:
            continue
        lines.append(f"#### {PART_HEADINGS[part]}")
        for s in items:
            desc = str(s.get("short_description") or s["description"]).strip()
            path = s["path"]
            lines.append(f"- {s['name']}: {desc} (file: {path})")
    lines.append(END_MARKER)
    return "\n".join(lines)


def splice_section(agents_text: str, block: str) -> str:
    """Replace the body of the '### Available skills' section with `block`.

    Prefer the generated BEGIN/END markers when present. Older AGENTS.md files
    without markers fall back to replacing everything between the section
    heading and the next '### ' or '## ' heading. The heading itself is
    preserved.
    """
    marker_start = agents_text.find(BEGIN_MARKER)
    marker_end = agents_text.find(END_MARKER, marker_start + len(BEGIN_MARKER))
    if marker_start != -1 and marker_end != -1:
        marker_end += len(END_MARKER)
        head = agents_text[:marker_start].rstrip("\n") + "\n\n"
        tail = agents_text[marker_end:]
        if not tail.startswith("\n"):
            tail = "\n" + tail
        return head + block + tail

    lines = agents_text.splitlines(keepends=True)
    start_idx = None
    for i, line in enumerate(lines):
        if line.rstrip() == SECTION_HEADER:
            start_idx = i
            break
    if start_idx is None:
        raise SystemExit(
            f"AGENTS.md is missing the '{SECTION_HEADER}' section heading"
        )
    end_idx = len(lines)
    for j in range(start_idx + 1, len(lines)):
        stripped = lines[j].rstrip()
        if stripped.startswith("### ") or stripped.startswith("## "):
            end_idx = j
            break
    head = "".join(lines[: start_idx + 1])
    tail = "".join(lines[end_idx:])
    body = "\n" + block + "\n"
    if not tail.startswith("\n"):
        body += "\n"
    return head + body + tail


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if AGENTS.md is out of sync; do not write.",
    )
    args = parser.parse_args()

    skills = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    block = render_block(skills)
    current = AGENTS_PATH.read_text(encoding="utf-8")
    updated = splice_section(current, block)

    if args.check:
        if current != updated:
            sys.stderr.write(
                "AGENTS.md is out of sync with skill-catalog.json.\n"
                "Run: python workflow/scripts/sync_agents_md.py\n"
            )
            return 1
        print("OK  AGENTS.md is in sync with skill-catalog.json")
        return 0

    if current == updated:
        print("OK  AGENTS.md already in sync")
        return 0
    AGENTS_PATH.write_text(updated, encoding="utf-8")
    print(f"OK  AGENTS.md skills section synced from {CATALOG_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
