from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


RESOLVER_DIR = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "paper-writing"
    / "paper-outline-builder"
    / "scripts"
)
if str(RESOLVER_DIR) not in sys.path:
    sys.path.insert(0, str(RESOLVER_DIR))

import resolve_paper_dir as resolver


class OutlinePaperDirSelectionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name).resolve()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def project(self, name: str = "project") -> Path:
        path = self.root / name
        path.mkdir(parents=True)
        return path

    def mkdir(self, root: Path, relative: str) -> Path:
        path = root / relative
        path.mkdir(parents=True, exist_ok=True)
        return path.resolve()

    def write(self, root: Path, relative: str, text: str) -> Path:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def snapshot(self, root: Path) -> dict[str, tuple[str, bytes | None]]:
        result: dict[str, tuple[str, bytes | None]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            if path.is_dir():
                result[relative] = ("dir", None)
            else:
                result[relative] = ("file", path.read_bytes())
        return result

    def test_active_paper_dir_is_primary_current_field(self) -> None:
        project = self.project()
        expected = self.mkdir(project, "paper/aaai2027")
        self.write(
            project,
            "notes/CURRENT.md",
            "active_paper_dir: paper/aaai2027/\n"
            "candidate: paper/stale/main.tex\n"
            "active_artifact: paper/stale/main.pdf\n",
        )

        result = resolver.resolve_paper_dir(project)

        self.assertEqual(result.paper_dir, expected)
        self.assertEqual(result.sources, ("current.active_paper_dir",))
        self.assertFalse((project / "paper/stale").exists())

    def test_candidate_and_active_artifact_are_supported_fallbacks(self) -> None:
        for key in ("candidate", "active_artifact"):
            with self.subTest(key=key):
                project = self.project(key)
                expected = self.mkdir(project, "paper/candidate")
                self.write(
                    project,
                    "notes/CURRENT.md",
                    f"{key}: paper/candidate/main.tex\n",
                )

                result = resolver.resolve_paper_dir(project)

                self.assertEqual(result.paper_dir, expected)
                self.assertEqual(result.sources, (f"current.{key}",))

    def test_nearest_rules_allow_i002_candidate_and_protect_canonical(self) -> None:
        outer = self.project("outer")
        project = self.mkdir(outer, "topics/topic/ideas/i002")
        self.mkdir(project, "drafts")
        canonical = self.mkdir(project, "paper")
        expected = self.mkdir(project, "paper/aaai2027")
        self.write(
            outer,
            "AGENTS.md",
            "`paper/aaai2027/` is read-only.\n",
        )
        self.write(
            project,
            "AGENTS.md",
            "Resume from `notes/CURRENT.md` and `notes/project-state.md`, then "
            "read only the relevant evidence.\n\n"
            "The canonical ARR paper is `paper/main.tex` and "
            "`paper/main.pdf`; both are\n"
            "read-only. All AAAI-27 manuscript changes belong under "
            "`paper/aaai2027/`.\n",
        )
        self.write(
            project,
            "notes/CURRENT.md",
            "active_paper_dir: paper/aaai2027/\n"
            "active_artifact: paper/aaai2027/main.tex\n",
        )

        result = resolver.resolve_paper_dir(project / "drafts")

        self.assertEqual(result.paper_dir, expected)
        self.assertEqual(result.rules_path, project / "AGENTS.md")
        self.assertIn(canonical, result.protected_dirs)
        self.assertIn(expected, result.writable_dirs)
        self.assertNotIn(project / "notes", result.protected_dirs)
        with self.assertRaises(resolver.ProtectedPaperTargetError):
            resolver.resolve_paper_dir(
                project / "drafts",
                explicit_target=canonical,
            )

    def test_protected_current_target_fails(self) -> None:
        project = self.project()
        protected = self.mkdir(project, "paper")
        self.write(
            project,
            "AGENTS.md",
            "The canonical paper at `paper/` is read-only.\n",
        )
        self.write(
            project,
            "notes/CURRENT.md",
            "active_paper_dir: paper/\n",
        )

        with self.assertRaises(resolver.ProtectedPaperTargetError) as context:
            resolver.resolve_paper_dir(project)

        self.assertIn(protected, context.exception.paths)

    def test_conflicting_sources_fail(self) -> None:
        project = self.project()
        first = self.mkdir(project, "paper/first")
        second = self.mkdir(project, "paper/second")
        self.write(
            project,
            "notes/CURRENT.md",
            "active_paper_dir: paper/first/\n",
        )

        with self.assertRaises(
            resolver.ConflictingPaperTargetError
        ) as context:
            resolver.resolve_paper_dir(project, explicit_target=second)

        self.assertEqual(set(context.exception.paths), {first, second})

    def test_active_rule_and_current_conflict_fails(self) -> None:
        project = self.project()
        first = self.mkdir(project, "paper/first")
        second = self.mkdir(project, "paper/second")
        self.write(
            project,
            "AGENTS.md",
            "The active paper candidate is `paper/first/`.\n",
        )
        self.write(
            project,
            "notes/CURRENT.md",
            "candidate: paper/second/main.tex\n",
        )

        with self.assertRaises(
            resolver.ConflictingPaperTargetError
        ) as context:
            resolver.resolve_paper_dir(project)

        self.assertEqual(set(context.exception.paths), {first, second})

    def test_multiple_fallback_candidates_fail(self) -> None:
        project = self.project()
        first = self.mkdir(project, "paper/first")
        second = self.mkdir(project, "paper/second")
        self.write(
            project,
            "notes/CURRENT.md",
            "candidate: paper/first/main.tex\n"
            "active_artifact: paper/second/main.pdf\n",
        )

        with self.assertRaises(
            resolver.MultiplePaperCandidatesError
        ) as context:
            resolver.resolve_paper_dir(project)

        self.assertEqual(set(context.exception.paths), {first, second})

    def test_no_candidate_fails(self) -> None:
        project = self.project()
        self.write(project, "AGENTS.md", "No active paper is selected.\n")
        self.write(project, "notes/CURRENT.md", "phase: ideation\n")

        with self.assertRaises(resolver.NoPaperCandidateError):
            resolver.resolve_paper_dir(project)

    def test_named_but_missing_candidate_fails_without_creating_stub(self) -> None:
        project = self.project()
        missing = project / "paper/candidate"
        self.write(
            project,
            "notes/CURRENT.md",
            "candidate: paper/candidate/main.tex\n",
        )
        before = self.snapshot(project)

        with self.assertRaises(resolver.MissingPaperTargetError):
            resolver.resolve_paper_dir(project)

        self.assertFalse(missing.exists())
        self.assertEqual(self.snapshot(project), before)

    def test_success_and_failure_have_no_filesystem_side_effects(self) -> None:
        project = self.project()
        self.mkdir(project, "paper")
        self.mkdir(project, "paper/aaai2027")
        self.write(
            project,
            "AGENTS.md",
            "`paper/` is read-only. Manuscript changes belong under "
            "`paper/aaai2027/`.\n",
        )
        self.write(
            project,
            "notes/CURRENT.md",
            "active_paper_dir: paper/aaai2027/\n",
        )
        before = self.snapshot(project)

        resolver.resolve_paper_dir(project)
        with self.assertRaises(resolver.ProtectedPaperTargetError):
            resolver.resolve_paper_dir(
                project,
                explicit_target=project / "paper",
            )

        self.assertEqual(self.snapshot(project), before)
        self.assertFalse((project / "drafts/outline.md").exists())
        self.assertFalse((project / "paper/aaai2027/INVARIANTS.md").exists())

    def test_cli_returns_json_without_writing(self) -> None:
        project = self.project()
        expected = self.mkdir(project, "paper/candidate")
        self.write(
            project,
            "notes/CURRENT.md",
            "candidate: paper/candidate/main.tex\n",
        )
        before = self.snapshot(project)
        stdout = io.StringIO()
        stderr = io.StringIO()

        with redirect_stdout(stdout), redirect_stderr(stderr):
            return_code = resolver.main(["--start", str(project)])

        self.assertEqual(return_code, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(
            json.loads(stdout.getvalue())["paper_dir"],
            str(expected),
        )
        self.assertEqual(self.snapshot(project), before)


if __name__ == "__main__":
    unittest.main()
