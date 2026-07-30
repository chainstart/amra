#!/usr/bin/env python3
"""Independent component-partition audit of the general beta^4 K coefficient.

This verifier deliberately does not import the page-partition transfer or the
interpolation verifier.  It reconstructs the first nine coefficients of each
fixed-page forest polynomial by exposing the component containing a fixed core
block and using the weighted bipartite Matrix--Tree formula.
"""

from __future__ import annotations

import argparse
import json
import math
from functools import lru_cache


def integer_choose(value: int, degree: int) -> int:
    """Generalized binomial coefficient for an integer upper argument."""
    if degree < 0:
        return 0
    numerator = math.prod(value - offset for offset in range(degree))
    return numerator // math.factorial(degree)


def component_tree_weight(
    twos: int,
    ones: int,
    pages: int,
) -> int:
    """Weighted tree sum on one nontrivial bipartite component."""
    core_count = twos + ones
    if core_count < 1 or pages < 1:
        raise ValueError("a nontrivial component must meet both sides")
    core_weight_sum = 2 * twos + ones
    core_weight_product = 2**twos
    return (
        pages ** (core_count - 1)
        * core_weight_sum ** (pages - 1)
        * core_weight_product
    )


@lru_cache(maxsize=None)
def bipartite_forest_coefficients(
    twos: int,
    ones: int,
    pages: int,
    maximum_degree: int = 8,
) -> tuple[int, ...]:
    """Forest polynomial for core weights ``2^twos 1^ones`` and pages.

    Vertices of each type remain labelled.  The recurrence selects the
    component containing one fixed core vertex, so every component partition
    is counted exactly once.
    """
    if min(twos, ones, pages, maximum_degree) < 0:
        raise ValueError("population and degree parameters must be nonnegative")
    if twos + ones == 0:
        # Page-only components can only be isolated vertices.
        return (1, *([0] * maximum_degree))

    pivot_is_two = twos > 0
    remaining_twos = twos - int(pivot_is_two)
    remaining_ones = ones - int(not pivot_is_two)
    coefficients = [0] * (maximum_degree + 1)

    for extra_twos in range(remaining_twos + 1):
        for extra_ones in range(remaining_ones + 1):
            component_twos = extra_twos + int(pivot_is_two)
            component_ones = extra_ones + int(not pivot_is_two)
            component_core_count = component_twos + component_ones
            core_choices = (
                math.comb(remaining_twos, extra_twos)
                * math.comb(remaining_ones, extra_ones)
            )
            for component_pages in range(pages + 1):
                if component_pages == 0:
                    if component_core_count != 1:
                        continue
                    component_degree = 0
                    tree_weight = 1
                else:
                    component_degree = component_core_count + component_pages - 1
                    if component_degree > maximum_degree:
                        continue
                    tree_weight = component_tree_weight(
                        component_twos,
                        component_ones,
                        component_pages,
                    )
                page_choices = math.comb(pages, component_pages)
                remainder = bipartite_forest_coefficients(
                    twos - component_twos,
                    ones - component_ones,
                    pages - component_pages,
                    maximum_degree - component_degree,
                )
                multiplier = core_choices * page_choices * tree_weight
                for remainder_degree, value in enumerate(remainder):
                    coefficients[component_degree + remainder_degree] += (
                        multiplier * value
                    )
    return tuple(coefficients)


def reduced_beta8_numerator(s: int, page_count: int) -> int:
    """Return [beta^8] of D/(1+k beta)^(2s-2k-2)."""
    if s < 4 or page_count < 0:
        raise ValueError("the disjoint-marked-edge profile needs s >= 4")
    target_degree = 8
    profiles = [
        bipartite_forest_coefficients(
            two_blocks,
            s - 2 * two_blocks,
            page_count,
            target_degree,
        )
        for two_blocks in range(3)
    ]
    determinant = [
        sum(
            profiles[1][left] * profiles[1][degree - left]
            - profiles[0][left] * profiles[2][degree - left]
            for left in range(degree + 1)
        )
        for degree in range(target_degree + 1)
    ]

    exponent = 2 * s - 2 * page_count - 2
    reduced: list[int] = []
    for degree in range(4, target_degree + 1):
        value = determinant[degree]
        for power in range(1, degree - 3):
            value -= (
                integer_choose(exponent, power)
                * page_count**power
                * reduced[degree - 4 - power]
            )
        reduced.append(value)
    return reduced[-1]


def predicted_beta8_numerator(s: int, page_count: int) -> int:
    """Closed formula before division by 2*k*(k-1)."""
    k = page_count
    polynomial = (
        4 * k**7
        + 12 * k**6
        + 12 * k**5 * s
        - 73 * k**5
        + 46 * k**4 * s
        - 507 * k**4
        + 3 * k**3 * s**2
        - 105 * k**3 * s
        + 54 * k**3
        + 12 * k**2 * s**2
        - 1036 * k**2 * s
        + 6672 * k**2
        - 6 * k * s**2
        - 531 * k * s
        + 5868 * k
        - 135 * s**2
        + 7110 * s
        - 37800
    )
    numerator = k * (k - 1) * (k - 2) * polynomial
    if numerator % 3:
        raise AssertionError("the displayed beta^8 numerator is not integral")
    return numerator // 3


def audit_rows() -> list[dict[str, int | bool]]:
    # The last three points lie outside the 11-by-9 interpolation grid used by
    # the primary verifier, and k=5,6 exercise the actual boundary s=k.
    points = (
        (2, 4),
        (3, 4),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 8),
        (11, 13),
        (12, 15),
        (14, 17),
    )
    rows: list[dict[str, int | bool]] = []
    for page_count, s in points:
        reconstructed = reduced_beta8_numerator(s, page_count)
        predicted = predicted_beta8_numerator(s, page_count)
        rows.append(
            {
                "page_count": page_count,
                "s": s,
                "component_reconstruction": reconstructed,
                "closed_formula": predicted,
                "match": reconstructed == predicted,
            }
        )
    if not all(bool(row["match"]) for row in rows):
        raise AssertionError("independent beta^4 component audit failed")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    rows = audit_rows()
    if args.json:
        print(json.dumps(rows, indent=2, sort_keys=True))
    else:
        for row in rows:
            print(
                "k={page_count} s={s} reconstructed={component_reconstruction} "
                "formula={closed_formula} match={match}".format(**row)
            )


if __name__ == "__main__":
    main()
