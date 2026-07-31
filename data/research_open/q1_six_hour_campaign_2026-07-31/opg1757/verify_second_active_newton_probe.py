#!/usr/bin/env python3
"""Finite probe of the second active base-four Newton order.

This checks the exact B4/B2 and B5/B3 comparisons obtained from (3f) in
BASE4_NEWTON_GLOBAL_ATTACK.md.  It is finite evidence, not a universal
proof.
"""

from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

import sympy as sp


EIGHT_DIR = (
    Path(__file__).resolve().parents[2]
    / "q1_eight_hour_campaign_2026-07-29"
    / "opg1757"
)
sys.path.insert(0, str(EIGHT_DIR))
try:
    import fixed_page_union_formula as fixed  # type: ignore
    import five_page_union_formula as five  # type: ignore
finally:
    sys.path.pop(0)

BETA = fixed.BETA
Z = sp.symbols("z")


@lru_cache(maxsize=None)
def b2(s: int) -> sp.Expr:
    return sp.expand(
        4
        * BETA**4
        * (1 + 2 * BETA) ** (2 * s - 6)
        * (1 + s * BETA) ** (2 * s - 8)
    )


@lru_cache(maxsize=None)
def b3(s: int) -> sp.Expr:
    if s == 4:
        return 24 * BETA**6
    x = 1 + 3 * BETA
    z = 1 + 2 * BETA
    lam = 1 + s * BETA
    kernel = (
        1
        + 12 * BETA
        + (6 * s + 30) * BETA**2
        + 28 * s * BETA**3
        + 6 * s**2 * BETA**4
    )
    return sp.expand(
        12
        * BETA**4
        * lam ** (2 * s - 10)
        * (x ** (2 * s - 8) * kernel - z ** (2 * s - 6) * lam**2)
    )


def normalized_row(expression: sp.Expr, pages: int, s: int, q: int) -> sp.Expr:
    polynomial = sp.Poly(expression, BETA)
    return sp.expand(
        sum(
            sp.Rational(
                polynomial.coeff_monomial(BETA ** (2 * pages + offset)),
                sp.factorial(pages),
            )
            * sp.Integer(s) ** (-(2 * s - 8 - 2 * q + offset))
            * Z**offset
            for offset in range(2 * q + 1)
        )
    )


@lru_cache(maxsize=None)
def row_b2(s: int, q: int) -> sp.Expr:
    return normalized_row(b2(s), 2, s, q)


@lru_cache(maxsize=None)
def row_b3(s: int, q: int) -> sp.Expr:
    return normalized_row(b3(s), 3, s, q)


@lru_cache(maxsize=None)
def row_b4(s: int, q: int) -> sp.Expr:
    return normalized_row(fixed.b4_expression_at_s(s), 4, s, q)


@lru_cache(maxsize=None)
def row_b5(s: int, q: int) -> sp.Expr:
    return normalized_row(five.b5_expression_at_s(s), 5, s, q)


def reduced_second_active(s: int, odd: bool) -> sp.Poly:
    m = s - 5
    if odd:
        q = 2 * m + 1
        difference = row_b4(s, q) - (m + 1) * row_b2(s - 1, q)
        common_order = max(0, 2 * s - 12)
    else:
        q = 2 * m
        difference = row_b5(s, q) - (m + 1) * row_b3(s - 1, q)
        common_order = max(0, 2 * s - 14)
    reduced = sp.cancel(difference / (1 + Z) ** common_order)
    numerator, denominator = sp.fraction(reduced)
    if denominator != 1:
        raise AssertionError("claimed common (1+z) factor did not divide")
    return sp.Poly(sp.expand(numerator), Z)


def audit(maximum_s: int = 20) -> int:
    checked = 0
    for s in range(5, maximum_s + 1):
        m = s - 5
        odd_q = 2 * m + 1
        odd_difference = sp.Poly(
            row_b4(s, odd_q) - (m + 1) * row_b2(s - 1, odd_q),
            Z,
        )
        for difference in reversed(odd_difference.all_coeffs()):
            if difference <= 0:
                raise AssertionError(f"odd second-active failure at {s}")
            checked += 1

        if m == 0:
            continue
        even_q = 2 * m
        even_difference = sp.Poly(
            row_b5(s, even_q) - (m + 1) * row_b3(s - 1, even_q),
            Z,
        )
        for difference in reversed(even_difference.all_coeffs()):
            if difference <= 0:
                raise AssertionError(f"even second-active failure at {s}")
            checked += 1
    return checked


def audit_transport_recurrences(maximum_s: int = 20) -> int:
    odd_previous = reduced_second_active(6, odd=True)
    even_previous = reduced_second_active(6, odd=False)
    checked = 0
    for s in range(6, maximum_s):
        odd_next = reduced_second_active(s + 1, odd=True)
        even_next = reduced_second_active(s + 1, odd=False)
        odd_remainder = sp.Poly(
            sp.expand(
                odd_next.as_expr()
                - (s + 4 * Z) ** 2 * odd_previous.as_expr()
            ),
            Z,
        )
        even_remainder = sp.Poly(
            sp.expand(
                even_next.as_expr()
                - (s + 5 * Z) ** 2 * even_previous.as_expr()
            ),
            Z,
        )
        for label, remainder in (
            ("odd", odd_remainder),
            ("even", even_remainder),
        ):
            for coefficient_value in remainder.all_coeffs():
                if coefficient_value <= 0:
                    raise AssertionError(
                        f"{label} transport remainder failed at {s}"
                    )
                checked += 1
        odd_previous = odd_next
        even_previous = even_next
    return checked


def audit_odd_universal_kernel() -> tuple[int, int, int]:
    """Audit the fixed kernel and four top-coefficient certificates.

    This is a transcription check for the exact argument in
    SECOND_ACTIVE_NEWTON_RECURRENCE_ATTACK.md, not an interpolation in s.
    """

    n = sp.symbols("n", integer=True, nonnegative=True)
    u = n + 6 + 2 * Z
    v = n + 5 + 2 * Z
    m = 2 * n
    i_values = [
        (n + 7) * (2 * n**2 + 22 * n + 27),
        2 * (n**4 + 32 * n**3 + 601 * n**2 + 2130 * n + 1974),
        76 * n**4 + 1429 * n**3 + 15241 * n**2 + 42266 * n + 35086,
        4
        * (
            6 * n**5
            + 201 * n**4
            + 3462 * n**3
            + 25238 * n**2
            + 57629 * n
            + 42843
        ),
        2
        * (
            110 * n**5
            + 2828 * n**4
            + 36819 * n**3
            + 194748 * n**2
            + 371397 * n
            + 245175
        ),
        8
        * (
            3 * n**6
            + 115 * n**5
            + 2802 * n**4
            + 26849 * n**3
            + 107106 * n**2
            + 170502 * n
            + 98430
        ),
        2
        * (
            42 * n**6
            + 1795 * n**5
            + 24517 * n**4
            + 150304 * n**3
            + 439416 * n**2
            + 568736 * n
            + 279360
        ),
    ]
    d_values = [
        14,
        292,
        150 * n + 2743,
        8 * (242 * n + 1839),
        32 * (15 * n**2 + 357 * n + 1511),
        1024 * (3 * n**2 + 33 * n + 91),
        128 * (2 * n + 11) * (2 * n**2 + 22 * n + 61),
    ]
    q_values = [
        2 * (2 * n + 5),
        4 * (n**2 + 17 * n + 47),
        74 * n**2 + 646 * n + 1695,
        8 * (3 * n**3 + 76 * n**2 + 490 * n + 1145),
        4 * (49 * n**3 + 718 * n**2 + 3880 * n + 7819),
        8
        * (
            3 * n**4
            + 94 * n**3
            + 1020 * n**2
            + 4728 * n
            + 8044
        ),
        4
        * (
            21 * n**4
            + 440 * n**3
            + 3480 * n**2
            + 12320 * n
            + 16480
        ),
    ]
    j_i = sum(
        i_values[j] * (n + 6) ** (2 - j) * Z**j for j in range(7)
    )
    j_a = sum(
        (q_values[j] + 7 * d_values[j])
        * (n + 6) ** (2 - j)
        * Z**j
        for j in range(7)
    )
    kernel = sp.cancel(
        2 * u * j_i
        + sp.expand_func(sp.binomial(m + 2, 3)) * Z * j_a
        - 2 * (n + 2) * v**5 * (1 + Z) ** 2
    )
    kernel_monomials = 0
    for degree in range(8):
        numerator, denominator = sp.fraction(
            sp.cancel(sp.Poly(kernel, Z).coeff_monomial(Z**degree))
        )
        if any(value <= 0 for value in sp.Poly(numerator, n).all_coeffs()):
            raise AssertionError(f"odd fixed kernel failed at degree {degree}")
        if denominator.subs(n, 1) <= 0:
            raise AssertionError("odd fixed-kernel denominator is not positive")
        kernel_monomials += len(sp.Poly(numerator, n).all_coeffs())

    negative_parts = [
        96 * n - 128,
        96 * n**3 + 352 * n**2 - 384 * n - 2496,
        48 * n**5
        + 392 * n**4
        + 600 * n**3
        - 3488 * n**2
        - 14728 * n
        - 17064,
        48 * n**7
        + 584 * n**6
        + 2040 * n**5
        - 3888 * n**4
        - 51856 * n**3
        - 170648 * n**2
        - 264488 * n
        - 168240,
    ]
    x = sp.symbols("x", integer=True, nonnegative=True)
    shifted_monomials = 0
    for order, expression in enumerate(negative_parts):
        shifted = sp.Poly(sp.expand(expression.subs(n, x + order + 2)), x)
        if any(value <= 0 for value in shifted.all_coeffs()):
            raise AssertionError(f"top shift certificate failed at {order}")
        shifted_monomials += len(shifted.all_coeffs())

    boundary_values = [
        6676,
        117000,
        1947088,
        853360,
        23016212,
        551714560,
        3493752,
        150983432,
        5256031416,
        162813496168,
    ]
    if any(value <= 0 for value in boundary_values):
        raise AssertionError("top boundary certificate failed")
    return kernel_monomials, shifted_monomials, len(boundary_values)


if __name__ == "__main__":
    count = audit()
    recurrence_count = audit_transport_recurrences()
    kernel_count, top_shift_count, top_boundary_count = (
        audit_odd_universal_kernel()
    )
    print("OPG SECOND-ACTIVE NEWTON PROBE: PASS")
    print(f"positive_coefficients_through_q31: {count}")
    print(f"positive_transport_remainders_through_s20: {recurrence_count}")
    print(f"odd_kernel_positive_monomials: {kernel_count}")
    print(f"odd_top_shift_positive_monomials: {top_shift_count}")
    print(f"odd_top_positive_boundary_values: {top_boundary_count}")
    print("status: ODD_EXACT_CERTIFICATE_PENDING_INDEPENDENT_AUDIT")
    print("status_even_and_full_newton: FINITE_EVIDENCE_ONLY")
