#!/usr/bin/env python3
"""Exact coefficient audit for the all-orders ordinary top symbol."""

from __future__ import annotations

import argparse
import json

import sympy as sp

from verify_top_six_newton_tail import J, S, profile


def normalized_profile_value(
    loss: int,
    profile_index: int,
    edge_count: int,
) -> sp.Expr:
    polynomial = sp.Poly(profile(profile_index, edge_count), S)
    power = 2 * edge_count - loss
    coefficient = (
        sp.S.Zero
        if power < 0
        else polynomial.coeff_monomial(S**power)
    )
    return sp.factor(
        coefficient * 2**edge_count * sp.factorial(edge_count)
    )


def interpolate_profile(loss: int, profile_index: int) -> sp.Expr:
    values = [
        normalized_profile_value(loss, profile_index, edge_count)
        for edge_count in range(loss + 4)
    ]
    polynomial = sp.interpolate(
        [
            (edge_count, values[edge_count])
            for edge_count in range(loss + 1)
        ],
        J,
    )
    assert sp.degree(polynomial, J) <= loss
    for edge_count in range(loss + 1, loss + 4):
        assert sp.simplify(
            polynomial.subs(J, edge_count) - values[edge_count]
        ) == 0
    return sp.factor(polynomial)


def symbol_records(maximum_loss: int) -> list[dict[str, object]]:
    x = sp.symbols("x")
    expected_a = sp.series(
        sp.sqrt(1 - 2 * x), x, 0, maximum_loss + 1
    ).removeO()
    expected_b = sp.series(
        -2 * x / sp.sqrt(1 - 2 * x),
        x,
        0,
        maximum_loss,
    ).removeO()
    expected_c = sp.series(
        -2 * x**2 / (1 - 2 * x) ** sp.Rational(3, 2),
        x,
        0,
        maximum_loss - 1,
    ).removeO()

    records = []
    for loss in range(maximum_loss + 1):
        profiles = [
            interpolate_profile(loss, profile_index)
            for profile_index in range(3)
        ]
        a = sp.Poly(profiles[0], J).coeff_monomial(J**loss)
        b = (
            sp.S.Zero
            if loss == 0
            else sp.Poly(profiles[1] - profiles[0], J)
            .coeff_monomial(J ** (loss - 1))
        )
        c = (
            sp.S.Zero
            if loss < 2
            else sp.Rational(1, 2)
            * sp.Poly(
                profiles[2] - 2 * profiles[1] + profiles[0],
                J,
            ).coeff_monomial(J ** (loss - 2))
        )
        assert a == sp.expand(expected_a).coeff(x, loss)
        assert b == (
            sp.S.Zero
            if loss == 0
            else sp.expand(expected_b).coeff(x, loss - 1)
        )
        assert c == (
            sp.S.Zero
            if loss < 2
            else sp.expand(expected_c).coeff(x, loss - 2)
        )
        records.append(
            {
                "loss": loss,
                "A": str(a),
                "B": str(b),
                "C": str(c),
            }
        )
    determinant_symbol = sp.factor(
        (
            -2 * (x / 2) / sp.sqrt(1 - x)
        ) ** 2
        - 2
        * sp.sqrt(1 - x)
        * (
            -2
            * (x / 2) ** 2
            / (1 - x) ** sp.Rational(3, 2)
        )
    )
    assert sp.simplify(
        determinant_symbol - 2 * x**2 / (1 - x)
    ) == 0
    return records


def audit(maximum_loss: int = 12) -> dict[str, object]:
    records = symbol_records(maximum_loss)
    return {
        "schema": "amra.opg1757.ordinary-top-symbol.v1",
        "scope": (
            "Coefficientwise profile interpolation with redundant "
            "points, exact A/B/C resummation checks, and determinant "
            "symbol simplification. The all-orders step rests on the "
            "formal Lagrange extraction in the accompanying proof."
        ),
        "maximum_loss": maximum_loss,
        "records": records,
        "record_count": len(records),
        "determinant_symbol": "2*x**2/(1-x)",
        "ordinary_leading_symbol": "1/(1-x)",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-loss", type=int, default=12)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.maximum_loss),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
