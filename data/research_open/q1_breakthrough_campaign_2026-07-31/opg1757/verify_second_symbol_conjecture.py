#!/usr/bin/env python3
"""Exact q<=6 evidence for the candidate universal second symbol."""

from __future__ import annotations

import json
import math
import pathlib
import sys

import sympy as sp


HERE = pathlib.Path(__file__).resolve().parent
OLD = (
    HERE.parents[1]
    / "q1_three_hour_campaign_2026-07-31"
    / "opg1757"
)
sys.path.insert(0, str(OLD))


def audit() -> dict[str, object]:
    import verify_fifth_q4 as q4
    import verify_fourth_q3 as q3
    import verify_second_deficit as q2
    import verify_seventh_q6 as q6
    import verify_sixth_q5 as q5

    s = q2.S
    z = sp.symbols("z")
    atom = 1 + 2 * z + 2 * z**2
    arrays: dict[int, tuple[sp.Expr, ...]] = {
        1: (
            4 * (s**2 + 4 * s - 24),
            8 * (s**2 - s - 8),
            4 * (s - 2) * (2 * s - 7),
        ),
        2: q2.EXPECTED_NORMALIZED_LAYERS,
        3: q3.EXPECTED_Q3_NORMALIZED_LAYERS,
        4: q4.EXPECTED_Q4_NORMALIZED_LAYERS,
        5: q5.EXPECTED_Q5_NORMALIZED_LAYERS,
        6: q6.EXPECTED_Q6_NORMALIZED_LAYERS,
    }

    checked = 0
    rows = []
    for deficit, expressions in arrays.items():
        measured = sum(
            sp.Poly(sp.cancel(expression), s).coeff_monomial(
                s ** (2 * deficit - 1)
            )
            * z**offset
            for offset, expression in enumerate(expressions)
        )
        defect = deficit * (
            4
            - sp.Rational(2 * (deficit - 10), 3) * z
            - (3 * deficit + 4) * z**2
            - 2 * (2 * deficit + 11) * z**3
            - sp.Rational(2 * (4 * deficit + 29), 3) * z**4
        )
        expected = sp.cancel(
            sp.Rational(4, math.factorial(deficit))
            * atom ** (deficit - 2)
            * defect
        )
        if sp.cancel(measured - expected) != 0:
            raise AssertionError(
                f"second-symbol conjecture fails at q={deficit}"
            )
        checked += len(expressions)
        rows.append([deficit, str(sp.factor(measured))])

    return {
        "schema": "amra.opg1757.second-symbol-conjecture.v1",
        "status": "PASS",
        "claim_status": "COMPUTATIONAL_CONJECTURE",
        "deficits_checked": list(arrays),
        "exact_coefficients_checked": checked,
        "rows": rows,
        "firewall": "no arbitrary-q claim; q<=6 exact evidence only",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
