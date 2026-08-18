#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_candidates(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    return data.get("candidates") or data.get("papers") or []


def seed_candidates_into_workspace(workspace: Path) -> dict:
    workspace = workspace.resolve()
    raw_path = workspace / "raw_candidates.json"
    seed_path = workspace / "seeded_candidates.json"

    existing = load_candidates(raw_path)
    seeded = load_candidates(seed_path)

    merged = list(existing) + list(seeded)
    payload = {
        "candidates": merged,
        "existing_count": len(existing),
        "seeded_count": len(seeded),
        "merged_count": len(merged),
    }
    raw_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pre-flight merge seeded_candidates.json into workspace/raw_candidates.json for PO"
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="PO workspace directory (defaults to current directory)",
    )
    args = parser.parse_args()

    payload = seed_candidates_into_workspace(args.workspace)
    print(
        f"OK: existing={payload['existing_count']} seeded={payload['seeded_count']} merged={payload['merged_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
