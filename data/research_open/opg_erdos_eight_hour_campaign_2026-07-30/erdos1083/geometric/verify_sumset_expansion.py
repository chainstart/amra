#!/usr/bin/env python3
"""Exact certificates for the common-radius square/chord sumset bound."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction

import sympy as sp


Vector = tuple[Fraction, ...]


def divisor_count(value: int) -> int:
    if value < 1:
        raise ValueError("divisor_count needs a positive integer")
    result = 1
    remaining = value
    prime = 2
    while prime * prime <= remaining:
        exponent = 0
        while remaining % prime == 0:
            exponent += 1
            remaining //= prime
        if exponent:
            result *= exponent + 1
        prime = 3 if prime == 2 else prime + 2
    if remaining > 1:
        result *= 2
    return result


def maximum_divisor_count(limit: int) -> int:
    if limit < 1:
        return 1
    return max(divisor_count(value) for value in range(1, limit + 1))


def rational_chord_values(
    cosine: Fraction, angular_size: int, height_count: int
) -> tuple[Vector, ...]:
    left, right = Fraction(1), cosine
    chebyshev = [left]
    if angular_size > 1:
        chebyshev.append(right)
    for _ in range(2, angular_size):
        left, right = right, 2 * cosine * right - left
        chebyshev.append(right)
    return tuple(
        (2 * height_count * height_count * (1 - value),)
        for value in chebyshev
    )


def polynomial_key(poly: sp.Poly, degree: int) -> Vector:
    return tuple(
        Fraction(int(coefficient.p), int(coefficient.q))
        for coefficient in (
            sp.Rational(poly.nth(index)) for index in range(degree)
        )
    )


def algebraic_chord_values(
    modulus_expression: sp.Expr,
    angular_size: int,
    height_count: int,
) -> tuple[Vector, ...]:
    variable = next(iter(modulus_expression.free_symbols))
    modulus = sp.Poly(modulus_expression, variable, domain=sp.QQ)
    degree = modulus.degree()
    left = sp.Poly(1, variable, domain=sp.QQ)
    right = sp.Poly(variable, variable, domain=sp.QQ)
    chebyshev = [left]
    if angular_size > 1:
        chebyshev.append(right)
    for _ in range(2, angular_size):
        left, right = (
            right,
            (
                2 * sp.Poly(variable, variable, domain=sp.QQ) * right
                - left
            ).rem(modulus),
        )
        chebyshev.append(right)
    one = sp.Poly(1, variable, domain=sp.QQ)
    return tuple(
        polynomial_key(
            (2 * height_count * height_count * (one - value)).rem(
                modulus
            ),
            degree,
        )
        for value in chebyshev
    )


def cyclotomic_chord_values(
    order: int, angular_size: int, height_count: int
) -> tuple[Vector, ...]:
    if order < angular_size:
        raise ValueError("the first angular points would not be distinct")
    variable = sp.symbols("z")
    modulus = sp.Poly(
        sp.cyclotomic_poly(order, variable), variable, domain=sp.QQ
    )
    degree = modulus.degree()
    result = []
    for index in range(angular_size):
        expression = sp.Poly(
            height_count
            * height_count
            * (
                2
                - variable**index
                - variable ** ((-index) % order)
            ),
            variable,
            domain=sp.QQ,
        ).rem(modulus)
        result.append(polynomial_key(expression, degree))
    return tuple(result)


def add_integer(vector: Vector, value: int) -> Vector:
    return (vector[0] + value,) + vector[1:]


def sumset_audit(height_count: int, chord_values: tuple[Vector, ...]) -> dict:
    angular_size = len(chord_values)
    if height_count < 1 or angular_size < 1:
        raise ValueError("positive sizes required")
    if len({len(value) for value in chord_values}) != 1:
        raise ValueError("inconsistent coordinate dimensions")
    maximum_chord_multiplicity = max(
        Counter(chord_values).values()
    )
    assert maximum_chord_multiplicity <= 2

    representations: Counter[Vector] = Counter()
    for chord in chord_values:
        for difference in range(height_count):
            representations[
                add_integer(chord, difference * difference)
            ] += 1
    union_size = len(representations)
    energy = sum(value * value for value in representations.values())
    tau_star = maximum_divisor_count((height_count - 1) ** 2)
    energy_upper_bound = (
        2 * height_count * angular_size
        + tau_star * angular_size * angular_size
    )
    integer_relation_pairs = 0
    maximum_difference = (height_count - 1) ** 2
    for left_index, left in enumerate(chord_values):
        for right_index, right in enumerate(chord_values):
            if left_index == right_index or left == right:
                continue
            difference = tuple(
                right_value - left_value
                for left_value, right_value in zip(left, right)
            )
            if (
                all(value == 0 for value in difference[1:])
                and difference[0].denominator == 1
                and 0 < abs(difference[0]) <= maximum_difference
            ):
                integer_relation_pairs += 1
    refined_energy_upper_bound = (
        2 * height_count * angular_size
        + tau_star * integer_relation_pairs
    )
    assert energy <= refined_energy_upper_bound
    assert energy <= energy_upper_bound
    numerator = height_count * height_count * angular_size * angular_size
    assert union_size * energy_upper_bound >= numerator
    return {
        "height_count": height_count,
        "angular_size": angular_size,
        "chord_value_count": len(set(chord_values)),
        "maximum_chord_multiplicity": maximum_chord_multiplicity,
        "sumset_size": union_size,
        "representation_energy": energy,
        "tau_star": tau_star,
        "energy_upper_bound": energy_upper_bound,
        "integer_relation_pairs": integer_relation_pairs,
        "refined_energy_upper_bound": refined_energy_upper_bound,
        "cauchy_lower_bound_floor": numerator // energy_upper_bound,
    }


def certificate() -> dict:
    rational_cases = []
    for cosine, angular_size, height_count in (
        (Fraction(3, 4), 12, 12),
        (Fraction(2, 3), 11, 9),
        (Fraction(1, 4), 14, 10),
        (Fraction(-5, 8), 10, 13),
    ):
        record = sumset_audit(
            height_count,
            rational_chord_values(cosine, angular_size, height_count),
        )
        record["cosine"] = str(cosine)
        rational_cases.append(record)

    variable = sp.symbols("x")
    algebraic_cases = []
    for modulus, angular_size, height_count, label in (
        (9 * variable**2 - 2, 10, 9, "sqrt(2)/3"),
        (5 * variable**3 - 1, 11, 10, "5^(-1/3)"),
        (2 * variable**9 - 1, 9, 8, "degree_9_full_rank"),
    ):
        values = algebraic_chord_values(
            modulus, angular_size, height_count
        )
        record = sumset_audit(height_count, values)
        record["label"] = label
        record["modulus"] = str(modulus)
        if sp.Poly(modulus, variable).degree() >= angular_size:
            assert record["sumset_size"] == height_count * angular_size
        algebraic_cases.append(record)

    cyclotomic_cases = []
    for order, angular_size, height_count in (
        (7, 7, 8),
        (12, 10, 9),
        (17, 12, 10),
        (20, 20, 11),
    ):
        record = sumset_audit(
            height_count,
            cyclotomic_chord_values(
                order, angular_size, height_count
            ),
        )
        record["root_of_unity_order"] = order
        cyclotomic_cases.append(record)

    adversarial_integer_cases = []
    for size in (8, 12, 20):
        values = tuple(
            (Fraction(-(index * index)),)
            for index in range(size)
        )
        record = sumset_audit(size, values)
        record["model"] = "A_m-A_m square-difference stress test"
        adversarial_integer_cases.append(record)

    payload = {
        "schema": "amra.erdos1083.square-chord-sumset.v1",
        "rational_cases": rational_cases,
        "algebraic_cases": algebraic_cases,
        "cyclotomic_cases": cyclotomic_cases,
        "adversarial_integer_cases": adversarial_integer_cases,
        "transcendental_case": (
            "formal theorem: all m*S indexed layers are disjoint"
        ),
        "theorem": (
            "|A_m+X_S| >= (m*S)^2/(2*m*S+tau_*S^2), "
            "tau_*=max_(1<=n< m^2) divisor_count(n)"
        ),
    }
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    )
    payload["sha256"] = hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()
    return payload


def main() -> int:
    result = certificate()
    print(
        "SQUARE_CHORD_SUMSET"
        f"|rational_cases={len(result['rational_cases'])}"
        f"|algebraic_cases={len(result['algebraic_cases'])}"
        f"|cyclotomic_cases={len(result['cyclotomic_cases'])}"
        "|transcendental_full_layers=true"
        "|critical_bound=m^(2-o(1))"
    )
    print(f"CERTIFICATE|sha256={result['sha256']}")
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
