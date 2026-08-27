#!/usr/bin/env python3
"""Finite exact checks for the final-round quotient-gap zero-band lemma.

This is only an endpoint and indexing sanity check.  The asymptotic input in
the proof is the Baker--Harman--Pintz short-interval theorem, not this scan.
"""

from __future__ import annotations

import argparse
import bisect
from fractions import Fraction
from math import ceil, floor


def primes_below(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * limit
    if limit:
        sieve[0] = 0
    if limit > 1:
        sieve[1] = 0
    for p in range(2, int((limit - 1) ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p : limit : p] = b"\x00" * (
                ((limit - 1 - p * p) // p) + 1
            )
    return [p for p, flag in enumerate(sieve) if flag]


def first_odd_in_interval(lo: Fraction, hi: Fraction) -> int:
    t = ceil(lo)
    if t % 2 == 0:
        t += 1
    if t > floor(hi):
        raise AssertionError((lo, hi, t))
    return t


def chosen_gap(k: int, n: int) -> tuple[int, Fraction, Fraction, Fraction]:
    """Return t=2q+1 and the exact open gap (a,b), centered at x."""

    t = first_odd_in_interval(Fraction(4 * n, 3 * k), Fraction(3 * n, 2 * k))
    a = Fraction(2 * n - k, t)
    x = Fraction(2 * n, t)
    b = Fraction(2 * n + k, t)
    assert t >= 3 and t % 2 == 1
    assert Fraction(4 * k, 3) <= x <= Fraction(3 * k, 2)
    assert k < a < x < b < 2 * k
    return t, a, x, b


def zero_band_upper(k: int) -> int:
    """Largest N satisfying 4*N <= k**(59/40), using integers only."""

    target = k**59
    lo, hi = 0, k * k
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if (4 * mid) ** 40 <= target:
            lo = mid
        else:
            hi = mid - 1
    return lo


def violates_support(k: int, n: int, p: int) -> bool:
    """Check that no integer quotient satisfies 2|n-qp| <= p-k."""

    q0 = n // p
    return all(2 * abs(n - q * p) > p - k for q in (q0 - 1, q0, q0 + 1, q0 + 2))


def scan(k_values: list[int], max_n_per_k: int) -> None:
    rows = 0
    for k in k_values:
        primes = primes_below(2 * k + 1)
        primes = primes[bisect.bisect_right(primes, k) :]
        upper = zero_band_upper(k)
        lower = 12 * k
        if upper < lower:
            print(f"k={k}: asymptotic band empty at the conservative constant 1/4")
            continue
        span = upper - lower + 1
        if span <= max_n_per_k:
            samples = range(lower, upper + 1)
        else:
            samples = sorted(
                {
                    lower + (span - 1) * j // (max_n_per_k - 1)
                    for j in range(max_n_per_k)
                }
            )
        worst_margin = None
        for n in samples:
            _, a, _, b = chosen_gap(k, n)
            left = bisect.bisect_right(primes, a)
            if left == len(primes) or not Fraction(primes[left]) < b:
                raise AssertionError(("prime-free chosen gap", k, n, a, b))
            p = primes[left]
            if not violates_support(k, n, p):
                raise AssertionError(("gap prime still supported", k, n, p, a, b))
            margin = min(Fraction(p) - a, b - Fraction(p))
            worst_margin = margin if worst_margin is None else min(worst_margin, margin)
            rows += 1
        print(
            f"k={k}: checked={len(samples)} band=[{lower},{upper}] "
            f"minimum_exact_endpoint_margin={worst_margin}"
        )
    print(f"total_checked_frequencies={rows}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n-per-k", type=int, default=100_000)
    parser.add_argument("k", nargs="*", type=int, default=[10_000, 20_000, 50_000])
    args = parser.parse_args()
    scan(args.k, args.max_n_per_k)


if __name__ == "__main__":
    main()
