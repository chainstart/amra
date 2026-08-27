#!/usr/bin/env python3
"""Exact-normalization check for the L=2 periodized carry majorant.

The finite examples validate identities only; they are not asymptotic
evidence for the required small-CRT estimate.
"""

from fractions import Fraction
import itertools
import json
import math


def centered(value: int, modulus: int) -> int:
    value %= modulus
    return value if 2 * value <= modulus else value - modulus


def crt_lift(residues: tuple[int, ...], moduli: tuple[int, ...]) -> int:
    period = math.prod(moduli)
    value = 0
    for residue, modulus in zip(residues, moduli):
        cofactor = period // modulus
        value += residue * cofactor * pow(cofactor, -1, modulus)
    return centered(value, period)


def beta_l2(a: int, b: Fraction) -> Fraction:
    if Fraction(abs(a)) >= b:
        return Fraction(0)
    return (b - abs(a)) / (b * b)


def sinc(x: float) -> float:
    return 1.0 if x == 0 else math.sin(x) / x


def one_system(k: int, offsets: tuple[int, ...], delta: int, h: int,
               z_cap: int) -> dict[str, object]:
    moduli = tuple(k + d for d in offsets)
    period = math.prod(moduli)
    assert h < period / 2
    b = Fraction((delta - 1) // 2) + Fraction(1, 2)
    local = tuple(range(-math.floor(b), math.floor(b) + 1))

    exact_frequency_sum = Fraction(0)
    admitted = 0
    for word in itertools.product(local, repeat=len(moduli)):
        global_frequency = crt_lift(word, moduli)
        if abs(global_frequency) >= h:
            continue
        admitted += 1
        coefficient = math.prod(beta_l2(a, b) for a in word)
        exact_frequency_sum += (
            Fraction(period, h)
            * (1 - Fraction(abs(global_frequency), h))
            * coefficient
        )

    # The exact-carry diagonal is only one summand in the positive
    # periodized product.  This brute box checks the inequality numerically.
    partial_nonzero = 0.0
    for word in itertools.product(range(-z_cap, z_cap + 1), repeat=len(moduli)):
        if all(value == 0 for value in word):
            continue
        numerator = sum(
            value * (period // modulus)
            for value, modulus in zip(word, moduli)
        )
        diagonal = sinc(math.pi * h * numerator / period) ** 2
        local_weight = math.prod(
            sinc(math.pi * float(b) * value / modulus) ** 2
            for value, modulus in zip(word, moduli)
        )
        partial_nonzero += diagonal * local_weight

    return {
        "k": k,
        "offsets": offsets,
        "moduli": moduli,
        "P": period,
        "b": str(b),
        "h": h,
        "h_lt_P_over_2": 2 * h < period,
        "small_frequency_words": len(local) ** len(moduli),
        "admitted_centered_global_frequencies": admitted,
        "S_exact_numerator": exact_frequency_sum.numerator,
        "S_exact_denominator": exact_frequency_sum.denominator,
        "S_float": float(exact_frequency_sum),
        "Omega_0": 1,
        "S_minus_Omega_0": float(exact_frequency_sum - 1),
        "z_box_cap": z_cap,
        "partial_H_nonzero": partial_nonzero,
        "partial_majorized": partial_nonzero <= float(exact_frequency_sum - 1) + 1e-12,
    }


def main() -> None:
    rows = [
        one_system(7, (4, 6), 4, 5, 30),
        one_system(100, (5, 6, 7), 4, 17, 9),
    ]
    print(json.dumps({"classification": "finite_identity_check_only", "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
