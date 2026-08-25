#!/usr/bin/env python3
"""Analyse recent signed-cycle decay in blind fixed-rule extensions."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def blind_only_cycle_metrics(rows: list[dict], training_cutoff: int) -> dict:
    """Score signed cycles using endpoints created strictly after training."""
    if not rows:
        endpoints = []
    else:
        endpoints = [
            endpoint for endpoint in rows[-1]["last_sixteen_endpoints"]
            if endpoint["rare_index"] > training_cutoff
        ]
    values = [endpoint["normalised_deleted_mass"] for endpoint in endpoints]
    differences = [right - left for left, right in zip(values, values[1:])]
    rises = sorted((value for value in differences if value > 0), reverse=True)
    drops = sorted((-value for value in differences if value < 0), reverse=True)
    second_rise = rises[1] if len(rises) >= 2 else 0.0
    second_drop = drops[1] if len(drops) >= 2 else 0.0
    floor = min(second_rise, second_drop)
    amplitude_pairs = [
        (math.log(endpoint["rare_index"]), math.log(abs(difference)))
        for endpoint, difference in zip(endpoints[1:], differences)
        if difference != 0
    ]
    amplitude_slope = None
    if len(amplitude_pairs) >= 3:
        mean_x = sum(x for x, _ in amplitude_pairs) / len(amplitude_pairs)
        mean_y = sum(y for _, y in amplitude_pairs) / len(amplitude_pairs)
        denominator = sum((x - mean_x) ** 2 for x, _ in amplitude_pairs)
        if denominator:
            amplitude_slope = sum(
                (x - mean_x) * (y - mean_y) for x, y in amplitude_pairs
            ) / denominator
    return {
        "post_training_endpoint_count_in_final_window": len(endpoints),
        "post_training_difference_count": len(differences),
        "post_training_rise_count": len(rises),
        "post_training_drop_count": len(drops),
        "post_training_second_largest_rise": second_rise,
        "post_training_second_largest_drop": second_drop,
        "post_training_two_cycle_floor": floor,
        "post_training_log_log_slope_of_step_amplitudes": amplitude_slope,
        "blind_only_cycle_gate_passed": floor > 0,
    }


def log_slope(rows: list[dict]) -> float | None:
    pairs = [
        (math.log(row["N"]), math.log(row["signed_metrics"]["recent_two_cycle_floor"]))
        for row in rows if row["signed_metrics"]["recent_two_cycle_floor"] > 0
    ]
    if len(pairs) < 3:
        return None
    mean_x = sum(x for x, _ in pairs) / len(pairs)
    mean_y = sum(y for _, y in pairs) / len(pairs)
    denominator = sum((x - mean_x) ** 2 for x, _ in pairs)
    if denominator == 0:
        return None
    return sum((x - mean_x) * (y - mean_y) for x, y in pairs) / denominator


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = json.loads(args.input.read_text())
    if source.get("status") not in {"completed", "completed_early_max_index"}:
        raise ValueError("blind extension source is not complete")
    summaries = []
    total_rows = 0
    for schedule in source["schedules"]:
        rows = schedule["extension_rows"]
        training_cutoff = schedule["source_parameters"]["N"]
        blind_metrics = blind_only_cycle_metrics(rows, training_cutoff)
        training_metrics = schedule["training_signed_metrics"]
        training_floor = training_metrics.get(
            "strict_recent_two_cycle_floor",
            training_metrics.get("recent_two_cycle_floor", 0.0),
        )
        total_rows += len(rows)
        cutoffs = [row["N"] for row in rows]
        if cutoffs != sorted(set(cutoffs)):
            raise AssertionError("extension cutoffs are not strictly increasing")
        floors = [row["signed_metrics"]["recent_two_cycle_floor"] for row in rows]
        capacities = [row["attacked_cell_capacity_utilisation_proxy"] for row in rows]
        last_three = floors[-3:]
        final_three_floor = min(last_three) if len(last_three) == 3 else 0.0
        historical_max = max(floors, default=0.0)
        ratio = 0.0 if historical_max == 0 else floors[-1] / historical_max
        persistence_gate = (
            len(rows) >= 4
            and len(last_three) == 3
            and final_three_floor > 0
            and final_three_floor >= 0.5 * historical_max
        )
        summaries.append({
            "training_rank": schedule["training_rank"],
            "source_parameters": schedule["source_parameters"],
            "extension_count": len(rows),
            "largest_cutoff": max(cutoffs, default=0),
            "strict_zero_floor_count": sum(value == 0 for value in floors),
            "historical_max_strict_floor": historical_max,
            "final_strict_floor": floors[-1] if floors else 0.0,
            "final_three_strict_floor": final_three_floor,
            "final_to_historical_max_ratio": ratio,
            "log_log_amplitude_slope_on_positive_rows": log_slope(rows),
            "initial_capacity_utilisation_proxy": capacities[0] if capacities else None,
            "final_capacity_utilisation_proxy": capacities[-1] if capacities else None,
            "finite_persistence_gate_passed": persistence_gate,
            "blind_only_cycle_metrics": blind_metrics,
            "training_strict_floor": training_floor,
            "blind_to_training_floor_ratio": (
                None if training_floor == 0
                else blind_metrics["post_training_two_cycle_floor"] / training_floor
            ),
            "last_four_extensions": rows[-4:],
        })
    summaries.sort(
        key=lambda row: (
            row["final_three_strict_floor"], row["final_strict_floor"],
            row["largest_cutoff"],
        ),
        reverse=True,
    )
    payload = {
        "schema_version": "erdos-25.fixed-rule-blind-analysis.v1",
        "status": "passed",
        "source_elapsed_seconds": source["elapsed_seconds"],
        "source_simulations": source["simulations"],
        "source_exact_rare_indices_simulated": source["exact_rare_indices_simulated"],
        "schedules_analysed": len(summaries),
        "extension_rows_analysed": total_rows,
        "finite_persistence_gate": "at least four blind extensions and each of the final three strict floors at least half the schedule's historical extension maximum",
        "finite_persistence_gate_passers": sum(row["finite_persistence_gate_passed"] for row in summaries),
        "blind_only_cycle_gate": "the final endpoint window contains at least two rises and two drops between endpoints whose rare indices are all strictly beyond the frozen training cutoff",
        "blind_only_cycle_gate_passers": sum(
            row["blind_only_cycle_metrics"]["blind_only_cycle_gate_passed"]
            for row in summaries
        ),
        "ranked_schedules": summaries,
        "interpretation_limit": "Only the blind-only gate excludes training endpoints. Both gates are adversarial finite evidence only: passing does not certify a nonzero limsup/liminf gap, and failing does not prove convergence. The legacy persistence diagnostic reuses overlapping endpoint windows and must not be counted as independent cycles.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "passed",
        "schedules": len(summaries),
        "rows": total_rows,
        "finite_persistence_gate_passers": payload["finite_persistence_gate_passers"],
        "blind_only_cycle_gate_passers": payload["blind_only_cycle_gate_passers"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
