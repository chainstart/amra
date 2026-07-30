#!/usr/bin/env python3
"""Exact 130-plane graded front-end for the remaining Q-dimension-two branch."""

from __future__ import annotations

import hashlib

from audit_quadratic_relation_d3_bound import relation_planes


PRIME = 3
V_BASIS = ([1, 0], [0, 1])
PROJECTIVE_LINES = ((1, 0), (0, 1), (1, 1), (1, 2))
COMMUTATOR = [0, 1, 2, 0]


def row_basis(rows: list[list[int]], columns: int) -> list[list[int]]:
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
        if output == len(matrix):
            break
    return matrix[:output]


def tensor(left: list[int], right: list[int]) -> list[int]:
    return [
        left_value * right_value % PRIME
        for left_value in left
        for right_value in right
    ]


def vector_sum(*vectors: list[int]) -> list[int]:
    return [
        sum(coordinates) % PRIME for coordinates in zip(*vectors)
    ]


def propagate(relations: list[list[int]]) -> list[list[int]]:
    return row_basis(
        [
            tensor(vector, relation)
            for vector in V_BASIS
            for relation in relations
        ]
        + [
            tensor(relation, vector)
            for relation in relations
            for vector in V_BASIS
        ],
        2 * len(relations[0]),
    )


def complement(
    relations: list[list[int]], ambient_dimension: int, dimension: int
) -> list[list[int]]:
    rows = row_basis(relations, ambient_dimension)
    output: list[list[int]] = []
    for coordinate in range(ambient_dimension):
        vector = [
            1 if index == coordinate else 0
            for index in range(ambient_dimension)
        ]
        enlarged = row_basis(rows + [vector], ambient_dimension)
        if len(enlarged) > len(rows):
            output.append(vector)
            rows = enlarged
        if len(output) == dimension:
            return output
    raise RuntimeError("failed to construct quotient complement")


def linear_combination(
    coefficients: tuple[int, int], vectors: list[list[int]]
) -> list[int]:
    return [
        sum(
            coefficient * vector[index]
            for coefficient, vector in zip(coefficients, vectors)
        )
        % PRIME
        for index in range(len(vectors[0]))
    ]


def universal_relations(
    plane: tuple[tuple[int, ...], ...],
    extra_degree_five: list[int] | None = None,
) -> tuple[tuple[int, ...], dict[int, list[list[int]]]]:
    ideals: dict[int, list[list[int]]] = {
        2: row_basis([list(row) for row in plane], 4)
    }
    degree_two_basis = complement(ideals[2], 4, 2)
    ideals[3] = propagate(ideals[2])

    degree_four_identities: list[list[int]] = []
    for value in PROJECTIVE_LINES:
        value_vector = list(value)
        for direction in degree_two_basis:
            degree_four_identities.append(
                vector_sum(
                    tensor(tensor(value_vector, value_vector), direction),
                    tensor(tensor(value_vector, direction), value_vector),
                    tensor(tensor(direction, value_vector), value_vector),
                )
            )
    ideals[4] = row_basis(
        propagate(ideals[3]) + degree_four_identities, 16
    )

    degree_five_identities: list[list[int]] = []
    for coefficients in PROJECTIVE_LINES:
        direction = linear_combination(
            coefficients, degree_two_basis
        )
        for value in V_BASIS:
            degree_five_identities.append(
                vector_sum(
                    tensor(tensor(direction, direction), value),
                    tensor(tensor(direction, value), direction),
                    tensor(tensor(value, direction), direction),
                )
            )
    ideals[5] = row_basis(
        propagate(ideals[4]) + degree_five_identities, 32
    )
    if extra_degree_five is not None:
        ideals[5] = row_basis(
            ideals[5] + [extra_degree_five], 32
        )
    ideals[6] = propagate(ideals[5])
    ideals[7] = propagate(ideals[6])
    dimensions = tuple(
        2**degree - len(ideals[degree])
        for degree in range(2, 8)
    )
    return dimensions, ideals


def same_coset(
    left: list[int], right: list[int], relations: list[list[int]]
) -> bool:
    difference = [
        (left_value - right_value) % PRIME
        for left_value, right_value in zip(left, right)
    ]
    return len(row_basis(relations + [difference], 8)) == len(
        relations
    )


def leading_cube_image_size(relations: list[list[int]]) -> int:
    representatives: list[list[int]] = []
    for first in range(PRIME):
        for second in range(PRIME):
            value = [first, second]
            cube_word = tensor(tensor(value, value), value)
            if not any(
                same_coset(cube_word, prior, relations)
                for prior in representatives
            ):
                representatives.append(cube_word)
    return len(representatives)


def contains_commutator(
    plane: tuple[tuple[int, ...], ...],
) -> bool:
    rows = [list(row) for row in plane]
    return len(row_basis(rows + [COMMUTATOR], 4)) == len(
        row_basis(rows, 4)
    )


def commutative_quadratic_zero_lines(
    plane: tuple[tuple[int, ...], ...],
) -> int:
    """Count projective zeros of the relation modulo xy-yx."""

    relation = next(
        list(row)
        for row in plane
        if len(row_basis([COMMUTATOR, list(row)], 4)) == 2
    )
    return sum(
        (
            relation[0] * x * x
            + relation[1] * x * y
            + relation[2] * y * x
            + relation[3] * y * y
        )
        % PRIME
        == 0
        for x, y in PROJECTIVE_LINES
    )


def main() -> int:
    planes = relation_planes()
    universal_profile_counts: dict[tuple[int, ...], int] = {}
    q_bijective_planes = 0
    q_bijective_d4_one_planes = 0
    q_bijective_d4_two_planes = 0
    commutative_d4_two_planes = 0
    commutative_factor_types = {0: 0, 2: 0}
    full_tail_planes: list[
        tuple[int, tuple[tuple[int, ...], ...], dict[int, list[list[int]]]]
    ] = []
    for plane_index, plane in enumerate(planes):
        dimensions, ideals = universal_relations(plane)
        universal_profile_counts[dimensions] = (
            universal_profile_counts.get(dimensions, 0) + 1
        )
        if leading_cube_image_size(ideals[3]) == 9:
            q_bijective_planes += 1
            if dimensions[2] == 1:
                q_bijective_d4_one_planes += 1
            elif dimensions[2] == 2:
                q_bijective_d4_two_planes += 1
                assert contains_commutator(plane)
                commutative_d4_two_planes += 1
                zero_lines = commutative_quadratic_zero_lines(plane)
                assert zero_lines in commutative_factor_types
                commutative_factor_types[zero_lines] += 1
        if dimensions == (2, 2, 2, 2, 2, 2):
            full_tail_planes.append((plane_index, plane, ideals))
    assert q_bijective_planes == 12
    assert q_bijective_d4_one_planes == 3
    assert q_bijective_d4_two_planes == 9
    assert commutative_d4_two_planes == 9
    assert commutative_factor_types == {0: 3, 2: 6}
    assert len(full_tail_planes) == 13

    target_cases: list[tuple[int, int]] = []
    q_two_cases: list[tuple[int, int]] = []
    q_one_cases = 0
    collapsed_cases = 0
    for plane_index, plane, ideals in full_tail_planes:
        degree_five_basis = complement(ideals[5], 32, 2)
        for line_index, coefficients in enumerate(PROJECTIVE_LINES):
            relation = linear_combination(
                coefficients, degree_five_basis
            )
            dimensions, extended_ideals = universal_relations(
                plane, relation
            )
            if dimensions == (2, 2, 2, 1, 1, 1):
                target_cases.append((plane_index, line_index))
                image_size = leading_cube_image_size(
                    extended_ideals[3]
                )
                if image_size == 9:
                    q_two_cases.append((plane_index, line_index))
                elif image_size == 3:
                    q_one_cases += 1
                else:
                    raise AssertionError(image_size)
            elif dimensions == (2, 2, 2, 1, 0, 0):
                collapsed_cases += 1
            else:
                raise AssertionError(dimensions)
    assert len(target_cases) == 16
    assert len(q_two_cases) == 12
    assert q_one_cases == 4
    assert collapsed_cases == 36

    case_text = ",".join(
        f"{plane_index}:{line_index}"
        for plane_index, line_index in target_cases
    )
    digest = hashlib.sha256(case_text.encode("ascii")).hexdigest()
    q_two_text = ",".join(
        f"{plane_index}:{line_index}"
        for plane_index, line_index in q_two_cases
    )
    q_two_digest = hashlib.sha256(
        q_two_text.encode("ascii")
    ).hexdigest()
    print(
        "DIM11_Q2_GRADED_FRONTEND"
        "|field=F3"
        f"|quadratic_relation_planes={len(planes)}"
        f"|q_bijective_relation_planes={q_bijective_planes}"
        f"|q_bijective_d4_one_planes={q_bijective_d4_one_planes}"
        f"|q_bijective_d4_two_planes={q_bijective_d4_two_planes}"
        "|q_bijective_maximum_d4=2"
        f"|q_bijective_d4_two_commutative={commutative_d4_two_planes}"
        "|commutative_irreducible_quadratics=3"
        "|commutative_split_quadratics=6"
        f"|universal_full_tail_planes={len(full_tail_planes)}"
        "|degree5_projective_extensions=52"
        f"|target_profile_cases={len(target_cases)}"
        f"|Q2_target_cases={len(q_two_cases)}"
        f"|non_Q2_target_cases={q_one_cases}"
        f"|collapsed_A6_cases={collapsed_cases}"
        f"|target_case_sha256={digest}"
        f"|Q2_case_sha256={q_two_digest}"
    )
    print(f"DIM11_Q2_TARGET_CASES|cases={case_text}")
    print(f"DIM11_Q2_NINE_POINT_CASES|cases={q_two_text}")
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
