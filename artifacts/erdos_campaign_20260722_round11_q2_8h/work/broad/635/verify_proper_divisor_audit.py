#!/usr/bin/env python3
"""Solver-free finite checks for PROPER_DIVISOR_HALL_AUDIT.md.

The two displayed counterexamples are exact proofs of failure of the stated
templates.  The prime-oddpart forest scan is only finite conjecture guidance.
"""

from __future__ import annotations

import json


def valuation_oddpart(value: int) -> tuple[int, int]:
    valuation = 0
    while value % 2 == 0:
        valuation += 1
        value //= 2
    return valuation, value


def conflict(left: int, right: int) -> bool:
    difference = abs(left - right)
    return difference >= 2 and max(left, right) % difference == 0


def proper_divisors(value: int) -> list[int]:
    answer = set()
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            if 1 < divisor < value:
                answer.add(divisor)
            other = value // divisor
            if 1 < other < value:
                answer.add(other)
        divisor += 1
    return sorted(answer)


class DisjointSet:
    def __init__(self) -> None:
        self.parent: dict[int, int] = {}

    def find(self, value: int) -> int:
        self.parent.setdefault(value, value)
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def add_edge(self, left: int, right: int) -> bool:
        root_left, root_right = self.find(left), self.find(right)
        if root_left == root_right:
            return False
        self.parent[root_left] = root_right
        return True


def prime_sieve(limit: int) -> bytearray:
    prime = bytearray(b"\x01") * (limit + 1)
    prime[:2] = b"\x00\x00"
    for value in range(2, int(limit ** 0.5) + 1):
        if prime[value]:
            start = value * value
            prime[start::value] = b"\x00" * (((limit - start) // value) + 1)
    return prime


def main() -> None:
    # Failure of the least-prime-factor canonical choice.
    first = (150, 154)
    first_targets = []
    for value in first:
        _, oddpart = valuation_oddpart(value)
        least = proper_divisors(oddpart)[0]
        first_targets.append(value - least)
    assert first_targets == [147, 147]
    assert not conflict(*first)

    # Failure of the private-proper-neighbour induction.
    second = (280, 286)
    second_neighbourhoods = []
    for value in second:
        _, oddpart = valuation_oddpart(value)
        second_neighbourhoods.append(sorted(value - divisor
                                            for divisor in proper_divisors(oddpart)))
    assert second_neighbourhoods == [[273, 275], [273, 275]]
    assert not conflict(*second)

    # Finite guidance for the possible feedback-edge theorem.
    limit = 1_000_000
    prime = prime_sieve(limit)
    forest = DisjointSet()
    edges = 0
    for value in range(2, limit + 1, 2):
        valuation, oddpart = valuation_oddpart(value)
        if oddpart <= 1 or not prime[oddpart]:
            continue
        scale = 1 << valuation
        lower, upper = (scale - 1) * oddpart, (scale + 1) * oddpart
        if upper > limit:
            continue
        assert forest.add_edge(lower, upper)
        edges += 1

    print(json.dumps({
        "schema": "amra.erdos635.proper-divisor-audit.v1",
        "status": "PASS",
        "least_prime_choice_collision": {
            "independent_left_vertices": list(first),
            "common_target": first_targets[0],
        },
        "no_private_neighbour_equality_block": {
            "independent_left_vertices": list(second),
            "proper_lower_neighbourhood": second_neighbourhoods[0],
        },
        "prime_oddpart_canonical_forest_probe": {
            "maximum_center_and_endpoint": limit,
            "edges": edges,
            "cycle_found": False,
            "global_claim": False,
        },
        "scope_warning": "Counterexamples are exact; the finite forest scan is not an asymptotic proof.",
    }, indent=2))


if __name__ == "__main__":
    main()
