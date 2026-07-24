#!/usr/bin/env python3
"""Validate the R003 intake package without network access."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROBLEMS = ("193", "91", "509", "1002")


def load_json(name: str):
    with (ROOT / name).open(encoding="utf-8") as handle:
        return json.load(handle)


result = load_json("RESULT.json")
manifest = load_json("SOURCE_MANIFEST.json")
timing = load_json("TIMING.json")

assert result["cycle_id"] == "R003"
assert result["original_problem_closed_count"] == 0
assert result["paper_level_result_count"] == 0
assert set(result["problems"]) == set(PROBLEMS)
assert set(manifest["problems"]) == set(PROBLEMS)
assert set(timing["problem_active_seconds"]) == set(PROBLEMS)
assert sum(timing["problem_active_seconds"].values()) == timing["total_active_agent_seconds"]
assert timing["total_active_agent_seconds"] <= timing["wall_seconds"]

for problem in PROBLEMS:
    assert (ROOT / f"{problem}_REPORT.md").is_file()
    assert result["problems"][problem]["official_status"] == "OPEN"
    assert result["problems"][problem]["decision"]

scripts = (
    "verify_193_parikh.py",
    "verify_91_plateau.py",
    "verify_509_cubic_mst.py",
    "verify_1002_farey.py",
)
for script in scripts:
    completed = subprocess.run(
        [sys.executable, str(ROOT / script)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert completed.stdout.startswith("PASS")

checksum_lines = (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
listed = set()
for line in checksum_lines:
    digest, relative = line.split("  ", 1)
    assert relative != "SHA256SUMS"
    data = (ROOT / relative).read_bytes()
    assert hashlib.sha256(data).hexdigest() == digest
    listed.add(relative)

expected = {
    path.name
    for path in ROOT.iterdir()
    if path.is_file() and path.name != "SHA256SUMS"
}
assert listed == expected

print("PASS: R003 intake #193/#91/#509/#1002 package")
