"""Tests for lint_skill_catalog.py drift and warning checks."""
from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import lint_skill_catalog


class LintSkillCatalogTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.skills_root = self.root / "skills" / "paper-writing"
        self.skills_root.mkdir(parents=True)
        self.catalog_path = self.root / "skill-catalog.json"
        self.output_map_path = self.root / "skill-output-map.md"
        self.output_map_path.write_text("", encoding="utf-8")

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_skill(
        self,
        name: str,
        *,
        frontmatter: bool = True,
        body_extra: str = "",
        handoff: str | None = None,
        produce: str = "`out.md`",
    ) -> Path:
        skill_dir = self.skills_root / name
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        header = (
            f"---\nname: {name}\ndescription: Test skill.\n---\n\n"
            if frontmatter
            else ""
        )
        handoff_section = (
            "## Handoff\n" + handoff + "\n" if handoff is not None else ""
        )
        skill_md.write_text(
            header
            + "# Test Skill\n\n"
            + "## Produce\n"
            + f"- {produce}\n\n"
            + handoff_section
            + body_extra,
            encoding="utf-8",
        )
        return skill_md

    def write_catalog(self, entries: list[dict]) -> None:
        self.catalog_path.write_text(
            json.dumps(entries, indent=2) + "\n",
            encoding="utf-8",
        )

    def catalog_entry(self, name: str, path: Path) -> dict:
        return {
            "part": "paper-writing",
            "category": "Test",
            "name": name,
            "title": "Test Skill",
            "description": "Test skill.",
            "path": str(path),
            "consumes": [],
            "produces": ["`out.md`"],
        }

    def run_lint(self) -> tuple[int | None, str]:
        stdout = io.StringIO()
        argv = [
            "lint_skill_catalog.py",
            "--catalog",
            str(self.catalog_path),
            "--skills-root",
            str(self.skills_root),
        ]
        with mock.patch.object(sys, "argv", argv), mock.patch.object(
            lint_skill_catalog,
            "OUTPUT_MAP_PATH",
            str(self.output_map_path),
        ):
            with redirect_stdout(stdout):
                try:
                    lint_skill_catalog.main()
                except SystemExit as exc:
                    return int(exc.code or 0), stdout.getvalue()
        return None, stdout.getvalue()

    def test_missing_frontmatter_is_an_error(self) -> None:
        skill_md = self.write_skill("missing-frontmatter", frontmatter=False)
        self.write_catalog([self.catalog_entry("missing-frontmatter", skill_md)])

        code, output = self.run_lint()

        self.assertEqual(code, 1)
        self.assertIn("missing required frontmatter", output)

    def test_retired_router_field_is_an_error(self) -> None:
        skill_md = self.write_skill("handoff-source")
        entry = self.catalog_entry("handoff-source", skill_md)
        entry["next_skills"] = ["$missing"]
        self.write_catalog([entry])

        code, output = self.run_lint()

        self.assertEqual(code, 1)
        self.assertIn("retired router field 'next_skills'", output)

    def test_extra_skill_directory_is_catalog_drift_error(self) -> None:
        self.write_skill("uncataloged")
        self.write_catalog([])

        code, output = self.run_lint()

        self.assertEqual(code, 1)
        self.assertIn("has no catalog entry", output)

    def test_relative_catalog_path_resolves_from_research_root(self) -> None:
        skill_md = self.write_skill("portable-path")
        relative_path = skill_md.relative_to(self.root).as_posix()
        self.write_catalog([self.catalog_entry("portable-path", Path(relative_path))])

        with mock.patch.object(lint_skill_catalog, "RESEARCH_ROOT", str(self.root)):
            code, output = self.run_lint()

        self.assertEqual(code, 0, output)

    def test_forbidden_hardcoded_path_is_warning_only(self) -> None:
        skill_md = self.write_skill(
            "finish",
            body_extra="Use `paper/review-log.md` in prose.\n",
        )
        self.write_catalog([self.catalog_entry("finish", skill_md)])

        code, output = self.run_lint()

        self.assertEqual(code, 0)
        self.assertIn("W2", output)
        self.assertIn("paper/review-log.md", output)

    def test_review_state_is_rejected_even_with_normalized_paper_dir(self) -> None:
        skill_md = self.write_skill(
            "review-state-holder",
            body_extra="Use `<paper-dir>/review-state.json` as workflow state.\n",
        )
        self.write_catalog([self.catalog_entry("review-state-holder", skill_md)])

        code, output = self.run_lint()

        self.assertEqual(code, 1)
        self.assertIn("E6", output)
        self.assertIn("review-state.json", output)

    def test_handoff_section_is_retired(self) -> None:
        skill_md = self.write_skill(
            "handoff-source", handoff="- Pass to $other-skill.\n"
        )
        other_md = self.write_skill("other-skill")
        self.write_catalog(
            [
                self.catalog_entry("handoff-source", skill_md),
                self.catalog_entry("other-skill", other_md),
            ]
        )

        code, output = self.run_lint()

        self.assertEqual(code, 1)
        self.assertIn("## handoff", output)

    def test_shared_routing_reference_is_retired(self) -> None:
        skill_md = self.write_skill(
            "routing-reference",
            body_extra="Read `../../_shared/workflow-map.md`.\n",
        )
        self.write_catalog([self.catalog_entry("routing-reference", skill_md)])

        code, output = self.run_lint()

        self.assertEqual(code, 1)
        self.assertIn("workflow-map.md", output)


if __name__ == "__main__":
    unittest.main()
