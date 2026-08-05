#!/usr/bin/env python3
"""Exact second-Newton certificates at the PNL negative-root a-chart."""

from __future__ import annotations

from fractions import Fraction
import gc
import json

from verify_negative_c_direct_chambers import (
    add,
    bernstein_transform,
    constant,
    multiply,
    variable,
)
from verify_negative_nonshared_double_negative_gram import cleared_polynomial
from verify_negative_page_direct_chambers import digest
from verify_negative_q0_no_positive_gram import (
    build_delta,
    common_monomial,
    divide_monomial,
    scale,
)
from verify_opposite_nonshared_chambers import divide_one_minus_variable
from verify_pnl_double_corner_blowup import (
    activity_blowup,
    compactify_scale,
    projective_chart,
    radial_projective_chart,
    row,
    substitute_slot,
)
from verify_rlp_projective_corner_reduction import (
    polynomial_sum,
    reverse_slot,
)


H_DEVIATION_SLOTS = (0, 1, 4, 5, 6, 7)
SECOND_NEWTON_SLOTS = (0, 2, 1, 4, 5, 6, 7)
SECOND_CONTROL_SLOTS = (2, 0, 1, 4, 5, 6, 7)
EXPECTED = {
    "below": {
        "centered_sha256": "bb27cc415caba57130abd5ff540d6e3e06c34c15dee30b16c04619ad9205a9ac",
        "centered_negative": 105870,
        "radial_sha256": "76a2e2ff1c8cbfe2ac679aaf413752d25513d4b3d70f05228e04e5ee0b7d5f37",
        "controls_nonzero": 4114824,
        "controls_minimum": Fraction(729, 2444464),
        "controls_maximum": Fraction(1843968),
        "controls_sha256": "0ce856b96face2e42a3f430b431caee76f0c14d6bdb772191d54dc4dd3d4ddfe",
    },
    "above": {
        "centered_sha256": "99cfbf5160488a95d875497fe9148aae2f85dae2438fb4cd9e7f19ee029d0ed5",
        "centered_negative": 105400,
        "radial_sha256": "9d64f3409f817dbbe4460cadabc63dc1a9f6d69eeb683f5c9914feacc07c73d7",
        "controls_nonzero": 4154514,
        "controls_minimum": Fraction(2662, 12341),
        "controls_maximum": Fraction(5467500),
        "controls_sha256": "5fd44a4695d86b6d71ddca050087a153e6d58dc4ee418d69cfacbd9c4415bb38",
    },
}


def negative_root_polynomial():
    delta, forest_count, connected_count = build_delta()
    cleared = cleared_polynomial(delta, "PNL", 1)
    core = divide_monomial(cleared, common_monomial(cleared))
    quotient = divide_one_minus_variable(core, 6)
    local = quotient
    for slot in (2, 4, 6, 7):
        local = reverse_slot(local, slot)
    h_chart = activity_blowup(local, "h")
    boundary = compactify_scale(projective_chart(h_chart, 0))
    for slot in H_DEVIATION_SLOTS:
        boundary = reverse_slot(boundary, slot)

    a, root_ratio, H, s = (variable(slot) for slot in (0, 2, 4, 7))
    L = polynomial_sum(H, scale(a, 3))
    denominator = add(L, s)
    numerator = multiply(s, add(constant(1), root_ratio, -1))
    result, degree = substitute_slot(boundary, 2, numerator, denominator)
    assert degree == 4
    assert len(result) == 59892
    assert digest(result) == (
        "c8eb9954de0d5402b7942e9cc9bfdcb6e3942efddcc67674ae8d92866737d896"
    )
    return result, forest_count, connected_count


def centered_a_chart(a_radial, side):
    centered = a_radial
    for slot in (1, 5, 6):
        centered = reverse_slot(centered, slot)
    d = variable(7)
    if side == "below":
        numerator = scale(add(constant(1), d, -1), 2)
    else:
        numerator = add(constant(2), d)
    centered, degree = substitute_slot(centered, 7, numerator, constant(3))
    assert degree == 6
    return centered


def second_newton_face(poly):
    order = min(sum(m[slot] for slot in SECOND_NEWTON_SLOTS) for m in poly)
    face = {
        monomial: value
        for monomial, value in poly.items()
        if sum(monomial[slot] for slot in SECOND_NEWTON_SLOTS) == order
    }
    return order, face


def build_record():
    negative_root, forest_count, connected_count = negative_root_polynomial()
    a_radial = radial_projective_chart(
        negative_root, H_DEVIATION_SLOTS, 0, 7
    )
    assert row(a_radial) == {
        "terms": 59892,
        "degrees": [20, 4, 4, 0, 6, 5, 2, 6],
        "negative_power_coefficients": 29914,
        "sha256": "e33459bb90c297dac3f44fd334293345f96a776d708d77f937be315383490876",
    }

    side_records = {}
    expected_face = {(0, 0, 2, 0, 0, 0, 0, 0): Fraction(352836)}
    for side in ("below", "above"):
        centered = centered_a_chart(a_radial, side)
        expected = EXPECTED[side]
        centered_row = row(centered)
        assert centered_row == {
            "terms": 212156,
            "degrees": [20, 4, 4, 0, 6, 5, 2, 6],
            "negative_power_coefficients": expected["centered_negative"],
            "sha256": expected["centered_sha256"],
        }
        order, face = second_newton_face(centered)
        assert order == 2
        assert face == expected_face

        z_radial = radial_projective_chart(
            centered, SECOND_NEWTON_SLOTS, 2, order
        )
        z_radial_row = row(z_radial)
        assert z_radial_row == {
            "terms": 212156,
            "degrees": [20, 4, 44, 0, 6, 5, 2, 6],
            "negative_power_coefficients": expected["centered_negative"],
            "sha256": expected["radial_sha256"],
        }
        controls = bernstein_transform(z_radial, list(SECOND_CONTROL_SLOTS))
        assert len(controls) == expected["controls_nonzero"]
        assert all(value > 0 for value in controls.values())
        assert min(controls.values()) == expected["controls_minimum"]
        assert max(controls.values()) == expected["controls_maximum"]
        assert digest(controls) == expected["controls_sha256"]
        total_controls = 45 * 21 * 5 * 7 * 6 * 3 * 7
        side_records[side] = {
            "s_ratio_interval": "[0,2/3]" if side == "below" else "[2/3,1]",
            "centered_polynomial": centered_row,
            "second_newton_order": order,
            "second_newton_face": {
                **row(face),
                "identity": "352836*zeta^2",
            },
            "zeta_max_radial_polynomial": z_radial_row,
            "control_slots": list(SECOND_CONTROL_SLOTS),
            "bernstein_total": total_controls,
            "bernstein_nonzero": len(controls),
            "bernstein_zero": total_controls - len(controls),
            "bernstein_minimum_nonzero": str(min(controls.values())),
            "bernstein_maximum": str(max(controls.values())),
            "bernstein_sha256": digest(controls),
        }
        del controls, z_radial, centered
        gc.collect()

    return {
        "schema": "amra.opg1757.round7.pnl-a-root-second-newton.v1",
        "domain": "the negative moving-root branch inside the h-dominant c-maximal PNL chart",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "negative_root_polynomial": row(negative_root),
        },
        "a_max_radial_chart": {
            "coordinates": "a=r; the other five h-boundary deviations are r times ratios in [0,1]",
            "polynomial": row(a_radial),
            "accumulation": "r=zeta=H/a=0, (delta1/a,delta2/a,e/a)=(1,1,1), s/a=2/3",
        },
        "second_newton_coordinates": "A=1-delta1/a, B=1-delta2/a, E=1-e/a; split S=s/a at 2/3 and blow up (r,zeta,A,H/a,B,E,|S-2/3|)^2",
        "sides": side_records,
        "conclusion": "both zeta-maximal charts of the second Newton fan are exactly Bernstein-nonnegative, with every stored nonzero control strictly positive",
        "coverage_change": 0,
        "scope": "the other six maximum-direction charts of each second Newton fan, the rest of the first a-max chart, the other first-level negative-root directions, the positive-root branch, q3:PNL, and OPG-1757 are not claimed",
    }


def main():
    print(json.dumps(build_record(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
