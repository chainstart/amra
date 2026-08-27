#!/usr/bin/env python3
"""Finite exact guards for ROUND4_FULL_RESIDUE_OWNER_FLOW.md.

The positive-density and all-sufficiently-large-K assertions in the note are
proved symbolically.  The computations here only guard the constructions,
owner definitions, endpoint conventions, and exact product identities.
"""

from __future__ import annotations

import json
from fractions import Fraction
from hashlib import sha256
from math import prod
from pathlib import Path


def primes_upto(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = b"\x00" * (
                (limit - p * p) // p + 1
            )
    return [p for p in range(2, limit + 1) if sieve[p]]


def factor_squarefree(n: int, primes: list[int]) -> list[int] | None:
    factors: list[int] = []
    value = n
    for p in primes:
        if p * p > value:
            break
        if value % p:
            continue
        value //= p
        factors.append(p)
        if value % p == 0:
            return None
    if value > 1:
        factors.append(value)
    return factors


def is_support_minimal(plus: list[int], minus: list[int]) -> bool:
    """Exhaust signed subrelations; intended only for small double stars."""

    if prod(plus) != prod(minus) or len(plus) == len(minus):
        return False
    full_plus = (1 << len(plus)) - 1
    full_minus = (1 << len(minus)) - 1
    for left_mask in range(1, full_plus + 1):
        left = prod(plus[i] for i in range(len(plus)) if left_mask >> i & 1)
        for right_mask in range(1, full_minus + 1):
            if left_mask == full_plus and right_mask == full_minus:
                continue
            right = prod(
                minus[i] for i in range(len(minus)) if right_mask >> i & 1
            )
            if left == right:
                return False
    return True


def top_ratio(plus: list[int], minus: list[int], p: int) -> Fraction:
    numerator = 1
    denominator = 1
    for n in plus:
        if n % p == 0:
            while n % p == 0:
                n //= p
            numerator *= n
    for n in minus:
        if n % p == 0:
            while n % p == 0:
                n //= p
            denominator *= n
    return Fraction(numerator, denominator)


def owner_top_ratio(plus: list[int], minus: list[int], p: int) -> int:
    ratio = top_ratio(plus, minus, p)
    if ratio.numerator > ratio.denominator:
        candidates = [n for n in plus if n % p == 0]
    elif ratio.denominator > ratio.numerator:
        candidates = [n for n in minus if n % p == 0]
    else:
        candidates = [n for n in plus + minus if n % p == 0]
    return max(candidates, key=lambda n: (remove_prime(n, p), n))


def remove_prime(n: int, p: int) -> int:
    while n % p == 0:
        n //= p
    return n


def double_star_guards() -> dict[str, object]:
    primes = primes_upto(1000)
    examples = []
    for n in (3 * 5 * 7, 5 * 7 * 11, 3 * 5 * 7 * 11, 5 * 11 * 13 * 17):
        factors = factor_squarefree(n, primes)
        assert factors is not None and len(factors) >= 3 and n % 2
        p = factors[-1]
        lower = factors[:-1]
        plus = lower + [2 * p]
        minus = [2, n]
        assert len(plus) != len(minus)
        assert prod(plus) == prod(minus)
        assert is_support_minimal(plus, minus)
        ratio = top_ratio(plus, minus, p)
        assert ratio == Fraction(2, prod(lower))
        assert owner_top_ratio(plus, minus, p) == n
        examples.append(
            {
                "n": n,
                "top_prime": p,
                "ratio": f"{ratio.numerator}/{ratio.denominator}",
                "owner": n,
            }
        )

    density_rows = []
    for exponent in (12, 14, 16, 18):
        bound = 1 << exponent
        local_primes = primes_upto(int(bound**0.5) + 1)
        count = 0
        for n in range(bound // 2 + 1, bound + 1, 2):
            factors = factor_squarefree(n, local_primes)
            if factors is not None and len(factors) >= 3:
                count += 1
        density_rows.append(
            {"N": bound, "owners_guarded": count, "ratio_to_N": count / bound}
        )
    return {
        "minimal_examples": examples,
        "density_rows": density_rows,
        "scope": "finite guards only; density 2/pi^2 is proved by the odd-squarefree asymptotic and deletion of Omega<=2",
    }


def ceil_log2(n: int) -> int:
    return (n - 1).bit_length()


def balanced_parts(total: int, count: int) -> list[int]:
    quotient, remainder = divmod(total, count)
    return [quotient + 1] * remainder + [quotient] * (count - remainder)


def path_values(labels: list[int], k: int) -> list[int]:
    q = [labels[0]]
    q.extend(labels[i - 1] * labels[i] for i in range(1, len(labels)))
    q.append(labels[-1])
    c = [ceil_log2(value) for value in q]
    ceiling_imbalance = sum(c[::2]) - sum(c[1::2])
    decrements = balanced_parts(k - ceiling_imbalance, len(q[::2]))
    assert max(decrements) <= 5
    result = []
    even_index = 0
    for index, value in enumerate(q):
        decrement = 0
        if index % 2 == 0:
            decrement = decrements[even_index]
            even_index += 1
        exponent = k - c[index] - decrement
        assert exponent >= 0
        result.append((1 << exponent) * value)
    assert prod(result[::2]) == prod(result[1::2])
    return result


def largest_prime_factor(n: int) -> int:
    largest = 1
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            largest = divisor
            n //= divisor
        divisor += 1 if divisor == 2 else 2
    return max(largest, n)


def owner_residue_boundary(plus: list[int], minus: list[int], p: int) -> int:
    ratio = top_ratio(plus, minus, p)
    residue_product = ratio.numerator * ratio.denominator
    if residue_product == 1:
        return min(n for n in plus + minus if n % p == 0)
    q = largest_prime_factor(residue_product)
    exponent_sign = 0
    value = ratio.numerator
    while value % q == 0:
        exponent_sign += 1
        value //= q
    value = ratio.denominator
    while value % q == 0:
        exponent_sign -= 1
        value //= q
    assert exponent_sign
    shore = minus if exponent_sign > 0 else plus
    candidates = [n for n in shore if n % p and n % q == 0]
    assert candidates
    return min(candidates)


def long_path_book_guard() -> dict[str, object]:
    k = 80
    n_bound = 1 << k
    s = k // 4
    root_index = 3
    available = [p for p in primes_upto(1 << (k // 8)) if p > 1 << (k // 16)]
    iterator = iter(available)
    circuits = []
    owners = []
    roots = []
    top_rows = []
    for _ in range(4):
        block = sorted(next(iterator) for _ in range(2 * s - 2))
        labels: list[int | None] = [None] * (2 * s)
        labels[root_index - 1] = 3
        labels[root_index] = 5
        for index, prime in zip(
            [j for j, value in enumerate(labels) if value is None], block
        ):
            labels[index] = prime
        exact_labels = [int(value) for value in labels]
        values = path_values(exact_labels, k)
        assert all(n_bound // 64 < value <= n_bound for value in values)
        assert len(values) == len(set(values))
        plus, minus = values[::2], values[1::2]
        p = exact_labels[-1]
        q = exact_labels[-2]
        assert p == max(exact_labels) and q == max(x for x in exact_labels if x != p)
        ratio = top_ratio(plus, minus, p)
        assert largest_prime_factor(ratio.numerator * ratio.denominator) == q
        owner = owner_residue_boundary(plus, minus, p)
        assert owner == values[-3]
        circuits.append(set(values))
        owners.append(owner)
        roots.append(values[root_index])
        top_rows.append(
            {
                "top_prime": p,
                "boundary_prime": q,
                "ratio": f"{ratio.numerator}/{ratio.denominator}",
                "owner": owner,
            }
        )
    assert len(set(roots)) == 1
    common_root = roots[0]
    for i, first in enumerate(circuits):
        for second in circuits[i + 1 :]:
            assert first & second == {common_root}
    assert len(set(owners)) == len(owners)
    return {
        "K": k,
        "s": s,
        "circuits": len(circuits),
        "common_root": common_root,
        "distinct_boundary_owners": len(set(owners)),
        "top_rows": top_rows,
        "scope": "finite construction guard; the all-K book count uses disjoint prime blocks and the symbolic path padding lemma",
    }


def main() -> None:
    payload = {
        "status": "PASS",
        "double_star_top_ratio_owner": double_star_guards(),
        "long_path_boundary_owner": long_path_book_guard(),
        "classification": {
            "top_ratio_owner": "killed globally by a positive-density double-star family",
            "boundary_owner_cluster_load": "killed by common-root long-path books",
            "global_M786R_08": "open",
        },
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
