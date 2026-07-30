#!/usr/bin/env python3
"""Finite audits for the fixed-number-field weighted terminal theorem.

The arbitrary-field proof is ideal-theoretic.  This verifier checks its
combinatorial envelopes, rational special case, logarithmic unit count,
and the Salem-unit obstruction when conjugate-height control is removed.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math

import sympy as sp


def divisor_count(value: int) -> int:
    if value < 1:
        raise ValueError("positive integer required")
    count = 0
    for divisor in range(1, math.isqrt(value) + 1):
        if value % divisor == 0:
            count += 1 if divisor * divisor == value else 2
    return count


def integer_two_square_count(value: int) -> int:
    if value == 0:
        raise ValueError("the terminal theorem excludes n=0")
    if value < 0:
        return 0
    count = 0
    for x in range(-math.isqrt(value), math.isqrt(value) + 1):
        remainder = value - x * x
        y = math.isqrt(remainder)
        if y * y == remainder:
            count += 1 if y == 0 else 2
    return count


def ideal_divisor_local_envelope(norm_exponent: int, field_degree: int):
    """Exhaust synthetic prime-ideal exponents over one rational prime."""
    if norm_exponent < 0 or field_degree < 1:
        raise ValueError("invalid exponent or degree")
    envelope = (norm_exponent + 1) ** field_degree
    maximum = 0
    checked = 0
    # Every prime-ideal exponent is at most v_p(Norm(n)); allowing all
    # D-tuples is a superset of actual splitting patterns.
    for exponents in itertools.product(
        range(norm_exponent + 1), repeat=field_degree
    ):
        number_of_divisors = math.prod(value + 1 for value in exponents)
        assert number_of_divisors <= envelope
        maximum = max(maximum, number_of_divisors)
        checked += 1
    return {
        "norm_exponent": norm_exponent,
        "degree": field_degree,
        "patterns_checked": checked,
        "maximum": maximum,
        "tau_power_envelope": envelope,
    }


def unit_log_box_lattice_count(rank: int, logarithmic_radius: int) -> int:
    """Toy Z^rank count modeling a fixed log-unit lattice."""
    if rank < 0 or logarithmic_radius < 0:
        raise ValueError("nonnegative arguments required")
    return (2 * logarithmic_radius + 1) ** rank


def salem_single_embedding_obstruction(maximum_power: int = 24):
    """Verify a unit obstruction without all-conjugate height control."""
    variable = sp.symbols("X")
    polynomial = sp.Poly(
        variable**4 - variable**3 - variable**2 - variable + 1,
        variable,
    )
    roots = [complex(root) for root in sp.nroots(polynomial, n=40)]
    real_roots = [root for root in roots if abs(root.imag) < 1e-25]
    circle_roots = [
        root
        for root in roots
        if abs(root.imag) >= 1e-25 and abs(abs(root) - 1) < 1e-25
    ]
    assert len(real_roots) == 2
    assert len(circle_roots) == 2
    expanding_root = max(real_roots, key=abs)
    circle_root = circle_roots[0]
    assert abs(expanding_root) > 1

    samples = []
    for power in range(1, maximum_power + 1):
        unit_circle_value = circle_root**power
        x_circle = unit_circle_value + 1 / unit_circle_value
        y_circle = -1j * (
            unit_circle_value - 1 / unit_circle_value
        )
        assert abs(x_circle.imag) < 1e-12
        assert abs(y_circle.imag) < 1e-12
        assert abs(x_circle.real) <= 2 + 1e-12
        assert abs(y_circle.real) <= 2 + 1e-12
        assert abs(x_circle * x_circle + y_circle * y_circle - 4) < 1e-12

        real_value = expanding_root**power
        x_other = real_value + 1 / real_value
        samples.append(
            {
                "power": power,
                "distinguished_x_abs": abs(x_circle.real),
                "distinguished_y_abs": abs(y_circle.real),
                "other_conjugate_x_abs": abs(x_other),
            }
        )
    assert samples[-1]["other_conjugate_x_abs"] > 1000
    return {
        "salem_polynomial": str(polynomial.as_expr()),
        "constant_norm_equation": "x_m^2+y_m^2=4",
        "bounded_distinguished_coordinates": True,
        "unbounded_other_conjugate": True,
        "powers_checked": maximum_power,
        "last_sample": samples[-1],
    }


def audit():
    rational_checks = 0
    for value in range(1, 501):
        assert integer_two_square_count(value) <= 4 * divisor_count(value)
        rational_checks += 1

    ideal_checks = []
    for degree in (1, 2, 3, 4):
        for exponent in range(5):
            ideal_checks.append(
                ideal_divisor_local_envelope(exponent, degree)
            )

    unit_counts = []
    for rank in range(5):
        values = [
            unit_log_box_lattice_count(rank, radius)
            for radius in (1, 2, 4, 8)
        ]
        assert values == sorted(values)
        unit_counts.append(
            {
                "rank": rank,
                "counts": values,
                "growth": f"O((log B)^{rank})",
            }
        )

    return {
        "schema": (
            "amra.erdos1083.fixed-number-field-weighted-chart.v1"
        ),
        "verdict": "PASS",
        "theorem_scope": (
            "Fixed K, nonzero labels, algebraic-integral scaled chord "
            "and height coordinates, and polynomial bounds at every "
            "embedding. The fibre is t^o(1)."
        ),
        "rational_two_square_checks": rational_checks,
        "ideal_local_envelopes": len(ideal_checks),
        "unit_log_lattice": unit_counts,
        "missing_conjugate_height_obstruction": (
            salem_single_embedding_obstruction()
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
