#!/usr/bin/env python3
"""CLI helper for searching and downloading arXiv papers.

Adapted for this workspace from:
https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep
Repository license: MIT
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ATOM_NS = "http://www.w3.org/2005/Atom"
API_BASE = "http://export.arxiv.org/api/query"
USER_AGENT = "research-workflow/1.0 (local arxiv helper)"
MIN_PDF_BYTES = 10_240
NEW_STYLE_ID_RE = re.compile(r"^\d{4}\.\d{4,5}(v\d+)?$")
OLD_STYLE_ID_RE = re.compile(r"^[A-Za-z.-]+/\d{7}(v\d+)?$")


def normalize_id(arxiv_id: str) -> str:
    value = arxiv_id.strip()
    if "/abs/" in value:
        value = value.split("/abs/", 1)[1]
    if "/pdf/" in value:
        value = value.split("/pdf/", 1)[1]
    if value.startswith("id:"):
        value = value[3:]
    if value.endswith(".pdf"):
        value = value[:-4]
    if "v" in value.split(".")[-1]:
        value = value.rsplit("v", 1)[0]
    return value


def looks_like_arxiv_id(value: str) -> bool:
    value = value.strip()
    return bool(NEW_STYLE_ID_RE.match(value) or OLD_STYLE_ID_RE.match(value))


def build_api_url(query: str, max_results: int, start: int) -> str:
    query = query.strip()
    if query.startswith("id:") or looks_like_arxiv_id(query):
        params = {"id_list": normalize_id(query)}
    else:
        params = {
            "search_query": query,
            "start": start,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }
    return f"{API_BASE}?{urllib.parse.urlencode(params)}"


def fetch_atom(url: str) -> ET.Element:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return ET.fromstring(resp.read())


def parse_entry(entry: ET.Element) -> dict[str, object]:
    raw_id = entry.findtext(f"{{{ATOM_NS}}}id", "")
    arxiv_id = normalize_id(raw_id)
    title = (entry.findtext(f"{{{ATOM_NS}}}title", "") or "").strip().replace("\n", " ")
    abstract = (entry.findtext(f"{{{ATOM_NS}}}summary", "") or "").strip().replace("\n", " ")
    published = (entry.findtext(f"{{{ATOM_NS}}}published", "") or "")[:10]
    updated = (entry.findtext(f"{{{ATOM_NS}}}updated", "") or "")[:10]
    authors = [
        author.findtext(f"{{{ATOM_NS}}}name", "")
        for author in entry.findall(f"{{{ATOM_NS}}}author")
    ]
    categories = [
        category.get("term", "")
        for category in entry.findall(f"{{{ATOM_NS}}}category")
        if category.get("term")
    ]
    return {
        "id": arxiv_id,
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "published": published,
        "updated": updated,
        "categories": categories,
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        "abs_url": f"https://arxiv.org/abs/{arxiv_id}",
    }


def search(query: str, max_results: int = 10, start: int = 0) -> list[dict[str, object]]:
    root = fetch_atom(build_api_url(query, max_results=max_results, start=start))
    return [parse_entry(entry) for entry in root.findall(f"{{{ATOM_NS}}}entry")]


def download(arxiv_id: str, output_dir: str = "papers") -> dict[str, object]:
    clean_id = normalize_id(arxiv_id)
    safe_id = clean_id.replace("/", "_")

    dest_dir = Path(output_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{safe_id}.pdf"

    if dest.exists():
        return {
            "id": clean_id,
            "path": str(dest),
            "size_kb": dest.stat().st_size // 1024,
            "skipped": True,
        }

    pdf_url = f"https://arxiv.org/pdf/{clean_id}.pdf"
    req = urllib.request.Request(pdf_url, headers={"User-Agent": USER_AGENT})

    data: bytes | None = None
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            break
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt == 1:
                time.sleep(5)
                continue
            raise

    if data is None:
        raise RuntimeError(f"Failed to download {pdf_url}")
    if len(data) < MIN_PDF_BYTES:
        raise ValueError(
            f"Downloaded file is only {len(data)} bytes; likely an error page, not a PDF"
        )

    dest.write_bytes(data)
    return {
        "id": clean_id,
        "path": str(dest),
        "size_kb": len(data) // 1024,
        "skipped": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search and download arXiv papers.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search arXiv papers")
    search_parser.add_argument("query", help="Search query or arXiv ID")
    search_parser.add_argument("--max", type=int, default=10, metavar="N")
    search_parser.add_argument("--start", type=int, default=0)

    download_parser = subparsers.add_parser("download", help="Download an arXiv PDF")
    download_parser.add_argument("id", help="arXiv paper ID, e.g. 2301.07041")
    download_parser.add_argument("--dir", default="papers", metavar="DIR")
    download_parser.add_argument("--delay", type=float, default=1.0)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "search":
        print(json.dumps(search(args.query, max_results=args.max, start=args.start), ensure_ascii=False, indent=2))
        return 0

    if args.command == "download":
        result = download(args.id, output_dir=args.dir)
        if not result.get("skipped"):
            time.sleep(args.delay)
        print(json.dumps(result, ensure_ascii=False))
        return 0

    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    sys.exit(main())
