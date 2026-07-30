#!/usr/bin/env python3
"""Exponent and finite tensor checks for ruled-stability extraction.

The random objects below are incidence tensors, not Euclidean metrics.
They certify the stated limitation of tensor-only dyadic/DRC/BSG
arguments.
"""

from __future__ import annotations

import itertools
import json
import random
from fractions import Fraction


def dyadic_ledger(weight_exponent: Fraction) -> dict[str, Fraction]:
    """Critical exponents for a cell weight t^omega."""

    omega = Fraction(weight_exponent)
    if omega < 3 or omega > 4:
        raise ValueError("critical mass-carrying omega lies in [3,4]")
    return {
        "left_plane_pairs": Fraction(2),
        "distance_labels": Fraction(3),
        "cell_weight": omega,
        "support_edges": Fraction(8)-omega,
        "average_left_degree": Fraction(6)-omega,
        "average_right_degree": Fraction(5)-omega,
        "total_representation_mass": Fraction(8),
        "uniform_aggregate_energy": Fraction(13),
        "diagonal_energy": Fraction(8)+omega,
    }


def common_neighbour_exponent(
    weight_exponent: Fraction, left_vertices: int
) -> Fraction:
    """Random-support exponent for h common plane-pair neighbours."""

    omega = Fraction(weight_exponent)
    return Fraction(3)+left_vertices*(Fraction(3)-omega)


def endpoint_common_target_exponent(source_vertices: int) -> Fraction:
    """Random balanced-colour exponent inside one Q-by-Q cell."""

    return Fraction(3)-2*source_vertices


def random_support_model(q: int, seed: int = 1083) -> dict[str, int]:
    """One-scale plane-pair/distance support with exact left degrees."""

    if q < 3:
        raise ValueError("q must be at least three")
    generator = random.Random(seed)
    left_count = q*q
    right_count = q**3
    left_degree = q*q
    supports = [
        frozenset(generator.sample(range(right_count), left_degree))
        for _ in range(left_count)
    ]
    right_degrees = [0]*right_count
    for support in supports:
        for label in support:
            right_degrees[label] += 1

    weight = q**4
    total_mass = sum(len(support)*weight for support in supports)
    diagonal_energy = sum(
        len(support)*weight*weight for support in supports
    )
    aggregate_energy = sum(
        (degree*weight)**2 for degree in right_degrees
    )

    max_common = {}
    for size in (2, 3, 4):
        maximum = 0
        for chosen in itertools.combinations(supports, size):
            intersection = set(chosen[0])
            for support in chosen[1:]:
                intersection.intersection_update(support)
                if not intersection:
                    break
            maximum = max(maximum, len(intersection))
        max_common[size] = maximum

    assert total_mass == q**8
    assert diagonal_energy == q**12
    assert aggregate_energy >= q**13
    return {
        "q": q,
        "left_vertices": left_count,
        "right_vertices": right_count,
        "left_degree": left_degree,
        "support_edges": left_count*left_degree,
        "cell_weight": weight,
        "row_mass": left_degree*weight,
        "total_mass": total_mass,
        "aggregate_energy": aggregate_energy,
        "diagonal_energy": diagonal_energy,
        "cross_energy": aggregate_energy-diagonal_energy,
        "maximum_right_degree": max(right_degrees),
        "minimum_right_degree": min(right_degrees),
        "maximum_pair_common_labels": max_common[2],
        "maximum_triple_common_labels": max_common[3],
        "maximum_four_common_labels": max_common[4],
    }


def symmetric_plane_pair_support_model(
    q: int, seed: int = 1083
) -> dict[str, int]:
    """Support on unordered plane pairs, copied to reverse orientations."""

    if q < 4:
        raise ValueError("q must be at least four")
    generator = random.Random(seed)
    unordered_pairs = tuple(itertools.combinations(range(q), 2))
    right_count = q**3
    row_degree = q*q
    supports = {
        pair: frozenset(generator.sample(range(right_count), row_degree))
        for pair in unordered_pairs
    }
    oriented_right_degrees = [0]*right_count
    for support in supports.values():
        for label in support:
            oriented_right_degrees[label] += 2

    weight = q**4
    oriented_rows = 2*len(unordered_pairs)
    total_mass = oriented_rows*row_degree*weight
    diagonal_energy = oriented_rows*row_degree*weight*weight
    aggregate_energy = sum(
        (degree*weight)**2 for degree in oriented_right_degrees
    )
    cs_lower = total_mass*total_mass//right_count

    maximum_four_common = 0
    if len(unordered_pairs) >= 4:
        for chosen_pairs in itertools.combinations(unordered_pairs, 4):
            intersection = set(supports[chosen_pairs[0]])
            for pair in chosen_pairs[1:]:
                intersection.intersection_update(supports[pair])
                if not intersection:
                    break
            maximum_four_common = max(
                maximum_four_common, len(intersection)
            )

    assert aggregate_energy >= cs_lower
    return {
        "q": q,
        "unordered_plane_pairs": len(unordered_pairs),
        "oriented_rows": oriented_rows,
        "right_vertices": right_count,
        "row_degree": row_degree,
        "cell_weight": weight,
        "row_mass": row_degree*weight,
        "total_mass": total_mass,
        "aggregate_energy": aggregate_energy,
        "aggregate_cs_lower": cs_lower,
        "diagonal_energy": diagonal_energy,
        "cross_energy": aggregate_energy-diagonal_energy,
        "maximum_four_independent_common_labels": maximum_four_common,
    }


def random_balanced_endpoint_cell(
    q: int, seed: int = 1083
) -> dict[str, int]:
    """Partition Q^2 endpoint pairs into q^2 equal label classes."""

    if q < 3:
        raise ValueError("q must be at least three")
    generator = random.Random(seed)
    source_size = q**3
    label_count = q*q
    class_size = q**4
    pairs = [
        (left, right)
        for left in range(source_size)
        for right in range(source_size)
    ]
    generator.shuffle(pairs)

    maximum_codegree = 0
    maximum_source_degree = 0
    for label in range(label_count):
        chunk = pairs[label*class_size:(label+1)*class_size]
        neighbours = [set() for _ in range(source_size)]
        for left, right in chunk:
            neighbours[left].add(right)
        maximum_source_degree = max(
            maximum_source_degree,
            max(map(len, neighbours)),
        )
        for left, other in itertools.combinations(range(source_size), 2):
            maximum_codegree = max(
                maximum_codegree,
                len(neighbours[left].intersection(neighbours[other])),
            )

    assert label_count*class_size == source_size**2
    return {
        "q": q,
        "endpoint_side_Q": source_size,
        "labels_in_plane_pair": label_count,
        "pairs_per_label": class_size,
        "maximum_one_source_degree": maximum_source_degree,
        "maximum_two_source_codegree": maximum_codegree,
    }


def split_rotation_ledger(q: int) -> dict[str, int]:
    """Exact source/rotation marginal ledger of the split reservoir."""

    if q < 3:
        raise ValueError("q must be at least three")
    active_angles = q
    source_per_angle = q**3
    fibre_size = q*q
    reservoir_fibres = q*q*(q-1)
    rotation_counts = [
        reservoir_fibres*(fibre_size-2*index)
        for index in range(1, active_angles+1)
    ]
    normalized_rotation_codegree_numerator = (
        reservoir_fibres
        * sum(fibre_size-2*index for index in range(1, q+1))**2
    )
    normalized_rotation_codegree = (
        normalized_rotation_codegree_numerator//fibre_size
    )
    return {
        "N": q**5,
        "active_angles": active_angles,
        "source_per_angle": source_per_angle,
        "source_mass": active_angles*source_per_angle,
        "reservoir_fibres": reservoir_fibres,
        "fibre_size": fibre_size,
        "reservoir_mass": reservoir_fibres*fibre_size,
        "total_mass": (
            active_angles*source_per_angle
            + reservoir_fibres*fibre_size
        ),
        "minimum_rotation_count": min(rotation_counts),
        "normalized_rotation_codegree": normalized_rotation_codegree,
    }


def audit() -> dict[str, object]:
    ledger = dyadic_ledger(Fraction(4))
    support = random_support_model(5)
    symmetric_support = symmetric_plane_pair_support_model(7)
    endpoint = random_balanced_endpoint_cell(5)
    rotation = split_rotation_ledger(5)
    assert ledger["uniform_aggregate_energy"] == 13
    assert ledger["diagonal_energy"] == 12
    assert common_neighbour_exponent(4, 2) == 1
    assert common_neighbour_exponent(4, 3) == 0
    assert common_neighbour_exponent(4, 4) == -1
    assert endpoint_common_target_exponent(1) == 1
    assert endpoint_common_target_exponent(2) == -1
    assert rotation["total_mass"] == rotation["N"]
    return {
        "schema": "amra.erdos1083.ruled-stability-extraction.v1",
        "status": "TENSOR_LEVEL_NO_GO",
        "euclidean_counterexample": False,
        "weight_t_power": str(ledger["cell_weight"]),
        "aggregate_energy_t_power": str(
            ledger["uniform_aggregate_energy"]
        ),
        "diagonal_energy_t_power": str(ledger["diagonal_energy"]),
        "random_model_maximum_four_common_labels": (
            support["maximum_four_common_labels"]
        ),
        "symmetric_model_maximum_four_common_labels": (
            symmetric_support[
                "maximum_four_independent_common_labels"
            ]
        ),
        "random_endpoint_maximum_two_source_codegree": (
            endpoint["maximum_two_source_codegree"]
        ),
        "rotation_total_mass": rotation["total_mass"],
        "rotation_normalized_codegree": (
            rotation["normalized_rotation_codegree"]
        ),
        "missing_input": (
            "Euclidean coefficient alignment for the four-plane "
            "quadratic, beyond the R_(alpha,beta)(d) tensor."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
