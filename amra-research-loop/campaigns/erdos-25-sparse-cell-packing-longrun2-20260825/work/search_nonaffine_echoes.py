#!/usr/bin/env python3
"""Exact guarded search for non-affine echoes in the binary reservoir.

For target t=Qr-1 choose an even original modulus n=2d with gcd(Q,n)=2.
The conditional class inside -1 mod Q is exactly r mod d.  Conditions
r<d<=floor((Qr-1)/2), d odd, and increasing d make r its first positive
conditional representative, keep original moduli strictly increasing, and
ensure the original class is active at t.  Every marked echo is exact.
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
    attacks: list[tuple[int, int]] = []
    endpoints: list[int] = []
    for index, (left, right) in enumerate(zip(boundaries, boundaries[1:])):
        lo, hi = max(base, left), min(limit, right - 1)
        if lo > hi:
            continue
        endpoints.append(hi)
        if index % 2 == phase:
            attacks.append((lo, hi))
    return attacks, endpoints


def odd_at_least(value: int) -> int:
    return value if value % 2 else value + 1


def odd_at_most(value: int) -> int:
    return value if value % 2 else value - 1


def choose_step(low: int, high: int, policy: str, theta: float, rng: random.Random) -> int:
    if policy == "max":
        return high
    if policy == "min":
        return low
    if policy == "fraction":
        raw = low + theta * (high - low)
    elif policy == "jitter":
        local_theta = min(1.0, max(0.0, theta + rng.uniform(-0.35, 0.35)))
        raw = low + local_theta * (high - low)
    else:
        raise ValueError(policy)
    value = odd_at_least(int(round(raw)))
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
) -> dict | None:
    attacks, endpoints = alternating_intervals(base, growth, N, phase)
    if len(endpoints) < 6 or len(attacks) < 2:
        return None
    rng = random.Random(schedule_seed)
    deleted = np.zeros(N + 1, dtype=np.bool_)
    previous_step = Q // 2
    selected = 0
    echo_events = 0
    density_upper = 0.0
    nonaffine_steps = 0
    min_step_ratio = math.inf
    max_step_ratio = 0.0

    for lo, hi in attacks:
        for r in range(lo, hi + 1):
            if deleted[r]:
                continue
            # r<d makes r the least positive representative in index space.
            low = odd_at_least(max(previous_step + 1, r + 1, Q // 2 + 1))
            high = odd_at_most((Q * r - 1) // 2)
            if low > high:
                continue
            step = choose_step(low, high, policy, theta, rng)
            assert step % 2 == 1 and r < step <= (Q * r - 1) // 2
            assert step > previous_step
            previous_step = step
            selected += 1
            density_upper += 1.0 / (Q * step)
            if step != Q * r // 2 - 1:
                nonaffine_steps += 1
            min_step_ratio = min(min_step_ratio, step / r)
            max_step_ratio = max(max_step_ratio, step / r)
            positions = np.arange(r, N + 1, step, dtype=np.int64)
            echo_events += int(np.count_nonzero(~deleted[positions])) - 1
            deleted[positions] = True

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
    late_values = [row["normalised_deleted_mass"] for row in late]
    adjacent = [abs(b - a) for a, b in zip(late_values, late_values[1:])]
    return {
        "Q": Q,
        "N": N,
        "base": base,
        "growth": growth,
        "attack_phase": phase,
        "policy": policy,
        "theta": theta,
        "schedule_seed": schedule_seed,
        "selected_classes": selected,
        "nonaffine_selected_classes": nonaffine_steps,
        "echo_events_that_newly_deleted_points": echo_events,
        "sum_individual_eventual_density_upper": density_upper,
        "full_survivor_density_lower_bound": 0.5,
        "rare_cell_density": 1.0 / Q,
        "minimum_step_to_target_ratio": None if selected == 0 else min_step_ratio,
        "maximum_step_to_target_ratio": None if selected == 0 else max_step_ratio,
        "late_endpoint_range": max(late_values) - min(late_values),
        "late_endpoint_range_fraction_of_rare_cell": Q * (max(late_values) - min(late_values)),
        "largest_late_adjacent_change": max(adjacent, default=0.0),
        "largest_late_adjacent_change_fraction_of_rare_cell": Q * max(adjacent, default=0.0),
        "last_normalised_deleted_mass": endpoint_rows[-1]["normalised_deleted_mass"],
        "endpoint_count": len(endpoint_rows),
        "endpoint_rows": endpoint_rows,
        "deleted_bitmap_sha256": hashlib.sha256(deleted.tobytes()).hexdigest(),
        "certificate_scope": "Exact finite CRT simulation with strictly increasing original moduli n=2d and all evens surviving.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=4800)
    parser.add_argument("--seed", type=int, default=25082503)
    parser.add_argument("--max-index", type=int, default=500_000)
    parser.add_argument("--checkpoint-seconds", type=int, default=300)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    started_wall, started = time.time(), time.monotonic()
    deadline = started + args.seconds
    next_checkpoint = started + min(args.checkpoint_seconds, args.seconds)
    next_report = started + 60
    trials = simulated_trials = exact_points = 0
    best_range: dict | None = None
    best_change: dict | None = None
    best_strata: dict[str, dict] = {}

    def snapshot(status: str) -> dict:
        return {
            "schema_version": "erdos-25.nonaffine-echo-search.v1",
            "status": status,
            "guard_required": True,
            "seed": args.seed,
            "requested_seconds": args.seconds,
            "max_index": args.max_index,
            "started_unix": started_wall,
            "elapsed_seconds": time.monotonic() - started,
            "trials": trials,
            "simulated_trials": simulated_trials,
            "exact_rare_indices_simulated": exact_points,
            "best_late_endpoint_range": best_range,
            "best_late_adjacent_recovery_or_drop": best_change,
            "best_range_by_Q_policy_and_index_scale": best_strata,
            "interpretation_limit": "Finite exact stress test of non-affine binary-reservoir schedules; it neither proves convergence nor constructs an infinite oscillation.",
        }

    policies = ("max", "min", "fraction", "jitter")
    while time.monotonic() < deadline:
        Q = 2 ** rng.randint(2, 10)
        cap = max(10_000, min(args.max_index, int(10 ** rng.uniform(4.1, math.log10(args.max_index)))))
        base = rng.randint(2, min(300, max(2, cap // 100)))
        growth = math.exp(rng.uniform(math.log(1.2), math.log(max(1.35, min(5000.0, 8.0 * Q)))))
        phase = rng.randrange(2)
        policy = rng.choice(policies)
        theta = rng.random()
        schedule_seed = rng.randrange(2**63)
        result = simulate(Q, cap, base, growth, phase, policy, theta, schedule_seed)
        trials += 1
        if result is not None:
            simulated_trials += 1
            exact_points += cap
            if best_range is None or result["late_endpoint_range"] > best_range["late_endpoint_range"]:
                best_range = result
            if best_change is None or result["largest_late_adjacent_change"] > best_change["largest_late_adjacent_change"]:
                best_change = result
            key = f"Q={Q};policy={policy};floor_log2_N={cap.bit_length()-1}"
            current = best_strata.get(key)
            if current is None or result["late_endpoint_range"] > current["late_endpoint_range"]:
                best_strata[key] = result

        now = time.monotonic()
        if now >= next_checkpoint:
            atomic_json(args.output, snapshot("running"))
            next_checkpoint = now + args.checkpoint_seconds
        if now >= next_report:
            print(json.dumps({
                "elapsed_seconds": round(now - started, 1),
                "trials": trials,
                "simulated_trials": simulated_trials,
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
        "simulated_trials": simulated_trials,
        "exact_rare_indices_simulated": exact_points,
    }, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
