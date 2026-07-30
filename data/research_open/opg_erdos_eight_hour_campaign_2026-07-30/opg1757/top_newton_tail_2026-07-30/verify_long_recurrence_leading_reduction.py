#!/usr/bin/env python3
"""Exact finite search for the long-recurrence leading coefficients.

The generating-function reduction is proved in the accompanying note.
This script searches for a sign counterexample using exact fractions;
absence of one is not treated as an all-rank positivity proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction


def odd_double_factorial(value: int) -> int:
    result = 1
    for factor in range(1, value + 1, 2):
        result *= factor
    return result


def ordinary_laurent_layers(maximum_rank: int):
    c = [Fraction(0) for _ in range(maximum_rank + 1)]
    delta = [Fraction(0) for _ in c]
    epsilon = [Fraction(0) for _ in c]
    c[0] = Fraction(1)
    for rank in range(1, maximum_rank + 1):
        c[rank] = Fraction(
            (-1) ** (rank + 1)
            * odd_double_factorial(6 * rank - 3),
            9**rank * math.factorial(2 * rank),
        )
        delta[rank] = (
            -Fraction(6 * rank, 6 * rank - 5) * c[rank]
        )
        if rank >= 2:
            epsilon[rank] = -6 * (rank - 1) * c[rank - 1]
    return c, delta, epsilon


def falling_leading_coefficients(maximum_rank: int):
    c, delta, epsilon = ordinary_laurent_layers(maximum_rank + 2)
    result = []
    for rank in range(maximum_rank + 1):
        central_rank = rank + 2
        highest_layer = sum(
            delta[left] * delta[central_rank - left]
            - c[left] * epsilon[central_rank - left]
            for left in range(central_rank + 1)
        )
        result.append(
            highest_layer
            / (2 * math.factorial(3 * rank))
        )
    return result


def recurrence_leading_coefficients(falling):
    result = []
    for band in range(len(falling) - 1):
        value = -3 * (band + 1) * falling[band + 1]
        value -= sum(
            result[index] * falling[band - index]
            for index in range(band)
        )
        result.append(value)
    return result


def audit(maximum_band: int = 300):
    falling = falling_leading_coefficients(maximum_band)
    recurrence = recurrence_leading_coefficients(falling)

    expected_falling = [
        Fraction(1),
        Fraction(-11, 18),
        Fraction(143, 2592),
        Fraction(-3169, 1679616),
        Fraction(81037, 2418647040),
        Fraction(-110567, 304749527040),
    ]
    assert falling[: len(expected_falling)] == expected_falling
    expected_recurrence = [
        Fraction(11, 6),
        Fraction(341, 432),
        Fraction(74317, 186624),
        Fraction(13629341, 67184640),
        Fraction(175122877, 1693052928),
    ]
    assert recurrence[: len(expected_recurrence)] == expected_recurrence

    counterexamples = [
        band
        for band, value in enumerate(recurrence)
        if value <= 0
    ]
    payload = ";".join(
        f"{index}:{value.numerator}/{value.denominator}"
        for index, value in enumerate(recurrence)
    )
    return {
        "schema": "amra.opg1757.long-recurrence-leading-search.v1",
        "status": (
            "NO_COUNTEREXAMPLE_FINITE_EXACT_SEARCH"
            if not counterexamples
            else "COUNTEREXAMPLE_FOUND"
        ),
        "scope": (
            "Exact finite search only. All-rank positivity is reduced "
            "to negative nonconstant coefficients of log H(z)."
        ),
        "maximum_band": maximum_band - 1,
        "counterexample_bands": counterexamples,
        "first_falling_leading_coefficients": [
            str(value) for value in falling[:6]
        ],
        "first_recurrence_leading_coefficients": [
            str(value) for value in recurrence[:10]
        ],
        "last_recurrence_leading_coefficient": str(recurrence[-1]),
        "recurrence_coefficients_sha256": hashlib.sha256(
            payload.encode("ascii")
        ).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-band", type=int, default=299)
    arguments = parser.parse_args()
    if arguments.maximum_band < 0:
        raise ValueError("maximum band must be nonnegative")
    print(json.dumps(
        audit(arguments.maximum_band + 1),
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
