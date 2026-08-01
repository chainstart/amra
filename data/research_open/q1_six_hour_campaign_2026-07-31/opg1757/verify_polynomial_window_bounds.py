#!/usr/bin/env python3
"""Falsification checks for the candidate polynomial OPG window.

The universal argument is in POLYNOMIAL_GROWING_DEFICIT_WINDOW.md.
This script independently checks the exact profile EGF, boundary offsets,
the interpolation/falling/convolution constants, and the final geometric
majorant.  With --extended-endpoints it also checks every Laurent
coefficient in the frozen q=6 endpoint table against the new all-k bound.
"""

from __future__ import annotations

import argparse
import math
import sys
from fractions import Fraction
from pathlib import Path

from verify_uniform_height_envelope import master_profiles


def polynomial_coefficients(power: int) -> list[int]:
    """Coefficients of (1 + 2*z + 2*z^2)^power."""

    out = [1]
    for _ in range(power):
        nxt = [0] * (len(out) + 2)
        for degree, value in enumerate(out):
            nxt[degree] += value
            nxt[degree + 1] += 2 * value
            nxt[degree + 2] += 2 * value
        out = nxt
    return out


def leading_endpoint_weight(excess: int, components: int) -> Fraction:
    rho = components - 1
    return Fraction(
        1,
        2 ** (rho + excess)
        * math.factorial(rho)
        * math.factorial(excess),
    )


def exact_profile_mass(q: int, r: int) -> Fraction:
    """Baseline mass before the determinant's factors 4 and 2."""

    total = Fraction(0)
    for overlap, e, f, c, d in master_profiles(q, r):
        a = r - 2 * overlap - e - f
        total += (
            Fraction(
                math.comb(q + 1 - overlap, a),
                math.factorial(overlap),
            )
            * leading_endpoint_weight(e, c)
            * leading_endpoint_weight(f, d)
        )
    return total


def exact_profile_mass_five_tuple(q: int, r: int) -> Fraction:
    """Independent sum in (ell,rho,e,sigma,f) coordinates."""

    total = Fraction(0)
    for overlap in range(q + 2):
        remaining_rank = q + 1 - overlap
        for rho in range(remaining_rank + 1):
            for excess in range(remaining_rank - rho + 1):
                for sigma in range(
                    remaining_rank - rho - excess + 1
                ):
                    right_excess = (
                        remaining_rank - rho - excess - sigma
                    )
                    lambda_degree = (
                        r
                        - 2 * overlap
                        - excess
                        - right_excess
                    )
                    if not 0 <= lambda_degree <= remaining_rank:
                        continue
                    total += Fraction(
                        math.comb(remaining_rank, lambda_degree),
                        math.factorial(overlap)
                        * 2**remaining_rank
                        * math.factorial(rho)
                        * math.factorial(excess)
                        * math.factorial(sigma)
                        * math.factorial(right_excess),
                    )
    return total


def audit_profile_mass(max_q: int = 9) -> int:
    checked = 0
    for q in range(1, max_q + 1):
        coeff_q = polynomial_coefficients(q)
        coeff_next = polynomial_coefficients(q + 1)
        for r in range(2 * q + 1):
            measured = exact_profile_mass(q, r)
            independent = exact_profile_mass_five_tuple(q, r)
            expected = Fraction(coeff_next[r], math.factorial(q + 1))
            if measured != independent or measured != expected:
                raise AssertionError(
                    f"profile EGF mismatch at {(q, r)}: "
                    f"{measured} != {independent} != {expected}"
                )
            current = coeff_q[r]
            previous = coeff_q[r - 1] if r >= 1 else 0
            previous_two = coeff_q[r - 2] if r >= 2 else 0
            if previous > q * current:
                raise AssertionError(f"adjacent ratio failed at {(q, r)}")
            if previous_two > q * q * current:
                raise AssertionError(
                    f"two-step ratio failed at {(q, r)}"
                )
            absolute_ratio = Fraction(
                2 * coeff_next[r],
                (q + 1) * current,
            )
            if absolute_ratio > 10 * q:
                raise AssertionError(
                    f"profile/leading ratio failed at {(q, r)}"
                )
            checked += 1
    return checked


def audit_newton_triangle(max_degree: int = 10) -> int:
    """Reconstruct total-degree polynomials from the triangular grid."""

    checked = 0
    for degree in range(max_degree + 1):
        coefficients = {
            (i, j): (-1) ** (i + j) * (i + 2 * j + 1)
            for i in range(degree + 1)
            for j in range(degree + 1 - i)
        }

        def value(x: int, y: int) -> int:
            return sum(
                coefficient * x**i * y**j
                for (i, j), coefficient in coefficients.items()
            )

        differences: dict[tuple[int, int], int] = {}
        for i in range(degree + 1):
            for j in range(degree + 1 - i):
                differences[(i, j)] = sum(
                    (-1) ** (i - a + j - b)
                    * math.comb(i, a)
                    * math.comb(j, b)
                    * value(a, b)
                    for a in range(i + 1)
                    for b in range(j + 1)
                )
        for x in range(degree + 4):
            for y in range(degree + 4):
                reconstructed = sum(
                    difference
                    * math.comb(x, i)
                    * math.comb(y, j)
                    for (i, j), difference in differences.items()
                )
                if reconstructed != value(x, y):
                    raise AssertionError(
                        f"Newton triangle failed at {(degree, x, y)}"
                    )
                checked += 1
    return checked


def node_bound(k: int) -> int:
    d = 2 * k
    return (
        15
        * (d + 1)
        * 2 ** (2 * d)
        * math.factorial(d)
        * (2 * d + 4) ** (2 * d)
    )


def interpolation_node_envelope(k: int) -> int:
    return (64 * (k + 1)) ** (12 * k)


def loss_factor_envelope(k: int, q: int) -> int:
    if k == 0:
        return 1
    return (128 * (k + 1)) ** (16 * k) * q ** (2 * k)


def product_loss_envelope(k: int, q: int) -> int:
    return (256 * (k + 1)) ** (20 * k) * q ** (2 * k)


def falling_coefficients(shift: int, order: int) -> list[int]:
    """Absolute elementary-symmetric coefficients of (s-shift)_order."""

    coefficients = [1]
    for root in range(shift, shift + order):
        nxt = [0] * (len(coefficients) + 1)
        for loss, value in enumerate(coefficients):
            nxt[loss] += value
            nxt[loss + 1] += root * value
        coefficients = nxt
    return coefficients


def audit_constant_chain(max_q: int = 60) -> int:
    checked = 0
    for q in range(1, max_q + 1):
        for k in range(1, 2 * q + 3):
            d = 2 * k
            if node_bound(k) > interpolation_node_envelope(k):
                raise AssertionError(f"node envelope failed at k={k}")
            interpolation_upper = (
                (d + 1) ** 2
                * 2**d
                * interpolation_node_envelope(k)
                * (q + 1) ** d
            )
            if interpolation_upper > loss_factor_envelope(k, q):
                raise AssertionError(
                    f"interpolation envelope failed at {(q, k)}"
                )
            composition_upper = (
                math.comb(k + 3, 3)
                * (128 * (k + 1)) ** (16 * k)
                * q ** (2 * k)
            )
            if composition_upper > product_loss_envelope(k, q):
                raise AssertionError(
                    f"product convolution failed at {(q, k)}"
                )
            checked += 1

        for actual_loss in range(1, 2 * q + 1):
            apparent_loss = actual_loss + 2
            left = (
                10
                * q
                * product_loss_envelope(apparent_loss, q)
            )
            right = ((4096 * q) ** 67) ** actual_loss
            if left > right:
                raise AssertionError(
                    f"geometric tail failed at {(q, actual_loss)}"
                )
            checked += 1
    return checked


def audit_falling_factors(max_q: int = 12) -> int:
    checked = 0
    for q in range(1, max_q + 1):
        for r in range(2 * q + 1):
            for overlap, e, f, c, d in master_profiles(q, r):
                shifts = (1 + c + e, 1 + d + f, c + e, 2 + d + f)
                for shift in shifts:
                    coefficients = falling_coefficients(shift, overlap)
                    for loss, coefficient in enumerate(coefficients):
                        if coefficient > loss_factor_envelope(loss, q):
                            raise AssertionError(
                                "falling coefficient failed at "
                                f"{(q, r, shift, overlap, loss)}"
                            )
                        checked += 1
    return checked


def audit_window_constant() -> int:
    # Dividing q <= s^(1/67)/8192 into the threshold gives the exact
    # multiplier below; it must be strictly less than one.
    numerator = 2 * 4096**67
    denominator = 8192**67
    if numerator >= denominator:
        raise AssertionError("8192 window constant failed")
    return 67


def audit_extended_q6_endpoints() -> int:
    """Check all exact q=6 endpoint Laurent values against (7)."""

    old_dir = (
        Path(__file__).resolve().parents[2]
        / "q1_three_hour_campaign_2026-07-31"
        / "opg1757"
    )
    sys.path.insert(0, str(old_dir))
    try:
        import verify_seventh_q6 as frozen  # type: ignore
    finally:
        sys.path.pop(0)

    checked = 0
    for (h, excess, components), expression in (
        frozen.Q6_ENDPOINT_POLYNOMIALS.items()
    ):
        rho = components - 1
        rank = excess + rho
        leading = Fraction(
            1,
            2**rank
            * math.factorial(rho)
            * math.factorial(excess),
        )
        polynomial = frozen.sp.Poly(expression, frozen.S)
        for loss in range(1, 2 * rank + 1):
            coefficient = polynomial.coeff_monomial(
                frozen.S ** (2 * rank - loss)
            )
            relative = abs(Fraction(coefficient) / leading)
            if relative > loss_factor_envelope(loss, 6):
                raise AssertionError(
                    "exact q=6 endpoint loss failed at "
                    f"{(h, excess, components, loss)}"
                )
            checked += 1
    return checked


def audit_extended_q6_layers() -> int:
    """Check the final loss index and root envelope on all q=6 layers."""

    old_dir = (
        Path(__file__).resolve().parents[2]
        / "q1_three_hour_campaign_2026-07-31"
        / "opg1757"
    )
    sys.path.insert(0, str(old_dir))
    try:
        import verify_seventh_q6 as frozen  # type: ignore
    finally:
        sys.path.pop(0)

    q = 6
    symbol = polynomial_coefficients(q)
    geometric_base = (4096 * q) ** 67
    checked = 0
    for offset in range(2 * q + 1):
        polynomial = frozen.sp.Poly(
            frozen.EXPECTED_Q6_NORMALIZED_LAYERS[offset],
            frozen.S,
        )
        leading = Fraction(4 * symbol[offset], math.factorial(q))
        if Fraction(polynomial.coeff_monomial(frozen.S ** (2 * q))) != leading:
            raise AssertionError(f"q=6 leading symbol failed at r={offset}")
        for loss in range(1, 2 * q + 1):
            coefficient = Fraction(
                polynomial.coeff_monomial(
                    frozen.S ** (2 * q - loss)
                )
            )
            if abs(coefficient) > leading * geometric_base**loss:
                raise AssertionError(
                    f"q=6 final tail failed at {(offset, loss)}"
                )
            checked += 1
    return checked


def run_certificate(extended_endpoints: bool = False) -> dict[str, int]:
    result = {
        "exact_profile_coefficients": audit_profile_mass(),
        "newton_reconstructions": audit_newton_triangle(),
        "constant_chain_values": audit_constant_chain(),
        "falling_coefficients": audit_falling_factors(),
        "window_exponent": audit_window_constant(),
    }
    if extended_endpoints:
        result["exact_q6_endpoint_losses"] = audit_extended_q6_endpoints()
        result["exact_q6_layer_losses"] = audit_extended_q6_layers()
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--extended-endpoints", action="store_true")
    args = parser.parse_args()
    result = run_certificate(args.extended_endpoints)
    print("OPG POLYNOMIAL WINDOW BOUNDS CERTIFICATE: PASS")
    for name, value in result.items():
        print(f"{name}: {value}")
