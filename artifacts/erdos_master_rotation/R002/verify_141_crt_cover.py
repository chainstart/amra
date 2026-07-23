#!/usr/bin/env python3
"""Verify a corrected CRT reduction for Erdős Problem #141.

The construction forces every non-progression position to be composite and
checks that the remaining k linear forms are locally admissible.  Simultaneous
prime values still require Schinzel's Hypothesis H / Dickson's conjecture, so
this is not an unconditional solution.
"""

from __future__ import annotations

import argparse
import json
from math import gcd
from pathlib import Path


def primes_through(limit: int) -> list[int]:
    primes: list[int] = []
    for candidate in range(2, limit + 1):
        if all(candidate % prime for prime in primes if prime * prime <= candidate):
            primes.append(candidate)
    return primes


def next_primes(start: int, count: int) -> list[int]:
    result: list[int] = []
    candidate = max(2, start)
    while len(result) < count:
        if all(candidate % divisor for divisor in range(2, int(candidate**0.5) + 1)):
            result.append(candidate)
        candidate += 1
    return result


def crt(congruences: list[tuple[int, int]]) -> tuple[int, int]:
    value = 0
    modulus = 1
    for residue, next_modulus in congruences:
        if gcd(modulus, next_modulus) != 1:
            raise ValueError("CRT moduli must be pairwise coprime")
        step = (residue - value) * pow(modulus, -1, next_modulus) % next_modulus
        value += modulus * step
        modulus *= next_modulus
        value %= modulus
    return value, modulus


def verify_k(k: int, local_prime_limit: int) -> dict[str, object]:
    small_primes = primes_through(k)
    difference = 1
    for prime in small_primes:
        difference *= prime
    gap_offsets = [
        offset
        for offset in range(1, (k - 1) * difference)
        if offset % difference
    ]
    cover_primes = next_primes((k - 1) * difference + 1, len(gap_offsets))
    cover = dict(zip(gap_offsets, cover_primes))
    congruences = [(1, prime) for prime in small_primes]
    congruences.extend((-offset % prime, prime) for offset, prime in cover.items())
    base, slope = crt(congruences)

    gaps_verified = all((base + offset) % prime == 0 for offset, prime in cover.items())
    fixed_moduli = small_primes + cover_primes
    target_nonzero_at_fixed_moduli = all(
        (base + index * difference) % prime != 0
        for index in range(k)
        for prime in fixed_moduli
    )

    local_rows: list[dict[str, object]] = []
    locally_admissible = True
    for prime in primes_through(local_prime_limit):
        forbidden_parameters = {
            parameter
            for parameter in range(prime)
            if any(
                (slope * parameter + base + index * difference) % prime == 0
                for index in range(k)
            )
        }
        row_ok = len(forbidden_parameters) < prime
        locally_admissible &= row_ok
        local_rows.append(
            {
                "prime": prime,
                "forbidden_parameter_count": len(forbidden_parameters),
                "admissible": row_ok,
            }
        )

    passed = gaps_verified and target_nonzero_at_fixed_moduli and locally_admissible
    return {
        "k": k,
        "difference": difference,
        "gap_offset_count": len(gap_offsets),
        "base": base,
        "slope": slope,
        "slope_decimal_digits": len(str(slope)),
        "gaps_verified": gaps_verified,
        "target_nonzero_at_fixed_moduli": target_nonzero_at_fixed_moduli,
        "locally_admissible_through": local_prime_limit,
        "local_admissibility_verified": locally_admissible,
        "local_rows": local_rows,
        "passed": passed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", default="3,4")
    parser.add_argument("--local-prime-limit", type=int, default=500)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    values = [int(part) for part in args.k.split(",") if part.strip()]
    rows = [verify_k(k, args.local_prime_limit) for k in values]
    payload = {
        "schema_version": "amra.erdos141.corrected_crt.v1",
        "problem_id": "141",
        "rows": rows,
        "passed": all(bool(row["passed"]) for row in rows),
        "scope_note": (
            "The CRT cover and local admissibility are unconditional. Infinitely "
            "many simultaneous prime values remain conditional on Hypothesis H."
        ),
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
