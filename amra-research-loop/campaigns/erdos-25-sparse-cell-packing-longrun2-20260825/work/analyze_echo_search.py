#!/usr/bin/env python3
"""Mechanical replay and scale-stratified summary of the echo search."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path


def load_simulator(path: Path):
    spec = importlib.util.spec_from_file_location("echo_search", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load echo simulator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay(module, row: dict) -> dict:
    result = module.simulate(row["Q"], row["N"], row["base"], row["growth"], row["attack_phase"])
    assert result is not None
    for key in (
        "deleted_bitmap_sha256",
        "selected_classes",
        "echo_events_that_newly_deleted_points",
        "endpoint_count",
    ):
        assert result[key] == row[key], (key, result[key], row[key])
    for key in (
        "late_endpoint_range",
        "largest_late_adjacent_change",
        "last_normalised_deleted_mass",
        "sum_individual_eventual_density_upper",
    ):
        assert math.isclose(result[key], row[key], rel_tol=1e-13, abs_tol=1e-15), key
    return {
        "Q": row["Q"],
        "N": row["N"],
        "deleted_bitmap_sha256": row["deleted_bitmap_sha256"],
        "status": "passed",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--simulator", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source = json.loads(args.input.read_text())
    assert source["status"] in {"completed", "redirected_after_exact_theorem"}
    assert source["guard_required"] is True
    if source["status"] == "completed":
        assert source["elapsed_seconds"] >= 0.99 * source["requested_seconds"]
    else:
        assert source["elapsed_seconds"] >= 600
        assert source.get("redirect_reason")
    assert source["simulated_trials"] > 0
    assert source["exact_rare_indices_simulated"] > 0

    module = load_simulator(args.simulator)
    replayed = [
        replay(module, source["best_late_endpoint_range"]),
        replay(module, source["best_late_adjacent_recovery_or_drop"]),
    ]

    by_q: dict[int, list[dict]] = {}
    for key, row in source["best_range_by_Q_and_index_scale"].items():
        assert key.startswith(f"Q={row['Q']};")
        assert row["full_survivor_density_lower_bound"] == 0.5
        assert row["rare_cell_density"] == 1.0 / row["Q"]
        assert row["late_endpoint_range"] >= 0.0
        assert row["largest_late_adjacent_change"] >= 0.0
        by_q.setdefault(row["Q"], []).append(row)

    scale_summary = []
    largest_scale_by_q = []
    for q, rows in sorted(by_q.items()):
        rows.sort(key=lambda item: item["N"])
        for row in rows:
            scale_summary.append({
                "Q": q,
                "N": row["N"],
                "floor_log2_N": row["N"].bit_length() - 1,
                "late_endpoint_range": row["late_endpoint_range"],
                "range_fraction_of_rare_cell": row["late_endpoint_range_fraction_of_rare_cell"],
                "growth": row["growth"],
                "endpoint_count": row["endpoint_count"],
            })
        row = rows[-1]
        largest_scale_by_q.append({
            "Q": q,
            "N": row["N"],
            "late_endpoint_range": row["late_endpoint_range"],
            "range_fraction_of_rare_cell": row["late_endpoint_range_fraction_of_rare_cell"],
        })

    payload = {
        "schema_version": "erdos-25.cross-scale-echo-analysis.v1",
        "status": "passed",
        "source_status": source["status"],
        "source_elapsed_seconds": source["elapsed_seconds"],
        "source_trials": source["trials"],
        "source_simulated_trials": source["simulated_trials"],
        "source_exact_rare_indices_simulated": source["exact_rare_indices_simulated"],
        "mechanical_replays": replayed,
        "stratified_champions": scale_summary,
        "largest_sampled_scale_by_Q": largest_scale_by_q,
        "checks": [
            "source duration and completion-or-mathematical-redirection status checked",
            "global range and adjacent-change champions replay byte-for-byte",
            "all retained strata have the exact binary-reservoir density metadata",
            "all retained ranges and changes are nonnegative",
        ],
        "interpretation_limit": "Scale-stratified finite evidence cannot prove convergence. The all-parameter affine-family conclusion comes from affine_echo_multiples_theorem.md, not from this trend summary.",
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "passed",
        "replays": len(replayed),
        "stratified_champions": len(scale_summary),
        "simulated_trials": source["simulated_trials"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
