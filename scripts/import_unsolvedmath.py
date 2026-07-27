#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from amra.problem_banks.unsolvedmath import import_unsolvedmath_snapshot


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download and normalize the current UnsolvedMath catalog."
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Refetch index/set pages and download detail pages for newly discovered records.",
    )
    parser.add_argument(
        "--refresh-details",
        action="store_true",
        help="Also refetch every existing detail page instead of reusing the local detail snapshot.",
    )
    parser.add_argument("--workers", type=int, default=6, help="Concurrent detail-page requests.")
    parser.add_argument(
        "--delay",
        type=float,
        default=0.05,
        help="Delay in seconds after each request in a detail worker.",
    )
    parser.add_argument("--timeout", type=int, default=30, help="Per-request timeout in seconds.")
    args = parser.parse_args()
    payload = import_unsolvedmath_snapshot(
        repo_root=REPO_ROOT,
        refresh=args.refresh,
        refresh_details=args.refresh_details,
        timeout=args.timeout,
        workers=args.workers,
        request_delay=args.delay,
    )
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
