#!/usr/bin/env python3
"""Exact finite audit of the conjectural real-rooted ordinary symbols.

This is a finite certificate, not a proof for arbitrary depth.  Every
root statement is certified over QQ by square-free factorization and
rational isolating intervals; floating-point root finders are not used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math

import sympy as sp

from verify_explicit_polynomial_top_window import ordinary_polynomial


K = sp.symbols("k")
Z = sp.symbols("z")
X = sp.symbols("x")


def forced_factor(depth: int) -> sp.Poly:
    """The factor forced by the inactive coefficients d > 2k-4."""
    degree = (depth + 1) // 2
    return sp.Poly(
        sp.prod(K - root for root in range(2, degree + 2)),
        K,
    )


def reduced_polynomial(depth: int, polynomial: sp.Poly) -> sp.Poly:
    quotient, remainder = sp.div(polynomial, forced_factor(depth))
    if not remainder.is_zero:
        raise AssertionError("the forced inactive-depth factor is absent")
    if quotient.degree() != depth // 2:
        raise AssertionError("unexpected residual degree")
    return quotient.monic()


def coefficient_digest(polynomial: sp.Poly) -> str:
    payload = ",".join(str(value) for value in polynomial.all_coeffs())
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def falling_newton_coefficients(polynomial: sp.Poly) -> list[sp.Rational]:
    """Coefficients in (k-2)_j, obtained by exact forward differences."""
    degree = polynomial.degree()
    differences = [polynomial.eval(2 + offset) for offset in range(degree + 1)]
    result = []
    for index in range(degree + 1):
        result.append(sp.Rational(differences[0], math.factorial(index)))
        differences = [
            differences[position + 1] - differences[position]
            for position in range(len(differences) - 1)
        ]
    return result


def poisson_newton_residual(
    depth: int,
    newton_coefficients: list[sp.Rational],
) -> sp.Poly:
    """Return A_d(z)/z^ceil(d/2) from the exact Poisson transform."""
    first_nonzero = (depth + 1) // 2
    return sp.Poly(
        sum(
            newton_coefficients[index] * Z ** (index - first_nonzero)
            for index in range(first_nonzero, depth + 1)
        ),
        Z,
    ).monic()


def matching_polynomial(
    depth: int,
    newton_coefficients: list[sp.Rational],
) -> sp.Poly:
    """The parity polynomial H_d defined by A_d(x^2)=x^d H_d(x)."""
    return sp.Poly(
        sum(
            newton_coefficients[index] * X ** (2 * index - depth)
            for index in range((depth + 1) // 2, depth + 1)
        ),
        X,
    )


def matching_basis_recurrence(rows: list[sp.Poly]) -> dict[str, object]:
    """Expand x H_d-H_(d+1) in the same-parity earlier H rows."""
    positive_coefficients = []
    records = []
    for depth in range(1, len(rows) - 1):
        residual = sp.Poly(
            sp.expand(
                X * rows[depth].as_expr() - rows[depth + 1].as_expr()
            ),
            X,
        )
        coefficients = []
        for earlier_depth in range(depth - 1, -1, -2):
            coefficient = residual.coeff_monomial(X**earlier_depth)
            if coefficient <= 0:
                raise AssertionError(
                    "matching-basis connection coefficient is not positive"
                )
            coefficients.append(coefficient)
            positive_coefficients.append(coefficient)
            residual = sp.Poly(
                sp.expand(
                    residual.as_expr()
                    - coefficient * rows[earlier_depth].as_expr()
                ),
                X,
            )
        if not residual.is_zero:
            raise AssertionError("matching-basis recurrence has a residual")
        payload = ",".join(str(value) for value in coefficients)
        records.append(
            {
                "depth": depth,
                "number_of_positive_terms": len(coefficients),
                "coefficients_sha256": hashlib.sha256(
                    payload.encode("ascii")
                ).hexdigest(),
            }
        )
    return {
        "depths_checked": len(rows) - 2,
        "positive_connection_coefficients": len(positive_coefficients),
        "first_non_path_term": {
            "depth": 3,
            "H_0_coefficient": str(
                sp.expand(
                    X * rows[3].as_expr() - rows[4].as_expr()
                    - sp.Rational(152, 3) * rows[2].as_expr()
                )
            ),
        }
        if len(rows) >= 5
        else None,
        "records": records,
    }


def isolating_intervals(polynomial: sp.Poly, decimal_digits: int):
    intervals = polynomial.intervals(
        eps=sp.Rational(1, 10**decimal_digits)
    )
    if len(intervals) != polynomial.degree():
        raise AssertionError("not all residual roots are real and distinct")
    if any(multiplicity != 1 for _, multiplicity in intervals):
        raise AssertionError("a residual root is not simple")
    if any(left <= 0 for (left, _), _ in intervals):
        raise AssertionError("a residual root is not positive")
    return intervals


def certify_interlacing(
    depth: int,
    current_intervals,
    next_intervals,
) -> str:
    """Certify strict interlacing by disjoint rational root intervals."""
    labelled = [
        (left, right, "d")
        for (left, right), _ in current_intervals
    ] + [
        (left, right, "d+1")
        for (left, right), _ in next_intervals
    ]
    labelled.sort(key=lambda item: item[0])
    for previous, following in zip(labelled, labelled[1:]):
        if previous[1] >= following[0]:
            raise AssertionError(
                "isolating intervals are not disjoint; increase precision"
            )

    labels = "".join("A" if item[2] == "d" else "B" for item in labelled)
    residual_degree = depth // 2
    if depth % 2 == 0:
        expected = "AB" * residual_degree
    else:
        expected = "B" + "AB" * residual_degree
    if labels != expected:
        raise AssertionError(
            f"residual roots do not interlace: {labels} != {expected}"
        )
    return labels


def favard_obstruction(rows: list[sp.Poly]) -> dict[str, str | int]:
    """Record the first failure of a monic three-term recurrence."""
    for depth in range(1, len(rows) - 1):
        current = rows[depth]
        following = rows[depth + 1]
        previous = rows[depth - 1]
        alpha = (
            current.coeff_monomial(K ** (depth - 1))
            - following.coeff_monomial(K**depth)
        )
        residual = sp.Poly(
            sp.expand(
                following.as_expr()
                - (K - alpha) * current.as_expr()
            ),
            K,
        )
        beta = -residual.coeff_monomial(K ** (depth - 1))
        obstruction = sp.Poly(
            sp.expand(
                residual.as_expr() + beta * previous.as_expr()
            ),
            K,
        )
        if not obstruction.is_zero:
            return {
                "first_failed_depth": depth,
                "alpha": str(alpha),
                "beta": str(beta),
                "nonzero_residual": str(sp.factor(obstruction.as_expr())),
            }
    return {"first_failed_depth": -1}


def audit(
    maximum_depth: int = 50,
    interval_decimal_digits: int = 12,
) -> dict[str, object]:
    rows = [sp.Poly(1, K)]
    matching_rows = [sp.Poly(1, X)]
    residual_intervals = {}
    poisson_intervals = {}
    records = []

    for depth in range(1, maximum_depth + 1):
        polynomial = ordinary_polynomial(depth)
        rows.append(polynomial)
        if polynomial.LC() != 1 or polynomial.degree() != depth:
            raise AssertionError("ordinary-symbol normalization failed")

        coefficients = polynomial.all_coeffs()
        if not all(
            (-1) ** rank * coefficient > 0
            for rank, coefficient in enumerate(coefficients)
        ):
            raise AssertionError("ordinary coefficients are not alternating")

        factor = forced_factor(depth)
        residual = reduced_polynomial(depth, polynomial)
        intervals = isolating_intervals(
            residual, interval_decimal_digits
        )
        residual_intervals[depth] = intervals

        # The forced roots are distinct positive integers.  The first
        # residual interval must lie strictly to their right.
        largest_forced_root = (depth + 1) // 2 + 1
        if intervals and intervals[0][0][0] <= largest_forced_root:
            raise AssertionError("forced and residual roots overlap")

        newton = falling_newton_coefficients(polynomial)
        first_nonzero = next(
            index for index, value in enumerate(newton) if value
        )
        if first_nonzero != factor.degree():
            raise AssertionError("unexpected falling-factor support")
        if not all(
            (-1) ** (depth - index) * newton[index] > 0
            for index in range(first_nonzero, depth + 1)
        ):
            raise AssertionError(
                "falling-factor coefficients are not alternating"
            )

        poisson_residual = poisson_newton_residual(depth, newton)
        matching_rows.append(matching_polynomial(depth, newton))
        poisson_root_intervals = isolating_intervals(
            poisson_residual, interval_decimal_digits
        )
        poisson_intervals[depth] = poisson_root_intervals

        interval_payload = ";".join(
            f"{left},{right}"
            for (left, right), _ in intervals
        )
        poisson_interval_payload = ";".join(
            f"{left},{right}"
            for (left, right), _ in poisson_root_intervals
        )
        records.append(
            {
                "depth": depth,
                "degree": polynomial.degree(),
                "forced_integer_roots": (
                    [2, largest_forced_root]
                    if factor.degree()
                    else []
                ),
                "forced_factor_degree": factor.degree(),
                "residual_degree": residual.degree(),
                "positive_simple_residual_roots": len(intervals),
                "positive_simple_poisson_residual_roots": len(
                    poisson_root_intervals
                ),
                "coefficient_sha256": coefficient_digest(polynomial),
                "residual_intervals_sha256": hashlib.sha256(
                    interval_payload.encode("ascii")
                ).hexdigest(),
                "poisson_residual_intervals_sha256": hashlib.sha256(
                    poisson_interval_payload.encode("ascii")
                ).hexdigest(),
            }
        )

    interlacing = []
    poisson_interlacing = []
    for depth in range(1, maximum_depth):
        labels = certify_interlacing(
            depth,
            residual_intervals[depth],
            residual_intervals[depth + 1],
        )
        interlacing.append(
            {
                "depth_pair": [depth, depth + 1],
                "exact_interval_order": labels,
            }
        )
        poisson_labels = certify_interlacing(
            depth,
            poisson_intervals[depth],
            poisson_intervals[depth + 1],
        )
        poisson_interlacing.append(
            {
                "depth_pair": [depth, depth + 1],
                "exact_interval_order": poisson_labels,
            }
        )

    return {
        "schema": "amra.opg1757.ordinary-real-rootedness-finite.v1",
        "scope": (
            "Finite exact reconstruction from normalized Lagrange profiles, "
            "with two unused interpolation holdouts per row. Positive simple "
            "roots and strict residual interlacing are certified by rational "
            "isolating intervals. This is not an all-depth proof."
        ),
        "maximum_depth": maximum_depth,
        "interval_decimal_digits": interval_decimal_digits,
        "ordinary_rows_checked": maximum_depth,
        "strict_coefficient_alternation_rows": maximum_depth,
        "positive_simple_root_rows": maximum_depth,
        "positive_simple_poisson_root_rows": maximum_depth,
        "strict_residual_interlacing_pairs": maximum_depth - 1,
        "strict_poisson_interlacing_pairs": maximum_depth - 1,
        "falling_basis_alternation_rows": maximum_depth,
        "favard_three_term_obstruction": favard_obstruction(rows),
        "matching_basis_recurrence": matching_basis_recurrence(
            matching_rows
        ),
        "records": records,
        "interlacing": interlacing,
        "poisson_interlacing": poisson_interlacing,
        "classification": {
            "finite_depth_at_most_maximum": "exactly_certified",
            "all_depth_real_rootedness": "open",
            "all_depth_residual_interlacing": "open",
            "all_depth_poisson_real_rootedness": "open",
            "all_depth_poisson_interlacing": "open",
            "weighted_C_equals_3_via_Maclaurin": (
                "conditional_on_all_depth_real_rootedness"
            ),
        },
        "status": "finite_exact_certificate_passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-depth", type=int, default=50)
    parser.add_argument("--interval-decimal-digits", type=int, default=12)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.maximum_depth, args.interval_decimal_digits),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
