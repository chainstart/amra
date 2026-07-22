#!/usr/bin/env python3
"""Exact finite probe for the still-unproved even-l valuation pattern.

This is conjecture generation only.  It computes the Laurent coefficients
of sqrt(prod_j (w^2-(2j-1)^2)) by the identity q(t)^2=F(t), evaluates the
polynomial part exactly, and compares its 2-adic valuation with the proposed
formula.  A finite PASS is not a proof for arbitrary l or x.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import factorial


def valuation_2(value: Fraction | int) -> int:
    value = Fraction(value)
    if value == 0:
        raise ValueError("v_2(0) is infinite")
    numerator = abs(value.numerator)
    denominator = value.denominator
    answer = 0
    while numerator % 2 == 0:
        answer += 1
        numerator //= 2
    while denominator % 2 == 0:
        answer -= 1
        denominator //= 2
    return answer


def polynomial_part_coefficients(l: int) -> list[Fraction]:
    # F(t)=prod_{j=1}^l(1-(2j-1)^2 t).
    coefficients = [1]
    for j in range(1, l + 1):
        square = (2 * j - 1) ** 2
        coefficients = [coefficients[0]] + [
            (coefficients[i] if i < len(coefficients) else 0)
            - square * coefficients[i - 1]
            for i in range(1, len(coefficients) + 1)
        ]
    degree = l // 2
    q = [Fraction(1)]
    for n in range(1, degree + 1):
        convolution = sum(q[i] * q[n - i] for i in range(1, n))
        q.append((Fraction(coefficients[n]) - convolution) / 2)
    return q


def odd_part(value: int) -> int:
    while value % 2 == 0:
        value //= 2
    return value


def predicted_even_valuation(l: int) -> int:
    s = odd_part(l)
    return l - 2 * s - valuation_2(factorial(s))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-even-l", type=int, default=64)
    parser.add_argument("--max-x", type=int, default=127)
    args = parser.parse_args()
    failures = []
    cases = 0
    summaries = []
    for l in range(2, args.max_even_l + 1, 2):
        q = polynomial_part_coefficients(l)
        predicted = predicted_even_valuation(l)
        observed = set()
        for x in range(args.max_x + 1):
            w = 2 * x + 2 * l + 1
            Q = sum(q[j] * w ** (l - 2 * j) for j in range(len(q)))
            actual = valuation_2(Q) - l
            observed.add(actual)
            cases += 1
            if actual != predicted:
                failures.append({"l": l, "x": x, "actual": actual,
                                 "predicted": predicted})
                break
        summaries.append({"l": l, "odd_part": odd_part(l),
                          "predicted": predicted,
                          "observed": sorted(observed)})
        if failures:
            break
    print(json.dumps({
        "status": "PASS" if not failures else "FAIL",
        "scope_warning": "finite exact probe; the even-l formula is unproved",
        "formula": "v2(A_l(x)) = l - 2*oddpart(l) - v2(oddpart(l)!)",
        "max_even_l": args.max_even_l,
        "max_x": args.max_x,
        "cases_checked": cases,
        "failures": failures,
        "summaries": summaries,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
