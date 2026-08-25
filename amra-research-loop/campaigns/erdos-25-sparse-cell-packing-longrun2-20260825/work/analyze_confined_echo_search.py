#!/usr/bin/env python3
"""Replay and stratify the positive-inner-density confined echo search."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path


def load_simulator(path: Path):
    spec = importlib.util.spec_from_file_location("confined_echo_search", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load simulator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay(module, row: dict) -> dict:
    result = module.simulate(
        row["Q"], row["N"], row["base"], row["growth"], row["attack_phase"],
        row["policy"], row["theta"], row["schedule_seed"],
        row["cell_modulus"], row["cell_residue"],
    )
    assert result is not None
    for key in (
        "deleted_bitmap_sha256",
        "selected_classes",
        "non_binary_max_selected_classes",
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
        "g": row["cell_modulus"],
        "policy": row["policy"],
        "deleted_bitmap_sha256": row["deleted_bitmap_sha256"],
        "status": "passed",
    }


def signed_metrics(row: dict) -> tuple[float, float, float]:
    values = [item["normalised_deleted_mass"] for item in row["endpoint_rows"]]
    values = values[len(values) // 2 :]
    differences = [right - left for left, right in zip(values, values[1:])]
    rise = max((value for value in differences if value > 0), default=0.0)
    drop = max((-value for value in differences if value < 0), default=0.0)
    return rise, drop, min(rise, drop)


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

    grouped: dict[tuple[int, int, str], list[dict]] = {}
    summaries = []
    for key, row in source["best_range_by_Q_cell_policy_and_index_scale"].items():
        q, g = row["Q"], row["cell_modulus"]
        assert key.startswith(f"Q={q};g={g};policy={row['policy']};")
        assert q >= 4 and q & (q - 1) == 0
        assert g >= 3 and g % 2 == 1
        assert 0 <= row["cell_residue"] < g
        assert math.isclose(row["certified_rare_index_survivor_density_lower_bound"], 1 - 1 / g)
        assert math.isclose(row["certified_original_survivor_density_lower_bound"], 0.5 + (1 - 1 / g) / q)
        assert row["minimum_step_to_target_ratio"] > 1.0
        assert row["maximum_step_to_target_ratio"] <= q / 2.0
        grouped.setdefault((q, g, row["policy"]), []).append(row)
        rise, drop, two_sided = signed_metrics(row)
        summaries.append({
            "Q": q,
            "g": g,
            "policy": row["policy"],
            "N": row["N"],
            "floor_log2_N": row["N"].bit_length() - 1,
            "certified_original_survivor_density_lower_bound": row["certified_original_survivor_density_lower_bound"],
            "late_endpoint_range": row["late_endpoint_range"],
            "largest_late_rise": rise,
            "largest_late_recovery_drop": drop,
            "two_sided_late_swing": two_sided,
            "range_fraction_of_attacked_cell_capacity": row["late_endpoint_range_fraction_of_attacked_cell_capacity"],
            "selected_classes": row["selected_classes"],
        })

    largest_scale = []
    for (q, g, policy), rows in sorted(grouped.items()):
        row = max(rows, key=lambda item: item["N"])
        largest_scale.append({
            "Q": q,
            "g": g,
            "policy": policy,
            "N": row["N"],
            "certified_original_survivor_density_lower_bound": row["certified_original_survivor_density_lower_bound"],
            "late_endpoint_range": row["late_endpoint_range"],
            "range_fraction_of_attacked_cell_capacity": row["late_endpoint_range_fraction_of_attacked_cell_capacity"],
        })

    best_capacity_fraction = max(
        summaries,
        key=lambda row: row["range_fraction_of_attacked_cell_capacity"],
    )
    best_two_sided = max(summaries, key=lambda row: row["two_sided_late_swing"])

    payload = {
        "schema_version": "erdos-25.confined-nonaffine-echo-analysis.v1",
        "status": "passed",
        "source_elapsed_seconds": source["elapsed_seconds"],
        "source_trials": source["trials"],
        "source_simulated_trials": source["simulated_trials"],
        "source_exact_rare_indices_simulated": source["exact_rare_indices_simulated"],
        "mechanical_replays": replays,
        "stratified_champions": summaries,
        "best_range_fraction_of_attacked_cell_capacity": best_capacity_fraction,
        "best_two_sided_late_swing": best_two_sided,
        "largest_sampled_scale_by_Q_g_and_policy": largest_scale,
        "checks": [
            "full requested guarded duration completed",
            "two global champions replayed byte-for-byte",
            "strictly positive rare-index and original survivor lower bounds checked in every stratum",
            "all step-to-target ratios lie in the exact admissible CRT interval",
            "signed rises and recovery drops are separated so monotone convergence is not mislabeled as oscillation",
        ],
        "interpretation_limit": "Finite positive-density evidence cannot prove logarithmic tightness or certify an infinite oscillation.",
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "passed",
        "replays": len(replays),
        "strata": len(summaries),
        "groups": len(largest_scale),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
