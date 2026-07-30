#!/usr/bin/env python3
"""Exact regression for the arbitrary-height square-energy dichotomy."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from fractions import Fraction


def chebyshev(value: Fraction, index: int) -> Fraction:
    if index == 0:
        return Fraction(1)
    if index == 1:
        return value
    left, right = Fraction(1), value
    for _ in range(2, index + 1):
        left, right = right, 2 * value * right - left
    return right


def difference_multiplicity(values: set[Fraction]) -> int:
    counts = Counter(
        left - right
        for left in values
        for right in values
        if left != right
    )
    return max(counts.values(), default=0)


def layer_multiplicity(layers: tuple[Fraction, ...]) -> int:
    return max(Counter(layers).values(), default=0)


def energy(
    values: set[Fraction], layers: tuple[Fraction, ...]
) -> tuple[int, int]:
    representations = Counter(
        value + layer for value in values for layer in layers
    )
    return len(representations), sum(count * count for count in representations.values())


def audit_case(
    height_offsets: tuple[Fraction, ...],
    layers: tuple[Fraction, ...],
) -> dict[str, int]:
    if min(height_offsets) != 0 or len(set(height_offsets)) != len(
        height_offsets
    ):
        raise ValueError("need distinct nonnegative offsets starting at zero")
    if layer_multiplicity(layers) > 2:
        raise ValueError("the theorem permits layer multiplicity at most two")
    values = {offset * offset for offset in height_offsets}
    if len(values) != len(height_offsets):
        raise AssertionError("nonnegative distinct offsets must have distinct squares")
    m = len(values)
    S = len(layers)
    lam = difference_multiplicity(values)
    union_size, exact_energy = energy(values, layers)
    upper_energy = 2 * m * S + lam * S * S
    if exact_energy > upper_energy:
        raise AssertionError(
            ("energy", exact_energy, upper_energy, m, S, lam)
        )
    if union_size * upper_energy < m * m * S * S:
        raise AssertionError(
            ("cauchy", union_size, upper_energy, m, S, lam)
        )
    return {
        "height_count": m,
        "layer_count": S,
        "difference_multiplicity": lam,
        "union_size": union_size,
        "exact_energy": exact_energy,
        "energy_upper_bound": upper_energy,
    }


def divisor_count(value: int) -> int:
    result = 0
    for divisor in range(1, math.isqrt(value) + 1):
        if value % divisor == 0:
            result += 1 if divisor * divisor == value else 2
    return result


def lattice_audit(subset: tuple[int, ...]) -> dict[str, int]:
    values = {Fraction(value * value) for value in subset}
    lam = difference_multiplicity(values)
    height = max(subset)
    divisor_maximum = max(
        (divisor_count(value) for value in range(1, height * height + 1)),
        default=1,
    )
    if lam > divisor_maximum:
        raise AssertionError((subset, lam, divisor_maximum))
    return {
        "subset_size": len(subset),
        "height_bound": height,
        "difference_multiplicity": lam,
        "divisor_maximum": divisor_maximum,
    }


def audit() -> dict[str, object]:
    angle_cases = (
        (Fraction(3, 4), 11),
        (Fraction(2, 3), 10),
        (Fraction(4, 5), 12),
    )
    height_cases = (
        tuple(Fraction(value) for value in (0, 1, 3, 4, 8, 10)),
        tuple(Fraction(value, 2) for value in (0, 1, 4, 9, 13, 20)),
        tuple(Fraction(value) for value in (0, 2, 5, 11, 23, 47)),
    )
    records = []
    for cosine, angular_size in angle_cases:
        layers = tuple(
            2 * (1 - chebyshev(cosine, index))
            for index in range(angular_size)
        )
        if layer_multiplicity(layers) > 2:
            raise AssertionError(("angle multiplicity", cosine))
        for heights in height_cases:
            records.append(audit_case(heights, layers))

    # A repeated-layer regression: every value occurs exactly twice.
    repeated_layers = tuple(
        Fraction(value)
        for value in (0, 0, 2, 2, 7, 7, 13, 13)
    )
    records.append(audit_case(height_cases[0], repeated_layers))

    lattice_records = [
        lattice_audit(subset)
        for subset in (
            (0, 1, 2, 3, 4, 5),
            (0, 2, 3, 7, 11, 16),
            (0, 1, 4, 9, 16, 25),
            (0, 5, 13, 21, 34, 55),
        )
    ]

    # Deliberately create many squared-offset values differing by one.
    # Every nonnegative rational here can be realized by a real height
    # offset after taking its square root.
    resonant_values = {
        Fraction(index * index, 4) for index in range(1, 12, 2)
    }
    translated = {value + 1 for value in resonant_values}
    artificial_values = resonant_values | translated | {Fraction(0)}
    high_lambda = difference_multiplicity(artificial_values)
    if high_lambda < len(resonant_values):
        raise AssertionError(("high lambda", high_lambda))

    return {
        "schema": "amra.erdos1083.arbitrary-height-energy.v1",
        "scope": (
            "Finite exact regression for a human energy dichotomy; "
            "not an unconditional f_3 exponent improvement."
        ),
        "slice_records": records,
        "lattice_records": lattice_records,
        "artificial_high_lambda": high_lambda,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
