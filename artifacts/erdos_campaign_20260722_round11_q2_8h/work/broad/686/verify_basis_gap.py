#!/usr/bin/env python3
"""Reproduce the #686 monomial/Mahler basis gap at fixed parameters."""

from __future__ import annotations

import json
from math import factorial
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(
    ROOT / "artifacts/erdos_campaign_20260722_round10_4h/work/mixed"
))

from higher_cartier_mahler_certificates import (  # noqa: E402
    c_polynomial,
    certify,
    oddpart,
    v2_fraction,
    v2_integer,
)


def main() -> None:
    rows = []
    for m in (16, 24, 32, 40, 48, 56, 64):
        odd = oddpart(m)
        target = m - 2 * odd - v2_integer(factorial(odd))
        normalized_monomial_v2 = [
            v2_fraction(coefficient) - target
            for coefficient in c_polynomial(m)
            if coefficient
        ]
        certificate = certify(m)
        assert certificate["target_v2_C_m"] == target
        assert certificate["all_positive_order_coefficients_even"]
        assert min(normalized_monomial_v2) < 0
        rows.append({
            "m": m,
            "target_v2": target,
            "minimum_normalized_monomial_v2": min(normalized_monomial_v2),
            "negative_normalized_monomial_coefficients": sum(
                value < 0 for value in normalized_monomial_v2
            ),
            "mahler_all_integer_and_parity_certificate": True,
        })
    print(json.dumps({
        "schema": "amra.erdos686.cartier-basis-gap.v1",
        "status": "PASS",
        "rows": rows,
        "scope_warning": "Exact fixed-m certificates; no uniform-m inference.",
    }, indent=2))


if __name__ == "__main__":
    main()
