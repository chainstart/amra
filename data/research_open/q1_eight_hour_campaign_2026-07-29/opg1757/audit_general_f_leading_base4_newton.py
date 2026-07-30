#!/usr/bin/env python3
"""Audit the natural base-four Newton expansion of the first F coefficient."""

from __future__ import annotations

import argparse
import json
import math
from functools import lru_cache


def weighted_tree_component(twos: int, ones: int) -> int:
    size = twos + ones
    if size == 1:
        return 1
    return 2**twos * (2 * twos + ones) ** (size - 2)


@lru_cache(maxsize=None)
def complete_graph_forest_coefficients(
    twos: int,
    ones: int,
    maximum_degree: int,
) -> tuple[int, ...]:
    """Weighted complete-graph forest polynomial by a fixed-component split."""
    if twos + ones == 0:
        return (1, *([0] * maximum_degree))
    coefficients = [0] * (maximum_degree + 1)
    if ones:
        for component_twos in range(twos + 1):
            for other_ones in range(ones):
                degree = component_twos + other_ones
                if degree > maximum_degree:
                    continue
                multiplier = (
                    math.comb(twos, component_twos)
                    * math.comb(ones - 1, other_ones)
                    * weighted_tree_component(
                        component_twos,
                        other_ones + 1,
                    )
                )
                remainder = complete_graph_forest_coefficients(
                    twos - component_twos,
                    ones - other_ones - 1,
                    maximum_degree - degree,
                )
                for remainder_degree, value in enumerate(remainder):
                    coefficients[degree + remainder_degree] += (
                        multiplier * value
                    )
    else:
        for other_twos in range(twos):
            degree = other_twos
            if degree > maximum_degree:
                continue
            multiplier = (
                math.comb(twos - 1, other_twos)
                * weighted_tree_component(other_twos + 1, 0)
            )
            remainder = complete_graph_forest_coefficients(
                twos - other_twos - 1,
                0,
                maximum_degree - degree,
            )
            for remainder_degree, value in enumerate(remainder):
                coefficients[degree + remainder_degree] += multiplier * value
    return tuple(coefficients)


def first_f_coefficient(page_count: int, vertex_count: int) -> int:
    rows = [
        complete_graph_forest_coefficients(
            marked_edges,
            vertex_count - 2 * marked_edges,
            page_count,
        )
        for marked_edges in range(3)
    ]
    determinant = sum(
        rows[1][left] * rows[1][page_count - left]
        - rows[0][left] * rows[2][page_count - left]
        for left in range(page_count + 1)
    )
    numerator = math.factorial(page_count) * determinant
    denominator = 2 * page_count * (page_count - 1)
    if numerator % denominator:
        raise AssertionError("normalization ceased to be integral")
    return numerator // denominator


def forward_differences(values: list[int]) -> list[int]:
    coefficients: list[int] = []
    current = values
    while current:
        coefficients.append(current[0])
        current = [
            current[index + 1] - current[index]
            for index in range(len(current) - 1)
        ]
    return coefficients


def audit_row(page_count: int) -> dict[str, object]:
    degree = 2 * page_count - 4
    values = [
        first_f_coefficient(page_count, 4 + offset)
        for offset in range(degree + 1)
    ]
    newton = forward_differences(values)
    first_nonzero = next(
        (index for index, value in enumerate(newton) if value),
        None,
    )
    predicted_support = (page_count - 2) // 2
    return {
        "page_count": page_count,
        "degree": degree,
        "base_vertex_count": 4,
        "first_nonzero_newton_index": first_nonzero,
        "capacity_predicted_first_possible_index": predicted_support,
        "all_newton_coefficients_nonnegative": all(
            value >= 0 for value in newton
        ),
        "top_newton_coefficient": newton[-1],
        "expected_monic_top": math.factorial(degree),
        "newton_coefficients": newton,
    }


def build_audit(maximum_page_count: int = 30) -> dict[str, object]:
    if maximum_page_count < 2:
        raise ValueError("maximum page count must be at least two")
    rows = [
        audit_row(page_count)
        for page_count in range(2, maximum_page_count + 1)
    ]
    if not all(
        row["all_newton_coefficients_nonnegative"]
        and row["first_nonzero_newton_index"]
        == row["capacity_predicted_first_possible_index"]
        and row["top_newton_coefficient"] == row["expected_monic_top"]
        for row in rows
    ):
        raise AssertionError("base-four Newton audit failed")
    return {
        "schema": "amra.opg1757.F-leading-base4-Newton.v1",
        "scope": (
            "Finite exact evidence only: all Newton coefficients in "
            "binom(s-4,q) are nonnegative for k=2..maximum_page_count."
        ),
        "maximum_page_count": maximum_page_count,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-page-count", type=int, default=30)
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()
    audit = build_audit(args.maximum_page_count)
    if args.full:
        print(json.dumps(audit, indent=2, sort_keys=True))
        return
    for row in audit["rows"]:
        print(
            "k={page_count} first={first_nonzero_newton_index} "
            "nonnegative={all_newton_coefficients_nonnegative} "
            "top={top_newton_coefficient}".format(**row)
        )


if __name__ == "__main__":
    main()
