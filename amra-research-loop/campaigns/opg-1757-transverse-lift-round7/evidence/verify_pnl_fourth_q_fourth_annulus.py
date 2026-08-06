#!/usr/bin/env python3
"""Exact three-box certificate on the fourth dyadic PNL fourth-q annulus."""

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
from verify_pnl_a_boundary_third_newton import ACTIVE_SLOTS
from verify_pnl_double_corner_blowup import row, substitute_slot
from verify_pnl_fourth_q_third_annulus import fourth_q_chart
from verify_rlp_projective_corner_reduction import polynomial_sum


EXPECTED_BOXES = {
    "y_upper": {
        "parameterization": "y=(1+s)/2",
        "control_slots": ["t", "s", "Hbar", "b", "v", "d"],
        "polynomial": {
            "terms": 1548357,
            "degrees": [56, 0, 6, 0, 6, 10, 29, 6],
            "negative_power_coefficients": 772993,
            "sha256": "f7ffbaacd0052a5f1f480a8a570f67af4bed820358d62afc3ff97a099186f36b",
        },
        "nonzero": 6342903,
        "minimum": Fraction(
            66866630868257242644583176402256825460878175561391541255500341372816011034624,
            29,
        ),
        "maximum": Fraction(
            2866322477156774015431049977677976674918321880091269389693815272491907388087992320
        ),
        "sha256": "184943060ebdbd964d97f5b5f74ac01c6f3d3c7af151c2bf19e99c9e9a07c9ae",
    },
    "y_lower_b_lower": {
        "parameterization": "y=s/2, b=u/2",
        "control_slots": ["t", "s", "Hbar", "u", "v", "d"],
        "polynomial": {
            "terms": 1534986,
            "degrees": [56, 0, 6, 0, 6, 10, 29, 6],
            "negative_power_coefficients": 764953,
            "sha256": "73a6b111aee99216c3e7e10c926d866cb206293d895f03553f3d5e84ad478d8d",
        },
        "nonzero": 6451830,
        "minimum": Fraction(
            14002728023886008855224350501534981101129231849436822238173948072210412653277257410805760,
            2921943,
        ),
        "maximum": Fraction(
            405662100012636618894845984800430961788337440589549651297176752238527060527336652800
        ),
        "sha256": "2414bc2ae62479d015ff94bbe0c89b1a5427d038bd5bccf694f0e37f415550b8",
    },
    "y_lower_b_upper": {
        "parameterization": "y=s/2, b=(1+u)/2",
        "control_slots": ["t", "s", "Hbar", "u", "v", "d"],
        "polynomial": {
            "terms": 1546458,
            "degrees": [56, 0, 6, 0, 6, 10, 29, 6],
            "negative_power_coefficients": 771275,
            "sha256": "27099f0da9959f5195ab11e37ccdfeef680e9729a9da501aacf2f6d7906c4b86",
        },
        "nonzero": 6412728,
        "minimum": Fraction(
            1756448887530286401999821296708232802020302028156135542066253414590540358772326400
        ),
        "maximum": Fraction(
            2935114216608536591801395177142248115116361605213459855046466839031713165402104135680
        ),
        "sha256": "5e43dd00134a0cbde9728fdeacb27569f024a2da886ba7ba9d5b71775d9b0e96",
    },
}


def build_record():
    fourth_q = fourth_q_chart()
    q, y, b = (variable(slot) for slot in (0, 2, 5))
    annulus, q_degree = substitute_slot(
        fourth_q, 0, polynomial_sum(constant(1), q), constant(16)
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
        "schema": "amra.opg1757.round7.pnl-fourth-q-fourth-annulus.v1",
        "domain": "the q-maximal fourth-Newton chart inside the below-root v-maximal third chart",
        "base_chart_sha256": "2e44871e941553ecdaefad9a3750b5e1c1505f3d76bf5fb7ec5a70828a423c25",
        "q_interval": "[1/16,1/8]",
        "q_parameterization": "q=(1+t)/16 with 0<=t<=1; clear by the positive factor 16^56",
        "partition": "y>=1/2, or y<=1/2 split at b=1/2",
        "boxes": records,
        "strictly_positive_nonzero_controls": sum(
            record["bernstein_nonzero"] for record in records.values()
        ),
        "conclusion": "the complete fourth dyadic annulus 1/16<=q<=1/8 is exactly Bernstein-nonnegative; together with the prior ledgers this certifies the full q>=1/16 region of the q-maximal fourth chart",
        "coverage_change": 0,
        "scope": "the q<1/16 region, the v-maximal fourth chart, the other transverse directions, q3:PNL, and OPG-1757 are not claimed",
    }


def main():
    print(json.dumps(build_record(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
