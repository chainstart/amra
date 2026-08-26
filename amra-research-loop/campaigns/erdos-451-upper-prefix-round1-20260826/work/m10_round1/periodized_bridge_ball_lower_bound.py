#!/usr/bin/env python3
"""Enumerate a Euclidean ball inside the L=2 bridge box.

Only enumerated lattice vectors satisfying ``|H|<h`` and ``|a_i|<b`` are
retained; therefore their triangular weights give a rigorous finite lower
bound for S.  When the Euclidean radius contains the whole box and the
enumerator does not hit its solution cap, the reported sum is exact.
If the reported lower bound exceeds two, that particular (k, block, C)
falsifies the sufficient bridge at the tested h.  A lower bound below two
does not certify the bridge because the rest of the box is unenumerated.

This script requires the Sage Python environment (for fpylll) and must be
run behind ``openmath-memory-guard``.
"""

from __future__ import annotations

import argparse
import json
import math

from fpylll import Enumeration, GSO, IntegerMatrix, LLL


def primes_below(n: int) -> list[int]:
    sieve = bytearray(b"\x01") * n
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(n - 1) + 1):
        if sieve[p]:
            sieve[p * p : n : p] = b"\x00" * (((n - 1 - p * p) // p) + 1)
    return [p for p in range(2, n) if sieve[p]]


def actual_systems(min_k: int, max_k: int, step: int, min_rank: int,
                   max_rank: int, max_systems: int) -> list[dict[str, object]]:
    plist = primes_below(2 * max_k)
    rows: list[dict[str, object]] = []
    for k in range(min_k, max_k + 1, step):
        blocks: dict[int, list[int]] = {}
        for p in plist:
            if p <= k:
                continue
            if p >= 2 * k:
                break
            d = p - k
            delta = 1 << (d.bit_length() - 1)
            blocks.setdefault(delta, []).append(p)
        for delta, block in blocks.items():
            if min_rank <= len(block) <= max_rank:
                rows.append(
                    {
                        "k": k,
                        "delta": delta,
                        "moduli": tuple(block),
                        "offsets": tuple(p - k for p in block),
                    }
                )
    rows.sort(key=lambda row: (-len(row["moduli"]), row["k"], row["delta"]))
    return rows[:max_systems]


def canonical_sign(vector: tuple[int, ...]) -> tuple[int, ...]:
    for value in vector:
        if value < 0:
            return tuple(-x for x in vector)
        if value > 0:
            return vector
    return vector


def analyze(system: dict[str, object], poly_b: int, exponential_c: int,
            lll_delta: float, solution_cap: int, radius_fraction: float) -> dict[str, object]:
    k = int(system["k"])
    delta = int(system["delta"])
    moduli = tuple(int(p) for p in system["moduli"])
    offsets = tuple(int(d) for d in system["offsets"])
    q = len(moduli)
    period = math.prod(moduli)
    width_product = math.prod(offsets)
    b2 = 2 * ((delta - 1) // 2) + 1
    h_numerator = (k**poly_b) * (exponential_c**q) * period
    h = (h_numerator + width_product - 1) // width_product
    if 2 * h >= period:
        return {
            "label": f"k{k}-D{delta}",
            "rank": q,
            "skipped": "h_not_below_P_over_2",
        }

    scale = 2 * h
    rows = [[b2] + [scale] * q]
    for i, p in enumerate(moduli):
        vector = [0] * (q + 1)
        vector[i + 1] = -scale * p
        rows.append(vector)
    basis = IntegerMatrix.from_matrix(rows)
    LLL.reduction(basis, delta=lll_delta)
    gso = GSO.Mat(basis)
    gso.update_gso()

    box_radius = b2 * h
    radius = max(1, math.floor(radius_fraction * box_radius))
    radius_squared = radius * radius
    enumeration = Enumeration(gso, nr_solutions=solution_cap)
    solutions = enumeration.enumerate(0, q + 1, radius_squared, 0)

    seen: set[tuple[int, ...]] = set()
    positive_mass = 0.0
    outside_box = 0
    retained_inside = 0
    minimum_support = q + 1
    maximum_term = 0.0
    for _, coefficients in solutions:
        integer_coefficients = tuple(int(round(x)) for x in coefficients)
        scaled = tuple(
            sum(integer_coefficients[i] * int(basis[i, j]) for i in range(q + 1))
            for j in range(q + 1)
        )
        scaled = canonical_sign(scaled)
        if scaled in seen or not any(scaled):
            continue
        seen.add(scaled)
        if scaled[0] % b2 or any(value % scale for value in scaled[1:]):
            raise AssertionError("enumerated vector left the scaled lattice")
        global_lift = scaled[0] // b2
        locals_ = tuple(value // scale for value in scaled[1:])
        if any((global_lift - a) % p for a, p in zip(locals_, moduli)):
            raise AssertionError("enumerated vector failed its CRT congruence")
        if not (abs(global_lift) < h and all(2 * abs(a) < b2 for a in locals_)):
            outside_box += 1
            continue
        retained_inside += 1
        term = period / h
        term *= 1 - abs(global_lift) / h
        for a in locals_:
            term *= (1 - 2 * abs(a) / b2) / (b2 / 2)
        positive_mass += term
        maximum_term = max(maximum_term, term)
        minimum_support = min(minimum_support, sum(a != 0 for a in locals_))

    # fpylll returns one representative from each +/- pair.  The origin is
    # added separately, and every nonzero retained term is doubled.
    origin_term = (period / h) * (2 / b2) ** q
    lower_bound = origin_term + 2 * positive_mass
    hit_cap = len(solutions) >= solution_cap
    ball_contains_box = radius_fraction >= math.sqrt(q + 1)
    exact_box_sum = ball_contains_box and not hit_cap
    return {
        "classification": "finite_rigorous_subball_lower_bound_only",
        "label": f"k{k}-D{delta}",
        "k": k,
        "delta": delta,
        "rank": q,
        "C": exponential_c,
        "radius_fraction": radius_fraction,
        "P_digits": len(str(period)),
        "h_digits": len(str(h)),
        "enumeration_solutions": len(solutions),
        "unique_up_to_sign": len(seen),
        "retained_inside_up_to_sign": retained_inside,
        "enumeration_nodes": enumeration.get_nodes(),
        "solution_cap": solution_cap,
        "hit_solution_cap": hit_cap,
        "enumerated_outside_box": outside_box,
        "ball_contains_entire_bridge_box": ball_contains_box,
        "exact_S_computed": exact_box_sum,
        "origin_S_term": origin_term,
        "nonzero_ball_S_mass": 2 * positive_mass,
        "ball_S_lower_bound": lower_bound,
        "ball_alone_refutes_S_lt_2": lower_bound >= 2,
        "maximum_nonzero_single_term": maximum_term,
        "minimum_support_in_ball": None if not seen else minimum_support,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-k", type=int, default=300)
    parser.add_argument("--max-k", type=int, default=1800)
    parser.add_argument("--step", type=int, default=137)
    parser.add_argument("--min-rank", type=int, default=6)
    parser.add_argument("--max-rank", type=int, default=10)
    parser.add_argument("--max-systems", type=int, default=6)
    parser.add_argument("--poly-b", type=int, default=2)
    parser.add_argument("--exponential-c", type=int, default=6)
    parser.add_argument("--lll-delta", type=float, default=0.99)
    parser.add_argument("--solution-cap", type=int, default=2_000_000)
    parser.add_argument("--radius-fraction", type=float, default=0.8)
    args = parser.parse_args()
    systems = actual_systems(
        args.min_k,
        args.max_k,
        args.step,
        args.min_rank,
        args.max_rank,
        args.max_systems,
    )
    results = [
        analyze(
            system,
            args.poly_b,
            args.exponential_c,
            args.lll_delta,
            args.solution_cap,
            args.radius_fraction,
        )
        for system in systems
    ]
    print(
        json.dumps(
            {
                "classification": "finite_rigorous_subball_lower_bound_only",
                "parameters": vars(args),
                "systems": len(results),
                "refuted_by_subball": sum(
                    bool(row.get("ball_alone_refutes_S_lt_2")) for row in results
                ),
                "results": results,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
