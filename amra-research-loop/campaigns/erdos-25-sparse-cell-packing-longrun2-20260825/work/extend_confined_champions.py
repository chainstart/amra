#!/usr/bin/env python3
"""Extend fixed confined schedules to larger cutoffs without retuning them."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import time
from pathlib import Path


def load_simulator(path: Path):
    spec = importlib.util.spec_from_file_location("confined_echo_search", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load simulator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def signature(row: dict) -> tuple:
    return (
        row["Q"], row["base"], row["growth"], row["attack_phase"], row["policy"],
        row["theta"], row["schedule_seed"], row["cell_modulus"], row["cell_residue"],
    )


def signed_metrics(row: dict) -> tuple[float, float, float]:
    values = [item["normalised_deleted_mass"] for item in row["endpoint_rows"]]
    values = values[len(values) // 2 :]
    differences = [right - left for left, right in zip(values, values[1:])]
    rise = max((value for value in differences if value > 0), default=0.0)
    drop = max((-value for value in differences if value < 0), default=0.0)
    return rise, drop, min(rise, drop)


def run_at(module, source: dict, N: int) -> dict:
    result = module.simulate(
        source["Q"], N, source["base"], source["growth"], source["attack_phase"],
        source["policy"], source["theta"], source["schedule_seed"],
        source["cell_modulus"], source["cell_residue"],
    )
    assert result is not None
    rise, drop, two_sided = signed_metrics(result)
    return {
        "N": N,
        "integer_cutoff": N * source["Q"] - 1,
        "selected_classes": result["selected_classes"],
        "late_endpoint_range": result["late_endpoint_range"],
        "range_fraction_of_attacked_cell_capacity": result["late_endpoint_range_fraction_of_attacked_cell_capacity"],
        "largest_late_adjacent_change": result["largest_late_adjacent_change"],
        "largest_late_rise": rise,
        "largest_late_recovery_drop": drop,
        "two_sided_late_swing": two_sided,
        "last_normalised_deleted_mass": result["last_normalised_deleted_mass"],
        "endpoint_count": result["endpoint_count"],
        "last_six_endpoints": result["endpoint_rows"][-6:],
        "deleted_bitmap_sha256": result["deleted_bitmap_sha256"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--simulator", type=Path, required=True)
    parser.add_argument("--max-index", type=int, default=12_000_000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text())
    assert payload["status"] == "completed"
    rows = list(payload["best_range_by_Q_cell_policy_and_index_scale"].values())
    nonaffine = [row for row in rows if row["policy"] != "max"]
    choices = [
        max(nonaffine, key=lambda row: row["late_endpoint_range"]),
        max(nonaffine, key=lambda row: row["late_endpoint_range_fraction_of_attacked_cell_capacity"]),
        max(nonaffine, key=lambda row: signed_metrics(row)[2]),
        max(nonaffine, key=lambda row: signed_metrics(row)[1]),
        max(nonaffine, key=lambda row: row["N"]),
    ]
    unique = []
    seen = set()
    for row in choices:
        key = signature(row)
        if key not in seen:
            seen.add(key)
            unique.append(row)

    module = load_simulator(args.simulator)
    started = time.monotonic()
    schedules = []
    for source in unique:
        cutoffs = []
        N = source["N"]
        while N < args.max_index:
            cutoffs.append(N)
            N *= 2
        cutoffs.append(args.max_index)
        extension_rows = [run_at(module, source, N) for N in sorted(set(cutoffs))]
        schedules.append({
            "source_parameters": {key: source[key] for key in (
                "Q", "N", "base", "growth", "attack_phase", "policy", "theta",
                "schedule_seed", "cell_modulus", "cell_residue",
                "certified_rare_index_survivor_density_lower_bound",
                "certified_original_survivor_density_lower_bound",
            )},
            "extension_rows": extension_rows,
        })
    elapsed = time.monotonic() - started
    result = {
        "schema_version": "erdos-25.confined-champion-extension.v1",
        "status": "passed",
        "guard_required": True,
        "source_search": str(args.input),
        "max_index": args.max_index,
        "elapsed_seconds": elapsed,
        "fixed_schedules_extended": len(schedules),
        "schedules": schedules,
        "interpretation_limit": "Each row is an exact longer prefix of one fixed parameter schedule. Even persistence through the finite max_index is not an infinite counterexample.",
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "passed",
        "fixed_schedules_extended": len(schedules),
        "max_index": args.max_index,
        "elapsed_seconds": elapsed,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
