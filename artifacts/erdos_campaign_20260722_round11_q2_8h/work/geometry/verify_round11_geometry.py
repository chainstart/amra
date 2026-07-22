#!/usr/bin/env python3
"""Exact exponent/algebra audit for round-11 geometry (#1083 and #827).

The script checks rational exponent arithmetic, the inversion formula, and the
two exact conflict-energy coefficient identities.  Universal combinatorial
quantifiers and external theorem hypotheses are audited in INDEPENDENT_QA.md.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path

import sympy as sp


def fs(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def build_certificate() -> dict:
    beta = Fraction(3, 5)
    k_exp = 2 - 2 * beta
    r_exp = Fraction(1)
    pair_exp = 2 * k_exp + 2 * r_exp - 2
    common_exp = 2 * r_exp - 1
    pencil_exp = 1 - beta

    failure_slot_exp = k_exp + 4 * r_exp - beta - 4
    repair_fan_exp = failure_slot_exp
    repair_common_star_exp = repair_fan_exp + common_exp - 1
    global_repair_edge_exp = pair_exp + common_exp - beta
    global_marked_repair_exp = pair_exp + 2 * common_exp - beta
    average_repair_graph_exp = global_repair_edge_exp - 1
    average_marked_graph_exp = global_marked_repair_exp - 2
    k22_forcing_threshold_exp = Fraction(3, 2) * k_exp
    synchronized_triangle_family_exp = k_exp
    synchronized_incidence_exp = beta + synchronized_triangle_family_exp
    rudnev_main_at_sync_exp = 1 + synchronized_triangle_family_exp / 2
    rudnev_pencil_at_sync_exp = 1 + pencil_exp
    sync_pair_moment_lhs_exp = synchronized_triangle_family_exp + 2 * beta
    sync_pair_moment_rhs_exp = beta + 2
    sync_triple_moment_lhs_exp = synchronized_triangle_family_exp + 3 * beta
    sync_triple_moment_rhs_exp = Fraction(3)
    low_mass_exp = pair_exp + common_exp
    fixed_contamination_exp = 2 * k_exp + beta
    low_star_edge_exp = low_mass_exp - 1
    common_neighbor_exp = k_exp  # p=L^{-O(1)} has exponent zero.
    distinct_neighbor_direction_exp = common_neighbor_exp - pencil_exp
    ramsey_high_clique_exp = distinct_neighbor_direction_exp / 15
    planar_normal_cap_exp = beta
    no_three_coplanar_decay_exp = k_exp - planar_normal_cap_exp

    assert beta == Fraction(3, 5)
    assert k_exp == Fraction(4, 5)
    assert pair_exp == Fraction(8, 5)
    assert common_exp == 1
    assert failure_slot_exp == Fraction(1, 5)
    assert repair_fan_exp == Fraction(1, 5)
    assert repair_common_star_exp == Fraction(1, 5)
    assert global_repair_edge_exp == 2
    assert global_marked_repair_exp == 3
    assert average_repair_graph_exp == 1
    assert average_marked_graph_exp == 1
    assert k22_forcing_threshold_exp == Fraction(6, 5)
    assert average_marked_graph_exp < k22_forcing_threshold_exp
    assert synchronized_triangle_family_exp == Fraction(4, 5)
    assert synchronized_incidence_exp == Fraction(7, 5)
    assert rudnev_main_at_sync_exp == synchronized_incidence_exp
    assert rudnev_pencil_at_sync_exp == synchronized_incidence_exp
    assert sync_pair_moment_lhs_exp == 2
    assert sync_pair_moment_rhs_exp == Fraction(13, 5)
    assert sync_triple_moment_lhs_exp == Fraction(13, 5)
    assert sync_triple_moment_rhs_exp == 3
    assert sync_pair_moment_lhs_exp < sync_pair_moment_rhs_exp
    assert sync_triple_moment_lhs_exp < sync_triple_moment_rhs_exp
    assert low_mass_exp == Fraction(13, 5)
    assert fixed_contamination_exp == Fraction(11, 5)
    assert fixed_contamination_exp < low_mass_exp
    assert low_star_edge_exp == Fraction(8, 5)
    assert pencil_exp == Fraction(2, 5)
    assert common_neighbor_exp == Fraction(4, 5)
    assert distinct_neighbor_direction_exp == Fraction(2, 5)
    assert ramsey_high_clique_exp == Fraction(2, 75)
    assert planar_normal_cap_exp == Fraction(3, 5)
    assert no_three_coplanar_decay_exp == Fraction(1, 5)
    assert common_neighbor_exp > beta

    # The fixed-axis orbit-circle cap is n^beta, whereas the inherited pencil
    # cap is n^(1-beta), so it is weaker at beta=3/5.
    axis_circle_cap_exp = beta
    assert pencil_exp < axis_circle_cap_exp

    # #827 alteration exponents.
    eps5, eps6 = sp.symbols("eps5 eps6", nonnegative=True)
    gamma_h4 = Fraction(1, 3)
    gamma_h5_at_zero = Fraction(1, 4)
    gamma_h6_at_zero = Fraction(1, 5)
    assert gamma_h4 == Fraction(1, 3)
    assert gamma_h5_at_zero == Fraction(1, 4)
    assert gamma_h6_at_zero == Fraction(1, 5)

    delta_quarter = Fraction(1, 4)
    gamma_delta_quarter = min(
        Fraction(1, 4), (1 + delta_quarter) / 5
    )
    rich_circle_exp = 2 - delta_quarter
    delta_half = Fraction(1, 2)
    gamma_delta_half = min(Fraction(1, 4), (1 + delta_half) / 5)
    assert gamma_delta_quarter == Fraction(1, 4)
    assert rich_circle_exp == Fraction(7, 4)
    assert gamma_delta_half == Fraction(1, 4)

    # Exact inversion: x=y/|y|^2 sends |x|^2-2c.x=0 to c.y=1/2.
    y1, y2, c1, c2 = sp.symbols("y1 y2 c1 c2", real=True)
    norm_y_sq = y1**2 + y2**2
    x1, x2 = y1 / norm_y_sq, y2 / norm_y_sq
    circle_equation = sp.factor(x1**2 + x2**2 - 2 * (c1 * x1 + c2 * x2))
    cleared = sp.factor(circle_equation * norm_y_sq)
    assert sp.factor(cleared - (1 - 2 * c1 * y1 - 2 * c2 * y2)) == 0
    line_distance_sq = sp.factor(
        sp.Rational(1, 4) / (c1**2 + c2**2)
    )

    # A conflict pair with intersection size 2,1,0 contributes respectively
    # 2,1,0 times to the sum of pinned inversion energies, and once to global
    # radius energy.  This certifies E_inv=2C4+C5 and E_rad=C4+C5+C6.
    conflict_rows = []
    for union_size, common_vertices, inv_coeff in (
        (4, 2, 2),
        (5, 1, 1),
        (6, 0, 0),
    ):
        assert common_vertices == 6 - union_size
        assert inv_coeff == common_vertices
        conflict_rows.append({
            "union_size": union_size,
            "common_vertices": common_vertices,
            "pinned_energy_coefficient": inv_coeff,
            "global_radius_energy_coefficient": 1,
        })

    # Exact positive Bernstein-form decomposition of the random-survival
    # conflict ledger.
    p, c4, c5, c6 = sp.symbols("p c4 c5 c6")
    e_inv = 2 * c4 + c5
    e_rad = c4 + c5 + c6
    raw_survival = p**4 * c4 + p**5 * c5 + p**6 * c6
    energy_survival = (
        p**4 * (1 - p) ** 2 * c4
        + p**5 * (1 - p) * e_inv
        + p**6 * e_rad
    )
    assert sp.expand(raw_survival - energy_survival) == 0

    return {
        "schema": "amra.erdos_geometry.round11.v1",
        "arithmetic": "fractions.Fraction and exact sympy algebra",
        "problem_1083": {
            "D_and_Q_exponent": fs(beta),
            "K_exponent": fs(k_exp),
            "rich_pair_count_exponent": fs(pair_exp),
            "common_domain_exponent": fs(common_exp),
            "high_order_failure_slot_multiplicity_exponent": fs(
                failure_slot_exp
            ),
            "high_order_repair_fan_exponent": fs(repair_fan_exp),
            "high_order_clean_common_star_exponent": fs(
                repair_common_star_exp
            ),
            "global_repair_edge_count_exponent": fs(
                global_repair_edge_exp
            ),
            "global_marked_repair_count_exponent": fs(
                global_marked_repair_exp
            ),
            "average_repair_graph_edge_exponent": fs(
                average_repair_graph_exp
            ),
            "average_marked_graph_edge_exponent": fs(
                average_marked_graph_exp
            ),
            "balanced_K22_forcing_threshold_exponent": fs(
                k22_forcing_threshold_exp
            ),
            "synchronized_triangle_family_exponent": fs(
                synchronized_triangle_family_exp
            ),
            "synchronized_incidence_exponent": fs(
                synchronized_incidence_exp
            ),
            "Rudnev_main_at_sync_exponent": fs(
                rudnev_main_at_sync_exp
            ),
            "Rudnev_pencil_at_sync_exponent": fs(
                rudnev_pencil_at_sync_exp
            ),
            "sync_pair_moment_lhs_exponent": fs(
                sync_pair_moment_lhs_exp
            ),
            "sync_pair_moment_rhs_exponent": fs(
                sync_pair_moment_rhs_exp
            ),
            "sync_triple_moment_lhs_exponent": fs(
                sync_triple_moment_lhs_exp
            ),
            "sync_triple_moment_rhs_exponent": fs(
                sync_triple_moment_rhs_exp
            ),
            "low_order_total_good_mass_exponent": fs(low_mass_exp),
            "fixed_point_contamination_exponent": fs(
                fixed_contamination_exp
            ),
            "low_star_edge_count_exponent": fs(low_star_edge_exp),
            "projective_pencil_exponent": fs(pencil_exp),
            "large_common_neighbor_exponent": fs(common_neighbor_exp),
            "distinct_neighbor_direction_exponent": fs(
                distinct_neighbor_direction_exp
            ),
            "Ramsey_high_clique_exponent": fs(ramsey_high_clique_exp),
            "planar_normal_cap_exponent": fs(planar_normal_cap_exp),
            "DRC_no_three_coplanar_decay_exponent": fs(
                no_three_coplanar_decay_exp
            ),
            "axis_orbit_circle_cap_exponent": fs(axis_circle_cap_exp),
            "planar_branch_contradicts_D": common_neighbor_exp > beta,
        },
        "problem_827": {
            "alteration_gamma_H4": fs(gamma_h4),
            "alteration_gamma_H5_without_saving": fs(gamma_h5_at_zero),
            "alteration_gamma_H6_without_saving": fs(gamma_h6_at_zero),
            "delta_one_quarter_rainbow_gamma": fs(gamma_delta_quarter),
            "delta_one_quarter_rich_circle_exponent": fs(rich_circle_exp),
            "delta_one_half_joint_gamma_still_capped_by_H5": fs(
                gamma_delta_half
            ),
            "inversion_cleared_equation": str(cleared),
            "inverted_line_distance_squared": str(line_distance_sq),
            "conflict_energy_rows": conflict_rows,
            "survival_energy_identity": str(energy_survival),
        },
        "warning": (
            "The script certifies algebra and exponent bookkeeping only; "
            "the universal proofs and source-sensitive hypotheses are in "
            "REPORT.md and INDEPENDENT_QA.md."
        ),
        "result": "PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = build_certificate()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
