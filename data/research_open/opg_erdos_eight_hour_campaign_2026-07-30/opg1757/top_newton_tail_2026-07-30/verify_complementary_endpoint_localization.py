#!/usr/bin/env python3
"""Exact checks for the complementary endpoint-localization lemma.

The checks start from the finite Lagrange sums.  They do not import a
stored saddle profile or any finite-rank interpolation.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction

import sympy as sp


V, X = sp.symbols("v x")
QVAR = 1 - X


def falling(value: int, length: int) -> int:
    if length < 0:
        return 0
    result = 1
    for offset in range(length):
        result *= value - offset
    return result


def lagrange_e(s: int, component: int, degree: int) -> Fraction:
    if degree < 0:
        return Fraction(0)
    return sum(
        (
            Fraction(
                (-1) ** index
                * falling(component, index)
                * s ** (degree - index),
                2**index
                * math.factorial(index)
                * math.factorial(degree - index),
            )
        )
        for index in range(degree + 1)
    )


def hypergeometric_s(s: int, left: int, right: int) -> Fraction:
    return sum(
        Fraction(
            falling(left, index) * falling(right, index) * (-1) ** index,
            math.factorial(index) * (2 * s) ** index,
        )
        for index in range(min(left, right) + 1)
    )


def complementary_coefficient(
    s: int,
    left: int,
    right: int,
) -> Fraction:
    """Return [u^right] exp(u)(1-u/(2s))^left."""
    return sum(
        Fraction(
            falling(left, index) * (-1) ** index,
            math.factorial(index)
            * (2 * s) ** index
            * math.factorial(right - index),
        )
        for index in range(min(left, right) + 1)
    )


def original_main(s: int, edge_count: int, shift: int) -> Fraction:
    complement = s - shift - edge_count
    difference = (
        lagrange_e(s, complement, edge_count)
        - lagrange_e(s, complement, edge_count - 1)
    )
    return Fraction(
        2**edge_count
        * math.factorial(edge_count)
        * falling(s - shift, edge_count),
        s ** (2 * edge_count),
    ) * difference


def complementary_main(
    s: int,
    edge_count: int,
    shift: int,
) -> Fraction:
    complement = s - shift - edge_count
    # Coefficient of e^u(1-u/(2s))^(J-1)(Q+a-u/2).
    first = (
        (complement + shift)
        * complementary_coefficient(
            s,
            edge_count - 1,
            complement,
        )
    )
    second = Fraction(0)
    if complement >= 1:
        second = Fraction(1, 2) * complementary_coefficient(
            s,
            edge_count - 1,
            complement - 1,
        )
    coefficient = first - second
    return (
        Fraction(
            math.factorial(s - shift) * 2**edge_count,
            s ** (edge_count + 1),
        )
        * coefficient
    )


def original_exceptional(s: int, edge_count: int) -> Fraction:
    return (
        Fraction(
            4
            * 2**edge_count
            * math.factorial(edge_count)
            * falling(s - 4, edge_count - 1),
            s ** (2 * edge_count),
        )
        * lagrange_e(
            s,
            s - edge_count - 3,
            edge_count - 1,
        )
    )


def complementary_exceptional(
    s: int,
    edge_count: int,
) -> Fraction:
    complement = s - edge_count - 3
    coefficient = complementary_coefficient(
        s,
        edge_count - 1,
        complement,
    )
    return Fraction(
        8
        * edge_count
        * math.factorial(s - 4)
        * 2 ** (edge_count - 1),
        s ** (edge_count + 1),
    ) * coefficient


def audit() -> dict[str, object]:
    hypergeometric_checks = 0
    main_checks = 0
    exceptional_checks = 0

    for s in (11, 14, 19, 23):
        for edge_count in range(1, s // 2 + 1):
            for shift in (0, 2, 4):
                complement = s - shift - edge_count
                if complement < 0:
                    continue
                value = hypergeometric_s(
                    s,
                    edge_count,
                    complement,
                )
                if value != hypergeometric_s(
                    s,
                    complement,
                    edge_count,
                ):
                    raise AssertionError("S symmetry failed")
                if (
                    value
                    != math.factorial(complement)
                    * complementary_coefficient(
                        s,
                        edge_count,
                        complement,
                    )
                ):
                    raise AssertionError(
                        "complementary coefficient identity failed"
                    )
                hypergeometric_checks += 1

                if (
                    original_main(s, edge_count, shift)
                    != complementary_main(s, edge_count, shift)
                ):
                    raise AssertionError(
                        "main complementary identity failed"
                    )
                main_checks += 1

            if s - edge_count - 3 >= 0:
                if (
                    original_exceptional(s, edge_count)
                    != complementary_exceptional(s, edge_count)
                ):
                    raise AssertionError(
                        "exceptional complementary identity failed"
                    )
                exceptional_checks += 1

    phase = (
        V
        + X * sp.log(1 - V / 2)
        - QVAR * sp.log(V)
    )
    stationary_factor = sp.factor(sp.diff(phase, V))
    target_factor = sp.factor(
        -(V - 1) * (V - 2 * QVAR)
        / (2 * V * (1 - V / 2))
    )
    if sp.simplify(stationary_factor - target_factor) != 0:
        raise AssertionError("stationary factorization failed")
    hessian = sp.simplify(sp.diff(phase, V, 2).subs(V, 1))
    if sp.simplify(hessian - (1 - 2 * X)) != 0:
        raise AssertionError("complementary Hessian failed")

    main_amplitude_checks = 0
    for shift in (0, 2, 4):
        amplitude = (
            V ** (shift - 1)
            * (QVAR - V / 2)
            / (1 - V / 2)
        )
        for derivative in range(7):
            endpoint_jet = sp.simplify(
                sp.diff(amplitude, V, derivative)
                .subs(V, 1)
                .subs(X, 1)
            )
            if endpoint_jet.has(sp.zoo, sp.nan):
                raise AssertionError("singular main endpoint jet")
            main_amplitude_checks += 1

    exceptional_amplitude = V**2 / (1 - V / 2)
    exceptional_amplitude_checks = 0
    for derivative in range(7):
        endpoint_jet = sp.simplify(
            sp.diff(exceptional_amplitude, V, derivative).subs(V, 1)
        )
        if endpoint_jet.has(sp.zoo, sp.nan):
            raise AssertionError("singular exceptional endpoint jet")
        exceptional_amplitude_checks += 1

    return {
        "schema": "amra.opg1757.complementary-endpoint.v1",
        "status": "PASS",
        "hypergeometric_checks": hypergeometric_checks,
        "main_profile_checks": main_checks,
        "exceptional_profile_checks": exceptional_checks,
        "stationary_points": ["1", "2*(1-x)"],
        "hessian_at_v_one": str(hessian),
        "main_endpoint_jet_checks": main_amplitude_checks,
        "exceptional_endpoint_jet_checks": (
            exceptional_amplitude_checks
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args()
    print(json.dumps(audit(), indent=args.indent, sort_keys=True))


if __name__ == "__main__":
    main()
