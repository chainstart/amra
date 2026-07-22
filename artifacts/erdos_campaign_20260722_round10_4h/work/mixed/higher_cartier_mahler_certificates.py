#!/usr/bin/env python3
"""Exact Mahler certificates for previously unresolved #686 Cartier layers.

For each requested m this constructs
  C_m(z)=[v^m](1-zv)^(-1) prod_{j=1}^{2m}(1-binomial(j,2)v)^(1/2)
as a rational polynomial, computes all forward differences at zero, and
checks the parity certificate described in REPORT.md.  There is no sampling.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from math import factorial


def v2_integer(value: int) -> int:
    value = abs(value)
    if not value:
        raise ValueError("v2(0)")
    answer = 0
    while value % 2 == 0:
        answer += 1
        value //= 2
    return answer


def v2_fraction(value: Fraction) -> int:
    return v2_integer(value.numerator) - v2_integer(value.denominator)


def oddpart(value: int) -> int:
    while value % 2 == 0:
        value //= 2
    return value


def sqrt_product_coefficients(parameters: list[int], degree: int) -> list[Fraction]:
    polynomial = [1]
    for parameter in parameters:
        polynomial.append(0)
        for index in range(len(polynomial) - 1, 0, -1):
            polynomial[index] -= parameter * polynomial[index - 1]
    root = [Fraction(1)]
    for index in range(1, degree + 1):
        cross = sum(root[j] * root[index - j] for j in range(1, index))
        root.append((Fraction(polynomial[index]) - cross) / 2)
    return root


def c_polynomial(m: int) -> list[Fraction]:
    parameters = [j * (j - 1) // 2 for j in range(1, 2 * m + 1)]
    root = sqrt_product_coefficients(parameters, m)
    return list(reversed(root))


def evaluate(coefficients: list[Fraction], value: int) -> Fraction:
    answer = Fraction(0)
    for coefficient in reversed(coefficients):
        answer = answer * value + coefficient
    return answer


def mahler_coefficients(coefficients: list[Fraction]) -> list[Fraction]:
    row = [evaluate(coefficients, value) for value in range(len(coefficients))]
    answer = []
    while row:
        answer.append(row[0])
        row = [row[index + 1] - row[index] for index in range(len(row) - 1)]
    return answer


def certify(m: int) -> dict[str, object]:
    odd = oddpart(m)
    target = m - 2 * odd - v2_integer(factorial(odd))
    mahler = mahler_coefficients(c_polynomial(m))
    normalized = [value / Fraction(2) ** target for value in mahler]
    assert all(value.denominator == 1 for value in normalized)
    integers = [value.numerator for value in normalized]
    assert integers[0] % 2
    assert all(value % 2 == 0 for value in integers[1:])
    encoded = ",".join(map(str, integers)).encode()
    return {
        "m": m,
        "corresponding_half_length_l": 2 * m,
        "target_v2_C_m": target,
        "target_v2_A_2m": m + target,
        "normalized_mahler_v2": [v2_integer(value) for value in integers],
        "normalized_constant": integers[0],
        "all_positive_order_coefficients_even": True,
        "normalized_coefficients_sha256": hashlib.sha256(encoded).hexdigest(),
        "conclusion": f"v2(C_{m}(z))={target} for every integer z",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("m", nargs="*", type=int, default=[12, 20, 28])
    args = parser.parse_args()
    rows = [certify(m) for m in args.m]
    print(json.dumps({
        "status": "PASS",
        "scope": "exact all-integer-value certificates at the listed fixed m only",
        "rows": rows,
    }, indent=2))


if __name__ == "__main__":
    main()
