#!/usr/bin/env python3
"""Exact finite guards for S.1--S.4.

The universal prime supply is the prime-number-theorem dependency recorded in
SURVIVOR_DEEPENING.md.  Finite counts here are replay checks only.
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
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def primes_between(lower: int, upper: int) -> list[int]:
    return [value for value in range(lower + 1, upper) if is_prime(value)]


def product(values) -> int:
    result = 1
    for value in values:
        result *= value
    return result


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


def construct(base: int, K: int, A: int, controlled: list[int]) -> dict[str, object]:
    assert is_prime(base) and A >= 4
    h = K // 2
    X = base ** (h - A)
    s = K // 4
    assert X > base and s >= 1
    assert base not in controlled
    assert all(is_prime(p) and p < X for p in controlled)
    reservoir = primes_between(X, 2 * X)
    assert len(reservoir) >= 2 * s
    labels = reservoir[: 2 * s]

    rough = []
    for vertex in range(2 * s + 1):
        value = 1
        if vertex > 0:
            value *= labels[vertex - 1]
        if vertex < 2 * s:
            value *= labels[vertex]
        rough.append(value)
    assert len(set(rough)) == len(rough)
    assert all(value < 4 * X * X for value in rough)
    left_q, right_q = rough[0::2], rough[1::2]
    assert product(left_q) == product(right_q) == product(labels)

    left_e0 = [K - ceil_log_base(value, base) for value in left_q]
    right_e = [K - ceil_log_base(value, base) for value in right_q]
    assert min(left_e0 + right_e) >= 2 * A - 2
    delta = sum(left_e0) - sum(right_e)
    assert K - (s + 1) < delta < K + s
    quotient, remainder = divmod(delta, s + 1)
    decrements = [quotient + (index < remainder) for index in range(s + 1)]
    assert max(decrements) <= 5
    left_e = [value - decrement for value, decrement in zip(left_e0, decrements)]
    assert min(left_e + right_e) >= 1
    assert sum(left_e) == sum(right_e)

    left = [base**e * q for e, q in zip(left_e, left_q)]
    right = [base**e * q for e, q in zip(right_e, right_q)]
    values = left + right
    N = base**K
    assert len(set(values)) == len(values)
    assert product(left) == product(right)
    assert all(value <= N and value * base**6 > N for value in values)
    assert all(all(value % p for p in controlled) for value in values)
    return {
        "base": base,
        "K": K,
        "A": A,
        "N": N,
        "X": X,
        "s": s,
        "reservoir_size": len(reservoir),
        "labels": labels,
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


def construction_guard() -> dict[str, object]:
    cases = [
        (2, 20, 4, [3, 5, 7]),
        (3, 16, 4, [2, 5, 7]),
        (5, 12, 4, [2, 3, 7]),
    ]
    rows = []
    for base, K, A, controlled in cases:
        data = construct(base, K, A, controlled)
        values = data["left"] + data["right"]
        full = (1 << len(values)) - 1
        assert unbalanced_supports(values) == {full}
        zero_count = count_zero_transcript(data["N"], controlled)
        reciprocal_sum = sum((Fraction(1, p) for p in controlled), Fraction(0))
        assert zero_count >= data["N"] * (1 - reciprocal_sum)
        rows.append({
            "base": base,
            "K": K,
            "A": A,
            "support": len(values),
            "X": data["X"],
            "reservoir_size": data["reservoir_size"],
            "max_decrement": data["max_decrement"],
            "fixed_tail_b_power": 6,
            "only_bad_support_is_full": True,
            "zero_transcript_count": zero_count,
        })
    return {"rows": rows}


def symbolic_budget_guard() -> dict[str, object]:
    rows = []
    for base in (2, 3, 5, 7):
        for A in range(4, 11):
            for K in range(16, 513):
                s = K // 4
                remainder = K - 4 * s
                assert 0 <= remainder <= 3
                assert K + s < 5 * (s + 1)
                assert 2 * A - 2 - 5 >= 1
            rows.append({"base": base, "A": A, "K_range": [16, 512], "status": "PASS"})
    return {"rows": rows}


def randomized_charge_guard() -> dict[str, object]:
    N = 20_000
    threshold = 200
    seeds = [
        (Fraction(1, 8), [2, 5], "delete"),
        (Fraction(3, 8), [3, 5], "retain"),
        (Fraction(1, 2), [2, 7], "retain"),
    ]
    populations = [count_zero_transcript(N, primes) for _, primes, _ in seeds]
    L = min(populations)
    sizes = [
        population if leaf == "delete" else threshold
        for (_, _, leaf), population in zip(seeds, populations)
    ]
    expected = sum((weight * size for (weight, _, _), size in zip(seeds, sizes)), Fraction(0))
    probability_zero_deleted = sum((weight for weight, _, leaf in seeds if leaf == "delete"), Fraction(0))
    bound = expected / (L - threshold)
    assert probability_zero_deleted <= bound
    return {
        "N": N,
        "threshold": threshold,
        "L": L,
        "expected_deletion": str(expected),
        "probability_zero_deleted": str(probability_zero_deleted),
        "success_probability_bound": str(bound),
    }


def square_root_guard() -> dict[str, object]:
    rows = []
    for N in (10**6, 10**8, 10**10):
        lower = int(N**0.5)
        labels = [p for p in range(lower + 1, lower + 200) if is_prime(p)][:2]
        assert len(labels) == 2 and labels[0] * labels[1] > N
        rows.append({"N": N, "labels": labels, "product_exceeds_N": True})
    return {"rows": rows}


def main() -> None:
    payload = {
        "status": "PASS",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "symbolic_budget": symbolic_budget_guard(),
        "exact_constructions": construction_guard(),
        "randomized_charge": randomized_charge_guard(),
        "square_root_boundary": square_root_guard(),
        "scope": "finite replay for S.1--S.4; the universal prime supply is the separately declared prime-number-theorem dependency",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
