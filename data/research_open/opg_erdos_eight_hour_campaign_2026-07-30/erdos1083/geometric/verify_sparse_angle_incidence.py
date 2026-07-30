#!/usr/bin/env python3
"""Exact regression for sparse height-angle incidence expansion."""

from __future__ import annotations

import json
import random
from collections import Counter
from fractions import Fraction


def difference_multiplicity(values: tuple[Fraction, ...]) -> int:
    counts = Counter(
        left - right
        for left in values
        for right in values
        if left != right
    )
    return max(counts.values(), default=0)


def audit_pattern(
    height_values: tuple[Fraction, ...],
    chord_values: tuple[Fraction, ...],
    incidences: frozenset[tuple[int, int]],
) -> dict[str, int]:
    if len(set(height_values)) != len(height_values):
        raise ValueError("height-square values must be distinct")
    if max(Counter(chord_values).values(), default=0) > 2:
        raise ValueError("chord multiplicity exceeds two")
    if any(
        height < 0
        or height >= len(height_values)
        or angle < 0
        or angle >= len(chord_values)
        for height, angle in incidences
    ):
        raise ValueError("incidence index out of range")

    representations = Counter(
        height_values[height] + chord_values[angle]
        for height, angle in incidences
    )
    union_size = len(representations)
    exact_energy = sum(value * value for value in representations.values())
    lam = difference_multiplicity(height_values)
    I = len(incidences)
    J = len(chord_values)
    upper = 2 * I + lam * J * J
    if exact_energy > upper:
        raise AssertionError(
            ("energy", exact_energy, upper, height_values, chord_values)
        )
    if union_size * upper < I * I:
        raise AssertionError(("cauchy", union_size, upper, I))
    return {
        "height_count": len(height_values),
        "angle_count": J,
        "incidence_count": I,
        "difference_multiplicity": lam,
        "union_size": union_size,
        "exact_energy": exact_energy,
        "energy_upper_bound": upper,
    }


def audit() -> dict[str, object]:
    rng = random.Random(1083)
    records = []
    for trial in range(120):
        m = 3 + trial % 7
        J = 3 + (trial * 5) % 9
        heights = tuple(
            sorted(
                {
                    Fraction(value * value)
                    for value in rng.sample(range(0, 5 * m), m)
                }
            )
        )
        if len(heights) != m:
            raise AssertionError("sampled integer squares must be distinct")
        base_chords = [Fraction(value, 7) for value in range(J)]
        if trial % 3 == 0 and J >= 4:
            base_chords[-1] = base_chords[-2]
        chords = tuple(base_chords)
        incidences = frozenset(
            (height, angle)
            for height in range(m)
            for angle in range(J)
            if rng.randrange(5) < 3
        )
        if not incidences:
            incidences = frozenset({(0, 0)})
        records.append(audit_pattern(heights, chords, incidences))

    full_heights = tuple(Fraction(value * value) for value in range(8))
    full_chords = tuple(Fraction(value, 11) for value in range(9))
    full = audit_pattern(
        full_heights,
        full_chords,
        frozenset(
            (height, angle)
            for height in range(len(full_heights))
            for angle in range(len(full_chords))
        ),
    )

    return {
        "schema": "amra.erdos1083.sparse-angle-incidence.v1",
        "scope": (
            "Finite exact regression of a human incidence-energy theorem; "
            "not an unconditional f_3 improvement."
        ),
        "random_sparse_records": records,
        "full_rectangle_record": full,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
