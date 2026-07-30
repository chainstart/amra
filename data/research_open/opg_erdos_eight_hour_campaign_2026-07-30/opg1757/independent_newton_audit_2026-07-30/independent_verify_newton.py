#!/usr/bin/env python3
"""Independent exhaustive audit of the first two active Newton layers."""

from __future__ import annotations

import itertools
import math
from collections import Counter
from fractions import Fraction
from functools import lru_cache


def scaled(value: int, base: int, exponent: int, denominator: int = 1) -> Fraction:
    result = Fraction(value, denominator)
    return result * base**exponent if exponent >= 0 else result / base ** (-exponent)


class DisjointSet:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, vertex: int) -> int:
        while self.parent[vertex] != vertex:
            self.parent[vertex] = self.parent[self.parent[vertex]]
            vertex = self.parent[vertex]
        return vertex

    def join(self, left: int, right: int) -> bool:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return False
        self.parent[left_root] = right_root
        return True


@lru_cache(maxsize=None)
def exhaustive_rows(n: int) -> dict[str, Counter[int]]:
    """Enumerate edge subsets directly; no contraction or forest formula is used."""

    if n < 4:
        raise ValueError("two fixed disjoint edges require n >= 4")
    edges = tuple(itertools.combinations(range(n), 2))
    fixed_first = (0, 1)
    fixed_disjoint = (2, 3)
    fixed_adjacent = (0, 2)
    rows = {
        "W0": Counter(),
        "W1": Counter(),
        "W2": Counter(),
        "A": Counter(),
    }

    for edge_count in range(n):
        for chosen_tuple in itertools.combinations(edges, edge_count):
            chosen = set(chosen_tuple)
            components = DisjointSet(n)
            if not all(components.join(*edge) for edge in chosen):
                continue
            component_count = n - edge_count
            rows["W0"][component_count] += 1
            if fixed_first in chosen:
                rows["W1"][component_count] += 1
                if fixed_disjoint in chosen:
                    rows["W2"][component_count] += 1
                if fixed_adjacent in chosen:
                    rows["A"][component_count] += 1
    return rows


def liu_chow(n: int, components: int) -> Fraction:
    total = Fraction()
    for r in range(min(components - 1, n - components) + 1):
        total += Fraction(
            (-1) ** r * (components + r),
            2**r
            * n**r
            * math.factorial(r)
            * math.factorial(components - r - 1)
            * math.factorial(n - components - r),
        )
    return n ** (n - components - 1) * math.factorial(n - 1) * total


def adjacent_formula(n: int, components: int) -> Fraction:
    total = Fraction()
    for r in range(components):
        lower = n - components - r - 2
        if lower < 0:
            continue
        coefficient = Fraction(
            (-1) ** r
            * (components + r + 2)
            * math.factorial(n - 3),
            2**r
            * math.factorial(r)
            * math.factorial(components - r - 1)
            * math.factorial(lower),
        )
        total += coefficient * scaled(
            1, n, n - components - r - 3
        )
    return total


def table_formula(n: int, h: int, components: int) -> Fraction:
    if (h, components) == (0, 1):
        return scaled(1, n, n - 2)
    if (h, components) == (0, 2):
        return scaled((n - 1) * (n + 6), n, n - 4, 2)
    if (h, components) == (0, 3):
        return scaled(
            (n - 2) * (n - 1) * (n * n + 13 * n + 60),
            n,
            n - 6,
            8,
        )
    if (h, components) == (1, 1):
        return scaled(2, n, n - 3)
    if (h, components) == (1, 2):
        return scaled((n - 2) * (n + 6), n, n - 5)
    if (h, components) == (1, 3):
        return scaled(
            (n - 3) * (n - 2) * (n * n + 13 * n + 60),
            n,
            n - 7,
            4,
        )
    if (h, components) == (2, 1):
        return scaled(4, n, n - 4)
    if (h, components) == (2, 2):
        return scaled(2 * (n * n + 3 * n - 20), n, n - 6)
    if (h, components) == (2, 3):
        return scaled(
            (n - 4) * (n**3 + 10 * n * n + 17 * n - 210),
            n,
            n - 8,
            2,
        )
    raise ValueError((n, h, components))


def determinant(rows: dict[str, Counter[int]], total_components: int) -> int:
    return sum(
        rows["W1"][left] * rows["W1"][total_components - left]
        - rows["W0"][left] * rows["W2"][total_components - left]
        for left in range(1, total_components)
    )


def closed_determinant(n: int, total_components: int) -> Fraction:
    if total_components == 3:
        return scaled(4, n, 2 * n - 8)
    if total_components == 4:
        return scaled(4 * (n * n + 4 * n - 24), n, 2 * n - 10)
    if total_components == 5:
        polynomial = n**3 + 12 * n * n + 20 * n - 225
        return scaled(2 * (n - 4) * polynomial, n, 2 * n - 12)
    if total_components == 6:
        polynomial = (
            n**5
            + 16 * n**4
            + 52 * n**3
            - 587 * n * n
            - 3063 * n
            + 12240
        )
        return scaled(2 * (n - 4) * polynomial, n, 2 * n - 14, 3)
    raise ValueError(total_components)


def direct_c(n: int, k: int) -> Fraction:
    rows = exhaustive_rows(n)
    total_components = 2 * n - 2 - k
    raw = determinant(rows, total_components)
    return Fraction(math.factorial(k) * raw, 2 * k * (k - 1))


def forward_difference(values: list[Fraction]) -> Fraction:
    row = list(values)
    while len(row) > 1:
        row = [right - left for left, right in zip(row, row[1:])]
    return row[0]


def closed_first_coefficient(k: int) -> Fraction:
    if k % 2:
        n = (k + 5) // 2
        return scaled(2 * math.factorial(k - 2), n, k - 3)
    n = (k + 6) // 2
    return scaled(
        math.factorial(k - 2) * (k * k + 20 * k - 12),
        n,
        k - 4,
        2,
    )


def closed_second_coefficient(k: int) -> Fraction:
    if k % 2:
        n = (k + 7) // 2
        polynomial = n**3 + 12 * n * n + 20 * n - 225
        bracket = scaled(polynomial, n, 2 * n - 12) - 2 * scaled(
            1, n - 1, 2 * n - 10
        )
    else:
        n = (k + 8) // 2
        polynomial = (
            n**5
            + 16 * n**4
            + 52 * n**3
            - 587 * n * n
            - 3063 * n
            + 12240
        )
        secondary = n * n + 2 * n - 27
        bracket = scaled(polynomial, n, 2 * n - 14, 3) - 2 * scaled(
            secondary, n - 1, 2 * n - 12
        )
    return math.factorial(k - 2) * (n - 4) * bracket


def run_audit() -> dict[str, object]:
    formula_checks = 0
    orbit_checks = 0
    determinant_checks = 0

    for n in range(4, 8):
        rows = exhaustive_rows(n)
        for components in range(1, min(3, n) + 1):
            assert rows["W0"][components] == liu_chow(n, components)
            assert rows["A"][components] == adjacent_formula(n, components)
            for h, key in ((0, "W0"), (1, "W1"), (2, "W2")):
                assert rows[key][components] == table_formula(n, h, components)
                formula_checks += 1

            edge_count = n - components
            adjacent_orbits = n * (n - 1) * (n - 2) // 2
            disjoint_orbits = n * (n - 1) * (n - 2) * (n - 3) // 8
            assert (
                adjacent_orbits * rows["A"][components]
                + disjoint_orbits * rows["W2"][components]
                == math.comb(edge_count, 2) * rows["W0"][components]
            )
            orbit_checks += 1

        for total_components in range(3, 7):
            assert determinant(rows, total_components) == closed_determinant(
                n, total_components
            )
            determinant_checks += 1

    boundary = {}
    coefficient_checks = []
    for k in range(2, 8):
        q0 = (k - 2) // 2
        values = [direct_c(4 + offset, k) for offset in range(q0 + 2)]
        first = forward_difference(values[: q0 + 1])
        assert first == closed_first_coefficient(k)
        row = {"k": k, "q0": q0, "first": int(first)}
        if k >= 3:
            second = forward_difference(values)
            assert second == closed_second_coefficient(k)
            row["second"] = int(second)
        coefficient_checks.append(row)

    for k in (2, 3, 4):
        q0 = (k - 2) // 2
        values = [direct_c(4 + offset, k) for offset in range(q0 + 2)]
        first = forward_difference(values[: q0 + 1])
        boundary[k] = {
            "q0": q0,
            "values": [int(value) for value in values],
            "first": int(first),
        }
        if k >= 3:
            boundary[k]["second"] = int(forward_difference(values))

    assert boundary == {
        2: {"q0": 0, "values": [1, 1], "first": 1},
        3: {"q0": 0, "values": [2, 12], "first": 2, "second": 10},
        4: {"q0": 1, "values": [0, 84, 462], "first": 84, "second": 294},
    }

    return {
        "schema": "amra.opg1757.independent-newton-audit.v1",
        "method": "complete edge-subset enumeration, without weighted contraction",
        "n_range": [4, 7],
        "formula_checks": formula_checks,
        "edge_pair_orbit_checks": orbit_checks,
        "determinant_checks": determinant_checks,
        "coefficient_checks": coefficient_checks,
        "boundary_cases": boundary,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run_audit(), indent=2, sort_keys=True))
