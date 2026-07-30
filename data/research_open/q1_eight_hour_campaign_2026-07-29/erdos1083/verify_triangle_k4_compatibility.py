#!/usr/bin/env python3
"""Exact certificates for triangle and K4 squared-distance compatibility."""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import asdict, dataclass
from fractions import Fraction


EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
TRIANGLES = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))


@dataclass(frozen=True)
class K4ObstructionCertificate:
    lengths: tuple[int, ...]
    all_triangle_equations_hold: bool
    gram_entries: tuple[int, int, int]
    gram_product: int
    required_product: int
    k4_identity_holds: bool
    line_embedding_exists: bool


@dataclass(frozen=True)
class SupportCertificate:
    set_size: int
    point_quadruples: int
    compatible_six_tuples: int
    lower_bound: Fraction
    all_k4_identities_hold: bool
    cubic_upper_bound: int


def triangle_polynomial(first: int, second: int, third: int) -> int:
    return (third - first - second) ** 2 - 4 * first * second


def k4_identity(squares: dict[tuple[int, int], int]) -> tuple[int, int]:
    left = (
        (squares[(0, 1)] + squares[(0, 2)] - squares[(1, 2)])
        * (squares[(0, 1)] + squares[(0, 3)] - squares[(1, 3)])
        * (squares[(0, 2)] + squares[(0, 3)] - squares[(2, 3)])
    )
    right = (
        8
        * squares[(0, 1)]
        * squares[(0, 2)]
        * squares[(0, 3)]
    )
    return left, right


def all_triangle_equations(squares: dict[tuple[int, int], int]) -> bool:
    for first, middle, third in TRIANGLES:
        if triangle_polynomial(
            squares[tuple(sorted((first, middle)))],
            squares[tuple(sorted((middle, third)))],
            squares[tuple(sorted((first, third)))],
        ) != 0:
            return False
    return True


def line_embedding_exists(lengths: dict[tuple[int, int], int]) -> bool:
    for signs in itertools.product((-1, 1), repeat=3):
        points = (0,) + tuple(
            signs[index - 1] * lengths[(0, index)]
            for index in range(1, 4)
        )
        if all(
            abs(points[first] - points[second]) == length
            for (first, second), length in lengths.items()
        ):
            return True
    return False


def obstruction_certificate() -> K4ObstructionCertificate:
    lengths = {
        (0, 1): 1,
        (0, 2): 1,
        (0, 3): 2,
        (1, 2): 2,
        (1, 3): 1,
        (2, 3): 1,
    }
    squares = {edge: value * value for edge, value in lengths.items()}
    gram = (
        (squares[(0, 1)] + squares[(0, 2)] - squares[(1, 2)]) // 2,
        (squares[(0, 1)] + squares[(0, 3)] - squares[(1, 3)]) // 2,
        (squares[(0, 2)] + squares[(0, 3)] - squares[(2, 3)]) // 2,
    )
    left, right = k4_identity(squares)
    return K4ObstructionCertificate(
        lengths=tuple(lengths[edge] for edge in EDGES),
        all_triangle_equations_hold=all_triangle_equations(squares),
        gram_entries=gram,
        gram_product=gram[0] * gram[1] * gram[2],
        required_product=(
            squares[(0, 1)] * squares[(0, 2)] * squares[(0, 3)]
        ),
        k4_identity_holds=left == right,
        line_embedding_exists=line_embedding_exists(lengths),
    )


def squared_six_tuple(points: tuple[int, int, int, int]) -> tuple[int, ...]:
    return tuple(
        (points[first] - points[second]) ** 2
        for first, second in EDGES
    )


def support_certificate(size: int) -> SupportCertificate:
    values = tuple(range(1, size + 1))
    six_tuples = {
        squared_six_tuple(points)
        for points in itertools.product(values, repeat=4)
    }
    valid = True
    for values_tuple in six_tuples:
        squares = dict(zip(EDGES, values_tuple))
        left, right = k4_identity(squares)
        valid = valid and all_triangle_equations(squares) and left == right
    return SupportCertificate(
        set_size=size,
        point_quadruples=size**4,
        compatible_six_tuples=len(six_tuples),
        lower_bound=Fraction(size**3, 8),
        all_k4_identities_hold=valid,
        cubic_upper_bound=(2 * size - 1) ** 3,
    )


def triangle_saturation(size: int) -> int:
    return len(
        {
            (first * first, second * second, (first + second) ** 2)
            for first in range(1, size + 1)
            for second in range(1, size + 1)
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=8)
    args = parser.parse_args()
    support = support_certificate(args.size)
    payload = {
        "triangle_saturation": {
            "size": args.size,
            "edge_count": triangle_saturation(args.size),
            "expected": args.size**2,
        },
        "k4_obstruction": asdict(obstruction_certificate()),
        "k4_support": {
            **asdict(support),
            "lower_bound": str(support.lower_bound),
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
