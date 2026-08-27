#!/usr/bin/env python3
"""Exact three-box certificate on the third dyadic PNL fourth-q annulus."""

from __future__ import annotations

from fractions import Fraction
import gc
import json

from verify_negative_c_direct_chambers import (
    bernstein_transform,
    constant,
    variable,
)
from verify_negative_page_direct_chambers import digest
from verify_pnl_a_boundary_third_newton import (
    ACTIVE_SLOTS,
    ROOT_SLOTS,
    parameterized,
    transverse_data,
)
from verify_pnl_double_corner_blowup import (
    radial_projective_chart,
    row,
    substitute_slot,
)
from verify_rlp_projective_corner_reduction import polynomial_sum


EXPECTED_BOXES = {
    "y_upper": {
        "parameterization": "y=(1+s)/2",
        "control_slots": ["t", "s", "Hbar", "b", "v", "d"],
        "polynomial": {
            "terms": 1548355,
            "degrees": [56, 0, 6, 0, 6, 10, 29, 6],
            "negative_power_coefficients": 771637,
            "sha256": "b4a97c1dc52fc481814173d5a3e3cfa455e89403a19beb9f96c50048d6ffdf4f",
        },
        "nonzero": 6342903,
        "minimum": Fraction(
            288719599266701373796636857000180088121689690664617072647995392,
            225,
        ),
        "maximum": Fraction(
            249950351024904264873095336335426523972260510944078138546585600000
        ),
        "sha256": "9defb225132dc7e996438824ee6457fa44ebaf3f3baee3c99b970d5b4689426e",
    },
    "y_lower_b_lower": {
        "parameterization": "y=s/2, b=u/2",
        "control_slots": ["t", "s", "Hbar", "u", "v", "d"],
        "polynomial": {
            "terms": 1534984,
            "degrees": [56, 0, 6, 0, 6, 10, 29, 6],
            "negative_power_coefficients": 764932,
            "sha256": "6a6cd82516fe465f5d9fc6516a9788a825d8b03735d228a608dfca452b98b914",
        },
        "nonzero": 6451830,
        "minimum": Fraction(
            2141530632485625792181398562011605521956101964218746653779165184000,
            29,
        ),
        "maximum": Fraction(
            62810213289641541494105380450414487517691963875451438015660110643200
        ),
        "sha256": "05f42d9a1ee0b95dc90983356ccee942637232aee36b4189894d0e331ab1d815",
    },
    "y_lower_b_upper": {
        "parameterization": "y=s/2, b=(1+u)/2",
        "control_slots": ["t", "s", "Hbar", "u", "v", "d"],
        "polynomial": {
            "terms": 1546459,
            "degrees": [56, 0, 6, 0, 6, 10, 29, 6],
            "negative_power_coefficients": 770994,
            "sha256": "59e602c641332c568d55b2c371547c7b4c77742780e9ea40778349d8d50b0748",
        },
        "nonzero": 6412728,
        "minimum": Fraction(
            25189422410264330721793603209921788388419977438674721511634370560
        ),
        "maximum": Fraction(
            255949159449501967230049624407476760547594763206736013871703654400000
        ),
        "sha256": "ddf0e712b4b337902975fb26af4c4eb934d9b287e6c5b0ff082080a0c6ca38a3",
    },
}


def fourth_q_chart():
    data = transverse_data()
    below = parameterized(data["R_radial"], "below")
    assert row(below) == {
        "terms": 145406,
        "degrees": [28, 0, 6, 0, 6, 10, 2, 6],
        "negative_power_coefficients": 72505,
        "sha256": "2be1763b2daf5c675b967e00bf8d2a8dca41e73fe79bc2ebaf3243f667e7059e",
    }
    third_v = radial_projective_chart(below, ROOT_SLOTS, 6, 1)
    fourth_order = min(
        sum(monomial[slot] for slot in ROOT_SLOTS) for monomial in third_v
    )
    assert fourth_order == 1
    fourth_q = radial_projective_chart(third_v, ROOT_SLOTS, 0, fourth_order)
    assert row(fourth_q) == {
        "terms": 145406,
        "degrees": [56, 0, 6, 0, 6, 10, 29, 6],
        "negative_power_coefficients": 72505,
        "sha256": "2e44871e941553ecdaefad9a3750b5e1c1505f3d76bf5fb7ec5a70828a423c25",
    }
    del data, below, third_v
    gc.collect()
    return fourth_q


def build_record():
    fourth_q = fourth_q_chart()
    q, y, b = (variable(slot) for slot in (0, 2, 5))
    annulus, q_degree = substitute_slot(
        fourth_q, 0, polynomial_sum(constant(1), q), constant(8)
    )
    assert q_degree == 56
    del fourth_q
    gc.collect()

    records = {}
    for name, expected in EXPECTED_BOXES.items():
        y_numerator = (
            polynomial_sum(constant(1), y) if name == "y_upper" else y
        )
        box, y_degree = substitute_slot(annulus, 2, y_numerator, constant(2))
        assert y_degree == 6
        if name != "y_upper":
            b_numerator = (
                b
                if name == "y_lower_b_lower"
                else polynomial_sum(constant(1), b)
            )
            box, b_degree = substitute_slot(box, 5, b_numerator, constant(2))
            assert b_degree == 10
        box_row = row(box)
        assert box_row == expected["polynomial"]
        controls = bernstein_transform(box, list(ACTIVE_SLOTS))
        assert len(controls) == expected["nonzero"]
        assert all(value > 0 for value in controls.values())
        assert min(controls.values()) == expected["minimum"]
        assert max(controls.values()) == expected["maximum"]
        assert digest(controls) == expected["sha256"]
        records[name] = {
            "parameterization": expected["parameterization"],
            "polynomial": box_row,
            "control_slots": expected["control_slots"],
            "bernstein_total": 6451830,
            "bernstein_nonzero": len(controls),
            "bernstein_zero": 6451830 - len(controls),
            "bernstein_minimum_nonzero": str(min(controls.values())),
            "bernstein_maximum": str(max(controls.values())),
            "bernstein_sha256": digest(controls),
        }
        del controls, box
        gc.collect()

    return {
        "schema": "amra.opg1757.round7.pnl-fourth-q-third-annulus.v1",
        "domain": "the q-maximal fourth-Newton chart inside the below-root v-maximal third chart",
        "base_chart_sha256": "2e44871e941553ecdaefad9a3750b5e1c1505f3d76bf5fb7ec5a70828a423c25",
        "q_interval": "[1/8,1/4]",
        "q_parameterization": "q=(1+t)/8 with 0<=t<=1; clear by the positive factor 8^56",
        "partition": "y>=1/2, or y<=1/2 split at b=1/2",
        "boxes": records,
        "strictly_positive_nonzero_controls": sum(
            record["bernstein_nonzero"] for record in records.values()
        ),
        "conclusion": "the complete third dyadic annulus 1/8<=q<=1/4 is exactly Bernstein-nonnegative; together with pnl_a_boundary_third_newton.json this certifies the full q>=1/8 region of the q-maximal fourth chart",
        "coverage_change": 0,
        "scope": "the q<1/8 region, the v-maximal fourth chart, the other transverse directions, q3:PNL, and OPG-1757 are not claimed",
    }


def main():
    print(json.dumps(build_record(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
