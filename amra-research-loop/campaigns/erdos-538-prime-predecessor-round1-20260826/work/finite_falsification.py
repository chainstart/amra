#!/usr/bin/env python3
"""Guarded finite falsification for the r=2 Erdős 538 campaign.

Finite MILP optima are used only as kill tests and conjecture generators.  The
script checkpoints after every solve so a timeout or OOM cannot erase earlier
evidence.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import time
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_array


def primes_upto(n: int) -> list[int]:
    sieve = bytearray(b"\x01") * (n + 1)
    if n >= 0:
        sieve[0] = 0
    if n >= 1:
        sieve[1] = 0
    for p in range(2, math.isqrt(n) + 1):
        if sieve[p]:
            sieve[p * p : n + 1 : p] = b"\x00" * (((n - p * p) // p) + 1)
    return [i for i in range(2, n + 1) if sieve[i]]


def solve_independent(weights: list[float], edges: list[tuple[int, int, int]],
                      seconds: float) -> dict:
    n = len(weights)
    if edges:
        row = np.repeat(np.arange(len(edges), dtype=np.int32), 3)
        col = np.asarray(edges, dtype=np.int32).reshape(-1)
        data = np.ones(len(row), dtype=float)
        matrix = coo_array((data, (row, col)), shape=(len(edges), n)).tocsr()
        constraints = LinearConstraint(matrix, -np.inf, 2.0)
    else:
        constraints = None
    started = time.monotonic()
    result = milp(
        c=-np.asarray(weights),
        integrality=np.ones(n, dtype=np.uint8),
        bounds=Bounds(0.0, 1.0),
        constraints=constraints,
        options={"time_limit": max(1.0, seconds), "mip_rel_gap": 1e-9, "presolve": True},
    )
    x = np.zeros(n) if result.x is None else result.x
    selected = np.flatnonzero(x > 0.5).tolist()
    return {
        "success": bool(result.success),
        "status": int(result.status),
        "message": str(result.message),
        "objective": float(np.dot(weights, x)),
        "mip_gap": None if getattr(result, "mip_gap", None) is None else float(result.mip_gap),
        "nodes": None if getattr(result, "mip_node_count", None) is None else int(result.mip_node_count),
        "elapsed_seconds": round(time.monotonic() - started, 4),
        "selected": selected,
    }


def lattice_model(prime_list: list[int], depth: int):
    vectors = list(itertools.product(range(depth + 1), repeat=len(prime_list)))
    index = {v: i for i, v in enumerate(vectors)}
    weights = []
    for v in vectors:
        denominator = math.prod(p ** e for p, e in zip(prime_list, v))
        weights.append(1.0 / denominator)
    edge_set: set[tuple[int, int, int]] = set()
    for y in vectors:
        positive = [i for i, e in enumerate(y) if e]
        for coords in itertools.combinations(positive, 3):
            predecessors = []
            for coord in coords:
                z = list(y)
                z[coord] -= 1
                predecessors.append(index[tuple(z)])
            edge_set.add(tuple(sorted(predecessors)))
    return vectors, weights, sorted(edge_set)


def integer_model(n_max: int):
    ps = primes_upto(n_max)
    edge_set: set[tuple[int, int, int]] = set()
    g_hist: dict[int, int] = {}
    for i, p in enumerate(ps):
        for j in range(i + 1, len(ps)):
            q = ps[j]
            if q * ps[j + 1] > n_max if j + 1 < len(ps) else True:
                break
            for r in ps[j + 1 :]:
                if q * r > n_max:
                    break
                for g in range(1, n_max // (q * r) + 1):
                    edge = tuple(sorted((g * p * q - 1, g * p * r - 1, g * q * r - 1)))
                    edge_set.add(edge)
                    g_hist[g] = g_hist.get(g, 0) + 1
    weights = [1.0 / n for n in range(1, n_max + 1)]
    return weights, sorted(edge_set), g_hist


def compression_witness() -> dict:
    # With p,q,r=2,3,5, A={pqr,pr,pq} is admissible.  Dividing pqr by p
    # creates {qr,pr,pq}, the forbidden predecessor triple of pqr.
    before = {30, 15, 10}
    after = {6, 15, 10}

    def forbidden_triples(bound: int) -> set[tuple[int, int, int]]:
        _, edges, _ = integer_model(bound)
        return {tuple(x + 1 for x in edge) for edge in edges}

    edges = forbidden_triples(max(before | after))
    return {
        "before": sorted(before),
        "before_is_admissible": not any(set(e) <= before for e in edges),
        "shift": "30 -> 6 (delete the prime coordinate 5)",
        "after": sorted(after),
        "after_is_admissible": not any(set(e) <= after for e in edges),
        "created_edge": [6, 10, 15],
        "harmonic_weight_before": sum(1.0 / x for x in before),
        "harmonic_weight_after": sum(1.0 / x for x in after),
        "conclusion": "M538-01 is false: a weight-increasing coordinate down-shift can create a forbidden triple.",
    }


def checkpoint(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def remaining(deadline: float, cap: float = 180.0) -> float:
    return max(1.0, min(cap, deadline - time.monotonic() - 5.0))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=1800)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started_wall = time.time()
    deadline = time.monotonic() + args.seconds
    payload = {
        "schema_version": "amra.erdos538.finite-falsification.v1",
        "started_unix": started_wall,
        "budget_seconds": args.seconds,
        "epistemic_status": "finite falsification only; no completeness reduction",
        "compression_witness": compression_witness(),
        "runs": [],
    }
    checkpoint(args.output, payload)
    print(json.dumps(payload["compression_witness"], sort_keys=True), flush=True)

    schedules: list[tuple[str, object]] = []
    base_primes = primes_upto(43)
    for k in range(4, 14):
        schedules.append(("lattice", (base_primes[:k], 1, f"squarefree-first-{k}")))
    for k in range(3, 8):
        schedules.append(("lattice", (base_primes[:k], 2, f"depth2-first-{k}")))
    for k in range(3, 6):
        schedules.append(("lattice", (base_primes[:k], 3, f"depth3-first-{k}")))
    for n_max in [60, 100, 160, 250, 400, 650, 1000, 1600, 2500, 4000]:
        schedules.append(("integer", n_max))

    rng = random.Random(53820260826)
    random_trial = 0
    schedule_index = 0
    while time.monotonic() < deadline - 8:
        if schedule_index < len(schedules):
            kind, spec = schedules[schedule_index]
            schedule_index += 1
        else:
            kind = "lattice"
            k = rng.choice([7, 8, 9, 10, 11])
            pool = primes_upto(rng.choice([47, 67, 97]))
            selected_primes = sorted(rng.sample(pool, k))
            spec = (selected_primes, 1, f"random-squarefree-{random_trial}")
            random_trial += 1

        if kind == "lattice":
            prime_list, depth, label = spec
            vectors, weights, edges = lattice_model(prime_list, depth)
            result = solve_independent(weights, edges, remaining(deadline))
            chosen = result.pop("selected")
            layer_mass: dict[str, float] = {}
            layer_count: dict[str, int] = {}
            max_support = 0
            exponent_two_mass = 0.0
            for idx in chosen:
                support = sum(e > 0 for e in vectors[idx])
                max_support = max(max_support, support)
                layer = str(support)
                layer_count[layer] = layer_count.get(layer, 0) + 1
                layer_mass[layer] = layer_mass.get(layer, 0.0) + weights[idx]
                if max(vectors[idx]) >= 2:
                    exponent_two_mass += weights[idx]
            record = {
                "kind": kind,
                "label": label,
                "primes": prime_list,
                "depth": depth,
                "vertices": len(vectors),
                "edges": len(edges),
                "selected_count": len(chosen),
                "max_selected_support": max_support,
                "selected_layer_count": layer_count,
                "selected_layer_mass": layer_mass,
                "selected_exponent_ge2_mass": exponent_two_mass,
                **result,
            }
        else:
            n_max = int(spec)
            weights, edges, g_hist = integer_model(n_max)
            result = solve_independent(weights, edges, remaining(deadline))
            chosen = result.pop("selected")
            chosen_set = set(chosen)
            tight = sum(sum(v in chosen_set for v in edge) == 2 for edge in edges)
            saturated = sum(sum(v in chosen_set for v in edge) == 3 for edge in edges)
            record = {
                "kind": kind,
                "n_max": n_max,
                "vertices": n_max,
                "edges": len(edges),
                "distinct_g_scales": len(g_hist),
                "max_g": max(g_hist, default=0),
                "selected_count": len(chosen),
                "tight_edge_fraction": tight / len(edges) if edges else 0.0,
                "violated_edges": saturated,
                "harmonic_total": sum(weights),
                **result,
            }

        payload["runs"].append(record)
        payload["elapsed_seconds"] = round(time.time() - started_wall, 3)
        payload["completed_runs"] = len(payload["runs"])
        checkpoint(args.output, payload)
        print(json.dumps({k: v for k, v in record.items() if k not in {"selected_layer_mass"}}, sort_keys=True), flush=True)

        # A model that exhausts its cap is useful evidence; do not escalate its
        # dimension in the same family during this bounded admission round.
        if not record["success"] and record["elapsed_seconds"] >= 0.9 * min(180.0, args.seconds):
            schedules = [item for item in schedules[schedule_index:] if item[0] != kind]
            schedule_index = 0

    payload["elapsed_seconds"] = round(time.time() - started_wall, 3)
    payload["completed"] = True
    checkpoint(args.output, payload)
    print(json.dumps({"completed": True, "runs": len(payload["runs"]), "elapsed_seconds": payload["elapsed_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
