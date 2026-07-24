#!/usr/bin/env python3
"""Validate the self-contained R004 #776/#635 evidence package."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent

REQUIRED = {
    "776": [
        "REPORT.md",
        "RESULT.json",
        "CERTIFICATE.json",
        "SOURCE_MANIFEST.json",
        "TIMING.json",
        "SHA256SUMS",
        "verify_rank8_five_term_barrier.py",
    ],
    "635": [
        "REPORT.md",
        "RESULT.json",
        "GRADIENT_CERTIFICATE.json",
        "COMPONENT_CERTIFICATE.json",
        "PARALLEL_FAMILY_CERTIFICATE.json",
        "SOURCE_MANIFEST.json",
        "TIMING.json",
        "SHA256SUMS",
        "verify_shared_path_gradient.py",
        "search_bicyclic_components.py",
        "verify_parallel_cycle_family.py",
        "search_parallel_cycle_family.py",
        "verify_targeted_cycle_components.py",
    ],
}

VERIFIERS = [
    [sys.executable, "776/verify_rank8_five_term_barrier.py"],
    [sys.executable, "635/verify_shared_path_gradient.py"],
    [sys.executable, "635/verify_parallel_cycle_family.py"],
    [sys.executable, "635/search_parallel_cycle_family.py"],
    [sys.executable, "635/verify_targeted_cycle_components.py"],
    [
        sys.executable,
        "635/search_bicyclic_components.py",
        "--limit",
        "2000000",
    ],
]


def load_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(path)
    return value


def verify_sha(directory: Path) -> int:
    manifest = directory / "SHA256SUMS"
    checked = 0
    for raw_line in manifest.read_text(encoding="utf-8").splitlines():
        digest, relative = raw_line.split("  ", 1)
        target = directory / relative
        assert target.is_file(), target
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        assert actual == digest, (target, digest, actual)
        checked += 1
    assert checked >= len(REQUIRED[directory.name]) - 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-verifiers", action="store_true")
    args = parser.parse_args()

    sha_checks = 0
    active_seconds = 0
    start: datetime | None = None
    freeze: datetime | None = None
    for problem_id, names in REQUIRED.items():
        directory = ROOT / problem_id
        for name in names:
            assert (directory / name).is_file(), directory / name

        result = load_json(directory / "RESULT.json")
        assert result["problem_id"] == problem_id
        assert result["cycle_id"] == "R004"
        assert result["original_problem_closed"] is False
        assert result["proof_or_disproof"] is False
        assert result["q2_candidate"] is False
        assert result["outcome"] == "strict_progress_no_closure"

        timing = load_json(directory / "TIMING.json")
        seconds = int(timing["active_agent_seconds"])
        assert seconds == sum(
            int(phase["active_seconds"]) for phase in timing["phases"]
        )
        active_seconds += seconds
        this_start = datetime.fromisoformat(str(timing["started_at"]))
        this_freeze = datetime.fromisoformat(
            str(timing["research_frozen_at"])
        )
        start = this_start if start is None else start
        freeze = this_freeze if freeze is None else freeze
        assert this_start == start and this_freeze == freeze

        source = load_json(directory / "SOURCE_MANIFEST.json")
        assert source["problem_id"] == problem_id
        for name in names:
            if name.endswith("CERTIFICATE.json"):
                certificate = load_json(directory / name)
                assert certificate["status"] == "PASS"
        sha_checks += verify_sha(directory)

    assert start is not None and freeze is not None
    elapsed = int((freeze - start).total_seconds())
    assert active_seconds == 4206
    assert elapsed == 4206
    assert active_seconds >= 4200

    verifier_results: list[dict[str, object]] = []
    if args.run_verifiers:
        for command in VERIFIERS:
            completed = subprocess.run(
                command,
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            output = json.loads(completed.stdout)
            assert output["status"] == "PASS", command
            verifier_results.append(
                {
                    "command": " ".join(command),
                    "status": output["status"],
                }
            )

    result = {
        "schema": "amra.erdos-master-rotation.r004-package-validation.v1",
        "status": "PASS",
        "problems": ["776", "635"],
        "active_foreground_seconds": active_seconds,
        "minimum_required_seconds": 4200,
        "sha256_entries_checked": sha_checks,
        "verifiers_run": verifier_results,
        "original_problems_closed": [],
        "q2_candidates": [],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
