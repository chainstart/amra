#!/usr/bin/env python3
"""Guarded exact search for recovery after sparse-cell deletion blocks.

The old binary tower leaves all evens and the rare odd cell -1 modulo Q.
At a chosen rare-cell index r this search adds modulus rQ-2, residue 1, so
the target rQ-1 is deleted.  Inside the rare cell the same class repeats at
indices r + h(rQ/2-1).  The simulator marks those echoes exactly up to N.
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
        nxt = max(boundaries[-1] + 1, int(math.ceil(boundaries[-1] * growth)))
        boundaries.append(nxt)
    intervals: list[tuple[int, int]] = []
    endpoints: list[int] = []
    for index, (left, right) in enumerate(zip(boundaries, boundaries[1:])):
        lo = max(base, left)
        hi = min(limit, right - 1)
        if lo > hi:
            continue
        endpoints.append(hi)
        if index % 2 == phase:
            intervals.append((lo, hi))
    return intervals, endpoints


def simulate(Q: int, N: int, base: int, growth: float, phase: int) -> dict | None:
    attack_intervals, endpoints = alternating_intervals(base, growth, N, phase)
    if len(endpoints) < 6 or len(attack_intervals) < 2:
        return None

    deleted = np.zeros(N + 1, dtype=np.bool_)
    selected = 0
    density_upper = 0.0
    echo_events = 0
    half_Q = Q // 2

    for lo, hi in attack_intervals:
        # Only r below this threshold has a second point r+(rQ/2-1) <= N.
        echo_hi = min(hi, (N + 1) // (half_Q + 1))
        if lo <= echo_hi:
            for r in range(lo, echo_hi + 1):
                if deleted[r]:
                    continue
                selected += 1
                density_upper += 2.0 / (Q * (r * Q - 2))
                step = r * half_Q - 1
                positions = np.arange(r, N + 1, step, dtype=np.int64)
                echo_events += int(np.count_nonzero(~deleted[positions])) - 1
                deleted[positions] = True
        bulk_lo = max(lo, echo_hi + 1)
        if bulk_lo <= hi:
            local = deleted[bulk_lo : hi + 1]
            offsets = np.flatnonzero(~local)
            if offsets.size:
                indices = offsets.astype(np.float64) + bulk_lo
                selected += int(offsets.size)
                density_upper += float(np.sum(2.0 / (Q * (indices * Q - 2.0))))
                local[offsets] = True

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
    adjacent_changes = [abs(b - a) for a, b in zip(late_values, late_values[1:])]
    rare_total = float(np.sum(weights))
    return {
        "Q": Q,
        "N": N,
        "base": base,
        "growth": growth,
        "attack_phase": phase,
        "selected_classes": selected,
        "echo_events_that_newly_deleted_points": echo_events,
        "sum_individual_eventual_density_upper": density_upper,
        "full_survivor_density_lower_bound": 0.5,
        "rare_cell_density": 1.0 / Q,
        "deleted_rare_fraction_by_harmonic_mass": float(cumulative[-1]) / rare_total,
        "late_endpoint_range": max(late_values) - min(late_values),
        "late_endpoint_range_fraction_of_rare_cell": Q * (max(late_values) - min(late_values)),
        "largest_late_adjacent_change": max(adjacent_changes, default=0.0),
        "largest_late_adjacent_change_fraction_of_rare_cell": Q * max(adjacent_changes, default=0.0),
        "last_normalised_deleted_mass": endpoint_rows[-1]["normalised_deleted_mass"],
        "endpoint_count": len(endpoint_rows),
        "endpoint_rows": endpoint_rows,
        "deleted_bitmap_sha256": hashlib.sha256(deleted.tobytes()).hexdigest(),
        "certificate_scope": "Exact for the binary-reservoir attack family up to the finite rare-index cutoff N.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=5400)
    parser.add_argument("--seed", type=int, default=25082502)
    parser.add_argument("--max-index", type=int, default=2_000_000)
    parser.add_argument("--checkpoint-seconds", type=int, default=300)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    started_wall = time.time()
    started = time.monotonic()
    deadline = started + args.seconds
    next_checkpoint = started + min(args.checkpoint_seconds, args.seconds)
    next_report = started + 60
    trials = 0
    simulated_trials = 0
    exact_points = 0
    best_range: dict | None = None
    best_recovery: dict | None = None
    best_by_Q: dict[str, dict] = {}
    best_by_Q_and_scale: dict[str, dict] = {}

    def snapshot(status: str) -> dict:
        return {
            "schema_version": "erdos-25.cross-scale-echo-search.v1",
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
            "best_late_adjacent_recovery_or_drop": best_recovery,
            "best_range_by_Q": best_by_Q,
            "best_range_by_Q_and_index_scale": best_by_Q_and_scale,
            "interpretation_limit": "Finite exact stress test of one structured family; trends are not a universal cross-scale theorem.",
        }

    Q_values = [2**power for power in range(2, 12)]
    while time.monotonic() < deadline:
        Q = rng.choice(Q_values)
        cap = max(20_000, min(args.max_index, int(10 ** rng.uniform(4.4, math.log10(args.max_index)))))
        base = rng.randint(2, min(500, max(2, cap // 100)))
        max_growth = max(1.35, min(10_000.0, 8.0 * Q))
        growth = math.exp(rng.uniform(math.log(1.2), math.log(max_growth)))
        phase = rng.randrange(2)
        result = simulate(Q, cap, base, growth, phase)
        trials += 1
        if result is not None:
            simulated_trials += 1
            exact_points += cap
            if best_range is None or result["late_endpoint_range"] > best_range["late_endpoint_range"]:
                best_range = result
            if best_recovery is None or result["largest_late_adjacent_change"] > best_recovery["largest_late_adjacent_change"]:
                best_recovery = result
            key = str(Q)
            current = best_by_Q.get(key)
            if current is None or result["late_endpoint_range"] > current["late_endpoint_range"]:
                best_by_Q[key] = result
            scale_key = f"Q={Q};floor_log2_N={cap.bit_length() - 1}"
            current_scale = best_by_Q_and_scale.get(scale_key)
            if current_scale is None or result["late_endpoint_range"] > current_scale["late_endpoint_range"]:
                best_by_Q_and_scale[scale_key] = result

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
