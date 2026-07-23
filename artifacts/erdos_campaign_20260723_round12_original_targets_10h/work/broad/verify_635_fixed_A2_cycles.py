#!/usr/bin/env python3
"""Exact finite certificate for short cycles in the fixed-A=2 swap graph.

The symbolic reduction in 635_SEMIPRIME_SWAP_GRAPH.md shows that every
non-backtracking m-cycle supplies positive odd multipliers h_i with
prod(h_i) < 2**m.  Conversely those multipliers uniquely determine the two
cyclic prime sequences.  Hence enumerating the multiplier tuples is a
complete check for that fixed (A,m), not a cutoff in the prime variables.
"""

from __future__ import annotations

import json
import math


A = 2
MAX_LENGTH = 12


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    for divisor in range(3, math.isqrt(value) + 1, 2):
        if value % divisor == 0:
            return False
    return True


def seeds(multipliers: tuple[int, ...]) -> tuple[int, int] | None:
    """Return the two integral cyclic seeds from equations (8)--(9)."""
    length = len(multipliers)
    product = math.prod(multipliers)
    denominator = A**length - product
    assert denominator > 0

    forward = 0
    prefix = 1
    for index in range(length):
        forward += A ** (length - 1 - index) * prefix
        if index < length - 1:
            prefix *= multipliers[index]

    reverse = 0
    suffix = 1
    for index in range(length):
        reverse += A ** (length - 1 - index) * suffix
        if index < length - 1:
            suffix *= multipliers[length - 1 - index]

    if forward % denominator or reverse % denominator:
        return None
    return forward // denominator, reverse // denominator


def cyclic_sequences(
    multipliers: tuple[int, ...], first_seed: int, second_seed: int
) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    first: list[int] = []
    second: list[int] = []
    p_value, q_value = first_seed, second_seed
    for multiplier in multipliers:
        first.append(p_value)
        second.append(q_value)
        first_numerator = A * p_value - 1
        second_numerator = multiplier * q_value + 1
        if first_numerator % multiplier or second_numerator % A:
            return None
        p_value = first_numerator // multiplier
        q_value = second_numerator // A
    if (p_value, q_value) != (first_seed, second_seed):
        return None
    return tuple(first), tuple(second)


def audit_length(length: int) -> dict[str, object]:
    limit = A**length
    current = [1] * length
    tuple_count = 0
    prime_closed_walks: list[dict[str, object]] = []
    nonbacktracking = 0

    def visit(index: int, product: int) -> None:
        nonlocal tuple_count, nonbacktracking
        if index < length:
            maximum = (limit - 1) // product
            for multiplier in range(1, maximum + 1, 2):
                current[index] = multiplier
                visit(index + 1, product * multiplier)
            return

        tuple_count += 1
        multipliers = tuple(current)
        seed_pair = seeds(multipliers)
        if seed_pair is None:
            return
        sequences = cyclic_sequences(multipliers, *seed_pair)
        if sequences is None:
            return
        first, second = sequences
        if not all(value % 2 and is_prime(value) for value in first + second):
            return

        valid_edges = all(first[i] != second[i] for i in range(length))
        edges = [frozenset((first[i], second[i])) for i in range(length)]
        immediate_return = any(
            edges[index] == edges[(index - 1) % length]
            for index in range(length)
        )
        if valid_edges and not immediate_return:
            nonbacktracking += 1
        prime_closed_walks.append(
            {
                "multipliers": multipliers,
                "first": first,
                "second": second,
                "valid_distinct_prime_edges": valid_edges,
                "immediate_return": immediate_return,
            }
        )

    visit(0, 1)
    assert nonbacktracking == 0
    return {
        "length": length,
        "multiplier_tuples": tuple_count,
        "prime_closed_walks": prime_closed_walks,
        "nonbacktracking_candidates": nonbacktracking,
    }


def main() -> None:
    audits = [audit_length(length) for length in range(2, MAX_LENGTH + 1)]
    print(
        json.dumps(
            {
                "schema": "amra.erdos635.fixed-A2-short-cycle.v1",
                "status": "PASS",
                "A": A,
                "complete_lengths": [2, MAX_LENGTH],
                "audits": audits,
                "conclusion": (
                    "No non-backtracking fixed-A=2 cycle has length at most 12"
                ),
                "scope": (
                    "complete multiplier enumeration for the listed lengths; "
                    "not a proof for unbounded cycle length or the original problem"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
