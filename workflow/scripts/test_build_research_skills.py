import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parent / "build_research_skills.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "build_research_skills_under_test", MODULE_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class BuildResearchSkillsTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.workflow_root = self.root / "workflow"
        self.skills_dir = self.workflow_root / "skills"
        self.shared_dir = self.skills_dir / "_shared"
        self.shared_dir.mkdir(parents=True)
        self.research_root = self.root
        self.agents_path = self.research_root / "AGENTS.md"
        self.agents_path.write_text("manual agents instructions\n", encoding="utf-8")

        skill_dir = self.skills_dir / "research-ideation" / "paper-to-markdown"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            """---
name: paper-to-markdown
description: Use when a PDF should become markdown.
---

# Paper to Markdown

## Consume
- `source.pdf`

## Produce
- `paper.md`

## Boundaries
- Use $paper-summary-writer only for a separately requested summary.
""",
            encoding="utf-8",
        )

    def tearDown(self):
        self.tempdir.cleanup()

    def patch_paths(self, module):
        module.WORKFLOW_ROOT = self.workflow_root
        module.RESEARCH_ROOT = self.research_root
        module.SKILLS_DIR = self.skills_dir
        module.SHARED_DIR = self.shared_dir
        module.CATALOG_PATH = self.shared_dir / "skill-catalog.json"
        module.OUTPUT_MAP_PATH = self.shared_dir / "skill-output-map.md"
        module.AGENTS_PATH = self.agents_path

    def test_build_generates_catalog_output_map_and_agent_yaml(self):
        module = load_module()
        self.patch_paths(module)

        module.build()

        catalog = json.loads(module.CATALOG_PATH.read_text(encoding="utf-8"))
        self.assertEqual(catalog[0]["name"], "paper-to-markdown")
        self.assertEqual(catalog[0]["part"], "research-ideation")
        self.assertEqual(catalog[0]["produces"], ["`paper.md`"])
        self.assertEqual(
            catalog[0]["path"],
            "workflow/skills/research-ideation/paper-to-markdown/SKILL.md",
        )

        output_map = module.OUTPUT_MAP_PATH.read_text(encoding="utf-8")
        self.assertIn("`paper.md` -> `paper-to-markdown`", output_map)

        agent_yaml = (
            self.skills_dir
            / "research-ideation"
            / "paper-to-markdown"
            / "agents"
            / "openai.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn('display_name: "Paper to Markdown"', agent_yaml)
        self.assertIn("Use $paper-to-markdown to help with this task.", agent_yaml)

    def test_build_leaves_manual_agents_md_untouched(self):
        module = load_module()
        self.patch_paths(module)

        before = self.agents_path.read_text(encoding="utf-8")
        module.build()
        after = self.agents_path.read_text(encoding="utf-8")

        self.assertEqual(after, before)

    def test_build_preserves_existing_invocation_policy(self):
        module = load_module()
        self.patch_paths(module)
        skill_path = (
            self.skills_dir
            / "research-ideation"
            / "paper-to-markdown"
            / "SKILL.md"
        )
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace(
                "description: Use when a PDF should become markdown.",
                "description: Trigger only when the user explicitly asks to convert a PDF.",
            ),
            encoding="utf-8",
        )
        agents_dir = (
            self.skills_dir
            / "research-ideation"
            / "paper-to-markdown"
            / "agents"
        )
        agents_dir.mkdir(parents=True)
        (agents_dir / "openai.yaml").write_text(
            """interface:
  display_name: "Paper to Markdown"
  short_description: "Convert a paper PDF to Markdown"
  default_prompt: "Use $paper-to-markdown to convert this PDF."
policy:
  allow_implicit_invocation: false
""",
            encoding="utf-8",
        )

        module.build()

        agent_yaml = (agents_dir / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn(
            "policy:\n  allow_implicit_invocation: false\n",
            agent_yaml,
        )

    def test_explicit_only_description_requires_matching_agent_policy(self):
        module = load_module()
        self.patch_paths(module)
        skill_path = (
            self.skills_dir
            / "research-ideation"
            / "paper-to-markdown"
            / "SKILL.md"
        )
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace(
                "description: Use when a PDF should become markdown.",
                "description: Explicit-only. Trigger only when the user explicitly asks.",
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(SystemExit, "explicit-only invocation"):
            module.build()

    def test_disabled_implicit_invocation_requires_explicit_description(self):
        module = load_module()
        self.patch_paths(module)
        agents_dir = (
            self.skills_dir
            / "research-ideation"
            / "paper-to-markdown"
            / "agents"
        )
        agents_dir.mkdir(parents=True)
        (agents_dir / "openai.yaml").write_text(
            """interface:
  display_name: "Paper to Markdown"
  short_description: "Convert a paper PDF to Markdown"
  default_prompt: "Use $paper-to-markdown to convert this PDF."
policy:
  allow_implicit_invocation: false
""",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(SystemExit, "does not declare an explicit-only"):
            module.build()

    def test_build_drops_stale_catalog_routes(self):
        module = load_module()
        self.patch_paths(module)
        module.CATALOG_PATH.write_text(
            json.dumps(
                [
                    {
                        "part": "research-ideation",
                        "category": "Flow Support",
                        "name": "paper-to-markdown",
                        "title": "Paper to Markdown",
                        "description": "Use when a PDF should become markdown.",
                        "path": str(
                            self.skills_dir
                            / "research-ideation"
                            / "paper-to-markdown"
                            / "SKILL.md"
                        ),
                        "consumes": ["`source.pdf`"],
                        "produces": ["`paper.md`"],
                        "next_skills": [
                            "$existing-conditional-route",
                            "$paper-summary-writer",
                        ],
                    }
                ],
                indent=2,
            ),
            encoding="utf-8",
        )

        module.build()

        catalog = json.loads(module.CATALOG_PATH.read_text(encoding="utf-8"))
        self.assertNotIn("next_skills", catalog[0])

    def test_build_maps_every_real_produce_path_and_skips_mode_tokens(self):
        module = load_module()
        self.patch_paths(module)
        skill_path = (
            self.skills_dir
            / "research-ideation"
            / "paper-to-markdown"
            / "SKILL.md"
        )
        text = skill_path.read_text(encoding="utf-8").replace(
            "- `paper.md`",
            "- `paper.md` and `figures/index.json` in `preview` mode",
        )
        skill_path.write_text(text, encoding="utf-8")

        module.build()

        output_map = module.OUTPUT_MAP_PATH.read_text(encoding="utf-8")
        self.assertIn("`paper.md` -> `paper-to-markdown`", output_map)
        self.assertIn("`figures/index.json` -> `paper-to-markdown`", output_map)
        self.assertNotIn("`preview` ->", output_map)

    def test_infer_category_repairs_cross_part_stale_value(self):
        module = load_module()

        category = module.infer_category(
            "paper-story-framer",
            "paper-writing",
            {"category": "Standalone Utility"},
        )

        self.assertEqual(category, "Writing and Submission")

    def test_architecture_rejects_meta_skills_and_meta_state_artifacts(self):
        module = load_module()
        skills = [
            {
                "name": "phase-entry",
                "part": "research-ideation",
                "next_skills": [],
                "produce_refs": [
                    "notes/research-pipeline.md",
                    "paper/review-state.json",
                    "notes/plan-tree.md",
                    "paper/promotion-gate-result.md",
                    "notes/session-proposals/request.md",
                ],
                "consume_refs": ["experiments/plans/milestone-plan.md"],
            },
        ]

        errors = module.skill_architecture_errors(skills)

        self.assertTrue(any("meta-workflow Skill names" in error for error in errors))
        self.assertTrue(
            any("meta-state artifact" in error for error in errors)
        )
        self.assertTrue(any("review-state.json" in error for error in errors))
        self.assertTrue(any("plan-tree.md" in error for error in errors))
        self.assertTrue(any("promotion-gate-result.md" in error for error in errors))
        self.assertTrue(any("session-proposals" in error for error in errors))

    def test_architecture_rejects_machine_router_fields(self):
        module = load_module()
        errors = module.skill_architecture_errors(
            [
                {
                    "name": "leaf",
                    "part": "research-ideation",
                    "next_skills": ["$one"],
                    "produce_refs": ["artifact.md"],
                }
            ]
        )

        self.assertTrue(any("retired router field" in error for error in errors))

    def test_architecture_rejects_handoff_sections_and_router_docs(self):
        module = load_module()
        errors = module.skill_architecture_errors(
            [
                {
                    "name": "leaf",
                    "part": "research-ideation",
                    "produce_refs": ["artifact.md"],
                    "_text": (
                        "## Handoff\n- Pass onward.\n"
                        "Read `../../_shared/workflow-map.md`.\n"
                    ),
                }
            ]
        )

        self.assertTrue(any("Handoff sections are retired" in error for error in errors))
        self.assertTrue(any("retired routing reference" in error for error in errors))

    def test_architecture_does_not_impose_catalog_wide_count_or_size_caps(self):
        module = load_module()
        skills = [
            {
                "name": f"leaf-{index}",
                "part": "research-ideation",
                "produce_refs": [f"artifacts/{index}.md"],
                "_skill_bytes": 2048,
            }
            for index in range(160)
        ]
        errors = module.skill_architecture_errors(skills)

        self.assertEqual(errors, [])

    def test_resume_artifact_map_uses_direct_owner_contract(self):
        module = load_module()
        skills = [
            {
                "name": "idea-backlog-manager",
                "part": "research-ideation",
                "produces": [
                    "`notes/CURRENT.md`",
                    "`notes/project-state.md`",
                ],
            },
            {
                "name": "run-experiment",
                "part": "paper-writing",
                "produces": ["`notes/CURRENT.md`"],
            },
        ]
        owners = {
            "notes/CURRENT.md": [
                "idea-backlog-manager",
                "run-experiment",
            ],
            "notes/project-state.md": ["idea-backlog-manager"],
        }

        output_map = module.render_output_map(skills, owners)
        artifact_section = output_map.split("## By Artifact", 1)[1]

        self.assertIn(
            "- `notes/CURRENT.md` -> `idea-backlog-manager` at activation; "
            "thereafter the active artifact owner under the fixed resume contract",
            artifact_section,
        )
        self.assertIn(
            "- `notes/project-state.md` -> `idea-backlog-manager` at activation; "
            "thereafter the active artifact owner when scientific state "
            "materially changes",
            artifact_section,
        )
        self.assertNotIn("run-experiment", artifact_section)


if __name__ == "__main__":
    unittest.main()
