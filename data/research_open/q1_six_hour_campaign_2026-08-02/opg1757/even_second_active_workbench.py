#!/usr/bin/env python3
"""Exact workbench for the open even second-active Newton row.

The file records exact identities and finite route-selection probes.  Its
kernel recurrence is currently a conjecture; see EVEN_SECOND_ACTIVE_ATTACK.md
for the proof firewall.
"""

from __future__ import annotations

import argparse

import sympy as sp


BETA = sp.symbols("beta")
Z = sp.symbols("z")


def k3(s: int | sp.Expr) -> sp.Expr:
    b = BETA
    return (
        1
        + 12 * b
        + (6 * s + 30) * b**2
        + 28 * s * b**3
        + 6 * s**2 * b**4
    )


def k4(s: int | sp.Expr) -> sp.Expr:
    b = BETA
    return (
        1
        + 28 * b
        + (14 * s + 288) * b**2
        + (292 * s + 1264) * b**3
        + (75 * s**2 + 1918 * s + 2008) * b**4
        + (968 * s**2 + 4064 * s) * b**5
        + (160 * s**3 + 3072 * s**2) * b**6
        + 1024 * s**3 * b**7
        + 128 * s**4 * b**8
    )


def k5(s: int | sp.Expr) -> sp.Expr:
    b = BETA
    return (
        1
        + 48 * b
        + (24 * s + 960) * b**2
        + (980 * s + 10180) * b**3
        + (255 * s**2 + 15840 * s + 60045) * b**4
        + (8340 * s**2 + 126036 * s + 186420) * b**5
        + (
            1480 * s**3
            + 100240 * s**2
            + 494158 * s
            + 238210
        )
        * b**6
        + (35640 * s**3 + 528024 * s**2 + 766380 * s) * b**7
        + (4755 * s**4 + 283440 * s**3 + 1034550 * s**2) * b**8
        + (76300 * s**4 + 749000 * s**3) * b**9
        + (8250 * s**5 + 306750 * s**4) * b**10
        + 67500 * s**5 * b**11
        + 6250 * s**6 * b**12
    )


def f5(s: int) -> sp.Poly:
    b = BETA
    expression = (
        (1 + 5 * b) ** (2 * s - 12) * k5(s)
        - 3 * (1 + s * b) ** 2 * (1 + 4 * b) ** (2 * s - 10) * k4(s)
        + 3 * (1 + s * b) ** 4 * (1 + 3 * b) ** (2 * s - 8) * k3(s)
        - (1 + s * b) ** 6 * (1 + 2 * b) ** (2 * s - 6)
    )
    return sp.Poly(sp.expand(expression), b)


def j3(s: int) -> sp.Poly:
    b = BETA
    expression = (
        (1 + 3 * b) ** (2 * s - 8) * k3(s)
        - (1 + 2 * b) ** (2 * s - 6) * (1 + s * b) ** 2
    )
    return sp.Poly(sp.expand(expression), b)


def comparison_kernel(s: int) -> sp.Poly:
    """The sufficient bulk kernel K_s from the exact two-term row."""

    if s < 7:
        raise ValueError("the stable even kernel starts at s=7")
    u = s - 1
    expression = (
        f5(s).as_expr() / (3 * BETA**6)
        - 2
        * (s - 4)
        * u**2
        * (1 + u * BETA) ** 2
        * j3(u).as_expr()
        / BETA**2
    )
    result = sp.cancel(expression)
    numerator, denominator = sp.fraction(result)
    if denominator != 1:
        raise AssertionError("comparison kernel retained a denominator")
    return sp.Poly(sp.expand(numerator), BETA)


def even_h(s: int) -> sp.Poly:
    """Reduced even second-active row for s>=7."""

    if s < 7:
        raise ValueError("use the direct boundary formula at s=6")
    u = s - 1
    p5 = sp.cancel(f5(s).as_expr() / BETA**6)
    p3 = sp.cancel(j3(u).as_expr() / BETA**2)
    endpoint = sp.Rational(1, 3) * s ** (2 * s - 12) * p5.subs(
        BETA, Z / s
    )
    boundary = (
        2
        * (s - 4)
        * u ** (2 * s - 10)
        * (1 + Z) ** 2
        * p3.subs(BETA, Z / u)
    )
    return sp.Poly(sp.expand(endpoint - boundary), Z)


def kernel_remainder(s: int) -> sp.Poly:
    return sp.Poly(
        sp.expand(
            comparison_kernel(s + 1).as_expr()
            - (1 + 5 * BETA) ** 2 * comparison_kernel(s).as_expr()
        ),
        BETA,
    )


def even_transport(s: int) -> sp.Poly:
    return sp.Poly(
        sp.expand(
            even_h(s + 1).as_expr()
            - (s + 5 * Z) ** 2 * even_h(s).as_expr()
        ),
        Z,
    )


def second_transport(s: int) -> sp.Poly:
    return sp.Poly(
        sp.expand(
            even_transport(s + 1).as_expr()
            - s**2 * even_transport(s).as_expr()
        ),
        Z,
    )


def scan(maximum_s: int = 35) -> dict[str, int]:
    kernel_coefficients = kernel_remainder_coefficients = 0
    first_transport_coefficients = second_transport_coefficients = 0
    for s in range(7, maximum_s + 1):
        kernel = comparison_kernel(s)
        if any(value <= 0 for value in kernel.all_coeffs()):
            raise AssertionError(f"comparison kernel failed at s={s}")
        kernel_coefficients += len(kernel.all_coeffs())
        if s < maximum_s:
            remainder = kernel_remainder(s)
            if any(value <= 0 for value in remainder.all_coeffs()):
                raise AssertionError(f"kernel recurrence failed at s={s}")
            kernel_remainder_coefficients += len(remainder.all_coeffs())

            transport = even_transport(s)
            if any(value <= 0 for value in transport.all_coeffs()):
                raise AssertionError(f"even transport failed at s={s}")
            first_transport_coefficients += len(transport.all_coeffs())
        if s < maximum_s - 1:
            second = second_transport(s)
            if any(value <= 0 for value in second.all_coeffs()):
                raise AssertionError(f"second transport failed at s={s}")
            second_transport_coefficients += len(second.all_coeffs())
    return {
        "comparison_kernel_coefficients": kernel_coefficients,
        "kernel_recurrence_coefficients": kernel_remainder_coefficients,
        "even_transport_coefficients": first_transport_coefficients,
        "second_transport_coefficients": second_transport_coefficients,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-s", type=int, default=35)
    args = parser.parse_args()
    result = scan(args.maximum_s)
    print("OPG EVEN SECOND-ACTIVE WORKBENCH: FINITE PASS")
    for name, value in result.items():
        print(f"{name}: {value}")
    print("status: KERNEL_RECURRENCE_AND_EVEN_THEOREM_OPEN")
