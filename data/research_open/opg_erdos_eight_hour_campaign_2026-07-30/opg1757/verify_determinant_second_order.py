#!/usr/bin/env python3
"""Symbolic regression for the second-order component determinant asymptotic."""

from __future__ import annotations

import json
import math
from fractions import Fraction

import sympy as sp


U = sp.symbols("u")
RHO, SIGMA = sp.symbols("rho sigma", integer=True, nonnegative=True)


def truncate(expression: sp.Expr) -> sp.Expr:
    return sp.series(expression, U, 0, 4).removeO().expand()


def component_prefixes(variable: sp.Expr) -> dict[str, sp.Expr]:
    w0 = (
        1
        + 5 * variable * U
        + variable * (35 * variable - 47) * U**2 / 2
        + variable
        * (variable - 1)
        * (105 * variable - 364)
        * U**3
        / 2
    )
    adjacent = (
        3
        + 11 * variable * U
        + 5 * variable * (13 * variable - 37) * U**2 / 2
        + variable
        * (variable - 1)
        * (175 * variable - 1304)
        * U**3
        / 2
    )
    c = variable + 1
    w1 = truncate(2 * (1 - c * U) * w0 / (1 - U))
    w2 = truncate(
        (
            4 * (1 - c * U) * (1 - (c + 1) * U) * w0
            - 4 * U * (1 - U) * (1 - 2 * U) * adjacent
        )
        / ((1 - U) * (1 - 2 * U) * (1 - 3 * U))
    )
    return {"w0": w0, "adjacent": adjacent, "w1": w1, "w2": w2}


def audit(maximum_total: int = 24) -> dict[str, object]:
    left = component_prefixes(RHO)
    right = component_prefixes(SIGMA)
    ordered = truncate(
        left["w1"] * right["w1"] - left["w0"] * right["w2"]
    )
    symmetrized_u3 = sp.factor(
        (
            ordered.coeff(U, 3)
            + ordered.xreplace({RHO: SIGMA, SIGMA: RHO}).coeff(U, 3)
        )
        / 2
    )
    R = RHO + SIGMA
    expected = -2 * (
        5 * R**3
        - 9 * R**2
        + 4 * R
        - (20 * R + 16) * RHO * SIGMA
    )
    if sp.expand(symmetrized_u3 - expected) != 0:
        raise AssertionError((symmetrized_u3, expected))

    constants = []
    for total_components in range(3, maximum_total + 1):
        total = total_components - 2
        leading = Fraction(0)
        next_term = Fraction(0)
        for rho in range(total + 1):
            sigma = total - rho
            weight = Fraction(
                1,
                2**total * math.factorial(rho) * math.factorial(sigma),
            )
            leading += 2 * weight * (
                3 * total - (rho - sigma) ** 2
            )
            cubic = expected.subs({RHO: rho, SIGMA: sigma})
            next_term += weight * int(cubic)
        expected_leading = Fraction(
            4, math.factorial(total_components - 3)
        )
        expected_next = (
            Fraction(0)
            if total_components == 3
            else Fraction(16, math.factorial(total_components - 4))
        )
        if leading != expected_leading or next_term != expected_next:
            raise AssertionError(
                (
                    total_components,
                    leading,
                    expected_leading,
                    next_term,
                    expected_next,
                )
            )
        constants.append(
            {
                "total_components": total_components,
                "leading": str(leading),
                "next": str(next_term),
            }
        )

    return {
        "schema": "amra.opg1757.determinant-second-order.v1",
        "scope": "Symbolic regression of the human fixed-t expansion.",
        "symmetrized_u3": str(symmetrized_u3),
        "constant_checks": constants,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
