#!/usr/bin/env python3
"""Independent symbolic audit of odd second-active Newton positivity.

This file imports no previous campaign module.  It reconstructs the B4
kernel certificate, the four exceptional top coefficients, the two base
rows, and a finite recurrence sanity range.  The universal induction is
written in ODD_SECOND_ACTIVE_INDEPENDENT_AUDIT.md.
"""

from __future__ import annotations

import sympy as sp


N = sp.symbols("n", integer=True, positive=True)
Z = sp.symbols("z")
BETA = sp.symbols("beta")


def kernel_data(n: sp.Expr) -> tuple[list[sp.Expr], list[sp.Expr], list[sp.Expr]]:
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
    return i_values, d_values, q_values


def fixed_kernel() -> sp.Expr:
    i_values, d_values, q_values = kernel_data(N)
    u = N + 6 + 2 * Z
    v = N + 5 + 2 * Z
    j_i = sum(
        i_values[j] * (N + 6) ** (2 - j) * Z**j
        for j in range(7)
    )
    j_a = sum(
        (q_values[j] + 7 * d_values[j])
        * (N + 6) ** (2 - j)
        * Z**j
        for j in range(7)
    )
    return sp.cancel(
        2 * u * j_i
        + sp.expand_func(sp.binomial(2 * N + 2, 3)) * Z * j_a
        - 2 * (N + 2) * v**5 * (1 + Z) ** 2
    )


def audit_fixed_kernel() -> int:
    kernel = sp.Poly(fixed_kernel(), Z)
    checked = 0
    for degree in range(8):
        numerator, denominator = sp.fraction(
            sp.cancel(kernel.coeff_monomial(Z**degree))
        )
        numerator_poly = sp.Poly(numerator, N)
        if any(value <= 0 for value in numerator_poly.all_coeffs()):
            raise AssertionError(f"kernel numerator failed at z^{degree}")
        denominator_poly = sp.Poly(denominator, N)
        if any(value < 0 for value in denominator_poly.all_coeffs()):
            raise AssertionError(f"kernel denominator failed at z^{degree}")
        if denominator.subs(N, 1) <= 0:
            raise AssertionError(f"kernel denominator vanished at z^{degree}")
        checked += len(numerator_poly.all_coeffs())
    return checked


def k3_coefficients(s: sp.Expr) -> list[sp.Expr]:
    return [1, 12, 6 * s + 30, 28 * s, 6 * s**2]


def k4_coefficients(s: sp.Expr) -> list[sp.Expr]:
    return [
        1,
        28,
        14 * s + 288,
        292 * s + 1264,
        75 * s**2 + 1918 * s + 2008,
        968 * s**2 + 4064 * s,
        160 * s**3 + 3072 * s**2,
        1024 * s**3,
        128 * s**4,
    ]


def top_l_coefficient(n: sp.Expr, deficiency: int) -> sp.Expr:
    """Coefficient deficiency positions below the top of L_(n+5)."""

    s = n + 5
    m = 2 * n
    k3 = k3_coefficients(s)
    k4 = k4_coefficients(s)
    answer = sp.Integer(0)

    # (1+4b)^m K4: distribute the top deficiency between both factors.
    for first in range(deficiency + 1):
        second = deficiency - first
        if second <= 8:
            answer += (
                sp.binomial(m, first)
                * 4 ** (m - first)
                * k4[8 - second]
            )

    # -2(1+sb)^2(1+3b)^(m+2)K3.
    for first in range(min(2, deficiency) + 1):
        for second in range(deficiency - first + 1):
            third = deficiency - first - second
            if third <= 4:
                answer -= (
                    2
                    * sp.binomial(2, first)
                    * s ** (2 - first)
                    * sp.binomial(m + 2, second)
                    * 3 ** (m + 2 - second)
                    * k3[4 - third]
                )

    # +(1+sb)^4(1+2b)^(m+4).
    for first in range(min(4, deficiency) + 1):
        second = deficiency - first
        answer += (
            sp.binomial(4, first)
            * s ** (4 - first)
            * sp.binomial(m + 4, second)
            * 2 ** (m + 4 - second)
        )
    return sp.simplify(sp.expand_func(answer))


def top_h_coefficient(n: sp.Expr, deficiency: int) -> sp.Expr:
    """Top-reversed coefficient of H_(n+5)^o."""

    s = n + 5
    m = 2 * n
    endpoint_part = sp.cancel(
        top_l_coefficient(n, deficiency) * s ** (deficiency - 4)
    )
    boundary_part = sp.Integer(0)
    for second_deficiency in range(min(2, deficiency) + 1):
        first_deficiency = deficiency - second_deficiency
        boundary_part += (
            sp.binomial(2, second_deficiency)
            * sp.binomial(m + 2, first_deficiency)
            * (s - 1) ** first_deficiency
            * 2 ** (m + 2 - first_deficiency)
        )
    boundary_part *= 2 * (s - 4)
    return sp.simplify(sp.expand_func(endpoint_part - boundary_part))


def calculated_top_remainder(deficiency: int) -> sp.Expr:
    s = N + 5
    answer = top_h_coefficient(N + 1, deficiency)
    answer -= 16 * top_h_coefficient(N, deficiency)
    if deficiency >= 1:
        answer -= 8 * s * top_h_coefficient(N, deficiency - 1)
    if deficiency >= 2:
        answer -= s**2 * top_h_coefficient(N, deficiency - 2)
    return sp.simplify(sp.powdenest(sp.expand_func(answer), force=True))


def claimed_top_remainders() -> list[sp.Expr]:
    n = N
    return [
        4**n * (96 * n - 128) + 756 * 9**n,
        16**n * (1024 * n + 1024)
        + 4**n * (96 * n**3 + 352 * n**2 - 384 * n - 2496)
        + 9**n * (504 * n**2 + 2592 * n + 7344),
        16**n
        * (512 * n**3 + 3584 * n**2 + 12672 * n + 12160)
        + 4**n
        * (
            48 * n**5
            + 392 * n**4
            + 600 * n**3
            - 3488 * n**2
            - 14728 * n
            - 17064
        )
        + 9**n
        * (
            168 * n**4
            + 1644 * n**3
            + 7860 * n**2
            + 20604 * n
            + 28332
        ),
        sp.Rational(1, 3)
        * (
            16**n
            * (
                384 * n**5
                + 4800 * n**4
                + 30464 * n**3
                + 113280 * n**2
                + 236992 * n
                + 196224
            )
            + 4**n
            * (
                48 * n**7
                + 584 * n**6
                + 2040 * n**5
                - 3888 * n**4
                - 51856 * n**3
                - 170648 * n**2
                - 264488 * n
                - 168240
            )
            + 9**n
            * (
                112 * n**6
                + 1560 * n**5
                + 10016 * n**4
                + 38648 * n**3
                + 95904 * n**2
                + 149872 * n
                + 125304
            )
        ),
    ]


def audit_top_remainders() -> tuple[int, int, int]:
    claims = claimed_top_remainders()
    for deficiency, claim in enumerate(claims):
        difference = calculated_top_remainder(deficiency) - claim
        # Canonicalize the three exponential bases before polynomial
        # simplification.  SymPy intentionally does not always identify
        # a^(2*n) with (a^2)^n under a symbolic exponent automatically.
        difference = difference.xreplace(
            {
                2 ** (2 * N): 4**N,
                2 ** (4 * N): 16**N,
                3 ** (2 * N): 9**N,
            }
        )
        difference = sp.expand(difference)
        if difference != 0:
            raise AssertionError(
                f"top recurrence identity failed at deficiency {deficiency}"
            )

    possibly_negative = [
        96 * N - 128,
        96 * N**3 + 352 * N**2 - 384 * N - 2496,
        48 * N**5
        + 392 * N**4
        + 600 * N**3
        - 3488 * N**2
        - 14728 * N
        - 17064,
        48 * N**7
        + 584 * N**6
        + 2040 * N**5
        - 3888 * N**4
        - 51856 * N**3
        - 170648 * N**2
        - 264488 * N
        - 168240,
    ]
    x = sp.symbols("x", integer=True, nonnegative=True)
    shifted_terms = 0
    for deficiency, expression in enumerate(possibly_negative):
        shifted = sp.Poly(
            sp.expand(expression.subs(N, x + deficiency + 2)), x
        )
        if any(value <= 0 for value in shifted.all_coeffs()):
            raise AssertionError(
                f"shifted top polynomial failed at {deficiency}"
            )
        shifted_terms += len(shifted.all_coeffs())

    exceptional_values = 0
    for deficiency, claim in enumerate(claims):
        for n_value in range(1, deficiency + 2):
            if claim.subs(N, n_value) <= 0:
                raise AssertionError(
                    f"top boundary failed at {(deficiency, n_value)}"
                )
            exceptional_values += 1
    return len(claims), shifted_terms, exceptional_values


def l_polynomial(s: int) -> sp.Expr:
    m = 2 * s - 10
    k3 = sum(
        value * BETA**degree
        for degree, value in enumerate(k3_coefficients(s))
    )
    k4 = sum(
        value * BETA**degree
        for degree, value in enumerate(k4_coefficients(s))
    )
    return sp.expand(
        (1 + 4 * BETA) ** m * k4
        - 2 * (1 + s * BETA) ** 2 * (1 + 3 * BETA) ** (m + 2) * k3
        + (1 + s * BETA) ** 4 * (1 + 2 * BETA) ** (m + 4)
    )


def h_polynomial(s: int) -> sp.Poly:
    m = 2 * s - 10
    p = sp.cancel(l_polynomial(s) / BETA**4)
    endpoint_part = sp.expand(s**m * p.subs(BETA, Z / s))
    boundary_part = (
        2
        * (s - 4)
        * (s - 1 + 2 * Z) ** (m + 2)
        * (1 + Z) ** 2
    )
    return sp.Poly(sp.expand(endpoint_part - boundary_part), Z)


def audit_bases_and_finite_recurrence(maximum_s: int = 12) -> int:
    expected_five = sp.Poly(52 + 64 * Z + 28 * Z**2, Z)
    expected_six = sp.Poly(
        14132
        + 50328 * Z
        + 76976 * Z**2
        + 65104 * Z**3
        + 32256 * Z**4
        + 8912 * Z**5
        + 1076 * Z**6,
        Z,
    )
    # At s=5 the common (1+z) exponent in the homogenized B4 formula is
    # negative, so A_s-Q_s is not the natural-support row.  Reconstruct
    # q=1 directly from its three exact normalized layer polynomials.
    s_value = 5
    base_value = 4
    q_one = [
        lambda value: 4 * (value**2 + 4 * value - 24),
        lambda value: 8 * (value**2 - value - 8),
        lambda value: 4 * (value - 2) * (2 * value - 7),
    ]
    direct_five = sp.Poly(
        sum(
            (expression(s_value) - expression(base_value)) * Z**degree
            for degree, expression in enumerate(q_one)
        ),
        Z,
    )
    if direct_five != expected_five:
        raise AssertionError("H_5 direct base row mismatch")
    if h_polynomial(6) != expected_six:
        raise AssertionError("H_6 base row mismatch")

    checked = len(expected_five.all_coeffs()) + len(expected_six.all_coeffs())
    previous = expected_six
    for s in range(6, maximum_s):
        following = h_polynomial(s + 1)
        remainder = sp.Poly(
            sp.expand(
                following.as_expr() - (s + 4 * Z) ** 2 * previous.as_expr()
            ),
            Z,
        )
        if any(value <= 0 for value in remainder.all_coeffs()):
            raise AssertionError(f"finite odd recurrence failed at s={s}")
        checked += len(remainder.all_coeffs())
        previous = following
    return checked


def run_certificate() -> dict[str, int | tuple[int, int, int]]:
    return {
        "fixed_kernel_positive_monomials": audit_fixed_kernel(),
        "top_identity_shift_boundary": audit_top_remainders(),
        "base_and_finite_recurrence_coefficients": (
            audit_bases_and_finite_recurrence()
        ),
    }


if __name__ == "__main__":
    result = run_certificate()
    print("OPG ODD SECOND-ACTIVE INDEPENDENT CERTIFICATE: PASS")
    for name, value in result.items():
        print(f"{name}: {value}")
