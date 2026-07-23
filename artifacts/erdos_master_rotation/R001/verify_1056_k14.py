#!/usr/bin/env python3
"""Independently verify the published finite k=14 witness for Erdős #1056."""

from __future__ import annotations

import argparse
import json
from math import isqrt
from pathlib import Path


PRIME = 10_428_007
EXPECTED_RESIDUE = 8_978_998
ENDPOINTS = [
    816_488,
    1_251_081,
    3_384_225,
    4_112_650,
    4_237_275,
    4_431_559,
    4_467_010,
    4_835_062,
    7_328_694,
    7_385_077,
    7_415_726,
    8_460_938,
    8_689_396,
    9_295_594,
    9_661_614,
]


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    if number % 2 == 0:
        return number == 2
    for divisor in range(3, isqrt(number) + 1, 2):
        if number % divisor == 0:
            return False
    return True


def verify() -> dict[str, object]:
    endpoint_set = set(ENDPOINTS)
    residues: dict[int, int] = {}
    factorial = 1
    for value in range(1, ENDPOINTS[-1] + 1):
        factorial = factorial * value % PRIME
        if value in endpoint_set:
            residues[value] = factorial

    endpoint_residues = [residues[value] for value in ENDPOINTS]
    intervals: list[dict[str, int | bool]] = []
    for left, right in zip(ENDPOINTS, ENDPOINTS[1:]):
        product = residues[right] * pow(residues[left], -1, PRIME) % PRIME
        intervals.append(
            {
                "left": left + 1,
                "right": right,
                "product_mod_p": product,
                "verified_one": product == 1,
            }
        )

    prime_verified = is_prime(PRIME)
    same_residue = len(set(endpoint_residues)) == 1
    expected_residue = endpoint_residues[0] == EXPECTED_RESIDUE
    all_intervals_one = all(bool(row["verified_one"]) for row in intervals)
    passed = prime_verified and same_residue and expected_residue and all_intervals_one
    return {
        "schema_version": "amra.erdos1056.k14_verification.v1",
        "problem_id": "1056",
        "prime": PRIME,
        "prime_verified_by_trial_division": prime_verified,
        "endpoint_count": len(ENDPOINTS),
        "interval_count": len(intervals),
        "endpoints": ENDPOINTS,
        "common_factorial_residue": endpoint_residues[0],
        "expected_residue": EXPECTED_RESIDUE,
        "all_endpoint_residues_equal": same_residue,
        "expected_residue_verified": expected_residue,
        "all_interval_products_one": all_intervals_one,
        "intervals": intervals,
        "passed": passed,
        "scope_note": "This verifies only the finite case k=14 and hence every 2<=k<=14 by truncation; it does not address arbitrary k.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = verify()
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
