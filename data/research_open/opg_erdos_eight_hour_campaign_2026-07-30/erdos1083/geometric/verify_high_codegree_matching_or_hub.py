#!/usr/bin/env python3
"""Exact verifier for the high-codegree matching-or-hub theorem.

The finite-field construction is an abstract incidence tensor, not a
Euclidean metric.
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction


def maximum_matching_size(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
) -> int:
    """Brute-force matching size for the tiny exhaustive certificate."""

    maximum = 0
    for size in range(1, len(edges) + 1):
        for chosen in itertools.combinations(edges, size):
            endpoints = tuple(
                endpoint for edge in chosen for endpoint in edge
            )
            if len(set(endpoints)) == 2 * size:
                maximum = max(maximum, size)
    return maximum


def exhaustive_weighted_extraction_check() -> int:
    """Check the finite weighted lemma on every 4-vertex 0..3 weighting."""

    vertices = 4
    target_matching = 2
    edges = tuple(itertools.combinations(range(vertices), 2))
    checked = 0
    for weights in itertools.product(range(4), repeat=len(edges)):
        total = sum(weights)
        if total == 0:
            continue
        threshold = Fraction(total, 4 * vertices * vertices)
        rich_edges = tuple(
            edge
            for edge, weight in zip(edges, weights)
            if weight >= threshold
        )
        if maximum_matching_size(vertices, rich_edges) >= target_matching:
            checked += 1
            continue
        rich_degrees = [0] * vertices
        for (left, right), weight in zip(edges, weights):
            if weight >= threshold:
                rich_degrees[left] += weight
                rich_degrees[right] += weight
        if max(rich_degrees) < Fraction(
            3 * total, 8 * target_matching
        ):
            raise AssertionError("weighted matching-or-hub lemma failed")
        checked += 1
    return checked


def critical_exponent_ledger(
    label_mass_exponent: Fraction,
    matching_exponent: Fraction = Fraction(1, 2),
):
    """Return the dyadic and dichotomy exponents at scale lambda."""

    lam = Fraction(label_mass_exponent)
    kappa = Fraction(matching_exponent)
    if lam < 5 or lam > 6:
        raise ValueError("lambda must lie in [5,6]")
    if kappa <= 0 or kappa >= 1:
        raise ValueError("kappa must lie in (0,1)")
    label_count = Fraction(13) - 2 * lam
    rich_cell = lam - 2
    automatic_matching = lam - 5
    hub_mass = lam - kappa
    hub_label_count = label_count - 1
    return {
        "lambda": lam,
        "kappa": kappa,
        "label_count": label_count,
        "rich_cell": rich_cell,
        "automatic_matching": automatic_matching,
        "hub_mass": hub_mass,
        "hub_label_count": hub_label_count,
    }


def polynomial_value(
    coefficients: tuple[int, int, int],
    value: int,
    prime: int,
) -> int:
    a, b, c = coefficients
    return (a * value * value + b * value + c) % prime


def finite_field_tensor(prime: int) -> dict[str, int]:
    """Build the quadratic-evaluation support tensor over F_prime."""

    if (
        prime < 3
        or any(
            prime % divisor == 0
            for divisor in range(2, int(prime**0.5) + 1)
        )
    ):
        raise ValueError("prime must be an odd prime")

    labels = tuple(itertools.product(range(prime), repeat=3))
    rows = tuple(itertools.product(range(prime), repeat=2))
    support_by_label = {}
    row_degrees = {row: 0 for row in rows}

    for label in labels:
        support = frozenset(
            (u, polynomial_value(label, u, prime))
            for u in range(prime)
        )
        support_by_label[label] = support
        for row in support:
            row_degrees[row] += 1

    label_degrees = [
        len(support_by_label[label])
        for label in labels
    ]
    if set(label_degrees) != {prime}:
        raise AssertionError("label support degree is not q")
    if set(row_degrees.values()) != {prime**2}:
        raise AssertionError("row support degree is not q^2")

    weight = prime**4
    support_cells = sum(label_degrees)
    total_mass = support_cells * weight
    diagonal_energy = support_cells * weight**2
    label_masses = [
        degree * weight for degree in label_degrees
    ]
    aggregate_energy = sum(mass * mass for mass in label_masses)

    matching_sizes = {}
    for label, support in support_by_label.items():
        # Each left vertex has one edge.  A maximum matching can select
        # one edge for every distinct right value.
        matching_sizes[label] = len({right for _, right in support})

    good_matching_labels = sum(
        size >= (prime + 1) // 2
        for label, size in matching_sizes.items()
        if label[0] != 0 or label[1] != 0
    )
    if good_matching_labels != prime**3 - prime:
        raise AssertionError("nonconstant matching count failed")

    # Exhaustive K_{3,2} and K_{4,2} audits for test-size primes.
    maximum_triple_common = 0
    triple_row_checks = 0
    maximum_four_common = 0
    four_row_checks = 0
    label_sets_by_row = {
        row: frozenset(
            label
            for label in labels
            if row in support_by_label[label]
        )
        for row in rows
    }
    maximum_pair_common = 0
    compatible_pair_checks = 0
    for first, second in itertools.combinations(rows, 2):
        common_size = len(
            label_sets_by_row[first].intersection(
                label_sets_by_row[second]
            )
        )
        maximum_pair_common = max(maximum_pair_common, common_size)
        if first[0] != second[0]:
            if common_size != prime:
                raise AssertionError(
                    "two-node interpolation count failed"
                )
            compatible_pair_checks += 1
        elif common_size != 0:
            raise AssertionError("one input received two values")

    for chosen_rows in itertools.combinations(rows, 3):
        common = set(label_sets_by_row[chosen_rows[0]])
        for row in chosen_rows[1:]:
            common.intersection_update(label_sets_by_row[row])
            if not common:
                break
        maximum_triple_common = max(
            maximum_triple_common, len(common)
        )
        triple_row_checks += 1
    if maximum_triple_common > 1:
        raise AssertionError("unexpected K_3,2")

    for chosen_rows in itertools.combinations(rows, 4):
        common = set(label_sets_by_row[chosen_rows[0]])
        for row in chosen_rows[1:]:
            common.intersection_update(label_sets_by_row[row])
            if not common:
                break
        maximum_four_common = max(maximum_four_common, len(common))
        four_row_checks += 1
    if maximum_four_common > 1:
        raise AssertionError("unexpected K_4,2")

    return {
        "prime": prime,
        "planes": 2 * prime,
        "unordered_cross_rows": len(rows),
        "labels": len(labels),
        "support_cells": support_cells,
        "cell_weight": weight,
        "row_support_degree": prime**2,
        "label_support_degree": prime,
        "row_mass": prime**6,
        "label_mass": prime**5,
        "total_mass": total_mass,
        "diagonal_energy": diagonal_energy,
        "aggregate_energy": aggregate_energy,
        "cross_plane_codegree": aggregate_energy - diagonal_energy,
        "good_matching_labels": good_matching_labels,
        "guaranteed_matching_size": (prime + 1) // 2,
        "maximum_pair_row_common_labels": maximum_pair_common,
        "compatible_pair_checks": compatible_pair_checks,
        "maximum_triple_row_common_labels": maximum_triple_common,
        "triple_row_checks": triple_row_checks,
        "maximum_four_row_common_labels": maximum_four_common,
        "four_row_checks": four_row_checks,
    }


def audit(prime: int = 7) -> dict[str, object]:
    weighted_checks = exhaustive_weighted_extraction_check()
    ledgers = {
        str(lam): {
            key: str(value)
            for key, value in critical_exponent_ledger(lam).items()
        }
        for lam in (
            Fraction(5),
            Fraction(11, 2),
            Fraction(6),
        )
    }
    if critical_exponent_ledger(Fraction(11, 2))[
        "automatic_matching"
    ] != Fraction(1, 2):
        raise AssertionError("matching split exponent failed")
    if critical_exponent_ledger(Fraction(11, 2))[
        "hub_mass"
    ] != Fraction(5):
        raise AssertionError("hub exponent failed")
    if critical_exponent_ledger(Fraction(11, 2))[
        "hub_label_count"
    ] != Fraction(1):
        raise AssertionError("hub label exponent failed")

    model = finite_field_tensor(prime)
    expected = {
        "support_cells": prime**4,
        "cell_weight": prime**4,
        "row_mass": prime**6,
        "label_mass": prime**5,
        "total_mass": prime**8,
        "diagonal_energy": prime**12,
        "aggregate_energy": prime**13,
        "cross_plane_codegree": prime**13 - prime**12,
        "maximum_pair_row_common_labels": prime,
        "maximum_triple_row_common_labels": 1,
        "maximum_four_row_common_labels": 1,
    }
    for key, value in expected.items():
        if model[key] != value:
            raise AssertionError(
                f"{key}: got {model[key]}, expected {value}"
            )

    return {
        "schema": "amra.erdos1083.high-codegree-matching-hub.v1",
        "status": "PASS",
        "exhaustive_weighted_graph_checks": weighted_checks,
        "critical_ledgers": ledgers,
        "finite_field_model": model,
        "claim_boundary": (
            "Abstract weighted plane-pair/distance tensor only; "
            "no Euclidean realizability claim."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=7)
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.prime),
            indent=args.indent,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
