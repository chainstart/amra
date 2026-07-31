#!/usr/bin/env python3
"""Independent component-set-partition audit of the beta^5--beta^8 theorem.

This implementation does not use the page-partition transfer or its
interpolation grid.  It sums bipartite-forest connected components using
the weighted Cayley formula and checks the resulting deconvolved kernel
against the printed all-k formulas at independent parameter pairs.
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from itertools import combinations

from verify_general_k_beta5_beta8 import K, S, claimed_coefficient


def generalized_binomial(top: int, lower: int) -> int:
    numerator = math.prod(top - offset for offset in range(lower))
    return numerator // math.factorial(lower)


@lru_cache(maxsize=None)
def forest_polynomial(
    core_weights: tuple[int, ...],
    page_count: int,
    maximum_degree: int,
) -> tuple[int, ...]:
    """Unrooted weighted K_(core,pages) forest polynomial.

    The distinguished first core vertex either is isolated or belongs to
    a unique nontrivial component with core set I and page set J.  The
    weighted bipartite Cayley factor is

        |J|^(|I|-1) (sum_I w)^(|J|-1) prod_I w.
    """

    if not core_weights:
        return (1, *([0] * maximum_degree))

    first = core_weights[0]
    remainder_weights = core_weights[1:]
    result = list(
        forest_polynomial(
            remainder_weights, page_count, maximum_degree
        )
    )
    indices = tuple(range(len(remainder_weights)))
    for extra_count in range(len(indices) + 1):
        for selected_indices in combinations(indices, extra_count):
            selected_set = set(selected_indices)
            selected_weights = (first,) + tuple(
                remainder_weights[index] for index in selected_indices
            )
            unused_weights = tuple(
                remainder_weights[index]
                for index in indices
                if index not in selected_set
            )
            for selected_pages in range(1, page_count + 1):
                degree = len(selected_weights) + selected_pages - 1
                if degree > maximum_degree:
                    continue
                component_weight = (
                    math.comb(page_count, selected_pages)
                    * selected_pages ** (len(selected_weights) - 1)
                    * sum(selected_weights) ** (selected_pages - 1)
                    * math.prod(selected_weights)
                )
                tail = forest_polynomial(
                    unused_weights,
                    page_count - selected_pages,
                    maximum_degree - degree,
                )
                for tail_degree, value in enumerate(tail):
                    result[degree + tail_degree] += (
                        component_weight * value
                    )
    return tuple(result)


def reduced_kernel_numerators(
    core_count: int,
    page_count: int,
    maximum_degree: int = 12,
) -> tuple[int, ...]:
    profiles = tuple(
        forest_polynomial(
            tuple([2] * doubled + [1] * (core_count - 2 * doubled)),
            page_count,
            maximum_degree,
        )
        for doubled in range(3)
    )
    determinant = tuple(
        sum(
            profiles[1][left] * profiles[1][degree - left]
            - profiles[0][left] * profiles[2][degree - left]
            for left in range(degree + 1)
        )
        for degree in range(maximum_degree + 1)
    )
    exponent = 2 * core_count - 2 * page_count - 2
    reduced: list[int] = []
    for degree in range(4, maximum_degree + 1):
        value = determinant[degree]
        for power in range(1, degree - 3):
            value -= (
                generalized_binomial(exponent, power)
                * page_count**power
                * reduced[degree - 4 - power]
            )
        reduced.append(value)
    return tuple(reduced)


def audit() -> dict[str, object]:
    parameter_pairs = ((4, 4), (4, 7), (5, 5), (5, 7), (6, 8))
    records = []
    for page_count, core_count in parameter_pairs:
        reduced = reduced_kernel_numerators(core_count, page_count)
        rank_values = {}
        for rank in range(5, 9):
            numerator = reduced[rank]
            denominator = 2 * page_count * (page_count - 1)
            if numerator % denominator:
                raise AssertionError("kernel normalization lost integrality")
            actual = numerator // denominator
            expected = claimed_coefficient(rank).subs(
                {K: page_count, S: core_count}
            )
            if actual != expected:
                raise AssertionError(
                    f"independent component audit failed at beta^{rank}"
                )
            rank_values[str(rank)] = str(actual)
        records.append(
            {
                "k": page_count,
                "s": core_count,
                "K_beta5_to_beta8": rank_values,
            }
        )
    return {
        "schema": "amra.opg1757.general-k-beta5-beta8-independent.v1",
        "status": "PASS",
        "method": (
            "Independent connected-component set-partition recurrence "
            "using the weighted bipartite Cayley formula; no page-state "
            "transfer and no interpolation."
        ),
        "records": records,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
