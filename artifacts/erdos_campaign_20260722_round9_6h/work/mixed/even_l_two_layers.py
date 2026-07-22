#!/usr/bin/env python3
"""Exact audit for the proved even-l layers and higher-layer seeds of #686.

The accompanying REPORT.md contains the general coefficient proofs.  This
script checks the transformations and congruences with exact Fractions; it is
only a regression test and never extrapolates a finite scan.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import comb, factorial


def v2_integer(value: int) -> int:
    if value == 0:
        raise ValueError("v2(0)")
    value = abs(value)
    answer = 0
    while value % 2 == 0:
        answer += 1
        value //= 2
    return answer


def v2(value: Fraction | int) -> int:
    value = Fraction(value)
    return v2_integer(value.numerator) - v2_integer(value.denominator)


def sqrt_product_coefficients(parameters: list[int], degree: int) -> list[Fraction]:
    polynomial = [1]
    for parameter in parameters:
        polynomial.append(0)
        for index in range(len(polynomial) - 1, 0, -1):
            polynomial[index] -= parameter * polynomial[index - 1]
    root = [Fraction(1)]
    for index in range(1, degree + 1):
        cross = sum(root[j] * root[index - j] for j in range(1, index))
        root.append((Fraction(polynomial[index]) - cross) / 2)
    return root


def odd_square_coefficients(l: int) -> list[Fraction]:
    return sqrt_product_coefficients([(2 * j - 1) ** 2 for j in range(1, l + 1)], l // 2)


def triangular_middle_polynomial(m: int) -> list[Fraction]:
    """Ascending coefficients of C_m(z)."""
    triangular = [j * (j - 1) // 2 for j in range(1, 2 * m + 1)]
    root = sqrt_product_coefficients(triangular, m)
    return list(reversed(root))


def evaluate(coefficients: list[Fraction], value: int) -> Fraction:
    answer = Fraction(0)
    for coefficient in reversed(coefficients):
        answer = answer * value + coefficient
    return answer


def mahler_coefficients(coefficients: list[Fraction]) -> list[Fraction]:
    values = [evaluate(coefficients, value) for value in range(len(coefficients))]
    answer = []
    while values:
        answer.append(values[0])
        values = [values[index + 1] - values[index] for index in range(len(values) - 1)]
    return answer


def odd_part(value: int) -> int:
    while value % 2 == 0:
        value //= 2
    return value


def product_polynomial(parameters: list[int]) -> list[int]:
    answer = [1]
    for parameter in parameters:
        answer.append(0)
        for index in range(len(answer) - 1, 0, -1):
            answer[index] -= parameter * answer[index - 1]
    return answer


def check_mod4_odd_middle(m: int) -> bool:
    assert m % 2 == 1
    actual = product_polynomial([j * (j - 1) // 2 for j in range(1, 2 * m + 1)])
    expected = [(-1) ** j * comb(m, j) for j in range(m + 1)]
    expected += [0] * m
    return all((x - y) % 4 == 0 for x, y in zip(actual, expected))


def check_first_doubling_quotient(s: int) -> bool:
    """Check X=v^2/(1-v) mod 2 through degree 2s in P/(1-v)^(2s)=1+2X."""
    assert s % 2 == 1
    middle = 2 * s
    actual = product_polynomial([
        j * (j - 1) // 2 for j in range(1, 2 * middle + 1)
    ])
    baseline = [(-1) ** j * comb(middle, j) for j in range(middle + 1)]
    baseline += [0] * middle
    half_difference = [((x - y) // 2) % 2 for x, y in zip(actual, baseline)]
    denominator = [comb(middle, j) % 2 for j in range(middle + 1)]
    quotient = []
    for degree in range(middle + 1):
        value = half_difference[degree]
        for index in range(1, min(degree, middle) + 1):
            value ^= denominator[index] & quotient[degree - index]
        quotient.append(value)
    return quotient == [0, 0] + [1] * (middle - 1)


def check_third_layer_seed(s: int) -> bool:
    """Check the proved mod-8 seed for l=8s, s odd, through degree 4s.

    If P_(4s)/(1-v)^(4s)=1+4Y, then over F_2
      Y=(v^2+v^3+v^5+v^6)/(1+v^4).
    This seed alone does not prove the valuation formula at this layer.
    """
    assert s % 2 == 1
    middle = 4 * s
    actual = product_polynomial([
        j * (j - 1) // 2 for j in range(1, 2 * middle + 1)
    ])
    baseline = [(-1) ** j * comb(middle, j) for j in range(middle + 1)]
    baseline += [0] * middle
    quarter_difference = [((x - y) // 4) % 2 for x, y in zip(actual, baseline)]
    denominator = [comb(middle, j) % 2 for j in range(middle + 1)]
    quotient = []
    for degree in range(middle + 1):
        value = quarter_difference[degree]
        for index in range(1, min(degree, middle) + 1):
            value ^= denominator[index] & quotient[degree - index]
        quotient.append(value)
    expected = []
    numerator_degrees = {2, 3, 5, 6}
    for degree in range(middle + 1):
        expected.append(sum(
            degree >= base and (degree - base) % 4 == 0
            for base in numerator_degrees
        ) % 2)
    return quotient == expected


def check_third_layer_mod16_lift(s: int) -> bool:
    """Check Y=s(v^2+v^3+2v^4+v^5+3v^6)/(1-v)^4 mod 4."""
    assert s % 2 == 1
    middle = 4 * s
    actual = product_polynomial([
        j * (j - 1) // 2 for j in range(1, 2 * middle + 1)
    ])
    baseline = [(-1) ** j * comb(middle, j) for j in range(middle + 1)]
    baseline += [0] * middle
    rhs = [((x - y) // 4) % 4 for x, y in zip(actual, baseline)]
    denominator = [coefficient % 4 for coefficient in baseline]
    quotient = []
    for degree in range(middle + 1):
        value = rhs[degree]
        for index in range(1, min(degree, middle) + 1):
            value -= denominator[index] * quotient[degree - index]
        quotient.append(value % 4)

    block_denominator = [1, -4, 6, -4, 1]
    numerator = [0] * (middle + 1)
    for degree, coefficient in {2: 1, 3: 1, 4: 2, 5: 1, 6: 3}.items():
        if degree <= middle:
            numerator[degree] = (s * coefficient) % 4
    expected = []
    for degree in range(middle + 1):
        value = numerator[degree]
        for index in range(1, min(degree, 4) + 1):
            value -= block_denominator[index] * expected[degree - index]
        expected.append(value % 4)
    return quotient == expected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-l", type=int, default=64)
    parser.add_argument("--max-x", type=int, default=63)
    args = parser.parse_args()
    rows = []
    failures = []
    triangular_cache: dict[int, list[Fraction]] = {}
    for l in range(2, args.max_l + 1, 2):
        m = l // 2
        layer = v2_integer(l)
        if layer not in (1, 2):
            continue
        q = odd_square_coefficients(l)
        c = triangular_cache.setdefault(m, triangular_middle_polynomial(m))
        congruence_ok = (
            check_mod4_odd_middle(m)
            if layer == 1
            else check_first_doubling_quotient(m // 2)
        )
        expected = (
            -v2_integer(factorial(m))
            if layer == 1
            else 2 * (m // 2) - v2_integer(factorial(m // 2))
        )
        row_failures = 0
        for x in range(args.max_x + 1):
            w = 2 * x + 2 * l + 1
            z = (w * w - 1) // 8
            original_q = sum(q[j] * w ** (l - 2 * j) for j in range(len(q)))
            transformed_q = 8 ** m * evaluate(c, z)
            actual = v2(original_q) - l
            if original_q != transformed_q or actual != expected:
                row_failures += 1
                failures.append({"l": l, "x": x, "actual": actual, "expected": expected})
        rows.append({
            "l": l,
            "v2_l": layer,
            "predicted_v2_A": expected,
            "coefficient_congruence_pass": congruence_ok,
            "evaluations": args.max_x + 1,
            "failures": row_failures,
        })
        if not congruence_ok:
            failures.append({"l": l, "kind": "coefficient_congruence"})
    # This is deliberately labelled a probe: proving this integer-valued
    # Cartier congruence for all m would iterate the two proved layers.
    cartier_cases = 0
    cartier_failures = []
    for m in range(1, args.max_l // 4 + 1):
        current = triangular_cache.setdefault(m, triangular_middle_polynomial(m))
        doubled = triangular_cache.setdefault(2 * m, triangular_middle_polynomial(2 * m))
        odd = odd_part(m)
        target = 2 * m - 2 * odd - v2_integer(factorial(odd))
        for z in range(-args.max_x, args.max_x + 1):
            difference = evaluate(doubled, z) - (-1) ** m * 2**m * evaluate(current, z)
            cartier_cases += 1
            if difference and v2(difference) < target + 1:
                cartier_failures.append({
                    "m": m, "z": z, "actual": v2(difference),
                    "required": target + 1,
                })
    third_layer_seed_rows = [
        {
            "l": 8 * s,
            "s": s,
            "mod8_seed_pass": check_third_layer_seed(s),
            "mod16_lift_pass": check_third_layer_mod16_lift(s),
            "pass": check_third_layer_seed(s) and check_third_layer_mod16_lift(s),
        }
        for s in range(1, args.max_l // 8 + 1, 2)
    ]
    isolated_higher_layers = []
    for m in (4, 8):
        coefficients = triangular_cache.setdefault(m, triangular_middle_polynomial(m))
        target = m - 2 * odd_part(m) - v2_integer(factorial(odd_part(m)))
        normalized = [value / 2**target for value in mahler_coefficients(coefficients)]
        isolated_higher_layers.append({
            "l": 2 * m,
            "predicted_v2_C": target,
            "normalized_mahler_coefficients": [int(value) for value in normalized],
            "constant_odd_all_higher_even": (
                all(value.denominator == 1 for value in normalized)
                and int(normalized[0]) % 2 == 1
                and all(int(value) % 2 == 0 for value in normalized[1:])
            ),
        })
    third_layer_divisibility_rows = []
    for s in range(1, args.max_l // 8 + 1, 2):
        m = 4 * s
        coefficients = triangular_cache.setdefault(m, triangular_middle_polynomial(m))
        valuations = [v2(evaluate(coefficients, z)) for z in range(args.max_x + 1)]
        required = 2 if s == 1 else 3
        third_layer_divisibility_rows.append({
            "l": 8 * s,
            "s": s,
            "required_v2_C": required,
            "minimum_observed_v2_C": min(valuations),
            "pass": all(value >= required for value in valuations),
        })
    print(json.dumps({
        "status": "PASS" if (
            not failures
            and all(row["pass"] for row in third_layer_seed_rows)
            and all(
                row["constant_odd_all_higher_even"]
                for row in isolated_higher_layers
            )
            and all(row["pass"] for row in third_layer_divisibility_rows)
        ) else "FAIL",
        "scope": "finite regression only; general proof is in REPORT.md",
        "max_l": args.max_l,
        "max_x": args.max_x,
        "rows": rows,
        "evaluations": sum(row["evaluations"] for row in rows),
        "failures": failures,
        "unproved_cartier_doubling_probe": {
            "claim": "C_(2m)(z) = (-1)^m 2^m C_m(z) mod 2^(T(2m)+1) as integer-valued functions",
            "cases": cartier_cases,
            "failures": cartier_failures,
            "global_claim": False,
        },
        "proved_third_layer_mod8_seed": {
            "claim": "P_(4s)/(1-v)^(4s)=1+4Y; Y=(v^2+v^3+v^5+v^6)/(1+v^4) mod 2 and its stated mod-4 lift for odd s",
            "rows": third_layer_seed_rows,
            "all_pass": all(row["pass"] for row in third_layer_seed_rows),
            "full_valuation_claim": False,
        },
        "proved_isolated_higher_layer_integer_valued_certificates": isolated_higher_layers,
        "proved_third_layer_uniform_divisibility_regression": third_layer_divisibility_rows,
    }, indent=2))


if __name__ == "__main__":
    main()
