#!/usr/bin/env python3
"""Exact graded front-end for the dim-12 profile (2,3,2,2,1,1,1).

The audit enumerates every required low-degree relation subspace and
all 13 projective directions in A2 for ad_w^2(V)=0.  It is a necessary
associated-graded certificate, not a filtered algebra construction.
"""

from __future__ import annotations

import hashlib
import itertools

from audit_dim11_q2_graded_frontend import (
    complement,
    row_basis,
    tensor,
    vector_sum,
)


PRIME = 3
V_BASIS = ([1, 0], [0, 1])
V_PROJECTIVE = ((1, 0), (0, 1), (1, 1), (1, 2))


def grassmannian_subspaces(
    dimension: int, ambient_dimension: int
):
    """Yield all RREF subspaces in deterministic pivot/value order."""

    for pivots in itertools.combinations(
        range(ambient_dimension), dimension
    ):
        slots = [
            (row_index, column)
            for row_index, pivot in enumerate(pivots)
            for column in range(pivot + 1, ambient_dimension)
            if column not in pivots
        ]
        for values in itertools.product(
            range(PRIME), repeat=len(slots)
        ):
            rows = [
                [0] * ambient_dimension for _ in range(dimension)
            ]
            for row_index, pivot in enumerate(pivots):
                rows[row_index][pivot] = 1
            for (row_index, column), value in zip(slots, values):
                rows[row_index][column] = value
            yield rows


def propagate(relations: list[list[int]]) -> list[list[int]]:
    return row_basis(
        [
            tensor(list(vector), relation)
            for vector in V_BASIS
            for relation in relations
        ]
        + [
            tensor(relation, list(vector))
            for relation in relations
            for vector in V_BASIS
        ],
        2 * len(relations[0]),
    )


def add_quotient_relations(
    base_relations: list[list[int]],
    ambient_dimension: int,
    target_dimension: int,
):
    """Yield every ideal extension with the requested quotient dimension."""

    quotient_dimension = ambient_dimension - len(base_relations)
    added_dimension = quotient_dimension - target_dimension
    if added_dimension < 0:
        return
    quotient_basis = complement(
        base_relations, ambient_dimension, quotient_dimension
    )
    for extension_index, subspace in enumerate(
        grassmannian_subspaces(added_dimension, quotient_dimension)
    ):
        added_relations = [
            [
                sum(
                    coefficient * basis_vector[column]
                    for coefficient, basis_vector in zip(
                        row, quotient_basis
                    )
                )
                % PRIME
                for column in range(ambient_dimension)
            ]
            for row in subspace
        ]
        yield extension_index, row_basis(
            base_relations + added_relations, ambient_dimension
        )


def quotient_rank(
    vectors: list[list[int]], relations: list[list[int]]
) -> int:
    columns = len(vectors[0])
    return len(row_basis(relations + vectors, columns)) - len(
        relations
    )


def image_size(
    vectors: list[list[int]], relations: list[list[int]]
) -> int:
    representatives: list[list[int]] = []
    for vector in vectors:
        if not any(
            quotient_rank(
                [[
                    (left - right) % PRIME
                    for left, right in zip(vector, prior)
                ]],
                relations,
            )
            == 0
            for prior in representatives
        ):
            representatives.append(vector)
    return len(representatives)


def leading_a1_cube_signature(
    cubic_relations: list[list[int]],
) -> tuple[int, int]:
    cubes = [
        tensor(tensor([x, y], [x, y]), [x, y])
        for x in range(PRIME)
        for y in range(PRIME)
    ]
    return (
        quotient_rank(cubes, cubic_relations),
        image_size(cubes, cubic_relations),
    )


def all_a2_points(a2_basis: list[list[int]]) -> list[list[int]]:
    return [
        [
            sum(
                coefficient * basis_vector[column]
                for coefficient, basis_vector in zip(
                    (first, second, third), a2_basis
                )
            )
            % PRIME
            for column in range(4)
        ]
        for first in range(PRIME)
        for second in range(PRIME)
        for third in range(PRIME)
    ]


def main() -> int:
    quadratic_lines = list(grassmannian_subspaces(1, 4))
    a2_projective = list(grassmannian_subspaces(1, 3))
    assert len(quadratic_lines) == 40
    assert len(a2_projective) == 13

    degree4_cases: list[
        tuple[int, int, list[list[int]], list[list[int]]]
    ] = []
    for quadratic_index, quadratic_relations in enumerate(
        quadratic_lines
    ):
        a2_basis = complement(quadratic_relations, 4, 3)
        base_cubic_relations = propagate(quadratic_relations)
        for cubic_index, cubic_relations in add_quotient_relations(
            base_cubic_relations, 8, 2
        ):
            if leading_a1_cube_signature(cubic_relations) != (2, 9):
                continue

            degree4_identities: list[list[int]] = []
            for value in V_PROJECTIVE:
                value_vector = list(value)
                for direction in a2_basis:
                    degree4_identities.append(
                        vector_sum(
                            tensor(
                                tensor(value_vector, value_vector),
                                direction,
                            ),
                            tensor(
                                tensor(value_vector, direction),
                                value_vector,
                            ),
                            tensor(
                                tensor(direction, value_vector),
                                value_vector,
                            ),
                        )
                    )
            degree4_relations = row_basis(
                propagate(cubic_relations) + degree4_identities,
                16,
            )
            if 16 - len(degree4_relations) != 2:
                continue
            degree4_cases.append((
                quadratic_index,
                cubic_index,
                a2_basis,
                degree4_relations,
            ))
    assert len(degree4_cases) == 36

    outcome_counts: dict[tuple[int, int, int], int] = {}
    surviving_ids: list[str] = []
    degree5_extensions = 0
    for (
        quadratic_index,
        cubic_index,
        a2_basis,
        degree4_relations,
    ) in degree4_cases:
        degree5_identities: list[list[int]] = []
        for projective_row in a2_projective:
            coefficients = projective_row[0]
            direction = [
                sum(
                    coefficient * basis_vector[column]
                    for coefficient, basis_vector in zip(
                        coefficients, a2_basis
                    )
                )
                % PRIME
                for column in range(4)
            ]
            for value in V_BASIS:
                value_vector = list(value)
                degree5_identities.append(
                    vector_sum(
                        tensor(tensor(direction, direction), value_vector),
                        tensor(tensor(direction, value_vector), direction),
                        tensor(tensor(value_vector, direction), direction),
                    )
                )
        base_degree5_relations = row_basis(
            propagate(degree4_relations) + degree5_identities,
            32,
        )
        assert 32 - len(base_degree5_relations) == 2

        for degree5_index, degree5_relations in add_quotient_relations(
            base_degree5_relations, 32, 1
        ):
            degree5_extensions += 1
            degree6_relations = propagate(degree5_relations)
            degree7_relations = propagate(degree6_relations)
            d6 = 64 - len(degree6_relations)
            d7 = 128 - len(degree7_relations)

            a2_cubes = [
                tensor(tensor(point, point), point)
                for point in all_a2_points(a2_basis)
            ]
            cube_image_size = image_size(
                a2_cubes, degree6_relations
            )
            outcome = (d6, d7, cube_image_size)
            outcome_counts[outcome] = (
                outcome_counts.get(outcome, 0) + 1
            )
            if outcome == (1, 1, 3):
                surviving_ids.append(
                    f"{quadratic_index}:{cubic_index}:{degree5_index}"
                )

    assert degree5_extensions == 144
    assert outcome_counts == {
        (0, 0, 1): 96,
        (1, 1, 3): 48,
    }
    assert len(surviving_ids) == 48
    case_text = ",".join(surviving_ids)
    digest = hashlib.sha256(case_text.encode("ascii")).hexdigest()
    print(
        "DIM12_2322111_GRADED_FRONTEND"
        "|field=F3"
        "|quadratic_relation_lines=40"
        "|A2_projective_directions=13"
        "|degree4_frontends=36"
        "|degree5_projective_extensions=144"
        "|collapsed_d6_d7_image1=96"
        "|target_d6_d7_image3=48"
        f"|target_case_sha256={digest}"
        "|filtered_lift_checked=false"
        "|full_raw_closure_checked=false"
        "|status=necessary_graded_cases_only"
    )
    print(f"DIM12_2322111_TARGET_CASES|cases={case_text}")
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
