#!/usr/bin/env python3
"""Exact arithmetic audit of the rejected quasirandom route for #934.

This does not prove the group-theoretic normal form.  It verifies the rational
constant calculation and the universal incompatibility D >= 11r with the
already proved order bound N <= 2r^2-3r+2.
"""

from __future__ import annotations

from fractions import Fraction
import json


GAMMA = Fraction(253, 225)
COEFF = 11 * (GAMMA - 1) - GAMMA * GAMMA


def audit_r(r: int) -> dict[str, object]:
    a = r * r - r + 1
    n_upper = 2 * r * r - 3 * r + 2
    denominator = (GAMMA - 1) * r * r + r - 1
    threshold_upper = GAMMA * GAMMA * r**3 / denominator
    margin = 11 * denominator - GAMMA * GAMMA * r * r
    # D^2 <= N-1 and N <= n_upper; compare exactly with (11r)^2.
    dimension_margin = 121 * r * r - (n_upper - 1)
    return {
        "r": r,
        "a": a,
        "n_upper": n_upper,
        "n_upper_lt_2a": n_upper < 2 * a,
        "threshold_lt_11r": threshold_upper < 11 * r,
        "threshold_margin_num": margin.numerator,
        "threshold_margin_den": margin.denominator,
        "dimension_margin_positive": dimension_margin > 0,
    }


def main() -> None:
    records = [audit_r(r) for r in range(1, 10001)]
    assert COEFF == Fraction(5291, 50625)
    assert all(row["n_upper_lt_2a"] for row in records)
    assert all(row["threshold_lt_11r"] for row in records)
    assert all(row["dimension_margin_positive"] for row in records)
    print(json.dumps({
        "schema": "amra.erdos934.round8.quasirandom_vacuity.v1",
        "gamma": "253/225",
        "coefficient": f"{COEFF.numerator}/{COEFF.denominator}",
        "checked_r_interval": [1, 10000],
        "symbolic_identities": {
            "threshold_margin":
                "(5291/50625) r^2 + 11 r - 11 > 0",
            "dimension_obstruction":
                "D^2 <= N-1 <= 2r^2-3r+1 < 121r^2",
        },
        "result": "PASS_VACUOUS_ROUTE_REJECTED",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
