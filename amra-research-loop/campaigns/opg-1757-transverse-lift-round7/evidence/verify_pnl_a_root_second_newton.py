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
EXPECTED = {
    "below": {
        "centered_sha256": "bb27cc415caba57130abd5ff540d6e3e06c34c15dee30b16c04619ad9205a9ac",
        "centered_negative": 105870,
        "closed_charts": {
            "zeta": {
                "slot": 2,
                "radial_sha256": "76a2e2ff1c8cbfe2ac679aaf413752d25513d4b3d70f05228e04e5ee0b7d5f37",
                "controls_nonzero": 4114824,
                "controls_minimum": Fraction(729, 2444464),
                "controls_maximum": Fraction(1843968),
                "controls_sha256": "0ce856b96face2e42a3f430b431caee76f0c14d6bdb772191d54dc4dd3d4ddfe",
            },
            "r": {
                "slot": 0,
                "radial_sha256": "777c2b286f925581d5b8ef37b827d9de5005659ae098f69d102cf684fe339fab",
                "controls_nonzero": 943110,
                "controls_minimum": Fraction(13122, 4790071),
                "controls_maximum": Fraction(1382976),
                "controls_sha256": "0850b4040dd3320c04c76b350859d94d4bf0a3d5400991507b78cafee0525fd9",
            },
            "Hbar": {
                "slot": 4,
                "radial_sha256": "6392d4c90fae4b7fc5a4a722c6ab03b329a420afc2c0a9a336c5d5c97ab30f7b",
                "controls_nonzero": 2857800,
                "controls_minimum": Fraction(81, 152779),
                "controls_maximum": Fraction(1843968),
                "controls_sha256": "1b446d96360c21e68a43cf1a4b6832d6d44cf23949d266317f8f20ac1b427169",
            },
        },
    },
    "above": {
        "centered_sha256": "99cfbf5160488a95d875497fe9148aae2f85dae2438fb4cd9e7f19ee029d0ed5",
        "centered_negative": 105400,
        "closed_charts": {
            "zeta": {
                "slot": 2,
                "radial_sha256": "9d64f3409f817dbbe4460cadabc63dc1a9f6d69eeb683f5c9914feacc07c73d7",
                "controls_nonzero": 4154514,
                "controls_minimum": Fraction(2662, 12341),
                "controls_maximum": Fraction(5467500),
                "controls_sha256": "5fd44a4695d86b6d71ddca050087a153e6d58dc4ee418d69cfacbd9c4415bb38",
            },
            "r": {
                "slot": 0,
                "radial_sha256": "b424ffe5d5ee3528a6634d4ff2c5a7cbcc6226f3c2344c1051223ad4261e129e",
                "controls_nonzero": 952560,
                "controls_minimum": Fraction(1782, 12341),
                "controls_maximum": Fraction(4100625),
                "controls_sha256": "48e0c9d4819a446da1246f0e8482409d32ba0493f89c8695fd048c8a96533aa9",
            },
            "Hbar": {
                "slot": 4,
                "radial_sha256": "c80602ac4e99f71763c0574e2c354af4f4aea24eaf27391c45d7e7ebd24b1e29",
                "controls_nonzero": 2885610,
                "controls_minimum": Fraction(616, 1763),
                "controls_maximum": Fraction(5467500),
                "controls_sha256": "12d42b142c5c793bea0eecfcd86dac4a1781edc04880db8d85848e5bc20d2f50",
            },
            "B": {
                "slot": 5,
                "radial_sha256": "c8e4c43683aa1bd6719ea01a24aabfceed67000f7394f9e422246e50abdd4337",
                "controls_nonzero": 3363080,
                "controls_minimum": Fraction(6561, 44935),
                "controls_maximum": Fraction(5467500),
                "controls_sha256": "10f4ea92306c02bbb3b6b9af0ddaf75f3ca1708caf5c2870131559244dcf84bc",
            },
            "d": {
                "slot": 7,
                "radial_sha256": "146044d1d81fd8ae0b388f71f0e10906c2175d090d76948b020205e5d02f9457",
                "controls_nonzero": 2877600,
                "controls_minimum": Fraction(6561, 44935),
                "controls_maximum": Fraction(5467500),
                "controls_sha256": "8d0f3f1b1eadcbfcac24456e937b51c31ca84afeadc0bda3772eb80839794654",
            },
        },
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

        chart_records = {}
        for name, chart_expected in expected["closed_charts"].items():
            maximum_slot = chart_expected["slot"]
            radial = radial_projective_chart(
                centered, SECOND_NEWTON_SLOTS, maximum_slot, order
            )
            radial_row = row(radial)
            radial_degrees = list(centered_row["degrees"])
            radial_degrees[maximum_slot] = 44
            assert radial_row == {
                "terms": 212156,
                "degrees": radial_degrees,
                "negative_power_coefficients": expected["centered_negative"],
                "sha256": chart_expected["radial_sha256"],
            }
            control_slots = (
                maximum_slot,
                *(slot for slot in SECOND_NEWTON_SLOTS if slot != maximum_slot),
            )
            controls = bernstein_transform(radial, list(control_slots))
            controls_minimum = min(controls.values())
            controls_maximum = max(controls.values())
            controls_digest = digest(controls)
            assert len(controls) == chart_expected["controls_nonzero"]
            assert all(value > 0 for value in controls.values())
            assert controls_minimum == chart_expected["controls_minimum"]
            assert controls_maximum == chart_expected["controls_maximum"]
            assert controls_digest == chart_expected["controls_sha256"]
            total_controls = 1
            for slot in control_slots:
                total_controls *= radial_degrees[slot] + 1
            chart_records[name] = {
                "radial_polynomial": radial_row,
                "control_slots": list(control_slots),
                "bernstein_total": total_controls,
                "bernstein_nonzero": len(controls),
                "bernstein_zero": total_controls - len(controls),
                "bernstein_minimum_nonzero": str(controls_minimum),
                "bernstein_maximum": str(controls_maximum),
                "bernstein_sha256": controls_digest,
            }
            del controls, radial
            gc.collect()
        side_records[side] = {
            "s_ratio_interval": "[0,2/3]" if side == "below" else "[2/3,1]",
            "centered_polynomial": centered_row,
            "second_newton_order": order,
            "second_newton_face": {
                **row(face),
                "identity": "352836*zeta^2",
            },
            "closed_maximum_charts": chart_records,
        }
        del centered
        gc.collect()

    return {
        "schema": "amra.opg1757.round7.pnl-a-root-second-newton.v2",
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
        "conclusion": "the below-side zeta-, r-, and Hbar-maximal charts and the above-side zeta-, r-, Hbar-, B-, and d-maximal charts are exactly Bernstein-nonnegative, with every stored nonzero control strictly positive",
        "coverage_change": 0,
        "scope": "the below-side A-, B-, C-, and d-maximal charts, the above-side A- and C-maximal charts, the rest of the first a-max chart, the other first-level negative-root directions, the positive-root branch, q3:PNL, and OPG-1757 are not claimed",
    }


def main():
    print(json.dumps(build_record(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
