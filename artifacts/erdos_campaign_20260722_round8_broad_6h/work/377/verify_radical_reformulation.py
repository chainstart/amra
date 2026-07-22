#!/usr/bin/env python3
"""Finite exact checks for the prefix and Euler-product forms of #377."""

from fractions import Fraction
from math import gcd, log


def primes_up_to(n: int) -> list[int]:
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            sieve[p * p : n + 1 : p] = b"\x00" * (((n - p * p) // p) + 1)
    return [p for p in range(2, n + 1) if sieve[p]]


def missing_by_digits(n: int, p: int) -> bool:
    half = (p - 1) // 2
    x = n
    while x:
        if x % p > half:
            return False
        x //= p
    return True


def missing_by_prefixes(n: int, p: int) -> bool:
    power = p
    while power <= 2 * n:
        if n % power > (power - 1) // 2:
            return False
        power *= p
    return True


def main() -> None:
    max_n = 3000
    primes = primes_up_to(max_n)
    max_euler_error = 0.0
    checks = 0
    for n in range(2, max_n + 1):
        ps = [p for p in primes if p <= n]
        missing = []
        euler_ratio = Fraction(1, 1)
        for p in ps:
            d = missing_by_digits(n, p)
            assert d == missing_by_prefixes(n, p)
            if d:
                missing.append(p)
                euler_ratio *= Fraction(p, p - 1)
            checks += 1
        reciprocal_sum = sum(1.0 / p for p in missing)
        error = abs(log(float(euler_ratio)) - reciprocal_sum)
        max_euler_error = max(max_euler_error, error)
        assert error <= sum(1.0 / (p * (p - 1)) for p in missing) + 1e-12
    print(
        "status=PASS "
        f"digit_prefix_checks={checks} "
        f"max_log_euler_minus_reciprocal={max_euler_error:.12f}"
    )


if __name__ == "__main__":
    main()
