#!/usr/bin/env python3
"""Exact certificate for the realizable parity lifting barrier."""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class EdgeCertificate:
    cycle_pair: tuple[int, int]
    external_pair: tuple[int, int]
    common_sum: int
    cycle_offset: int
    external_offset: int
    offset_difference: int
    selected_value_count: int
    representation_count: int
    average_representation_multiplicity: float
    target_values_verified: bool


@dataclass(frozen=True)
class BarrierCertificate:
    height_count: int
    edge_certificates: tuple[EdgeCertificate, ...]
    all_external_indices_distinct: bool
    external_indices_disjoint_from_cycle: bool
    transversal_point_cycle_count: int


def squared_offset(pair: tuple[int, int]) -> int:
    return (2 ** pair[0] - 2 ** pair[1]) ** 2


def selected_values(height_count: int, same_parity: bool) -> set[int]:
    return {
        difference * difference
        for difference in range(height_count)
        if (difference % 2 == 0) == same_parity
        and (same_parity or difference > 0)
    }


def representation_edges(
    height_count: int,
    same_parity: bool,
) -> set[tuple[int, int]]:
    selected = selected_values(height_count, same_parity)
    return {
        (left, right)
        for left in range(height_count)
        for right in range(height_count)
        if (left - right) ** 2 in selected
    }


def transversal_cycle_count(height_count: int) -> int:
    edge_types = (True, True, True, False)
    graphs = [
        representation_edges(height_count, edge_type)
        for edge_type in edge_types
    ]
    return sum(
        all(
            (values[index], values[(index + 1) % 4]) in graphs[index]
            for index in range(4)
        )
        for values in itertools.product(range(height_count), repeat=4)
    )


def k23_cycle_parities(
    labels: tuple[int, int, int, int, int, int],
) -> tuple[int, int, int]:
    """Cycle parities in K_{2,3}.

    Labels are (a-x,a-y,a-z,b-x,b-y,b-z).
    """

    ax, ay, az, bx, by, bz = labels
    return (
        ax ^ ay ^ bx ^ by,
        ax ^ az ^ bx ^ bz,
        ay ^ az ^ by ^ bz,
    )


def barrier_certificate(height_count: int) -> BarrierCertificate:
    if height_count < 4 or height_count % 2:
        raise ValueError("need an even height count >= 4")
    cycle_pairs = ((0, 7), (7, 1), (1, 16), (16, 0))
    external_pairs = ((3, 4), (2, 6), (8, 9), (5, 11))
    edge_types = (True, True, True, False)
    certificates = []
    for cycle_pair, external_pair, same_parity in zip(
        cycle_pairs,
        external_pairs,
        edge_types,
    ):
        cycle_offset = squared_offset(cycle_pair)
        external_offset = squared_offset(external_pair)
        difference = cycle_offset - external_offset
        selected = selected_values(height_count, same_parity)
        target = {difference + value for value in selected}
        verified = all(
            external_offset + target_value
            == cycle_offset + selected_value
            for target_value, selected_value in zip(
                sorted(target),
                sorted(selected),
            )
        )
        representation_count = len(
            representation_edges(height_count, same_parity)
        )
        certificates.append(
            EdgeCertificate(
                cycle_pair=cycle_pair,
                external_pair=external_pair,
                common_sum=sum(cycle_pair),
                cycle_offset=cycle_offset,
                external_offset=external_offset,
                offset_difference=difference,
                selected_value_count=len(selected),
                representation_count=representation_count,
                average_representation_multiplicity=(
                    representation_count / len(selected)
                ),
                target_values_verified=verified,
            )
        )
    external_indices = [
        index for pair in external_pairs for index in pair
    ]
    return BarrierCertificate(
        height_count=height_count,
        edge_certificates=tuple(certificates),
        all_external_indices_distinct=(
            len(set(external_indices)) == len(external_indices)
        ),
        external_indices_disjoint_from_cycle=(
            set(external_indices).isdisjoint(
                index for pair in cycle_pairs for index in pair
            )
        ),
        transversal_point_cycle_count=transversal_cycle_count(height_count),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--height-count", type=int, default=20)
    args = parser.parse_args()
    print(
        json.dumps(
            asdict(barrier_certificate(args.height_count)),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
