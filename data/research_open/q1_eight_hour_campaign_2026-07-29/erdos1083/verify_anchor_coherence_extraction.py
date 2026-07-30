#!/usr/bin/env python3
"""Verify the anchor-coherence extraction barrier and exponent ledger."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from fractions import Fraction


def exponent_ledger(
    eta_numerator: int, eta_denominator: int
) -> dict[str, Fraction]:
    eta = Fraction(eta_numerator, eta_denominator)
    hub_exponent = Fraction(2, 3) - eta / 2
    overlap_exponent = Fraction(10, 3) - eta
    coherent_bound_exponent = Fraction(3)
    bucket_count_exponent = (
        overlap_exponent - coherent_bound_exponent
    ) / 2
    return {
        "eta": eta,
        "minimal_hub_exponent": hub_exponent,
        "overlap_exponent": overlap_exponent,
        "union_exponent": Fraction(8, 3) + eta,
        "other_symbol_multiplicity_exponent": Fraction(1, 3) - eta,
        "coherent_bound_exponent": coherent_bound_exponent,
        "required_retention_exponent": (
            coherent_bound_exponent - overlap_exponent
        ),
        "one_hub_anchor_mass_exponent": (
            overlap_exponent - hub_exponent - 1
        ),
        "one_anchor_pair_mass_exponent": (
            overlap_exponent - 2 * hub_exponent - 2
        ),
        "one_random_anchor_per_hub_mass_exponent": (
            overlap_exponent - 2
        ),
        "maximum_bucket_count_exponent": bucket_count_exponent,
        "minimum_bucket_size_exponent": 1 - bucket_count_exponent,
        "value_level_joint_moment_exponent": overlap_exponent,
        "required_joint_moment_exponent": Fraction(11, 3) + eta,
        "missing_joint_factor_exponent": Fraction(1, 3) + 2 * eta,
    }


def latin_anchor_barrier(
    prime: int, hub_count: int
) -> dict[str, object]:
    if hub_count >= prime:
        raise ValueError("need distinct slopes in the finite field")
    slopes = tuple(range(hub_count))
    nonzero_fibres = range(1, prime)
    values = range(prime)
    block_anchor_counts: dict[tuple[int, int], Counter[int]] = {}
    anchor_vertex_degrees: Counter[tuple[int, int]] = Counter()
    pair_multiplicities = []
    common_label_services = 0

    for hub in range(hub_count):
        for fibre in nonzero_fibres:
            block_anchor_counts[(hub, fibre)] = Counter(
                (value + slopes[hub] * fibre) % prime
                for value in values
            )

    for first_hub, second_hub in itertools.combinations(
        range(hub_count), 2
    ):
        pair_count: Counter[tuple[int, int]] = Counter()
        for fibre in nonzero_fibres:
            for value in values:
                first_anchor = (
                    value + slopes[first_hub] * fibre
                ) % prime
                second_anchor = (
                    value + slopes[second_hub] * fibre
                ) % prime
                pair_count[(first_anchor, second_anchor)] += 1
                anchor_vertex_degrees[
                    (first_hub, first_anchor)
                ] += 1
                anchor_vertex_degrees[
                    (second_hub, second_anchor)
                ] += 1
                common_label_services += first_anchor == second_anchor
        pair_multiplicities.extend(pair_count.values())
        assert len(pair_count) == prime * (prime - 1)

    return {
        "prime": prime,
        "hub_count": hub_count,
        "fibre_count": prime - 1,
        "block_count": hub_count * (prime - 1),
        "incidence_count": hub_count * (prime - 1) * prime,
        "unordered_service_count": (
            hub_count
            * (hub_count - 1)
            // 2
            * prime
            * (prime - 1)
        ),
        "every_block_uses_each_anchor_once": all(
            len(counts) == prime and set(counts.values()) == {1}
            for counts in block_anchor_counts.values()
        ),
        "pair_multiplicity_minimum": min(pair_multiplicities),
        "pair_multiplicity_maximum": max(pair_multiplicities),
        "common_label_services": common_label_services,
        "anchor_degree_minimum": min(anchor_vertex_degrees.values()),
        "anchor_degree_maximum": max(anchor_vertex_degrees.values()),
        "expected_anchor_degree": (hub_count - 1) * (prime - 1),
    }


def finite_marginal_barrier(
    fibre_count: int,
    block_count_per_fibre: int,
    block_size: int,
    hub_block_count: int,
    other_group_size: int,
) -> dict[str, int]:
    other_block_count = block_count_per_fibre - hub_block_count
    if other_block_count % other_group_size:
        raise ValueError("other blocks must split into equal groups")
    other_group_count = other_block_count // other_group_size
    incidence_count = (
        fibre_count * block_count_per_fibre * block_size
    )
    union_size = fibre_count * block_size * (
        1 + other_group_count
    )
    unordered_hub_overlap = (
        fibre_count
        * block_size
        * hub_block_count
        * (hub_block_count - 1)
        // 2
    )
    unordered_other_overlap = (
        fibre_count
        * other_group_count
        * block_size
        * other_group_size
        * (other_group_size - 1)
        // 2
    )
    ordered_overlap = 2 * (
        unordered_hub_overlap + unordered_other_overlap
    )
    return {
        "fibre_count": fibre_count,
        "block_count": fibre_count * block_count_per_fibre,
        "incidence_count": incidence_count,
        "union_size": union_size,
        "unordered_hub_overlap": unordered_hub_overlap,
        "unordered_other_overlap": unordered_other_overlap,
        "ordered_overlap": ordered_overlap,
        "triangle_degree_sum": incidence_count,
        "joint_moment": ordered_overlap,
        "maximum_reuse_degree": max(
            hub_block_count - 1, other_group_size - 1
        ),
        "triangle_degree": 1,
    }


def squared_distance(
    first: tuple[Fraction, Fraction],
    second: tuple[Fraction, Fraction],
) -> Fraction:
    return sum(
        (left - right) ** 2
        for left, right in zip(first, second, strict=True)
    )


def gram_rectangle_identity(
    first_hub: tuple[Fraction, Fraction],
    second_hub: tuple[Fraction, Fraction],
    first_partner: tuple[Fraction, Fraction],
    second_partner: tuple[Fraction, Fraction],
) -> bool:
    left = (
        squared_distance(first_hub, first_partner)
        + squared_distance(second_hub, second_partner)
        - squared_distance(first_hub, second_partner)
        - squared_distance(second_hub, first_partner)
    )
    right = 2 * sum(
        (hub_left - hub_right) * (partner_right - partner_left)
        for hub_left, hub_right, partner_left, partner_right in zip(
            first_hub,
            second_hub,
            first_partner,
            second_partner,
            strict=True,
        )
    )
    return left == right


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=13)
    parser.add_argument("--hub-count", type=int, default=5)
    parser.add_argument("--eta-numerator", type=int, default=1)
    parser.add_argument("--eta-denominator", type=int, default=30)
    args = parser.parse_args()
    result = {
        "exponents": exponent_ledger(
            args.eta_numerator, args.eta_denominator
        ),
        "latin_anchor_barrier": latin_anchor_barrier(
            args.prime, args.hub_count
        ),
        "finite_marginal_barrier": finite_marginal_barrier(
            fibre_count=13,
            block_count_per_fibre=13,
            block_size=13,
            hub_block_count=3,
            other_group_size=2,
        ),
        "gram_rectangle_identity": gram_rectangle_identity(
            (Fraction(2), Fraction(5)),
            (Fraction(7), Fraction(-3)),
            (Fraction(11), Fraction(4)),
            (Fraction(-2), Fraction(9)),
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
