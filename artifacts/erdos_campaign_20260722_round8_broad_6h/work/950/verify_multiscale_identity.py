#!/usr/bin/env python3
"""Finite falsifier for Abel/dyadic identities and the robust tuple bound."""

from itertools import combinations
from math import log


def primes_up_to(n: int) -> list[int]:
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            sieve[p * p : n + 1 : p] = b"\x00" * (((n - p * p) // p) + 1)
    return [p for p in range(2, n + 1) if sieve[p]]


def check_number(n: int, prime_set: set[int]) -> None:
    indicators = [int(n - d in prime_set) for d in range(1, n - 1)]
    direct = sum(a / d for d, a in enumerate(indicators, 1))
    partial = 0
    abel = 0.0
    for d, a in enumerate(indicators[:-1], 1):
        partial += a
        abel += partial / (d * (d + 1))
    partial += indicators[-1]
    abel += partial / (n - 2)
    assert abs(direct - abel) < 1e-12

    shell_total = 0.0
    lo = 1
    while lo <= n - 2:
        hi = min(2 * lo, n - 1)
        count = sum(indicators[lo - 1 : hi - 1])
        shell_total += count / lo
        lo *= 2
    assert 0.5 * shell_total <= direct + 1e-12
    assert direct <= shell_total + 1e-12


def robust_yield(hs: tuple[int, ...], m: int) -> float:
    best = float("inf")
    for subset in combinations(range(len(hs)), m + 1):
        j = subset[-1]
        value = sum(1.0 / (hs[j] - hs[i] + 1) for i in subset[:-1])
        best = min(best, value)
    return best


def main() -> None:
    max_n = 5000
    prime_set = set(primes_up_to(max_n))
    for n in range(3, max_n + 1):
        check_number(n, prime_set)

    tuple_checks = 0
    for hs in (
        (0, 2, 6, 8, 12),
        (0, 4, 10, 18, 28, 40),
        (0, 6, 12, 30, 42, 60, 72),
    ):
        h = hs[-1]
        for m in range(1, len(hs)):
            bound = m * log(h + 1) / (len(hs) - 1)
            assert robust_yield(hs, m) <= bound + 1e-12
            tuple_checks += 1
    print(
        f"status=PASS abel_dyadic_n=3..{max_n} "
        f"robust_tuple_checks={tuple_checks}"
    )


if __name__ == "__main__":
    main()
