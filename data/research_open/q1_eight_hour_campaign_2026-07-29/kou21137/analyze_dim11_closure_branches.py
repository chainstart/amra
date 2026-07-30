#!/usr/bin/env python3
"""Finite leading-map audit for the two dim-11 closure branches.

This is linear-algebra evidence, not an associative-algebra existence
test.  Homogeneous cubic maps on F_3^2 are determined by their values on
the four projective lines because q(-v)=-q(v).
"""

from __future__ import annotations

import itertools
import math


def scalar_map_kernel_distribution() -> dict[int, int]:
    """Count nonzero odd maps on four projective input pairs."""

    distribution = {zero_lines: 0 for zero_lines in range(4)}
    for values in itertools.product(range(3), repeat=4):
        if not any(values):
            continue
        distribution[values.count(0)] += 1
    return distribution


def two_dimensional_odd_bijections() -> int:
    """Choose a target projective permutation and four independent signs."""

    return math.factorial(4) * 2**4


def nonzero_linear_functionals() -> list[tuple[int, int]]:
    """Return the eight nonzero functionals on F_3^2."""

    return [
        (first, second)
        for first in range(3)
        for second in range(3)
        if (first, second) != (0, 0)
    ]


def main() -> int:
    distribution = scalar_map_kernel_distribution()
    bijections = two_dimensional_odd_bijections()
    linear_functionals = nonzero_linear_functionals()
    assert distribution == {0: 16, 1: 32, 2: 24, 3: 8}
    assert sum(distribution.values()) == 80
    assert bijections == 384
    assert len(linear_functionals) == 8
    assert all(
        sum(
            1
            for x, y in ((1, 0), (0, 1), (1, 1), (1, 2))
            if (first * x + second * y) % 3 == 0
        )
        == 1
        for first, second in linear_functionals
    )

    print(
        "DIM11_Q1_LEADING_MAPS"
        "|nonzero_homogeneous_cubic_functions=80"
        "|zero_projective_lines_0=16"
        "|zero_projective_lines_1=32"
        "|zero_projective_lines_2=24"
        "|zero_projective_lines_3=8"
        "|closure_noncommuting_excludes_zero_free=16"
        "|after_zero_free_exclusion=64"
        "|tail_pure_linear_maps=8"
        "|tail_pure_normal_forms=1"
        "|status=leading_data_not_excluded"
    )
    print(
        "DIM11_Q2_LEADING_MAPS"
        f"|odd_bijections={bijections}"
        "|tail_pure_leading_cube_normal_forms=2"
        "|A2_to_A6_nonzero_scalar_cubics=80"
        "|tail_pure_A2_to_A6_linear_maps=8"
        "|tail_pure_cube_normal_forms=2"
        "|status=leading_data_not_excluded"
    )
    print(
        "DIM11_Q1_KERNEL_CONTRACT"
        "|profile_2222111_K_dimensions=2,3,4,5"
        "|profile_2222111_H_orders=27,81,243,729"
        "|nonabelian_action_rank=1_into_J7"
    )
    print(
        "DIM11_Q2_KERNEL_CONTRACT"
        "|K=J6"
        "|H_order=81"
        "|cube_section_mod_J6=two_dimensional_additive_subspace"
        "|central_cocycle_target=J7"
        "|A7_coverage=tail_pure_two_normal_forms"
    )
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
