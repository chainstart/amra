#!/usr/bin/env python3
"""Validate structure, JSON, scripts, and SHA256SUMS for this intake package."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROBLEMS = ("521", "757", "517", "174")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


required = [
    ROOT / "SUMMARY.md",
    ROOT / "SOURCE_MANIFEST.json",
    ROOT / "TIMING.json",
    ROOT / "SHA256SUMS",
]
for problem in PROBLEMS:
    required.extend((ROOT / problem / "REPORT.md", ROOT / problem / "RESULT.json"))
for path in required:
    assert path.is_file(), f"missing {path.relative_to(ROOT)}"

manifest = json.loads((ROOT / "SOURCE_MANIFEST.json").read_text())
assert set(manifest["problems"]) == set(PROBLEMS)

active = 0
for problem in PROBLEMS:
    result = json.loads((ROOT / problem / "RESULT.json").read_text())
    assert result["problem_id"] == problem
    assert result["official_status"] == "OPEN"
    assert result["statement_quantifiers_verified"] is True
    assert result["research_timing"]["active_seconds"] <= 5400
    assert result["claim_guard"]
    active += result["research_timing"]["active_seconds"]

timing = json.loads((ROOT / "TIMING.json").read_text())
assert active == sum(timing["problem_active_seconds"].values())
assert (
    active + timing["shared_source_report_and_qa_seconds"]
    == timing["total_active_agent_seconds"]
)

scripts = (
    ROOT / "521" / "verify_reversal.py",
    ROOT / "757" / "verify_base_extension_obstruction.py",
    ROOT / "174" / "verify_lrw_kite.py",
)
for script in scripts:
    completed = subprocess.run(
        [sys.executable, "-B", str(script)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "'status': 'PASS'" in completed.stdout

checksum_lines = (ROOT / "SHA256SUMS").read_text().splitlines()
seen = set()
for line in checksum_lines:
    expected, relative = line.split("  ", 1)
    path = ROOT / relative
    assert path.is_file(), f"checksum target missing: {relative}"
    assert sha256(path) == expected, f"checksum mismatch: {relative}"
    seen.add(relative)

all_payload = {
    str(path.relative_to(ROOT))
    for path in ROOT.rglob("*")
    if path.is_file() and path.name != "SHA256SUMS"
}
assert seen == all_payload, f"checksum coverage mismatch: {seen ^ all_payload}"

print(
    json.dumps(
        {
            "status": "PASS",
            "problems": list(PROBLEMS),
            "payload_files_checked": len(all_payload),
            "active_agent_hours": timing["total_active_agent_hours"],
        },
        sort_keys=True,
    )
)

