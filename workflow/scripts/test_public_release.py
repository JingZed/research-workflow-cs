from __future__ import annotations

import json
from pathlib import Path
import unittest

import build_research_skills
import check_public_release


class PublicReleaseTest(unittest.TestCase):
    def test_end_to_end_workflow_guide_is_present(self) -> None:
        guide = check_public_release.ROOT / "WORKFLOW.md"
        self.assertTrue(guide.is_file())
        text = guide.read_text(encoding="utf-8")
        for heading in (
            "## 1. Prepare the root and topic",
            "## 2. Establish scope and collect literature",
            "## 3. Turn a candidate into a research direction",
            "## 4. Run, monitor, and interpret experiments",
            "## 5. Build the paper story and artifacts",
            "## 6. Finish, promote, and deliver",
            "## 7. Resume and verify",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)
        self.assertIn("init_research_workspace.py", text)
        self.assertIn("validate_research_workflow.py", text)

    def test_static_release_contract_passes(self) -> None:
        self.assertEqual(
            check_public_release.collect_errors(include_commands=False),
            [],
        )

    def test_catalog_paths_are_relative_and_resolve_inside_release(self) -> None:
        catalog = json.loads(
            check_public_release.CATALOG_PATH.read_text(encoding="utf-8")
        )
        for entry in catalog:
            with self.subTest(skill=entry["name"]):
                path = Path(entry["path"])
                self.assertFalse(path.is_absolute())
                resolved = check_public_release.ROOT / path
                self.assertTrue(resolved.is_file())
                self.assertTrue(
                    check_public_release._within(
                        resolved,
                        check_public_release.ROOT,
                    )
                )

    def test_skill_tree_is_materialized_and_cache_free(self) -> None:
        self.assertFalse(check_public_release.SKILLS_DIR.is_symlink())
        self.assertEqual(
            list(check_public_release.SKILLS_DIR.rglob("__pycache__")),
            [],
        )
        self.assertEqual(
            list(check_public_release.SKILLS_DIR.rglob("*.pyc")),
            [],
        )

    def test_project_and_upstream_mit_licenses_are_complete(self) -> None:
        self.assertEqual(check_public_release.license_errors(), [])
        self.assertFalse(list(check_public_release.ROOT.rglob("*_PENDING.md")))

    def test_explicit_only_wording_detector_is_bidirectional_contract_input(self) -> None:
        self.assertTrue(
            build_research_skills.description_requires_explicit_invocation(
                "Explicit-only. Trigger only when the user explicitly asks."
            )
        )
        self.assertFalse(
            build_research_skills.description_requires_explicit_invocation(
                "Use when a paper PDF needs structured conversion."
            )
        )


if __name__ == "__main__":
    unittest.main()
