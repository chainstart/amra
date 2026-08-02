#!/usr/bin/env python3
"""Independent falsification certificate for the eighth-root OPG window.

The universal proof is POWER_EIGHTH_WINDOW_THEOREM.md.  This program
reconstructs the five-coordinate profile EGF without importing the
previous campaign, checks the sharpened endpoint/interpolation envelope,
and stress-tests the four-factor and final geometric inequalities.
Finite checks are not substitutes for the displayed universal bounds.
"""

from __future__ import annotations

import math
from fractions import Fraction


FINAL_BASE = 2**23


def symbol_coefficients(power: int) -> list[int]:
    """Coefficients of (1 + 2*z + 2*z^2)^power."""

    coefficients = [1]
    for _ in range(power):
        next_coefficients = [0] * (len(coefficients) + 2)
        for degree, value in enumerate(coefficients):
            next_coefficients[degree] += value
            next_coefficients[degree + 1] += 2 * value
            next_coefficients[degree + 2] += 2 * value
        coefficients = next_coefficients
    return coefficients


def five_coordinate_profile_mass(q: int, r: int) -> Fraction:
    """One determinant side, including the overlap factorial."""

    total = Fraction(0)
    rank = q + 1
    for overlap in range(rank + 1):
        for rho in range(rank - overlap + 1):
            for excess in range(rank - overlap - rho + 1):
                for sigma in range(
                    rank - overlap - rho - excess + 1
                ):
                    right_excess = (
                        rank - overlap - rho - excess - sigma
                    )
                    selected = r - 2 * overlap - excess - right_excess
                    if not 0 <= selected <= rank - overlap:
                        continue
                    total += Fraction(
                        math.comb(rank - overlap, selected),
                        math.factorial(overlap)
                        * 2 ** (rank - overlap)
                        * math.factorial(rho)
                        * math.factorial(excess)
                        * math.factorial(sigma)
                        * math.factorial(right_excess),
                    )
    return total


def audit_profile_egf(max_q: int = 10) -> int:
    checked = 0
    for q in range(1, max_q + 1):
        current = symbol_coefficients(q)
        following = symbol_coefficients(q + 1)
        for r in range(2 * q + 1):
            measured = five_coordinate_profile_mass(q, r)
            expected = Fraction(following[r], math.factorial(q + 1))
            if measured != expected:
                raise AssertionError(f"profile EGF failed at {(q, r)}")

            previous = current[r - 1] if r else 0
            previous_two = current[r - 2] if r >= 2 else 0
            if previous > q * current[r]:
                raise AssertionError(f"one-step word map failed at {(q, r)}")
            if previous_two > q * q * current[r]:
                raise AssertionError(f"two-step word map failed at {(q, r)}")

            absolute_to_leading = Fraction(
                2 * following[r], (q + 1) * current[r]
            )
            if absolute_to_leading > 10 * q:
                raise AssertionError(f"profile ratio failed at {(q, r)}")
            checked += 1
    return checked


def node_bound(k: int) -> int:
    return (
        15
        * (2 * k + 1)
        * 2 ** (4 * k)
        * math.factorial(2 * k)
        * (4 * k + 4) ** (4 * k)
    )


def interpolated_upper(k: int, q: int) -> int:
    return (
        (2 * k + 1) ** 2
        * 2 ** (2 * k)
        * node_bound(k)
        * (q + 1) ** (2 * k)
    )


def one_factor_envelope(k: int, q: int) -> int:
    if k == 0:
        return 1
    return (64 * (k + 1)) ** (6 * k) * q ** (2 * k)


def four_factor_envelope(k: int, q: int) -> int:
    return (128 * (k + 1)) ** (6 * k) * q ** (2 * k)


def audit_sharpened_endpoint(max_q: int = 80) -> int:
    checked = 0
    for q in range(1, max_q + 1):
        for k in range(1, 2 * q + 3):
            if interpolated_upper(k, q) > one_factor_envelope(k, q):
                raise AssertionError(f"endpoint envelope failed at {(q, k)}")

            compositions = math.comb(k + 3, 3)
            product_upper = (
                compositions
                * (64 * (k + 1)) ** (6 * k)
                * q ** (2 * k)
            )
            if product_upper > four_factor_envelope(k, q):
                raise AssertionError(f"four-factor envelope failed at {(q, k)}")
            checked += 1
    return checked


def falling_coefficients(shift: int, order: int) -> list[int]:
    coefficients = [1]
    for root in range(shift, shift + order):
        next_coefficients = [0] * (len(coefficients) + 1)
        for loss, value in enumerate(coefficients):
            next_coefficients[loss] += value
            next_coefficients[loss + 1] += root * value
        coefficients = next_coefficients
    return coefficients


def audit_falling_factors(max_q: int = 30) -> int:
    """Use every allowable order and every shift up to q+4."""

    checked = 0
    for q in range(1, max_q + 1):
        for order in range(q + 1):
            for shift in range(1, q + 5):
                for loss, coefficient in enumerate(
                    falling_coefficients(shift, order)
                ):
                    if coefficient > one_factor_envelope(loss, q):
                        raise AssertionError(
                            f"falling envelope failed at "
                            f"{(q, order, shift, loss)}"
                        )
                    checked += 1
    return checked


def raw_loss_ratio_bound(q: int, actual_loss: int) -> int:
    apparent_loss = actual_loss + 2
    return (
        10
        * q
        * four_factor_envelope(apparent_loss, q)
    )


def audit_geometric_majorant(max_q: int = 150) -> int:
    checked = 0
    for q in range(1, max_q + 1):
        geometric_base = (FINAL_BASE * q) ** 8
        for actual_loss in range(1, 2 * q + 1):
            if raw_loss_ratio_bound(q, actual_loss) > (
                geometric_base**actual_loss
            ):
                raise AssertionError(
                    f"eighth-power majorant failed at {(q, actual_loss)}"
                )
            checked += 1
    return checked


def audit_window_constant() -> int:
    divisor = 2**24
    if 2 * FINAL_BASE**8 >= divisor**8:
        raise AssertionError("simultaneous window constant is not strict")
    return 8


def run_certificate() -> dict[str, int]:
    return {
        "exact_profile_coefficients": audit_profile_egf(),
        "endpoint_and_convolution_values": audit_sharpened_endpoint(),
        "falling_coefficients": audit_falling_factors(),
        "geometric_loss_values": audit_geometric_majorant(),
        "window_exponent_denominator": audit_window_constant(),
    }


if __name__ == "__main__":
    result = run_certificate()
    print("OPG EIGHTH-ROOT WINDOW CERTIFICATE: PASS")
    for name, value in result.items():
        print(f"{name}: {value}")
