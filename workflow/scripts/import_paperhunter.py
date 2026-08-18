#!/usr/bin/env python3
"""Import PaperHunter library entries into the research workflow leads file."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ARXIV_ID_RE = re.compile(r"\b(\d{4}\.\d{4,5})(?:v\d+)?\b")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSONL row: {exc}") from exc
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )


def normalize_text(value: object) -> str:
    return " ".join(str(value or "").split())


def normalize_title(value: object) -> str:
    return normalize_text(value).casefold()


def extract_arxiv_id(*values: object) -> str | None:
    for value in values:
        match = ARXIV_ID_RE.search(str(value or ""))
        if match:
            return match.group(1)
    return None


def stable_paper_id(paper: dict[str, Any]) -> str:
    arxiv_id = extract_arxiv_id(
        paper.get("arxivId"),
        paper.get("paperId"),
        paper.get("pageUrl"),
        paper.get("entryUrl"),
        paper.get("pdfUrl"),
    )
    if arxiv_id:
        return arxiv_id
    for field in ("paperId", "arxivId"):
        value = normalize_text(paper.get(field))
        if value:
            return value.replace("/", "_")
    title_slug = re.sub(r"[^a-z0-9]+", "-", normalize_title(paper.get("title"))).strip("-")
    return title_slug[:80] or "unknown-paper"


def paper_year(paper: dict[str, Any]) -> int | None:
    for field in ("year", "published"):
        value = paper.get(field)
        if isinstance(value, int):
            return value
        match = re.search(r"\b(19|20)\d{2}\b", str(value or ""))
        if match:
            return int(match.group(0))
    return None


def collect_papers(library: dict[str, Any], scope: str) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    scopes = ("favorites", "downloads") if scope == "all" else (scope,)
    collected: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for section in scopes:
        entries = library.get(section) or {}
        if not isinstance(entries, dict):
            continue
        for entry in entries.values():
            if not isinstance(entry, dict) or not isinstance(entry.get("paper"), dict):
                continue
            collected.append((entry["paper"], {"section": section, **entry}))
    return collected


def known_keys(rows: list[dict[str, Any]]) -> set[str]:
    keys: set[str] = set()
    for row in rows:
        for field in ("paper_id", "arxiv_id"):
            value = normalize_text(row.get(field))
            if value:
                keys.add(f"{field}:{value.casefold()}")
        title = normalize_title(row.get("title"))
        if title:
            keys.add(f"title:{title}")
    return keys


def row_keys(row: dict[str, Any]) -> set[str]:
    keys = set()
    for field in ("paper_id", "arxiv_id"):
        value = normalize_text(row.get(field))
        if value:
            keys.add(f"{field}:{value.casefold()}")
    title = normalize_title(row.get("title"))
    if title:
        keys.add(f"title:{title}")
    return keys


def provenance(paper: dict[str, Any], entry: dict[str, Any]) -> list[dict[str, str]]:
    source = normalize_text(paper.get("source")) or "unknown"
    items: list[dict[str, str]] = []
    for field in ("pageUrl", "entryUrl", "pdfUrl"):
        url = normalize_text(paper.get(field))
        if url:
            items.append(
                {
                    "provider": f"paperhunter:{source}",
                    "evidence_url": url,
                    "kind": field,
                }
            )
    filename = normalize_text(entry.get("filename"))
    if filename:
        items.append(
            {
                "provider": "paperhunter:downloaded_papers",
                "evidence_url": filename,
                "kind": "downloaded_filename",
            }
        )
    return items


def paperhunter_to_lead(paper: dict[str, Any], entry: dict[str, Any]) -> dict[str, Any]:
    pdf_url = normalize_text(paper.get("pdfUrl"))
    is_downloaded = bool(paper.get("isDownloaded") or entry.get("filename"))
    paper_id = stable_paper_id(paper)
    arxiv_id = extract_arxiv_id(paper_id, paper.get("arxivId"), paper.get("paperId"))
    return {
        "paper_id": paper_id,
        "arxiv_id": arxiv_id,
        "title": normalize_text(paper.get("title")) or "Untitled",
        "authors": normalize_text(paper.get("authors")) or None,
        "year": paper_year(paper),
        "venue": normalize_text(paper.get("venue") or paper.get("sourceLabel")) or None,
        "source": normalize_text(paper.get("source")) or "paperhunter",
        "abstract": normalize_text(paper.get("fullAbstract") or paper.get("abstract")) or None,
        "discovery_status": "discovered",
        "triage_status": "untriaged",
        "access_status": "downloaded" if is_downloaded else ("downloadable" if pdf_url else "unresolved"),
        "import_source": "paperhunter",
        "source_provenance": provenance(paper, entry),
    }


def import_paperhunter_library(
    library_path: Path,
    leads_path: Path,
    *,
    scope: str = "favorites",
    corpus_path: Path | None = None,
) -> dict[str, int]:
    library = load_json(library_path)
    existing_leads = read_jsonl(leads_path)
    corpus_rows = read_jsonl(corpus_path) if corpus_path else []
    existing = known_keys(existing_leads)
    known_in_corpus = known_keys(corpus_rows)

    added_rows: list[dict[str, Any]] = []
    skipped_known = 0
    skipped_duplicate = 0
    for paper, entry in collect_papers(library, scope):
        row = paperhunter_to_lead(paper, entry)
        keys = row_keys(row)
        if keys & known_in_corpus:
            skipped_known += 1
            continue
        if keys & existing or any(keys & row_keys(added) for added in added_rows):
            skipped_duplicate += 1
            continue
        added_rows.append(row)

    if added_rows:
        write_jsonl(leads_path, existing_leads + added_rows)

    return {
        "seen": len(collect_papers(library, scope)),
        "added": len(added_rows),
        "skipped_known": skipped_known,
        "skipped_duplicate": skipped_duplicate,
        "total_leads": len(existing_leads) + len(added_rows),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Import PaperHunter data/library.json into paper-leads.jsonl."
    )
    parser.add_argument("library_json", type=Path, help="Path to PaperHunter data/library.json")
    parser.add_argument("paper_leads_jsonl", type=Path, help="Target paper-leads.jsonl")
    parser.add_argument(
        "--scope",
        choices=("favorites", "downloads", "all"),
        default="favorites",
        help="Which PaperHunter inbox section to import",
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        help="Optional topic synthesis/literature-corpus.jsonl for deduplication",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    stats = import_paperhunter_library(
        args.library_json,
        args.paper_leads_jsonl,
        scope=args.scope,
        corpus_path=args.corpus,
    )
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
