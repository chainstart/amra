#!/usr/bin/env python3
"""Exact third-Newton certificates inside the open PNL above/A boundary."""

from __future__ import annotations

from fractions import Fraction
import gc
import json

from verify_negative_c_direct_chambers import (
    add,
    bernstein_transform,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_page_direct_chambers import digest
from verify_negative_q0_no_positive_gram import scale
from verify_pnl_a_root_second_newton import (
    H_DEVIATION_SLOTS,
    SECOND_NEWTON_SLOTS,
    centered_a_chart,
    negative_root_polynomial,
    second_newton_face,
)
from verify_pnl_double_corner_blowup import (
    radial_projective_chart,
    row,
    substitute_slot,
)
from verify_rlp_projective_corner_reduction import (
    polynomial_sum,
    product,
    reverse_slot,
    square,
)


TRANSVERSE_SLOTS = (0, 4, 6, 7)
ROOT_SLOTS = (0, 6)
ACTIVE_SLOTS = (0, 2, 4, 5, 6, 7)
EXPECTED_CONTROLS = {
    ("below", "R"): {
        "slot": 0,
        "radial_sha256": "6df9efb4a3492cc18d9f9e2a672186f918a747666ff5f4e2e34191ab6cf6e0a4",
        "nonzero": 328419,
        "minimum": Fraction(48229972252, 225),
        "maximum": Fraction(26696634898972500),
        "sha256": "da59a931a468698dff2265f1a785524fe4ab86e05beead9b5f9ea4f1f3f63962",
    },
    ("above", "R"): {
        "slot": 0,
        "radial_sha256": "60a24b49f5e7f559ef86f16f3b3164c1e7e3ee0cc8664affc714e01536cb4f22",
        "nonzero": 328517,
        "minimum": Fraction(48229972252, 225),
        "maximum": Fraction(26696634898972500),
        "sha256": "97f465a71f712dba3b7bd99e13558765ff974a24c84db44d5faf27ffadf44ec5",
    },
    ("above", "v"): {
        "slot": 6,
        "radial_sha256": "05efe7d2f12cbf311ba2a6953094c994588e5c59d6cd2a7f0cf08cfe6f5c69fc",
        "nonzero": 3214610,
        "minimum": Fraction(1722499009, 225),
        "maximum": Fraction(26696634898972500),
        "sha256": "a086c26d760c093bff23755a786b1d12df660227177d75ff2addbfddd077286c",
    },
}
EXPECTED_K_NONPOSITIVE = {
    "high_B": {
        "polynomial": {
            "terms": 44630,
            "degrees": [28, 0, 4, 0, 6, 5, 2, 6],
            "negative_power_coefficients": 22016,
            "sha256": "87733107ec673b7875a21ffa88dd46e5d313eb390be82c253ef0caac2a9653c2",
        },
        "nonzero": 125629,
        "minimum": Fraction(279936, 7),
        "maximum": Fraction(91892272500),
        "sha256": "c10c4f9d392e4b3b17b7d35c35e84b33ca2138ef751269dc8e8dccb48409c148",
    },
    "low_B_high_zeta": {
        "polynomial": {
            "terms": 57455,
            "degrees": [28, 0, 4, 0, 6, 9, 2, 6],
            "negative_power_coefficients": 28172,
            "sha256": "f58635dfd33dd775b0cdc8aebfff7a3f5a7265ae976c1889f775ea0b26cf1f07",
        },
        "nonzero": 208747,
        "minimum": Fraction(246071287, 18),
        "maximum": Fraction(1345394761672500),
        "sha256": "5685efd042850a7c7e891f45ca8687b0a7ac4b5be0a508e5a55c0653c6e82f4f",
    },
}


def specialize(poly, slot, value):
    value = Fraction(value)
    result = {}
    for monomial, coefficient in poly.items():
        reduced = list(monomial)
        exponent = reduced[slot]
        reduced[slot] = 0
        key = tuple(reduced)
        result[key] = result.get(key, Fraction()) + coefficient * value**exponent
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def transverse_data():
    negative_root, forest_count, connected_count = negative_root_polynomial()
    a_radial = radial_projective_chart(
        negative_root, H_DEVIATION_SLOTS, 0, 7
    )
    centered = centered_a_chart(a_radial, "above")
    second_order, _ = second_newton_face(centered)
    assert second_order == 2
    second_A = radial_projective_chart(
        centered, SECOND_NEWTON_SLOTS, 1, second_order
    )
    assert row(second_A) == {
        "terms": 212156,
        "degrees": [20, 44, 4, 0, 6, 5, 2, 6],
        "negative_power_coefficients": 105400,
        "sha256": "12f569bee239feb9eae8bc376ffe3f034f29e690e69f2fac3cd51a719374752f",
    }
    boundary = specialize(second_A, 1, 1)
    assert row(boundary) == {
        "terms": 34738,
        "degrees": [16, 0, 4, 0, 6, 5, 2, 6],
        "negative_power_coefficients": 17174,
        "sha256": "1a281747d0472ad41551d4004f3f73cbfc12ceec3b74fb69e0362b2c31cc6ace",
    }
    zero_face = boundary
    for slot, value in ((0, 1), (4, 0), (6, 1), (7, 0)):
        zero_face = specialize(zero_face, slot, value)
    assert not zero_face

    local = reverse_slot(boundary, 0)
    local = reverse_slot(local, 6)
    assert row(local) == {
        "terms": 43109,
        "degrees": [16, 0, 4, 0, 6, 5, 2, 6],
        "negative_power_coefficients": 21256,
        "sha256": "c53b8d5addcec77b99338fca665162a4a3c116af1f9989ae184cd61e37fd194d",
    }
    transverse_order = min(
        sum(monomial[slot] for slot in TRANSVERSE_SLOTS)
        for monomial in local
    )
    assert transverse_order == 2
    transverse_face = {
        monomial: coefficient
        for monomial, coefficient in local.items()
        if sum(monomial[slot] for slot in TRANSVERSE_SLOTS) == transverse_order
    }
    R, zeta, B, C = (variable(slot) for slot in (0, 2, 5, 6))
    moving_root = polynomial_sum(
        scale(product(B, R, zeta), 4),
        scale(multiply(B, R), 7),
        scale(C, 11),
        multiply(R, zeta),
        scale(R, -1),
    )
    expected_face = product(
        constant(4),
        B,
        square(polynomial_sum(scale(B, 2), constant(1))),
        square(polynomial_sum(scale(zeta, 2), constant(9))),
        square(moving_root),
    )
    assert transverse_face == expected_face
    assert row(transverse_face) == {
        "terms": 50,
        "degrees": [2, 0, 4, 0, 0, 5, 2, 0],
        "negative_power_coefficients": 5,
        "sha256": "dbe8f2b735fa56e3f10ef79a12955aeaeea471b4dadf5592ac0b6914b0f0ff55",
    }
    R_radial = radial_projective_chart(
        local, TRANSVERSE_SLOTS, 0, transverse_order
    )
    assert row(R_radial) == {
        "terms": 43109,
        "degrees": [28, 0, 4, 0, 6, 5, 2, 6],
        "negative_power_coefficients": 21256,
        "sha256": "8e1e366bc878c79bde044b0acf955f3d0277260c11704ca882b293a413ea5f15",
    }
    return {
        "negative_root": negative_root,
        "a_radial": a_radial,
        "second_A": second_A,
        "boundary": boundary,
        "local": local,
        "transverse_face": transverse_face,
        "R_radial": R_radial,
        "forest_count": forest_count,
        "connected_count": connected_count,
    }


def parameterized(R_radial, side):
    b, y, u = (variable(slot) for slot in (5, 2, 6))
    one = constant(1)
    one_minus_b = add(one, b, -1)
    one_minus_y = add(one, y, -1)
    poly, B_degree = substitute_slot(R_radial, 5, b, constant(7))
    assert B_degree == 5
    poly, zeta_degree = substitute_slot(
        poly,
        2,
        scale(multiply(one_minus_b, y), 7),
        polynomial_sum(constant(7), scale(b, 4)),
    )
    assert zeta_degree == 4
    K = multiply(one_minus_b, one_minus_y)
    numerator = (
        multiply(K, u)
        if side == "below"
        else polynomial_sum(K, multiply(add(constant(11), K, -1), u))
    )
    poly, C_degree = substitute_slot(poly, 6, numerator, constant(11))
    assert C_degree == 2
    return reverse_slot(poly, 6) if side == "below" else poly


def expected_root_face():
    R, y, b = (variable(slot) for slot in (0, 2, 5))
    one_minus_b = add(constant(1), b, -1)
    one_minus_y = add(constant(1), y, -1)
    first_square = polynomial_sum(
        scale(product(b, y), 7), scale(b, 4), scale(y, -7), constant(7)
    )
    second_square = polynomial_sum(
        scale(product(b, y), 14), scale(b, -36), scale(y, -14), constant(-63)
    )
    return product(
        constant(28),
        R,
        square(one_minus_b),
        square(polynomial_sum(scale(b, 2), constant(7))),
        polynomial_sum(scale(b, 4), constant(7)),
        polynomial_sum(scale(b, 4), constant(21)),
        square(one_minus_y),
        square(first_square),
        square(second_square),
    )


def expected_fourth_face():
    q, y, b, v = (variable(slot) for slot in (0, 2, 5, 6))
    one_minus_b = add(constant(1), b, -1)
    one_minus_y = add(constant(1), y, -1)
    first_square = polynomial_sum(
        scale(product(b, y), 7), scale(b, 4), scale(y, -7), constant(7)
    )
    second_square = polynomial_sum(
        scale(product(b, y), 14), scale(b, -36), scale(y, -14), constant(-63)
    )
    bracket = polynomial_sum(
        product(
            q,
            polynomial_sum(scale(b, 4), constant(21)),
            square(first_square),
        ),
        scale(
            product(b, polynomial_sum(scale(b, 4), constant(7)), v),
            847,
        ),
    )
    return product(
        constant(28),
        square(one_minus_b),
        square(polynomial_sum(scale(b, 2), constant(7))),
        polynomial_sum(scale(b, 4), constant(7)),
        square(one_minus_y),
        square(second_square),
        bracket,
    )


def K_nonpositive_parameterized(R_radial, patch):
    b, y = (variable(slot) for slot in (5, 2))
    if patch == "high_B":
        poly, degree = substitute_slot(
            R_radial,
            5,
            polynomial_sum(constant(1), scale(b, 6)),
            constant(7),
        )
        assert degree == 5
        return poly
    poly, degree = substitute_slot(R_radial, 5, b, constant(7))
    assert degree == 5
    numerator = polynomial_sum(
        scale(add(constant(1), b, -1), 7),
        scale(multiply(b, y), 11),
    )
    denominator = polynomial_sum(constant(7), scale(b, 4))
    poly, degree = substitute_slot(poly, 2, numerator, denominator)
    assert degree == 4
    return poly


def build_record():
    data = transverse_data()
    root_face_expected = expected_root_face()
    fourth_face_expected = expected_fourth_face()
    sides = {}
    below_fourth_record = None
    for side in ("below", "above"):
        poly = parameterized(data["R_radial"], side)
        expected_poly = {
            "below": {
                "terms": 145406,
                "degrees": [28, 0, 6, 0, 6, 10, 2, 6],
                "negative_power_coefficients": 72505,
                "sha256": "2be1763b2daf5c675b967e00bf8d2a8dca41e73fe79bc2ebaf3243f667e7059e",
            },
            "above": {
                "terms": 145423,
                "degrees": [28, 0, 6, 0, 6, 10, 2, 6],
                "negative_power_coefficients": 72235,
                "sha256": "b860e6b723a578760edaa7b4e3db58ac43941c21fe869bf3a00ff2429b169814",
            },
        }[side]
        assert row(poly) == expected_poly
        root_order = min(
            sum(monomial[slot] for slot in ROOT_SLOTS) for monomial in poly
        )
        assert root_order == 1
        root_face = {
            monomial: coefficient
            for monomial, coefficient in poly.items()
            if sum(monomial[slot] for slot in ROOT_SLOTS) == root_order
        }
        assert root_face == root_face_expected
        assert row(root_face) == {
            "terms": 77,
            "degrees": [1, 0, 6, 0, 0, 10, 0, 0],
            "negative_power_coefficients": 36,
            "sha256": "a4c9992531033f45e8ccde0e6af6c008a86e9d750a668e081c5747725367af1c",
        }

        closed = {}
        chart_names = ("R",) if side == "below" else ("R", "v")
        for name in chart_names:
            expected = EXPECTED_CONTROLS[(side, name)]
            maximum_slot = expected["slot"]
            radial = radial_projective_chart(
                poly, ROOT_SLOTS, maximum_slot, root_order
            )
            radial_row = row(radial)
            assert radial_row["sha256"] == expected["radial_sha256"]
            control_slots = (
                maximum_slot,
                *(slot for slot in ACTIVE_SLOTS if slot != maximum_slot),
            )
            controls = bernstein_transform(radial, list(control_slots))
            controls_minimum = min(controls.values())
            controls_maximum = max(controls.values())
            controls_digest = digest(controls)
            assert len(controls) == expected["nonzero"]
            assert all(value > 0 for value in controls.values())
            assert controls_minimum == expected["minimum"]
            assert controls_maximum == expected["maximum"]
            assert controls_digest == expected["sha256"]
            total = 1
            for slot in control_slots:
                total *= radial_row["degrees"][slot] + 1
            closed[name] = {
                "radial_polynomial": radial_row,
                "control_slots": list(control_slots),
                "bernstein_total": total,
                "bernstein_nonzero": len(controls),
                "bernstein_zero": total - len(controls),
                "bernstein_minimum_nonzero": str(controls_minimum),
                "bernstein_maximum": str(controls_maximum),
                "bernstein_sha256": controls_digest,
            }
            del controls, radial
            gc.collect()
        sides[side] = {
            "C_ratio_interval": "[0,K/11]" if side == "below" else "[K/11,1]",
            "parameterized_polynomial": expected_poly,
            "root_order": root_order,
            "root_face": {
                **row(root_face),
                "identity": "28*R*(1-b)^2*(2*b+7)^2*(4*b+7)*(4*b+21)*(1-y)^2*(7*b*y+4*b-7*y+7)^2*(14*b*y-36*b-14*y-63)^2",
            },
            "closed_maximum_charts": closed,
        }
        if side == "below":
            third_v = radial_projective_chart(poly, ROOT_SLOTS, 6, root_order)
            third_v_row = row(third_v)
            assert third_v_row == {
                "terms": 145406,
                "degrees": [28, 0, 6, 0, 6, 10, 29, 6],
                "negative_power_coefficients": 72505,
                "sha256": "44e2a18c05eca1e00a198c271c773a91995a6305b8f6c4a9bfbe6059e41028e1",
            }
            fourth_order = min(
                sum(monomial[slot] for slot in ROOT_SLOTS)
                for monomial in third_v
            )
            assert fourth_order == 1
            fourth_face = {
                monomial: coefficient
                for monomial, coefficient in third_v.items()
                if sum(monomial[slot] for slot in ROOT_SLOTS) == fourth_order
            }
            assert fourth_face == fourth_face_expected
            assert row(fourth_face) == {
                "terms": 122,
                "degrees": [1, 0, 6, 0, 0, 10, 1, 0],
                "negative_power_coefficients": 55,
                "sha256": "97d4008cf2dc069d014f671c365942b1a2fa16918b4072d894bd770e68d61bda",
            }
            below_fourth_record = {
                "third_v_radial_polynomial": third_v_row,
                "fourth_order": fourth_order,
                "fourth_face": {
                    **row(fourth_face),
                    "identity": "28*(1-b)^2*(2*b+7)^2*(4*b+7)*(1-y)^2*(14*b*y-36*b-14*y-63)^2*(q*(4*b+21)*(7*b*y+4*b-7*y+7)^2+847*b*(4*b+7)*v)",
                },
            }
            del third_v
        del poly
        gc.collect()

    K_nonpositive_records = {}
    for patch, expected in EXPECTED_K_NONPOSITIVE.items():
        poly = K_nonpositive_parameterized(data["R_radial"], patch)
        assert row(poly) == expected["polynomial"]
        controls = bernstein_transform(poly, list(ACTIVE_SLOTS))
        controls_minimum = min(controls.values())
        controls_maximum = max(controls.values())
        controls_digest = digest(controls)
        assert len(controls) == expected["nonzero"]
        assert all(value > 0 for value in controls.values())
        assert controls_minimum == expected["minimum"]
        assert controls_maximum == expected["maximum"]
        assert controls_digest == expected["sha256"]
        total = 1
        for slot in ACTIVE_SLOTS:
            total *= expected["polynomial"]["degrees"][slot] + 1
        K_nonpositive_records[patch] = {
            "parameterization": (
                "B=(1+6*b)/7, zeta=y"
                if patch == "high_B"
                else "B=b/7, zeta=(7*(1-b)+11*b*y)/(7+4*b)"
            ),
            "polynomial": expected["polynomial"],
            "control_slots": list(ACTIVE_SLOTS),
            "bernstein_total": total,
            "bernstein_nonzero": len(controls),
            "bernstein_zero": total - len(controls),
            "bernstein_minimum_nonzero": str(controls_minimum),
            "bernstein_maximum": str(controls_maximum),
            "bernstein_sha256": controls_digest,
        }
        del controls, poly
        gc.collect()

    return {
        "schema": "amra.opg1757.round7.pnl-a-boundary-third-newton.v1",
        "domain": "the rho=1 boundary of the above-side A-maximal chart in the PNL second Newton fan",
        "reconstruction": {
            "deletion_forests": data["forest_count"],
            "endpoint_connected_forests": data["connected_count"],
            "second_A_radial_polynomial": row(data["second_A"]),
            "rho_one_boundary": row(data["boundary"]),
        },
        "transverse_zero_face": "r=1, Hbar=0, C=1, d=0, with zeta and B free",
        "transverse_local_polynomial": row(data["local"]),
        "transverse_order": 2,
        "transverse_face": {
            **row(data["transverse_face"]),
            "identity": "4*B*(2*B+1)^2*(2*zeta+9)^2*(11*C+R*((4*B+1)*zeta+7*B-1))^2",
        },
        "transverse_R_max_radial_polynomial": row(data["R_radial"]),
        "root_parameterization": "B=b/7, zeta=7*(1-b)*y/(7+4*b), K=(1-b)*(1-y); split C/R at K/11 and let v measure distance from the moving root",
        "K_nonpositive_patches": K_nonpositive_records,
        "below_open_v_fourth_face": below_fourth_record,
        "sides": sides,
        "conclusion": "the full K<=0 region and the below-side R-maximal and above-side R- and v-maximal charts of the K>=0 third Newton root are exactly Bernstein-nonnegative, with every stored nonzero control strictly positive; the next face in the open below/v chart is also manifestly nonnegative",
        "coverage_change": 0,
        "scope": "the below-side v-maximal chart for K>=0, the other transverse maximum directions, the rest of the above/A second-Newton chart, q3:PNL, and OPG-1757 are not claimed",
    }


def main():
    print(json.dumps(build_record(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
