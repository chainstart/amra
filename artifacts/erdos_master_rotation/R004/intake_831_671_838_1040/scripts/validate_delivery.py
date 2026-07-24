#!/usr/bin/env python3
"""Structural, provenance, timing, and checksum validation for this intake."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PROBLEMS = ("831", "671", "838", "1040")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def check_required_files() -> None:
    required = [
        "SOURCE_MANIFEST.md",
        "SOURCE_MANIFEST.json",
        "RESULTS.json",
        "TIMING.csv",
        "TIMING.md",
        "SHA256SUMS",
        "671/source_audit.txt",
        "671/compat_mathlib_4.27.patch",
        "671/compile_original_mathlib_4.27.log",
        "671/compile_compat_mathlib_4.27.log",
    ]
    for problem in PROBLEMS:
        required.extend((f"REPORT_{problem}.md", f"RESULT_{problem}.md"))
    missing = [name for name in required if not (ROOT / name).is_file()]
    assert not missing, f"missing deliverables: {missing}"


def check_results() -> None:
    data = json.loads((ROOT / "RESULTS.json").read_text())
    assert set(data) == set(PROBLEMS)
    assert data["671"]["official_status"] == "OPEN"
    assert data["671"]["mathematical_classification"] == (
        "LOCALLY_VERIFIED_FULL_SOLUTION_CANDIDATE"
    )
    assert data["671"]["first_public_full_claim"] == "2026-06-22T23:12:00"
    assert data["671"]["formal_claim_submitted"] == "2026-07-15T13:26:03"
    assert data["671"]["local_lean"]["exit_code"] == 0
    assert data["671"]["local_lean"]["axioms"] == [
        "propext",
        "Classical.choice",
        "Quot.sound",
    ]
    for problem in ("831", "838", "1040"):
        assert data[problem]["official_status"] == "OPEN"
        assert data[problem]["original_problem_closed"] is False
    assert data["1040"]["partial_label"] == "STRICT_PARTIAL"
    assert data["1040"]["novelty_established"] is False


def check_timing() -> None:
    with (ROOT / "TIMING.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert rows
    assert set(row["problem"] for row in rows) == set(PROBLEMS)
    active_rows = [row for row in rows if row["counts_as_foreground"] == "yes"]
    total = sum(int(row["active_seconds"]) for row in active_rows)
    assert total >= 4200, total
    by_problem = {
        problem: sum(
            int(row["active_seconds"])
            for row in active_rows
            if row["problem"] == problem
        )
        for problem in PROBLEMS
    }
    assert all(0 < seconds <= 5400 for seconds in by_problem.values()), by_problem
    # Rows are recorded as disjoint intervals; no parallel work is credited.
    intervals = sorted((row["start"], row["end"]) for row in active_rows)
    assert all(a_end <= b_start for (_, a_end), (b_start, _) in zip(intervals, intervals[1:]))


def check_671_evidence() -> None:
    patch = (ROOT / "671/compat_mathlib_4.27.patch").read_text()
    minus_lines = [line for line in patch.splitlines() if line.startswith("-") and not line.startswith("---")]
    plus_lines = [line for line in patch.splitlines() if line.startswith("+") and not line.startswith("+++")]
    assert len(minus_lines) == 7
    assert len(plus_lines) == 7
    for old, new, count in (
        ("continuous_finsetSum", "continuous_finset_sum", 2),
        ("Polynomial.eval_finsetSum", "Polynomial.eval_finset_sum", 1),
        ("tendsto_finsetProd", "tendsto_finset_prod", 3),
        ("tendsto_finsetSum", "tendsto_finset_sum", 1),
    ):
        assert patch.count(old) == count
        assert patch.count(new) == count

    compat_log = (ROOT / "671/compile_compat_mathlib_4.27.log").read_text()
    assert "exit_code: 0" in compat_log
    stdout = compat_log.split("complete_stdout_stderr:\n", 1)[1].split(
        "\n\nInterpretation:", 1
    )[0]
    assert stdout.strip() == (
        "'Erdos671.erdos_671' depends on axioms: "
        "[propext, Classical.choice, Quot.sound]"
    )
    assert "sorryAx" not in stdout

    audit = (ROOT / "671/source_audit.txt").read_text()
    for token in (
        "2026-06-22 23:12",
        "2026-07-15 13:26:03",
        "3854ae85aca322b5ad2c65fb9c7bae5ca19ed939ceca99521365d8690b8d8923",
        "2da73e90ffcde451b6479f8b63f81e2150c26c40e6e1002e71d2e4b596a045a6",
        "Total changed identifiers: 7",
    ):
        assert token in audit


def check_manifest() -> None:
    manifest = (ROOT / "SOURCE_MANIFEST.md").read_text()
    machine_manifest = json.loads((ROOT / "SOURCE_MANIFEST.json").read_text())
    source_ids = {source["id"] for source in machine_manifest["sources"]}
    assert {"official_831", "official_671", "official_838", "official_1040"} <= source_ids
    assert {"lean_671_decoded_original", "pendyala_2026"} <= source_ids
    assert all(len(source["sha256"]) == 64 for source in machine_manifest["sources"])
    for problem in PROBLEMS:
        assert f"www.erdosproblems.com/{problem}" in manifest
    for arxiv_id in ("1402.6276", "1604.08657", "2503.18270", "2604.03036", "2606.17097"):
        assert arxiv_id in manifest
    assert "STRICT_PARTIAL" in manifest


def check_checksums() -> None:
    entries: list[tuple[str, str]] = []
    for line in (ROOT / "SHA256SUMS").read_text().splitlines():
        expected, relative = line.split("  ", 1)
        entries.append((expected, relative))
    assert entries
    assert "SHA256SUMS" not in {relative for _, relative in entries}
    actual_files = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS"
    }
    assert {relative for _, relative in entries} == actual_files
    for expected, relative in entries:
        assert digest(ROOT / relative) == expected, relative


def main() -> None:
    check_required_files()
    check_results()
    check_timing()
    check_671_evidence()
    check_manifest()
    check_checksums()
    print("R004_DELIVERY_STRUCTURE_OK")
    print("R004_FOREGROUND_TIMING_AT_LEAST_4200_SECONDS_OK")
    print("R004_SHA256_MANIFEST_OK")


if __name__ == "__main__":
    main()
