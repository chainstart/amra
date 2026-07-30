#!/usr/bin/env python3
"""Verify the cross-fibre shared-endpoint audit."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from fractions import Fraction


def squared_value_triples(
    first: tuple[int, ...],
    second: tuple[int, ...],
    third: tuple[int, ...],
) -> Counter[tuple[int, int, int]]:
    return Counter(
        (
            (left - middle) ** 2,
            (left - right) ** 2,
            (middle - right) ** 2,
        )
        for left, middle, right in itertools.product(first, second, third)
    )


def triangle_polynomial(value_triple: tuple[int, int, int]) -> bool:
    first, second, third = value_triple
    return (first + second - third) ** 2 == 4 * first * second


def selected_mod_seven_values(m: int) -> set[int]:
    return {
        difference * difference
        for difference in range(1, m)
        if difference % 7 in {1, 6}
    }


def selected_mod_seven_edges(m: int) -> set[tuple[int, int]]:
    values = selected_mod_seven_values(m)
    return {
        (left, right)
        for left in range(m)
        for right in range(m)
        if (left - right) ** 2 in values
    }


def selected_triangle_count(m: int) -> int:
    relation = selected_mod_seven_edges(m)
    return sum(
        (first, second) in relation
        and (first, third) in relation
        and (second, third) in relation
        for first, second, third in itertools.product(range(m), repeat=3)
    )


def selected_value_triangle_count(m: int) -> int:
    values = selected_mod_seven_values(m)
    return sum(
        triangle_polynomial(triple)
        for triple in itertools.product(values, repeat=3)
    )


def exponent_ledger(
    eta_numerator: int, eta_denominator: int, delta_numerator: int,
    delta_denominator: int
) -> dict[str, Fraction]:
    eta = Fraction(eta_numerator, eta_denominator)
    delta = Fraction(delta_numerator, delta_denominator)
    full_incidence_cap = Fraction(11, 3) + eta
    large_block_threshold = Fraction(5, 3) + eta + delta
    large_block_count = full_incidence_cap - large_block_threshold
    retained_tests = (
        3 + 2 + 3 * (1 - large_block_threshold)
    )
    return {
        "eta": eta,
        "delta": delta,
        "full_incidence_cap": full_incidence_cap,
        "large_block_threshold": large_block_threshold,
        "large_block_count": large_block_count,
        "bad_radius_triangles": large_block_count + 1,
        "forced_correlation": Fraction(10, 3) - eta,
        "retained_compatible_tests": retained_tests,
        "retained_tests_expected": 3 - 3 * eta - 3 * delta,
        "selected_incidence": Fraction(3),
        "test_degree_per_incidence": retained_tests - 3,
        "propagation_gap": Fraction(1, 3) + 2 * eta,
    }


def build_certificate(m: int) -> dict[str, object]:
    if m % 7:
        raise ValueError("m must be divisible by seven")
    sample_sets = (
        tuple(range(m)),
        tuple(2 * value + 1 for value in range(m)),
        tuple(value * value - 3 for value in range(m)),
    )
    triples = squared_value_triples(*sample_sets)
    return {
        "height_count": m,
        "point_triple_count": m**3,
        "distinct_value_triple_count": len(triples),
        "maximum_point_preimage": max(triples.values()),
        "all_value_triples_compatible": all(
            triangle_polynomial(triple) for triple in triples
        ),
        "theorem_lower_bound": Fraction(m * m, 4),
        "selected_mod_seven_value_count": len(
            selected_mod_seven_values(m)
        ),
        "selected_mod_seven_edge_count": len(
            selected_mod_seven_edges(m)
        ),
        "selected_mod_seven_triangle_count": selected_triangle_count(m),
        "selected_mod_seven_value_triangle_count": (
            selected_value_triangle_count(m)
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--height-count", type=int, default=14)
    parser.add_argument("--eta-numerator", type=int, default=1)
    parser.add_argument("--eta-denominator", type=int, default=30)
    parser.add_argument("--delta-numerator", type=int, default=1)
    parser.add_argument("--delta-denominator", type=int, default=100)
    args = parser.parse_args()
    result = {
        "finite_certificate": build_certificate(args.height_count),
        "exponent_ledger": exponent_ledger(
            args.eta_numerator,
            args.eta_denominator,
            args.delta_numerator,
            args.delta_denominator,
        ),
    }
    print(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
            default=lambda value: (
                int(value)
                if isinstance(value, Fraction) and value.denominator == 1
                else str(value)
            ),
        )
    )


if __name__ == "__main__":
    main()
