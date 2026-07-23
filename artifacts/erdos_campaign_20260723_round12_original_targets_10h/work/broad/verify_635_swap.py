#!/usr/bin/env python3
"""Exact finite regression for the #635 semiprime swap formulas.

The symbolic nesting proof is in 635_SEMIPRIME_SWAP_GRAPH.md.  This program
only guards signs, endpoint conventions, and the displayed six-cycle.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict


def primes_up_to(limit: int) -> list[int]:
    prime = bytearray(b"\x01") * (limit + 1)
    prime[:2] = b"\x00\x00"
    for value in range(2, math.isqrt(limit) + 1):
        if prime[value]:
            prime[value * value :: value] = b"\x00" * (
                (limit - value * value) // value + 1
            )
    return [value for value in range(3, limit + 1, 2) if prime[value]]


def main() -> None:
    primes = primes_up_to(500)
    incident: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    all_incident: dict[int, list[tuple[int, int, int, int]]] = defaultdict(list)
    formula_checks = 0
    for exponent in range(1, 9):
        scale = 1 << exponent
        for index, p in enumerate(primes):
            for q in primes[index + 1 :]:
                x = scale * p * q
                if x > 250_000:
                    break
                lower, upper = x - q, x - p
                assert lower == q * (scale * p - 1)
                assert upper == p * (scale * q - 1)
                assert upper - lower == q - p
                incident[(scale, lower)].append((q, p))
                incident[(scale, upper)].append((p, q))
                all_incident[lower].append((x, scale, q, p))
                all_incident[upper].append((x, scale, p, q))
                formula_checks += 1

    collision_checks = 0
    for (scale, vertex), representations in incident.items():
        for first_index, (r0, s0) in enumerate(representations):
            for u0, v0 in representations[first_index + 1 :]:
                r, s, u, v = r0, s0, u0, v0
                if r == u:
                    assert s == v
                    continue
                if r > u:
                    r, s, u, v = u, v, r, s
                assert (scale * s - 1) % u == 0
                h = (scale * s - 1) // u
                assert h == (scale * v - 1) // r
                assert h % 2 == 1 and h != scale
                first = (min(r, s), max(r, s))
                second = (min(u, v), max(u, v))
                nested = (
                    first[0] < second[0] < second[1] < first[1]
                    or second[0] < first[0] < first[1] < second[1]
                )
                assert nested, (scale, vertex, (r, s), (u, v), h)
                collision_checks += 1

    mixed_conflict_checks = 0
    fixed_conflict_checks = 0
    for vertex, representations in all_incident.items():
        for first_index, (x, scale, r, s) in enumerate(representations):
            for y, other_scale, u, v in representations[first_index + 1 :]:
                assert x != y and r != u
                difference = abs(u - r)
                two_part = 0
                odd_part = difference
                while odd_part % 2 == 0:
                    odd_part //= 2
                    two_part += 1
                scale_exponent = scale.bit_length() - 1
                other_exponent = other_scale.bit_length() - 1
                predicted = two_part <= min(scale_exponent, other_exponent) and (
                    odd_part == 1 or odd_part == s == v
                )
                actual = x % abs(x - y) == 0
                assert abs(x - y) == difference
                assert predicted == actual, (
                    vertex,
                    (x, scale, r, s),
                    (y, other_scale, u, v),
                )
                mixed_conflict_checks += 1
                if scale == other_scale:
                    assert actual == (difference == scale)
                    fixed_conflict_checks += 1

    degree_three = all_incident[399]
    degree_three_labels = sorted(entry[0] for entry in degree_three)
    assert degree_three_labels == [402, 406, 418]
    for first_index, first in enumerate(degree_three_labels):
        for second in degree_three_labels[first_index + 1 :]:
            assert first % abs(first - second) != 0

    degree_four_data = [
        (9474, 2, 3, 1579),
        (9478, 2, 7, 677),
        (9482, 2, 11, 431),
        (9512, 8, 41, 29),
    ]
    degree_four_labels = sorted(entry[0] for entry in degree_four_data)
    for label, scale, omitted, partner in degree_four_data:
        assert label == scale * omitted * partner
        assert label - omitted == 9471
    for first_index, first in enumerate(degree_four_labels):
        for second in degree_four_labels[first_index + 1 :]:
            assert first % abs(first - second) != 0

    six_cycle = [
        (29184, 3, 19, 29165, 29181),
        (29252, 71, 103, 29149, 29181),
        (29432, 13, 283, 29149, 29419),
        (29492, 73, 101, 29391, 29419),
        (29488, 19, 97, 29391, 29469),
        (29472, 3, 307, 29165, 29469),
    ]
    degrees: dict[int, int] = defaultdict(int)
    for x, p, q, lower, upper in six_cycle:
        scale = x // (p * q)
        assert scale >= 2 and scale & (scale - 1) == 0
        assert (x - q, x - p) == (lower, upper)
        degrees[lower] += 1
        degrees[upper] += 1
    assert len(degrees) == 6 and set(degrees.values()) == {2}
    left_vertices = [entry[0] for entry in six_cycle]
    conflict_pairs: list[tuple[int, int, int]] = []
    for index, first in enumerate(left_vertices):
        for second in left_vertices[index + 1 :]:
            difference = abs(first - second)
            if first % difference == 0:
                assert second % difference == 0
                conflict_pairs.append((first, second, difference))
    assert conflict_pairs == [
        (29184, 29488, 304),
        (29492, 29488, 4),
        (29488, 29472, 16),
    ]

    oriented_cycle = [
        (29184, 512, 19, 3),
        (29252, 4, 71, 103),
        (29432, 8, 283, 13),
        (29492, 4, 73, 101),
        (29488, 16, 97, 19),
        (29472, 32, 3, 307),
    ]
    multipliers: list[int] = []
    label_increments: list[int] = []
    vertex_increments: list[int] = []
    for index, (x, scale, p, q) in enumerate(oriented_cycle):
        previous_x, previous_scale, previous_p, previous_q = oriented_cycle[index - 1]
        assert previous_x - previous_q == x - p
        numerator = previous_scale * previous_p - 1
        assert numerator % p == 0
        h = numerator // p
        assert scale * q == h * previous_q + 1
        multipliers.append(h)
        label_increments.append(p - previous_q)
        vertex_increments.append(p - q)
    assert sum(label_increments) == 0
    assert sum(vertex_increments) == 0
    assert sum(
        h * increment for h, increment in zip(multipliers, label_increments)
    ) == sum(
        scale * increment
        for (_, scale, _, _), increment in zip(oriented_cycle, vertex_increments)
    )
    assert math.prod(multipliers) < math.prod(
        scale for _, scale, _, _ in oriented_cycle
    )

    print(
        json.dumps(
            {
                "schema": "amra.erdos635.swap-regression.v1",
                "status": "PASS",
                "formula_checks": formula_checks,
                "fixed_valuation_collision_checks": collision_checks,
                "mixed_valuation_local_conflict_checks": mixed_conflict_checks,
                "fixed_valuation_local_conflict_checks": fixed_conflict_checks,
                "independent_degree_three_witness": {
                    "right_vertex": 399,
                    "left_labels": degree_three_labels,
                },
                "independent_degree_four_witness": {
                    "right_vertex": 9471,
                    "left_labels": degree_four_labels,
                },
                "six_cycle_vertices": sorted(degrees),
                "six_cycle_left_conflicts": conflict_pairs,
                "six_cycle_mixed_path_ledger": {
                    "multipliers": multipliers,
                    "label_increment_sum": sum(label_increments),
                    "vertex_increment_sum": sum(vertex_increments),
                    "weighted_identity": sum(
                        h * increment
                        for h, increment in zip(multipliers, label_increments)
                    ),
                },
                "scope": "finite regression only; the nesting theorem is symbolic",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
