#!/usr/bin/env python3
"""Independent replay of exact identities and the reported finite maximiser."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path


def primes_upto(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = b"\x00" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


def digit_carry_free(n: int, p: int) -> bool:
    half = (p - 1) // 2
    while n:
        if n % p > half:
            return False
        n //= p
    return True


def legendre_valuation(n: int, p: int) -> int:
    valuation = 0
    power = p
    while power <= 2 * n:
        valuation += (2 * n) // power - 2 * (n // power)
        power *= p
    return valuation


def interval_predicate(n: int, p: int) -> bool:
    if p * p <= 2 * n:
        raise ValueError("one-level interval predicate used outside its exact range")
    q = n // p
    return 2 * (n - q * p) < p


def direct_mass(n: int) -> tuple[list[int], Fraction]:
    accepted = [p for p in primes_upto(n) if legendre_valuation(n, p) == 0]
    return accepted, sum((Fraction(1, p) for p in accepted), Fraction())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.evidence.read_text())
    maximum = payload["maximum"]
    n = int(maximum["n"])
    accepted, exact_mass = direct_mass(n)
    assert accepted == payload["accepted_primes_at_maximum"]
    assert abs(float(exact_mass) - float(maximum["value"])) < 2e-11
    for test_n in range(1, 5000):
        for p in primes_upto(test_n):
            by_digits = digit_carry_free(test_n, p)
            by_valuation = legendre_valuation(test_n, p) == 0
            assert by_digits == by_valuation, (test_n, p)
            if p * p > 2 * test_n:
                assert by_digits == interval_predicate(test_n, p), (test_n, p)
    witness = payload["single_top_power_test"]
    witness_n = int(witness["n"])
    witness_p = int(witness["p"])
    top = int(witness["top_power"])
    bad = int(witness["bad_lower_power"])
    assert 2 * (witness_n % top) < top
    assert 2 * (witness_n % bad) >= bad
    assert not digit_carry_free(witness_n, witness_p)
    print(
        json.dumps(
            {
                "verified": True,
                "maximum_n": n,
                "maximum_float": float(exact_mass),
                "maximum_exact": f"{exact_mass.numerator}/{exact_mass.denominator}",
                "accepted_prime_count": len(accepted),
                "identity_replay_n": 4999,
                "claims_not_verified": [
                    "that n=3250 remains maximal beyond the finite max_n_scanned",
                    "that the public reciprocal sum is uniformly bounded",
                ],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
