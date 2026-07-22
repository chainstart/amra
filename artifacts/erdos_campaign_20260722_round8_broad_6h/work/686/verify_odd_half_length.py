#!/usr/bin/env python3
"""Exact finite sanity check for odd_half_length_2adic_theorem.md.

The theorem is proved on paper; this script independently generates the
formal square-root coefficients by the identity Q(t)^2=F_l(t), checks their
predicted valuations for odd l, and checks integer evaluations at several
positive and negative x.  It is not used to extend a finite check to all l.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import factorial


def v2_integer(n: int) -> int:
    if n == 0:
        raise ValueError("v2(0)")
    n = abs(n)
    answer = 0
    while n % 2 == 0:
        n //= 2
        answer += 1
    return answer


def v2(value: Fraction) -> int:
    return v2_integer(value.numerator) - v2_integer(value.denominator)


def coefficients(l: int) -> list[Fraction]:
    elementary = [1]
    for odd in range(1, 2 * l, 2):
        elementary.append(0)
        square = odd * odd
        for j in range(len(elementary) - 1, 0, -1):
            elementary[j] += elementary[j - 1] * square
    q = [Fraction(1)]
    for j in range(1, l // 2 + 1):
        cross = sum(q[a] * q[j - a] for a in range(1, j))
        q.append((Fraction((-1) ** j * elementary[j]) - cross) / 2)
    return q


def polynomial_part(l: int, x: int, q: list[Fraction]) -> Fraction:
    w = 2 * x + 2 * l + 1
    return Fraction(1, 2**l) * sum(
        coefficient * w ** (l - 2 * j) for j, coefficient in enumerate(q)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-l", type=int, default=99)
    args = parser.parse_args()
    checked_coefficients = 0
    checked_values = 0
    for l in range(1, args.max_l + 1, 2):
        q = coefficients(l)
        for j, coefficient in enumerate(q):
            predicted = -v2_integer(factorial(2 * j))
            assert v2(coefficient) == predicted
            checked_coefficients += 1
        expected = -l - v2_integer(factorial(l))
        for x in (-3, -1, 0, 1, l, 2 * l + 1, 101):
            value = polynomial_part(l, x, q)
            assert value != 0 and v2(value) == expected
            normalized = value / Fraction(2**expected if expected >= 0 else 1,
                                          1 if expected >= 0 else 2 ** (-expected))
            assert normalized.denominator == 1 and normalized.numerator % 2
            checked_values += 1
    print(json.dumps({
        "status": "PASS",
        "odd_l_through": args.max_l if args.max_l % 2 else args.max_l - 1,
        "coefficients_checked": checked_coefficients,
        "integer_values_checked": checked_values,
        "global_claim_from_finite_check": False,
    }, separators=(",", ":")))


if __name__ == "__main__":
    main()
