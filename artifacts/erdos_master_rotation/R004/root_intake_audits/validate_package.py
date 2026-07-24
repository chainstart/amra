#!/usr/bin/env python3
"""Validate the R004 root intake/audit package and its claim guards."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED = {"187", "313", "323", "644", "689", "749", "811", "812", "920", "949"}
REPORTS = {
    "187": "187_REPORT.md",
    "313": "313_REPORT.md",
    "323": "323_REPORT.md",
    "644": "644_REPORT.md",
    "689": "689_AUDIT.md",
    "749": "749_REPORT.md",
    "811": "811_REPORT.md",
    "812": "812_REPORT.md",
    "920": "920_AUDIT.md",
    "949": "949_REPORT.md",
}


def load(name: str):
    return json.loads((ROOT / name).read_text())


result = load("RESULT.json")
timing = load("TIMING.json")
sources = load("SOURCE_MANIFEST.json")

assert result["cycle_id"] == timing["cycle_id"] == sources["cycle_id"] == "R004"
assert set(result["problems"]) == EXPECTED
assert set(timing["problem_active_seconds"]) == EXPECTED
assert set(sources["problems"]) == EXPECTED
assert sum(timing["problem_active_seconds"].values()) == timing["total_active_agent_seconds"]
assert timing["total_active_agent_seconds"] == 1800
assert timing["total_active_agent_hours"] == 0.5
assert result["original_problem_closed_count"] == 1
assert result["new_original_problem_proof_by_amra_count"] == 0
assert result["paper_level_new_result_count"] == 0
assert result["problems"]["920"]["original_problem_closed_mathematically"] is True
assert result["problems"]["920"]["official_status"] == "OPEN"
assert result["problems"]["920"]["related_official_status"] == "#986 PROVED"
assert result["problems"]["689"]["original_problem_closed_mathematically"] == "UNCONFIRMED"
assert all(not result["problems"][pid]["q2_candidate"] for pid in EXPECTED)
for problem_id, filename in REPORTS.items():
    text = (ROOT / filename).read_text()
    assert len(text) > 500, (problem_id, filename)

if (ROOT / "SHA256SUMS").exists():
    for line in (ROOT / "SHA256SUMS").read_text().splitlines():
        if not line.strip():
            continue
        expected_hash, filename = line.split("  ", 1)
        payload = (ROOT / filename).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == expected_hash, filename

print("PASS: R004 root intake/audit package")
