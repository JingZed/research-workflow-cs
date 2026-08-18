from __future__ import annotations

import filecmp
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "experiment-execution"
    / "promote-run-outputs"
    / "scripts"
    / "promote_run_outputs.py"
)
FIXED_TIME = "2026-07-25T12:00:00.000000+00:00"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "run_promotion_contract_under_test", MODULE_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class RunPromotionContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.module = load_module()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write(self, path: Path, content: str) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def make_roots(self, name: str) -> tuple[Path, Path, Path]:
        case_root = self.root / name
        run_dir = case_root / "runs" / "run-001"
        staging_dir = run_dir / "staged"
        canonical_dir = case_root / "canonical"
        staging_dir.mkdir(parents=True)
        canonical_dir.mkdir(parents=True)
        return run_dir, staging_dir, canonical_dir

    def build_plan(
        self,
        run_dir: Path,
        staging_dir: Path,
        canonical_dir: Path,
        includes: list[str],
    ):
        return self.module.build_plan(
            run_dir=run_dir,
            staging_dir=staging_dir,
            canonical_dir=canonical_dir,
            includes=includes,
            created_at=FIXED_TIME,
        )

    def test_exact_paths_replace_with_archive_and_manifest(self) -> None:
        run_dir, staging_dir, canonical_dir = self.make_roots("success")
        existing_source = self.write(
            staging_dir / "metrics" / "summary.json",
            '{"score": 0.91}\n',
        )
        new_source = self.write(
            staging_dir / "tables" / "new-table.txt",
            "new table\n",
        )
        existing_destination = self.write(
            canonical_dir / "metrics" / "summary.json",
            '{"score": 0.42}\n',
        )
        old_bytes = existing_destination.read_bytes()

        plan = self.build_plan(
            run_dir,
            staging_dir,
            canonical_dir,
            ["tables/new-table.txt", "metrics/summary.json"],
        )
        self.assertEqual(plan["version"], 2)
        self.assertEqual(plan["status"], "awaiting-user-confirmation")
        self.assertEqual(
            [entry["relative_path"] for entry in plan["files"]],
            ["metrics/summary.json", "tables/new-table.txt"],
        )
        self.assertEqual(plan["files"][0]["source"], str(existing_source))
        self.assertEqual(
            plan["files"][0]["destination"], str(existing_destination)
        )
        self.assertTrue(plan["files"][0]["destination_state"]["exists"])
        self.assertFalse(plan["files"][1]["destination_state"]["exists"])
        self.assertFalse(plan["files"][0]["source_matches_destination"])
        self.assertIsNone(plan["files"][1]["source_matches_destination"])

        plan_path = run_dir / "promotion-plan.json"
        self.module.atomic_write_json(plan_path, plan)
        with mock.patch.object(
            sys,
            "argv",
            [
                "promote_run_outputs.py",
                "apply",
                "--plan",
                str(plan_path),
                "--approval-note",
                "current task confirmed exact paths",
            ],
        ):
            result = self.module.main()

        self.assertEqual(result, 0)
        manifest = json.loads(
            (run_dir / "promotion-manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["status"], "promoted")
        self.assertEqual(
            manifest["approval_note"], "current task confirmed exact paths"
        )
        self.assertIsNone(manifest["failure"])
        self.assertEqual(manifest["rollback_errors"], [])
        self.assertIn("Restore each archived file", manifest["rollback"])

        by_path = {
            entry["relative_path"]: entry for entry in manifest["files"]
        }
        existing_result = by_path["metrics/summary.json"]
        archive = Path(existing_result["archive"])
        self.assertTrue(archive.is_file())
        self.assertEqual(archive.read_bytes(), old_bytes)
        self.assertTrue(
            filecmp.cmp(existing_source, existing_destination, shallow=False)
        )
        self.assertTrue(existing_result["source_matches_destination"])
        self.assertTrue(
            existing_result["archive_matches_previous_destination"]
        )

        new_result = by_path["tables/new-table.txt"]
        new_destination = canonical_dir / "tables" / "new-table.txt"
        self.assertIsNone(new_result["archive"])
        self.assertTrue(filecmp.cmp(new_source, new_destination, shallow=False))
        self.assertEqual(
            list(canonical_dir.parent.glob(".replacement-*")),
            [],
        )

    def test_rejects_glob_absolute_parent_dot_duplicate_and_missing(self) -> None:
        run_dir, staging_dir, canonical_dir = self.make_roots("reject")
        source = self.write(staging_dir / "metrics" / "summary.json", "{}\n")
        invalid_paths = (
            ("glob", "metrics/*.json"),
            ("absolute", str(source.resolve())),
            ("parent", "../summary.json"),
            ("dot", "metrics/./summary.json"),
        )
        for name, include in invalid_paths:
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.build_plan(
                    run_dir,
                    staging_dir,
                    canonical_dir,
                    [include],
                )

        with self.assertRaisesRegex(ValueError, "duplicate include paths"):
            self.build_plan(
                run_dir,
                staging_dir,
                canonical_dir,
                ["metrics/summary.json", "metrics/summary.json"],
            )

        with self.assertRaisesRegex(
            FileNotFoundError, "staged file not found"
        ):
            self.build_plan(
                run_dir,
                staging_dir,
                canonical_dir,
                ["metrics/missing.json"],
            )

    def test_source_change_after_plan_is_rejected_before_mutation(self) -> None:
        run_dir, staging_dir, canonical_dir = self.make_roots("source-change")
        source = self.write(staging_dir / "result.txt", "new\n")
        destination = self.write(canonical_dir / "result.txt", "old\n")
        plan = self.build_plan(
            run_dir, staging_dir, canonical_dir, ["result.txt"]
        )

        source.write_text("changed source\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "source result.txt changed"):
            self.module.apply_plan(
                plan,
                approval_note="current task confirmed exact paths",
            )

        self.assertEqual(destination.read_text(encoding="utf-8"), "old\n")
        self.assertFalse(Path(plan["archive_dir"]).exists())

    def test_destination_change_after_plan_is_rejected_before_mutation(
        self,
    ) -> None:
        run_dir, staging_dir, canonical_dir = self.make_roots(
            "destination-change"
        )
        self.write(staging_dir / "result.txt", "new\n")
        destination = self.write(canonical_dir / "result.txt", "old\n")
        plan = self.build_plan(
            run_dir, staging_dir, canonical_dir, ["result.txt"]
        )

        destination.write_text("external change\n", encoding="utf-8")
        with self.assertRaisesRegex(
            ValueError, "destination result.txt changed"
        ):
            self.module.apply_plan(
                plan,
                approval_note="current task confirmed exact paths",
            )

        self.assertEqual(
            destination.read_text(encoding="utf-8"), "external change\n"
        )
        self.assertFalse(Path(plan["archive_dir"]).exists())

    def test_symlink_escape_is_rejected_for_source_and_destination(
        self,
    ) -> None:
        source_run, source_staging, source_canonical = self.make_roots(
            "source-symlink"
        )
        outside_source = self.root / "outside-source"
        self.write(outside_source / "result.txt", "outside\n")
        (source_staging / "escape").symlink_to(
            outside_source, target_is_directory=True
        )
        with self.assertRaisesRegex(
            ValueError, "symlinked replacement path is forbidden"
        ):
            self.build_plan(
                source_run,
                source_staging,
                source_canonical,
                ["escape/result.txt"],
            )

        destination_run, destination_staging, destination_canonical = (
            self.make_roots("destination-symlink")
        )
        self.write(destination_staging / "nested" / "result.txt", "new\n")
        outside_destination = self.root / "outside-destination"
        outside_destination.mkdir()
        (destination_canonical / "nested").symlink_to(
            outside_destination, target_is_directory=True
        )
        with self.assertRaisesRegex(
            ValueError, "symlinked replacement path is forbidden"
        ):
            self.build_plan(
                destination_run,
                destination_staging,
                destination_canonical,
                ["nested/result.txt"],
            )
        self.assertEqual(list(outside_destination.iterdir()), [])

    def test_old_plan_version_is_rejected(self) -> None:
        run_dir, _, _ = self.make_roots("old-plan")
        plan_path = run_dir / "old-plan.json"
        self.module.atomic_write_json(
            plan_path,
            {
                "version": 1,
                "kind": "run-output-promotion-plan",
                "status": "planned",
            },
        )
        with self.assertRaisesRegex(
            ValueError, "unsupported replacement plan version"
        ):
            self.module.load_plan(plan_path)

    def test_second_file_fault_rolls_back_all_destinations(self) -> None:
        run_dir, staging_dir, canonical_dir = self.make_roots("rollback")
        first_source = self.write(staging_dir / "a.txt", "new a\n")
        second_source = self.write(staging_dir / "b.txt", "new b\n")
        first_destination = self.write(canonical_dir / "a.txt", "old a\n")
        second_destination = self.write(canonical_dir / "b.txt", "old b\n")
        first_old = first_destination.read_bytes()
        second_old = second_destination.read_bytes()
        plan = self.build_plan(
            run_dir,
            staging_dir,
            canonical_dir,
            ["a.txt", "b.txt"],
        )

        original_copy_and_compare = self.module.copy_and_compare
        injected: list[Path] = []

        def inject_second_file_fault(source: Path, destination: Path):
            state = original_copy_and_compare(source, destination)
            if source == second_source and "prepared" in destination.parts:
                destination.write_text(
                    "fault after verified second-file copy\n",
                    encoding="utf-8",
                )
                injected.append(destination)
            return state

        with mock.patch.object(
            self.module,
            "copy_and_compare",
            side_effect=inject_second_file_fault,
        ):
            manifest = self.module.apply_plan(
                plan,
                approval_note="current task confirmed exact paths",
                applied_at=FIXED_TIME,
            )

        self.assertEqual(len(injected), 1)
        self.assertEqual(manifest["status"], "failed")
        self.assertIn(
            "canonical destination differs from source: b.txt",
            manifest["failure"],
        )
        self.assertEqual(manifest["rollback_errors"], [])
        self.assertEqual(first_destination.read_bytes(), first_old)
        self.assertEqual(second_destination.read_bytes(), second_old)
        self.assertTrue(
            all(item["restored"] for item in manifest["files"])
        )

        archive_dir = Path(plan["archive_dir"])
        self.assertEqual((archive_dir / "a.txt").read_bytes(), first_old)
        self.assertEqual((archive_dir / "b.txt").read_bytes(), second_old)
        self.assertEqual(
            list(canonical_dir.parent.glob(".replacement-*")),
            [],
        )
        self.assertTrue(first_source.is_file())
        self.assertTrue(second_source.is_file())


if __name__ == "__main__":
    unittest.main()
