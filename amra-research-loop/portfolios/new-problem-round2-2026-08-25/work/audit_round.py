#!/usr/bin/env python3
"""Adversarial small-domain replay for new-problem round 2."""

from __future__ import annotations

import itertools
import json
import math
import os
import bisect
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "evidence"


def primes_through(n: int) -> list[int]:
    return [
        x
        for x in range(2, n + 1)
        if all(x % d for d in range(2, math.isqrt(x) + 1))
    ]


def audit_317() -> dict[str, object]:
    exact_files = [
        EVIDENCE / "erdos_317_signed_lcm_2_24.json",
        EVIDENCE / "erdos_317_signed_lcm_25_28.json",
        EVIDENCE / "erdos_317_signed_lcm_29_30.json",
    ]
    rows = [row for path in exact_files for row in json.loads(path.read_text())["rows"]]
    status = {row["n"]: row["exact_mitm_status"] for row in rows}
    if [n for n in range(2, 5) if status[n] != "sat"]:
        raise AssertionError("expected equality witnesses at n=2,3,4")
    if [n for n in range(5, 31) if status[n] != "unsat"]:
        raise AssertionError("meet-in-the-middle gap in n=5,...,30")

    # Independent implementation: build L_n with math.lcm at every n rather
    # than using the production script's prime-power increment table.
    lcm_value = 1
    uncovered: list[int] = []
    all_primes = primes_through(10_000)
    for n in range(1, 10_001):
        lcm_value = math.lcm(lcm_value, n)
        if n < 5:
            continue
        found = False
        active_primes = all_primes[: bisect.bisect_right(all_primes, n)]
        for p in reversed(active_primes):
            if 2 * p <= n:
                break
            required = pow((lcm_value // p) % p, -1, p)
            if required not in (1, p - 1):
                found = True
                break
        if not found:
            uncovered.append(n)
    if uncovered:
        raise AssertionError(f"singleton-prime audit uncovered {uncovered[:10]}")
    return {
        "mitm_exact_range": [2, 30],
        "mitm_sat_exactly": [2, 3, 4],
        "independent_modular_replay_range": [5, 10_000],
        "uncovered": uncovered,
    }


def maximum_rank_two_representations(
    exponents: tuple[int, ...], chosen: set[tuple[int, int]]
) -> int:
    count = 0
    for p, exponent in enumerate(exponents):
        if exponent == 0:
            continue
        reduced = list(exponents)
        reduced[p] -= 1
        if all(e in (0, 1) for e in reduced):
            support = tuple(i for i, e in enumerate(reduced) if e)
            if len(support) == 2 and tuple(sorted(support)) in chosen:
                count += 1
    return count


def audit_538() -> dict[str, object]:
    k = 5
    all_edges = list(itertools.combinations(range(k), 2))
    graph_count = 0
    for mask in range(1 << len(all_edges)):
        chosen = {edge for bit, edge in enumerate(all_edges) if mask & (1 << bit)}
        triangle_free = all(
            sum(tuple(sorted(e)) in chosen for e in ((a, b), (a, c), (b, c))) <= 2
            for a, b, c in itertools.combinations(range(k), 3)
        )
        max_representations = max(
            maximum_rank_two_representations(exponents, chosen)
            for exponents in itertools.product((0, 1, 2), repeat=k)
        )
        if triangle_free != (max_representations <= 2):
            raise AssertionError(f"rank-two equivalence failed for mask={mask}")
        graph_count += 1
    replay = json.loads((EVIDENCE / "erdos_538_squarefree_rank2.json").read_text())
    if not all(
        row["optimum_numerator"] == row["cut_optimum_numerator"]
        and row["optimum_denominator"] == row["cut_optimum_denominator"]
        for row in replay["rows"]
    ):
        raise AssertionError("weighted optimum/cut replay mismatch")
    return {
        "all_graphs_checked_on_vertices": k,
        "graph_count": graph_count,
        "exponent_vectors_per_graph": 3**k,
        "triangle_free_equivalence": True,
        "weighted_optimum_matches_cut_through_vertices": 6,
    }


def distinct_part_lcms_by_combinations(t: int) -> set[int]:
    result: set[int] = set()
    for size in range(1, t + 1):
        minimum_sum = size * (size + 1) // 2
        if minimum_sum > t:
            break
        for parts in itertools.combinations(range(1, t + 1), size):
            if sum(parts) == t:
                result.add(math.lcm(*parts))
    return result


def audit_859() -> dict[str, object]:
    evidence = json.loads((EVIDENCE / "erdos_859_density_toward_80.json").read_text())
    rows = {row["t"]: row for row in evidence["rows"]}
    for t in range(1, 16):
        lcms = distinct_part_lcms_by_combinations(t)
        minimal = sorted(
            value for value in lcms if not any(other != value and value % other == 0 for other in lcms)
        )
        if minimal != rows[t]["minimal_generators"]:
            raise AssertionError(f"independent lcm generators disagree at t={t}")
        density = Fraction(rows[t]["density_numerator"], rows[t]["density_denominator"])
        if not (0 < density <= 1):
            raise AssertionError(f"invalid density at t={t}")
    return {
        "independent_generator_replay_range": [1, 15],
        "production_exact_through": evidence["exact_through"],
        "production_stop_reason": evidence["stop_reason"],
        "all_checks_passed": True,
    }


def main() -> None:
    cgroup = Path("/proc/self/cgroup").read_text().strip()
    payload = {
        "schema_version": "amra.new-problem-round2-audit.v1",
        "resource_guard": {
            "observed_cgroup": cgroup,
            "inside_openmath_slice": "openmath.slice" in cgroup,
        },
        "erdos_317": audit_317(),
        "erdos_538": audit_538(),
        "erdos_859": audit_859(),
        "pid": os.getpid(),
    }
    output = EVIDENCE / "adversarial_replay.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
