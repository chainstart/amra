#!/usr/bin/env python3
"""Blindly extend frozen fixed-rule champions over increasing cutoffs."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
import time
from pathlib import Path


def load_simulator(path: Path):
    spec = importlib.util.spec_from_file_location("confined_echo_search", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load simulator from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def source_signature(row: dict) -> tuple:
    return (
        row["Q"], row["base"], row["growth"], row["attack_phase"],
        row["policy"], row["theta"], row["schedule_seed"],
        row["cell_modulus"], row["cell_residue"],
    )


def signed_metrics(row: dict, final_differences: int = 14) -> dict:
    values = [item["normalised_deleted_mass"] for item in row["endpoint_rows"]]
    differences = [right - left for left, right in zip(values, values[1:])]
    tail = differences[-final_differences:]
    rises = [value for value in tail if value > 0]
    drops = [-value for value in tail if value < 0]
    second_rise = 0.0 if len(tail) < 10 or len(rises) < 2 else sorted(rises, reverse=True)[1]
    second_drop = 0.0 if len(tail) < 10 or len(drops) < 2 else sorted(drops, reverse=True)[1]
    latest_rise = next((value for value in reversed(tail) if value > 0), 0.0)
    latest_drop = next((-value for value in reversed(tail) if value < 0), 0.0)
    return {
        "tail_difference_count": len(tail),
        "tail_rise_count": len(rises),
        "tail_drop_count": len(drops),
        "second_largest_recent_rise": second_rise,
        "second_largest_recent_drop": second_drop,
        "recent_two_cycle_floor": min(second_rise, second_drop),
        "latest_rise": latest_rise,
        "latest_drop": latest_drop,
        "latest_two_sided_floor": min(latest_rise, latest_drop),
    }


def extension_row(row: dict, elapsed: float) -> dict:
    metrics = signed_metrics(row)
    return {
        "N": row["N"],
        "integer_cutoff": row["N"] * row["Q"] - 1,
        "elapsed_segment_seconds": elapsed,
        "selected_classes": row["selected_classes"],
        "echo_events_that_newly_deleted_points": row["echo_events_that_newly_deleted_points"],
        "last_normalised_deleted_mass": row["last_normalised_deleted_mass"],
        "attacked_cell_capacity_utilisation_proxy": row["Q"] * row["cell_modulus"] * row["last_normalised_deleted_mass"],
        "signed_metrics": metrics,
        "endpoint_count": row["endpoint_count"],
        "last_sixteen_endpoints": row["endpoint_rows"][-16:],
        "deleted_bitmap_sha256": row["deleted_bitmap_sha256"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=5400)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--simulator", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--champions", type=int, default=24)
    parser.add_argument("--skip-champions", type=int, default=0)
    parser.add_argument("--growth", type=float, default=1.65)
    parser.add_argument("--max-index", type=int, default=600_000_000)
    args = parser.parse_args()
    source = json.loads(args.input.read_text())
    if source.get("status") not in {"completed", "passed"}:
        raise ValueError("training search must be completed before blind extension")
    all_candidates = source.get("strict_champions", source.get("champions", []))
    candidates = all_candidates[
        args.skip_champions : args.skip_champions + args.champions
    ]
    if not candidates:
        raise ValueError("training search has no champions")
    module = load_simulator(args.simulator)
    states = []
    for rank, candidate in enumerate(candidates, args.skip_champions + 1):
        states.append({
            "training_rank": rank,
            "source_parameters": {key: candidate[key] for key in (
                "Q", "N", "base", "growth", "attack_phase", "policy", "theta",
                "schedule_seed", "cell_modulus", "cell_residue",
                "certified_rare_index_survivor_density_lower_bound",
                "certified_original_survivor_density_lower_bound",
            )},
            "training_signed_metrics": candidate.get("strict_metrics", candidate.get("signed_metrics", {})),
            "next_N": max(candidate["N"] + 1, int(math.ceil(candidate["N"] * args.growth))),
            "extension_rows": [],
        })
    started_wall = time.time()
    started = time.monotonic()
    deadline = started + args.seconds
    next_report = started + 60
    exact_points = simulations = 0
    exhausted = False

    def snapshot(status: str) -> dict:
        return {
            "schema_version": "erdos-25.fixed-rule-blind-extension.v1",
            "status": status,
            "guard_required": True,
            "requested_seconds": args.seconds,
            "started_unix": started_wall,
            "elapsed_seconds": time.monotonic() - started,
            "training_source": str(args.input),
            "frozen_champions": len(states),
            "skipped_training_champions": args.skip_champions,
            "cutoff_growth": args.growth,
            "max_index": args.max_index,
            "simulations": simulations,
            "exact_rare_indices_simulated": exact_points,
            "schedules": states,
            "interpretation_limit": "Parameters were frozen before extension. Finite persistence or decay still proves neither an infinite counterexample nor a universal convergence theorem.",
        }

    cursor = 0
    while time.monotonic() < deadline:
        available = [state for state in states if state["next_N"] <= args.max_index]
        if not available:
            exhausted = True
            break
        state = available[cursor % len(available)]
        cursor += 1
        source_row = state["source_parameters"]
        cutoff = state["next_N"]
        segment_started = time.monotonic()
        result = module.simulate(
            source_row["Q"], cutoff, source_row["base"], source_row["growth"],
            source_row["attack_phase"], source_row["policy"], source_row["theta"],
            source_row["schedule_seed"], source_row["cell_modulus"],
            source_row["cell_residue"],
        )
        if result is None:
            raise RuntimeError("frozen schedule became invalid under extension")
        if source_signature(result) != source_signature(source_row):
            raise AssertionError("extension retuned a frozen rule")
        elapsed_segment = time.monotonic() - segment_started
        state["extension_rows"].append(extension_row(result, elapsed_segment))
        state["next_N"] = max(cutoff + 1, int(math.ceil(cutoff * args.growth)))
        exact_points += cutoff
        simulations += 1
        atomic_json(args.output, snapshot("running"))
        now = time.monotonic()
        if now >= next_report:
            best_floor = max(
                row["signed_metrics"]["recent_two_cycle_floor"]
                for item in states for row in item["extension_rows"]
            )
            print(json.dumps({
                "elapsed_seconds": round(now - started, 1),
                "simulations": simulations,
                "exact_rare_indices_simulated": exact_points,
                "best_extended_recent_two_cycle_floor": best_floor,
                "largest_cutoff": max(row["N"] for item in states for row in item["extension_rows"]),
            }, sort_keys=True), flush=True)
            next_report = now + 60
    status = "completed_early_max_index" if exhausted else "completed"
    payload = snapshot(status)
    payload["completed_unix"] = time.time()
    atomic_json(args.output, payload)
    print(json.dumps({
        "status": status,
        "elapsed_seconds": payload["elapsed_seconds"],
        "simulations": simulations,
        "exact_rare_indices_simulated": exact_points,
    }, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
