#!/usr/bin/env python3
"""Independent rational-identity certificate for the OPG q=6 layer.

This file deliberately does not import ``verify_seventh_q6``.  It transcribes
the thirteen proposed formulas and recomputes coefficients with the older
page-transfer/Newton engine.  The endpoint top-two theorem gives
``deg R_(6,r) <= 12+r``; division by the proved factor
``(s-4)(s-5)(s-6)`` leaves degree at most ``9+r``.  Thus ``10+r`` values
certify offset r, for 208 values in total and largest sample ``s=28``.
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
    boundary = (s - 6) * (s - 5) * (s - 4)
    return (
        Fraction(
            boundary
            * (
                s**9
                + 39 * s**8
                + 667 * s**7
                + 5064 * s**6
                - 10918 * s**5
                - 512106 * s**4
                - 2462113 * s**3
                + 15195399 * s**2
                + 108066951 * s
                - 385491960
            ),
            180,
        ),
        Fraction(
            boundary
            * (
                3 * s**9
                + 97 * s**8
                + 1309 * s**7
                + 5982 * s**6
                - 57396 * s**5
                - 834688 * s**4
                - 1331401 * s**3
                + 27140127 * s**2
                + 71718471 * s
                - 385491960
            ),
            45,
        ),
        Fraction(
            boundary
            * (
                36 * s**9
                + 922 * s**8
                + 8823 * s**7
                + 2697 * s**6
                - 647927 * s**5
                - 3900203 * s**4
                + 12372203 * s**3
                + 136241377 * s**2
                - 161376108 * s
                - 762037920
            ),
            90,
        ),
        Fraction(
            boundary
            * (
                630 * s**9
                + 11925 * s**8
                + 62010 * s**7
                - 515024 * s**6
                - 7196322 * s**5
                - 5179532 * s**4
                + 236824458 * s**3
                + 309695827 * s**2
                - 3320427270 * s
                + 2613794400
            ),
            405,
        ),
        Fraction(
            boundary
            * (
                780 * s**9
                + 9600 * s**8
                - 2795 * s**7
                - 743576 * s**6
                - 3024266 * s**5
                + 23040040 * s**4
                + 113327830 * s**3
                - 480942194 * s**2
                - 518446149 * s
                + 2114358750
            ),
            180,
        ),
        Fraction(
            2
            * boundary
            * (
                1428 * s**9
                + 8232 * s**8
                - 88109 * s**7
                - 881706 * s**6
                + 2148874 * s**5
                + 34670526 * s**4
                - 60290564 * s**3
                - 504561798 * s**2
                + 1398747555 * s
                - 575672202
            ),
            315,
        ),
        Fraction(
            boundary
            * (
                1968 * s**9
                - 1368 * s**8
                - 152196 * s**7
                - 177962 * s**6
                + 6502782 * s**5
                + 4420408 * s**4
                - 154686372 * s**3
                + 244336501 * s**2
                + 508123992 * s
                - 1041647256
            ),
            135,
        ),
        Fraction(
            2
            * boundary
            * (
                408 * s**9
                - 2884 * s**8
                - 21246 * s**7
                + 148389 * s**6
                + 709230 * s**5
                - 5314587 * s**4
                - 3005613 * s**3
                + 71300470 * s**2
                - 138576132 * s
                + 62098560
            ),
            45,
        ),
        Fraction(
            boundary
            * (2 * s - 11)
            * (
                1560 * s**8
                - 12260 * s**7
                - 48130 * s**6
                + 519793 * s**5
                + 526163 * s**4
                - 11229722 * s**3
                + 21034223 * s**2
                + 14038365 * s
                - 45227700
            ),
            180,
        ),
        Fraction(
            boundary
            * (2 * s - 11)
            * (2 * s - 9)
            * (
                420 * s**7
                - 4020 * s**6
                - 2565 * s**5
                + 119107 * s**4
                - 214808 * s**3
                - 906217 * s**2
                + 3037523 * s
                - 2155500
            ),
            135,
        ),
        Fraction(
            boundary
            * (2 * s - 11)
            * (2 * s - 9)
            * (
                144 * s**7
                - 2264 * s**6
                + 10144 * s**5
                + 11306 * s**4
                - 208341 * s**3
                + 525041 * s**2
                - 290924 * s
                - 271056
            ),
            90,
        ),
        Fraction(
            boundary
            * (2 * s - 11)
            * (2 * s - 9) ** 2
            * (2 * s - 7)
            * (s**2 - s - 8)
            * (6 * s**3 - 77 * s**2 + 307 * s - 358),
            45,
        ),
        Fraction(
            boundary
            * (s - 3)
            * (2 * s - 11)
            * (2 * s - 9)
            * (2 * s - 7)
            * (
                504 * s**5
                - 10836 * s**4
                + 90342 * s**3
                - 360955 * s**2
                + 677187 * s
                - 457250
            ),
            11340,
        ),
    )


def primitive_q6_coefficients(s: int) -> dict[int, int]:
    """Recompute a q=6 row with the pre-existing primitive transfer."""

    research_open = Path(__file__).resolve().parents[2]
    primitive_dir = (
        research_open / "q1_eight_hour_campaign_2026-07-29" / "opg1757"
    )
    sys.path.insert(0, str(primitive_dir))
    try:
        from tp2_barrier_search import pooled_t_newton_rows
    finally:
        sys.path.pop(0)
    depth = 2 * s - 11
    return {
        int(degree): int(coefficient)
        for row_depth, degree, coefficient in pooled_t_newton_rows(
            s, 4 * s - 8
        )
        if int(row_depth) == depth
    }


@lru_cache(maxsize=1)
def audit_rational_q6_certificate(
    sample_start: int = 7,
) -> tuple[tuple[int, int, int], ...]:
    maximum_s = max(
        sample_start + (offset + 10) - 1 for offset in range(13)
    )
    primitive = {
        s: primitive_q6_coefficients(s)
        for s in range(sample_start, maximum_s + 1)
    }
    rows: list[tuple[int, int, int]] = []
    for offset in range(13):
        required = offset + 10
        for s in range(sample_start, sample_start + required):
            depth = 2 * s - 11
            degree = 4 * s - 22 + offset
            raw = primitive[s].get(degree, 0)
            measured_numerator = Fraction(
                raw, math.factorial(depth)
            ) / (Fraction(s) ** (2 * s - 20))
            proposed_numerator = (
                Fraction(s) ** offset
                * expected_normalized_layers(s)[offset]
            )
            if measured_numerator != proposed_numerator:
                raise AssertionError(
                    "independent q=6 rational-certificate mismatch at "
                    f"(s,r)=({s},{offset}): "
                    f"{measured_numerator} != {proposed_numerator}"
                )
            rows.append((s, offset, raw))
    if len(rows) != 208:
        raise AssertionError("q=6 coefficient certificate count changed")
    boundary = primitive_q6_coefficients(6)
    if boundary:
        raise AssertionError(f"q=6 boundary B_1 was nonzero: {boundary}")
    return tuple(rows)


def main() -> None:
    rows = audit_rational_q6_certificate()
    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    print(
        json.dumps(
            {
                "status": "PASS",
                "schema": "amra.opg1757.q6.independent.v1",
                "coefficient_values": len(rows),
                "offsets": 13,
                "s_range": [
                    min(row[0] for row in rows),
                    max(row[0] for row in rows),
                ],
                "boundary": "B_1(6,beta)=0",
                "degree_bound": "deg R_(6,r) <= 12+r",
                "boundary_factor": "(s-4)*(s-5)*(s-6)",
                "quotient_degree_bound": "deg(R/F_6) <= 9+r",
                "sha256": hashlib.sha256(payload).hexdigest(),
                "scope": (
                    "q=6 complete-split pooled layer only; no arbitrary-q "
                    "positivity or arbitrary-host conclusion"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
