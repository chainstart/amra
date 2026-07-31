#!/usr/bin/env python3
"""Independent semantic audit for the OPG-1757 q=3 layer.

This module deliberately does not import ``verify_fourth_q3`` or either
endpoint enumerator used by that verifier.  It supplies two separate checks.

1. Hyperedges are contracted by enumerating subsets of *positions* in the
   current profile.  The remaining ordinary forest is evaluated by assigning
   the exceptional vertices and labelled unit vertices to temporarily
   labelled components.  This differs from the equal-weight aggregation in
   the main verifier.
2. The final seven coefficients are recomputed by the primitive page-transfer
   and Newton-pooling engine from the earlier campaign.  The seven proposed
   formulas are transcribed independently below.

The main verifier compares all 345 endpoint values returned here with its
symbolic table.  The primitive audit is a finite falsification check, whereas
the all-s conclusion uses the proved Abel degree bound.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Iterator


Profile = tuple[int, ...]


def weak_compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first, *tail)


@lru_cache(maxsize=None)
def independent_forest_weight(profile: Profile, components: int) -> int:
    """Weighted complete-graph forest via labelled component allocation.

    Unit vertices remain labelled through the multinomial coefficient.
    Exceptional vertices are assigned by position, even when two have equal
    weights.  Division by ``components!`` removes the temporary component
    labels.
    """

    if components < 1 or components > len(profile):
        return 0
    unit_count = profile.count(1)
    exceptional = tuple(weight for weight in profile if weight != 1)
    total = 0
    for assignment in itertools.product(
        range(components), repeat=len(exceptional)
    ):
        exceptional_sums = [0] * components
        exceptional_counts = [0] * components
        exceptional_products = [1] * components
        for weight, cell in zip(exceptional, assignment):
            exceptional_sums[cell] += weight
            exceptional_counts[cell] += 1
            exceptional_products[cell] *= weight

        for unit_cells in weak_compositions(unit_count, components):
            if any(
                exceptional_counts[index] + unit_cells[index] == 0
                for index in range(components)
            ):
                continue
            multiplicity = math.factorial(unit_count)
            product = 1
            for index, unit_cell in enumerate(unit_cells):
                multiplicity //= math.factorial(unit_cell)
                size = exceptional_counts[index] + unit_cell
                if size > 1:
                    weight_sum = exceptional_sums[index] + unit_cell
                    product *= (
                        weight_sum ** (size - 2)
                        * exceptional_products[index]
                    )
            total += multiplicity * product

    divisor = math.factorial(components)
    if total % divisor:
        raise AssertionError("temporary component labels did not divide")
    return total // divisor


@lru_cache(maxsize=None)
def direct_contractions(
    profile: Profile, selection_size: int
) -> tuple[tuple[int, Profile], ...]:
    """Enumerate actual subsets of profile positions for one hyperedge."""

    rows: list[tuple[int, Profile]] = []
    for selected in itertools.combinations(
        range(len(profile)), selection_size
    ):
        selected_set = set(selected)
        multiplicity = math.prod(profile[index] for index in selected)
        destination = tuple(
            sorted(
                [
                    profile[index]
                    for index in range(len(profile))
                    if index not in selected_set
                ]
                + [sum(profile[index] for index in selected)]
            )
        )
        rows.append((multiplicity, destination))
    return tuple(rows)


@lru_cache(maxsize=None)
def independent_hyperforest_weight(
    s: int, h: int, excess: int, components: int
) -> int:
    """Unordered nonbinary hyperedges plus an independent forest evaluator."""

    initial = tuple(sorted((2,) * h + (1,) * (s - 2 * h)))
    if excess == 0:
        return independent_forest_weight(initial, components)

    layer: dict[tuple[Profile, int], int] = {(initial, 0): 1}
    answer = Fraction(0)
    for nonbinary_count in range(1, excess + 1):
        next_layer: defaultdict[tuple[Profile, int], int] = defaultdict(int)
        for (profile, used_excess), coefficient in layer.items():
            for added_excess in range(
                1, excess - used_excess + 1
            ):
                for multiplicity, destination in direct_contractions(
                    profile, added_excess + 2
                ):
                    next_layer[
                        (destination, used_excess + added_excess)
                    ] += coefficient * multiplicity
        layer = dict(next_layer)
        ordered_weight = sum(
            coefficient * independent_forest_weight(profile, components)
            for (profile, used_excess), coefficient in layer.items()
            if used_excess == excess
        )
        answer += Fraction(
            ordered_weight, math.factorial(nonbinary_count)
        )

    if answer.denominator != 1:
        raise AssertionError("unordered hyperforest weight was fractional")
    return answer.numerator


def q3_endpoint_entries() -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (h, excess, components)
        for h in range(3)
        for excess in range(5)
        for components in range(1, 6 - excess)
    )


def endpoint_point_count(excess: int, components: int) -> int:
    return 2 * components + 3 * excess - 1


@lru_cache(maxsize=1)
def independent_endpoint_certificate(
    sample_start: int = 8,
) -> tuple[tuple[int, int, int, int, int], ...]:
    """Return the 345 direct-position endpoint values."""

    rows: list[tuple[int, int, int, int, int]] = []
    for h, excess, components in q3_endpoint_entries():
        required = endpoint_point_count(excess, components)
        for s in range(sample_start, sample_start + required):
            rows.append(
                (
                    s,
                    h,
                    excess,
                    components,
                    independent_hyperforest_weight(
                        s, h, excess, components
                    ),
                )
            )
    if len(rows) != 345:
        raise AssertionError("q=3 endpoint certificate count changed")
    return tuple(rows)


def expected_normalized_layers(s: int) -> tuple[Fraction, ...]:
    """Independent numeric transcription of the seven q=3 formulas."""

    return (
        Fraction(
            2
            * (s - 4)
            * (
                s**5
                + 16 * s**4
                + 52 * s**3
                - 587 * s**2
                - 3063 * s
                + 12240
            ),
            3,
        ),
        Fraction(
            4
            * (s - 4)
            * (
                3 * s**5
                + 31 * s**4
                - 16 * s**3
                - 1217 * s**2
                - 1038 * s
                + 12240
            ),
            3,
        ),
        Fraction(
            2
            * (s - 4)
            * (
                18 * s**5
                + 85 * s**4
                - 678 * s**3
                - 3138 * s**2
                + 13195 * s
                - 2475
            ),
            3,
        ),
        Fraction(
            8
            * (s - 4)
            * (
                8 * s**5
                - 6 * s**4
                - 314 * s**3
                + 432 * s**2
                + 2847 * s
                - 5265
            ),
            3,
        ),
        Fraction(
            2
            * (s - 4)
            * (2 * s - 9)
            * (
                18 * s**4
                - 29 * s**3
                - 391 * s**2
                + 1054 * s
                - 312
            ),
            3,
        ),
        Fraction(
            4
            * (s - 4)
            * (2 * s - 9)
            * (2 * s - 7)
            * (3 * s - 7)
            * (s**2 - s - 8),
            3,
        ),
        Fraction(
            2
            * (s - 4)
            * (s - 3)
            * (2 * s - 9)
            * (2 * s - 7)
            * (2 * s**2 - 11 * s + 13),
            3,
        ),
    )


def expected_q3_coefficients(s: int) -> dict[int, int]:
    depth = 2 * s - 8
    result: dict[int, int] = {}
    for offset, polynomial in enumerate(expected_normalized_layers(s)):
        value = (
            Fraction(math.factorial(depth))
            * Fraction(s) ** (2 * s - 14 + offset)
            * polynomial
        )
        if value.denominator != 1:
            raise AssertionError("q=3 formula was not integral")
        if value:
            result[4 * s - 16 + offset] = value.numerator
    return result


def primitive_q3_coefficients(s: int) -> dict[int, int]:
    """Recompute one row using the pre-existing primitive transfer."""

    research_open = Path(__file__).resolve().parents[2]
    primitive_dir = (
        research_open / "q1_eight_hour_campaign_2026-07-29" / "opg1757"
    )
    sys.path.insert(0, str(primitive_dir))
    try:
        from tp2_barrier_search import pooled_t_newton_rows
    finally:
        sys.path.pop(0)
    depth = 2 * s - 8
    return {
        int(degree): int(coefficient)
        for row_depth, degree, coefficient in pooled_t_newton_rows(
            s, 4 * s - 8
        )
        if int(row_depth) == depth
    }


def audit_primitive_q3(
    minimum_s: int = 4, maximum_s: int = 16
) -> tuple[tuple[int, int, int], ...]:
    rows: list[tuple[int, int, int]] = []
    for s in range(minimum_s, maximum_s + 1):
        measured = primitive_q3_coefficients(s)
        expected = expected_q3_coefficients(s)
        if measured != expected:
            raise AssertionError(
                f"primitive q=3 mismatch at s={s}: "
                f"{measured} != {expected}"
            )
        rows.extend(
            (s, degree, coefficient)
            for degree, coefficient in sorted(expected.items())
        )
    return tuple(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--minimum-s", type=int, default=4)
    parser.add_argument("--maximum-s", type=int, default=16)
    args = parser.parse_args()
    endpoints = independent_endpoint_certificate()
    primitive = audit_primitive_q3(args.minimum_s, args.maximum_s)
    payload = json.dumps(
        [endpoints, primitive], separators=(",", ":")
    ).encode("utf-8")
    print(
        json.dumps(
            {
                "status": "PASS",
                "independent_endpoint_values": len(endpoints),
                "largest_endpoint_s": max(row[0] for row in endpoints),
                "primitive_q3_rows": len(primitive),
                "primitive_s_range": [
                    args.minimum_s,
                    args.maximum_s,
                ],
                "sha256": hashlib.sha256(payload).hexdigest(),
                "scope": (
                    "independent finite audit; the all-s proof uses the "
                    "Abel degree lemma"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
