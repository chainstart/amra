#!/usr/bin/env python3
"""Exact reverse-coefficient certificate for third-active transports.

The all-parameter argument is a dominant-exponential ratio proof.  Direct
finite transport expansions are used only to guard reverse indexing.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


OLD_LANE = (
    Path(__file__).resolve().parents[2]
    / "q1_eight_hour_campaign_2026-07-29"
    / "opg1757"
)
sys.path.insert(0, str(OLD_LANE))

from five_page_union_formula import (  # noqa: E402
    k3_coefficients,
    k4_coefficients,
    k5_coefficients,
)
from six_page_union_formula import k6_coefficients  # noqa: E402
from seven_page_union_formula import k7_coefficients  # noqa: E402


B = sp.symbols("b")
S = sp.symbols("s", integer=True, positive=True)
N = sp.symbols("n", integer=True, nonnegative=True)
X = sp.symbols("x", integer=True, nonnegative=True)


def choose_fixed(top: sp.Expr, bottom: int) -> sp.Expr:
    if bottom < 0:
        return sp.S.Zero
    return sp.prod(top - index for index in range(bottom)) / sp.factorial(bottom)


def convolution(left: list[sp.Expr], right: list[sp.Expr]) -> list[sp.Expr]:
    result = [sp.S.Zero] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return [sp.expand(value) for value in result]


def lambda_coefficients(power: int, parameter: sp.Expr) -> list[sp.Expr]:
    return [sp.binomial(power, degree) * parameter**degree for degree in range(power + 1)]


def top_component(
    base: int,
    exponent: sp.Expr,
    kernel: list[sp.Expr],
    total_degree: sp.Expr,
) -> sp.Expr:
    """Coefficient after factoring base**(2*S), at a reverse-fixed degree."""

    value = sp.S.Zero
    for index, entry in enumerate(kernel):
        complement = sp.simplify(exponent - (total_degree - index))
        if complement.is_Integer and complement >= 0:
            residual = sp.simplify(exponent - complement - 2 * S)
            if not residual.is_Integer:
                raise AssertionError(residual)
            value += (
                entry
                * choose_fixed(exponent, int(complement))
                * sp.Integer(base) ** int(residual)
            )
    return sp.expand(value)


KERNELS = {
    3: k3_coefficients,
    4: k4_coefficients,
    5: k5_coefficients,
    6: k6_coefficients,
    7: k7_coefficients,
}


def f_components(page: int, parameter: sp.Expr, degree: sp.Expr) -> dict[int, sp.Expr]:
    """Return base components of [b^degree] F_page(parameter,b)."""

    result: dict[int, sp.Expr] = {}
    # F_p has binomial multipliers (-1)^(p-j) C(p-2,j-2), j=2,...,p.
    for base in range(2, page + 1):
        multiplier = (-1) ** (page - base) * sp.binomial(page - 2, base - 2)
        lambda_power = 2 * (page - base)
        exponent = 2 * parameter - 2 * base - 2
        page_kernel = [sp.S.One] if base == 2 else KERNELS[base](parameter)
        full_kernel = convolution(
            lambda_coefficients(lambda_power, parameter), page_kernel
        )
        result[base] = sp.expand(
            multiplier * top_component(base, exponent, full_kernel, degree)
        )
    return result


def add_parts(target: dict[int, sp.Expr], parts: dict[int, sp.Expr], multiplier: sp.Expr) -> None:
    for base, value in parts.items():
        target[base] = sp.cancel(target.get(base, sp.S.Zero) + multiplier * value)


def odd_h_top(offset: int) -> dict[int, sp.Expr]:
    """[z^(2s-6-offset)] H_s^o = sum base^(2s) D_base(s)."""

    degree = 2 * S - 6 - offset
    result: dict[int, sp.Expr] = {}
    add_parts(
        result,
        f_components(6, S, degree + 8),
        sp.Rational(1, 12) * S ** (offset - 8),
    )

    parameter = S - 1
    for shift in range(3):
        parts = f_components(4, parameter, degree - shift + 4)
        multiplier = (
            -(S - 4)
            * sp.binomial(2, shift)
            * parameter ** (offset + shift - 6)
        )
        add_parts(result, parts, multiplier)

    exponent = 2 * S - 10
    value = sp.S.Zero
    for shift in range(5):
        power_degree = sp.simplify(degree - shift)
        complement = sp.simplify(exponent - power_degree)
        if complement.is_Integer and complement >= 0:
            value += (
                sp.binomial(4, shift)
                * choose_fixed(exponent, int(complement))
                * sp.Integer(2) ** int(power_degree - 2 * S)
                * (S - 2) ** int(complement)
            )
    result[2] = sp.cancel(
        result.get(2, 0) + (S - 4) * (S - 5) * value
    )
    return {base: sp.factor(value) for base, value in result.items()}


def even_h_top(offset: int) -> dict[int, sp.Expr]:
    """[z^(2s-6-offset)] H_s^e = sum base^(2s) D_base(s)."""

    degree = 2 * S - 6 - offset
    result: dict[int, sp.Expr] = {}
    add_parts(
        result,
        f_components(7, S, degree + 10),
        sp.Rational(1, 60) * S ** (offset - 10),
    )

    parameter = S - 1
    for shift in range(3):
        parts = f_components(5, parameter, degree - shift + 6)
        multiplier = (
            -sp.Rational(1, 3)
            * (S - 4)
            * sp.binomial(2, shift)
            * parameter ** (offset + shift - 8)
        )
        add_parts(result, parts, multiplier)

    parameter = S - 2
    for shift in range(5):
        parts = f_components(3, parameter, degree - shift + 2)
        multiplier = (
            (S - 4)
            * (S - 5)
            * sp.binomial(4, shift)
            * parameter ** (offset + shift - 6)
        )
        add_parts(result, parts, multiplier)
    return {base: sp.factor(value) for base, value in result.items()}


def transport_top(parity: str, offset: int) -> dict[int, sp.Expr]:
    getter = odd_h_top if parity == "odd" else even_h_top
    page = 6 if parity == "odd" else 7
    current = getter(offset)
    previous1 = getter(offset - 1) if offset >= 1 else {}
    previous2 = getter(offset - 2) if offset >= 2 else {}
    following = getter(offset)
    result: dict[int, sp.Expr] = {}
    for base in range(2, page + 1):
        value = (
            base**2 * following.get(base, 0).subs(S, S + 1)
            - page**2 * current.get(base, 0)
            - 2 * S * page * previous1.get(base, 0)
            - S**2 * previous2.get(base, 0)
        )
        result[base] = sp.factor(sp.cancel(value))
    return result


def shifted_parts(parity: str, offset: int) -> dict[int, sp.Poly]:
    start = 8 if parity == "odd" else 9
    result = {}
    for base, value in transport_top(parity, offset).items():
        shifted = sp.cancel(sp.Integer(base) ** (2 * start) * value.subs(S, N + start))
        result[base] = sp.Poly(sp.expand(shifted), N)
    return result


def negative_envelope(parts: dict[int, sp.Poly], dominant: int) -> sp.Poly:
    value = sp.S.Zero
    for base, polynomial in parts.items():
        if base == dominant:
            continue
        for (degree,), coefficient in polynomial.terms():
            if coefficient < 0:
                value -= coefficient * N**degree
    return sp.Poly(sp.expand(value), N)


def find_ratio_certificate(parity: str, offset: int, maximum_shift: int = 30) -> dict[str, object] | None:
    parts = shifted_parts(parity, offset)
    page = 6 if parity == "odd" else 7
    dominant = next(
        base
        for base in range(page, 1, -1)
        if parts[base].as_expr() != 0
    )
    if any(parts[base].as_expr() != 0 for base in range(dominant + 1, page + 1)):
        raise AssertionError("a higher nonzero base was skipped")
    lower = dominant - 1
    positive = parts[dominant]
    envelope = negative_envelope(parts, dominant)
    for shift in range(maximum_shift + 1):
        shifted_positive = sp.Poly(sp.expand(positive.as_expr().subs(N, X + shift)), X)
        shifted_envelope = sp.Poly(sp.expand(envelope.as_expr().subs(N, X + shift)), X)
        if any(value <= 0 for value in shifted_positive.all_coeffs()):
            continue
        if envelope.as_expr() != 0 and any(value < 0 for value in shifted_envelope.all_coeffs()):
            continue
        if envelope.as_expr() == 0:
            return {"shift": shift, "ratio_terms": 0, "gap": positive.eval(shift)}
        cross = sp.Poly(
            sp.expand(
                dominant**2
                * positive.as_expr().subs(N, N + 1)
                * envelope.as_expr()
                - lower**2
                * envelope.as_expr().subs(N, N + 1)
                * positive.as_expr()
            ),
            N,
        )
        shifted_cross = sp.Poly(sp.expand(cross.as_expr().subs(N, X + shift)), X)
        if any(value < 0 for value in shifted_cross.all_coeffs()):
            continue
        gap = dominant ** (2 * shift) * positive.eval(shift) - lower ** (2 * shift) * envelope.eval(shift)
        if gap <= 0:
            continue
        exceptional_values = []
        for n in range(shift):
            exact = sum(
                sp.Integer(base) ** (2 * n) * polynomial.eval(n)
                for base, polynomial in parts.items()
            )
            if exact <= 0:
                raise AssertionError((parity, offset, n, exact))
            exceptional_values.append(exact)
        return {
            "shift": shift,
            "dominant": dominant,
            "ratio_terms": len(shifted_cross.all_coeffs()),
            "gap": gap,
            "dominant_degree": positive.degree(),
            "envelope_degree": envelope.degree(),
            "exceptional_values": exceptional_values,
        }
    return None


def direct_crosschecks() -> int:
    """Guard the reverse formulas against the exact forward workbench."""

    import third_active_workbench as direct

    checks = 0
    for parity, start, offsets in (("odd", 8, 8), ("even", 9, 10)):
        for s in range(start, start + 4):
            transport = direct.transport_remainder(parity, s)
            for offset in range(offsets):
                degree = 2 * s - 4 - offset
                reconstructed = sum(
                    sp.Integer(base) ** (2 * s) * value.subs(S, s)
                    for base, value in transport_top(parity, offset).items()
                )
                if reconstructed != transport[degree]:
                    raise AssertionError(
                        (parity, s, offset, reconstructed, transport[degree])
                    )
                checks += 1
    return checks


EXPECTED_SHIFTS = {
    "odd": (0, 2, 1, 1, 0, 0, 0, 1),
    "even": (0, 4, 3, 2, 1, 1, 1, 2, 2, 3),
}


def certify() -> dict[str, object]:
    result: dict[str, object] = {}
    ratio_monomials = exceptional_count = 0
    for parity, shifts in EXPECTED_SHIFTS.items():
        certificates = []
        for offset, expected_shift in enumerate(shifts):
            certificate = find_ratio_certificate(parity, offset)
            if certificate is None:
                raise AssertionError((parity, offset, "no ratio certificate"))
            if certificate["shift"] != expected_shift:
                raise AssertionError((parity, offset, certificate["shift"]))
            ratio_monomials += int(certificate["ratio_terms"])
            exceptional_count += len(certificate["exceptional_values"])
            certificates.append(certificate)
        result[parity] = certificates
    result["ratio_shift_monomials"] = ratio_monomials
    result["exceptional_values"] = exceptional_count
    result["direct_crosschecks"] = direct_crosschecks()
    return result


def main() -> None:
    result = certify()
    print("OPG THIRD-ACTIVE TRANSPORT TOP-BAND CERTIFICATE: PASS")
    for parity in ("odd", "even"):
        print(f"{parity}_top_offsets: {len(result[parity])}")
        print(
            f"{parity}_ratio_shifts:",
            [certificate["shift"] for certificate in result[parity]],
        )
        print(
            f"{parity}_dominant_bases:",
            [certificate["dominant"] for certificate in result[parity]],
        )
    print("ratio_shift_monomials:", result["ratio_shift_monomials"])
    print("exceptional_values:", result["exceptional_values"])
    print("direct_crosschecks:", result["direct_crosschecks"])
    print("status_full_transports: OPEN")


if __name__ == "__main__":
    main()
