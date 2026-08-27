#!/usr/bin/env python3
"""Exact finite guards for U.1--U.3.

The universal conclusions are proved in SURVIVOR_DEEPENING.md.  These finite
instances check identities, strict inequalities, support minimality, and the
zero-signature counting interface without finite-to-universal extrapolation.
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


def next_primes(start: int, count: int) -> list[int]:
    result: list[int] = []
    candidate = start + 1
    while len(result) < count:
        if is_prime(candidate):
            result.append(candidate)
        candidate += 1
    return result


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


def construct(base: int, exponent: int, controlled: list[int]) -> dict[str, object]:
    assert is_prime(base) and exponent >= 32
    m = exponent // 16
    roughness = base**m
    assert base not in controlled
    assert all(is_prime(p) and p < roughness for p in controlled)

    labels = next_primes(roughness, 2 * m)
    assert all(labels[index] < 2 ** (index + 1) * roughness for index in range(2 * m))
    assert labels[-1] < base ** (3 * m)

    rough_parts = []
    for vertex in range(2 * m + 1):
        value = 1
        if vertex > 0:
            value *= labels[vertex - 1]
        if vertex < 2 * m:
            value *= labels[vertex]
        rough_parts.append(value)
    assert len(set(rough_parts)) == 2 * m + 1
    assert all(value < base ** (6 * m) for value in rough_parts)

    left_q = rough_parts[0::2]
    right_q = rough_parts[1::2]
    assert product(left_q) == product(right_q) == product(labels)

    left_e0 = [exponent - ceil_log_base(value, base) for value in left_q]
    right_e = [exponent - ceil_log_base(value, base) for value in right_q]
    delta = sum(left_e0) - sum(right_e)
    assert 0 < delta < exponent + m
    quotient, remainder = divmod(delta, m + 1)
    decrements = [quotient + (index < remainder) for index in range(m + 1)]
    assert max(decrements) <= 17
    left_e = [value - decrement for value, decrement in zip(left_e0, decrements)]
    assert min(left_e + right_e) >= 0
    assert sum(left_e) == sum(right_e)

    left = [base**e * q for e, q in zip(left_e, left_q)]
    right = [base**e * q for e, q in zip(right_e, right_q)]
    values = left + right
    N = base**exponent
    assert len(set(values)) == len(values)
    assert product(left) == product(right)
    assert all(value <= N and value * base**18 > N for value in values)
    assert all(all(value % p for p in controlled) for value in values)

    return {
        "base": base,
        "K": exponent,
        "N": N,
        "m": m,
        "support": len(values),
        "roughness": roughness,
        "labels": labels,
        "left": left,
        "right": right,
        "delta": delta,
        "max_decrement": max(decrements),
        "controlled": controlled,
    }


def count_zero_signature(N: int, controlled: list[int]) -> int:
    total = 0
    for mask in range(1 << len(controlled)):
        chosen = [controlled[index] for index in range(len(controlled)) if mask & (1 << index)]
        term = N // product(chosen)
        total += -term if mask.bit_count() % 2 else term
    return total


def symbolic_budget_guard() -> dict[str, object]:
    rows = []
    for base in (2, 3, 5, 7):
        for exponent in range(32, 257):
            m = exponent // 16
            remainder = exponent - 16 * m
            assert m >= 2
            assert exponent - 6 * m - 17 >= 0
            assert 17 * m + remainder <= 17 * (m + 1)
        rows.append({"base": base, "K_range": [32, 256], "tail_power": 18, "status": "PASS"})
    return {"rows": rows}


def construction_guard() -> dict[str, object]:
    cases = [
        (2, 64, [3, 5, 7]),
        (3, 64, [2, 5, 7]),
        (5, 48, [2, 3, 7]),
    ]
    rows = []
    for base, exponent, controlled in cases:
        data = construct(base, exponent, controlled)
        values = data["left"] + data["right"]
        full = (1 << len(values)) - 1
        assert unbalanced_supports(values) == {full}
        zero_count = count_zero_signature(data["N"], controlled)
        reciprocal_sum = sum((Fraction(1, p) for p in controlled), Fraction(0))
        assert zero_count >= data["N"] * (1 - reciprocal_sum)
        rows.append({
            "base": base,
            "K": exponent,
            "support": data["support"],
            "max_decrement": data["max_decrement"],
            "strict_fixed_tail": True,
            "only_bad_support_is_full": True,
            "zero_signature_count": zero_count,
            "zero_signature_union_bound": str(1 - reciprocal_sum),
        })
    return {"rows": rows}


def independent_rounding_guard() -> dict[str, object]:
    rows = []
    for exponent in (64, 96, 128):
        support = 2 * (exponent // 16) + 1
        g = 1
        marginal_upper = Fraction(18 * g, exponent)
        assert marginal_upper < 1
        survival_lower = (1 - marginal_upper) ** support
        assert survival_lower > 0
        rows.append({
            "K": exponent,
            "support": support,
            "g": g,
            "marginal_upper": str(marginal_upper),
            "positive_all_survive_lower_bound": str(survival_lower),
        })
    return {"rows": rows}


def main() -> None:
    payload = {
        "status": "PASS",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "symbolic_budget": symbolic_budget_guard(),
        "exact_constructions": construction_guard(),
        "independent_rounding": independent_rounding_guard(),
        "scope": "finite exact guards for separately proved U.1--U.3; no finite-to-universal inference",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
