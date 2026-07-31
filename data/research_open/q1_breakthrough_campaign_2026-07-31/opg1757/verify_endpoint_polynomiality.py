#!/usr/bin/env python3
"""Regression certificate for uniform endpoint polynomiality."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import sympy as sp


HERE = pathlib.Path(__file__).resolve().parent
OLD = (
    HERE.parents[1]
    / "q1_three_hour_campaign_2026-07-31"
    / "opg1757"
)
sys.path.insert(0, str(OLD))


def audit(extended_q6: bool = False) -> dict[str, object]:
    if extended_q6:
        from verify_seventh_q6 import Q6_ENDPOINT_POLYNOMIALS as table
    else:
        from verify_sixth_q5 import Q5_ENDPOINT_POLYNOMIALS as table

    from verify_second_deficit import S

    checked = 0
    for (h, excess, components), expression in table.items():
        numerator, denominator = sp.fraction(expression)
        if sp.Poly(denominator, S).degree() != 0:
            raise AssertionError(
                "endpoint denominator remains at "
                f"{(h, excess, components)}"
            )
        expected_degree = 2 * components + 2 * excess - 2
        if sp.Poly(numerator, S).degree() != expected_degree:
            raise AssertionError(
                "endpoint degree mismatch at "
                f"{(h, excess, components)}"
            )
        checked += 1

    return {
        "schema": "amra.opg1757.endpoint-polynomiality.v1",
        "status": "PASS",
        "theorem_status": "PROVED",
        "extended_q6": extended_q6,
        "endpoint_polynomials_checked": checked,
        "scope": "finite regression audit of an all-parameter proof",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--extended-q6", action="store_true")
    args = parser.parse_args()
    print(json.dumps(audit(args.extended_q6), indent=2, sort_keys=True))
