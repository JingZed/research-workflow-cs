#!/usr/bin/env python3
"""Minimal Semantic Scholar client with centralized auth and rate limiting."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

import requests


DEFAULT_BASE_URL = "https://api.semanticscholar.org/graph/v1"
DEFAULT_MIN_INTERVAL_SECONDS = 1.05


def load_api_tokens() -> dict[str, str]:
    tokens: dict[str, str] = {}
    root = Path(__file__).resolve().parents[2]
    candidates = [
        root / "workflow" / "api_tokens.env",
        root / "api_tokens.env",
        Path.cwd() / "api_tokens.env",
    ]

    seen: set[Path] = set()
    for path in candidates:
        resolved = path.resolve()
        if resolved in seen or not resolved.exists():
            continue
        seen.add(resolved)
        for raw in resolved.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            tokens[key.strip()] = value.strip()

    env_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    if env_key:
        tokens["SEMANTIC_SCHOLAR_API_KEY"] = env_key

    return tokens


class SemanticScholarClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        min_interval_seconds: float = DEFAULT_MIN_INTERVAL_SECONDS,
        timeout_seconds: float = 30.0,
    ) -> None:
        if api_key is None:
            api_key = load_api_tokens().get("SEMANTIC_SCHOLAR_API_KEY")
        if not api_key:
            raise ValueError("Missing SEMANTIC_SCHOLAR_API_KEY in workflow/api_tokens.env or environment")

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.min_interval_seconds = float(min_interval_seconds)
        self.timeout_seconds = float(timeout_seconds)
        self._last_request_ts = 0.0
        self.session = requests.Session()
        self.session.headers.update(
            {
                "x-api-key": self.api_key,
                "User-Agent": "research-workflow/semantic-scholar-client",
            }
        )

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request_ts
        remaining = self.min_interval_seconds - elapsed
        if remaining > 0:
            time.sleep(remaining)

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        self._throttle()
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.session.request(method, url, timeout=self.timeout_seconds, **kwargs)
        self._last_request_ts = time.monotonic()

        if response.status_code == 429:
            raise RuntimeError(
                "Semantic Scholar rate limited the request. "
                "Keep usage below 1 request/second cumulative across endpoints."
            )
        response.raise_for_status()
        return response.json()

    def get_paper(self, paper_id: str, fields: str | None = None) -> dict[str, Any]:
        params = {}
        if fields:
            params["fields"] = fields
        return self._request("GET", f"paper/{paper_id}", params=params)

    def search_paper(self, query: str, limit: int = 10, fields: str | None = None) -> dict[str, Any]:
        params = {"query": query, "limit": int(limit)}
        if fields:
            params["fields"] = fields
        return self._request("GET", "paper/search", params=params)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Minimal Semantic Scholar helper with auth and throttling.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_search = sub.add_parser("search", help="Search papers")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=5)
    p_search.add_argument("--fields", default="title,year,venue,externalIds,openAccessPdf,url")

    p_get = sub.add_parser("get", help="Get one paper by paperId/CorpusId/DOI/arXiv")
    p_get.add_argument("paper_id")
    p_get.add_argument("--fields", default="title,year,venue,externalIds,openAccessPdf,url")

    args = parser.parse_args()
    client = SemanticScholarClient()
    if args.cmd == "search":
        data = client.search_paper(args.query, limit=args.limit, fields=args.fields)
    else:
        data = client.get_paper(args.paper_id, fields=args.fields)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
