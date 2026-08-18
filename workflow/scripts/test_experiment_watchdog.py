from __future__ import annotations

import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
from unittest import mock


MODULE_PATH = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "experiment-execution"
    / "experiment-watchdog"
    / "scripts"
    / "watch_experiment_runs.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "experiment_watchdog_under_test", MODULE_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ExperimentWatchdogTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.module = load_module()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_status(
        self,
        runs_dir: Path,
        run_id: str,
        payload: object,
    ) -> Path:
        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True)
        (run_dir / "status.json").write_text(
            json.dumps(payload),
            encoding="utf-8",
        )
        return run_dir

    def run_main(self, *args: str) -> int:
        with mock.patch.object(
            sys,
            "argv",
            ["watch_experiment_runs.py", *args],
        ):
            return self.module.main()

    def test_help_lists_the_deterministic_watchdog_interface(self) -> None:
        stdout = io.StringIO()
        with mock.patch.object(
            sys,
            "argv",
            ["watch_experiment_runs.py", "--help"],
        ), redirect_stdout(stdout), self.assertRaises(SystemExit) as raised:
            self.module.parse_args()

        self.assertEqual(raised.exception.code, 0)
        output = stdout.getvalue()
        for flag in (
            "--runs-dir",
            "--report-path",
            "--state-path",
            "--idea-root",
            "--stall-hours",
            "--now",
            "--write-unchanged",
        ):
            self.assertIn(flag, output)

    def test_fixed_clock_classifies_all_run_states(self) -> None:
        runs_dir = self.root / "experiments" / "runs"
        completed = self.write_status(
            runs_dir,
            "01-completed",
            {"status": "completed"},
        )
        failed = self.write_status(
            runs_dir,
            "02-failed",
            {"status": "failed"},
        )
        running = self.write_status(
            runs_dir,
            "03-running",
            {
                "status": "running",
                "start_time": "2026-07-25T08:00:00+00:00",
                "stdout_log": "stdout.log",
            },
        )
        stalled = self.write_status(
            runs_dir,
            "04-stalled",
            {
                "status": "running",
                "start_time": "2026-07-25T08:00:00+00:00",
                "stderr_log": "stderr.log",
            },
        )
        unknown = self.write_status(
            runs_dir,
            "05-unknown",
            {"status": "queued"},
        )
        self.assertTrue(completed.is_dir())
        self.assertTrue(failed.is_dir())
        self.assertTrue(unknown.is_dir())

        running_log = running / "stdout.log"
        running_log.write_text("active\n", encoding="utf-8")
        running_epoch = datetime.fromisoformat(
            "2026-07-25T11:30:00+00:00"
        ).timestamp()
        os.utime(running_log, (running_epoch, running_epoch))

        stalled_log = stalled / "stderr.log"
        stalled_log.write_text("quiet\n", encoding="utf-8")
        stalled_epoch = datetime.fromisoformat(
            "2026-07-25T08:30:00+00:00"
        ).timestamp()
        os.utime(stalled_log, (stalled_epoch, stalled_epoch))

        report_path = runs_dir / "watchdog-report.md"
        state_path = runs_dir / "watchdog-state.json"
        result = self.run_main(
            "--runs-dir",
            str(runs_dir),
            "--report-path",
            str(report_path),
            "--state-path",
            str(state_path),
            "--stall-hours",
            "2",
            "--now",
            "2026-07-25T12:00:00+00:00",
        )

        self.assertEqual(result, 0)
        state = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(
            state["generated_at"],
            "2026-07-25T12:00:00+00:00",
        )
        self.assertEqual(state["stall_hours"], 2.0)
        classifications = {
            item["run_id"]: item["classification"]
            for item in state["runs"]
        }
        self.assertEqual(
            classifications,
            {
                "01-completed": "completed",
                "02-failed": "failed",
                "03-running": "running",
                "04-stalled": "stalled",
                "05-unknown": "unknown",
            },
        )
        by_id = {item["run_id"]: item for item in state["runs"]}
        self.assertEqual(
            by_id["03-running"]["last_activity"],
            "2026-07-25T11:30:00+00:00",
        )
        self.assertEqual(
            by_id["04-stalled"]["last_activity"],
            "2026-07-25T08:30:00+00:00",
        )

        report = report_path.read_text(encoding="utf-8")
        headings = [
            report.index("## Stalled"),
            report.index("## Failed"),
            report.index("## Running"),
            report.index("## Completed"),
            report.index("## Unknown"),
        ]
        self.assertEqual(headings, sorted(headings))

    def test_unchanged_sweep_does_not_rewrite_outputs(self) -> None:
        runs_dir = self.root / "experiments" / "runs"
        self.write_status(
            runs_dir,
            "run-001",
            {
                "status": "running",
                "start_time": "2026-07-25T11:00:00+00:00",
            },
        )
        report_path = runs_dir / "watchdog-report.md"
        state_path = runs_dir / "watchdog-state.json"
        common_args = (
            "--runs-dir",
            str(runs_dir),
            "--report-path",
            str(report_path),
            "--state-path",
            str(state_path),
            "--stall-hours",
            "2",
        )

        self.assertEqual(
            self.run_main(
                *common_args,
                "--now",
                "2026-07-25T12:00:00+00:00",
            ),
            0,
        )
        original_report = report_path.read_bytes()
        original_state = state_path.read_bytes()

        self.assertEqual(
            self.run_main(
                *common_args,
                "--now",
                "2026-07-25T12:30:00+00:00",
            ),
            0,
        )
        self.assertEqual(report_path.read_bytes(), original_report)
        self.assertEqual(state_path.read_bytes(), original_state)

        (runs_dir / "run-001" / "status.json").write_text(
            json.dumps({"status": "completed"}),
            encoding="utf-8",
        )
        self.assertEqual(
            self.run_main(
                *common_args,
                "--now",
                "2026-07-25T12:45:00+00:00",
            ),
            0,
        )
        transitioned_state = state_path.read_bytes()
        self.assertNotEqual(transitioned_state, original_state)
        self.assertEqual(
            json.loads(transitioned_state)["runs"][0]["classification"],
            "completed",
        )

        self.assertEqual(
            self.run_main(
                *common_args,
                "--now",
                "2026-07-25T13:00:00+00:00",
                "--write-unchanged",
            ),
            0,
        )
        self.assertNotEqual(state_path.read_bytes(), transitioned_state)

    def test_capability_modes_resolve_off_on_and_auto(self) -> None:
        cases = (
            ("off-available", "off", True, False),
            ("on-available", "on", True, True),
            ("on-unavailable", "on", False, False),
            ("auto-available", "auto", True, True),
            ("auto-unavailable", "auto", False, False),
        )
        for name, configured, available, enabled in cases:
            with self.subTest(name=name):
                idea_root = self.root / name / "idea"
                notes_dir = idea_root / "notes"
                notes_dir.mkdir(parents=True)
                (notes_dir / "capabilities.yaml").write_text(
                    "version: 1\n"
                    "capabilities:\n"
                    f"  watchdog: {configured}\n",
                    encoding="utf-8",
                )
                runs_dir = idea_root / "experiments" / "runs"
                if available:
                    runs_dir.mkdir(parents=True)

                state = self.module.load_watchdog_capability(
                    idea_root,
                    runs_dir,
                )

                self.assertEqual(state["configured"], configured)
                self.assertEqual(state["available"], available)
                self.assertEqual(state["enabled"], enabled)
                self.assertTrue(state["reason"])

    def assert_invalid_input_preserves_outputs(
        self,
        case_name: str,
        status_text: str,
        exception_type: type[BaseException],
    ) -> None:
        case_root = self.root / case_name
        runs_dir = case_root / "runs"
        run_dir = runs_dir / "run-001"
        run_dir.mkdir(parents=True)
        (run_dir / "status.json").write_text(
            status_text,
            encoding="utf-8",
        )
        report_path = case_root / "watchdog-report.md"
        state_path = case_root / "watchdog-state.json"
        report_path.write_text("old report\n", encoding="utf-8")
        state_path.write_text('{"old": true}\n', encoding="utf-8")

        with self.assertRaises(exception_type):
            self.run_main(
                "--runs-dir",
                str(runs_dir),
                "--report-path",
                str(report_path),
                "--state-path",
                str(state_path),
                "--now",
                "2026-07-25T12:00:00+00:00",
            )

        self.assertEqual(
            report_path.read_text(encoding="utf-8"),
            "old report\n",
        )
        self.assertEqual(
            state_path.read_text(encoding="utf-8"),
            '{"old": true}\n',
        )
        self.assertEqual(
            list(case_root.glob(".watchdog-report.md.*.tmp")),
            [],
        )
        self.assertEqual(
            list(case_root.glob(".watchdog-state.json.*.tmp")),
            [],
        )

    def test_corrupt_json_leaves_no_half_written_outputs(self) -> None:
        self.assert_invalid_input_preserves_outputs(
            "corrupt-json",
            '{"status": "running"',
            json.JSONDecodeError,
        )

    def test_timezone_free_timestamp_leaves_no_half_written_outputs(
        self,
    ) -> None:
        self.assert_invalid_input_preserves_outputs(
            "timezone-free",
            json.dumps(
                {
                    "status": "running",
                    "start_time": "2026-07-25T10:00:00",
                }
            ),
            ValueError,
        )


if __name__ == "__main__":
    unittest.main()
