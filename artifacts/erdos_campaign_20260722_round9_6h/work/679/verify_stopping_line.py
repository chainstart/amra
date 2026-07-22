#!/usr/bin/env python3
"""Finite audit of the exact conductor stopping-line identity."""

from itertools import combinations
from math import prod


def subsets(items):
    items = tuple(items)
    for r in range(len(items) + 1):
        yield from combinations(items, r)


def main() -> None:
    primes = (3, 5, 7, 11, 13)
    h_count = 2
    shift0 = 1
    t = 0.7
    a = 1.0 - t
    q = prod(primes)
    means = {p: 1.0 - h_count * a / p for p in primes}

    def local(p: int, n: int) -> float:
        active = any((n - shift0 - j) % p == 0 for j in range(h_count))
        return t if active else 1.0

    def direct_tail(n: int, cutoff: int) -> float:
        total = 0.0
        for chosen in subsets(primes):
            if prod(chosen) <= cutoff:
                continue
            chosen_set = set(chosen)
            total += prod(
                local(p, n) - means[p] if p in chosen_set else means[p]
                for p in primes
            )
        return total

    def stopping_tail(n: int, cutoff: int, order: tuple[int, ...]):
        total = 0.0
        absolute_frontier = 0.0
        for index, crossing_prime in enumerate(order):
            earlier = order[:index]
            later = order[index + 1 :]
            for chosen in subsets(earlier):
                conductor = prod(chosen)
                if not (conductor <= cutoff < conductor * crossing_prime):
                    continue
                chosen_set = set(chosen)
                term = (local(crossing_prime, n) - means[crossing_prime])
                term *= prod(local(p, n) for p in later)
                term *= prod(
                    local(p, n) - means[p] if p in chosen_set else means[p]
                    for p in earlier
                )
                total += term
                absolute_frontier += abs(term)
        return total, absolute_frontier

    max_error = 0.0
    max_frontier = 0.0
    interval_ledger = []
    for cutoff in (5, 20, 100, 500):
        tails = []
        for n in range(q):
            direct = direct_tail(n, cutoff)
            tails.append(direct)
            for order in (primes, tuple(reversed(primes))):
                stopped, absolute_frontier = stopping_tail(n, cutoff, order)
                max_error = max(max_error, abs(direct - stopped))
                max_frontier = max(max_frontier, absolute_frontier)
        start, length = 137, 1000
        interval_ledger.append((cutoff, sum(tails[start : start + length])))

    assert max_error < 2e-12
    print(
        "status=PASS "
        f"Q={q} cutoffs=4 orders=2 max_identity_error={max_error:.3e} "
        f"max_absolute_frontier={max_frontier:.6f} "
        "interval_tails="
        + ",".join(f"D{d}:{value:.6e}" for d, value in interval_ledger)
    )


if __name__ == "__main__":
    main()
