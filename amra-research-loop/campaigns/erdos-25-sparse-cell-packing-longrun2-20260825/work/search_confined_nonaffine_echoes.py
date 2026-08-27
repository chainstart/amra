#!/usr/bin/env python3
"""Exact non-affine echo search with a certified positive inner survivor.

Targets satisfy r=a (mod g), and every odd echo step d is divisible by the
fixed odd g.  Hence every new progression stays inside that one coarse cell;
the other g-1 cells give an exact rare-index survivor-density lower bound
1-1/g at every finite stage and in the limit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import time
from pathlib import Path

import numpy as np


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def alternating_intervals(base: int, growth: float, limit: int, phase: int) -> tuple[list[tuple[int, int]], list[int]]:
    boundaries = [base]
    while boundaries[-1] <= limit:
        boundaries.append(max(boundaries[-1] + 1, int(math.ceil(boundaries[-1] * growth))))
    attacks, endpoints = [], []
    for index, (left, right) in enumerate(zip(boundaries, boundaries[1:])):
        lo, hi = max(base, left), min(limit, right - 1)
        if lo > hi:
            continue
        endpoints.append(hi)
        if index % 2 == phase:
            attacks.append((lo, hi))
    return attacks, endpoints


def admissible_at_least(value: int, g: int) -> int:
    quotient = (value + g - 1) // g
    if quotient % 2 == 0:
        quotient += 1
    return g * quotient


def admissible_at_most(value: int, g: int) -> int:
    quotient = value // g
    if quotient % 2 == 0:
        quotient -= 1
    return g * quotient


def choose_step(low: int, high: int, g: int, policy: str, theta: float, rng: random.Random) -> int:
    if policy == "max":
        return high
    if policy == "min":
        return low
    local = theta if policy == "fraction" else min(1.0, max(0.0, theta + rng.uniform(-0.4, 0.4)))
    target = int(round(low + local * (high - low)))
    value = admissible_at_least(target, g)
    return min(high, max(low, value))


def simulate(
    Q: int,
    N: int,
    base: int,
    growth: float,
    phase: int,
    policy: str,
    theta: float,
    schedule_seed: int,
    cell_modulus: int,
    cell_residue: int,
) -> dict | None:
    attacks, endpoints = alternating_intervals(base, growth, N, phase)
    if len(endpoints) < 6 or len(attacks) < 2:
        return None
    g, a = cell_modulus, cell_residue
    assert g >= 3 and g % 2 == 1 and 0 <= a < g
    rng = random.Random(schedule_seed)
    deleted = np.zeros(N + 1, dtype=np.bool_)
    previous_step = Q // 2
    selected = nonaffine = echoes = 0
    density_upper = 0.0
    min_ratio, max_ratio = math.inf, 0.0

    for lo, hi in attacks:
        r = lo + ((a - lo) % g)
        while r <= hi:
            if not deleted[r]:
                low = admissible_at_least(max(previous_step + 1, r + 1, Q // 2 + 1), g)
                high = admissible_at_most((Q * r - 1) // 2, g)
                if low <= high:
                    step = choose_step(low, high, g, policy, theta, rng)
                    assert step % 2 == 1 and step % g == 0
                    assert r < step <= (Q * r - 1) // 2 and step > previous_step
                    previous_step = step
                    selected += 1
                    density_upper += 1.0 / (Q * step)
                    # A fixed affine chart has constant step-c*r over all selected r.
                    # This local count merely distinguishes the binary max chart.
                    if step != Q * r // 2 - 1:
                        nonaffine += 1
                    min_ratio, max_ratio = min(min_ratio, step / r), max(max_ratio, step / r)
                    positions = np.arange(r, N + 1, step, dtype=np.int64)
                    echoes += int(np.count_nonzero(~deleted[positions])) - 1
                    deleted[positions] = True
            r += g

    indices = np.arange(1, N + 1, dtype=np.float64)
    weights = 1.0 / (Q * indices - 1.0)
    cumulative = np.cumsum(weights * deleted[1:])
    endpoint_rows = []
    for endpoint in endpoints:
        raw = float(cumulative[endpoint - 1])
        endpoint_rows.append({
            "rare_index": endpoint,
            "integer_cutoff": endpoint * Q - 1,
            "deleted_harmonic_mass": raw,
            "normalised_deleted_mass": raw / math.log(endpoint * Q - 1),
        })
    late = endpoint_rows[len(endpoint_rows) // 2 :]
    values = [row["normalised_deleted_mass"] for row in late]
    adjacent = [abs(y - x) for x, y in zip(values, values[1:])]
    global_lower = 0.5 + (1.0 - 1.0 / g) / Q
    return {
        "Q": Q,
        "N": N,
        "base": base,
        "growth": growth,
        "attack_phase": phase,
        "policy": policy,
        "theta": theta,
        "schedule_seed": schedule_seed,
        "cell_modulus": g,
        "cell_residue": a,
        "selected_classes": selected,
        "non_binary_max_selected_classes": nonaffine,
        "echo_events_that_newly_deleted_points": echoes,
        "sum_individual_eventual_density_upper": density_upper,
        "certified_rare_index_survivor_density_lower_bound": 1.0 - 1.0 / g,
        "certified_original_survivor_density_lower_bound": global_lower,
        "attacked_cell_density_in_rare_indices": 1.0 / g,
        "minimum_step_to_target_ratio": None if selected == 0 else min_ratio,
        "maximum_step_to_target_ratio": None if selected == 0 else max_ratio,
        "late_endpoint_range": max(values) - min(values),
        "late_endpoint_range_fraction_of_attacked_cell_capacity": Q * g * (max(values) - min(values)),
        "largest_late_adjacent_change": max(adjacent, default=0.0),
        "largest_late_adjacent_change_fraction_of_attacked_cell_capacity": Q * g * max(adjacent, default=0.0),
        "last_normalised_deleted_mass": endpoint_rows[-1]["normalised_deleted_mass"],
        "endpoint_count": len(endpoint_rows),
        "endpoint_rows": endpoint_rows,
        "deleted_bitmap_sha256": hashlib.sha256(deleted.tobytes()).hexdigest(),
        "certificate_scope": "Exact finite CRT simulation; all attacks stay in one g-cell, certifying positive inner and global survivor density.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=4800)
    parser.add_argument("--seed", type=int, default=25082504)
    parser.add_argument("--max-index", type=int, default=750_000)
    parser.add_argument("--checkpoint-seconds", type=int, default=300)
    parser.add_argument("--exclude-max", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    started_wall, started = time.time(), time.monotonic()
    deadline = started + args.seconds
    next_checkpoint = started + min(args.checkpoint_seconds, args.seconds)
    next_report = started + 60
    trials = simulated = exact_points = 0
    best_range = best_change = None
    strata: dict[str, dict] = {}

    def snapshot(status: str) -> dict:
        return {
            "schema_version": "erdos-25.confined-nonaffine-echo-search.v1",
            "status": status,
            "guard_required": True,
            "seed": args.seed,
            "requested_seconds": args.seconds,
            "max_index": args.max_index,
            "max_policy_excluded": args.exclude_max,
            "started_unix": started_wall,
            "elapsed_seconds": time.monotonic() - started,
            "trials": trials,
            "simulated_trials": simulated,
            "exact_rare_indices_simulated": exact_points,
            "best_late_endpoint_range": best_range,
            "best_late_adjacent_recovery_or_drop": best_change,
            "best_range_by_Q_cell_policy_and_index_scale": strata,
            "interpretation_limit": "Positive inner density is exact, but all schedules and cutoffs remain finite; no universal convergence or counterexample follows.",
        }

    Q_values = [2**power for power in range(2, 11)]
    g_values = [3, 5, 9, 15]
    policies = ["min", "fraction", "jitter"] if args.exclude_max else ["max", "min", "fraction", "jitter"]
    while time.monotonic() < deadline:
        Q, g = rng.choice(Q_values), rng.choice(g_values)
        cap = max(12_000, min(args.max_index, int(10 ** rng.uniform(4.2, math.log10(args.max_index)))))
        base = rng.randint(2, min(400, max(2, cap // 100)))
        growth = math.exp(rng.uniform(math.log(1.2), math.log(max(1.35, min(5000.0, 8.0 * Q)))))
        phase, policy, theta = rng.randrange(2), rng.choice(policies), rng.random()
        schedule_seed, a = rng.randrange(2**63), rng.randrange(g)
        result = simulate(Q, cap, base, growth, phase, policy, theta, schedule_seed, g, a)
        trials += 1
        if result is not None:
            simulated += 1
            exact_points += cap
            if best_range is None or result["late_endpoint_range"] > best_range["late_endpoint_range"]:
                best_range = result
            if best_change is None or result["largest_late_adjacent_change"] > best_change["largest_late_adjacent_change"]:
                best_change = result
            key = f"Q={Q};g={g};policy={policy};floor_log2_N={cap.bit_length()-1}"
            old = strata.get(key)
            if old is None or result["late_endpoint_range"] > old["late_endpoint_range"]:
                strata[key] = result
        now = time.monotonic()
        if now >= next_checkpoint:
            atomic_json(args.output, snapshot("running"))
            next_checkpoint = now + args.checkpoint_seconds
        if now >= next_report:
            print(json.dumps({
                "elapsed_seconds": round(now - started, 1),
                "trials": trials,
                "simulated_trials": simulated,
                "exact_rare_indices_simulated": exact_points,
                "best_late_endpoint_range": None if best_range is None else best_range["late_endpoint_range"],
            }, sort_keys=True), flush=True)
            next_report = now + 60
    payload = snapshot("completed") | {"completed_unix": time.time()}
    atomic_json(args.output, payload)
    print(json.dumps({
        "status": "completed",
        "elapsed_seconds": payload["elapsed_seconds"],
        "trials": trials,
        "simulated_trials": simulated,
        "exact_rare_indices_simulated": exact_points,
    }, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
