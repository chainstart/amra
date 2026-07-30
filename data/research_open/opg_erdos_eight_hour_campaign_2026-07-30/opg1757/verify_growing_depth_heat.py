#!/usr/bin/env python3
"""Symbolic checks for the growing-depth heat-operator attack.

The script works only with truncated formal series in u=1/n.  It derives
the normalized component OGFs from the exact Gaussian representation,
applies the edge-orbit identities, and extracts the determinant kernel.
It also compares the heat coefficients with exact Liu--Chow counts.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from functools import lru_cache

import sympy as sp


U, Y, Z, S, R = sp.symbols("u y z s R")


def truncate(expression: sp.Expr, order: int) -> sp.Expr:
    """Return the u-series through u**order."""
    return sp.series(expression, U, 0, order + 1).removeO().expand()


def tilted_gaussian_moment(power: int) -> sp.Expr:
    """Return E[Y**power exp(Y)] / exp(z/2)."""
    mgf = sp.exp(Z * S - Z * S**2 / 2)
    value = sp.diff(mgf, S, power).subs(S, 1) / sp.exp(Z / 2)
    return sp.expand(value)


def tilted_expectation(polynomial: sp.Expr) -> sp.Expr:
    """Apply P(Y) -> E[P(Y) exp(Y)] / exp(z/2)."""
    polynomial = sp.Poly(sp.expand(polynomial), Y)
    return sp.expand(
        sum(
            coefficient * tilted_gaussian_moment(power[0])
            for power, coefficient in polynomial.terms()
        )
    )


def binomial_power_correction(b: int, order: int) -> sp.Expr:
    """Series of (1+uY)**(1/u-b) / exp(Y)."""
    logarithm = sum(
        (-1) ** j
        * U**j
        * (Y ** (j + 1) / (j + 1) + b * Y**j / j)
        for j in range(1, order + 1)
    )
    return truncate(sp.exp(logarithm), order)


def normalized_component_ogf(
    b: int, prefactor: sp.Expr, order: int
) -> sp.Expr:
    """Return G/e**(z/2) through u**order."""
    correction = binomial_power_correction(b, order)
    return truncate(
        sum(
            U**j
            * tilted_expectation(
                prefactor * sp.expand(correction).coeff(U, j)
            )
            for j in range(order + 1)
        ),
        order,
    )


def theta_on_half_exponential(polynomial: sp.Expr) -> sp.Expr:
    """Conjugated action e^(-z/2) theta e^(z/2)."""
    return sp.expand(Z * sp.diff(polynomial, Z) + Z * polynomial / 2)


def determinant_kernel(order: int) -> dict[str, sp.Expr]:
    """Return normalized OGF factors and exp(-z) determinant kernel."""
    g0 = normalized_component_ogf(2, 1 + Y, order)
    adjacent = normalized_component_ogf(4, 3 + Y, order)
    theta_g0 = theta_on_half_exponential(g0)
    theta2_g0 = theta_on_half_exponential(theta_g0)

    # e^(-z/2) B1 and e^(-z/2) B2.  Here component c is 1+theta.
    b1 = truncate(
        2 * (g0 - U * (g0 + theta_g0)) / (1 - U),
        order,
    )
    first = (
        g0
        - U * (3 * g0 + 2 * theta_g0)
        + U**2 * (2 * g0 + 3 * theta_g0 + theta2_g0)
    )
    b2 = truncate(
        (
            4 * first
            - 4 * U * (1 - U) * (1 - 2 * U) * adjacent
        )
        / ((1 - U) * (1 - 2 * U) * (1 - 3 * U)),
        order,
    )
    kernel = truncate(b1**2 - g0 * b2, order)
    return {
        "g0": sp.collect(g0, U),
        "adjacent": sp.collect(adjacent, U),
        "b1": sp.collect(b1, U),
        "b2": sp.collect(b2, U),
        "kernel": sp.collect(kernel, U),
    }


@lru_cache(maxsize=None)
def liu_chow_normalized(n: int, components: int) -> Fraction:
    """W0,c / n**(n-2), directly from the finite Liu--Chow sum."""
    total = Fraction(0)
    for j in range(components):
        product = math.prod(
            Fraction(n - ell, n)
            for ell in range(1, components + j)
        )
        total += (
            Fraction((-1) ** j * (components + j), 2**j)
            * product
            / (
                math.factorial(j)
                * math.factorial(components - j - 1)
            )
        )
    return total


@lru_cache(maxsize=None)
def adjacent_normalized(n: int, components: int) -> Fraction:
    """A_c / n**(n-4), directly from the contraction sum."""
    total = Fraction(0)
    for j in range(components):
        product = math.prod(
            Fraction(n - ell, n)
            for ell in range(3, components + j + 2)
        )
        total += (
            Fraction(
                (-1) ** j * (components + j + 2),
                2**j,
            )
            * product
            / (
                math.factorial(j)
                * math.factorial(components - j - 1)
            )
        )
    return total


@lru_cache(maxsize=None)
def orbit_normalized(
    n: int, components: int
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Return W0/n^(n-2), A/n^(n-4), W1/n^(n-3), W2/n^(n-4)."""
    u = Fraction(1, n)
    w0 = liu_chow_normalized(n, components)
    adjacent = adjacent_normalized(n, components)
    w1 = 2 * (1 - components * u) * w0 / (1 - u)
    w2 = (
        4
        * (1 - components * u)
        * (1 - (components + 1) * u)
        * w0
        - 4 * u * (1 - u) * (1 - 2 * u) * adjacent
    ) / ((1 - u) * (1 - 2 * u) * (1 - 3 * u))
    return w0, adjacent, w1, w2


@lru_cache(maxsize=None)
def exact_normalized_determinant(
    n: int, total_components: int
) -> Fraction:
    """Return C_t(n)/n**(2n-6) from exact normalized component counts."""
    total = Fraction(0)
    for left in range(1, total_components):
        right = total_components - left
        w0_left, _, w1_left, _ = orbit_normalized(n, left)
        _, _, w1_right, w2_right = orbit_normalized(n, right)
        total += w1_left * w1_right - w0_left * w2_right
    return total


def exact_determinant(n: int, total_components: int) -> int:
    """Return the integer C_t(n)."""
    value = (
        exact_normalized_determinant(n, total_components)
        * n ** (2 * n - 6)
    )
    if value.denominator != 1:
        raise AssertionError((n, total_components, value))
    return value.numerator


def exact_newton_sum(k: int, depth: int) -> int:
    """Return 2*a_(k,q0+depth)/(k-2)! from exact determinants."""
    q0 = (k - 2) // 2
    n0 = q0 + 4
    total0 = 3 if k % 2 else 4
    return sum(
        (-1) ** (depth - index)
        * math.comb(q0 + depth, depth - index)
        * exact_determinant(n0 + index, total0 + 2 * index)
        for index in range(depth + 1)
    )


def kernel_coefficient(
    kernel: sp.Expr, n: int, total_components: int
) -> Fraction:
    """Return [z**(t-2)] e**z kernel(z,1/n)."""
    degree = total_components - 2
    expression = (
        sp.exp(Z) * kernel.subs(U, Fraction(1, n))
    ).series(Z, 0, degree + 1).removeO().expand()
    value = sp.cancel(expression.coeff(Z, degree))
    return Fraction(int(sp.numer(value)), int(sp.denom(value)))


def diagonal_polynomial(kernel_coefficient: sp.Expr) -> sp.Expr:
    """Return R! [z**R] exp(z) kernel_coefficient(z)."""
    polynomial = sp.Poly(sp.expand(kernel_coefficient), Z)
    result = 0
    for (degree,), coefficient in polynomial.terms():
        falling = sp.prod(R - index for index in range(degree))
        result += coefficient * falling
    return sp.factor(result)


def coefficient_from_series(
    normalized_ogf: sp.Expr, n: int, components: int
) -> Fraction:
    """Evaluate [z**(c-1)] of a truncated normalized OGF."""
    value = sp.expand(
        sp.exp(Z / 2) * normalized_ogf
    ).series(Z, 0, components).removeO().coeff(Z, components - 1)
    value = sp.cancel(value.subs(U, Fraction(1, n)))
    return Fraction(int(sp.numer(value)), int(sp.denom(value)))


def audit(order: int = 6) -> dict[str, object]:
    rows = determinant_kernel(order)
    kernel_coefficients = {
        str(j): str(sp.factor(rows["kernel"].coeff(U, j)))
        for j in range(order + 1)
    }
    diagonal_polynomials = {
        str(j): str(
            diagonal_polynomial(rows["kernel"].coeff(U, j))
        )
        for j in range(order + 1)
    }
    if rows["kernel"].coeff(U, 0) != 0:
        raise AssertionError("determinant has a nonzero constant term")
    if rows["kernel"].coeff(U, 1) != 0:
        raise AssertionError("determinant has a nonzero linear term")
    if sp.expand(rows["kernel"].coeff(U, 2) - 4 * Z) != 0:
        raise AssertionError("wrong leading determinant kernel")
    if sp.expand(rows["kernel"].coeff(U, 3) - 16 * Z**2) != 0:
        raise AssertionError("wrong second determinant kernel")
    for degree in range(2, order + 1):
        polynomial = sp.Poly(
            diagonal_polynomial(rows["kernel"].coeff(U, degree)),
            R,
        )
        if polynomial.degree() != degree - 1:
            raise AssertionError((degree, polynomial))
        expected_leading = sp.Rational(
            2 * degree * (degree**2 - 1), 3
        )
        if polynomial.LC() != expected_leading:
            raise AssertionError(
                (degree, polynomial.LC(), expected_leading)
            )

    # The z**r coefficient has u-degree at most 2r.  Thus the truncated
    # series reproduces the exact count whenever 2(c-1) <= order.
    exact_checks = []
    for n in range(8, 15):
        for components in range(
            1, min(order // 2 + 1, n) + 1
        ):
            got0 = coefficient_from_series(
                rows["g0"], n, components
            )
            want0 = liu_chow_normalized(n, components)
            gota = coefficient_from_series(
                rows["adjacent"], n, components
            )
            wanta = adjacent_normalized(n, components)
            if got0 != want0 or gota != wanta:
                raise AssertionError(
                    (n, components, got0, want0, gota, wanta)
                )
            exact_checks.append((n, components))

    determinant_samples = []
    for n, total_components in ((24, 5), (32, 7), (48, 9)):
        exact = exact_normalized_determinant(n, total_components)
        approximation = kernel_coefficient(
            rows["kernel"], n, total_components
        )
        relative_error = abs(exact - approximation) / exact
        determinant_samples.append(
            {
                "n": n,
                "total_components": total_components,
                "exact": str(exact),
                "truncated": str(approximation),
                "relative_error": str(relative_error),
            }
        )

    return {
        "schema": "amra.opg1757.growing-depth-heat.v1",
        "order": order,
        "scope": (
            "Formal heat/Gaussian derivation and exact coefficient checks; "
            "not a proof of a uniform analytic remainder."
        ),
        "kernel_coefficients": kernel_coefficients,
        "diagonal_polynomials": diagonal_polynomials,
        "exact_count_checks": len(exact_checks),
        "determinant_samples": determinant_samples,
    }


def stress_audit(maximum_k: int = 60) -> dict[str, object]:
    """Independent exact-integer sign stress test (not part of the proof)."""
    if maximum_k < 8:
        raise ValueError("maximum_k must be at least eight")
    checks = []
    minimum_ratio = None
    minimum_case = None
    for k in range(8, maximum_k + 1):
        maximum_depth = min(6, math.isqrt(k))
        for depth in range(maximum_depth + 1):
            value = exact_newton_sum(k, depth)
            if value <= 0:
                raise AssertionError(("nonpositive", k, depth, value))
            q0 = (k - 2) // 2
            n = q0 + 4 + depth
            total = (3 if k % 2 else 4) + 2 * depth
            main = Fraction(
                4 * n ** (2 * n - 8),
                math.factorial(total - 3),
            )
            ratio = Fraction(value, 1) / main
            if minimum_ratio is None or ratio < minimum_ratio:
                minimum_ratio = ratio
                minimum_case = (k, depth)
            checks.append((k, depth))
    return {
        "schema": "amra.opg1757.growing-depth-stress.v1",
        "scope": "Exact integer stress test; not a proof.",
        "maximum_k": maximum_k,
        "checked_newton_coefficients": len(checks),
        "minimum_ratio_to_endpoint_main": str(minimum_ratio),
        "minimum_ratio_case": minimum_case,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=6)
    parser.add_argument("--stress-maximum-k", type=int, default=0)
    args = parser.parse_args()
    report = audit(args.order)
    if args.stress_maximum_k:
        report["stress"] = stress_audit(args.stress_maximum_k)
    print(json.dumps(report, indent=2, sort_keys=True))
