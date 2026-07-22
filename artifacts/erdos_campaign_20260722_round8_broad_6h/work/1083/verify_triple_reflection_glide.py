#!/usr/bin/env python3
"""Exact rational audit of the three-reflection glide criterion for #1083.

The universal complex-coordinate proof is in near_reflection_stability.md.
Here all affine matrices use Fraction arithmetic.  For every ordered triple of
sample pairwise nonparallel rational directions, the square of r1 r2 r3 is
checked to be the identity when the third line passes through L1 cap L2 and a
nonzero translation when it does not.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations
import json


Vector = tuple[F, F]
Matrix = tuple[tuple[F, F], tuple[F, F]]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))  # type: ignore[return-value]


def matvec(a: Matrix, x: Vector) -> Vector:
    return tuple(sum(a[i][k] * x[k] for k in range(2)) for i in range(2))  # type: ignore[return-value]


def add(x: Vector, y: Vector) -> Vector:
    return (x[0] + y[0], x[1] + y[1])


def reflection(direction: tuple[int, int], point: Vector) -> tuple[Matrix, Vector]:
    x, y = map(F, direction)
    norm = x * x + y * y
    a: Matrix = (
        (2 * x * x / norm - 1, 2 * x * y / norm),
        (2 * x * y / norm, 2 * y * y / norm - 1),
    )
    ap = matvec(a, point)
    return a, (point[0] - ap[0], point[1] - ap[1])


def compose(left: tuple[Matrix, Vector], right: tuple[Matrix, Vector]) -> tuple[Matrix, Vector]:
    a, b = left
    c, d = right
    return matmul(a, c), add(matvec(a, d), b)


def determinant(u: tuple[int, int], v: tuple[int, int]) -> int:
    return u[0] * v[1] - u[1] * v[0]


def main() -> None:
    directions = [(1, 0), (0, 1), (1, 1), (1, 2), (2, 1), (1, -1), (2, -1)]
    identity: Matrix = ((F(1), F(0)), (F(0), F(1)))
    zero: Vector = (F(0), F(0))
    tested = 0
    for d1, d2, d3 in permutations(directions, 3):
        if determinant(d1, d2) == 0 or determinant(d1, d3) == 0 or determinant(d2, d3) == 0:
            continue
        r1 = reflection(d1, zero)
        r2 = reflection(d2, zero)

        # Concurrent case: all three lines pass through the origin.
        r3_concurrent = reflection(d3, zero)
        w = compose(compose(r1, r2), r3_concurrent)
        w2 = compose(w, w)
        assert w2 == (identity, zero)

        # Nonconcurrent case: translate L3 by its integer normal vector.
        point = (F(-d3[1]), F(d3[0]))
        r3_shifted = reflection(d3, point)
        w = compose(compose(r1, r2), r3_shifted)
        w2 = compose(w, w)
        assert w2[0] == identity
        assert w2[1] != zero
        tested += 1

    print(json.dumps({
        "schema": "amra.erdos1083.round8.triple_reflection_glide.v1",
        "ordered_pairwise_nonparallel_triples_checked": tested,
        "arithmetic": "exact rational affine 2x2 matrices",
        "concurrent_case": "(r1 r2 r3)^2 is identity",
        "nonconcurrent_case": "(r1 r2 r3)^2 is a nonzero translation",
        "warning": "finite audit only; universal proof is in markdown",
        "result": "PASS",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
