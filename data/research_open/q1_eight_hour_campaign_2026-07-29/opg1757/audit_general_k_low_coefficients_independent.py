#!/usr/bin/env python3
"""Independent audit of the general-k low-coefficient calculation.

This verifier deliberately does not import any of the fixed-page formula
modules.  It checks the argument in three different ways:

1. derive the four-, five-, and six-edge cycle defects symbolically;
2. enumerate all bipartite edge subsets through degree six for small stable
   parameters and reconstruct the first three coefficients of K_k;
3. compute the complete-graph forest determinant that occurs at the first
   possible degree of F_k by a component recurrence, rather than by the
   Bell-state transfer.
"""

from __future__ import annotations

import functools
import itertools
import math

import sympy as sp


K, S, H = sp.symbols("k s h", integer=True)


def c2(value: sp.Expr) -> sp.Expr:
    return value * (value - 1) / 2


def c3(value: sp.Expr) -> sp.Expr:
    return value * (value - 1) * (value - 2) / 6


def second_difference(expression: sp.Expr) -> sp.Expr:
    return sp.expand(
        expression.subs(H, 0)
        + expression.subs(H, 2)
        - 2 * expression.subs(H, 1)
    )


def symbolic_k_coefficients() -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    """Derive [beta^0..2] K_k from the cycle classification."""

    ones = S - 2 * H
    q = c2(ones) + 4 * H * ones + 16 * c2(H)
    t = 2 * c2(ones) + 12 * H * ones + 64 * c2(H)
    u = 10 * c2(ones) + 92 * H * ones + 640 * c2(H)
    v = c2(ones) + 8 * H * ones + 64 * c2(H)
    w = c3(ones) + 4 * H * c2(ones) + 16 * c2(H) * ones

    edge_e2 = ((K * S) ** 2 - K * (S + 2 * H)) / 2
    four = c2(K) * q
    five = c2(K) * (K * S * q - 2 * t)
    six = (
        c2(K) * (edge_e2 * q - 2 * K * S * t + u)
        - 2 * c3(K) * v
        + (6 * c3(K) - 2 * c2(K)) * w
    )

    d4 = second_difference(four)
    d5 = second_difference(five) + K * S * d4
    d6 = (
        second_difference(six)
        + K * S * second_difference(five)
        + four.subs(H, 0) * edge_e2.subs(H, 2)
        + four.subs(H, 2) * edge_e2.subs(H, 0)
        - 2 * four.subs(H, 1) * edge_e2.subs(H, 1)
    )

    exponent = 2 * S - 2 * K - 2
    n4 = sp.factor(d4)
    n5 = sp.factor(d5 - exponent * K * n4)
    n6 = sp.factor(
        d6
        - exponent * K * n5
        - c2(exponent) * K**2 * n4
    )
    normalizer = 2 * K * (K - 1)
    return tuple(sp.factor(value / normalizer) for value in (n4, n5, n6))


def is_forest(
    core_count: int,
    page_count: int,
    selected: tuple[tuple[int, int, int], ...],
) -> bool:
    parent = list(range(core_count + page_count))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for core, page, _ in selected:
        left = find(core)
        right = find(core_count + page)
        if left == right:
            return False
        parent[left] = right
    return True


def bipartite_forest_coefficients(
    page_count: int, s: int, two_blocks: int, maximum_degree: int = 7
) -> list[int]:
    """Enumerate H_h directly through ``maximum_degree``."""

    weights = [2] * two_blocks + [1] * (s - 2 * two_blocks)
    edges = [
        (core, page, weight)
        for core, weight in enumerate(weights)
        for page in range(page_count)
    ]
    answer: list[int] = []
    for degree in range(maximum_degree + 1):
        total = 0
        for selected in itertools.combinations(edges, degree):
            if is_forest(len(weights), page_count, selected):
                total += math.prod(edge[2] for edge in selected)
        answer.append(total)
    return answer


def convolution_coefficient(
    left: list[int], right: list[int], degree: int
) -> int:
    return sum(
        left[index] * right[degree - index]
        for index in range(degree + 1)
    )


def brute_k_coefficients(
    page_count: int, s: int
) -> tuple[int, int, int, int]:
    """Reconstruct the first four K_k coefficients from full forests."""

    profiles = [
        bipartite_forest_coefficients(page_count, s, h) for h in range(3)
    ]
    determinant = [
        convolution_coefficient(profiles[1], profiles[1], degree)
        - convolution_coefficient(profiles[0], profiles[2], degree)
        for degree in range(8)
    ]
    if determinant[:4] != [0, 0, 0, 0]:
        raise AssertionError("the unrestricted-slot cancellation failed")

    exponent = 2 * s - 2 * page_count - 2
    n4 = determinant[4]
    n5 = determinant[5] - exponent * page_count * n4
    n6 = (
        determinant[6]
        - exponent * page_count * n5
        - math.comb(exponent, 2) * page_count**2 * n4
    )
    n7 = (
        determinant[7]
        - exponent * page_count * n6
        - math.comb(exponent, 2) * page_count**2 * n5
        - math.comb(exponent, 3) * page_count**3 * n4
    )
    normalizer = 2 * page_count * (page_count - 1)
    if any(value % normalizer for value in (n4, n5, n6, n7)):
        raise AssertionError("normalization is not integral")
    return tuple(value // normalizer for value in (n4, n5, n6, n7))


@functools.cache
def weighted_complete_forest_coefficients(
    double_vertices: int, unit_vertices: int, maximum_degree: int
) -> tuple[int, ...]:
    """Forest polynomial for edge weights w_i w_j, by components.

    The component containing a distinguished vertex has ``a`` double and
    ``b`` unit vertices.  Weighted Cayley gives tree weight

        2^a (2a+b)^(a+b-2)

    for a nontrivial component.
    """

    result = [0] * (maximum_degree + 1)
    if double_vertices + unit_vertices == 0:
        result[0] = 1
        return tuple(result)

    if double_vertices:
        choices = (
            (a, b, math.comb(double_vertices - 1, a - 1)
             * math.comb(unit_vertices, b))
            for a in range(1, double_vertices + 1)
            for b in range(unit_vertices + 1)
        )
    else:
        choices = (
            (0, b, math.comb(unit_vertices - 1, b - 1))
            for b in range(1, unit_vertices + 1)
        )

    for a, b, multiplicity in choices:
        size = a + b
        degree = size - 1
        if degree > maximum_degree:
            continue
        tree_weight = (
            1
            if size == 1
            else 2**a * (2 * a + b) ** (size - 2)
        )
        remainder = weighted_complete_forest_coefficients(
            double_vertices - a,
            unit_vertices - b,
            maximum_degree - degree,
        )
        for old_degree, coefficient in enumerate(remainder):
            if old_degree + degree <= maximum_degree:
                result[old_degree + degree] += (
                    multiplicity * tree_weight * coefficient
                )
    return tuple(result)


def first_f_coefficient(page_count: int, s: int) -> int:
    """Evaluate the complete-graph extraction in formula (17)."""

    profiles = [
        weighted_complete_forest_coefficients(h, s - 2 * h, page_count)
        for h in range(3)
    ]
    determinant = sum(
        profiles[1][degree] * profiles[1][page_count - degree]
        - profiles[0][degree] * profiles[2][page_count - degree]
        for degree in range(page_count + 1)
    )
    numerator = math.factorial(page_count) * determinant
    denominator = 2 * page_count * (page_count - 1)
    if numerator % denominator:
        raise AssertionError("formula (17) is not integral")
    return numerator // denominator


def main() -> None:
    symbolic = symbolic_k_coefficients()
    expected = (
        sp.S.One,
        2 * (K - 2) * (K + 3),
        (K - 2)
        * ((K + 3) * S + 2 * K**3 + 7 * K**2 - 9 * K - 60),
        2
        * (K - 2)
        * (
            (3 * K**3 + 11 * K**2 - 11 * K - 105) * S
            + (K - 3)
            * (2 * K**4 + 13 * K**3 + 18 * K**2 - 96 * K - 300)
        )
        / 3,
    )
    if any(
        sp.expand(a - b) != 0
        for a, b in zip(symbolic, expected[:3])
    ):
        raise AssertionError("symbolic low-coefficient formula failed")

    brute_rows: list[tuple[int, int, tuple[int, int, int, int]]] = []
    for page_count in range(2, 5):
        s = page_count + 3
        actual = brute_k_coefficients(page_count, s)
        target = tuple(
            int(expression.subs({K: page_count, S: s}))
            for expression in expected
        )
        if actual != target:
            raise AssertionError(
                f"direct forest mismatch at k={page_count}, s={s}"
            )
        brute_rows.append((page_count, s, actual))

    extraction_rows: list[tuple[int, int, int]] = []
    for page_count in range(2, 11):
        for s in (max(4, page_count), max(4, page_count) + 1):
            value = first_f_coefficient(page_count, s)
            if value < 0:
                raise AssertionError(
                    f"negative extraction at k={page_count}, s={s}"
                )
            extraction_rows.append((page_count, s, value))

    print("SYMBOLIC_K_LOW|", tuple(map(str, symbolic)))
    print("DIRECT_BIPARTITE_ROWS|", brute_rows)
    print("COMPLETE_GRAPH_EXTRACTION_ROWS|", extraction_rows)
    print("STATUS|PASS")


if __name__ == "__main__":
    main()
