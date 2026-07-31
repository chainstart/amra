#!/usr/bin/env python3
"""Independent polynomial-identity certificate for the OPG q=5 layer.

This module does not import ``verify_sixth_q5``.  It uses the primitive
page-transfer/Newton engine from the earlier campaign and independently
transcribes the eleven proposed formulas.

The fixed-deficit degree theorem gives ``deg R_(5,r) <= r+12``.  The proved
boundary factor ``(s-4)(s-5)`` reduces the quotient degree to at most r+10,
so exactly r+11 non-boundary values certify offset r.  The eleven offsets
therefore require 176 values, with largest sample s=26.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path


def expected_normalized_layers(s: int) -> tuple[Fraction, ...]:
    return (
        Fraction(
            (s - 5)
            * (s - 4)
            * (
                s**8
                + 29 * s**7
                + 321 * s**6
                + 459 * s**5
                - 23239 * s**4
                - 161291 * s**3
                + 565356 * s**2
                + 5972364 * s
                - 18174240
            ),
            30,
        ),
        Fraction(
            (s - 5)
            * (s - 4)
            * (
                3 * s**8
                + 68 * s**7
                + 504 * s**6
                - 1638 * s**5
                - 45762 * s**4
                - 122342 * s**3
                + 1328907 * s**2
                + 3955734 * s
                - 18174240
            ),
            9,
        ),
        Fraction(
            (s - 5)
            * (s - 4)
            * (
                30 * s**8
                + 489 * s**7
                + 1507 * s**6
                - 27821 * s**5
                - 221251 * s**4
                + 486683 * s**3
                + 6647577 * s**2
                - 10477962 * s
                - 22921920
            ),
            18,
        ),
        Fraction(
            4
            * (s - 5)
            * (s - 4)
            * (
                60 * s**8
                + 600 * s**7
                - 1660 * s**6
                - 47888 * s**5
                - 67659 * s**4
                + 1513961 * s**3
                + 1517269 * s**2
                - 20404086 * s
                + 21846888
            ),
            45,
        ),
        Fraction(
            (s - 5)
            * (s - 4)
            * (
                540 * s**8
                + 2040 * s**7
                - 35935 * s**6
                - 208854 * s**5
                + 1192098 * s**4
                + 6034869 * s**3
                - 29097509 * s**2
                - 883302 * s
                + 73389888
            ),
            45,
        ),
        Fraction(
            2
            * (s - 5)
            * (s - 4)
            * (
                444 * s**8
                - 1044 * s**7
                - 29951 * s**6
                + 35449 * s**5
                + 1048166 * s**4
                - 2139865 * s**3
                - 11917920 * s**2
                + 40844052 * s
                - 29418336
            ),
            45,
        ),
        Fraction(
            (s - 5)
            * (s - 4)
            * (2 * s - 11)
            * (
                108 * s**7
                - 312 * s**6
                - 5189 * s**5
                + 13371 * s**4
                + 106278 * s**3
                - 396539 * s**2
                + 84492 * s
                + 609444
            ),
            9,
        ),
        Fraction(
            4
            * (s - 5)
            * (s - 4)
            * (2 * s - 11)
            * (2 * s - 9)
            * (
                12 * s**6
                - 52 * s**5
                - 365 * s**4
                + 1758 * s**3
                + 2151 * s**2
                - 16288 * s
                + 15300
            ),
            9,
        ),
        Fraction(
            (s - 5)
            * (s - 4)
            * (2 * s - 11)
            * (2 * s - 9)
            * (
                300 * s**6
                - 3060 * s**5
                + 4025 * s**4
                + 50419 * s**3
                - 194938 * s**2
                + 175488 * s
                + 64656
            ),
            90,
        ),
        Fraction(
            (s - 5)
            * (s - 4)
            * (2 * s - 11)
            * (2 * s - 9)
            * (2 * s - 7)
            * (s**2 - s - 8)
            * (30 * s**3 - 345 * s**2 + 1255 * s - 1398),
            45,
        ),
        Fraction(
            (s - 5)
            * (s - 4) ** 2
            * (s - 3)
            * (2 * s - 11)
            * (2 * s - 9)
            * (2 * s - 7)
            * (12 * s**3 - 136 * s**2 + 469 * s - 446),
            90,
        ),
    )


def primitive_q5_coefficients(s: int) -> dict[int, int]:
    research_open = Path(__file__).resolve().parents[2]
    primitive_dir = (
        research_open / "q1_eight_hour_campaign_2026-07-29" / "opg1757"
    )
    sys.path.insert(0, str(primitive_dir))
    try:
        from tp2_barrier_search import pooled_t_newton_rows
    finally:
        sys.path.pop(0)
    depth = 2 * s - 10
    return {
        int(degree): int(coefficient)
        for row_depth, degree, coefficient in pooled_t_newton_rows(
            s, 4 * s - 8
        )
        if int(row_depth) == depth
    }


@lru_cache(maxsize=1)
def audit_rational_q5_certificate(
    sample_start: int = 6,
) -> tuple[tuple[int, int, int], ...]:
    maximum_s = max(
        sample_start + (offset + 11) - 1 for offset in range(11)
    )
    primitive = {
        s: primitive_q5_coefficients(s)
        for s in range(sample_start, maximum_s + 1)
    }
    rows: list[tuple[int, int, int]] = []
    for offset in range(11):
        required = offset + 11
        for s in range(sample_start, sample_start + required):
            depth = 2 * s - 10
            degree = 4 * s - 20 + offset
            raw = primitive[s].get(degree, 0)
            measured_numerator = Fraction(
                raw, math.factorial(depth)
            ) / (Fraction(s) ** (2 * s - 18))
            proposed_numerator = (
                Fraction(s) ** offset
                * expected_normalized_layers(s)[offset]
            )
            if measured_numerator != proposed_numerator:
                raise AssertionError(
                    "independent q=5 rational-certificate mismatch at "
                    f"(s,r)=({s},{offset}): "
                    f"{measured_numerator} != {proposed_numerator}"
                )
            rows.append((s, offset, raw))
    if len(rows) != 176:
        raise AssertionError("q=5 coefficient certificate count changed")
    boundary = primitive_q5_coefficients(5)
    if boundary:
        raise AssertionError(f"q=5 boundary B_0 was nonzero: {boundary}")
    return tuple(rows)


def main() -> None:
    rows = audit_rational_q5_certificate()
    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    print(
        json.dumps(
            {
                "status": "PASS",
                "schema": "amra.opg1757.q5.independent.v1",
                "coefficient_values": len(rows),
                "offsets": 11,
                "s_range": [
                    min(row[0] for row in rows),
                    max(row[0] for row in rows),
                ],
                "boundary": "B_0(5,beta)=0",
                "boundary_factor": "(s-4)*(s-5)",
                "sha256": hashlib.sha256(payload).hexdigest(),
                "scope": (
                    "q=5 complete-split pooled layer only; no arbitrary-q "
                    "positivity or arbitrary-host conclusion"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
