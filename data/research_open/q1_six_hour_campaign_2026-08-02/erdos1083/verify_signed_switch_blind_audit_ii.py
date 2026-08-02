#!/usr/bin/env python3
"""Independent finite guards for SIGNED_SWITCH_BLIND_AUDIT_II.md.

This file deliberately imports none of the four author verifiers.  The
all-parameter proofs are audited in the accompanying note; these checks are
finite regression guards for their exact algebra, automata, quotient tiles,
and endpoint constants.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
FILES = [
    "CYCLOTOMIC_SIMULTANEOUS_POSITIVE_MULTIPLE_BOUND.md",
    "FINITE_QUOTIENT_SHADOW_ESCAPE.md",
    "PHI6_SWITCH_CUBE_TRANSVERSE_FIBER_RIGIDITY.md",
    "TRANSVERSE_BINARY_BOX_PHI6_SWITCH_BOUND.md",
    "SIGNED_SWITCH_RESULT_DEPENDENCY_MAP.md",
    "MULTIDIRECTIONAL_TENSOR_SWITCH_BARRIER.md",
]


Poly = dict[tuple[int, ...], int]


def add_term(poly: Poly, exponent: tuple[int, ...], coefficient: int) -> None:
    value = poly.get(exponent, 0) + coefficient
    if value:
        poly[exponent] = value
    else:
        poly.pop(exponent, None)


def multiply(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for a, ca in left.items():
        for b, cb in right.items():
            add_term(result, tuple(x + y for x, y in zip(a, b)), ca * cb)
    return result


def is_mask(poly: Poly) -> bool:
    return all(coefficient == 1 for coefficient in poly.values())


def univariate_division(numerator: list[int], denominator: list[int]) -> list[int]:
    work = numerator[:]
    quotient = [0] * max(1, len(numerator) - len(denominator) + 1)
    top = len(denominator) - 1
    assert denominator[top] == 1
    for degree in range(len(work) - 1, top - 1, -1):
        coefficient = work[degree]
        quotient[degree - top] = coefficient
        for index, value in enumerate(denominator):
            work[degree - top + index] -= coefficient * value
    assert all(value == 0 for value in work[:top])
    return quotient


def check_cyclotomic_algebra() -> dict[str, int]:
    identities = 0
    rectangle_states = 0
    for prime in (2, 3, 5, 7):
        p_s = [1] * prime
        for scale in range(1, 9):
            if math.gcd(prime, scale) != 1:
                continue
            numerator = [0] * (prime * scale - scale + 1)
            for index in range(prime):
                numerator[index * scale] = 1
            h = univariate_division(numerator, p_s)

            p_a = [1] * scale
            p_a_of_s = [0] * (prime * (scale - 1) + 1)
            for index in range(scale):
                p_a_of_s[index * prime] = 1
            p_s_of_a = numerator

            def one_poly(values: list[int]) -> Poly:
                return {(index,): value for index, value in enumerate(values) if value}

            assert multiply(one_poly(h), one_poly(p_a)) == one_poly(p_a_of_s)
            assert multiply(one_poly(h), one_poly(p_s)) == one_poly(p_s_of_a)
            identities += 2

            # Finite independent check of the rectangular mass mechanism.
            # Fixing one column potential to zero removes additive redundancy.
            for rows in itertools.product(range(-1, 2), repeat=scale):
                for tail in itertools.product(range(-1, 2), repeat=prime - 1):
                    columns = (0,) + tail
                    matrix = [r + c for r in rows for c in columns]
                    if min(matrix) < 0 or max(matrix) == 0:
                        continue
                    assert sum(matrix) >= min(prime, scale)
                    rectangle_states += 1

    for bound in range(1, 40):
        farey = sum(
            1
            for a in range(1, bound + 1)
            for b in range(1, bound + 1)
            if math.gcd(a, b) == 1
        )
        totient = 1 + 2 * sum(
            sum(math.gcd(r, j) == 1 for j in range(1, r + 1))
            for r in range(2, bound + 1)
        )
        assert farey == totient <= bound * bound
    return {"sharp_identities": identities, "rectangle_states": rectangle_states}


def check_finite_quotient_and_escape() -> dict[str, int]:
    quotient_tiles = 0
    for dimension in range(1, 4):
        for denominator in range(1, 6):
            modulus = 2 * denominator
            h_set = list(itertools.product((0, denominator), repeat=dimension))
            y_set = list(itertools.product(range(denominator), repeat=dimension))
            sums = [
                tuple((x + y) % modulus for x, y in zip(h, y))
                for h in h_set
                for y in y_set
            ]
            assert len(sums) == modulus**dimension
            assert len(set(sums)) == modulus**dimension
            quotient_tiles += 1

    centre = {(0,): 1, (1,): 1, (4,): 1}
    signed = {(0,): 1, (4,): -1, (5,): 1, (7,): 1}
    expected = {(0,): 1, (1,): 1, (6,): 1, (7,): 1, (9,): 1, (11,): 1}
    assert multiply(centre, signed) == expected
    assert sum(signed.values()) == 2 < sum(centre.values()) == 3

    minimum_modulus_margin = float("inf")
    for order in range(2, 513):
        for frequency in range(1, order):
            angle = 2 * math.pi * frequency / order
            root = complex(math.cos(angle), math.sin(angle))
            minimum_modulus_margin = min(
                minimum_modulus_margin,
                abs(1 + root + root**4),
            )
    assert minimum_modulus_margin > 1e-6
    return {
        "quotient_tiles": quotient_tiles,
        "torsion_orders_checked": 511,
    }


def factor(dimension: int, coordinate: int, kind: str) -> Poly:
    zero = (0,) * dimension
    one = list(zero)
    one[coordinate] = 1
    if kind == "A":
        return {zero: 1, tuple(one): 1}
    two = list(zero)
    two[coordinate] = 2
    return {zero: 1, tuple(one): -1, tuple(two): 1}


def product_for_subset(dimension: int, subset: set[int], kind: str = "T") -> Poly:
    result: Poly = {(0,) * dimension: 1}
    for coordinate in sorted(subset):
        result = multiply(result, factor(dimension, coordinate, kind))
    return result


def check_phi6_automaton_and_fibres() -> dict[str, int]:
    words = 0
    for length in range(1, 13):
        t = {(0,): 1, (1,): -1, (2,): 1}
        for bits in itertools.product((0, 1), repeat=length):
            f = {(index,): bit for index, bit in enumerate(bits) if bit}
            product = multiply(f, t)
            padded = (0, 0) + bits + (0, 0)
            avoids = all(padded[i : i + 3] not in ((0, 1, 0), (1, 0, 1))
                         for i in range(len(padded) - 2))
            assert is_mask(product) == avoids
            if bits and any(bits) and avoids:
                assert sum(bits) >= 2
                if sum(bits) == 2:
                    occupied = [index for index, bit in enumerate(bits) if bit]
                    assert occupied[1] == occupied[0] + 1
            words += 1

    valid_rank_two = 0
    grid = list(itertools.product(range(3), repeat=2))
    switches = {
        frozenset(subset): product_for_subset(2, set(subset))
        for size in range(3)
        for subset in itertools.combinations(range(2), size)
    }
    for selection in range(1, 1 << len(grid)):
        a_poly = {grid[index]: 1 for index in range(len(grid)) if selection >> index & 1}
        if all(is_mask(multiply(a_poly, switch)) for switch in switches.values()):
            assert len(a_poly) >= 4
            if len(a_poly) == 4:
                xs = sorted({point[0] for point in a_poly})
                ys = sorted({point[1] for point in a_poly})
                assert len(xs) == len(ys) == 2
                assert xs[1] == xs[0] + 1 and ys[1] == ys[0] + 1
                assert set(a_poly) == set(itertools.product(xs, ys))
            valid_rank_two += 1
    return {"binary_words": words, "valid_rank_two_fibres": valid_rank_two}


def check_binary_box_endpoint() -> dict[str, float | int]:
    quotient_tiles = 0
    for dimension in range(1, 4):
        for denominator in range(1, 5):
            modulus = 2 * denominator
            h_set = set(itertools.product((0, denominator), repeat=dimension))
            y_set = set(itertools.product(range(denominator), repeat=dimension))
            assert {
                tuple((x + y) % modulus for x, y in zip(h, y))
                for h in h_set
                for y in y_set
            } == set(itertools.product(range(modulus), repeat=dimension))
            quotient_tiles += 1

    for dimension in range(1, 7):
        a_product: Poly = {(0,) * dimension: 1}
        t_product: Poly = {(0,) * dimension: 1}
        for coordinate in range(dimension):
            a_product = multiply(a_product, factor(dimension, coordinate, "A"))
            t_product = multiply(t_product, factor(dimension, coordinate, "T"))
        endpoint = multiply(a_product, t_product)
        assert is_mask(a_product) and is_mask(endpoint)
        assert len(a_product) == len(endpoint) == 2**dimension
        assert set(endpoint) == {
            tuple(3 * bit for bit in bits)
            for bits in itertools.product((0, 1), repeat=dimension)
        }

    p = 1 / 7
    entropy = -p * math.log2(p) - (1 - p) * math.log2(1 - p)
    exponent = (7 / 9) * entropy
    gap = 5 / 9 - exponent
    assert abs(entropy - 0.5916727785823274) < 1e-15
    assert abs(exponent - 0.46018993889736574) < 1e-15
    assert abs(gap - 0.09536561665818982) < 1e-15
    return {
        "separating_quotient_tiles": quotient_tiles,
        "entropy": entropy,
        "endpoint_exponent": exponent,
        "gap": gap,
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    result = {
        "status": "PASS",
        "cyclotomic": check_cyclotomic_algebra(),
        "finite_quotient": check_finite_quotient_and_escape(),
        "phi6": check_phi6_automaton_and_fibres(),
        "binary_box": check_binary_box_endpoint(),
        "audited_sha256": {name: sha256(HERE / name) for name in FILES},
        "imports_author_verifiers": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
