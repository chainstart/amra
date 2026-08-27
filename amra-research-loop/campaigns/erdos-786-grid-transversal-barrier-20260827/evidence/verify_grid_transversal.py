#!/usr/bin/env python3
"""Finite exact guards for the grid-transversal argument.

The script does not certify the asymptotic prime-number-theorem step.  It
checks the finite incidence algebra, exact marginals, transversal inequality,
and several advertised counterexamples on small symbolic prime pools.
"""

from __future__ import annotations

from collections import Counter
from itertools import permutations, product
from math import comb, prod


def prime_factors(n: int) -> Counter[int]:
    factors: Counter[int] = Counter()
    p = 2
    while p * p <= n:
        while n % p == 0:
            factors[p] += 1
            n //= p
        p += 1
    if n > 1:
        factors[n] += 1
    return factors


def grid_support(rows: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    d = len(rows[0])
    row_values = tuple(prod(row) for row in rows)
    column_values = tuple(prod(rows[i][j] for i in range(len(rows))) for j in range(d))
    return row_values, column_values


def check_grid_algebra() -> None:
    rows = ((2, 3, 5), (7, 11, 13))
    row_values, column_values = grid_support(rows)
    assert len(set(row_values + column_values)) == 5
    assert prod(row_values) == prod(column_values)
    assert len(row_values) != len(column_values)
    assert all(sum(prime_factors(value).values()) in {2, 3} for value in row_values + column_values)

    # A subproduct equality selects row/column indicators.  Exhaust all
    # proper selections for the K_(2,3) example.
    for row_mask in range(1 << 2):
        for col_mask in range(1 << 3):
            left = prod(row_values[i] for i in range(2) if row_mask >> i & 1)
            right = prod(column_values[j] for j in range(3) if col_mask >> j & 1)
            if left == right:
                assert (row_mask, col_mask) in {(0, 0), (3, 7)}


def all_small_grids() -> tuple[list[frozenset[int]], set[int], set[int]]:
    pools = ((2, 3, 5), (7, 11, 13))
    edges: set[frozenset[int]] = set()
    row_universe: set[int] = set()
    column_universe: set[int] = set()
    for rows in product(*(tuple(permutations(pool, 3)) for pool in pools)):
        row_values, column_values = grid_support(rows)
        row_universe.update(row_values)
        column_universe.update(column_values)
        edges.add(frozenset(row_values + column_values))
    return sorted(edges, key=lambda edge: tuple(sorted(edge))), row_universe, column_universe


def check_exact_transversal_bound() -> None:
    edges, row_universe, column_universe = all_small_grids()
    assert len(row_universe) == 2 * comb(3, 3) == 2
    assert len(column_universe) == 3**2 == 9
    universe = sorted(row_universe | column_universe)
    assert len(edges) == 6

    minimum = len(universe)
    for mask in range(1 << len(universe)):
        deletion = {universe[i] for i in range(len(universe)) if mask >> i & 1}
        if all(deletion & edge for edge in edges):
            d_col = len(deletion & column_universe)
            d_row = len(deletion & row_universe)
            assert 3 * d_col / 9 + d_row / comb(3, 3) >= 1
            minimum = min(minimum, len(deletion))
    assert minimum == 1  # Here the row-binomial term, not the column term, controls.
    assert comb(3, 3) < 3 ** 2 / 3  # Kills the all-parameter binomial shortcut.


def check_exact_marginals() -> None:
    pools = ((2, 3, 5, 17), (7, 11, 13, 19))
    grids = list(product(*(tuple(permutations(pool, 3)) for pool in pools)))
    fixed_column = 2 * 7
    fixed_row = 2 * 3 * 5
    column_hits = 0
    row_hits = 0
    for rows in grids:
        row_values, column_values = grid_support(rows)
        column_hits += sum(value == fixed_column for value in column_values)
        row_hits += fixed_row in row_values
    # Across all three column positions, the expected number of appearances
    # is d/m^(d-1); row 1 is uniform over C(m,d) unordered products.
    assert column_hits / len(grids) == 3 / 4**2
    assert row_hits / len(grids) == 1 / comb(4, 3)

    # Two columns cannot use the same prime from row 1, so they are not
    # independent samples from the column universe.
    assert all(rows[0][0] != rows[0][1] for rows in grids)


def check_height_and_tail() -> None:
    d = 4
    x = 200
    rows = ((101, 103, 107, 109), (113, 127, 131, 137), (139, 149, 151, 157))
    row_values, column_values = grid_support(rows)
    n = x**d
    assert max(row_values + column_values) <= n
    assert min(row_values + column_values) > (x / 2) ** (d - 1)


def check_dense_atlas_conditions() -> None:
    d = 3
    r = d - 1
    m = 1000
    delta = 0.5
    assert delta * m >= 2 * d * r
    assert m > 2**d * 6 * delta ** (-d)
    lower_matchings = (delta * m**r / 2) ** d
    row_blocked_upper = 6 * m ** (r * d - 1)
    assert row_blocked_upper < lower_matchings


def main() -> None:
    check_grid_algebra()
    check_exact_transversal_bound()
    check_exact_marginals()
    check_height_and_tail()
    check_dense_atlas_conditions()
    print("PASS: grid algebra, marginals, transversal bound, counterexamples, and height guards")


if __name__ == "__main__":
    main()
