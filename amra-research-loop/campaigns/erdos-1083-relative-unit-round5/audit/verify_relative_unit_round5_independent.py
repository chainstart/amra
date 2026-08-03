#!/usr/bin/env python3
"""Independent reconstruction of the round-five two-stage unit lemma.

This file does not import the author checker or its generated JSON.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations
import json
from math import gcd


def rank(rows: list[list[int]]) -> int:
    a = [[Fraction(x) for x in row] for row in rows]
    piv = 0
    for col in range(len(a[0])):
        hit = next((i for i in range(piv, len(a)) if a[i][col]), None)
        if hit is None:
            continue
        a[piv], a[hit] = a[hit], a[piv]
        q = a[piv][col]
        a[piv] = [x / q for x in a[piv]]
        for i in range(len(a)):
            if i != piv and a[i][col]:
                q = a[i][col]
                a[i] = [x - q * y for x, y in zip(a[i], a[piv])]
        piv += 1
    return piv


def det(a: list[list[int]]) -> int:
    if len(a) == 1:
        return a[0][0]
    return sum(
        (-1) ** j * x * det([row[:j] + row[j + 1 :] for row in a[1:]])
        for j, x in enumerate(a[0])
    )


def matvec(a: list[list[int]], v: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(x * y for x, y in zip(row, v)) for row in a)


def squarefree(q: Fraction) -> tuple[Fraction, int]:
    n = q.numerator * q.denominator
    square, free, p = 1, 1, 2
    while p * p <= n:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        square *= p ** (e // 2)
        if e % 2:
            free *= p
        p += 1
    if n > 1:
        free *= n
    return Fraction(square, q.denominator), free


def distance_label(x: tuple[Fraction, Fraction], y: tuple[Fraction, Fraction]):
    tau, z = x
    sigma, w = y
    rational = tau + sigma + (z - w) ** 2
    coefficient, radicand = squarefree(tau * sigma)
    radical = -2 * coefficient
    if radicand == 1:
        rational += radical
        radical = Fraction()
    return rational, radical, radicand


def geometry(shift: Fraction):
    positions = {
        1: (0, 2, 4, 6, 8, 10),
        2: (0, 1, 4, 5, 8, 9),
        3: (0, 1, 2, 6, 7, 8),
    }
    targets = []
    for scalar, support in positions.items():
        z = Fraction(scalar, 2)
        for p in support:
            tau = Fraction(100 + p) + shift - (1 + z * z)
            assert tau > 0
            targets.append((tau, z))
            assert sorted((tau + 1 + z * z, tau + 1 + z * z + scalar)) == [
                Fraction(100 + p) + shift,
                Fraction(100 + p + scalar) + shift,
            ]
    indexed = [distance_label(x, y) for x, y in combinations(targets, 2)]
    labels = Counter(indexed)
    multiplicity_histogram = Counter(labels.values())
    fibres: dict[object, list[int]] = {}
    for i, value in enumerate(indexed):
        fibres.setdefault(value, []).append(i)
    partition = sorted(tuple(indices) for indices in fibres.values())
    return labels, dict(sorted(multiplicity_histogram.items())), partition


def main() -> None:
    # Derived afresh from the eight displayed equations in the lemma.
    full = [
        [1, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1],
        [0, 0, 1, -1, 0, -1, 0],
        [0, 0, 1, 0, -1, 0, -1],
    ]
    stage1 = [full[i] for i in (0, 1, 2, 6, 7)]
    gauge = (1, 0, -1, -1, -1, 0, 0)
    spectrum = (0, 0, 1, 0, 0, 1, 1)
    assert rank(stage1) == 5
    assert matvec(stage1, gauge) == (0,) * 5
    assert matvec(stage1, spectrum) == (0,) * 5
    assert rank(full) == 6
    assert matvec(full, gauge) == (0,) * 8
    assert matvec(full, spectrum) == (0, 0, 0, 1, 1, 1, 0, 0)

    minors = []
    for rr in combinations(range(8), 6):
        for cc in combinations(range(7), 6):
            d = det([[full[i][j] for j in cc] for i in rr])
            if d:
                minors.append(abs(d))
    minor_gcd = 0
    for d in minors:
        minor_gcd = gcd(minor_gcd, d)
    assert minor_gcd == 1

    # Direct substitution in the full affine system.
    for a in (Fraction(-2, 3), Fraction(), Fraction(5, 7)):
        particular = (a, 2 * a, -3 * a, Fraction(), 2 * a, -3 * a, -5 * a)
        rhs = (a, 2 * a, 3 * a, -a, -2 * a, -3 * a, 0, 0)
        assert matvec(full, particular) == rhs
        for delta in (Fraction(-11, 5), Fraction(), Fraction(7, 4)):
            u = tuple(x + delta * y for x, y in zip(particular, gauge))
            assert matvec(full, u) == rhs
            assert u[0] == a if delta == 0 else u[0] != a

    labels0, hist0, partition0 = geometry(Fraction())
    labels1, hist1, partition1 = geometry(Fraction(1, 4))
    assert len(labels0) == len(labels1) == 127
    assert set(labels0) != set(labels1)

    payload = {
        "schema": "amra.erdos1083.relative-unit-round5.independent-audit.v1",
        "stage1_rank": rank(stage1),
        "stage1_kernel_rank": 7 - rank(stage1),
        "stage1_generators_verified": [gauge, spectrum],
        "absolute_spectrum_fixed_rank": rank(full),
        "absolute_spectrum_fixed_kernel_rank": 7 - rank(full),
        "primitive_rank_minor_gcd": minor_gcd,
        "gauge_generator_verified": gauge,
        "spectrum_generator_full_image": matvec(full, spectrum),
        "gauge_slice": "u(G)=a iff delta=0 on the displayed affine line",
        "shift_0_distinct_labels": len(labels0),
        "shift_1_4_distinct_labels": len(labels1),
        "absolute_label_sets_equal": set(labels0) == set(labels1),
        "shift_0_multiplicity_histogram": hist0,
        "shift_1_4_multiplicity_histogram": hist1,
        "multiplicity_histograms_equal": hist0 == hist1,
        "indexed_collision_partitions_equal": partition0 == partition1,
        "interpretation_127_127": "equal finite cardinalities only; the absolute label sets differ and no asymptotic or exponent gain follows",
        "public_exponent_changed": False,
    }
    print(json.dumps(payload, indent=2, sort_keys=True, default=list))


if __name__ == "__main__":
    main()
