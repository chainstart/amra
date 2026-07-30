#!/usr/bin/env python3
"""Verify the anchor-coherent iterated partner-reuse network."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from fractions import Fraction

Point = tuple[int, int]


def add(first: Point, second: Point) -> Point:
    return first[0] + second[0], first[1] + second[1]


def subtract(first: Point, second: Point) -> Point:
    return first[0] - second[0], first[1] - second[1]


def hub_points(hub_count: int, base: int = 4) -> tuple[Point, ...]:
    if base < 4:
        raise ValueError("the B_4 certificate requires base at least four")
    return tuple((index, base**index) for index in range(hub_count))


def difference_set(hubs: tuple[Point, ...]) -> set[Point]:
    return {
        subtract(first, second)
        for first in hubs
        for second in hubs
        if first != second
    }


def b4_certificate(hub_count: int, base: int = 4) -> dict[str, object]:
    hubs = hub_points(hub_count, base)
    seen: dict[tuple[int, int, int], tuple[int, ...]] = {}
    collision = None
    checked = 0
    for size in range(1, 5):
        for indices in itertools.combinations_with_replacement(
            range(hub_count), size
        ):
            total = (
                sum(index for index in indices),
                sum(base**index for index in indices),
            )
            checked += 1
            previous = seen.get((size, *total))
            if previous is not None and previous != indices:
                collision = (previous, indices)
                break
            seen[(size, *total)] = indices
        if collision is not None:
            break
    return {
        "hub_count": hub_count,
        "base": base,
        "checked_multisets": checked,
        "is_b4": collision is None,
        "collision": collision,
        "difference_count": len(difference_set(hubs)),
    }


def codegree_certificate(
    hub_count: int, base: int = 4
) -> dict[str, object]:
    hubs = hub_points(hub_count, base)
    differences = difference_set(hubs)
    representation_count: Counter[Point] = Counter(
        subtract(first, second)
        for first in differences
        for second in differences
    )
    zero = (0, 0)
    on_difference = {
        shift: representation_count[shift] for shift in differences
    }
    off_difference = {
        shift: count
        for shift, count in representation_count.items()
        if shift != zero and shift not in differences
    }
    return {
        "hub_count": hub_count,
        "difference_count": len(differences),
        "expected_difference_count": hub_count * (hub_count - 1),
        "on_difference_minimum": min(on_difference.values()),
        "on_difference_maximum": max(on_difference.values()),
        "expected_on_difference": 2 * hub_count - 4,
        "off_difference_maximum": max(off_difference.values(), default=0),
        "off_difference_bound": 4,
        "zero_codegree": representation_count[zero],
    }


def graph_certificate(
    nodes: set[Point], hub_count: int, base: int = 4
) -> dict[str, object]:
    differences = difference_set(hub_points(hub_count, base))
    ordered_nodes = tuple(sorted(nodes))
    neighbours = {
        node: {
            other
            for other in ordered_nodes
            if other != node and subtract(other, node) in differences
        }
        for node in ordered_nodes
    }
    degrees = {node: len(values) for node, values in neighbours.items()}
    edge_count = sum(degrees.values()) // 2
    wedge_by_middle = sum(
        degree * (degree - 1) // 2 for degree in degrees.values()
    )
    wedge_by_endpoints = sum(
        len(neighbours[first] & neighbours[second])
        for first, second in itertools.combinations(ordered_nodes, 2)
    )
    degree_sum = sum(degrees.values())
    degree_square_sum = sum(degree**2 for degree in degrees.values())
    node_count = len(nodes)
    coarse_moment_bound = (
        2 * hub_count * degree_sum + 4 * node_count**2
    )
    service_bound = (
        2 * node_count * hub_count
        + 2 * node_count ** Fraction(3, 2)
    )
    return {
        "node_count": node_count,
        "edge_count": edge_count,
        "oriented_service_count": degree_sum,
        "maximum_degree": max(degrees.values(), default=0),
        "degree_square_sum": degree_square_sum,
        "wedge_by_middle": wedge_by_middle,
        "wedge_by_endpoints": wedge_by_endpoints,
        "wedge_identity_holds": wedge_by_middle == wedge_by_endpoints,
        "coarse_moment_bound": coarse_moment_bound,
        "moment_bound_holds": degree_square_sum <= coarse_moment_bound,
        "service_bound": service_bound,
        "service_bound_holds": degree_sum <= service_bound,
    }


def single_star_nodes(
    hub_count: int, base: int = 4, centre: Point = (0, 0)
) -> set[Point]:
    differences = difference_set(hub_points(hub_count, base))
    return {centre} | {add(centre, difference) for difference in differences}


def parallel_clique_certificate(
    hub_count: int,
    orbit_count: int,
    base: int = 4,
    product_index: int | None = None,
) -> dict[str, object]:
    if product_index is None:
        product_index = 3 * hub_count
    hubs = hub_points(hub_count, base)
    maximum_radial_sum = max(
        base**u + base ** (product_index - u)
        for u in range(hub_count)
    )
    orbit_step = maximum_radial_sum + 1
    all_orbits = []
    cycle_checks: dict[int, bool] = {}
    layer_counts: Counter[int] = Counter()

    for orbit in range(orbit_count):
        total_energy = (orbit + 2) * orbit_step
        nodes = []
        for u, hub in enumerate(hubs):
            radius_index = product_index - u
            height_squared = (
                total_energy - base**u - base**radius_index
            )
            state = (radius_index, total_energy - base**u)
            assert height_squared > 0
            assert add(state, hub) == (product_index, total_energy)
            nodes.append(
                {
                    "hub_index": u,
                    "radius_index": radius_index,
                    "height_squared": height_squared,
                    "state": state,
                }
            )
            layer_counts[radius_index] += 1
        all_orbits.append(nodes)

    first_orbit = all_orbits[0]
    for length in (4, 6, 8):
        if hub_count < length:
            continue
        selected = first_orbit[:length]
        cycle_checks[length] = all(
            add(
                selected[index]["state"],
                hubs[selected[index]["hub_index"]],
            )
            == add(
                selected[(index + 1) % length]["state"],
                hubs[selected[(index + 1) % length]["hub_index"]],
            )
            for index in range(length)
        )

    return {
        "hub_count": hub_count,
        "orbit_count": orbit_count,
        "product_index": product_index,
        "service_count": orbit_count * hub_count * (hub_count - 1) // 2,
        "maximum_layer_count": max(layer_counts.values()),
        "expected_layer_count": orbit_count,
        "all_heights_positive": all(
            node["height_squared"] > 0
            for orbit in all_orbits
            for node in orbit
        ),
        "cycle_checks": cycle_checks,
    }


def exponent_certificate(
    eta_numerator: int, eta_denominator: int
) -> dict[str, Fraction]:
    eta = Fraction(eta_numerator, eta_denominator)
    alpha = Fraction(5, 6) + 2 * eta
    coherent_c = 2 - 1 / alpha
    required_c = (2 + 30 * eta) / (5 + 12 * eta)
    return {
        "eta": eta,
        "critical_hub_exponent": alpha,
        "coherent_network_c": coherent_c,
        "required_c": required_c,
        "margin": coherent_c - required_c,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub-count", type=int, default=8)
    parser.add_argument("--orbit-count", type=int, default=12)
    parser.add_argument("--base", type=int, default=4)
    parser.add_argument("--eta-numerator", type=int, default=1)
    parser.add_argument("--eta-denominator", type=int, default=30)
    args = parser.parse_args()

    star = single_star_nodes(args.hub_count, args.base)
    result = {
        "b4": b4_certificate(args.hub_count, args.base),
        "codegrees": codegree_certificate(
            args.hub_count, args.base
        ),
        "single_star_graph": graph_certificate(
            star, args.hub_count, args.base
        ),
        "parallel_cliques": parallel_clique_certificate(
            args.hub_count, args.orbit_count, args.base
        ),
        "exponents": exponent_certificate(
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
