#!/usr/bin/env python3
"""Exact finite guards for Q.1--Q.4.

The all-parameter proofs are in SURVIVOR_DEEPENING.md.  This script checks
finite arithmetic instances, exhaustive small-support minimality, adaptive
zero-transcript behavior, and the expectation charging identity.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n == p:
            return True
        if n % p == 0:
            return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % n == 0:
            continue
        value = pow(base, d, n)
        if value in (1, n - 1):
            continue
        for _ in range(s - 1):
            value = value * value % n
            if value == n - 1:
                break
        else:
            return False
    return True


def next_primes(start: int, count: int) -> list[int]:
    result: list[int] = []
    candidate = start + 1
    if candidate > 2 and candidate % 2 == 0:
        candidate += 1
    while len(result) < count:
        if is_prime(candidate):
            result.append(candidate)
        candidate += 1 if candidate == 2 else 2
    return result


def product(values) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def ceil_log_base(value: int, base: int) -> int:
    exponent = 0
    power = 1
    while power < value:
        power *= base
        exponent += 1
    return exponent


def unbalanced_supports(values: list[int]) -> set[int]:
    groups: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for mask in range(1 << len(values)):
        chosen = [values[index] for index in range(len(values)) if mask & (1 << index)]
        groups[product(chosen)].append((mask.bit_count(), mask))
    supports: set[int] = set()
    for records in groups.values():
        for (left_count, left_mask), (right_count, right_mask) in combinations(records, 2):
            if left_count != right_count:
                supports.add(left_mask ^ right_mask)
    return supports


def construct(base: int, K: int, epsilon: Fraction, controlled: list[int]) -> dict[str, object]:
    assert is_prime(base) and 0 < epsilon < Fraction(1, 2)
    u = ceil_fraction((Fraction(1, 2) - epsilon) * K)
    s = (epsilon * K).numerator // ((epsilon * K).denominator * 4)
    D = ceil_fraction(Fraction(8, 1) / epsilon + 1)
    assert s >= 1
    cutoff = base**u
    assert base not in controlled
    assert all(is_prime(p) and p < cutoff for p in controlled)

    labels = next_primes(cutoff, 2 * s)
    assert all(labels[index] < 2 ** (index + 1) * cutoff for index in range(2 * s))
    assert labels[-1] < base ** (u + 2 * s)

    rough = []
    for vertex in range(2 * s + 1):
        value = 1
        if vertex > 0:
            value *= labels[vertex - 1]
        if vertex < 2 * s:
            value *= labels[vertex]
        rough.append(value)
    assert len(set(rough)) == len(rough)
    assert all(value < base ** (2 * u + 4 * s) for value in rough)

    left_q = rough[0::2]
    right_q = rough[1::2]
    assert product(left_q) == product(right_q) == product(labels)
    left_e0 = [K - ceil_log_base(value, base) for value in left_q]
    right_e = [K - ceil_log_base(value, base) for value in right_q]
    delta = sum(left_e0) - sum(right_e)
    assert K - (s + 1) < delta < K + s
    quotient, remainder = divmod(delta, s + 1)
    decrements = [quotient + (index < remainder) for index in range(s + 1)]
    assert max(decrements) <= D
    left_e = [value - decrement for value, decrement in zip(left_e0, decrements)]
    assert min(left_e + right_e) >= 0
    assert sum(left_e) == sum(right_e)

    left = [base**e * q for e, q in zip(left_e, left_q)]
    right = [base**e * q for e, q in zip(right_e, right_q)]
    values = left + right
    N = base**K
    assert len(set(values)) == len(values)
    assert product(left) == product(right)
    assert all(value <= N and value * base ** (D + 1) > N for value in values)
    assert all(all(value % p for p in controlled) for value in values)
    return {
        "base": base,
        "K": K,
        "epsilon": str(epsilon),
        "u": u,
        "s": s,
        "D": D,
        "N": N,
        "controlled": controlled,
        "left": left,
        "right": right,
        "delta": delta,
        "max_decrement": max(decrements),
    }


def count_zero_transcript(N: int, primes: list[int]) -> int:
    total = 0
    for mask in range(1 << len(primes)):
        selected = [primes[index] for index in range(len(primes)) if mask & (1 << index)]
        term = N // product(selected)
        total += -term if mask.bit_count() % 2 else term
    return total


def valuation(n: int, prime: int) -> int:
    result = 0
    while n % prime == 0:
        result += 1
        n //= prime
    return result


def follow_zero_tree(n: int, zero_primes: list[int], zero_leaf: str) -> str:
    for index, prime in enumerate(zero_primes):
        if valuation(n, prime) != 0:
            # Off-zero branches may contain unrelated additional queries.
            return f"off_zero_{index}"
    return zero_leaf


def construction_and_transcript_guard() -> dict[str, object]:
    cases = [
        (2, 64, Fraction(1, 4), [3, 5, 7]),
        (3, 48, Fraction(1, 4), [2, 5, 7]),
        (2, 128, Fraction(1, 8), [3, 5, 7, 11]),
    ]
    rows = []
    for base, K, epsilon, controlled in cases:
        data = construct(base, K, epsilon, controlled)
        values = data["left"] + data["right"]
        if len(values) <= 10:
            full = (1 << len(values)) - 1
            assert unbalanced_supports(values) == {full}
        assert all(follow_zero_tree(value, controlled, "retain") == "retain" for value in values)
        zero_count = count_zero_transcript(data["N"], controlled)
        reciprocal_sum = sum((Fraction(1, p) for p in controlled), Fraction(0))
        assert zero_count >= data["N"] * (1 - reciprocal_sum)
        rows.append({
            "base": base,
            "K": K,
            "epsilon": str(epsilon),
            "support": len(values),
            "cutoff_exponent": data["u"],
            "tail_exponent": data["D"] + 1,
            "max_decrement": data["max_decrement"],
            "zero_transcript_count": zero_count,
            "only_bad_support_is_full": len(values) <= 10,
            "all_vertices_reach_retain_zero_leaf": True,
        })
    return {"rows": rows}


def randomized_charge_guard() -> dict[str, object]:
    N = 10_000
    threshold = 100
    seeds = [
        {"weight": Fraction(1, 10), "zero_primes": [2, 5], "zero_leaf": "delete"},
        {"weight": Fraction(3, 10), "zero_primes": [3, 5], "zero_leaf": "retain"},
        {"weight": Fraction(3, 5), "zero_primes": [2, 7], "zero_leaf": "retain"},
    ]
    populations = [count_zero_transcript(N, seed["zero_primes"]) for seed in seeds]
    L = min(populations)
    deletion_sizes = [
        threshold + max(0, population - threshold) if seed["zero_leaf"] == "delete" else threshold
        for seed, population in zip(seeds, populations)
    ]
    expected_cost = sum(
        (seed["weight"] * size for seed, size in zip(seeds, deletion_sizes)),
        Fraction(0),
    )
    probability_zero_deleted = sum(
        (seed["weight"] for seed in seeds if seed["zero_leaf"] == "delete"),
        Fraction(0),
    )
    bound = expected_cost / (L - threshold)
    assert probability_zero_deleted <= bound
    return {
        "N": N,
        "threshold": threshold,
        "zero_populations": populations,
        "L": L,
        "expected_cost": str(expected_cost),
        "probability_zero_deleted": str(probability_zero_deleted),
        "success_probability_upper_bound": str(bound),
        "indicator_charge_verified": True,
    }


def square_root_barrier_guard() -> dict[str, object]:
    for N in (10**6, 10**8, 10**10):
        lower = int(N**0.5) + 1
        p, q = next_primes(lower, 2)
        assert p * q > N
    return {"instances": 3, "two_primes_above_sqrt_exceed_N": True}


def main() -> None:
    payload = {
        "status": "PASS",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "construction_and_transcripts": construction_and_transcript_guard(),
        "randomized_charge": randomized_charge_guard(),
        "square_root_barrier": square_root_barrier_guard(),
        "scope": "finite exact guards for separately proved Q.1--Q.4; no finite-to-universal inference",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
