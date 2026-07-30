#!/usr/bin/env python3
"""Run and checkpoint the KOU-21.137 odd-prime SmallGroups search."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import sys
from typing import Any, Mapping

from amra.discovery.second_batch_arithmetic import (
    GAP_BINARY,
    run_second_batch_arithmetic_search,
)


SCHEMA = "amra.kou_21_137.odd_power_scan_run.v2"


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _implementation_fingerprint() -> dict[str, object]:
    repository = Path(__file__).resolve().parents[1]
    files = (
        Path(__file__).resolve(),
        repository / "src/amra/discovery/second_batch_arithmetic.py",
        GAP_BINARY.resolve(),
    )
    return {
        "schema": "amra.kou_21_137.odd_power_implementation.v1",
        "files": [
            {
                "path": str(path),
                "sha256": _file_sha256(path),
            }
            for path in files
        ],
    }


def _atomic_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--prime", type=int, default=3)
    parser.add_argument("--orders", type=int, nargs="+", default=[243, 729])
    parser.add_argument("--max-cases", type=int, default=571)
    parser.add_argument("--chunk-size", type=int, default=16)
    parser.add_argument("--time-seconds", type=int, default=1200)
    parser.add_argument("--memory-limit-mib", type=int, default=1536)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from output-dir/checkpoint.json when it exists.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    output_dir = args.output_dir.resolve()
    checkpoint_path = output_dir / "checkpoint.json"
    result_path = output_dir / "result.json"
    manifest_path = output_dir / "manifest.json"
    checkpoint: Mapping[str, Any] | None = None
    if args.resume and checkpoint_path.exists():
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    implementation = _implementation_fingerprint()
    if checkpoint is not None:
        if not manifest_path.is_file():
            raise RuntimeError(
                "resume checkpoint exists without its provenance manifest"
            )
        previous_manifest = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
        if (
            previous_manifest.get("schema") != SCHEMA
            or previous_manifest.get("implementation") != implementation
        ):
            raise RuntimeError(
                "resume implementation does not match the prior manifest"
            )

    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--output-dir",
        str(output_dir),
        "--prime",
        str(args.prime),
        "--orders",
        *(str(order) for order in args.orders),
        "--max-cases",
        str(args.max_cases),
        "--chunk-size",
        str(args.chunk_size),
        "--time-seconds",
        str(args.time_seconds),
        "--memory-limit-mib",
        str(args.memory_limit_mib),
    ]
    if args.resume:
        command.append("--resume")
    started_at = datetime.now(timezone.utc).isoformat()
    _atomic_json(
        manifest_path,
        {
            "schema": SCHEMA,
            "status": "running",
            "started_at": started_at,
            "command": command,
            "budget": {
                "prime": args.prime,
                "target_orders": args.orders,
                "max_cases": args.max_cases,
                "group_chunk_size": args.chunk_size,
                "time_seconds": args.time_seconds,
                "memory_limit_mib": args.memory_limit_mib,
            },
            "resumed": checkpoint is not None,
            "implementation": implementation,
        },
    )

    observed_peak_mib = 0.0

    def progress(cursor: Mapping[str, Any], checked: int) -> None:
        nonlocal observed_peak_mib
        _atomic_json(checkpoint_path, dict(cursor))
        parent_peak_mib = (
            resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
        )
        child_peak_mib = (
            resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024
        )
        observed_peak_mib = max(
            observed_peak_mib, parent_peak_mib, child_peak_mib
        )
        if observed_peak_mib >= args.memory_limit_mib:
            raise MemoryError(
                f"memory guard reached after {checked} groups: "
                f"{observed_peak_mib:.1f} MiB"
            )

    result = run_second_batch_arithmetic_search(
        "unsolvedmath-kou-21.137",
        strategy_id="odd-p-smallgroups",
        budget={
            "prime": args.prime,
            "target_orders": args.orders,
            "max_cases": args.max_cases,
            "group_chunk_size": args.chunk_size,
            "time_seconds": args.time_seconds,
            "memory_mb": args.memory_limit_mib,
        },
        seed=0,
        checkpoint=checkpoint,
        progress=progress,
    )
    if _implementation_fingerprint() != implementation:
        raise RuntimeError("implementation files changed during the scan")
    completed_at = datetime.now(timezone.utc).isoformat()
    _atomic_json(result_path, result)
    _atomic_json(
        checkpoint_path,
        dict(result["checkpoint"]),
    )
    metrics = dict(result["metrics"])
    summary = {
        "checked_cases": int(result["checked_cases"]),
        "groups_checked_by_order": metrics.get("groups_checked_by_order", {}),
        "exponent_p2_groups_checked": int(
            metrics.get("exponent_p2_groups_checked", 0)
        ),
        "power_image_subgroups_checked": int(
            metrics.get("power_image_subgroups_checked", 0)
        ),
        "candidate": result["candidate"],
        "outcome": result["outcome"],
        "stop_reason": result["stop_reason"],
        "observed_peak_rss_mib": round(observed_peak_mib, 3),
        "catalogue_sha256": metrics.get("catalogue_sha256"),
        "gap_version": result["tool_versions"].get("gap"),
        "smallgrp_version": result["tool_versions"].get("smallgrp"),
    }
    _atomic_json(
        manifest_path,
        {
            "schema": SCHEMA,
            "status": "completed",
            "started_at": started_at,
            "completed_at": completed_at,
            "command": command,
            "budget": {
                "prime": args.prime,
                "target_orders": args.orders,
                "max_cases": args.max_cases,
                "group_chunk_size": args.chunk_size,
                "time_seconds": args.time_seconds,
                "memory_limit_mib": args.memory_limit_mib,
            },
            "resumed": checkpoint is not None,
            "implementation": implementation,
            "summary": summary,
            "result_file": result_path.name,
            "checkpoint_file": checkpoint_path.name,
        },
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
