#!/usr/bin/env python3
"""Exact certificates for the open even second-active Newton row.

This verifier proves two infinite boundary bands and records a structural
failure of one natural fixed-layer induction.  It does *not* prove the full
even row.  All polynomial identities use exact ``sympy`` arithmetic.
"""

from __future__ import annotations

from functools import cache
from math import factorial

import sympy as sp


BETA = sp.symbols("beta")
S = sp.symbols("s", integer=True)
N = sp.symbols("n", integer=True, nonnegative=True)
X = sp.symbols("x", integer=True, nonnegative=True)


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


def lambda_coefficients(power: int, s: sp.Expr) -> list[sp.Expr]:
    return [sp.binomial(power, j) * s**j for j in range(power + 1)]


def coefficients(expression: sp.Expr) -> list[sp.Expr]:
    polynomial = sp.Poly(sp.expand(expression), BETA)
    return [polynomial.coeff_monomial(BETA**j) for j in range(polynomial.degree() + 1)]


def convolution(left: list[sp.Expr], right: list[sp.Expr]) -> list[sp.Expr]:
    result = [sp.Integer(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return [sp.expand(value) for value in result]


@cache
def choose_fixed(top: sp.Expr, bottom: int) -> sp.Expr:
    """Polynomial version of binomial(top, bottom), for fixed bottom."""

    if bottom < 0:
        return sp.Integer(0)
    numerator = sp.sympify(sp.prod(top - j for j in range(bottom)))
    return sp.cancel(numerator / sp.Integer(factorial(bottom)))


def power_kernel_coefficient(
    base: int,
    exponent: sp.Expr,
    kernel: list[sp.Expr],
    degree: int,
) -> sp.Expr:
    value = sp.Integer(0)
    for i, entry in enumerate(kernel):
        power = degree - i
        if power >= 0:
            value += entry * sp.Integer(base) ** power * choose_fixed(exponent, power)
    return sp.expand(value)


@cache
def f_coefficient(degree: int) -> sp.Expr:
    """Return [beta^degree] F_s as a polynomial in symbolic S."""

    c5 = coefficients(k5(S))
    c4 = convolution(lambda_coefficients(2, S), coefficients(k4(S)))
    c3 = convolution(lambda_coefficients(4, S), coefficients(k3(S)))
    c2 = lambda_coefficients(6, S)
    return sp.expand(
        power_kernel_coefficient(5, 2 * S - 12, c5, degree)
        - 3 * power_kernel_coefficient(4, 2 * S - 10, c4, degree)
        + 3 * power_kernel_coefficient(3, 2 * S - 8, c3, degree)
        - power_kernel_coefficient(2, 2 * S - 6, c2, degree)
    )


@cache
def j_coefficient(s: sp.Expr, degree: int) -> sp.Expr:
    c3 = coefficients(k3(s))
    c2 = lambda_coefficients(2, s)
    return sp.expand(
        power_kernel_coefficient(3, 2 * s - 8, c3, degree)
        - power_kernel_coefficient(2, 2 * s - 6, c2, degree)
    )


@cache
def comparison_coefficient(degree: int) -> sp.Expr:
    """Return [beta^degree] K_s from the bulk comparison lemma."""

    u = S - 1
    boundary = (
        j_coefficient(u, degree + 2)
        + 2 * u * j_coefficient(u, degree + 1)
        + u**2 * j_coefficient(u, degree)
    )
    return sp.cancel(
        f_coefficient(degree + 6) / 3
        - 2 * (S - 4) * u**2 * boundary
    )


def f5_direct(s: int) -> sp.Poly:
    b = BETA
    expression = (
        (1 + 5 * b) ** (2 * s - 12) * k5(s)
        - 3 * (1 + s * b) ** 2 * (1 + 4 * b) ** (2 * s - 10) * k4(s)
        + 3 * (1 + s * b) ** 4 * (1 + 3 * b) ** (2 * s - 8) * k3(s)
        - (1 + s * b) ** 6 * (1 + 2 * b) ** (2 * s - 6)
    )
    return sp.Poly(sp.expand(expression), b)


def j3_direct(s: int) -> sp.Poly:
    b = BETA
    expression = (
        (1 + 3 * b) ** (2 * s - 8) * k3(s)
        - (1 + s * b) ** 2 * (1 + 2 * b) ** (2 * s - 6)
    )
    return sp.Poly(sp.expand(expression), b)


def comparison_direct(s: int) -> sp.Poly:
    u = s - 1
    expression = (
        f5_direct(s).as_expr() / (3 * BETA**6)
        - 2
        * (s - 4)
        * u**2
        * (1 + u * BETA) ** 2
        * j3_direct(u).as_expr()
        / BETA**2
    )
    return sp.Poly(sp.cancel(expression), BETA)


def certify_low_bulk_columns(maximum_degree: int = 30) -> dict[str, int]:
    positive_monomials = 0
    for degree in range(maximum_degree + 1):
        start = max(7, (degree + 7) // 2)
        shifted = sp.Poly(
            sp.expand(comparison_coefficient(degree).subs(S, X + start)), X
        )
        if any(value <= 0 for value in shifted.all_coeffs()):
            raise AssertionError(f"comparison column {degree} is not certified")
        positive_monomials += len(shifted.all_coeffs())

    # Independent direct convolutions check the coefficient transcription.
    crosschecks = 0
    for s in range(7, 13):
        direct = comparison_direct(s)
        for degree in range(maximum_degree + 1):
            expected = comparison_coefficient(degree).subs(S, s)
            actual = direct.coeff_monomial(BETA**degree)
            if sp.expand(expected - actual) != 0:
                raise AssertionError((s, degree, expected, actual))
            crosschecks += 1
    return {
        "universal_columns": maximum_degree + 1,
        "positive_shifted_monomials": positive_monomials,
        "direct_crosschecks": crosschecks,
    }


def top_component(
    base: int,
    exponent: sp.Expr,
    kernel: list[sp.Expr],
    total_degree: sp.Expr,
) -> sp.Expr:
    """Top coefficient after factoring out base**(2*S)."""

    value = sp.Integer(0)
    for i, entry in enumerate(kernel):
        complement = sp.simplify(exponent - (total_degree - i))
        if complement.is_Integer and complement >= 0:
            residual_power = sp.simplify(exponent - complement - 2 * S)
            if not residual_power.is_Integer:
                raise AssertionError(residual_power)
            value += (
                entry
                * choose_fixed(exponent, int(complement))
                * sp.Integer(base) ** int(residual_power)
            )
    return sp.expand(value)


def j_top_components(s: sp.Expr, total_degree: sp.Expr) -> dict[int, sp.Expr]:
    return {
        3: top_component(3, 2 * s - 8, coefficients(k3(s)), total_degree),
        2: -top_component(
            2,
            2 * s - 6,
            lambda_coefficients(2, s),
            total_degree,
        ),
    }


def top_row_components(offset: int) -> dict[int, sp.Expr]:
    """Represent [z^(2s-6-offset)] H_s as sum a^(2s) D_a(s)."""

    total = 2 * S - offset
    result = {
        5: top_component(5, 2 * S - 12, coefficients(k5(S)), total) / 3,
        4: -top_component(
            4,
            2 * S - 10,
            convolution(lambda_coefficients(2, S), coefficients(k4(S))),
            total,
        ),
        3: top_component(
            3,
            2 * S - 8,
            convolution(lambda_coefficients(4, S), coefficients(k3(S))),
            total,
        ),
        2: -top_component(
            2,
            2 * S - 6,
            lambda_coefficients(6, S),
            total,
        )
        / 3,
    }
    for base in result:
        result[base] = sp.cancel(result[base] * S ** (offset - 6))

    u = S - 1
    row_degree = 2 * S - 6 - offset
    for shift in range(3):
        j_parts = j_top_components(u, row_degree - shift + 2)
        multiplier = (
            -2
            * (S - 4)
            * sp.binomial(2, shift)
            * u ** (2 * S - 10 - (row_degree - shift))
        )
        for base, value in j_parts.items():
            result[base] = sp.cancel(result[base] + multiplier * value)
    return {base: sp.factor(sp.cancel(value)) for base, value in result.items()}


def top_polynomials(offset: int) -> dict[int, sp.Poly]:
    """Return P_a(n) with top coefficient = sum a^(2n) P_a(n)."""

    result = {}
    for base, value in top_row_components(offset).items():
        shifted = sp.expand(sp.expand_func((base**14 * value).subs(S, N + 7)))
        result[base] = sp.Poly(shifted, N)
    return result


def negative_envelope(parts: dict[int, sp.Poly]) -> sp.Poly:
    """Envelope all negative lower-base monomials by 16^n Q(n)."""

    expression = sp.Integer(0)
    for base in (4, 3, 2):
        for (degree,), coefficient in parts[base].terms():
            if coefficient < 0:
                expression -= coefficient * N**degree
    return sp.Poly(sp.expand(expression), N)


TOP_STARTS = (0, 0, 0, 1, 1, 2)


def certify_top_six() -> dict[str, int]:
    ratio_monomials = exceptional_values = direct_crosschecks = 0
    for offset, start in enumerate(TOP_STARTS):
        parts = top_polynomials(offset)
        positive = parts[5]
        envelope = negative_envelope(parts)
        if any(value <= 0 for value in positive.all_coeffs()):
            raise AssertionError((offset, "nonpositive 25-base polynomial"))
        if any(value <= 0 for value in envelope.all_coeffs()):
            raise AssertionError((offset, "nonpositive envelope"))

        cross = sp.Poly(
            sp.expand(
                25 * positive.as_expr().subs(N, N + 1) * envelope.as_expr()
                - 16 * envelope.as_expr().subs(N, N + 1) * positive.as_expr()
            ),
            N,
        )
        shifted_cross = sp.Poly(sp.expand(cross.as_expr().subs(N, X + start)), X)
        if any(value < 0 for value in shifted_cross.all_coeffs()):
            raise AssertionError((offset, "ratio monotonicity failed"))
        ratio_monomials += len(shifted_cross.all_coeffs())

        initial_gap = (
            sp.Integer(25) ** start * positive.eval(start)
            - sp.Integer(16) ** start * envelope.eval(start)
        )
        if initial_gap <= 0:
            raise AssertionError((offset, "ratio base failed", initial_gap))

        for n in range(start):
            exact = sum(
                sp.Integer(base) ** (2 * n) * polynomial.eval(n)
                for base, polynomial in parts.items()
            )
            if exact <= 0:
                raise AssertionError((offset, n, exact))
            exceptional_values += 1

        # Direct full polynomial checks guard the reverse extraction.
        for s in range(7, 11):
            row = even_row_direct(s)
            degree = 2 * s - 6 - offset
            exact = sum(
                sp.Integer(base) ** (2 * (s - 7))
                * polynomial.eval(s - 7)
                for base, polynomial in parts.items()
            )
            if exact != row.coeff_monomial(sp.Symbol("z") ** degree):
                raise AssertionError((offset, s, exact))
            direct_crosschecks += 1

    z = sp.Symbol("z")
    boundary_six = sp.cancel(even_row_direct(6).as_expr() / (1 + z) ** 2)
    expected_six = 972 + 2480 * z + 2760 * z**2 + 1504 * z**3 + 348 * z**4
    if sp.expand(boundary_six - expected_six) != 0:
        raise AssertionError(("s=6 boundary", boundary_six))

    return {
        "universal_top_coefficients": 6,
        "ratio_shift_monomials": ratio_monomials,
        "exceptional_values": exceptional_values,
        "direct_crosschecks": direct_crosschecks,
        "boundary_six_coefficients": 5,
    }


def even_row_direct(s: int) -> sp.Poly:
    z = sp.Symbol("z")
    u = s - 1
    endpoint = (
        sp.Rational(1, 3)
        * s ** (2 * s - 12)
        * sp.cancel(f5_direct(s).as_expr() / BETA**6).subs(BETA, z / s)
    )
    boundary = (
        2
        * (s - 4)
        * u ** (2 * s - 10)
        * (1 + z) ** 2
        * sp.cancel(j3_direct(u).as_expr() / BETA**2).subs(BETA, z / u)
    )
    return sp.Poly(sp.expand(endpoint - boundary), z)


def recurrence_layer_data() -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    b = BETA
    u2, u3, u4, u5 = (1 + j * b for j in range(2, 6))
    lam = lambda value: 1 + value * b
    a5 = sp.expand(k5(S + 1) - k5(S))
    a4 = sp.expand(
        3
        * (
            u5**2 * lam(S) ** 2 * k4(S)
            - u4**2 * lam(S + 1) ** 2 * k4(S + 1)
        )
    )
    a3 = sp.expand(
        3 * lam(S + 1) ** 4 * u3**4 * k3(S + 1)
        - 3 * u5**2 * lam(S) ** 4 * u3**2 * k3(S)
        - 6 * (S - 3) * S**2 * b**4 * lam(S) ** 2 * u3**2 * k3(S)
        + 6
        * (S - 4)
        * (S - 1) ** 2
        * b**4
        * u5**2
        * lam(S - 1) ** 2
        * k3(S - 1)
    )
    a2 = sp.expand(
        -lam(S + 1) ** 6 * u2**6
        + u5**2 * lam(S) ** 6 * u2**4
        + 6 * (S - 3) * S**2 * b**4 * lam(S) ** 4 * u2**4
        - 6
        * (S - 4)
        * (S - 1) ** 2
        * b**4
        * u5**2
        * lam(S - 1) ** 4
        * u2**2
    )
    return a5, a4, a3, a2


def certify_fixed_layer_obstruction() -> dict[str, int]:
    """Check the universal leading-term derivation and finite witnesses."""

    a5, a4, a3, a2 = recurrence_layer_data()
    y2, y3 = sp.symbols("y2 y3")
    generic_layer = sp.Poly(sp.expand(y3 * a5 + y2 * a4 + a3), BETA)
    u2 = 1 + 2 * BETA

    leading_by_delta = []
    for delta in range(1, 6):
        coefficient = sp.Poly(
            sp.expand(u2**delta * generic_layer.as_expr()), BETA
        ).coeff_monomial(BETA ** (delta + 3))
        leading = sp.Poly(coefficient, S).coeff_monomial(S ** (delta + 2))
        leading_by_delta.append(sp.expand(leading))
    if leading_by_delta != [-36, -12, 0, 0, 0]:
        raise AssertionError(leading_by_delta)
    if sp.Poly(a2, S).degree() > 7:
        raise AssertionError("A2 has an unexpected S-degree")

    def product_coefficient(
        power: int, polynomial: sp.Poly, degree: int
    ) -> sp.Expr:
        value = sp.Integer(0)
        for j in range(max(0, degree - polynomial.degree()), min(power, degree) + 1):
            value += (
                sp.binomial(power, j)
                * 2**j
                * polynomial.coeff_monomial(BETA ** (degree - j))
            )
        return sp.expand(value)

    # Exact fixed-R target-coefficient extractions sanity-check the closed
    # leading coefficient without expanding irrelevant beta coefficients.
    witnesses = 0
    a2_polynomial = sp.Poly(a2, BETA)
    for depth in (6, 10, 16):
        target_degree = depth + 3
        target = product_coefficient(depth, a2_polynomial, target_degree)
        for r in range(depth):
            layer = sp.Poly(sp.expand(3**r * a5 + 2**r * a4 + a3), BETA)
            target += (
                choose_fixed(2 * S - 10, r)
                * product_coefficient(depth - r, layer, target_degree - r)
            )
        leading = sp.Poly(sp.expand(target), S).coeff_monomial(S ** (depth + 2))
        expected = sp.Rational(
            -3 * 2**depth * (depth + 5), factorial(depth - 1)
        )
        if sp.expand(leading - expected) != 0:
            raise AssertionError((depth, leading, expected))
        witnesses += 1
    return {
        "universal_delta_identities": 5,
        "fixed_depth_symbolic_witnesses": witnesses,
    }


def main() -> None:
    low = certify_low_bulk_columns()
    top = certify_top_six()
    obstruction = certify_fixed_layer_obstruction()
    print("OPG EVEN SECOND-ACTIVE PARTIAL CERTIFICATE: PASS")
    for section in (low, top, obstruction):
        for name, value in section.items():
            print(f"{name}: {value}")
    print("status_full_even_row: OPEN")


if __name__ == "__main__":
    main()
