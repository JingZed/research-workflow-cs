import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parent / "seed_candidates_for_po.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "seed_candidates_for_po_under_test", MODULE_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SeedCandidatesForPoTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tempdir.name) / "workspace"
        self.workspace.mkdir(parents=True)

    def tearDown(self):
        self.tempdir.cleanup()

    def write_json(self, path: Path, payload):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def read_json(self, path: Path):
        return json.loads(path.read_text(encoding="utf-8"))

    def test_creates_raw_candidates_when_missing(self):
        module = load_module()
        seed_path = self.workspace / "seeded_candidates.json"
        self.write_json(
            seed_path,
            {
                "candidates": [
                    {
                        "title": "Paper A",
                        "url": "https://arxiv.org/abs/1234.5678",
                        "snippet": "seeded",
                        "discovered_for": ["related_work[2.1]"],
                    }
                ]
            },
        )

        module.seed_candidates_into_workspace(self.workspace)

        raw = self.read_json(self.workspace / "raw_candidates.json")
        self.assertEqual(raw["seeded_count"], 1)
        self.assertEqual(raw["existing_count"], 0)
        self.assertEqual(raw["merged_count"], 1)
        self.assertEqual(raw["candidates"][0]["title"], "Paper A")

    def test_merges_seeded_candidates_with_existing_raw_candidates(self):
        module = load_module()
        self.write_json(
            self.workspace / "raw_candidates.json",
            {
                "candidates": [
                    {
                        "title": "Existing Paper",
                        "url": "https://example.com/existing",
                        "snippet": "raw",
                        "discovered_for": ["intro.1"],
                    }
                ]
            },
        )
        self.write_json(
            self.workspace / "seeded_candidates.json",
            {
                "candidates": [
                    {
                        "title": "Seeded Paper",
                        "url": "https://example.com/seeded",
                        "snippet": "seed",
                        "discovered_for": ["related_work[2.1]"],
                    }
                ]
            },
        )

        module.seed_candidates_into_workspace(self.workspace)

        raw = self.read_json(self.workspace / "raw_candidates.json")
        titles = [item["title"] for item in raw["candidates"]]
        self.assertEqual(titles, ["Existing Paper", "Seeded Paper"])
        self.assertEqual(raw["existing_count"], 1)
        self.assertEqual(raw["seeded_count"], 1)
        self.assertEqual(raw["merged_count"], 2)


if __name__ == "__main__":
    unittest.main()
