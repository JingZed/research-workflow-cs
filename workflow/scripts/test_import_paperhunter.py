import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parent / "import_paperhunter.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "import_paperhunter_under_test", MODULE_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ImportPaperHunterTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def write_json(self, path: Path, payload):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def read_jsonl(self, path: Path):
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_imports_favorites_as_untriaged_leads(self):
        module = load_module()
        library_path = self.root / "PaperHunter" / "data" / "library.json"
        leads_path = self.root / "discovery" / "paper-leads.jsonl"
        self.write_json(
            library_path,
            {
                "favorites": {
                    "2503.07003": {
                        "paper": {
                            "title": "Large Language Models Often Say One Thing and Do Another",
                            "authors": "Alice Smith, Bob Jones",
                            "year": 2025,
                            "venue": "ICLR 2025",
                            "paperId": "2503.07003",
                            "arxivId": "2503.07003",
                            "source": "arxiv",
                            "pageUrl": "https://arxiv.org/abs/2503.07003",
                            "pdfUrl": "https://arxiv.org/pdf/2503.07003.pdf",
                            "fullAbstract": "A full abstract.",
                        }
                    }
                }
            },
        )

        stats = module.import_paperhunter_library(library_path, leads_path, scope="favorites")

        rows = self.read_jsonl(leads_path)
        self.assertEqual(stats["added"], 1)
        self.assertEqual(rows[0]["paper_id"], "2503.07003")
        self.assertEqual(rows[0]["arxiv_id"], "2503.07003")
        self.assertEqual(rows[0]["triage_status"], "untriaged")
        self.assertEqual(rows[0]["access_status"], "downloadable")
        self.assertEqual(rows[0]["source_provenance"][0]["provider"], "paperhunter:arxiv")
        self.assertEqual(rows[0]["abstract"], "A full abstract.")

    def test_skips_entries_already_known_in_topic_corpus(self):
        module = load_module()
        library_path = self.root / "PaperHunter" / "data" / "library.json"
        leads_path = self.root / "discovery" / "paper-leads.jsonl"
        corpus_path = self.root / "synthesis" / "literature-corpus.jsonl"
        self.write_json(
            library_path,
            {
                "downloads": {
                    "known": {
                        "filename": "Known Paper (2503.07003).pdf",
                        "paper": {
                            "title": "Known Paper",
                            "authors": "Alice Smith",
                            "year": 2025,
                            "paperId": "2503.07003",
                            "arxivId": "2503.07003",
                            "source": "arxiv",
                            "pdfUrl": "https://arxiv.org/pdf/2503.07003.pdf",
                            "pageUrl": "https://arxiv.org/abs/2503.07003",
                        },
                    }
                }
            },
        )
        corpus_path.parent.mkdir(parents=True, exist_ok=True)
        corpus_path.write_text(
            json.dumps(
                {
                    "paper_id": "2503.07003",
                    "arxiv_id": "2503.07003",
                    "title": "Known Paper",
                    "authors": ["Smith, Alice"],
                    "venue": None,
                    "year": 2025,
                    "relevant_to": ["background"],
                    "summary_path": None,
                    "read_status": "unread",
                    "read_basis": "title/abstract only",
                    "pdf_path": None,
                    "notes": None,
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        stats = module.import_paperhunter_library(
            library_path,
            leads_path,
            scope="downloads",
            corpus_path=corpus_path,
        )

        self.assertEqual(stats["added"], 0)
        self.assertEqual(stats["skipped_known"], 1)
        self.assertFalse(leads_path.exists())


if __name__ == "__main__":
    unittest.main()
