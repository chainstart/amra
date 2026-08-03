#!/usr/bin/env python3
"""Exact small-D unit/translation adversary for normalized quotient moments."""

from fractions import Fraction
from itertools import combinations, product
from math import comb
import json


Poly = dict[Fraction, int]


def mul(left: Poly, right: Poly) -> Poly:
    out: Poly = {}
    for a, ca in left.items():
        for b, cb in right.items():
            out[a + b] = out.get(a + b, 0) + ca * cb
    return {e: c for e, c in out.items() if c}


def shift(poly: Poly, amount: Fraction) -> Poly:
    return {e + amount: c for e, c in poly.items()}


def mask_support(poly: Poly) -> tuple[Fraction, ...]:
    assert all(c == 1 for c in poly.values())
    return tuple(sorted(poly))


def squarefree_split(number: int) -> tuple[int, int]:
    assert number >= 1
    square = 1
    radical = 1
    p = 2
    rest = number
    while p * p <= rest:
        exponent = 0
        while rest % p == 0:
            rest //= p
            exponent += 1
        square *= p ** (exponent // 2)
        if exponent % 2:
            radical *= p
        p += 1
    if rest > 1:
        radical *= rest
    return square, radical


def sqrt_fraction(value: Fraction) -> tuple[Fraction, int]:
    # sqrt(n/d)=sqrt(n*d)/d, then remove the largest integer square.
    square, radical = squarefree_split(value.numerator * value.denominator)
    return Fraction(square, value.denominator), radical


def distance_key(tau1: Fraction, z1: Fraction,
                 tau2: Fraction, z2: Fraction) -> tuple[Fraction, int, Fraction]:
    constant = tau1 + tau2 + (z1 - z2) ** 2
    coefficient, radical = sqrt_fraction(tau1 * tau2)
    coefficient *= -2
    if radical == 1:
        return constant + coefficient, 1, Fraction(0)
    return constant, radical, coefficient


def target_label_count(t: Fraction) -> tuple[int, int]:
    complements = {
        1: (0, 2, 4, 6, 8, 10),
        2: (0, 1, 4, 5, 8, 9),
        3: (0, 1, 2, 6, 7, 8),
    }
    targets: list[tuple[int, Fraction, Fraction]] = []
    for lam, base in complements.items():
        z = Fraction(lam, 2)
        for a in base:
            tau = Fraction(100 + a) - lam * t - 1 - z * z
            assert tau > 0
            targets.append((lam, tau, z))
    labels = {
        distance_key(p[1], p[2], q[1], q[2])
        for p, q in combinations(targets, 2)
    }
    return len(targets), len(labels)


def main() -> None:
    x = {Fraction(1): 1}
    one = {Fraction(0): 1}
    G = {Fraction(0): 1, Fraction(1): 1}
    F0 = {Fraction(0): 1, Fraction(2): 1}
    R1 = one
    R3 = {Fraction(0): 1, Fraction(1): -1, Fraction(2): 1}
    H2 = {Fraction(0): 1, Fraction(1): 1, Fraction(2): 1}
    H3 = {Fraction(0): 1, Fraction(2): -1, Fraction(4): 1}
    B = mul(R3, mul(H2, H3))
    Q1 = B
    Q3 = mul(H2, H3)

    assert B == {Fraction(0): 1, Fraction(4): 1, Fraction(8): 1}
    PA0 = mul(G, B)
    PA1 = mul(F0, Q1)
    PA3 = mul(F0, Q3)
    assert mask_support(PA0) == (0, 1, 4, 5, 8, 9)
    assert mask_support(PA1) == (0, 2, 4, 6, 8, 10)
    assert mask_support(PA3) == (0, 1, 2, 6, 7, 8)
    assert mul(R1, Q1) == B and mul(R3, Q3) == B
    assert mul(G, R1) == G
    assert mul(G, R3) == {Fraction(0): 1, Fraction(3): 1}

    # Translation t changes only Laurent units in the normalized factor data.
    translation_checks = []
    for t in (Fraction(0), Fraction(-1, 4), Fraction(-1, 2)):
        assert -1 <= t and t + 1 <= 1
        Gt = shift(G, t)
        F0t = shift(F0, 2 * t)
        R1t = R1
        R3t = shift(R3, 2 * t)
        Bt = shift(B, -3 * t)
        Q1t = Bt
        Q3t = shift(Q3, -5 * t)
        assert mul(Gt, Bt) == shift(PA0, -2 * t)
        assert mul(R1t, Q1t) == Bt
        assert mul(R3t, Q3t) == Bt
        assert mul(F0t, Q1t) == shift(PA1, -t)
        assert mul(F0t, Q3t) == shift(PA3, -3 * t)
        assert mul(Gt, R3t) == shift({Fraction(0): 1, Fraction(3): 1}, 3 * t)

        targets, distance_labels = target_label_count(t)
        translation_checks.append({
            "t": str(t),
            "source_X": [str(t), str(t + 1)],
            "target_count": targets,
            "target_target_distance_labels": distance_labels,
        })

    by_t = {row["t"]: row["target_target_distance_labels"] for row in translation_checks}
    assert by_t["0"] == 127
    assert by_t["-1/4"] == 145

    # The two leaf rows have the same Boolean factor vectors for every t.
    boolean_vectors = {"lambda_1": [1, 1, 1], "lambda_3": [0, 1, 1]}

    boolean_guards = []
    for dimension in (2, 4, 6, 8, 10):
        layer = [bits for bits in product((0, 1), repeat=dimension)
                 if sum(bits) == dimension // 2]
        first_walsh = []
        for coordinate in range(dimension):
            numerator = sum(1 if bits[coordinate] == 0 else -1 for bits in layer)
            first_walsh.append(Fraction(numerator, len(layer)))
        assert all(value == 0 for value in first_walsh)
        assert len(layer) == comb(dimension, dimension // 2)
        boolean_guards.append({
            "D": dimension,
            "middle_layer_rows": len(layer),
            "all_degree_one_walsh_moments": 0,
        })

    print(json.dumps({
        "schema": "amra.erdos1083.moment-round4.small-d-unit-translation-adversary.v1",
        "exact_block": {
            "source": "X_t={t,t+1}",
            "scalars": [1, 2, 3],
            "common_spectrum": list(range(100, 112)),
            "common_factor_on_odd_leaves": "G=1+x",
            "center_mask": "F0=1+x^2",
            "B": "1+x^4+x^8",
            "Q1_normalized": "(x^2-x+1)(x^2+x+1)(x^4-x^2+1)",
            "Q3_normalized": "(x^2+x+1)(x^4-x^2+1)",
            "boolean_vectors": boolean_vectors,
            "paired_positive_products": True,
            "common_X_scalar_copies": True,
            "actual_reverse_circle_geometry": True,
        },
        "translation_checks": translation_checks,
        "boolean_moment_guards": {
            "middle_layers": boolean_guards,
            "conclusion": "degree-one Fourier moments can vanish on binomially many exactly recovered quotient vectors",
        },
        "adversarial_pair": {
            "same_normalized_boolean_data": True,
            "same_factor_root_and_log_derivative_data_after_unit_quotient": True,
            "same_per_row_source_target_spectrum": list(range(100, 112)),
            "t_0_target_distance_labels": by_t["0"],
            "t_minus_quarter_target_distance_labels": by_t["-1/4"],
            "opposite_collision_behavior": "127 versus 145 exact target-target squared-distance labels",
        },
        "scope": (
            "Kills every unit-blind inference that normalized Boolean/factor moments and the common per-row spectrum determine target-target collision behaviour. "
            "The finite pair does not refute a uniform lower bound common to both models or an asymptotic unit-aware theorem."
        ),
        "public_exponent_changed": False,
        "lean_used": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
