#!/usr/bin/env python3
"""Certificates for the critical square-root bottom Newton window."""

from __future__ import annotations

import json
import math
from fractions import Fraction


WINDOW_DENOMINATOR = 2**28
WINDOW_K0 = 9*2**58


def parameters(k: int, depth: int) -> tuple[int, int, int]:
    """Return q0, N, R for the last Newton term."""

    if k < 2 or depth < 0:
        raise ValueError("need k >= 2 and nonnegative depth")
    q0 = (k-2)//2
    n = q0+4+depth
    excess = (1 if k % 2 else 2)+2*depth
    return q0, n, excess


def maximum_certified_depth(k: int) -> int:
    """floor(sqrt(k)/2^28), using exact integer arithmetic."""

    if k < 0:
        raise ValueError("k must be nonnegative")
    return math.isqrt(k)//WINDOW_DENOMINATOR


def exp_minus_one_upper(x: Fraction) -> Fraction:
    """The elementary upper bound exp(x)-1 <= x/(1-x)."""

    if x < 0 or x >= 1:
        raise ValueError("need 0 <= x < 1")
    return x/(1-x)


def window_certificate(k: int, depth: int) -> dict[str, object]:
    """Check the exact sufficient inequalities for Theorem 1."""

    if k < WINDOW_K0:
        raise ValueError("k is below the explicit theorem threshold")
    if depth > maximum_certified_depth(k):
        raise ValueError("depth is outside the certified window")
    _, n, excess = parameters(k, depth)
    heat_condition = n >= 2**52*(excess+1)**2
    x = Fraction((excess+1)**2, n)
    alternating_parameter = Fraction(excess*excess, n)
    error_upper = (
        Fraction(2**51*(excess+1)**2, n)
        +2*exp_minus_one_upper(alternating_parameter)
    )
    assert heat_condition
    assert x <= Fraction(1, 2**52)
    assert alternating_parameter <= x
    assert error_upper < 1
    return {
        "k": k,
        "depth": depth,
        "N": n,
        "R": excess,
        "heat_condition": heat_condition,
        "x": str(x),
        "relative_error_upper": str(error_upper),
        "positive": error_upper < 1,
    }


def main_term_ratio_exact(n: int, excess: int) -> Fraction:
    """Exact alternating ratio S_(N,R) from leading determinant terms."""

    if n < 5 or excess < 1:
        raise ValueError("need N >= 5 and R >= 1")
    total = Fraction(0)
    for ell in range((excess-1)//2+1):
        earlier_excess = excess-2*ell
        ratio = (
            Fraction(math.comb(n-4, ell))
            *Fraction(earlier_excess, excess)
            *Fraction(
                math.factorial(excess),
                math.factorial(earlier_excess),
            )
            *Fraction(
                (n-ell)**(2*(n-ell)-8),
                n**(2*n-8),
            )
        )
        total += (-1)**ell*ratio
    return total


def main_term_ratio_float(n: int, excess: int) -> float:
    """Stable floating evaluation of the same alternating ratio."""

    if n < 5 or excess < 1:
        raise ValueError("need N >= 5 and R >= 1")
    terms = []
    for ell in range((excess-1)//2+1):
        earlier_excess = excess-2*ell
        logarithm = (
            math.lgamma(n-3)
            -math.lgamma(ell+1)
            -math.lgamma(n-3-ell)
            +math.log(earlier_excess/excess)
            +math.lgamma(excess+1)
            -math.lgamma(earlier_excess+1)
            +(2*(n-ell)-8)*math.log(n-ell)
            -(2*n-8)*math.log(n)
        )
        terms.append(((-1)**ell)*math.exp(logarithm))
    return math.fsum(terms)


def predicted_main_scaling(n: int, excess: int) -> float:
    """exp(-e^-2 R^2/N)."""

    return math.exp(
        -Fraction(excess*excess, n)/math.e**2
    )


def determinant_relative_remainder_bound(
    n: int, excess: int
) -> Fraction:
    """Relative form of the existing determinant remainder (25)."""

    if n < 1 or excess < 1:
        raise ValueError("need positive N and R")
    return Fraction(
        2**48*(excess+1)**3,
        excess*n,
    )


def scaling_samples() -> list[dict[str, object]]:
    """Finite samples for the rigorous main-term scaling theorem."""

    samples = []
    for target_lambda in (Fraction(1, 4), Fraction(1), Fraction(4)):
        for n in (1000, 5000, 20000):
            excess = max(1, round(math.sqrt(float(target_lambda)*n)))
            if excess % 2 == 0:
                excess += 1
            value = main_term_ratio_float(n, excess)
            predicted = predicted_main_scaling(n, excess)
            samples.append({
                "target_lambda": str(target_lambda),
                "N": n,
                "R": excess,
                "actual_lambda": excess*excess/n,
                "main_term_ratio": value,
                "predicted": predicted,
                "absolute_error": abs(value-predicted),
            })
    return samples


def audit() -> dict[str, object]:
    boundary_cases = []
    for k in (
        WINDOW_K0,
        WINDOW_K0+1,
        4*WINDOW_K0,
        100*WINDOW_K0+1,
    ):
        depth = maximum_certified_depth(k)
        boundary_cases.append(window_certificate(k, depth))

    exact_checks = []
    for n in (20, 40, 80):
        for excess in (3, 5, 7):
            exact_value = main_term_ratio_exact(n, excess)
            float_value = main_term_ratio_float(n, excess)
            assert abs(float(exact_value)-float_value) < 1e-10
            exact_checks.append((n, excess))

    return {
        "schema": "amra.opg1757.critical-sqrt-bottom-window.v1",
        "verdict": "PASS",
        "explicit_c": "2^-28",
        "explicit_k0": WINDOW_K0,
        "boundary_certificates": boundary_cases,
        "exact_main_sum_checks": len(exact_checks),
        "main_term_scaling": "exp(-exp(-2)*R^2/N)",
        "tau_scaling": "exp(-8*exp(-2)*tau^2)",
        "determinant_remainder_barrier": (
            "2^48*(R+1)^3/(R*N), tending to 2^48*lambda"
        ),
        "scaling_samples": scaling_samples(),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
