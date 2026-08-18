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

    def test_preview_is_domain_neutral_and_does_not_write(self):
        root = self.parent / "workspace"
        plan = self.module.initialize(str(root), apply=False)

        self.assertEqual(
            [path.relative_to(root).as_posix() for path in plan.directories],
            ["synthesis", "ideas", "papers"],
        )
        self.assertEqual(
            [path.relative_to(root).as_posix() for path in plan.files],
            ["ideas/registry.yaml"],
        )
        self.assertFalse(root.exists())

    def test_apply_creates_only_minimal_structure(self):
        root = self.parent / "workspace"
        self.module.initialize(str(root), apply=True)

        self.assertTrue((root / "synthesis").is_dir())
        self.assertTrue((root / "ideas").is_dir())
        self.assertTrue((root / "papers").is_dir())
        self.assertEqual(
            (root / "ideas" / "registry.yaml").read_text(encoding="utf-8"),
            self.module.REGISTRY_TEXT,
        )
        self.assertEqual(
            sorted(path.name for path in root.iterdir()),
            ["ideas", "papers", "synthesis"],
        )

    def test_apply_is_idempotent_and_preserves_registry(self):
        root = self.parent / "workspace"
        self.module.initialize(str(root), apply=True)
        registry = root / "ideas" / "registry.yaml"
        registry.write_text("active_id: i001\nactive_entry: ideas/i001\nideas: []\n", encoding="utf-8")

        plan = self.module.initialize(str(root), apply=True)

        self.assertEqual(plan.directories, ())
        self.assertEqual(plan.files, ())
        self.assertIn("active_id: i001", registry.read_text(encoding="utf-8"))

    def test_refuses_unrelated_top_level_entries(self):
        root = self.parent / "workspace"
        root.mkdir()
        (root / "notes.md").write_text("user content\n", encoding="utf-8")

        with self.assertRaisesRegex(self.module.WorkspaceInitError, "unrelated"):
            self.module.plan_workspace(str(root))

    def test_refuses_file_collision(self):
        root = self.parent / "workspace"
        root.mkdir()
        (root / "ideas").write_text("not a directory\n", encoding="utf-8")

        with self.assertRaisesRegex(self.module.WorkspaceInitError, "not a directory"):
            self.module.plan_workspace(str(root))

    def test_refuses_symlinked_root(self):
        target = self.parent / "target"
        target.mkdir()
        link = self.parent / "workspace-link"
        link.symlink_to(target, target_is_directory=True)

        with self.assertRaisesRegex(self.module.WorkspaceInitError, "symlink"):
            self.module.plan_workspace(str(link))


if __name__ == "__main__":
    unittest.main()
