#!/usr/bin/env python3
"""Exact, solver-free certificate for a false structural route in #963.

The proposed strengthening said that every finite integer set P of
dissociation dimension r is contained in an affine Boolean r-cube.  This
script verifies that

    P = {1,6,7,8,13,14,20,21,27,34,35}

has dissociation dimension four but is not contained in any affine image of
{0,1}^4 over Q (and hence not over R).

The non-containment check is finite and exact.  An eleven-point containment
chooses eleven distinct vertices of the four-cube.  Up to coordinate
permutations and coordinate complements there are 27 such subsets.  For each
orbit representative we choose an affine basis of five vertices and try all
11P5 assignments of distinct values of P to that basis.  The remaining six
values are forced by rational affine interpolation.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction


P = (1, 6, 7, 8, 13, 14, 20, 21, 27, 34, 35)
VERTICES = tuple(range(16))


def bits(v: int) -> tuple[int, ...]:
    return tuple((v >> i) & 1 for i in range(4))


def subset_sums(values: tuple[int, ...]) -> dict[int, int]:
    answer: dict[int, int] = {}
    for mask in range(1 << len(values)):
        total = sum(value for i, value in enumerate(values) if mask >> i & 1)
        answer.setdefault(total, mask)
    return answer


def dissociated(values: tuple[int, ...]) -> bool:
    return len(subset_sums(values)) == 1 << len(values)


def first_collision(values: tuple[int, ...]) -> tuple[int, int]:
    seen: dict[int, int] = {}
    for mask in range(1 << len(values)):
        total = sum(value for i, value in enumerate(values) if mask >> i & 1)
        if total in seen:
            return seen[total], mask
        seen[total] = mask
    raise AssertionError("the tuple is dissociated")


def transform(v: int, permutation: tuple[int, ...], complement: int) -> int:
    result = 0
    for target_coordinate in range(4):
        bit = ((v >> permutation[target_coordinate]) & 1) ^ (
            (complement >> target_coordinate) & 1
        )
        result |= bit << target_coordinate
    return result


def orbit_representatives() -> tuple[list[tuple[int, ...]], int]:
    unseen = set(itertools.combinations(VERTICES, len(P)))
    representatives: list[tuple[int, ...]] = []
    covered = 0
    permutations = tuple(itertools.permutations(range(4)))
    while unseen:
        representative = min(unseen)
        orbit = {
            tuple(sorted(transform(v, permutation, complement) for v in representative))
            for permutation in permutations
            for complement in range(16)
        }
        removed = unseen.intersection(orbit)
        covered += len(removed)
        unseen.difference_update(removed)
        representatives.append(representative)
    return representatives, covered


def matrix_inverse(matrix: list[list[Fraction]]) -> list[list[Fraction]] | None:
    n = len(matrix)
    augmented = [
        row[:] + [Fraction(i == j) for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    for column in range(n):
        pivot = next((row for row in range(column, n)
                      if augmented[row][column]), None)
        if pivot is None:
            return None
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [entry / scale for entry in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [a - scale * b for a, b in
                                  zip(augmented[row], augmented[column])]
    return [row[n:] for row in augmented]


def affine_row(v: int) -> list[Fraction]:
    return [Fraction(1), *(Fraction(bit) for bit in bits(v))]


def interpolation_weights(vertices: tuple[int, ...]) -> tuple[
        tuple[int, ...], dict[int, tuple[Fraction, ...]]]:
    for basis in itertools.combinations(vertices, 5):
        inverse = matrix_inverse([affine_row(v) for v in basis])
        if inverse is None:
            continue
        weights: dict[int, tuple[Fraction, ...]] = {}
        for v in vertices:
            row = affine_row(v)
            # If M has basis rows, the vector of basis values is M*a.
            # Thus f(v)=row*M^{-1}*values.
            weights[v] = tuple(
                sum(row[k] * inverse[k][j] for k in range(5))
                for j in range(5)
            )
        return basis, weights
    raise AssertionError("eleven vertices of Q_4 must affinely span Q^4")


def main() -> None:
    dissociated_bases = [values for values in itertools.combinations(P, 4)
                         if dissociated(values)]
    assert dissociated_bases
    five_collisions = {
        values: first_collision(values)
        for values in itertools.combinations(P, 5)
    }
    assert len(five_collisions) == 462

    representatives, covered = orbit_representatives()
    assert covered == 4368 == len(tuple(itertools.combinations(VERTICES, len(P))))
    assert len(representatives) == 27

    assignments_checked = 0
    containment_witness = None
    representative_digest = hashlib.sha256(
        json.dumps(representatives, separators=(",", ":")).encode()
    ).hexdigest()
    collision_digest = hashlib.sha256(
        json.dumps([
            [values, masks]
            for values, masks in sorted(five_collisions.items())
        ], separators=(",", ":")).encode()
    ).hexdigest()

    for representative in representatives:
        basis, weights = interpolation_weights(representative)
        for assigned in itertools.permutations(P, 5):
            assignments_checked += 1
            image = tuple(
                sum(weight * value for weight, value in zip(weights[v], assigned))
                for v in representative
            )
            if len(set(image)) == len(P) and set(image) == set(map(Fraction, P)):
                containment_witness = {
                    "vertices": representative,
                    "basis": basis,
                    "assigned_basis_values": assigned,
                    "image": [str(value) for value in image],
                }
                break
        if containment_witness is not None:
            break

    expected_assignments = len(representatives) * 11 * 10 * 9 * 8 * 7
    assert assignments_checked == expected_assignments
    assert containment_witness is None
    result = {
        "status": "PASS",
        "set": P,
        "dissociation_dimension": 4,
        "sample_dissociated_four_set": dissociated_bases[0],
        "five_subsets_with_explicit_collision": len(five_collisions),
        "five_collision_certificate_sha256": collision_digest,
        "cube_vertex_subsets": 4368,
        "cube_symmetry_orbits": len(representatives),
        "orbit_representatives_sha256": representative_digest,
        "ordered_affine_basis_assignments_checked": assignments_checked,
        "affine_four_cube_containment": False,
        "arithmetic": "fractions.Fraction exact rational arithmetic",
        "scope": "finite certificate refuting the affine-cube strengthening; not #963",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
