#!/usr/bin/env python3
"""Exact finite identities and asymptotic optimizer behind the #838 1/4 barrier."""

from fractions import Fraction
from math import comb


def flag_count(sizes: list[int]) -> int:
    ans = 1
    for a, b in zip(sizes, sizes[1:]):
        ans *= comb(a, b)
    return ans


def flags_containing_fixed_k_set(sizes: list[int], k: int) -> int:
    ans = 1
    for a, b in zip(sizes, sizes[1:]):
        ans *= comb(a - k, b - k)
    return ans


def check_flag_telescope() -> None:
    test_flags = [
        ([30, 18, 11, 7], 4),
        ([45, 31, 20, 13, 9], 6),
        ([70, 51, 29, 17, 12, 8], 5),
    ]
    for sizes, k in test_flags:
        ratio = Fraction(flag_count(sizes), flags_containing_fixed_k_set(sizes, k))
        endpoint_ratio = Fraction(comb(sizes[0], k), comb(sizes[-1], k))
        assert ratio == endpoint_ratio
        print(f"FLAG_TELESCOPE_OK sizes={sizes} k={k} ratio={ratio}")


def check_quadratic_barrier() -> None:
    # alpha(1-alpha) <= 1/4 is exactly (2 alpha - 1)^2 >= 0.
    for numerator in range(1, 1000):
        alpha = Fraction(numerator, 1000)
        value = alpha * (1 - alpha)
        assert value <= Fraction(1, 4)
    assert Fraction(1, 2) * Fraction(1, 2) == Fraction(1, 4)
    print("QUADRATIC_BARRIER_OK max=1/4 at alpha=1/2")


if __name__ == "__main__":
    check_flag_telescope()
    check_quadratic_barrier()
