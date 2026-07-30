#!/usr/bin/env python3
"""Verify the Gram rectangle energy and translation-fan barrier."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction

Point = tuple[Fraction, Fraction]


def exponent_ledger(
    eta_numerator: int, eta_denominator: int
) -> dict[str, Fraction]:
    eta = Fraction(eta_numerator, eta_denominator)
    service = Fraction(10, 3) - eta
    union = Fraction(8, 3) + eta
    cell_moment = 2 * service - union
    target = Fraction(11, 3) + eta
    required_average = Fraction(1, 3) + 2 * eta
    return {
        "eta": eta,
        "service_exponent": service,
        "union_exponent": union,
        "cell_moment_exponent": cell_moment,
        "target_point_moment_exponent": target,
        "cell_surplus_exponent": cell_moment - target,
        "cell_average_gain_exponent": cell_moment - service,
        "required_average_gain_exponent": required_average,
        "maximum_point_representation_exponent": (
            cell_moment - target
        ),
        "unconditional_representation_cap_exponent": Fraction(2),
        "unconditional_point_moment_exponent": (
            cell_moment - 2
        ),
    }


def radial_offset(first: int, second: int, ratio: int = 2) -> int:
    return (ratio**first - ratio**second) ** 2


def squared_distance(first: Point, second: Point) -> Fraction:
    return (first[0] - second[0]) ** 2 + (
        first[1] - second[1]
    ) ** 2


def gram_identity(
    first_hub: Point,
    first_partner: Point,
    second_hub: Point,
    second_partner: Point,
) -> bool:
    left = (
        squared_distance(first_hub, first_partner)
        + squared_distance(second_hub, second_partner)
        - squared_distance(first_hub, second_partner)
        - squared_distance(second_hub, first_partner)
    )
    right = 2 * (
        (first_hub[0] - second_hub[0])
        * (second_partner[0] - first_partner[0])
        + (first_hub[1] - second_hub[1])
        * (second_partner[1] - first_partner[1])
    )
    return left == right


def translation_fan(
    service_count: int,
    ratio: int = 2,
    indices: tuple[int, int, int, int] = (0, 6, 1, 5),
) -> dict[str, object]:
    first_hub_index, first_partner_index, second_hub_index, (
        second_partner_index
    ) = indices
    if (
        first_hub_index + first_partner_index
        != second_hub_index + second_partner_index
    ):
        raise ValueError("diagonal radius pairs need the same product")

    first_offset = radial_offset(
        first_hub_index, first_partner_index, ratio
    )
    second_offset = radial_offset(
        second_hub_index, second_partner_index, ratio
    )
    delta = Fraction(second_offset - first_offset)
    parameter = Fraction(1)
    first_vertical_difference = (
        parameter + delta / parameter
    ) / 2
    second_vertical_difference = (
        delta / parameter - parameter
    ) / 2
    cross_vertical_difference = Fraction(7)

    services = []
    cross_cell_counts: Counter[tuple[int, Fraction]] = Counter()
    point_cross_signatures = set()
    all_gram_identities = True

    for index in range(service_count):
        translation = Fraction(10_000 * index)
        first_hub = (
            Fraction(ratio**first_hub_index),
            translation,
        )
        first_partner = (
            Fraction(ratio**first_partner_index),
            translation + first_vertical_difference,
        )
        second_hub = (
            Fraction(ratio**second_hub_index),
            translation
            + cross_vertical_difference
            + second_vertical_difference,
        )
        second_partner = (
            Fraction(ratio**second_partner_index),
            translation + cross_vertical_difference,
        )
        first_diagonal = squared_distance(
            first_hub, first_partner
        )
        second_diagonal = squared_distance(
            second_hub, second_partner
        )
        first_cross = squared_distance(
            first_hub, second_partner
        )
        second_cross = squared_distance(
            second_hub, first_partner
        )
        first_cell = (
            first_hub_index + second_partner_index,
            first_cross,
        )
        second_cell = (
            second_hub_index + first_partner_index,
            second_cross,
        )
        cross_cell_counts[first_cell] += 1
        cross_cell_counts[second_cell] += 1
        point_cross_signatures.add(
            (first_cell, first_hub, second_partner)
        )
        point_cross_signatures.add(
            (second_cell, second_hub, first_partner)
        )
        all_gram_identities &= gram_identity(
            first_hub,
            first_partner,
            second_hub,
            second_partner,
        )
        services.append(
            {
                "first_diagonal": first_diagonal,
                "second_diagonal": second_diagonal,
                "first_cross": first_cross,
                "second_cross": second_cross,
            }
        )

    cell_moment = sum(
        multiplicity**2
        for multiplicity in cross_cell_counts.values()
    )
    point_moment = len(point_cross_signatures)
    return {
        "service_count": service_count,
        "height_count_per_radius": service_count,
        "diagonal_product_sums_match": (
            first_hub_index + first_partner_index
            == second_hub_index + second_partner_index
        ),
        "all_diagonal_distances_match": all(
            service["first_diagonal"]
            == service["second_diagonal"]
            for service in services
        ),
        "all_first_cross_values_match": (
            len({service["first_cross"] for service in services}) == 1
        ),
        "all_second_cross_values_match": (
            len({service["second_cross"] for service in services})
            == 1
        ),
        "all_gram_identities": all_gram_identities,
        "cross_cell_count": len(cross_cell_counts),
        "cross_occurrence_count": sum(cross_cell_counts.values()),
        "cell_moment": cell_moment,
        "expected_cell_moment": 2 * service_count**2,
        "point_pair_signature_count": len(point_cross_signatures),
        "point_moment": point_moment,
        "expected_point_moment": 2 * service_count,
        "first_vertical_difference": first_vertical_difference,
        "second_vertical_difference": second_vertical_difference,
    }


def cauchy_moment(
    cell_multiplicities: tuple[int, ...],
    point_parts: tuple[tuple[int, ...], ...],
) -> dict[str, object]:
    if len(cell_multiplicities) != len(point_parts):
        raise ValueError("each cell needs one point-pair partition")
    if any(
        sum(parts) != multiplicity
        for multiplicity, parts in zip(
            cell_multiplicities, point_parts, strict=True
        )
    ):
        raise ValueError("point parts must sum to their cell count")
    occurrence_count = sum(cell_multiplicities)
    cell_count = len(cell_multiplicities)
    maximum_part_count = max(map(len, point_parts), default=0)
    cell_moment = sum(value**2 for value in cell_multiplicities)
    point_moment = sum(
        value**2 for parts in point_parts for value in parts
    )
    return {
        "occurrence_count": occurrence_count,
        "cell_count": cell_count,
        "maximum_point_pairs_per_cell": maximum_part_count,
        "cell_moment": cell_moment,
        "point_moment": point_moment,
        "cell_cauchy_holds": (
            cell_moment * cell_count >= occurrence_count**2
        ),
        "point_refinement_holds": (
            point_moment * maximum_part_count >= cell_moment
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--service-count", type=int, default=17)
    parser.add_argument("--eta-numerator", type=int, default=1)
    parser.add_argument("--eta-denominator", type=int, default=30)
    args = parser.parse_args()
    result = {
        "exponents": exponent_ledger(
            args.eta_numerator, args.eta_denominator
        ),
        "translation_fan": translation_fan(args.service_count),
        "finite_cauchy": cauchy_moment(
            (7, 5, 4),
            ((3, 2, 2), (2, 2, 1), (1, 1, 1, 1)),
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
