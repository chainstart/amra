#!/usr/bin/env python3
"""Re-run certificates and verify the R004 #809/#592 package."""

from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess


ROOT = pathlib.Path(__file__).resolve().parent


def load_json(path: pathlib.Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_json(script: pathlib.Path):
    completed = subprocess.run(
        ["python3", str(script)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def total_809_counts(certificate):
    instances = (
        certificate["dense_instances"]
        + certificate["sparse_hub_instances"]
    )
    pair_count = sum(item["edge_pairs_checked"] for item in instances)
    details = {}
    for item in instances:
        for name, value in item["detailed_template_case_counts"].items():
            details[name] = details.get(name, 0) + value
    return pair_count, details


def verify_checksum_file(checksum_path: pathlib.Path):
    checked = 0
    base = checksum_path.parent
    for raw_line in checksum_path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        digest, relative = raw_line.split("  ", 1)
        path = base / relative
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == digest, (path, digest, actual)
        checked += 1
    return checked


def main():
    json_files = sorted(ROOT.rglob("*.json"))
    for path in json_files:
        load_json(path)

    top_result = load_json(ROOT / "RESULT.json")
    result809 = load_json(ROOT / "809" / "RESULT.json")
    result592 = load_json(ROOT / "592" / "RESULT.json")
    timing = load_json(ROOT / "TIMING.json")
    assert top_result["official_status_rechecked"] == {
        "809": "OPEN",
        "592": "OPEN",
    }
    assert top_result["original_closed"] == {
        "809": False,
        "592": False,
    }
    assert not result809["original_closed"]
    assert not result592["original_closed"]
    assert not result809["q2_candidate"]
    assert not result592["q2_candidate"]
    assert timing["active_research_seconds"] >= 4200
    assert sum(timing["problem_active_seconds"].values()) == 4270
    assert all(
        timing["problem_active_seconds"][key]
        <= timing["problem_budget_caps_seconds"][key]
        for key in ("809", "592")
    )

    actual809 = run_json(ROOT / "809" / "verify_809_split_union.py")
    saved809 = load_json(ROOT / "809" / "verification.json")
    assert actual809 == saved809
    assert actual809["passed"]
    assert len(actual809["dense_instances"]) == 16
    assert len(actual809["sparse_hub_instances"]) == 15
    pairs, details = total_809_counts(actual809)
    assert pairs == 1022637
    assert len(details) == 10
    assert all(value > 0 for value in details.values())
    assert actual809["optimization"]["rational_pairs_checked"] == 80601
    assert actual809["optimization"]["minimum"] == "1/2"

    actual592 = run_json(
        ROOT / "592" / "verify_592_commutation_guard.py"
    )
    saved592 = load_json(ROOT / "592" / "verification.json")
    assert actual592 == saved592
    assert actual592["passed"]
    assert (
        actual592["successor_pushout_obstruction"]
        ["configurations_checked"]
        == 24
    )
    assert (
        actual592["finite_Gamma_root_guard"]
        ["finite_Gamma_free_forces_empty_T_omega_root_label"]
    )
    assert not (
        actual592["minimal_noncommutation_certificate"]
        ["symmetric_merge_preserves_both_histories"]
    )
    assert actual592["source_schedules"]["case4_inside"][
        "unique_ordered_replay"
    ] == ["TU", "SU", "ST"]
    assert actual592["source_schedules"]["case5_outside"][
        "unique_ordered_replay"
    ] == ["ST", "SU", "TU"]

    checksum_files = [
        ROOT / "809" / "SHA256SUMS",
        ROOT / "592" / "SHA256SUMS",
        ROOT / "SHA256SUMS",
    ]
    checksum_counts = {
        str(path.relative_to(ROOT)): verify_checksum_file(path)
        for path in checksum_files
    }
    print(
        json.dumps(
            {
                "json_files_parsed": len(json_files),
                "809_edge_pairs_rechecked": pairs,
                "809_template_subclasses_hit": len(details),
                "592_pushout_configurations_rechecked": 24,
                "checksum_entries_verified": checksum_counts,
                "passed": True,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
