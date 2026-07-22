#!/usr/bin/env python3
"""Exact algebra/exponent audit for round-10 geometry (#1083 and #827).

This script checks only rational exponent arithmetic and the fixed-hyperbola
root-product identity.  The combinatorial quantifiers are proved in REPORT.md.
"""

from __future__ import annotations

from fractions import Fraction
import json

import sympy as sp


def f(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    beta = Fraction(3, 5)

    # Critical #1083 layer Q=D=n^beta, suppressing logarithms.
    k_exp = 2 - 2 * beta
    domain_exp = Fraction(1)
    pencil_exp = 1 - beta
    total_overlap_exp = 2 * k_exp + 2 * domain_exp - 1
    rich_pair_count_exp = total_overlap_exp - 1
    cylinder_count_exp = rich_pair_count_exp - 2 * pencil_exp
    cylinder_occupancy_exp = 2 * domain_exp - 1 - beta
    cylinder_incidence_exp = cylinder_count_exp + cylinder_occupancy_exp
    ideal_two_dof_incidence_exp = (
        Fraction(2, 3) + Fraction(2, 3) * cylinder_count_exp
    )
    boundary_components_per_pair_exp = (
        2 * domain_exp - 1 - beta
    )

    assert k_exp == Fraction(4, 5)
    assert total_overlap_exp == Fraction(13, 5)
    assert rich_pair_count_exp == Fraction(8, 5)
    assert cylinder_count_exp == Fraction(4, 5)
    assert cylinder_occupancy_exp == Fraction(2, 5)
    assert cylinder_incidence_exp == Fraction(6, 5)
    assert ideal_two_dof_incidence_exp == cylinder_incidence_exp
    assert boundary_components_per_pair_exp == Fraction(2, 5)

    # A fixed t-fold common-domain star has R^t/n^(t-1), hence still
    # exponent one at the critical R=n^(1-o(1)) scale (logs suppressed).
    fixed_depth_star_rows = []
    for t in range(2, 7):
        exponent = t * domain_exp - (t - 1)
        assert exponent == 1
        fixed_depth_star_rows.append({
            "depth": t,
            "common_domain_exponent": f(exponent),
        })

    # Conditions used to remove parallel pairs and axis-fixed points.
    kr_exp = k_exp + domain_exp
    kr2q_exp = k_exp + 2 * domain_exp + beta
    max_axis_fixed_mass_scale_exp = (1 - beta) + 1
    assert kr_exp > 1
    assert kr2q_exp > 3
    assert 2 * domain_exp > max_axis_fixed_mass_scale_exp

    # #827: on one normalized hyperbola, fixing x,y makes the radius
    # equation a true quadratic in z whose two roots multiply to 1/(xy).
    x, y, z, rho = sp.symbols("x y z rho", nonzero=True)
    F = sp.expand(
        (1 + x * y) * (1 + x * z) * (1 + y * z)
        - rho * x * y * z
    )
    poly = sp.Poly(F, z)
    A, B, C = poly.all_coeffs()
    assert sp.factor(A - x * y * (1 + x * y)) == 0
    assert sp.factor(C - (1 + x * y)) == 0
    assert sp.factor(C / A - 1 / (x * y)) == 0

    # Midpoint-energy construction: a largest layer of [0,M-1]^d on a
    # Euclidean sphere has N >= M^(d-2)/d and hence energy exponent below.
    energy_rows = []
    for d in (6, 10, 22, 102):
        exponent = 3 - Fraction(2, d - 2)
        assert exponent < 3
        energy_rows.append({
            "ambient_dimension": d,
            "midpoint_energy_lower_exponent": f(exponent),
        })
    assert energy_rows[-1]["midpoint_energy_lower_exponent"] == "149/50"

    old_sampling_p = -Fraction(23, 30)
    all_color_cube_count = Fraction(4)
    surviving_cube_exp = all_color_cube_count + 6 * old_sampling_p
    assert surviving_cube_exp == -Fraction(3, 5)

    cube_removal_p = -Fraction(3, 5)
    cube_free_subset_exp = 1 + cube_removal_p
    sampled_cube_exp = all_color_cube_count + 6 * cube_removal_p
    assert cube_free_subset_exp == sampled_cube_exp == Fraction(2, 5)

    # If the only H6 input is O(M^5), balancing qM and q^6 M^5 gives
    # q=M^(-4/5) and retains only M^(1/5).
    second_sampling_loss = Fraction(4, 5)
    retained_exp = 1 - second_sampling_loss
    h6_conflict_exp = 5 - 6 * second_sampling_loss
    assert retained_exp == h6_conflict_exp == Fraction(1, 5)

    print(json.dumps({
        "schema": "amra.erdos_geometry.round10.v1",
        "arithmetic": "fractions.Fraction and exact sympy polynomial algebra",
        "problem_1083_critical_exponents": {
            "D_and_Q": f(beta),
            "carrying_plane_count_K": f(k_exp),
            "reflection_domain_R": f(domain_exp),
            "projective_pencil_kappa": f(pencil_exp),
            "total_nonparallel_off_axis_overlap": f(total_overlap_exp),
            "number_of_rich_plane_pairs": f(rich_pair_count_exp),
            "number_of_distinct_rich_cylinders": f(cylinder_count_exp),
            "points_per_rich_cylinder": f(cylinder_occupancy_exp),
            "cylinder_incidence_lower_exponent": f(
                cylinder_incidence_exp
            ),
            "hypothetical_two_dof_ST_main_exponent": f(
                ideal_two_dof_incidence_exp
            ),
            "boundary_components_per_high_order_pair": f(
                boundary_components_per_pair_exp
            ),
            "fixed_depth_common_domain_rows": fixed_depth_star_rows,
        },
        "problem_1083_conditions": {
            "K_times_R_exponent": f(kr_exp),
            "K_times_R_squared_times_Q_exponent": f(kr2q_exp),
            "axis_fixed_total_scale_exponent": f(
                max_axis_fixed_mass_scale_exp
            ),
            "R_squared_exponent": f(2 * domain_exp),
        },
        "problem_827_fixed_hyperbola": {
            "quadratic_A": str(A),
            "quadratic_B": str(B),
            "quadratic_C": str(C),
            "root_product": str(sp.factor(C / A)),
        },
        "problem_827_midpoint_energy_rows": energy_rows,
        "problem_827_all_color_cube_sampling": {
            "cube_count_upper_exponent": f(all_color_cube_count),
            "sampling_probability_exponent": f(old_sampling_p),
            "expected_surviving_cube_exponent": f(surviving_cube_exp),
            "cube_removal_sampling_exponent": f(cube_removal_p),
            "cube_free_subset_exponent": f(cube_free_subset_exp),
            "second_sampling_probability_loss": f(second_sampling_loss),
            "retained_vertex_exponent": f(retained_exp),
            "H6_conflict_exponent": f(h6_conflict_exp),
        },
        "warning": "The universal combinatorial and generic-projection arguments are in REPORT.md.",
        "result": "PASS",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
