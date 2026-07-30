#!/usr/bin/env python3
"""Exact counterexample search for ordinary-polynomial real-rootedness."""

from __future__ import annotations

import argparse
import json

import sympy as sp

from independent_verify_all_fixed_rank_ordinary_symbol_algorithm import (
    exact_ordinary_polynomial,
)


K = sp.symbols("k")


def first_defect(depth: int):
    return sp.Rational(
        22 * depth**3
        + 147 * depth**2
        + 161 * depth
        - 258,
        36,
    )


def forced_boundary(depth: int):
    return range(2, (depth + 3) // 2 + 1)


def residual_polynomial(depth: int):
    polynomial = exact_ordinary_polynomial(depth)
    for root in forced_boundary(depth):
        quotient, remainder = sp.div(
            polynomial,
            sp.Poly(K - root, K),
        )
        assert remainder.is_zero
        polynomial = quotient
    return polynomial.monic()


def recurrence_obstructions():
    even = [
        sp.Poly(1, K),
        residual_polynomial(2),
        residual_polynomial(4),
        residual_polynomial(6),
    ]
    odd = [
        sp.Poly(1, K),
        residual_polynomial(3),
        residual_polynomial(5),
        residual_polynomial(7),
    ]
    records = {}
    for name, sequence in (("even", even), ("odd", odd)):
        previous = sequence[1]
        current = sequence[2]
        following = sequence[3]
        degree = current.degree()
        alpha = sp.Poly(
            K * current.as_expr() - following.as_expr(),
            K,
        ).coeff_monomial(K**degree)
        remainder = sp.Poly(
            sp.expand(
                (K - alpha) * current.as_expr()
                - following.as_expr()
            ),
            K,
        )
        beta = remainder.coeff_monomial(
            K ** (degree - 1)
        )
        obstruction = sp.factor(
            remainder.as_expr() - beta * previous.as_expr()
        )
        assert obstruction != 0
        records[name] = {
            "alpha": str(alpha),
            "beta": str(beta),
            "obstruction": str(obstruction),
        }
    assert records["even"]["obstruction"] == "2148751/12"
    assert records["odd"]["obstruction"] == "55578361/48"
    return records


def hessenberg_minor_obstruction():
    polynomials = [
        sp.Poly(1, K),
        *[exact_ordinary_polynomial(depth) for depth in range(1, 5)],
    ]
    coefficients = []
    for depth in range(4):
        remainder = sp.Poly(
            K * polynomials[depth].as_expr()
            - polynomials[depth + 1].as_expr(),
            K,
        )
        row = {}
        for basis_index in range(depth, -1, -1):
            coefficient = remainder.coeff_monomial(
                K**basis_index
            )
            row[basis_index] = coefficient
            remainder = sp.Poly(
                sp.expand(
                    remainder.as_expr()
                    - coefficient
                    * polynomials[basis_index].as_expr()
                ),
                K,
            )
        assert remainder.is_zero
        coefficients.append(row)

    value = sp.det(
        sp.Matrix(
            [
                [coefficients[2][1], coefficients[3][1]],
                [coefficients[2][2], coefficients[3][2]],
            ]
        )
    )
    assert value == -125667
    return value


def audit(maximum_depth: int = 30):
    root_checks = 0
    coefficient_checks = 0
    weighted_checks = 0
    boundary_checks = 0
    rows = []

    for depth in range(1, maximum_depth + 1):
        polynomial = exact_ordinary_polynomial(depth)
        assert polynomial.degree() == depth
        assert sp.gcd(polynomial, polynomial.diff()).degree() == 0
        positive_roots = polynomial.count_roots(0, sp.oo)
        assert positive_roots == depth
        root_checks += 1

        assert (
            -polynomial.coeff_monomial(K ** (depth - 1))
            == first_defect(depth)
        )
        assert first_defect(depth) <= 3 * depth**3

        for rank in range(depth + 1):
            coefficient = polynomial.coeff_monomial(
                K ** (depth - rank)
            )
            assert (-1) ** rank * coefficient > 0
            coefficient_checks += 1
            assert abs(coefficient) <= (
                sp.binomial(depth, rank)
                * (3 * depth**2) ** rank
            )
            weighted_checks += 1

        for root in forced_boundary(depth):
            assert polynomial.eval(root) == 0
            boundary_checks += 1

        rows.append(
            {
                "depth": depth,
                "positive_simple_roots": int(positive_roots),
                "forced_boundary_roots": list(
                    forced_boundary(depth)
                ),
            }
        )

    recurrence = recurrence_obstructions()
    minor = hessenberg_minor_obstruction()
    return {
        "schema": "amra.opg1757.independent-ordinary-real-root-attack.v1",
        "imports_root_claim_or_verifier": False,
        "maximum_depth": maximum_depth,
        "exact_sturm_root_checks": root_checks,
        "strict_alternating_coefficient_checks": coefficient_checks,
        "weighted_C3_checks": weighted_checks,
        "forced_boundary_root_checks": boundary_checks,
        "three_term_recurrence_obstructions": recurrence,
        "hessenberg_negative_minor": str(minor),
        "rows": rows,
        "classification": {
            "real_rooted_all_d": "open",
            "weighted_C3_conditional_on_real_rootedness": "proved",
            "standard_three_term_route": "disproved_in_natural_normalization",
            "naive_TN_hessenberg_route": "disproved",
        },
        "status": "finite_real_root_search_passed",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-depth", type=int, default=30)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.maximum_depth),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
