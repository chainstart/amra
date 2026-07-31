#!/usr/bin/env python3
"""Independent semantic audit for the OPG-1757 second-depth formula.

This file deliberately does not import either campaign verifier.  It uses
two small, direct implementations:

1. the primitive page chain, enumerating subsets of *positions* in every
   current block profile (rather than aggregating equal block sizes);
2. unordered labelled hyperedge sets, checked for hypergraphic
   acyclicity with a disjoint-set data structure, followed by a brute-force
   enumeration of the remaining ordinary forest.

The first implementation checks the five final coefficients for small
parameters.  Comparing the two implementations checks the j! ordering
factor and the 1/m! interpretation for every excess species through three,
including three ternary hyperedges.

These are finite falsification tests.  The all-s proof is supplied
separately by the denominator-aware Abel lemma in
ABEL_EXCEPTIONAL_PROFILE_LEMMA.md.  Together they provide the required
cleared-denominator identity certificate.
"""

from __future__ import annotations

import argparse
import itertools
import math
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache


Profile = tuple[int, ...]


class DSU:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union_roots(self, roots: tuple[int, ...]) -> None:
        root = roots[0]
        for other in roots[1:]:
            self.parent[other] = root


@lru_cache(maxsize=None)
def direct_transitions(
    profile: Profile, maximum_size: int
) -> tuple[tuple[int, int, Profile], ...]:
    """Enumerate actual subsets of current block positions."""

    rows: list[tuple[int, int, Profile]] = []
    block_count = len(profile)
    for size in range(2, min(block_count, maximum_size) + 1):
        for selected in itertools.combinations(range(block_count), size):
            selected_set = set(selected)
            multiplicity = math.prod(profile[index] for index in selected)
            destination = tuple(
                sorted(
                    [
                        profile[index]
                        for index in range(block_count)
                        if index not in selected_set
                    ]
                    + [sum(profile[index] for index in selected)]
                )
            )
            rows.append((size, multiplicity, destination))
    return tuple(rows)


def direct_chain(
    profile: Profile, maximum_order: int, maximum_degree: int
) -> list[list[int]]:
    """Primitive nilpotent chain with no equal-weight aggregation."""

    vector: dict[tuple[Profile, int], int] = {(profile, 0): 1}
    result: list[list[int]] = []
    for _ in range(maximum_order + 1):
        row = [0] * (maximum_degree + 1)
        for (_, degree), coefficient in vector.items():
            row[degree] += coefficient
        result.append(row)
        next_vector: defaultdict[tuple[Profile, int], int] = defaultdict(int)
        for (source, degree), coefficient in vector.items():
            for size, multiplicity, destination in direct_transitions(
                source, maximum_degree - degree
            ):
                next_vector[(destination, degree + size)] += (
                    coefficient * multiplicity
                )
        vector = dict(next_vector)
    return result


def initial_profile(s: int, h: int) -> Profile:
    return tuple(sorted((2,) * h + (1,) * (s - 2 * h)))


def closed_polynomials(s: int) -> tuple[Fraction, ...]:
    return (
        Fraction(
            2 * (s - 4) * (s**3 + 12 * s**2 + 20 * s - 225)
        ),
        Fraction(
            8
            * (s - 4)
            * (3 * s**3 + 20 * s**2 - 28 * s - 225),
            3,
        ),
        Fraction(
            4 * (s - 4) * (4 * s**3 + 6 * s**2 - 85 * s + 72)
        ),
        Fraction(
            8 * (s - 4) * (2 * s - 5) * (s**2 - s - 8)
        ),
        Fraction(
            2 * (s - 4) * (s - 3) * (2 * s - 7) * (6 * s - 11),
            3,
        ),
    )


def signed_product_coefficient(
    left: list[int],
    right: list[int],
    lambda_exponent: int,
    s: int,
    target_degree: int,
) -> int:
    total = 0
    for left_degree, left_value in enumerate(left):
        if not left_value:
            continue
        for right_degree, right_value in enumerate(right):
            if not right_value:
                continue
            lambda_degree = target_degree - left_degree - right_degree
            if 0 <= lambda_degree <= lambda_exponent:
                total += (
                    left_value
                    * right_value
                    * math.comb(lambda_exponent, lambda_degree)
                    * s**lambda_degree
                )
    return total


def raw_second_deficit(s: int) -> dict[int, int]:
    """Compute B_(2s-7) directly from primitive chains and overlaps."""

    depth = 2 * s - 7
    maximum_degree = 4 * s - 10
    chains = {
        h: direct_chain(
            initial_profile(s, h), depth, maximum_degree
        )
        for h in range(3)
    }
    result: dict[int, int] = {}
    for degree in range(2 * depth, maximum_degree + 1):
        coefficient = 0
        for left_order in range(depth + 1):
            for right_order in range(depth + 1):
                overlap = left_order + right_order - depth
                # At this depth, overlap >= 3 already has minimum beta
                # degree above the global top face.
                if overlap < 0 or overlap > 2:
                    continue
                if overlap > min(left_order, right_order):
                    continue
                lambda_exponent = 3 - overlap
                multiplier = math.factorial(depth) // (
                    math.factorial(overlap)
                    * math.factorial(left_order - overlap)
                    * math.factorial(right_order - overlap)
                )
                positive = signed_product_coefficient(
                    chains[1][left_order],
                    chains[1][right_order],
                    lambda_exponent,
                    s,
                    degree,
                )
                negative = signed_product_coefficient(
                    chains[0][left_order],
                    chains[2][right_order],
                    lambda_exponent,
                    s,
                    degree,
                )
                coefficient += multiplier * (positive - negative)
        if coefficient:
            result[degree] = coefficient
    return result


def expected_second_deficit(s: int) -> dict[int, int]:
    depth = 2 * s - 7
    result: dict[int, int] = {}
    for offset, polynomial in enumerate(closed_polynomials(s)):
        scale = (
            Fraction(math.factorial(depth))
            * Fraction(s) ** (2 * s - 12 + offset)
        )
        value = scale * polynomial
        if value.denominator != 1:
            raise AssertionError("closed coefficient was not integral")
        if value:
            result[4 * s - 14 + offset] = value.numerator
    return result


@lru_cache(maxsize=None)
def ordinary_forest_weight(profile: Profile, components: int) -> int:
    """Brute-force every ordinary edge subset on a contracted profile."""

    block_count = len(profile)
    edge_count = block_count - components
    if edge_count < 0:
        return 0
    edges = list(itertools.combinations(range(block_count), 2))
    total = 0
    for forest in itertools.combinations(edges, edge_count):
        dsu = DSU(block_count)
        weight = 1
        acyclic = True
        for left, right in forest:
            left_root = dsu.find(left)
            right_root = dsu.find(right)
            if left_root == right_root:
                acyclic = False
                break
            dsu.union_roots((left_root, right_root))
            weight *= profile[left] * profile[right]
        if acyclic:
            total += weight
    return total


def nonbinary_size_patterns(excess: int) -> tuple[tuple[int, ...], ...]:
    return {
        0: ((),),
        1: ((3,),),
        2: ((4,), (3, 3)),
        3: ((5,), (3, 4), (3, 3, 3)),
    }[excess]


def hyperedge_configurations(
    vertex_count: int, sizes: tuple[int, ...]
):
    """Yield each unordered nonbinary hyperedge set exactly once."""

    if not sizes:
        yield ()
        return
    choices = {
        size: tuple(itertools.combinations(range(vertex_count), size))
        for size in set(sizes)
    }
    grouped: list[
        tuple[tuple[tuple[int, ...], ...], ...]
    ] = []
    for size, count in itertools.groupby(sizes):
        multiplicity = sum(1 for _ in count)
        grouped.append(
            tuple(itertools.combinations(choices[size], multiplicity))
        )
    for blocks in itertools.product(*grouped):
        yield tuple(edge for block in blocks for edge in block)


def semantic_hyperforest_weight(
    profile: Profile, excess: int, components: int
) -> int:
    """Unordered labelled-hyperedge semantics, independent of contractions."""

    vertex_count = len(profile)
    total = 0
    for sizes in nonbinary_size_patterns(excess):
        for hyperedges in hyperedge_configurations(vertex_count, sizes):
            dsu = DSU(vertex_count)
            incidence_weight = 1
            acyclic = True
            for edge in hyperedges:
                roots = tuple(dsu.find(vertex) for vertex in edge)
                if len(set(roots)) != len(roots):
                    acyclic = False
                    break
                dsu.union_roots(roots)
                incidence_weight *= math.prod(
                    profile[vertex] for vertex in edge
                )
            if not acyclic:
                continue
            component_members: defaultdict[int, list[int]] = defaultdict(list)
            for vertex in range(vertex_count):
                component_members[dsu.find(vertex)].append(vertex)
            contracted = tuple(
                sorted(
                    sum(profile[vertex] for vertex in members)
                    for members in component_members.values()
                )
            )
            total += incidence_weight * ordinary_forest_weight(
                contracted, components
            )
    return total


def displayed_component_polynomial(
    h: int, excess: int, components: int, s: int
) -> Fraction:
    """Independent transcription of SECOND_DEFICIT_COMPONENT_TABLE.md."""

    table = {
        (0, 0, 1): Fraction(1),
        (1, 0, 1): Fraction(1),
        (2, 0, 1): Fraction(1),
        (0, 0, 2): Fraction((s - 1) * (s + 6), 2),
        (1, 0, 2): Fraction((s - 2) * (s + 6), 2),
        (2, 0, 2): Fraction(s**2 + 3 * s - 20, 2),
        (0, 0, 3): Fraction(
            (s - 2) * (s - 1) * (s**2 + 13 * s + 60), 8
        ),
        (1, 0, 3): Fraction(
            (s - 3) * (s - 2) * (s**2 + 13 * s + 60), 8
        ),
        (2, 0, 3): Fraction(
            (s - 4) * (s**3 + 10 * s**2 + 17 * s - 210), 8
        ),
        (0, 0, 4): Fraction(
            (s - 3)
            * (s - 2)
            * (s - 1)
            * (s**3 + 21 * s**2 + 202 * s + 840),
            48,
        ),
        (1, 0, 4): Fraction(
            (s - 4)
            * (s - 3)
            * (s - 2)
            * (s**3 + 21 * s**2 + 202 * s + 840),
            48,
        ),
        (2, 0, 4): Fraction(
            (s - 5)
            * (s - 4)
            * (s**4 + 18 * s**3 + 133 * s**2 + 138 * s - 3024),
            48,
        ),
        (0, 1, 1): Fraction((s - 2) * (s - 1), 2),
        (1, 1, 1): Fraction((s - 3) * (s - 2), 2),
        (2, 1, 1): Fraction((s - 4) * (s - 3), 2),
        (0, 1, 2): Fraction(
            (s - 3) * (s - 2) * (s - 1) * (3 * s + 20), 12
        ),
        (1, 1, 2): Fraction(
            (s - 4) * (s - 3) * (s - 2) * (3 * s + 20), 12
        ),
        (2, 1, 2): Fraction(
            (s - 5) * (s - 4) * (3 * s**2 + 11 * s - 66), 12
        ),
        (0, 1, 3): Fraction(
            (s - 4)
            * (s - 3)
            * (s - 2)
            * (s - 1)
            * (3 * s**2 + 43 * s + 210),
            48,
        ),
        (1, 1, 3): Fraction(
            (s - 5)
            * (s - 4)
            * (s - 3)
            * (s - 2)
            * (3 * s**2 + 43 * s + 210),
            48,
        ),
        (2, 1, 3): Fraction(
            (s - 6)
            * (s - 5)
            * (s - 4)
            * (3 * s**3 + 34 * s**2 + 69 * s - 728),
            48,
        ),
        (0, 2, 1): Fraction(
            (s - 3) * (s - 2) * (s - 1) * (3 * s - 8), 24
        ),
        (1, 2, 1): Fraction(
            (s - 4) * (s - 3) * (s - 2) * (3 * s - 11), 24
        ),
        (2, 2, 1): Fraction(
            (s - 5) * (s - 4) * (s - 3) * (3 * s - 14), 24
        ),
        (0, 2, 2): Fraction(
            (s - 4)
            * (s - 3)
            * (s - 2)
            * (s - 1)
            * (3 * s**2 + 11 * s - 80),
            48,
        ),
        (1, 2, 2): Fraction(
            (s - 5)
            * (s - 4)
            * (s - 3)
            * (s - 2)
            * (3 * s**2 + 8 * s - 102),
            48,
        ),
        (2, 2, 2): Fraction(
            (s - 6)
            * (s - 5)
            * (s - 4)
            * (3 * s**3 - 4 * s**2 - 145 * s + 406),
            48,
        ),
        (0, 3, 1): Fraction(
            (s - 4) ** 2
            * (s - 3) ** 2
            * (s - 2)
            * (s - 1),
            48,
        ),
        (1, 3, 1): Fraction(
            (s - 5) ** 2
            * (s - 4) ** 2
            * (s - 3)
            * (s - 2),
            48,
        ),
        (2, 3, 1): Fraction(
            (s - 6) ** 2
            * (s - 5) ** 2
            * (s - 4)
            * (s - 3),
            48,
        ),
    }
    return table[(h, excess, components)]


def audit_ordering_factors(s: int = 7) -> int:
    """Check every endpoint, table entry, and excess species through three."""

    checked = 0
    endpoint_pairs = (
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 1),
        (2, 2),
        (3, 1),
    )
    for h in range(3):
        profile = initial_profile(s, h)
        maximum_order = len(profile) - 1
        maximum_degree = 2 * maximum_order + 3
        chain = direct_chain(profile, maximum_order, maximum_degree)
        for excess, components in endpoint_pairs:
            order = len(profile) - components - excess
            if order < 0:
                continue
            measured = chain[order][2 * order + excess]
            semantic = semantic_hyperforest_weight(
                profile, excess, components
            )
            expected = math.factorial(order) * semantic
            if measured != expected:
                raise AssertionError(
                    "ordering mismatch at "
                    f"(s,h,e,c)=({s},{h},{excess},{components}): "
                    f"{measured} != {expected}"
                )
            exponent = s - h - 2 * components - excess
            table_value = (
                Fraction(2**h)
                * Fraction(s) ** exponent
                * displayed_component_polynomial(
                    h, excess, components, s
                )
            )
            if table_value.denominator != 1:
                raise AssertionError("displayed component value is fractional")
            if semantic != table_value.numerator:
                raise AssertionError(
                    "component-table mismatch at "
                    f"(s,h,e,c)=({s},{h},{excess},{components}): "
                    f"{semantic} != {table_value.numerator}"
                )
            checked += 1
    return checked


def audit_rational_certificate_points(sample_start: int = 7) -> int:
    """Supply enough points for the weaker, denominator-aware degree bound.

    For excess e, the finite-type Abel expansion gives the normalized
    endpoint a denominator dividing s**e and a numerator of degree at most

        2*c + 3*e - 2.

    Thus 2*c+3*e-1 exact values prove a displayed polynomial identity
    after clearing the denominator.  The main verifier now uses the same
    count; this implementation remains independent and direct-position.
    """

    endpoint_pairs = (
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 1),
        (2, 2),
        (3, 1),
    )
    largest_s = max(
        sample_start + (2 * components + 3 * excess - 1) - 1
        for excess, components in endpoint_pairs
    )
    chains: dict[tuple[int, int], list[list[int]]] = {}
    for s in range(sample_start, largest_s + 1):
        for h in range(3):
            profile = initial_profile(s, h)
            maximum_order = len(profile) - 1
            chains[(s, h)] = direct_chain(
                profile,
                maximum_order,
                2 * maximum_order + 3,
            )

    checked = 0
    for h in range(3):
        for excess, components in endpoint_pairs:
            required = 2 * components + 3 * excess - 1
            for s in range(sample_start, sample_start + required):
                profile = initial_profile(s, h)
                order = len(profile) - components - excess
                chain_value = chains[(s, h)][order][
                    2 * order + excess
                ]
                if chain_value % math.factorial(order):
                    raise AssertionError("ordered chain did not divide by j!")
                measured = chain_value // math.factorial(order)
                exponent = s - h - 2 * components - excess
                expected = (
                    Fraction(2**h)
                    * Fraction(s) ** exponent
                    * displayed_component_polynomial(
                        h, excess, components, s
                    )
                )
                if expected.denominator != 1:
                    raise AssertionError(
                        "displayed component value is fractional"
                    )
                if measured != expected.numerator:
                    raise AssertionError(
                        "rational-certificate mismatch at "
                        f"(s,h,e,c)=({s},{h},{excess},{components}): "
                        f"{measured} != {expected.numerator}"
                    )
                checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--minimum-s", type=int, default=4)
    parser.add_argument("--maximum-s", type=int, default=7)
    parser.add_argument("--species-s", type=int, default=7)
    args = parser.parse_args()

    for s in range(args.minimum_s, args.maximum_s + 1):
        measured = raw_second_deficit(s)
        expected = expected_second_deficit(s)
        if measured != expected:
            raise AssertionError(
                f"raw pooled mismatch at s={s}: {measured} != {expected}"
            )
        print(f"raw pooled s={s}: PASS ({len(measured)} coefficients)")

    species = audit_ordering_factors(args.species_s)
    print(
        f"unordered hyperforest / ordered chain: PASS "
        f"({species} endpoints at s={args.species_s})"
    )
    certificate_points = audit_rational_certificate_points()
    print(
        "denominator-aware component certificate: PASS "
        f"({certificate_points} exact endpoint values)"
    )
    print("scope: finite falsification audit; not an all-s degree proof")


if __name__ == "__main__":
    main()
