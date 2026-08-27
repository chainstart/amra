#!/usr/bin/env python3
"""Mechanical replay and stratified summary for non-affine echo search."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path


def load_simulator(path: Path):
    spec = importlib.util.spec_from_file_location("nonaffine_echo_search", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load simulator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay(module, row: dict) -> dict:
    result = module.simulate(
        row["Q"], row["N"], row["base"], row["growth"],
        row["attack_phase"], row["policy"], row["theta"], row["schedule_seed"],
    )
    assert result is not None
    for key in (
        "deleted_bitmap_sha256",
        "selected_classes",
        "nonaffine_selected_classes",
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
        "policy": row["policy"],
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
    assert source["status"] == "completed"
    assert source["guard_required"] is True
    assert source["elapsed_seconds"] >= 0.99 * source["requested_seconds"]
    assert source["simulated_trials"] > 0
    module = load_simulator(args.simulator)
    replays = [
        replay(module, source["best_late_endpoint_range"]),
        replay(module, source["best_late_adjacent_recovery_or_drop"]),
    ]

    grouped: dict[tuple[int, str], list[dict]] = {}
    all_rows = []
    nonaffine_strata = 0
    for key, row in source["best_range_by_Q_policy_and_index_scale"].items():
        assert key.startswith(f"Q={row['Q']};policy={row['policy']};")
        assert row["Q"] >= 4 and row["Q"] & (row["Q"] - 1) == 0
        assert row["full_survivor_density_lower_bound"] == 0.5
        assert row["rare_cell_density"] == 1.0 / row["Q"]
        assert row["minimum_step_to_target_ratio"] > 1.0
        assert row["maximum_step_to_target_ratio"] <= row["Q"] / 2.0
        if row["nonaffine_selected_classes"] > 0:
            nonaffine_strata += 1
        grouped.setdefault((row["Q"], row["policy"]), []).append(row)
        all_rows.append({
            "Q": row["Q"],
            "policy": row["policy"],
            "N": row["N"],
            "floor_log2_N": row["N"].bit_length() - 1,
            "late_endpoint_range": row["late_endpoint_range"],
            "range_fraction_of_rare_cell": row["late_endpoint_range_fraction_of_rare_cell"],
            "selected_classes": row["selected_classes"],
            "nonaffine_selected_classes": row["nonaffine_selected_classes"],
        })

    largest_scale = []
    for (q, policy), rows in sorted(grouped.items()):
        row = max(rows, key=lambda item: item["N"])
        largest_scale.append({
            "Q": q,
            "policy": policy,
            "N": row["N"],
            "late_endpoint_range": row["late_endpoint_range"],
            "range_fraction_of_rare_cell": row["late_endpoint_range_fraction_of_rare_cell"],
        })

    payload = {
        "schema_version": "erdos-25.nonaffine-echo-analysis.v1",
        "status": "passed",
        "source_elapsed_seconds": source["elapsed_seconds"],
        "source_trials": source["trials"],
        "source_simulated_trials": source["simulated_trials"],
        "source_exact_rare_indices_simulated": source["exact_rare_indices_simulated"],
        "mechanical_replays": replays,
        "stratified_champions": all_rows,
        "strata_with_genuinely_nonaffine_steps": nonaffine_strata,
        "largest_sampled_scale_by_Q_and_policy": largest_scale,
        "checks": [
            "full requested guarded duration completed",
            "two global champions replayed byte-for-byte",
            "all retained Q are powers of two and all evens survive",
            "every retained step-to-target ratio lies in the proved admissible interval",
        ],
        "interpretation_limit": "Finite non-affine trends do not prove the required tail tightness and do not refute the public problem.",
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "passed",
        "replays": len(replays),
        "strata": len(all_rows),
        "nonaffine_strata": nonaffine_strata,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
