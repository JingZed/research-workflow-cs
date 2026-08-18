"""Smoke tests for sync_agents_md.py: idempotence + section preservation."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sync_agents_md


SAMPLE_SKILLS = [
    {
        "part": "research-ideation",
        "name": "paper-to-markdown",
        "description": "Convert a paper PDF into Markdown.",
        "path": "/abs/path/to/paper-to-markdown/SKILL.md",
    },
    {
        "part": "experiment-execution",
        "name": "run-experiment",
        "description": "Launch one ready experiment runbook.",
        "path": "/abs/path/to/run-experiment/SKILL.md",
    },
    {
        "part": "paper-writing",
        "name": "paper-story-framer",
        "description": "Frame an evidence-backed paper story.",
        "path": "/abs/path/to/paper-story-framer/SKILL.md",
    },
]


SAMPLE_AGENTS_BEFORE = """# AGENTS.md

## Skills
A skill is a reusable local workflow bundle.

## Literature Architecture
Topic-rooted layout.

### Available skills
#### Research Ideation
- old-stale-skill: This entry is stale and must be replaced. (file: /old/path/SKILL.md)

### How to use skills
- Discovery rule.

## CCB Communication Rule
After section.
"""


class RenderBlockTests(unittest.TestCase):
    def test_render_includes_markers_and_subheaders(self) -> None:
        block = sync_agents_md.render_block(SAMPLE_SKILLS)
        self.assertTrue(block.startswith(sync_agents_md.BEGIN_MARKER))
        self.assertTrue(block.endswith(sync_agents_md.END_MARKER))
        self.assertIn("#### Research Ideation", block)
        self.assertIn("#### Experiment Execution", block)
        self.assertIn("#### Paper Writing", block)
        self.assertIn("paper-to-markdown: Convert a paper PDF", block)

    def test_skips_empty_parts(self) -> None:
        skills = [SAMPLE_SKILLS[0]]
        block = sync_agents_md.render_block(skills)
        self.assertIn("#### Research Ideation", block)
        self.assertNotIn("#### Experiment Execution", block)


class SpliceSectionTests(unittest.TestCase):
    def test_replaces_old_body_preserves_surroundings(self) -> None:
        block = sync_agents_md.render_block(SAMPLE_SKILLS)
        result = sync_agents_md.splice_section(SAMPLE_AGENTS_BEFORE, block)
        self.assertNotIn("old-stale-skill", result)
        self.assertIn("paper-to-markdown", result)
        self.assertIn("## Literature Architecture", result)
        self.assertIn("## CCB Communication Rule", result)
        self.assertIn("### How to use skills", result)
        self.assertIn(sync_agents_md.SECTION_HEADER, result)

    def test_idempotent_on_already_synced(self) -> None:
        block = sync_agents_md.render_block(SAMPLE_SKILLS)
        once = sync_agents_md.splice_section(SAMPLE_AGENTS_BEFORE, block)
        twice = sync_agents_md.splice_section(once, block)
        self.assertEqual(once, twice)

    def test_missing_header_raises(self) -> None:
        bad = "# AGENTS.md\n\n## Skills\nNo header.\n"
        block = sync_agents_md.render_block(SAMPLE_SKILLS)
        with self.assertRaises(SystemExit):
            sync_agents_md.splice_section(bad, block)

    def test_section_at_eof(self) -> None:
        text = (
            "# AGENTS.md\n\n### Available skills\n"
            "- old-skill: stale (file: /old)\n"
        )
        block = sync_agents_md.render_block(SAMPLE_SKILLS)
        result = sync_agents_md.splice_section(text, block)
        self.assertNotIn("old-skill", result)
        self.assertIn(sync_agents_md.BEGIN_MARKER, result)
        self.assertIn(sync_agents_md.END_MARKER, result)

    def test_prefers_markers_over_heading_boundary_when_markers_exist(self) -> None:
        text = (
            "# AGENTS.md\n\n"
            "### Available skills\n\n"
            f"{sync_agents_md.BEGIN_MARKER}\n"
            "#### Research Ideation\n"
            "- old-skill: stale (file: /old)\n"
            "### Accidental generated heading\n"
            "- generated body that should be replaced\n"
            f"{sync_agents_md.END_MARKER}\n\n"
            "### How to use skills\n"
            "- Discovery rule.\n"
        )
        block = sync_agents_md.render_block(SAMPLE_SKILLS)

        result = sync_agents_md.splice_section(text, block)

        self.assertNotIn("old-skill", result)
        self.assertNotIn("Accidental generated heading", result)
        self.assertIn("paper-to-markdown", result)
        self.assertIn("### How to use skills", result)


class CheckModeTests(unittest.TestCase):
    def test_check_passes_on_synced_file(self) -> None:
        with mock.patch.object(sync_agents_md, "CATALOG_PATH") as catalog_mock, \
             mock.patch.object(sync_agents_md, "AGENTS_PATH") as agents_mock:
            catalog_mock.read_text.return_value = json.dumps(SAMPLE_SKILLS)
            block = sync_agents_md.render_block(SAMPLE_SKILLS)
            synced = sync_agents_md.splice_section(SAMPLE_AGENTS_BEFORE, block)
            agents_mock.read_text.return_value = synced
            with mock.patch.object(sys_argv := __import__("sys"), "argv", ["sync_agents_md.py", "--check"]):
                rc = sync_agents_md.main()
            self.assertEqual(rc, 0)

    def test_check_fails_on_drifted_file(self) -> None:
        with mock.patch.object(sync_agents_md, "CATALOG_PATH") as catalog_mock, \
             mock.patch.object(sync_agents_md, "AGENTS_PATH") as agents_mock:
            catalog_mock.read_text.return_value = json.dumps(SAMPLE_SKILLS)
            agents_mock.read_text.return_value = SAMPLE_AGENTS_BEFORE
            with mock.patch.object(sys_argv := __import__("sys"), "argv", ["sync_agents_md.py", "--check"]):
                rc = sync_agents_md.main()
            self.assertEqual(rc, 1)

    def test_write_mode_updates_tempfile(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            temp_root = Path(tempdir)
            catalog_path = temp_root / "skill-catalog.json"
            agents_path = temp_root / "AGENTS.md"
            catalog_path.write_text(json.dumps(SAMPLE_SKILLS), encoding="utf-8")
            agents_path.write_text(SAMPLE_AGENTS_BEFORE, encoding="utf-8")

            with mock.patch.object(sync_agents_md, "CATALOG_PATH", catalog_path), \
                 mock.patch.object(sync_agents_md, "AGENTS_PATH", agents_path), \
                 mock.patch.object(sys, "argv", ["sync_agents_md.py"]):
                rc = sync_agents_md.main()

            self.assertEqual(rc, 0)
            updated = agents_path.read_text(encoding="utf-8")
            self.assertIn("paper-to-markdown", updated)
            self.assertNotIn("old-stale-skill", updated)


if __name__ == "__main__":
    unittest.main()
