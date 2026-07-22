#!/usr/bin/env python3
"""Exact rational-exponent audit for the round-9 #1083 bridge/no-go.

The script certifies algebra on exponent inequalities only.  It neither
proves the geometric lemmas nor extrapolates from numerical point sets.
"""

from __future__ import annotations

from fractions import Fraction
import json


def render(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def row(beta: Fraction, a: Fraction) -> dict[str, str]:
    # D=n^beta, Q=n^a, ignoring polylogarithmic factors.
    plane_count = 2 - beta - a
    generator_threshold = 2 * a - beta
    incidence_mass = plane_count + a
    rudnev_main = 1 + plane_count / 2
    # kappa<2n/Q on the no-rich-line carrying layer, so kappa*n<=n^(2-a).
    projective_pencil_term = 2 - a
    average_domain_overlap = 2 * a - 1
    assert incidence_mass == 2 - beta
    assert incidence_mass <= rudnev_main  # equivalent to a <= beta
    assert incidence_mass <= projective_pencil_term
    return {
        "a": render(a),
        "K_exponent": render(plane_count),
        "g_threshold_exponent": render(generator_threshold),
        "KQ_incidence_exponent": render(incidence_mass),
        "Rudnev_n_sqrt_K_exponent": render(rudnev_main),
        "Rudnev_projective_pencil_term_upper_exponent": render(
            projective_pencil_term
        ),
        "average_pair_domain_overlap_exponent": render(
            average_domain_overlap
        ),
    }


def main() -> None:
    beta = Fraction(3, 5)
    scales = [Fraction(2, 5), Fraction(1, 2), Fraction(3, 5)]
    rows = [row(beta, a) for a in scales]
    assert 3 * beta - 2 == Fraction(-1, 5)
    assert 1 - beta == Fraction(2, 5)
    assert rows[-1]["KQ_incidence_exponent"] == rows[-1][
        "Rudnev_n_sqrt_K_exponent"
    ]
    assert all(a <= beta for a in scales)

    high_q_scales = [Fraction(1, 2), Fraction(11, 20), Fraction(3, 5)]
    high_q_rows = []
    for a in high_q_scales:
        forced_domain = 1 + a - beta
        composition_domain = 2 * forced_domain - 1
        rotation_shell = composition_domain - beta
        assert forced_domain <= 1
        assert composition_domain == 1 + 2 * a - 2 * beta
        high_q_rows.append({
            "a": render(a),
            "incidence_forced_reflection_domain_exponent": render(
                forced_domain
            ),
            "cauchy_composition_domain_exponent": render(
                composition_domain
            ),
            "rotation_cylinder_shell_exponent": render(rotation_shell),
            "automatic_high_q_condition": a > Fraction(1, 2),
        })
    assert high_q_rows[-1][
        "incidence_forced_reflection_domain_exponent"
    ] == "1/1"
    assert high_q_rows[-1][
        "cauchy_composition_domain_exponent"
    ] == "1/1"
    assert high_q_rows[-1][
        "rotation_cylinder_shell_exponent"
    ] == "2/5"

    print(json.dumps({
        "schema": "amra.erdos1083.round9.exponent_barrier.v1",
        "arithmetic": "fractions.Fraction; exact rational exponents",
        "critical_distance_exponent_beta": render(beta),
        "small_defect_mass_ratio_exponent_3beta_minus_2": render(
            3 * beta - 2
        ),
        "minimum_axis_pencil_count_exponent_1_minus_beta": render(
            1 - beta
        ),
        "rows": rows,
        "high_q_weighted_bridge_rows": high_q_rows,
        "identities_checked": [
            "KQ exponent = 2-beta at every carrying scale",
            "KQ <= n sqrt(K) is automatic exactly when a<=beta",
            "the corrected projective-pencil term kappa*n is at most exponent 2-a",
            "KQ reaches the projective-pencil upper exponent exactly at a=beta",
            "Rudnev main term is exactly saturated at a=beta",
            "small-defect mass / total mass has exponent 3beta-2=-1/5",
            "at a=beta=3/5 the weighted bridge forces reflection and composition domains of exponent 1",
            "a rotational composition then has a cylinder/axis shell of exponent 1-beta=2/5",
        ],
        "warning": "Exponent audit only; logarithms and constants are retained in REPORT.md.",
        "result": "PASS",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
