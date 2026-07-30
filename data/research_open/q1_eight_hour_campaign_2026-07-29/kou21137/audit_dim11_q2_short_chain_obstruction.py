#!/usr/bin/env python3
"""Exact graded certificate for the short-chain obstruction in dim(Q)=2.

For every surviving nine-point-image quadratic/front-end case, find a
basis (long, short) whose mixed quadratic products vanish, whose short
fifth power is the extra degree-five relation, and whose long-sixth
power annihilates the short generator in degree seven.
"""

from __future__ import annotations

import hashlib
import itertools

from audit_dim11_q2_graded_frontend import (
    PROJECTIVE_LINES,
    complement,
    leading_cube_image_size,
    linear_combination,
    row_basis,
    tensor,
    universal_relations,
)
from audit_quadratic_relation_d3_bound import relation_planes


PRIME = 3


def power_word(vector: tuple[int, int], degree: int) -> list[int]:
    result = list(vector)
    for _ in range(1, degree):
        result = tensor(result, list(vector))
    return result


def is_zero(vector: list[int], relations: list[list[int]]) -> bool:
    columns = len(vector)
    return len(row_basis(relations + [vector], columns)) == len(
        row_basis(relations, columns)
    )


def quotient_rank(
    vectors: list[list[int]], relations: list[list[int]]
) -> int:
    columns = len(vectors[0])
    return len(row_basis(relations + vectors, columns)) - len(
        row_basis(relations, columns)
    )


def ordered_bases() -> list[tuple[tuple[int, int], tuple[int, int]]]:
    nonzero = [
        vector
        for vector in itertools.product(range(PRIME), repeat=2)
        if vector != (0, 0)
    ]
    return [
        (first, second)
        for first in nonzero
        for second in nonzero
        if (first[0] * second[1] - first[1] * second[0]) % PRIME
    ]


def cross_chain_witnesses(
    ideals: dict[int, list[list[int]]],
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    witnesses = []
    for long, short in ordered_bases():
        long_word = list(long)
        short_word = list(short)
        if not is_zero(tensor(long_word, short_word), ideals[2]):
            continue
        if not is_zero(tensor(short_word, long_word), ideals[2]):
            continue
        if quotient_rank(
            [power_word(long, 2), power_word(short, 2)], ideals[2]
        ) != 2:
            continue
        if is_zero(power_word(long, 5), ideals[5]):
            continue
        if not is_zero(power_word(short, 5), ideals[5]):
            continue
        if is_zero(power_word(long, 6), ideals[6]):
            continue
        if not is_zero(
            tensor(power_word(long, 6), short_word), ideals[7]
        ):
            continue
        witnesses.append((long, short))
    return witnesses


def main() -> int:
    planes = relation_planes()
    q_two_cases: list[tuple[int, int]] = []
    certificate_rows: list[str] = []
    plane_indices: set[int] = set()

    for plane_index, plane in enumerate(planes):
        dimensions, ideals = universal_relations(plane)
        if dimensions != (2, 2, 2, 2, 2, 2):
            continue
        degree_five_basis = complement(ideals[5], 32, 2)
        for line_index, coefficients in enumerate(PROJECTIVE_LINES):
            relation = linear_combination(
                coefficients, degree_five_basis
            )
            extended_dimensions, extended_ideals = universal_relations(
                plane, relation
            )
            if extended_dimensions != (2, 2, 2, 1, 1, 1):
                continue
            if leading_cube_image_size(extended_ideals[3]) != 9:
                continue
            q_two_cases.append((plane_index, line_index))
            witnesses = cross_chain_witnesses(extended_ideals)
            assert witnesses
            long, short = witnesses[0]
            plane_indices.add(plane_index)
            certificate_rows.append(
                f"{plane_index}:{line_index}:"
                f"{long[0]}{long[1]}>{short[0]}{short[1]}"
            )

    assert len(q_two_cases) == 12
    assert len(plane_indices) == 6
    assert all(
        sum(
            1
            for case_plane, _ in q_two_cases
            if case_plane == plane_index
        )
        == 2
        for plane_index in plane_indices
    )

    certificate_text = ",".join(certificate_rows)
    digest = hashlib.sha256(
        certificate_text.encode("ascii")
    ).hexdigest()
    print(
        "DIM11_Q2_SHORT_CHAIN_AUDIT"
        "|field=F3"
        "|nine_point_frontend_cases=12"
        "|quadratic_planes=6"
        "|extensions_per_plane=2"
        "|mixed_quadratic_products_zero=12"
        "|short_square_nonzero=12"
        "|short_fifth_zero_in_A5=12"
        "|long_sixth_nonzero_in_A6=12"
        "|long_sixth_times_short_zero_in_A7=12"
        f"|certificate_sha256={digest}"
    )
    print(f"DIM11_Q2_SHORT_CHAIN_CASES|cases={certificate_text}")
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
