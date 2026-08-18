from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


MODULE_PATH = Path(__file__).resolve().parent / "init_research_workspace.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "init_research_workspace_under_test", MODULE_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class InitResearchWorkspaceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.parent = Path(self.tempdir.name).resolve()
        self.module = load_module()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_root_preview_lists_workflow_and_topics_without_writing(self):
        root = self.parent / "research"
        plan = self.module.initialize(str(root), apply=False)

        self.assertIsNone(plan.topic)
        self.assertEqual(
            [path.relative_to(root).as_posix() for path in plan.directories],
            ["workflow", "workflow/skills", "workflow/scripts", "topics"],
        )
        self.assertEqual(plan.files, ())
        self.assertFalse(root.exists())

    def test_topic_preview_is_nested_and_domain_neutral(self):
        root = self.parent / "research"
        plan = self.module.initialize(root.as_posix(), topic="my-topic", apply=False)

        self.assertEqual(plan.topic, "my-topic")
        self.assertEqual(
            [path.relative_to(root).as_posix() for path in plan.directories],
            [
                "workflow",
                "workflow/skills",
                "workflow/scripts",
                "topics",
                "topics/my-topic/synthesis",
                "topics/my-topic/ideas",
                "topics/my-topic/papers",
            ],
        )
        self.assertEqual(
            [path.relative_to(root).as_posix() for path in plan.files],
            ["topics/my-topic/ideas/registry.yaml"],
        )
        self.assertFalse(root.exists())

    def test_apply_root_creates_only_root_scaffold(self):
        root = self.parent / "research"
        self.module.initialize(str(root), apply=True)

        self.assertTrue((root / "workflow").is_dir())
        self.assertTrue((root / "workflow" / "skills").is_dir())
        self.assertTrue((root / "workflow" / "scripts").is_dir())
        self.assertTrue((root / "topics").is_dir())
        self.assertFalse((root / "synthesis").exists())
        self.assertFalse((root / "ideas").exists())
        self.assertFalse((root / "papers").exists())
        self.assertFalse((root / "infrastructure").exists())
        self.assertFalse((root / "deliverables").exists())
        self.assertFalse((root / "presentations").exists())

    def test_apply_topic_creates_topic_skeleton_and_registry(self):
        root = self.parent / "research"
        self.module.initialize(str(root), topic="my-topic", apply=True)

        topic_root = root / "topics" / "my-topic"
        self.assertTrue((topic_root / "synthesis").is_dir())
        self.assertTrue((topic_root / "ideas").is_dir())
        self.assertTrue((topic_root / "papers").is_dir())
        self.assertEqual(
            (topic_root / "ideas" / "registry.yaml").read_text(encoding="utf-8"),
            self.module.REGISTRY_TEXT,
        )
        self.assertFalse((root / "synthesis").exists())

    def test_apply_is_idempotent_and_preserves_registry(self):
        root = self.parent / "research"
        self.module.initialize(str(root), topic="my-topic", apply=True)
        registry = root / "topics" / "my-topic" / "ideas" / "registry.yaml"
        registry.write_text(
            "active_id: i001\nactive_entry: ideas/i001\nideas: []\n",
            encoding="utf-8",
        )

        plan = self.module.initialize(str(root), topic="my-topic", apply=True)

        self.assertEqual(plan.directories, ())
        self.assertEqual(plan.files, ())
        self.assertIn("active_id: i001", registry.read_text(encoding="utf-8"))

    def test_existing_workflow_root_is_preserved(self):
        root = self.parent / "research"
        (root / "workflow").mkdir(parents=True)
        (root / "README.md").write_text("user documentation\n", encoding="utf-8")

        plan = self.module.plan_workspace(str(root))

        self.assertNotIn(root / "workflow", plan.directories)
        self.assertIn(root / "topics", plan.directories)
        self.assertTrue((root / "README.md").is_file())

    def test_allows_existing_skills_projection_symlink(self):
        root = self.parent / "research"
        (root / "workflow").mkdir(parents=True)
        target = self.parent / "skill-source"
        target.mkdir()
        (root / "workflow" / "skills").symlink_to(target, target_is_directory=True)

        plan = self.module.plan_workspace(str(root))

        self.assertNotIn(root / "workflow" / "skills", plan.directories)
        self.assertIn(root / "workflow" / "scripts", plan.directories)

    def test_refuses_unrelated_nonempty_directory(self):
        root = self.parent / "research"
        root.mkdir()
        (root / "notes.md").write_text("user content\n", encoding="utf-8")

        with self.assertRaisesRegex(self.module.WorkspaceInitError, "Research-root marker"):
            self.module.plan_workspace(str(root))

    def test_refuses_file_collision(self):
        root = self.parent / "research"
        root.mkdir()
        (root / "workflow").write_text("not a directory\n", encoding="utf-8")

        with self.assertRaisesRegex(self.module.WorkspaceInitError, "not a directory"):
            self.module.plan_workspace(str(root))

    def test_refuses_symlinked_root(self):
        target = self.parent / "target"
        target.mkdir()
        link = self.parent / "research-link"
        link.symlink_to(target, target_is_directory=True)

        with self.assertRaisesRegex(self.module.WorkspaceInitError, "symlink"):
            self.module.plan_workspace(str(link))

    def test_refuses_nested_topic_name(self):
        root = self.parent / "research"

        with self.assertRaisesRegex(self.module.WorkspaceInitError, "one directory name"):
            self.module.plan_workspace(str(root), topic="one/two")

    def test_refuses_topic_with_unrelated_entries(self):
        root = self.parent / "research"
        topic_root = root / "topics" / "my-topic"
        topic_root.mkdir(parents=True)
        (topic_root / "notes.md").write_text("user content\n", encoding="utf-8")

        with self.assertRaisesRegex(self.module.WorkspaceInitError, "unrelated"):
            self.module.plan_workspace(str(root), topic="my-topic")


if __name__ == "__main__":
    unittest.main()
