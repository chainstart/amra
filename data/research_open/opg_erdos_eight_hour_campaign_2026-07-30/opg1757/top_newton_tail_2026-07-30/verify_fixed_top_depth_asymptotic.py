#!/usr/bin/env python3
"""Audit the fixed-top-depth asymptotic theorem for OPG-1757."""

from __future__ import annotations

import argparse
import json

import sympy as sp

from verify_top_six_newton_tail import (
    J,
    K,
    S,
    determinant_power_coefficients,
    newton_tail,
    profile,
    recorded_profile_symbols,
)


def profile_degree_audit(maximum_loss: int) -> list[dict[str, object]]:
    """Interpolate each normalized profile layer and test spare points."""
    records: list[dict[str, object]] = []
    for loss in range(maximum_loss + 1):
        for profile_index in range(3):
            values: list[sp.Expr] = []
            for edge_count in range(loss + 4):
                polynomial = sp.Poly(
                    profile(profile_index, edge_count), S
                )
                power = 2 * edge_count - loss
                coefficient = (
                    sp.S.Zero
                    if power < 0
                    else polynomial.coeff_monomial(S**power)
                )
                values.append(
                    sp.factor(
                        coefficient
                        * 2**edge_count
                        * sp.factorial(edge_count)
                    )
                )
            interpolant = sp.interpolate(
                [
                    (edge_count, values[edge_count])
                    for edge_count in range(loss + 1)
                ],
                J,
            )
            assert sp.degree(interpolant, J) <= loss
            for edge_count in range(loss + 1, loss + 4):
                assert (
                    sp.simplify(
                        interpolant.subs(J, edge_count)
                        - values[edge_count]
                    )
                    == 0
                )
            records.append(
                {
                    "loss": loss,
                    "profile": profile_index,
                    "degree": int(sp.degree(interpolant, J)),
                    "spare_checks": 3,
                }
            )
    return records


def leading_constant_recurrence(maximum_depth: int) -> list[sp.Rational]:
    """Rebuild the leading constants using only the triangular system."""
    constants = [sp.Integer(1)]
    for depth in range(1, maximum_depth + 1):
        value = -sum(
            constants[earlier]
            * (-1) ** (depth - earlier)
            * sp.Rational(
                2 ** (depth - earlier),
                sp.factorial(depth - earlier),
            )
            for earlier in range(depth)
        )
        value = sp.factor(value)
        assert value == sp.Rational(
            2**depth, sp.factorial(depth)
        )
        constants.append(value)
    return constants


def exact_tail_leading_audit() -> list[dict[str, object]]:
    """Check the six exact formulas against the general leading term."""
    symbols = recorded_profile_symbols()
    power_coefficients = determinant_power_coefficients(symbols)
    tail = newton_tail(power_coefficients)
    records = []
    for depth, expression in enumerate(tail):
        polynomial = sp.Poly(sp.expand(expression), K)
        assert polynomial.degree() == 2 * depth
        expected = sp.Rational(2**depth, sp.factorial(depth))
        assert polynomial.LC() == expected
        records.append(
            {
                "depth": depth,
                "degree": polynomial.degree(),
                "leading_constant": str(polynomial.LC()),
            }
        )
    return records


def audit(
    maximum_profile_loss: int = 12,
    maximum_abstract_depth: int = 64,
) -> dict[str, object]:
    profile_records = profile_degree_audit(maximum_profile_loss)
    constants = leading_constant_recurrence(maximum_abstract_depth)
    exact_records = exact_tail_leading_audit()
    return {
        "schema": "amra.opg1757.fixed-top-depth-asymptotic.v1",
        "scope": (
            "Checks the marked profile degree law at finite losses, "
            "the abstract all-depth leading recurrence, and the exact "
            "top-six formulas; the all-depth proof is the accompanying "
            "cycle-inclusion-exclusion argument."
        ),
        "profile_records": profile_records,
        "profile_checks": len(profile_records),
        "abstract_depth": maximum_abstract_depth,
        "abstract_leading_constants": [
            str(value) for value in constants
        ],
        "exact_tail": exact_records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-profile-loss", type=int, default=12)
    parser.add_argument("--maximum-abstract-depth", type=int, default=64)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(
                args.maximum_profile_loss,
                args.maximum_abstract_depth,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
