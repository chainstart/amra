#!/usr/bin/env python3
"""Exact rational audit of the exponent margins in the strengthened corollary."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def f(q: Fraction) -> str:
    return f"{q.numerator}/{q.denominator}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    c = Fraction(1, 16)
    theta_lower = Fraction(2, 5)
    theta_upper = Fraction(3, 5)

    # For r <= (2c+o(1)) log(k)/loglog(k), the first two Konyagin
    # errors are at most (log k)^(-(1-theta)/(6c+o(1))).
    first_two_uniform_margin = (1 - theta_upper) - 6 * c
    # The third error is at most (log k)^(-1/(12c+o(1))).
    third_uniform_margin = 1 - 12 * c
    # The additive lambda*r exponent at r=3 is (9-2theta)/21;
    # comparison with theta is (23theta-9)/21.
    additive_uniform_margin = (23 * theta_lower - 9) / 21

    assert first_two_uniform_margin > 0
    assert third_uniform_margin > 0
    assert additive_uniform_margin > 0

    result = {
        "schema_version": "erdos451.constant_optimization.audit.v1",
        "status": "pass",
        "explicit_c": f(c),
        "theta_interval": [f(theta_lower), f(theta_upper)],
        "exact_margins": {
            "first_two_errors": f(first_two_uniform_margin),
            "third_error": f(third_uniform_margin),
            "additive_lambda_r": f(additive_uniform_margin),
        },
        "parametric_condition": "c < min((1-theta)/6, 1/12)",
        "scope": (
            "Checks the exact exponent comparisons after Theorem 4.1 of "
            "arXiv:2606.19863; the cited Konyagin and short-prime-interval inputs "
            "remain external dependencies."
        ),
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
