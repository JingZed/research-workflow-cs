from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

import yaml


MODULE_PATH = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "research-ideation"
    / "idea-backlog-manager"
    / "scripts"
    / "activate_idea.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("activate_idea_under_test", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class IdeaActivationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.topic = Path(self.tempdir.name) / "topic"
        (self.topic / "synthesis").mkdir(parents=True)
        (self.topic / "ideas" / "i001").mkdir(parents=True)
        (self.topic / "ideas" / "i001" / "idea.md").write_text(
            "# Idea\n", encoding="utf-8"
        )
        self.registry = self.topic / "ideas" / "registry.yaml"
        self.registry.write_text(
            "active_id: null\n"
            "active_entry: null\n"
            "custom_registry_field: keep-me\n"
            "ideas:\n"
            "  - id: i001\n"
            "    title: Example Idea\n"
            "    slug: example-idea\n"
            "    status: promoted\n"
            "    canonical_dir: ideas/i001\n"
            "    custom_entry_field: keep-entry\n",
            encoding="utf-8",
        )
        self.module = load_module()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def args(self, *extra: str):
        return self.module.parse_args(
            [
                "--topic-root",
                str(self.topic),
                "--idea-id",
                "i001",
                "--next-action",
                "Frame a falsifiable hypothesis",
                "--last-updated",
                "2026-08-09 CST",
                *extra,
            ]
        )

    def test_activation_creates_both_state_files_and_preserves_registry_fields(self):
        plan = self.module.activate(self.args())

        self.assertTrue(plan["create_resume_state"])
        current = self.topic / "ideas" / "i001" / "notes" / "CURRENT.md"
        project_state = (
            self.topic / "ideas" / "i001" / "notes" / "project-state.md"
        )
        self.assertTrue(current.is_file())
        self.assertTrue(project_state.is_file())
        self.assertIn("next_action: Frame a falsifiable hypothesis", current.read_text())

        payload = yaml.safe_load(self.registry.read_text(encoding="utf-8"))
        self.assertEqual(payload["active_id"], "i001")
        self.assertEqual(payload["active_entry"], "ideas/i001")
        self.assertEqual(payload["custom_registry_field"], "keep-me")
        self.assertEqual(payload["ideas"][0]["status"], "active")
        self.assertEqual(payload["ideas"][0]["custom_entry_field"], "keep-entry")

    def test_dry_run_does_not_mutate(self):
        before = self.registry.read_bytes()
        plan = self.module.activate(self.args("--dry-run"))

        self.assertTrue(plan["create_resume_state"])
        self.assertEqual(self.registry.read_bytes(), before)
        self.assertFalse((self.topic / "ideas" / "i001" / "notes").exists())

    def test_refuses_to_replace_another_active_id(self):
        self.registry.write_text(
            self.registry.read_text(encoding="utf-8").replace(
                "active_id: null", "active_id: i999"
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(self.module.LifecycleError, "already has active_id"):
            self.module.activate(self.args())

    def test_refuses_active_status_without_active_pointer(self):
        self.registry.write_text(
            self.registry.read_text(encoding="utf-8").replace(
                "status: promoted", "status: active"
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(self.module.LifecycleError, "active_id is null"):
            self.module.activate(self.args())

    def test_refuses_one_sided_resume_state(self):
        notes = self.topic / "ideas" / "i001" / "notes"
        notes.mkdir()
        (notes / "CURRENT.md").write_text("phase: ideation\n", encoding="utf-8")

        with self.assertRaisesRegex(self.module.LifecycleError, "one-sided"):
            self.module.activate(self.args())

    def test_explicit_legacy_canonical_dir_can_be_activated_in_place(self):
        legacy = self.topic / "ideas" / "explorations" / "x001"
        legacy.mkdir(parents=True)
        (legacy / "idea.md").write_text("# Legacy Idea\n", encoding="utf-8")
        canonical = self.topic / "ideas" / "i001"
        (canonical / "idea.md").unlink()
        canonical.rmdir()
        canonical.symlink_to(Path("explorations") / "x001")
        self.registry.write_text(
            self.registry.read_text(encoding="utf-8").replace(
                "canonical_dir: ideas/i001",
                "canonical_dir: ideas/i001\n"
                "    legacy_id: x001\n"
                "    legacy_dir: ideas/explorations/x001\n"
                "    migration_status: canonical_alias",
            ),
            encoding="utf-8",
        )

        plan = self.module.activate(self.args())

        self.assertEqual(plan["canonical_dir"], "ideas/i001")
        self.assertTrue((legacy / "notes" / "CURRENT.md").is_file())


if __name__ == "__main__":
    unittest.main()
