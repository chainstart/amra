#!/usr/bin/env python3
"""Verify the 11-dimensional sharp witness for noncommuting raw cubes.

This is deliberately not a Wilson counterexample: the raw cube set is not
closed.  The witness shows only that a dimension-eleven lower bound obtained
from cube commutativity cannot be improved by dimension counting alone.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

PRIME = 3

# A_i denotes a^i for 1 <= i <= 5.  B_i denotes a^(i-1)b for
# 1 <= i <= 6.  The missing A_6 is killed.
BASIS = tuple(
    item
    for degree in range(1, 7)
    for item in (
        (("A", degree), ("B", degree))
        if degree <= 5
        else (("B", degree),)
    )
)
INDEX = {item: index for index, item in enumerate(BASIS)}
DIMENSION = len(BASIS)

Vector = tuple[int, ...]


def zero() -> Vector:
    return (0,) * DIMENSION


def basis_vector(kind: str, degree: int, coefficient: int = 1) -> Vector:
    values = [0] * DIMENSION
    values[INDEX[(kind, degree)]] = coefficient % PRIME
    return tuple(values)


def add(*vectors: Vector) -> Vector:
    return tuple(
        sum(vector[index] for vector in vectors) % PRIME
        for index in range(DIMENSION)
    )


def scale(coefficient: int, vector: Vector) -> Vector:
    return tuple(coefficient * value % PRIME for value in vector)


def basis_product(left: tuple[str, int], right: tuple[str, int]):
    left_kind, left_degree = left
    right_kind, right_degree = right
    total_degree = left_degree + right_degree
    if left_kind == "B":
        return None
    if right_kind == "A":
        if total_degree <= 5:
            return ("A", total_degree)
        return None
    if total_degree <= 6:
        return ("B", total_degree)
    return None


def multiply(left: Vector, right: Vector) -> Vector:
    result = [0] * DIMENSION
    for left_index, left_value in enumerate(left):
        if not left_value:
            continue
        for right_index, right_value in enumerate(right):
            if not right_value:
                continue
            target = basis_product(BASIS[left_index], BASIS[right_index])
            if target is not None:
                result[INDEX[target]] += left_value * right_value
    return tuple(value % PRIME for value in result)


def cube(vector: Vector) -> Vector:
    return multiply(multiply(vector, vector), vector)


def circle(left: Vector, right: Vector) -> Vector:
    """Multiplication in 1+J, with the leading 1 suppressed."""

    return add(left, right, multiply(left, right))


def all_vectors():
    yield from product(range(PRIME), repeat=DIMENSION)


def verify_basis_associativity() -> None:
    unit_vectors = [
        basis_vector(kind, degree) for kind, degree in BASIS
    ]
    for left in unit_vectors:
        for middle in unit_vectors:
            for right in unit_vectors:
                assert multiply(multiply(left, middle), right) == multiply(
                    left, multiply(middle, right)
                )


def filtration_profile() -> tuple[int, ...]:
    return tuple(
        sum(1 for _, basis_degree in BASIS if basis_degree == degree)
        for degree in range(1, 7)
    )


def build_audit() -> dict[str, object]:
    assert DIMENSION == 11
    assert filtration_profile() == (2, 2, 2, 2, 2, 1)
    verify_basis_associativity()

    raw_cubes = {cube(vector) for vector in all_vectors()}
    assert len(raw_cubes) == 171
    leading_fibres = Counter(
        (
            value[INDEX[("A", 3)]],
            value[INDEX[("B", 3)]],
        )
        for value in raw_cubes
    )
    assert leading_fibres[(0, 0)] == 9
    assert len(leading_fibres) == 7
    assert sorted(leading_fibres.values()) == [9] + [27] * 6

    a = basis_vector("A", 1)
    b = basis_vector("B", 1)
    u = cube(a)
    v = cube(add(a, b))
    top = basis_vector("B", 6)
    assert u == basis_vector("A", 3)
    assert v == add(basis_vector("A", 3), basis_vector("B", 3))
    assert add(multiply(u, v), scale(-1, multiply(v, u))) == top

    minus_u = cube(scale(-1, a))
    missing_product = circle(v, minus_u)
    assert missing_product == basis_vector("B", 3)
    assert missing_product not in raw_cubes

    zero_leading = {
        value
        for value in raw_cubes
        if value[INDEX[("A", 3)]] == 0
    }
    expected_zero_leading = {
        add(
            scale(left, basis_vector("B", 5)),
            scale(right, basis_vector("B", 6)),
        )
        for left in range(PRIME)
        for right in range(PRIME)
    }
    assert zero_leading == expected_zero_leading

    return {
        "schema": "amra.kou21137.dim11-sharp-noncommuting-cubes.v1",
        "field": "F_3",
        "dimension": DIMENSION,
        "filtration_profile": list(filtration_profile()),
        "raw_cube_count": len(raw_cubes),
        "zero_A3_cube_count": len(zero_leading),
        "leading_A3_image_size": len(leading_fibres),
        "leading_A3_fibre_sizes": sorted(leading_fibres.values()),
        "noncommuting_cube_commutator": "B_6",
        "missing_circle_product": "B_3",
        "raw_cube_set_closed": False,
        "wilson_counterexample": False,
    }


def main() -> None:
    audit = build_audit()
    print(
        "DIM11_SHARP_WITNESS"
        f"|dimension={audit['dimension']}"
        "|profile=2,2,2,2,2,1"
        f"|raw_cubes={audit['raw_cube_count']}"
        "|commutator=B6"
        "|missing_circle=B3"
        "|closed=false"
        "|wilson=false"
    )
    print("DONE")


if __name__ == "__main__":
    main()
