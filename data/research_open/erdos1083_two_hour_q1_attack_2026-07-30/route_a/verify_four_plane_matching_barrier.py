#!/usr/bin/env python3
"""Exact verifier for the route-A four-plane matching barrier.

All Euclidean coordinates and squared distances are represented by
fractions.Fraction.  No floating-point comparison enters the certificate.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Dict, List, Sequence, Tuple


RationalPoint2 = Tuple[Fraction, Fraction]
RationalPoint3 = Tuple[Fraction, Fraction, int]


def rational_rotation(k: int) -> Tuple[Fraction, Fraction]:
    """Return cos(phi), sin(phi) for phi=2 arctan(1/(16k))."""
    if k < 1:
        raise ValueError("k must be positive")
    u = Fraction(1, 16 * k)
    denominator = 1 + u * u
    return (1 - u * u) / denominator, 2 * u / denominator


def rotate(
    point: RationalPoint2, cosine: Fraction, sine: Fraction
) -> RationalPoint2:
    x, y = point
    return cosine * x - sine * y, sine * x + cosine * y


def horizontal_points(k: int) -> List[RationalPoint2]:
    cosine, sine = rational_rotation(k)
    points = [(Fraction(1), Fraction(0))]
    for _ in range(1, 2 * k):
        points.append(rotate(points[-1], cosine, sine))
    return points


def squared_horizontal_distance(
    p: RationalPoint2, q: RationalPoint2
) -> Fraction:
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def horizontal_labels(k: int) -> List[Fraction]:
    points = horizontal_points(k)
    return [squared_horizontal_distance(points[0], points[h]) for h in range(2 * k)]


def point_columns(k: int, q: int) -> List[List[RationalPoint3]]:
    if q < 1:
        raise ValueError("q must be positive")
    return [
        [(x, y, z) for z in range(q)]
        for x, y in horizontal_points(k)
    ]


def squared_distance(p: RationalPoint3, q: RationalPoint3) -> Fraction:
    return (
        (p[0] - q[0]) ** 2
        + (p[1] - q[1]) ** 2
        + Fraction((p[2] - q[2]) ** 2)
    )


def enumerate_squared_distances(k: int, q: int) -> set[Fraction]:
    columns = point_columns(k, q)
    points = [point for column in columns for point in column]
    return {squared_distance(p, r) for p in points for r in points}


def predicted_squared_distances(k: int, q: int) -> set[Fraction]:
    return {
        horizontal + vertical * vertical
        for horizontal, vertical in product(horizontal_labels(k), range(q))
    }


def adjacent_coefficient(k: int, edge_index: int) -> Fraction:
    points = horizontal_points(k)
    i = 2 * edge_index
    p, q = points[i], points[i + 1]
    return p[0] * q[0] + p[1] * q[1]


def cell_weight(q: int, height_difference: int) -> int:
    if not 0 <= height_difference < q:
        return 0
    if height_difference == 0:
        return q
    return 2 * (q - height_difference)


def exact_cell_weight_from_columns(
    k: int, q: int, edge_index: int, height_difference: int
) -> int:
    columns = point_columns(k, q)
    i = 2 * edge_index
    target = horizontal_labels(k)[1] + height_difference**2
    return sum(
        squared_distance(p, r) == target
        for p in columns[i]
        for r in columns[i + 1]
    )


def diagonalization_identity(
    c: Fraction, x: Fraction, y: Fraction, h: Fraction
) -> bool:
    left = x * x + y * y - 2 * c * x * y + h * h
    twice_right = (
        (1 - c) * (x + y) ** 2
        + (1 + c) * (x - y) ** 2
        + 2 * h * h
    )
    return 2 * left == twice_right


def coefficient_diverse_base_columns(k: int) -> List[Tuple[RationalPoint2, RationalPoint2]]:
    if k < 1:
        raise ValueError("k must be positive")
    return [
        (
            (Fraction(3 * r), Fraction(1)),
            (Fraction(3 * r + 1), Fraction(1)),
        )
        for r in range(1, k + 1)
    ]


def squared_cosine(p: RationalPoint2, q: RationalPoint2) -> Fraction:
    dot = p[0] * q[0] + p[1] * q[1]
    norm_p = p[0] * p[0] + p[1] * p[1]
    norm_q = q[0] * q[0] + q[1] * q[1]
    return dot * dot / (norm_p * norm_q)


def coefficient_diverse_points(k: int, q: int) -> List[RationalPoint3]:
    return [
        (point[0], point[1], z)
        for pair in coefficient_diverse_base_columns(k)
        for point in pair
        for z in range(q)
    ]


def enumerate_coefficient_diverse_distances(k: int, q: int) -> set[Fraction]:
    points = coefficient_diverse_points(k, q)
    return {squared_distance(p, r) for p in points for r in points}


def verify_coefficient_diverse_case(k: int, q: int) -> Dict[str, object]:
    base_pairs = coefficient_diverse_base_columns(k)
    base_points = [point for pair in base_pairs for point in pair]
    slopes = [point[1] / point[0] for point in base_points]
    assert len(set(slopes)) == 2 * k

    chord_squares = [squared_horizontal_distance(p, r) for p, r in base_pairs]
    assert chord_squares == [Fraction(1)] * k

    squared_coefficients = [squared_cosine(p, r) for p, r in base_pairs]
    assert squared_coefficients == sorted(set(squared_coefficients))

    distances = enumerate_coefficient_diverse_distances(k, q)
    assert len(distances) <= 3 * k * q

    for height_difference in range(q // 2 + 1):
        target = Fraction(1 + height_difference * height_difference)
        expected = cell_weight(q, height_difference)
        for p, r in base_pairs:
            left_column = [(p[0], p[1], z) for z in range(q)]
            right_column = [(r[0], r[1], z) for z in range(q)]
            actual = sum(
                squared_distance(left, right) == target
                for left in left_column
                for right in right_column
            )
            assert actual == expected

    return {
        "K": k,
        "Q": q,
        "point_count": 2 * k * q,
        "distinct_squared_coefficients": len(set(squared_coefficients)),
        "squared_distances_including_zero": len(distances),
        "upper_bound_3KQ": 3 * k * q,
        "exact_arithmetic": True,
    }


def verify_case(k: int, q: int) -> Dict[str, object]:
    if k < 1 or q < 1:
        raise ValueError("k and q must be positive")

    horizontal = horizontal_labels(k)
    assert horizontal[0] == 0
    assert all(horizontal[i] < horizontal[i + 1] for i in range(2 * k - 1))
    assert all(Fraction(0) <= value < Fraction(1) for value in horizontal)

    predicted = predicted_squared_distances(k, q)
    enumerated = enumerate_squared_distances(k, q)
    assert enumerated == predicted
    assert len(enumerated) == 2 * k * q

    cosine, _ = rational_rotation(k)
    coefficients = [adjacent_coefficient(k, edge) for edge in range(k)]
    assert coefficients == [cosine] * k

    max_rich_height = q // 2
    weights: List[int] = []
    for height_difference in range(max_rich_height + 1):
        expected = cell_weight(q, height_difference)
        assert expected >= q
        for edge in range(k):
            assert (
                exact_cell_weight_from_columns(
                    k, q, edge, height_difference
                )
                == expected
            )
        weights.append(expected)

    samples: Sequence[Tuple[Fraction, Fraction, Fraction, Fraction]] = (
        (Fraction(1, 3), Fraction(2, 5), Fraction(-7, 4), Fraction(3, 2)),
        (Fraction(-2), Fraction(5, 7), Fraction(11, 9), Fraction(-4, 5)),
    )
    for c in (Fraction(-3, 5), Fraction(0), Fraction(7, 11)):
        for x, y, h, _ in samples:
            assert diagonalization_identity(c, x, y, h)

    selected_cross_codegrees = [
        k * (k - 1) * weight * weight for weight in weights
    ]

    return {
        "K": k,
        "Q": q,
        "point_count": 2 * k * q,
        "squared_distances_including_zero": len(enumerated),
        "nonzero_squared_distances": len(enumerated) - 1,
        "common_rich_labels_checked": max_rich_height + 1,
        "common_adjacent_coefficient": str(cosine),
        "cell_weights": weights,
        "selected_cross_codegrees": selected_cross_codegrees,
        "exact_arithmetic": True,
    }


def main() -> None:
    for k, q in ((2, 5), (3, 6), (4, 7)):
        print(verify_case(k, q))
        print(verify_coefficient_diverse_case(k, q))


if __name__ == "__main__":
    main()
