#!/usr/bin/env python3
"""Fetch a paper PDF into the canonical source.pdf slot using Semantic Scholar first."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import requests

from semantic_scholar_client import SemanticScholarClient


def looks_like_doi(value: str) -> bool:
    return value.startswith("10.")


def extract_arxiv_id(value: str) -> str | None:
    m = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", value.strip())
    return m.group(1) if m else None


def to_s2_paper_id(identifier: str) -> str | None:
    identifier = identifier.strip()
    if looks_like_doi(identifier):
        return f"DOI:{identifier}"
    arxiv_id = extract_arxiv_id(identifier)
    if arxiv_id:
        return f"ARXIV:{arxiv_id}"
    if identifier.lower().startswith("corpusid:"):
        return identifier
    if identifier.isdigit():
        return f"CorpusId:{identifier}"
    return None


def download_pdf(url: str, dest: Path) -> tuple[bool, str]:
    try:
        with requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=60,
            stream=True,
            allow_redirects=True,
        ) as resp:
            resp.raise_for_status()
            with dest.open("wb") as fh:
                for chunk in resp.iter_content(chunk_size=1024 * 128):
                    if chunk:
                        fh.write(chunk)
        with dest.open("rb") as fh:
            sig = fh.read(4)
        if sig != b"%PDF":
            dest.unlink(missing_ok=True)
            return False, "downloaded file is not a PDF"
        return True, ""
    except Exception as exc:
        dest.unlink(missing_ok=True)
        return False, str(exc)


def resolve_metadata(client: SemanticScholarClient, identifier: str, title: str | None) -> dict[str, Any]:
    paper_id = to_s2_paper_id(identifier)
    fields = "title,year,venue,url,openAccessPdf,externalIds"
    if paper_id:
        return client.get_paper(paper_id, fields=fields)
    query = title or identifier
    data = client.search_paper(query, limit=5, fields=fields)
    rows = data.get("data", [])
    if not rows:
        raise RuntimeError("Semantic Scholar search returned no candidates")
    return rows[0]


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch a paper PDF using Semantic Scholar metadata first.")
    parser.add_argument("identifier", help="DOI, arXiv ID, CorpusId, URL, or title")
    parser.add_argument("target_dir", help="Target paper workspace directory")
    parser.add_argument("--title", help="Optional explicit title for search fallback")
    args = parser.parse_args()

    target_dir = Path(args.target_dir).expanduser().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    source_pdf = target_dir / "source.pdf"
    report_path = target_dir / "download-report.md"

    report: list[str] = ["# Download Report", "", f"- identifier: `{args.identifier}`"]
    attempts: list[tuple[str, str]] = []
    metadata: dict[str, Any] | None = None

    client = SemanticScholarClient()
    try:
        metadata = resolve_metadata(client, args.identifier, args.title)
        report.extend(
            [
                f"- semantic scholar title: `{metadata.get('title', 'unknown')}`",
                f"- semantic scholar venue: `{metadata.get('venue', 'unknown')}`",
                f"- semantic scholar year: `{metadata.get('year', 'unknown')}`",
            ]
        )
    except Exception as exc:
        report.append(f"- semantic scholar resolution: failed ({exc})")

    candidate_urls: list[tuple[str, str]] = []
    if metadata:
        oa = (metadata.get("openAccessPdf") or {}).get("url")
        if oa:
            candidate_urls.append(("semantic scholar openAccessPdf", oa))
        external_ids = metadata.get("externalIds") or {}
        arxiv_id = external_ids.get("ArXiv") or extract_arxiv_id(args.identifier)
        if arxiv_id:
            candidate_urls.append(("arXiv fallback", f"https://arxiv.org/pdf/{arxiv_id}.pdf"))
        direct_url = metadata.get("url")
        if isinstance(direct_url, str) and direct_url.lower().endswith(".pdf"):
            candidate_urls.append(("semantic scholar direct url", direct_url))

    if args.identifier.startswith("http") and args.identifier.lower().endswith(".pdf"):
        candidate_urls.append(("provided direct pdf url", args.identifier))

    deduped: list[tuple[str, str]] = []
    seen = set()
    for label, url in candidate_urls:
        if url in seen:
            continue
        seen.add(url)
        deduped.append((label, url))

    ok = False
    for label, url in deduped:
        success, err = download_pdf(url, source_pdf)
        attempts.append((label, url if success else f"{url} :: {err}"))
        if success:
            report.extend(
                [
                    "- status: `success`",
                    f"- local file: `{source_pdf}`",
                    f"- source used: `{label}`",
                    f"- resolved URL: {url}",
                ]
            )
            ok = True
            break

    if not ok:
        report.extend(["- status: `failed`", f"- local target: `{source_pdf}`", "- attempts:"])
        for label, info in attempts:
            report.append(f"  - `{label}`: {info}")
        report.append("- next action: manual PDF required")

    report.append("- raw semantic scholar metadata:")
    report.append("```json")
    report.append(json.dumps(metadata or {}, ensure_ascii=False, indent=2))
    report.append("```")
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")

    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
