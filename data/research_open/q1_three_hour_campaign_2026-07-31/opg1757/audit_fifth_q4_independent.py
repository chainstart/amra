#!/usr/bin/env python3
"""Independent exact-value certificate for the OPG-1757 q=4 layer.

This module does not import ``verify_fifth_q4``.  It recomputes the pooled
row with the primitive page-transfer/Newton engine from the earlier campaign
and independently transcribes the nine proposed formulas.

The fixed-deficit theorem proves that, for offset r,

    R_(4,r)(s) = s**r C_(4,r)(s)

is a polynomial of degree at most r+10.  Hence r+11 primitive values prove
one proposed formula.  Starting at s=6, the nine offsets require exactly
135 values and have largest sample s=24.  This is an identity certificate
under the previously proved degree theorem, not merely a small finite audit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path


def expected_normalized_layers(s: int) -> tuple[Fraction, ...]:
    """Independent numeric transcription of the nine q=4 formulas."""

    return (
        Fraction(
            (s - 5)
            * (s - 4)
            * (
                s**6
                + 25 * s**5
                + 229 * s**4
                + 211 * s**3
                - 10101 * s**2
                - 36081 * s
                + 183330
            ),
            6,
        ),
        Fraction(
            4
            * (s - 5)
            * (s - 4)
            * (
                s**6
                + 19 * s**5
                + 111 * s**4
                - 321 * s**3
                - 5409 * s**2
                - 3867 * s
                + 61110
            ),
            3,
        ),
        Fraction(
            2
            * (s - 5)
            * (s - 4)
            * (
                24 * s**6
                + 312 * s**5
                + 565 * s**4
                - 11427 * s**3
                - 42073 * s**2
                + 165669 * s
                + 98280
            ),
            9,
        ),
        Fraction(
            4
            * (s - 5)
            * (s - 4)
            * (
                50 * s**6
                + 355 * s**5
                - 1420 * s**4
                - 16156 * s**3
                + 21221 * s**2
                + 186954 * s
                - 305424
            ),
            15,
        ),
        Fraction(
            (s - 5)
            * (s - 4)
            * (
                68 * s**6
                + 88 * s**5
                - 3185 * s**4
                - 3446 * s**3
                + 64500 * s**2
                - 77429 * s
                - 68112
            ),
            3,
        ),
        Fraction(
            4
            * (s - 5)
            * (s - 4)
            * (
                60 * s**6
                - 264 * s**5
                - 1967 * s**4
                + 10074 * s**3
                + 10232 * s**2
                - 96345 * s
                + 103680
            ),
            9,
        ),
        Fraction(
            8
            * (s - 5)
            * (s - 4)
            * (2 * s - 9)
            * (
                4 * s**5
                - 22 * s**4
                - 54 * s**3
                + 489 * s**2
                - 704 * s
                - 18
            ),
            3,
        ),
        Fraction(
            4
            * (s - 5)
            * (s - 4)
            * (2 * s - 9)
            * (2 * s - 7)
            * (s**2 - s - 8)
            * (2 * s**2 - 13 * s + 19),
            3,
        ),
        Fraction(
            (s - 5)
            * (s - 4)
            * (s - 3)
            * (2 * s - 9)
            * (2 * s - 7)
            * (
                60 * s**3
                - 600 * s**2
                + 1865 * s
                - 1706
            ),
            90,
        ),
    )


def expected_q4_coefficients(s: int) -> dict[int, int]:
    if s < 5:
        raise ValueError("q=4 has nonnegative depth only for s>=5")
    depth = 2 * s - 9
    result: dict[int, int] = {}
    for offset, polynomial in enumerate(expected_normalized_layers(s)):
        value = (
            Fraction(math.factorial(depth))
            * Fraction(s) ** (2 * s - 16 + offset)
            * polynomial
        )
        if value.denominator != 1:
            raise AssertionError("q=4 formula was not integral")
        if value:
            result[4 * s - 18 + offset] = value.numerator
    return result


def primitive_q4_coefficients(s: int) -> dict[int, int]:
    """Recompute one q=4 row using the pre-existing primitive transfer."""

    research_open = Path(__file__).resolve().parents[2]
    primitive_dir = (
        research_open / "q1_eight_hour_campaign_2026-07-29" / "opg1757"
    )
    sys.path.insert(0, str(primitive_dir))
    try:
        from tp2_barrier_search import pooled_t_newton_rows
    finally:
        sys.path.pop(0)
    depth = 2 * s - 9
    return {
        int(degree): int(coefficient)
        for row_depth, degree, coefficient in pooled_t_newton_rows(
            s, 4 * s - 8
        )
        if int(row_depth) == depth
    }


@lru_cache(maxsize=1)
def audit_rational_q4_certificate(
    sample_start: int = 6,
) -> tuple[tuple[int, int, int], ...]:
    """Check the r+11 values required for each of the nine offsets."""

    maximum_s = max(
        sample_start + (offset + 11) - 1 for offset in range(9)
    )
    primitive = {
        s: primitive_q4_coefficients(s)
        for s in range(sample_start, maximum_s + 1)
    }
    rows: list[tuple[int, int, int]] = []
    for offset in range(9):
        required = offset + 11
        for s in range(sample_start, sample_start + required):
            depth = 2 * s - 9
            degree = 4 * s - 18 + offset
            raw = primitive[s].get(degree, 0)
            normalized_numerator = Fraction(
                raw, math.factorial(depth)
            ) / (Fraction(s) ** (2 * s - 16))
            proposed_numerator = (
                Fraction(s) ** offset
                * expected_normalized_layers(s)[offset]
            )
            if normalized_numerator != proposed_numerator:
                raise AssertionError(
                    "independent q=4 rational-certificate mismatch at "
                    f"(s,r)=({s},{offset}): "
                    f"{normalized_numerator} != {proposed_numerator}"
                )
            rows.append((s, offset, raw))
    if len(rows) != 135:
        raise AssertionError("q=4 coefficient certificate count changed")

    boundary = primitive_q4_coefficients(5)
    if boundary:
        raise AssertionError(f"q=4 boundary B_1 was nonzero: {boundary}")
    return tuple(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-start", type=int, default=6)
    args = parser.parse_args()
    rows = audit_rational_q4_certificate(args.sample_start)
    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    print(
        json.dumps(
            {
                "status": "PASS",
                "schema": "amra.opg1757.q4.independent.v1",
                "coefficient_values": len(rows),
                "offsets": 9,
                "s_range": [
                    min(row[0] for row in rows),
                    max(row[0] for row in rows),
                ],
                "boundary": "B_1(5,beta)=0",
                "sha256": hashlib.sha256(payload).hexdigest(),
                "scope": (
                    "q=4 complete-split pooled layer only; no arbitrary-q "
                    "or arbitrary-host conclusion"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
