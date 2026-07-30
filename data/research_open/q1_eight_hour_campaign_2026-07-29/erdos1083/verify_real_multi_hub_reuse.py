#!/usr/bin/env python3
"""Verify the real multi-hub coordinate-reuse barrier."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import defaultdict
from fractions import Fraction


def radial_offset(first: int, second: int) -> int:
    return (2**first - 2**second) ** 2


def multi_hub_star(
    hub_count: int, height_count: int, radius_count: int
) -> dict[str, object]:
    if hub_count > height_count:
        raise ValueError("receiving sets need at least hub_count positions")
    if radius_count < 3 * hub_count + 2:
        raise ValueError("radius universe is too small")

    hubs = tuple(range(hub_count))
    source_radius = 2 * hub_count
    maximum_offset = max(
        radial_offset(first, second)
        for first, second in itertools.combinations(range(radius_count), 2)
    )
    source_height_squared = 4 * maximum_offset + 1
    receiving_radicands: dict[int, set[int]] = defaultdict(set)
    services = []

    for first_hub, second_hub in itertools.combinations(hubs, 2):
        difference = second_hub - first_hub
        receiving_radius = source_radius - difference
        first_offset = radial_offset(first_hub, source_radius)
        second_offset = radial_offset(second_hub, receiving_radius)
        partner_squared = (
            source_height_squared + first_offset - second_offset
        )
        assert partner_squared > 0
        receiving_radicands[receiving_radius].add(partner_squared)
        services.append(
            {
                "first_hub": first_hub,
                "second_hub": second_hub,
                "source_radius": source_radius,
                "receiving_radius": receiving_radius,
                "first_sum": first_hub + source_radius,
                "second_sum": second_hub + receiving_radius,
                "first_shifted_value": (
                    first_offset + source_height_squared
                ),
                "second_shifted_value": (
                    second_offset + partner_squared
                ),
            }
        )

    return {
        "hub_count": hub_count,
        "height_count": height_count,
        "radius_count": radius_count,
        "source_radius": source_radius,
        "source_height_squared": source_height_squared,
        "service_count": len(services),
        "expected_service_count": hub_count * (hub_count - 1) // 2,
        "receiving_radius_count": len(receiving_radicands),
        "maximum_receiving_height_count": max(
            map(len, receiving_radicands.values())
        ),
        "total_partner_height_count": sum(
            map(len, receiving_radicands.values())
        ),
        "all_product_sums_match": all(
            service["first_sum"] == service["second_sum"]
            for service in services
        ),
        "all_shifted_values_match": all(
            service["first_shifted_value"]
            == service["second_shifted_value"]
            for service in services
        ),
    }


def subtraction_identity(
    first: tuple[Fraction, Fraction, Fraction],
    second: tuple[Fraction, Fraction, Fraction],
    shared_height: Fraction,
    first_delta: Fraction,
    second_delta: Fraction,
) -> bool:
    first_anchor, first_partner_anchor, first_partner = first
    second_anchor, second_partner_anchor, second_partner = second
    left = 2 * shared_height * (second_anchor - first_anchor)
    right = (
        second_anchor**2
        - first_anchor**2
        + (first_partner_anchor - first_partner) ** 2
        - (second_partner_anchor - second_partner) ** 2
        + first_delta
        - second_delta
    )
    first_equation = (
        (first_anchor - shared_height) ** 2
        - (first_partner_anchor - first_partner) ** 2
        == first_delta
    )
    second_equation = (
        (second_anchor - shared_height) ** 2
        - (second_partner_anchor - second_partner) ** 2
        == second_delta
    )
    return first_equation and second_equation and left == right


def exponent_ledger(
    eta_numerator: int, eta_denominator: int
) -> dict[str, Fraction]:
    eta = Fraction(eta_numerator, eta_denominator)
    required_c = (2 + 30 * eta) / (5 + 12 * eta)
    return {
        "eta": eta,
        "required_c": required_c,
        "best_unconditional_c": Fraction(0),
        "pointwise_service_exponent_in_u": Fraction(2),
        "required_pointwise_exponent": 2 - required_c,
        "coordinate_universe_exponent_in_l": Fraction(2),
        "required_second_moment_u_exponent": 4 - 2 * required_c,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub-count", type=int, default=8)
    parser.add_argument("--height-count", type=int, default=12)
    parser.add_argument("--radius-count", type=int, default=30)
    parser.add_argument("--eta-numerator", type=int, default=1)
    parser.add_argument("--eta-denominator", type=int, default=30)
    args = parser.parse_args()
    result = {
        "multi_hub_star": multi_hub_star(
            args.hub_count, args.height_count, args.radius_count
        ),
        "exponent_ledger": exponent_ledger(
            args.eta_numerator, args.eta_denominator
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
