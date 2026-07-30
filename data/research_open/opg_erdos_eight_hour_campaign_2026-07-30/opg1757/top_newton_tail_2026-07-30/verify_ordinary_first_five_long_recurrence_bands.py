#!/usr/bin/env python3
"""Exact audit of the first five all-depth H-recurrence bands."""

from __future__ import annotations

import argparse
import hashlib
import json

import sympy as sp


D, N, U = sp.symbols("d n u", integer=True)


def beta_polynomials() -> list[sp.Expr]:
    """Return the independently printed beta_(d,r), 0 <= r <= 5."""
    return [
        sp.Integer(1),
        -(
            22 * D**3 + 147 * D**2 + 161 * D - 258
        )
        / 36,
        (
            286 * D**6
            + 3546 * D**5
            + 12721 * D**4
            - 7812 * D**3
            - 86231 * D**2
            + 40338 * D
            + 209160
        )
        / 5184,
        -(
            158450 * D**9
            + 2651625 * D**8
            + 15805020 * D**7
            + 6658380 * D**6
            - 213815208 * D**5
            - 151402725 * D**4
            + 2063879770 * D**3
            + 1562087520 * D**2
            - 10631426832 * D
            - 6142443840
        )
        / 83980800,
        (
            5672590 * D**12
            + 111345780 * D**11
            + 940800098 * D**10
            + 1247424360 * D**9
            - 19928038791 * D**8
            - 49386060432 * D**7
            + 332001672380 * D**6
            + 627890141256 * D**5
            - 5187992393129 * D**4
            - 5254056336228 * D**3
            + 25894282085892 * D**2
            + 59075314211664 * D
            - 31756394113920
        )
        / 169305292800,
        (
            -15479380 * D**15
            - 325941210 * D**14
            - 3742393522 * D**13
            - 6592418448 * D**12
            + 111326408900 * D**11
            + 573131680737 * D**10
            - 2606390331587 * D**9
            - 10630453797180 * D**8
            + 79178201476618 * D**7
            + 110117646980439 * D**6
            - 1139766102529649 * D**5
            - 2901603595595082 * D**4
            + 14532178406634252 * D**3
            + 4464839765897784 * D**2
            + 14350329772954848 * D
            - 57046347650960640
        )
        / 42664933785600,
    ]


def signed_stirling_near_diagonal(maximum_defect: int) -> list[sp.Expr]:
    """Construct s(n,n-m) from the defining Stirling recurrence."""
    rows = [[sp.Integer(1)]]
    maximum_n = 2 * maximum_defect + 2
    for value in range(maximum_n):
        following = [sp.Integer(0)] * (value + 2)
        for index in range(value + 2):
            following[index] = (
                (rows[-1][index - 1] if index else 0)
                - value
                * (rows[-1][index] if index < len(rows[-1]) else 0)
            )
        rows.append(following)

    result = [sp.Integer(1)]
    for defect in range(1, maximum_defect + 1):
        points = [
            (
                value,
                rows[value][value - defect]
                if value >= defect
                else 0,
            )
            for value in range(2 * defect + 2)
        ]
        polynomial = sp.factor(sp.interpolate(points, N))
        if sp.expand(
            polynomial.subs(N, N + 1)
            - polynomial
            + N * result[defect - 1]
        ) != 0:
            raise AssertionError("Stirling recurrence failed")
        result.append(polynomial)
    return result


def derive_bands() -> tuple[list[sp.Expr], list[sp.Expr]]:
    beta = beta_polynomials()
    stirling = signed_stirling_near_diagonal(5)
    h = [sp.Integer(1)]
    for loss in range(1, 6):
        monomial_coefficient = sum(
            beta[rank]
            * sp.prod(
                D - rank - offset
                for offset in range(loss - rank)
            )
            / sp.factorial(loss - rank)
            * 2 ** (loss - rank)
            for rank in range(loss + 1)
        )
        h.append(
            sp.factor(
                monomial_coefficient
                - sum(
                    h[index]
                    * stirling[loss - index].subs(N, D - index)
                    for index in range(loss)
                )
            )
        )

    gamma = []
    for band in range(5):
        value = h[band + 1] - h[band + 1].subs(D, D + 1)
        value -= sum(
            gamma[index]
            * h[band - index].subs(D, D - 1 - 2 * index)
            for index in range(band)
        )
        gamma.append(sp.factor(value))
    return h, gamma


def audit() -> dict[str, object]:
    h, gamma = derive_bands()
    denominators = [
        6,
        432,
        933120,
        2351462400,
        84652646400,
    ]
    expected_first_values = [
        sp.Integer(18),
        sp.Integer(630),
        sp.Rational(399363, 4),
        sp.Rational(721102503, 20),
        sp.Rational(11688306931609, 480),
    ]

    records = []
    for band, (value, denominator) in enumerate(
        zip(gamma, denominators)
    ):
        shifted = sp.Poly(
            sp.cancel(
                denominator * value.subs(D, U + 2 * band + 1)
            ),
            U,
        )
        coefficients = shifted.all_coeffs()
        if any(coefficient <= 0 for coefficient in coefficients):
            raise AssertionError("shifted positivity certificate failed")
        if sp.simplify(
            value.subs(D, 2 * band + 1)
            - expected_first_values[band]
        ) != 0:
            raise AssertionError("first recurrence value mismatch")
        payload = ",".join(str(item) for item in coefficients)
        records.append(
            {
                "band": band,
                "minimum_depth": 2 * band + 1,
                "degree": shifted.degree(),
                "denominator": denominator,
                "shifted_coefficients": [
                    int(item) for item in coefficients
                ],
                "coefficient_sha256": hashlib.sha256(
                    payload.encode("ascii")
                ).hexdigest(),
                "first_value": str(expected_first_values[band]),
            }
        )

    return {
        "schema": "amra.opg1757.first-five-long-recurrence-bands.v1",
        "ordinary_to_newton_rows": len(h),
        "positive_bands": len(gamma),
        "records": records,
        "status": "all_depth_symbolic_audit_passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
