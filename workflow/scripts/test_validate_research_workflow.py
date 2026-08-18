import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parent / "validate_research_workflow.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "validate_research_workflow_under_test", MODULE_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ValidateResearchWorkflowTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.idea = Path(self.tempdir.name) / "idea"
        (self.idea / "notes").mkdir(parents=True)
        (self.idea / "artifact.md").write_text("artifact\n", encoding="utf-8")
        self.module = load_module()

    def tearDown(self):
        self.tempdir.cleanup()

    def test_minimal_idea_is_valid(self):
        errors: list[str] = []
        warnings: list[str] = []
        self.module.validate_current_md(self.idea, errors, warnings)
        self.module.validate_project_state(self.idea, errors, warnings)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_long_current_is_error(self):
        current = self.idea / "notes" / "CURRENT.md"
        current.write_text(
            "\n".join(["phase: writing", "next_action: compile"] + [f"x{i}: y" for i in range(16)]),
            encoding="utf-8",
        )
        errors: list[str] = []
        warnings: list[str] = []
        self.module.validate_current_md(self.idea, errors, warnings)
        self.assertTrue(any("maximum is 15" in error for error in errors))

    def test_required_current_rejects_unknown_top_level_field(self):
        (self.idea / "notes" / "CURRENT.md").write_text(
            "phase: writing\n"
            "active_artifact: artifact.md\n"
            "current_result: draft exists\n"
            "validation: passed\n"
            "open_blockers: none\n"
            "next_action: compile\n"
            "last_updated: today\n",
            encoding="utf-8",
        )
        errors: list[str] = []
        warnings: list[str] = []

        self.module.validate_current_md(
            self.idea,
            errors,
            warnings,
            required=True,
            allowed_root=Path(self.tempdir.name),
        )

        self.assertTrue(any("unknown top-level field 'validation'" in error for error in errors))

    def test_required_current_allows_indented_continuations(self):
        (self.idea / "notes" / "CURRENT.md").write_text(
            "phase: writing\n"
            "active_artifact: artifact.md\n"
            "current_result: draft exists;\n"
            "  no scientific result is claimed yet.\n"
            "open_blockers: none\n"
            "next_action: compile\n"
            "last_updated: today\n",
            encoding="utf-8",
        )
        errors: list[str] = []
        warnings: list[str] = []

        self.module.validate_current_md(
            self.idea,
            errors,
            warnings,
            required=True,
            allowed_root=Path(self.tempdir.name),
        )

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_required_current_rejects_duplicate_field(self):
        (self.idea / "notes" / "CURRENT.md").write_text(
            "phase: writing\n"
            "phase: review\n"
            "active_artifact: artifact.md\n"
            "current_result: draft exists\n"
            "open_blockers: none\n"
            "next_action: compile\n"
            "last_updated: today\n",
            encoding="utf-8",
        )
        errors: list[str] = []
        warnings: list[str] = []

        self.module.validate_current_md(
            self.idea,
            errors,
            warnings,
            required=True,
            allowed_root=Path(self.tempdir.name),
        )

        self.assertTrue(any("duplicate field 'phase'" in error for error in errors))

    def test_required_current_rejects_oversize_file(self):
        (self.idea / "notes" / "CURRENT.md").write_text(
            "phase: writing\n"
            "active_artifact: artifact.md\n"
            f"current_result: {'x' * 2100}\n"
            "open_blockers: none\n"
            "next_action: compile\n"
            "last_updated: today\n",
            encoding="utf-8",
        )
        errors: list[str] = []
        warnings: list[str] = []

        self.module.validate_current_md(
            self.idea,
            errors,
            warnings,
            required=True,
            allowed_root=Path(self.tempdir.name),
        )

        self.assertTrue(any("maximum is 2048 bytes" in error for error in errors))

    def test_nonrequired_current_rejects_legacy_fields(self):
        (self.idea / "notes" / "CURRENT.md").write_text(
            "phase: paused\n"
            "candidate: historical.md\n"
            "gate_status: retired\n"
            "open_blockers: none\n"
            "next_action: none\n"
            "last_updated: today\n",
            encoding="utf-8",
        )
        errors: list[str] = []
        warnings: list[str] = []

        self.module.validate_current_md(
            self.idea,
            errors,
            warnings,
            allowed_root=Path(self.tempdir.name),
        )

        self.assertTrue(any("unknown top-level field 'candidate'" in error for error in errors))
        self.assertTrue(any("unknown top-level field 'gate_status'" in error for error in errors))

    def test_invalid_capability_value_is_error(self):
        (self.idea / "notes" / "capabilities.yaml").write_text(
            "paper_build: sometimes\n", encoding="utf-8"
        )
        errors: list[str] = []
        self.module.validate_capabilities(self.idea, errors)
        self.assertTrue(any("invalid value" in error for error in errors))

    def test_boolean_capability_values_are_supported(self):
        (self.idea / "notes" / "capabilities.yaml").write_text(
            "paper_build: true\nremote_run: false\n", encoding="utf-8"
        )
        errors: list[str] = []
        self.module.validate_capabilities(self.idea, errors)
        self.assertEqual(errors, [])

    def test_active_project_without_project_state_is_warning(self):
        (self.idea / "hypothesis.md").write_text("# Hypothesis\n", encoding="utf-8")
        errors: list[str] = []
        warnings: list[str] = []
        self.module.validate_project_state(self.idea, errors, warnings)
        self.assertEqual(errors, [])
        self.assertTrue(any("missing detailed resume state" in warning for warning in warnings))

    def test_large_required_project_state_is_error(self):
        (self.idea / "notes" / "project-state.md").write_text(
            "# Project State\n" + "\n".join(f"line {index}" for index in range(121)),
            encoding="utf-8",
        )
        errors: list[str] = []
        warnings: list[str] = []

        self.module.validate_project_state(
            self.idea, errors, warnings, required=True
        )

        self.assertTrue(any("maximum is 120" in error for error in errors))

    def test_project_state_rejects_workflow_control_metadata(self):
        (self.idea / "notes" / "project-state.md").write_text(
            "# Project State\n\n## Harness State Repair\n\n"
            "Current routing:\n\n- next skill: paper-story-framer\n"
            "- gate status: blocked\n\n"
            "Update the session manifest with scientific_state_changed.\n",
            encoding="utf-8",
        )
        errors: list[str] = []
        warnings: list[str] = []

        self.module.validate_project_state(
            self.idea, errors, warnings, required=True
        )

        self.assertTrue(any("workflow-control heading" in error for error in errors))
        self.assertTrue(any("runtime routing field" in error for error in errors))
        self.assertTrue(any("session manifest contract" in error for error in errors))

    def test_conflicting_resume_phases_are_warning_not_error(self):
        (self.idea / "notes" / "CURRENT.md").write_text(
            "phase: reviewer-package-review\nnext_action: inspect\nlast_updated: today\n",
            encoding="utf-8",
        )
        (self.idea / "notes" / "project-state.md").write_text(
            "# Project State\n\n## Current Phase\n\n- Current phase: `portal-metadata-pending`\n",
            encoding="utf-8",
        )
        warnings: list[str] = []

        self.module.validate_resume_semantics(self.idea, warnings)

        self.assertEqual(len(warnings), 1)
        self.assertIn("resolve authority before resuming", warnings[0])

    def test_matching_resume_phases_have_no_semantic_warning(self):
        (self.idea / "notes" / "CURRENT.md").write_text(
            "phase: active-writing\nnext_action: compile\nlast_updated: today\n",
            encoding="utf-8",
        )
        (self.idea / "notes" / "project-state.md").write_text(
            "# Project State\n\n- 当前 phase: `active-writing`\n",
            encoding="utf-8",
        )
        warnings: list[str] = []

        self.module.validate_resume_semantics(self.idea, warnings)

        self.assertEqual(warnings, [])

    def test_required_resume_files_are_errors_when_missing(self):
        errors: list[str] = []
        warnings: list[str] = []

        self.module.validate_current_md(
            self.idea, errors, warnings, required=True
        )
        self.module.validate_project_state(
            self.idea, errors, warnings, required=True
        )

        self.assertTrue(any("missing canonical resume state" in error for error in errors))
        self.assertTrue(any("missing detailed resume state" in error for error in errors))

    def test_competing_current_is_error_for_required_state(self):
        (self.idea / "notes" / "CURRENT.md").write_text(
            "phase: ideation\nnext_action: test\nlast_updated: today\n",
            encoding="utf-8",
        )
        (self.idea / "notes" / "CURRENT 2.md").write_text(
            "old state\n", encoding="utf-8"
        )
        errors: list[str] = []
        warnings: list[str] = []

        self.module.validate_current_md(
            self.idea, errors, warnings, required=True
        )

        self.assertTrue(any("competing resume filename" in error for error in errors))

    def test_missing_active_artifact_is_error(self):
        (self.idea / "notes" / "CURRENT.md").write_text(
            "phase: ideation\n"
            "active_artifact: missing.md\n"
            "next_action: test\n"
            "last_updated: today\n",
            encoding="utf-8",
        )
        errors: list[str] = []
        warnings: list[str] = []

        self.module.validate_current_md(
            self.idea,
            errors,
            warnings,
            required=True,
            allowed_root=Path(self.tempdir.name),
        )

        self.assertTrue(any("points to missing artifact" in error for error in errors))

    def test_active_artifact_rejects_directory(self):
        (self.idea / "notes" / "CURRENT.md").write_text(
            "phase: ideation\n"
            "active_artifact: notes\n"
            "current_result: ready\n"
            "open_blockers: none\n"
            "next_action: test\n"
            "last_updated: today\n",
            encoding="utf-8",
        )
        errors: list[str] = []
        warnings: list[str] = []

        self.module.validate_current_md(
            self.idea,
            errors,
            warnings,
            required=True,
            allowed_root=Path(self.tempdir.name),
        )

        self.assertTrue(any("must point to one regular file" in error for error in errors))

    def test_active_artifact_rejects_large_file(self):
        large = self.idea / "large.md"
        large.write_text("x" * (self.module.ACTIVE_ARTIFACT_MAX_BYTES + 1), encoding="utf-8")
        (self.idea / "notes" / "CURRENT.md").write_text(
            "phase: ideation\n"
            "active_artifact: large.md\n"
            "current_result: ready\n"
            "open_blockers: none\n"
            "next_action: test\n"
            "last_updated: today\n",
            encoding="utf-8",
        )
        errors: list[str] = []
        warnings: list[str] = []

        self.module.validate_current_md(
            self.idea,
            errors,
            warnings,
            required=True,
            allowed_root=Path(self.tempdir.name),
        )

        self.assertTrue(any("maximum is 65536 bytes" in error for error in errors))

    def test_live_legacy_artifacts_are_rejected_but_history_is_ignored(self):
        (self.idea / "notes" / "research-pipeline 2.md").write_text(
            "legacy\n", encoding="utf-8"
        )
        history = self.idea / "notes" / "history"
        history.mkdir()
        (history / "review-state.json").write_text("{}\n", encoding="utf-8")
        errors: list[str] = []

        self.module.validate_live_legacy_artifacts(self.idea, errors)

        self.assertEqual(len(errors), 1)
        self.assertIn("research-pipeline 2.md", errors[0])

    def test_todo_is_bounded_and_unique(self):
        (self.idea / "TODO.md").write_text("- root\n", encoding="utf-8")
        (self.idea / "notes" / "TODO.md").write_text("- notes\n", encoding="utf-8")
        errors: list[str] = []

        self.module.validate_todo(self.idea, errors)

        self.assertTrue(any("only one lightweight TODO.md" in error for error in errors))

    def test_registry_identity_rejects_active_status_without_pointer(self):
        topic = Path(self.tempdir.name) / "topic"
        idea = topic / "ideas" / "i001"
        idea.mkdir(parents=True)
        (idea / "idea.md").write_text("# Idea\n", encoding="utf-8")
        (topic / "ideas" / "registry.yaml").write_text(
            "active_id: null\n"
            "active_entry: null\n"
            "ideas:\n"
            "  - id: i001\n"
            "    title: Example\n"
            "    slug: example\n"
            "    status: active\n"
            "    canonical_dir: ideas/i001\n",
            encoding="utf-8",
        )
        errors: list[str] = []
        warnings: list[str] = []

        self.module.validate_registry_identity(idea, errors, warnings)

        self.assertTrue(any("active_id is null" in error for error in errors))

    def test_main_returns_zero_for_minimal_idea(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(
            sys,
            "argv",
            ["validate_research_workflow.py", "--idea", str(self.idea)],
        ):
            with mock.patch.object(self.module, "validate_skill_policy"):
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    rc = self.module.main()
        self.assertEqual(rc, 0, stderr.getvalue())
        self.assertIn("validation passed", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
