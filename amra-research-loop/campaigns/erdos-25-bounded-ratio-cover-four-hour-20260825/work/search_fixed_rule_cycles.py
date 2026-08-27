#!/usr/bin/env python3
"""Search fixed non-affine rules using only recent signed cycles.

The exact simulator is imported from the preceding frozen campaign.  A rule
is completely determined by the stored parameters and is therefore stable
under later blind cutoff extension.  Training scores deliberately ignore the
full historical endpoint range.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
import random
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


def signature(row: dict) -> tuple:
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
    if len(tail) < 10 or len(rises) < 2 or len(drops) < 2:
        floor = 0.0
    else:
        floor = min(sorted(rises, reverse=True)[1], sorted(drops, reverse=True)[1])
    latest_rise = next((value for value in reversed(tail) if value > 0), 0.0)
    latest_drop = next((-value for value in reversed(tail) if value < 0), 0.0)
    return {
        "tail_difference_count": len(tail),
        "tail_rise_count": len(rises),
        "tail_drop_count": len(drops),
        "second_largest_recent_rise": 0.0 if len(rises) < 2 else sorted(rises, reverse=True)[1],
        "second_largest_recent_drop": 0.0 if len(drops) < 2 else sorted(drops, reverse=True)[1],
        "recent_two_cycle_floor": floor,
        "latest_rise": latest_rise,
        "latest_drop": latest_drop,
        "latest_two_sided_floor": min(latest_rise, latest_drop),
    }


def compact(row: dict) -> dict:
    keys = (
        "Q", "N", "base", "growth", "attack_phase", "policy", "theta",
        "schedule_seed", "cell_modulus", "cell_residue", "selected_classes",
        "non_binary_max_selected_classes", "echo_events_that_newly_deleted_points",
        "certified_rare_index_survivor_density_lower_bound",
        "certified_original_survivor_density_lower_bound",
        "minimum_step_to_target_ratio", "maximum_step_to_target_ratio",
        "last_normalised_deleted_mass", "endpoint_count", "deleted_bitmap_sha256",
    )
    result = {key: row[key] for key in keys}
    result["signed_metrics"] = signed_metrics(row)
    result["signed_metrics"]["cell_relative_recent_two_cycle_floor"] = (
        row["Q"] * row["cell_modulus"] * result["signed_metrics"]["recent_two_cycle_floor"]
    )
    result["last_sixteen_endpoints"] = row["endpoint_rows"][-16:]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=5400)
    parser.add_argument("--seed", type=int, default=25082506)
    parser.add_argument("--max-index", type=int, default=2_000_000)
    parser.add_argument("--checkpoint-seconds", type=int, default=300)
    parser.add_argument("--score-mode", choices=("raw", "cell_relative"), default="raw")
    parser.add_argument("--q-values", default="4,8,16,32,64")
    parser.add_argument("--g-values", default="3,5,7,9,15")
    parser.add_argument("--simulator", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    module = load_simulator(args.simulator)
    rng = random.Random(args.seed)
    started_wall = time.time()
    started = time.monotonic()
    deadline = started + args.seconds
    next_checkpoint = started + min(args.checkpoint_seconds, args.seconds)
    next_report = started + 60
    trials = simulated = exact_points = 0
    champions: dict[tuple, dict] = {}
    best = None

    def score(row: dict) -> float:
        key = (
            "recent_two_cycle_floor" if args.score_mode == "raw"
            else "cell_relative_recent_two_cycle_floor"
        )
        return row["signed_metrics"][key]

    def ranked() -> list[dict]:
        rows = list(champions.values())
        rows.sort(
            key=lambda row: (
                score(row),
                row["signed_metrics"]["latest_two_sided_floor"],
                row["N"],
            ),
            reverse=True,
        )
        return rows[:40]

    def snapshot(status: str) -> dict:
        return {
            "schema_version": "erdos-25.fixed-rule-signed-search.v1",
            "status": status,
            "guard_required": True,
            "seed": args.seed,
            "requested_seconds": args.seconds,
            "max_index": args.max_index,
            "score_mode": args.score_mode,
            "started_unix": started_wall,
            "elapsed_seconds": time.monotonic() - started,
            "trials": trials,
            "simulated_trials": simulated,
            "exact_rare_indices_simulated": exact_points,
            "best_fixed_rule": best,
            "champions": ranked(),
            "score_definition": "minimum of the second-largest rise and second-largest recovery drop among the final fourteen endpoint differences",
            "interpretation_limit": "Finite training evidence only; every retained rule must be frozen and blindly extended before it can survive falsification.",
        }

    q_values = [int(value) for value in args.q_values.split(",")]
    g_values = [int(value) for value in args.g_values.split(",")]
    if not q_values or any(value < 4 or value & (value - 1) for value in q_values):
        raise ValueError("q-values must be powers of two at least four")
    if not g_values or any(value < 3 or value % 2 == 0 for value in g_values):
        raise ValueError("g-values must be odd integers at least three")
    policies = ["min", "fraction", "jitter"]
    while time.monotonic() < deadline:
        q = rng.choice(q_values)
        g = rng.choice(g_values)
        cap = max(30_000, min(args.max_index, int(10 ** rng.uniform(4.5, math.log10(args.max_index)))))
        base = rng.randint(2, min(600, max(2, cap // 200)))
        growth = math.exp(rng.uniform(math.log(1.10), math.log(min(12.0, 1.5 * q))))
        phase = rng.randrange(2)
        policy = rng.choice(policies)
        theta = rng.random()
        schedule_seed = rng.randrange(2**63)
        residue = rng.randrange(g)
        row = module.simulate(q, cap, base, growth, phase, policy, theta, schedule_seed, g, residue)
        trials += 1
        if row is not None:
            simulated += 1
            exact_points += cap
            item = compact(row)
            key = signature(row)
            old = champions.get(key)
            if old is None or (
                score(item), item["N"]
            ) > (
                score(old), old["N"]
            ):
                champions[key] = item
            current = champions[key]
            if best is None or (
                score(current),
                current["signed_metrics"]["latest_two_sided_floor"],
            ) > (
                score(best),
                best["signed_metrics"]["latest_two_sided_floor"],
            ):
                best = current
            if len(champions) > 160:
                champions = {signature(row): row for row in ranked()}
        now = time.monotonic()
        if now >= next_checkpoint:
            atomic_json(args.output, snapshot("running"))
            next_checkpoint = now + args.checkpoint_seconds
        if now >= next_report:
            print(json.dumps({
                "elapsed_seconds": round(now - started, 1),
                "trials": trials,
                "exact_rare_indices_simulated": exact_points,
                "best_recent_two_cycle_floor": None if best is None else best["signed_metrics"]["recent_two_cycle_floor"],
                "best_score": None if best is None else score(best),
            }, sort_keys=True), flush=True)
            next_report = now + 60
    result = snapshot("completed")
    result["completed_unix"] = time.time()
    atomic_json(args.output, result)
    print(json.dumps({
        "status": "completed",
        "elapsed_seconds": result["elapsed_seconds"],
        "trials": trials,
        "simulated_trials": simulated,
        "exact_rare_indices_simulated": exact_points,
    }, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
