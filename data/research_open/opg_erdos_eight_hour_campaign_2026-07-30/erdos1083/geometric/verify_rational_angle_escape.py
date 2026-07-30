#!/usr/bin/env python3
"""Exact regression for the rational-angle escape theorem."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction


def chebyshev(value: Fraction, index: int) -> Fraction:
    if index < 0:
        raise ValueError("index must be nonnegative")
    if index == 0:
        return Fraction(1)
    if index == 1:
        return value
    left, right = Fraction(1), value
    for _ in range(2, index + 1):
        left, right = right, 2 * value * right - left
    return right


def valuation(value: int, prime: int) -> int:
    if value == 0:
        raise ValueError("valuation of zero is not used")
    result = 0
    value = abs(value)
    while value % prime == 0:
        result += 1
        value //= prime
    return result


def rational_valuation(value: Fraction, prime: int) -> int:
    return valuation(value.numerator, prime) - valuation(
        value.denominator, prime
    )


def two_power_denominator_audit(
    maximum_e: int, maximum_k: int
) -> list[dict[str, int]]:
    records = []
    for e in range(2, maximum_e + 1):
        denominator = 2**e
        for a in range(1, denominator, 2):
            for k in range(1, maximum_k + 1):
                value = chebyshev(Fraction(a, denominator), k)
                expected = (e - 1) * k + 1
                if value.denominator != 2**expected:
                    raise AssertionError(
                        (a, e, k, value, expected)
                    )
                difference = 1 - value
                if difference.denominator != 2**expected:
                    raise AssertionError(
                        ("difference", a, e, k, difference, expected)
                    )
            records.append(
                {
                    "numerator": a,
                    "denominator_exponent": e,
                    "checked_k": maximum_k,
                }
            )
    return records


def odd_prime_audit(maximum_k: int) -> list[dict[str, int]]:
    cases = (
        (2, 3, 3),
        (3, 5, 5),
        (5, 12, 3),
        (7, 18, 3),
        (11, 30, 5),
    )
    records = []
    for a, b, prime in cases:
        if math.gcd(a, b) != 1 or b % prime:
            raise AssertionError((a, b, prime))
        e = valuation(b, prime)
        for k in range(1, maximum_k + 1):
            difference = 1 - chebyshev(Fraction(a, b), k)
            if rational_valuation(difference, prime) != -e * k:
                raise AssertionError((a, b, prime, k, difference))
        records.append(
            {
                "numerator": a,
                "denominator": b,
                "prime": prime,
                "checked_k": maximum_k,
            }
        )
    return records


def distance_denominator_audit() -> list[dict[str, int]]:
    cases = (
        (6, 9, 3, 2),
        (12, 11, 5, 3),
        (20, 13, 7, 3),
    )
    records = []
    for m, angular_size, a, e in cases:
        if abs(a) >= 2**e:
            raise AssertionError("the audited rational must be a cosine")
        cosine = Fraction(a, 2**e)
        threshold = (2 * valuation(m, 2)) // (e - 1)
        seen_denominators = set()
        for k in range(threshold + 1, angular_size):
            values = {
                Fraction(d * d)
                + 2 * m * m * (1 - chebyshev(cosine, k))
                for d in range(m)
            }
            if len(values) != m:
                raise AssertionError((m, angular_size, a, e, k))
            denominators = {value.denominator for value in values}
            expected = {2 ** ((e - 1) * k - 2 * valuation(m, 2))}
            if denominators != expected:
                raise AssertionError(
                    (m, angular_size, a, e, k, denominators, expected)
                )
            if seen_denominators & denominators:
                raise AssertionError("different k layers collided")
            seen_denominators |= denominators
        records.append(
            {
                "height_count": m,
                "angular_size": angular_size,
                "cosine_numerator": a,
                "cosine_denominator_exponent": e,
                "usable_layers": max(0, angular_size - 1 - threshold),
            }
        )
    return records


def audit(maximum_e: int = 6, maximum_k: int = 18) -> dict[str, object]:
    return {
        "schema": "amra.erdos1083.rational-angle-escape.v1",
        "scope": (
            "Finite exact regression of the human p-adic denominator "
            "proof; not an unconditional f_3 exponent improvement."
        ),
        "two_power_records": two_power_denominator_audit(
            maximum_e, maximum_k
        ),
        "odd_prime_records": odd_prime_audit(maximum_k),
        "distance_records": distance_denominator_audit(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-e", type=int, default=6)
    parser.add_argument("--maximum-k", type=int, default=18)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.maximum_e, args.maximum_k),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
