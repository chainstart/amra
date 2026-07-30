#!/usr/bin/env python3
"""Exact quadratic audit excluding the dim(Q)=1 branch in profile 2222111.

The computation is only a finite certificate for the relation-plane
classification used by the accompanying human proof.  It does not
enumerate filtered associative algebras or impose raw-cube closure.
"""

from __future__ import annotations

import hashlib

from audit_quadratic_relation_d3_bound import (
    PRIME,
    rank,
    relation_planes,
    tensor_relation_rows,
)


PROJECTIVE_LINES = ((1, 0), (0, 1), (1, 1), (1, 2))
COMMUTATOR = [0, 1, 2, 0]  # xy-yx in the order xx,xy,yx,yy.


def tensor(left: list[int], right: list[int]) -> list[int]:
    return [
        left_value * right_value % PRIME
        for left_value in left
        for right_value in right
    ]


def propagate(rows: list[list[int]]) -> list[list[int]]:
    """Generate V I + I V in the next tensor degree."""

    unit_vectors = ([1, 0], [0, 1])
    return (
        [tensor(list(vector), row) for vector in unit_vectors for row in rows]
        + [tensor(row, list(vector)) for row in rows for vector in unit_vectors]
    )


def quotient_rank(vectors: list[list[int]], relations: list[list[int]]) -> int:
    columns = len(vectors[0]) if vectors else len(relations[0])
    return rank(relations + vectors, columns) - rank(relations, columns)


def cube_word(value: tuple[int, int]) -> list[int]:
    vector = list(value)
    return tensor(tensor(vector, vector), vector)


def q_signature(
    cubic_relations: list[list[int]],
) -> tuple[int, int, int]:
    cubes = [cube_word(value) for value in PROJECTIVE_LINES]
    span_dimension = quotient_rank(cubes, cubic_relations)
    zero_lines = sum(
        quotient_rank([cube], cubic_relations) == 0 for cube in cubes
    )

    representatives: list[list[int]] = [[0] * 8]
    for first in range(PRIME):
        for second in range(PRIME):
            cube = cube_word((first, second))
            if not any(
                quotient_rank(
                    [[(left - right) % PRIME for left, right in zip(cube, old)]],
                    cubic_relations,
                )
                == 0
                for old in representatives
            ):
                representatives.append(cube)
    return span_dimension, zero_lines, len(representatives)


def main() -> int:
    planes = relation_planes()
    assert len(planes) == 130

    distribution: dict[tuple[int, int], int] = {}
    q_one_planes: list[tuple[int, tuple[tuple[int, ...], ...]]] = []
    d3_two_count = 0
    for plane_index, plane in enumerate(planes):
        cubic_relations = tensor_relation_rows(plane)
        d3 = 8 - rank(cubic_relations, 8)
        if d3 != 2:
            continue
        d3_two_count += 1
        span_dimension, zero_lines, image_size = q_signature(
            cubic_relations
        )
        distribution[(span_dimension, zero_lines)] = (
            distribution.get((span_dimension, zero_lines), 0) + 1
        )
        if span_dimension == 1:
            assert zero_lines == 1
            assert image_size == 3
            q_one_planes.append((plane_index, plane))

    assert d3_two_count == 34
    assert distribution == {
        (1, 1): 4,
        (2, 0): 12,
        (2, 1): 12,
        (2, 2): 6,
    }
    assert len(q_one_planes) == 4

    universal_dimensions: set[tuple[int, ...]] = set()
    for _, plane in q_one_planes:
        quadratic_rows = [list(row) for row in plane]
        assert rank(quadratic_rows + [COMMUTATOR], 4) == 2
        relations = quadratic_rows
        dimensions = [4 - rank(relations, 4)]
        for degree in range(3, 8):
            relations = propagate(relations)
            dimensions.append(2**degree - rank(relations, 2**degree))
        universal_dimensions.add(tuple(dimensions))
    assert universal_dimensions == {(2, 2, 2, 2, 2, 2)}

    case_text = ";".join(
        f"{index}:" + ",".join("".join(map(str, row)) for row in plane)
        for index, plane in q_one_planes
    )
    digest = hashlib.sha256(case_text.encode("ascii")).hexdigest()
    print(
        "DIM11_Q1_QUADRATIC_AUDIT"
        "|field=F3"
        f"|quadratic_relation_planes={len(planes)}"
        f"|d3_two_planes={d3_two_count}"
        "|qdim1_zero_lines1=4"
        "|qdim2_zero_lines0=12"
        "|qdim2_zero_lines1=12"
        "|qdim2_zero_lines2=6"
        "|qdim1_image_size=3"
        "|qdim1_contains_xy_minus_yx=4"
        "|qdim1_universal_dimensions_d2_to_d7=2,2,2,2,2,2"
        f"|qdim1_case_sha256={digest}"
    )
    print(f"DIM11_Q1_RELATION_PLANES|cases={case_text}")
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
