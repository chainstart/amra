#!/usr/bin/env python3
"""Validate the completed R004 queue, effort contract and evidence manifests."""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
EXPECTED_QUEUES = {
    "closure_core": {"776", "809", "592", "635"},
    "intake": {
        "313",
        "749",
        "811",
        "831",
        "671",
        "949",
        "323",
        "644",
        "812",
        "838",
        "1040",
        "187",
    },
    "resolution_audit": {"920", "689"},
}
EXPECTED_PROBLEMS = set().union(*EXPECTED_QUEUES.values())
PACKAGE_MANIFESTS = (
    "core_776_635/SHA256SUMS",
    "core_809_592/SHA256SUMS",
    "intake_831_671_838_1040/SHA256SUMS",
    "root_intake_audits/SHA256SUMS",
    "qa_671/SHA256SUMS",
)


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def verify_manifest(path: Path) -> int:
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        target = path.parent / relative
        assert target.is_file(), target
        assert digest(target) == expected, target
        count += 1
    assert count > 0, path
    return count


def check_queue() -> None:
    queue = load_json(
        REPO / "artifacts/erdos_master_rotation/rotation_queue.json"
    )
    assert queue["cycle_id"] == "R004"
    queues = queue["queues"]
    for lane, expected in EXPECTED_QUEUES.items():
        rows = queues[lane]
        assert {str(row["problem_id"]) for row in rows} == expected
        assert all(row["cycle_progress"] == "completed" for row in rows)
        assert all(row["latest_outcome"] for row in rows)
    assert not queues["paper_conversion"]
    assert not queues["status_refresh"]


def check_events_and_ledger() -> None:
    event_path = REPO / "data/research_open/erdos_rotation/events.jsonl"
    events = [
        json.loads(line)
        for line in event_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    cycle_events = [row for row in events if row["cycle_id"] == "R004"]
    assert len(cycle_events) == 21
    assert {
        str(row["problem_id"])
        for row in cycle_events
        if row["problem_id"] is not None
    } == EXPECTED_PROBLEMS
    assert {
        str(row["problem_id"])
        for row in cycle_events
        if row["original_problem_closed"]
    } == {"671", "920"}
    assert not any(row["q2_candidate"] for row in cycle_events)
    event_hours = sum(
        Decimal(str(row["agent_hours"])) for row in cycle_events
    )
    assert abs(event_hours * 3600 - Decimal(14896)) < Decimal("0.001")

    ledger = load_json(
        REPO / "artifacts/erdos_master_rotation/master_ledger.json"
    )
    assert ledger["cycle_id"] == "R004"
    assert len(ledger["problems"]) == 630
    history = next(
        row
        for row in ledger["cycle_history"]
        if row["cycle_id"] == "R004"
    )
    assert history["event_count"] == 21
    assert history["problem_count"] == 18
    assert Decimal(str(history["registered_agent_hours"])) == Decimal(
        "4.137778"
    )
    assert history["original_closures"] == ["671", "920"]
    assert history["q2_candidates"] == []

    report = load_json(
        REPO / "artifacts/erdos_master_rotation/validation_report.json"
    )
    assert report["valid"] is True
    assert report["problem_count"] == report["unique_problem_count"] == 630
    assert report["event_count"] == len(events)


def check_contract_and_result() -> None:
    contract = load_json(ROOT / "BUDGET_CONTRACT.json")
    result = load_json(ROOT / "RESULT.json")
    timing = load_json(ROOT / "TIMING.json")
    assert contract["cycle_id"] == result["cycle_id"] == timing["cycle_id"] == (
        "R004"
    )
    minimum = int(contract["minimum_registered_active_agent_seconds"])
    registered = int(timing["registered_active_agent_seconds"])
    assert minimum == 14400
    assert registered == 14896 >= minimum
    assert sum(timing["package_active_agent_seconds"].values()) == registered
    assert sum(timing["problem_active_agent_seconds"].values()) == registered
    assert timing["sum_check"]["contract_margin_seconds"] == 496
    assert result["queue"]["completed"] == result["queue"]["total"] == 18
    assert result["budget_contract"]["satisfied"] is True
    assert {
        row["problem_id"] for row in result["original_problem_closures"]
    } == {"671", "920"}
    assert result["new_amra_original_problem_proofs"] == []
    assert result["q2_candidates"] == []
    assert result["paper_level_new_result_count"] == 0


def check_evidence() -> None:
    required = (
        "README.md",
        "RESULT.json",
        "SOURCE_MANIFEST.json",
        "TIMING.json",
        "BUDGET_CONTRACT.json",
        "validate_cycle.py",
        "qa_671/RESULT.json",
        "qa_671/INDEPENDENT_COMPILE.log",
        "root_intake_audits/920_AUDIT.md",
        "root_intake_audits/689_AUDIT.md",
    )
    assert all((ROOT / name).is_file() for name in required)
    checks = sum(verify_manifest(ROOT / name) for name in PACKAGE_MANIFESTS)
    assert checks >= 75
    if (ROOT / "SHA256SUMS").exists():
        assert verify_manifest(ROOT / "SHA256SUMS") >= 10


def main() -> None:
    check_queue()
    check_events_and_ledger()
    check_contract_and_result()
    check_evidence()
    print("PASS: R004 18/18 frozen queue actions completed")
    print("PASS: R004 14896 actual foreground agent-seconds >= 14400")
    print("PASS: R004 closures exactly {671, 920}; no Q2 promotion")
    print("PASS: R004 central ledger and package SHA256 manifests")


if __name__ == "__main__":
    main()
