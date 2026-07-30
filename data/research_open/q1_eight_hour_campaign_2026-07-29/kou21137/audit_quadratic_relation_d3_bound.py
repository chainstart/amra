#!/usr/bin/env python3
"""Exhaustive Gr(2,4)(F_3) audit for the quadratic-relation d3 bound."""

from __future__ import annotations

import itertools


PRIME = 3


def rank(rows: list[list[int]], columns: int) -> int:
    matrix = [
        [value % PRIME for value in row]
        for row in rows
        if any(value % PRIME for value in row)
    ]
    output = 0
    for column in range(columns):
        pivot = next(
            (
                index
                for index in range(output, len(matrix))
                if matrix[index][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[output], matrix[pivot] = matrix[pivot], matrix[output]
        inverse = 1 if matrix[output][column] == 1 else 2
        matrix[output] = [
            inverse * value % PRIME for value in matrix[output]
        ]
        for index, row in enumerate(matrix):
            if index == output or row[column] == 0:
                continue
            coefficient = row[column]
            matrix[index] = [
                (value - coefficient * pivot_value) % PRIME
                for value, pivot_value in zip(row, matrix[output])
            ]
        output += 1
    return output


def rref(rows: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    matrix = [list(row) for row in rows]
    output = 0
    for column in range(4):
        pivot = next(
            (
                index
                for index in range(output, len(matrix))
                if matrix[index][column] % PRIME
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[output], matrix[pivot] = matrix[pivot], matrix[output]
        inverse = 1 if matrix[output][column] % PRIME == 1 else 2
        matrix[output] = [
            inverse * value % PRIME for value in matrix[output]
        ]
        for index, row in enumerate(matrix):
            if index == output or row[column] % PRIME == 0:
                continue
            coefficient = row[column] % PRIME
            matrix[index] = [
                (value - coefficient * pivot_value) % PRIME
                for value, pivot_value in zip(row, matrix[output])
            ]
        output += 1
        if output == len(matrix):
            break
    return tuple(tuple(row) for row in matrix[:output])


def relation_planes() -> list[tuple[tuple[int, ...], ...]]:
    nonzero = [
        vector
        for vector in itertools.product(range(PRIME), repeat=4)
        if any(vector)
    ]
    planes = {
        rref((first, second))
        for first in nonzero
        for second in nonzero
        if rank([list(first), list(second)], 4) == 2
    }
    return sorted(planes)


def tensor_relation_rows(
    plane: tuple[tuple[int, ...], ...]
) -> list[list[int]]:
    rows: list[list[int]] = []
    for relation in plane:
        for outer in range(2):
            left = [0] * 8
            right = [0] * 8
            for word_index, coefficient in enumerate(relation):
                first, second = divmod(word_index, 2)
                left[4 * outer + 2 * first + second] = coefficient
                right[4 * first + 2 * second + outer] = coefficient
            rows.extend((left, right))
    return rows


def main() -> int:
    planes = relation_planes()
    assert len(planes) == 130
    distribution = {0: 0, 1: 0, 2: 0}
    maximum = 0
    for plane in planes:
        quotient_dimension = 8 - rank(
            tensor_relation_rows(plane), 8
        )
        assert quotient_dimension in distribution
        distribution[quotient_dimension] += 1
        maximum = max(maximum, quotient_dimension)
    assert maximum == 2
    assert sum(distribution.values()) == 130
    print(
        "QUADRATIC_RELATION_D3_AUDIT"
        "|field=F3"
        "|dim_V=2"
        "|dim_R=2"
        f"|grassmannian_planes={len(planes)}"
        f"|quotient_dim_0={distribution[0]}"
        f"|quotient_dim_1={distribution[1]}"
        f"|quotient_dim_2={distribution[2]}"
        f"|maximum_d3={maximum}"
        "|profile_2231111_possible=false"
    )
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
