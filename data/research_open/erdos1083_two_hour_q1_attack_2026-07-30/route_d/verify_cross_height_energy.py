#!/usr/bin/env python3
"""Exact certificates for the Route D cross-height analysis.

The finite model is checked using rational squared coordinates.  We never
need to adjoin the square roots used as Euclidean coordinates: the direct
distance calculation only involves their squares.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product


def endpoint_certificate() -> dict[str, Fraction]:
    """Return and verify every exponent at the former 9/41 endpoint."""

    s = Fraction(32, 41)
    u = Fraction(35, 41)
    h = Fraction(88, 41)
    r = Fraction(41, 41)
    d = Fraction(123, 41)

    domain = s + u + h
    collision_lower = 2 * domain - d
    same_height_upper = r + s + h

    assert domain == Fraction(155, 41)
    assert collision_lower == Fraction(187, 41)
    assert collision_lower == 2 * s + u + h
    assert same_height_upper == Fraction(161, 41)
    assert collision_lower - same_height_upper == Fraction(26, 41)
    assert h - 2 * r == Fraction(6, 41)

    return {
        "source_sines": s,
        "row_size": u,
        "height_count": h,
        "global_tangent_squares": r,
        "distance_budget": d,
        "triple_domain": domain,
        "collision_lower": collision_lower,
        "same_height_upper": same_height_upper,
        "same_height_gap": collision_lower - same_height_upper,
        "minimal_row_height_gap": h - 2 * r,
    }


def two_ninths_endpoint_certificate() -> dict[str, Fraction]:
    """Verify the cross-height gaps at the new 2/9 scalar endpoint."""

    s = Fraction(7, 9)
    u = Fraction(5, 6)
    h = Fraction(19, 9)
    r = Fraction(1)
    d = Fraction(3)

    domain = s + u + h
    collision_lower = 2 * domain - d
    same_height_upper = r + s + h

    assert domain == Fraction(67, 18)
    assert u + h == Fraction(53, 18)
    assert collision_lower == Fraction(40, 9)
    assert same_height_upper == Fraction(35, 9)
    assert collision_lower - same_height_upper == Fraction(5, 9)
    assert h - 2 * r == Fraction(1, 9)

    return {
        "source_sines": s,
        "row_size": u,
        "height_count": h,
        "global_tangent_squares": r,
        "distance_budget": d,
        "triple_domain": domain,
        "target_fibre_size": u + h,
        "collision_lower": collision_lower,
        "same_height_upper": same_height_upper,
        "same_height_gap": collision_lower - same_height_upper,
        "minimal_row_height_gap": h - 2 * r,
    }


def cancellation_model(
    source_count: int = 5,
    row_size: int = 7,
    height_count: int = 11,
) -> dict[str, object]:
    """Build the exact Euclidean cancellation model from the note.

    We set rho=1 and choose K>2*row_size*height_count.  The source sine
    coordinates are i/K.  At height -z, the j-th target has

        y^2 = C-z^2+2*z*j/K.

    Its squared distance from source point i is

        1+C+2*z*(i+j)/K.
    """

    if not (2 <= source_count <= row_size and height_count >= 2):
        raise ValueError("require 2 <= source_count <= row_size and height_count >= 2")

    k_den = 2 * row_size * height_count + 1
    c_shift = height_count * height_count + 1

    source_sines = tuple(Fraction(i, k_den) for i in range(1, source_count + 1))
    assert all(0 < x < 1 for x in source_sines)

    target_square_y: dict[tuple[int, int], Fraction] = {}
    producer_labels: dict[tuple[int, int], Fraction] = {}
    direct_distances: set[Fraction] = set()
    formula_distances: set[Fraction] = set()

    for z, j in product(
        range(1, height_count + 1),
        range(1, row_size + 1),
    ):
        y2 = Fraction(c_shift - z * z, 1) + Fraction(2 * z * j, k_den)
        assert y2 > 0
        target_square_y[(z, j)] = y2
        producer_labels[(z, j)] = 1 + y2

        # On the radius-one circle centered at height -z, translate
        # the same source angular set.  Every translated source point
        # is at the selected squared distance 1+y^2 from q_(z,j).
        for sine in source_sines:
            producer_distance = (1 - sine * sine) + y2 + sine * sine
            assert producer_distance == producer_labels[(z, j)]

        for i, sine in enumerate(source_sines, start=1):
            # Direct Cartesian calculation:
            # (rho*cos(phi))^2 + y^2 + (rho*sin(phi)+z)^2.
            direct = (1 - sine * sine) + y2 + (sine + z) ** 2
            formula = Fraction(1 + c_shift, 1) + Fraction(2 * z * (i + j), k_den)
            assert direct == formula
            direct_distances.add(direct)
            formula_distances.add(formula)

    # K>2UH separates the rational y^2 values belonging to different z.
    assert len(set(target_square_y.values())) == row_size * height_count
    assert direct_distances == formula_distances
    assert len(direct_distances) <= height_count * (source_count + row_size - 1)
    assert len(direct_distances) <= 2 * row_size * height_count

    return {
        "source_count": source_count,
        "row_size": row_size,
        "height_count": height_count,
        "denominator": k_den,
        "target_count": row_size * height_count,
        "target_plane_count": len(set(target_square_y.values())),
        "distance_count": len(direct_distances),
        "distance_upper": height_count * (source_count + row_size - 1),
        "source_sines": source_sines,
        "target_square_y": target_square_y,
        "producer_labels": producer_labels,
        "reverse_circle_count": height_count,
        "source_points_per_reverse_circle": source_count,
        "producers_per_reverse_circle": row_size,
        "distances": direct_distances,
    }


def minimal_row_pair_bound(global_size: int) -> int:
    """Maximum number of signed nonzero heights certified by endpoint pairs."""

    if global_size < 2:
        return 0
    return global_size * (global_size - 1)


def main() -> None:
    endpoint = endpoint_certificate()
    new_endpoint = two_ninths_endpoint_certificate()
    model = cancellation_model()

    print("endpoint certificate")
    for key, value in endpoint.items():
        print(f"  {key}: {value}")

    print("2/9 endpoint certificate")
    for key, value in new_endpoint.items():
        print(f"  {key}: {value}")

    print("finite Euclidean cancellation model")
    for key in (
        "source_count",
        "row_size",
        "height_count",
        "target_count",
        "target_plane_count",
        "distance_count",
        "distance_upper",
    ):
        print(f"  {key}: {model[key]}")


if __name__ == "__main__":
    main()
