#!/usr/bin/env python3
"""Exact arithmetic/algebra certificate for round-12 geometry.

This checks the exponent ledger and the elementary polynomial identities used
in REPORT.md.  Ramsey, torsion, incidence and universal quantifiers are audited
in INDEPENDENT_QA.md and are intentionally not inferred from finite tests.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path

import sympy as sp


def fs(x: F) -> str:
    return f"{x.numerator}/{x.denominator}"


def certificate() -> dict:
    beta = F(3, 5)
    K = F(4, 5)
    W = F(3, 5)
    kappa = F(2, 5)

    rat_linear = W - K
    rat_cube = (kappa - K) / 3
    rat_density = max(rat_linear, rat_cube)
    irrational_star = -rat_density
    gp_star = (K - W) / 2

    assert rat_linear == -F(1, 5)
    assert rat_cube == -F(2, 15)
    assert rat_density == -F(2, 15)
    assert irrational_star == F(2, 15)
    assert gp_star == F(1, 10)

    sphere_cap = beta
    rich_motion = 1 + F(4, 3) * sphere_cap
    assert rich_motion == F(9, 5)

    high_positive_L = 14
    high_near_linear_L = 21
    gp_positive_L = 19
    gp_near_linear_L = 28
    assert high_positive_L * irrational_star > rich_motion
    assert (high_positive_L - 1) * irrational_star <= rich_motion
    assert high_near_linear_L * irrational_star - rich_motion == 1
    assert gp_positive_L * gp_star > rich_motion
    assert (gp_positive_L - 1) * gp_star == rich_motion
    assert gp_near_linear_L * gp_star - rich_motion == 1

    full_star_loss_in_t = rich_motion / K
    full_star_L3_representations = 3 * K - rich_motion
    fixed_axis_rich_plane_pencil = 1 - beta
    synchronized_rotation_family = (
        full_star_L3_representations - fixed_axis_rich_plane_pencil
    )
    synchronized_structured_subfamily = full_star_L3_representations / 2
    glide_affine_incidence_power = F(4, 3)
    synchronized_glide_subfamily = (
        full_star_L3_representations / glide_affine_incidence_power
    )
    fixed_point_projective_incidence_power = F(4, 3)
    synchronized_fixed_point_subfamily = (
        full_star_L3_representations / fixed_point_projective_incidence_power
    )
    synchronized_glide_capacity_gap = (
        sphere_cap - synchronized_glide_subfamily
    )
    synchronized_fixed_point_capacity_gap = (
        sphere_cap - synchronized_fixed_point_subfamily
    )
    reflection_balanced_pencil = F(1, 5)
    reflection_balanced_active_axes = (
        full_star_L3_representations - 2 * reflection_balanced_pencil
    )
    fixed_axis_rich_rotation_capacity = beta
    fixed_axis_rotation_gap = (
        fixed_axis_rich_rotation_capacity - synchronized_rotation_family
    )
    assert full_star_loss_in_t == F(9, 4)
    assert full_star_L3_representations == F(3, 5)
    assert fixed_axis_rich_plane_pencil == F(2, 5)
    assert synchronized_rotation_family == F(1, 5)
    assert synchronized_structured_subfamily == F(3, 10)
    assert synchronized_glide_subfamily == F(9, 20)
    assert synchronized_fixed_point_subfamily == F(9, 20)
    assert synchronized_glide_capacity_gap == F(3, 20)
    assert synchronized_fixed_point_capacity_gap == F(3, 20)
    assert reflection_balanced_active_axes == F(1, 5)
    assert fixed_axis_rotation_gap == F(2, 5)
    # L=r+3 gives t^(r+3/4) representations.
    assert 3 - full_star_loss_in_t == F(3, 4)

    # Low-Q endpoint ledger for a in [2/5,1/2].
    low_rows = []
    for a in (F(2, 5), F(9, 20), F(1, 2)):
        M = 2 - beta - a
        low_linear = beta - M
        low_cube = (kappa - M) / 3
        low_rat_density = max(low_linear, low_cube)
        low_independent = -low_rat_density
        low_gp = (M - beta) / 2
        g_min = 2 * a - beta
        guaranteed_edge_mass = low_gp + g_min

        assert M == F(7, 5) - a
        assert low_linear == a - F(4, 5)
        assert low_cube == (a - 1) / 3
        assert low_rat_density == low_cube
        assert low_independent == (1 - a) / 3
        assert low_gp == F(2, 5) - a / 2
        assert guaranteed_edge_mass == -F(1, 5) + 3 * a / 2
        assert guaranteed_edge_mass <= F(11, 20)

        low_rows.append({
            "a": fs(a),
            "M": fs(M),
            "irrational_star": fs(low_independent),
            "general_position_star": fs(low_gp),
            "g_min": fs(g_min),
            "guaranteed_nonfixed_edge_mass": fs(guaranteed_edge_mass),
        })

    pinned_incidence = (F(7, 5) - F(2, 5)) + F(2, 5)
    concurrency_ledger = 1 + sphere_cap
    low_pair_moment_max = F(7, 5) + F(1, 2)
    low_pair_capacity = 2 + sphere_cap
    low_triple_moment_max = F(7, 5) + 2 * F(1, 2)
    low_triple_capacity = 3
    assert pinned_incidence == F(7, 5)
    assert concurrency_ledger == F(8, 5)
    assert concurrency_ledger - pinned_incidence == F(1, 5)
    assert low_pair_moment_max == F(19, 10)
    assert low_pair_capacity == F(13, 5)
    assert low_triple_moment_max == F(12, 5)
    assert low_triple_capacity == 3

    # Fixed-spherical-angle identity used in the rich-motion count.
    a, b, c, dot = sp.symbols("a b c dot", nonzero=True)
    dist_sq = sp.expand(a**2 + b**2 - 2 * a * b * dot)
    solved_dot = sp.solve(sp.Eq(dist_sq, c**2), dot)[0]
    assert sp.factor(solved_dot - (a**2 + b**2 - c**2) / (2 * a * b)) == 0

    # Quaternion/projective-line algebra in the fixed-point branch.
    q0, q1, q2, q3 = sp.symbols("q0 q1 q2 q3")
    skew_q = sp.Matrix([[0, -q3, q2], [q3, 0, -q1], [-q2, q1, 0]])
    quaternion_line_map = q0 * sp.eye(3) + skew_q
    quaternion_line_map_det = sp.factor(quaternion_line_map.det())
    assert quaternion_line_map_det == q0 * (q0**2 + q1**2 + q2**2 + q3**2)
    av = sp.Matrix(sp.symbols("av1 av2 av3"))
    bv = sp.Matrix(sp.symbols("bv1 bv2 bv3"))

    def qmul(x: tuple[sp.Expr, sp.Matrix], y: tuple[sp.Expr, sp.Matrix]):
        x0, xv = x
        y0, yv = y
        return x0 * y0 - xv.dot(yv), x0 * yv + y0 * xv + xv.cross(yv)

    quaternion_real_qab = sp.expand(
        qmul(qmul((q0, sp.Matrix([q1, q2, q3])), (sp.Integer(0), av)),
             (sp.Integer(0), bv))[0]
    )
    expected_real_qab = -q0 * av.dot(bv) - sp.Matrix([q1, q2, q3]).dot(
        av.cross(bv)
    )
    assert sp.expand(quaternion_real_qab - expected_real_qab) == 0

    # Glide quotient: reflection condition equals planar point-line incidence.
    alpha, beta_angle, da, db, lam = sp.symbols(
        "alpha beta_angle da db lam", nonzero=True
    )
    glide_condition = (
        2 * db * sp.sin(alpha)
        - 2 * da * sp.sin(beta_angle)
        + lam * sp.cos(alpha - beta_angle)
    )
    glide_x = da / sp.sin(alpha) - lam / 2
    glide_y = -(lam / 2) * sp.cos(alpha) / sp.sin(alpha)
    glide_incidence = (
        sp.sin(beta_angle) * glide_x
        + sp.cos(beta_angle) * glide_y
        - db
    )
    assert sp.trigsimp(glide_condition + 2 * sp.sin(alpha) * glide_incidence) == 0

    # #827 phase-diagram exponents.
    phase_rows = []
    for eta in (F(1, 100), F(1, 16), F(1, 12)):
        target = F(1, 4) + eta
        h4 = 4 * eta
        einv = 5 * (-F(3, 4) + eta) + (4 - 4 * eta)
        erad = 6 * (-F(3, 4) + eta) + (F(19, 4) - 5 * eta)
        bad_centers = 1 - 4 * eta
        overlap = 1 - 8 * eta
        assert h4 <= target
        assert einv == target
        assert erad == target
        assert overlap > 0
        multi_center_overlap = {}
        for j in range(2, 4):
            moment = j * (2 - 8 * eta) - (j - 1)
            center_tuple_count = j * (1 - 4 * eta)
            common = moment - center_tuple_count
            assert common == 1 - 4 * j * eta
            assert common >= 0
            multi_center_overlap[str(j)] = fs(common)
        phase_rows.append({
            "eta": fs(eta),
            "target_rainbow": fs(target),
            "H4_survival": fs(h4),
            "H5_energy_survival": fs(einv),
            "H6_energy_survival": fs(erad),
            "bad_center_count": fs(bad_centers),
            "two_center_overlap": fs(overlap),
            "j_center_common_endpoint_exponents": multi_center_overlap,
        })

    return {
        "schema": "amra.erdos_geometry.round12.v1",
        "arithmetic": "exact fractions.Fraction and sympy",
        "problem_1083": {
            "rational_angle_density_exponent": fs(rat_density),
            "pairwise_irrational_star_exponent": fs(irrational_star),
            "three_source_general_position_star_exponent": fs(gp_star),
            "sphere_and_plane_cap_exponent": fs(sphere_cap),
            "rich_rigid_motion_exponent": fs(rich_motion),
            "high_star_first_positive_word_length": high_positive_L,
            "high_star_near_linear_word_length": high_near_linear_L,
            "general_position_first_positive_word_length": gp_positive_L,
            "general_position_near_linear_word_length": gp_near_linear_L,
            "full_star_rich_motion_loss_in_t": fs(full_star_loss_in_t),
            "full_star_L3_same_motion_representation_exponent": fs(
                full_star_L3_representations
            ),
            "fixed_axis_Q_rich_plane_pencil_exponent": fs(
                fixed_axis_rich_plane_pencil
            ),
            "synchronized_infinite_order_rotation_family_exponent": fs(
                synchronized_rotation_family
            ),
            "crude_structured_plane_family_exponent": fs(
                synchronized_structured_subfamily
            ),
            "glide_affine_incidence_power": fs(glide_affine_incidence_power),
            "glide_structured_plane_family_exponent": fs(
                synchronized_glide_subfamily
            ),
            "fixed_point_projective_incidence_power": fs(
                fixed_point_projective_incidence_power
            ),
            "fixed_point_structured_plane_family_exponent": fs(
                synchronized_fixed_point_subfamily
            ),
            "glide_family_to_current_capacity_gap": fs(
                synchronized_glide_capacity_gap
            ),
            "fixed_point_family_to_current_capacity_gap": fs(
                synchronized_fixed_point_capacity_gap
            ),
            "reflection_branch_balanced_pencil_or_axes_exponents": {
                "pencil": fs(reflection_balanced_pencil),
                "active_axes": fs(reflection_balanced_active_axes),
            },
            "fixed_axis_rich_rotation_capacity_exponent": fs(
                fixed_axis_rich_rotation_capacity
            ),
            "fixed_axis_rotation_capacity_gap": fs(fixed_axis_rotation_gap),
            "full_star_fixed_r_representation_bonus_in_t": fs(
                3 - full_star_loss_in_t
            ),
            "low_Q_rows": low_rows,
            "pinned_incidence_exponent": fs(pinned_incidence),
            "concurrency_incidence_ceiling_exponent": fs(concurrency_ledger),
            "remaining_concurrency_gap": fs(concurrency_ledger - pinned_incidence),
            "low_Q_pair_moment_max": fs(low_pair_moment_max),
            "low_Q_pair_capacity": fs(low_pair_capacity),
            "low_Q_triple_moment_max": fs(low_triple_moment_max),
            "low_Q_triple_capacity": fs(low_triple_capacity),
            "fixed_angle_dot_product": str(solved_dot),
            "fixed_point_quaternion_line_map_determinant": str(
                quaternion_line_map_det
            ),
            "fixed_point_quaternion_real_qab_identity": "PASS",
            "glide_condition_to_point_line_identity": "PASS",
        },
        "problem_827": {"phase_rows": phase_rows},
        "warning": (
            "Finite algebra/exponent certificate only. It does not certify "
            "external theorem hypotheses, asymptotic universal proofs, novelty, "
            "publication priority, or either original problem."
        ),
        "result": "PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = certificate()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
