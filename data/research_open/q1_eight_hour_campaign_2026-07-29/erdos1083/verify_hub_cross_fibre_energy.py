#!/usr/bin/env python3
"""Verify hub cross-fibre energy models and exponent requirements."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import defaultdict
from fractions import Fraction


def radial_offset(first: int, second: int) -> int:
    return (2**first - 2**second) ** 2


def rational_hyperbola_pair(
    delta: int, parameter: int
) -> tuple[Fraction, Fraction]:
    value = Fraction(parameter, 1)
    shift = Fraction(delta, 1) / value
    return (value + shift) / 2, (shift - value) / 2


def real_pair_saturation(
    radius_count: int, height_count: int, first_hub: int, second_hub: int
) -> dict[str, object]:
    step = second_hub - first_hub
    overlap_size = (height_count - 1) // 2
    assigned: dict[int, set[Fraction]] = defaultdict(set)
    assigned[first_hub].add(Fraction(0))
    assigned[second_hub].add(Fraction(0))
    edge_certificates = []
    parameter_seed = 10**7

    for neighbour in range(radius_count):
        shifted_neighbour = neighbour - step
        if not 0 <= shifted_neighbour < radius_count:
            continue
        endpoints = {
            first_hub,
            second_hub,
            neighbour,
            shifted_neighbour,
        }
        if len(endpoints) < 4:
            continue
        first_offset = radial_offset(first_hub, neighbour)
        second_offset = radial_offset(second_hub, shifted_neighbour)
        delta = second_offset - first_offset
        targets = set()
        for index in range(overlap_size):
            parameter = (
                parameter_seed
                + neighbour * max(height_count, 1) * 100
                + index
            )
            first_height, second_height = rational_hyperbola_pair(
                delta, parameter
            )
            assigned[neighbour].add(first_height)
            assigned[shifted_neighbour].add(second_height)
            first_target = Fraction(first_offset) + first_height**2
            second_target = Fraction(second_offset) + second_height**2
            assert first_target == second_target
            targets.add(first_target)
        edge_certificates.append(
            {
                "first_sum": first_hub + neighbour,
                "second_sum": second_hub + shifted_neighbour,
                "target_count": len(targets),
            }
        )

    return {
        "radius_count": radius_count,
        "height_count": height_count,
        "overlap_size": overlap_size,
        "product_fibre_count": len(edge_certificates),
        "cross_fibre_energy": sum(
            edge["target_count"] for edge in edge_certificates
        ),
        "maximum_assigned_height_count": max(map(len, assigned.values())),
        "all_product_sums_match": all(
            edge["first_sum"] == edge["second_sum"]
            for edge in edge_certificates
        ),
        "all_target_counts_exact": all(
            edge["target_count"] == overlap_size
            for edge in edge_certificates
        ),
    }


def multiplicative_order(value: int, prime: int) -> int:
    current = 1
    for order in range(1, prime):
        current = current * value % prime
        if current == 1:
            return order
    raise AssertionError("invalid finite-field element")


def primitive_root(prime: int) -> int:
    for candidate in range(2, prime):
        if multiplicative_order(candidate, prime) == prime - 1:
            return candidate
    raise ValueError("prime has no primitive root")


def finite_field_model(prime: int, radius_count: int) -> dict[str, object]:
    if radius_count * 2 >= prime - 1:
        raise ValueError("require 2L < prime-1 to avoid exponent wrap")
    generator = primitive_root(prime)
    radii = [pow(generator, index, prime) for index in range(radius_count)]
    residues = {value * value % prime for value in range(prime)}
    fibres: dict[int, list[set[int]]] = defaultdict(list)
    for first, second in itertools.combinations(range(radius_count), 2):
        offset = (radii[first] - radii[second]) ** 2 % prime
        shifted = {(offset + value) % prime for value in residues}
        fibres[first + second].append(shifted)

    union_size = sum(len(set().union(*blocks)) for blocks in fibres.values())
    ordered_overlap = 0
    minimum_overlap = prime
    for blocks in fibres.values():
        for first_index, first in enumerate(blocks):
            for second_index, second in enumerate(blocks):
                if first_index == second_index:
                    continue
                overlap = len(first & second)
                ordered_overlap += overlap
                minimum_overlap = min(minimum_overlap, overlap)
    return {
        "prime": prime,
        "radius_count": radius_count,
        "generator": generator,
        "generator_order": multiplicative_order(generator, prime),
        "quadratic_residue_count": len(residues),
        "product_fibre_count": len(fibres),
        "union_size": union_size,
        "ordered_overlap": ordered_overlap,
        "minimum_same_fibre_overlap": minimum_overlap,
        "union_upper_bound": len(fibres) * prime,
        "intersection_lower_bound": Fraction(prime - 3, 4),
    }


def exponent_ledger(
    eta_numerator: int, eta_denominator: int
) -> dict[str, Fraction]:
    eta = Fraction(eta_numerator, eta_denominator)
    required_hub = Fraction(5, 6) + 2 * eta
    numerator = Fraction(4, 3) - eta
    required_c = 2 - numerator / required_hub
    return {
        "eta": eta,
        "required_hub": required_hub,
        "overlap_after_l_squared": numerator,
        "required_c": required_c,
        "closed_hub_exponent": numerator / (2 - required_c),
        "required_c_formula": (2 + 30 * eta) / (5 + 12 * eta),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta-numerator", type=int, default=1)
    parser.add_argument("--eta-denominator", type=int, default=30)
    args = parser.parse_args()
    result = {
        "exponent_ledger": exponent_ledger(
            args.eta_numerator, args.eta_denominator
        ),
        "real_pair_saturation": real_pair_saturation(18, 12, 0, 2),
        "finite_field_saturation": finite_field_model(43, 16),
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
