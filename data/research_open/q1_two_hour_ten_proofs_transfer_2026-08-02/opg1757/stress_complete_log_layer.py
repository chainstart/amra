#!/usr/bin/env python3
"""Large exact-integer stress scan for the OPG logarithmic layer.

This is deliberately separate from the proof certificate.  A successful run
is corroboration only and is never promoted to an unbounded theorem.
"""

from __future__ import annotations

import math

import sympy as sp

from verify_complete_log_layer import (
    B,
    S,
    even_w_components,
    odd_w_components,
    page_recurrence_components,
    source_hash,
)


PARAMETERS = tuple(range(23, 97)) + (
    100,
    112,
    128,
    160,
    200,
    250,
    320,
    400,
    512,
    750,
    1000,
    1500,
    2000,
    3000,
    5000,
    10000,
)


def evaluated_kernels(
    components: dict[int, sp.Expr], s: int
) -> dict[int, tuple[tuple[int, int], ...]]:
    return {
        a: tuple(
            (j, int(sp.Poly(coefficient, S).eval(s)))
            for (j,), coefficient in sp.Poly(expression, B).terms()
        )
        for a, expression in components.items()
    }


def coefficient_row(
    components: dict[int, sp.Expr], s: int, exponent: int, maximum: int
) -> list[int]:
    """Expand only the requested prefix, using exact Python integers."""

    result = [0] * (maximum + 1)
    for a, kernel in evaluated_kernels(components, s).items():
        base = [1]
        for degree in range(min(exponent, maximum)):
            base.append(
                base[-1] * (exponent - degree) * a // (degree + 1)
            )
        for shift, coefficient in kernel:
            if shift > maximum or coefficient == 0:
                continue
            for residual in range(min(exponent, maximum - shift) + 1):
                result[shift + residual] += coefficient * base[residual]
    return result


def stress() -> dict[str, object]:
    objects = (
        ("odd_sufficient", odd_w_components(), -15, 8, 12),
        ("odd_page", page_recurrence_components(6), -14, 8, 12),
        ("even_sufficient", even_w_components(), -17, 10, 14),
        ("even_page", page_recurrence_components(7), -16, 10, 14),
    )
    result: dict[str, object] = {}
    grand_total = 0
    for name, components, exponent_offset, shift, cutoff in objects:
        checks = 0
        nonempty_parameters = 0
        largest_degree = -1
        for s in PARAMETERS:
            maximum_d = min(
                math.ceil(241 * math.log(s)) - 1,
                2 * s - cutoff,
            )
            if maximum_d < 31:
                continue
            nonempty_parameters += 1
            largest_degree = max(largest_degree, maximum_d)
            row = coefficient_row(
                components,
                s,
                2 * s + exponent_offset,
                maximum_d + shift,
            )
            for d in range(31, maximum_d + 1):
                value = row[d + shift]
                if value <= 0:
                    raise AssertionError((name, s, d, value))
                checks += 1
        result[name] = {
            "parameters": nonempty_parameters,
            "coefficients": checks,
            "largest_s": max(PARAMETERS),
            "largest_d": largest_degree,
        }
        grand_total += checks
    result["grand_total_coefficients"] = grand_total
    result["role"] = "CORROBORATION_ONLY"
    result["source_sha256"] = source_hash()
    return result


def main() -> None:
    result = stress()
    print("OPG COMPLETE LOG-LAYER EXTENDED STRESS: PASS")
    for name in (
        "odd_sufficient",
        "odd_page",
        "even_sufficient",
        "even_page",
    ):
        print(name, result[name])
    print("grand_total_coefficients:", result["grand_total_coefficients"])
    print("role:", result["role"])
    print("source_sha256:", result["source_sha256"])
    print("status_original_opg1757: OPEN")


if __name__ == "__main__":
    main()
