#!/usr/bin/env python3
"""Exact invariant and no-go checks for fixed-valuation #635 cycles."""

from __future__ import annotations

import json
from fractions import Fraction
from math import prod


def orbit(a_value: int, multipliers: list[int], p0: int, q0: int):
    p_value, q_value = p0, q0
    p_values: list[int] = []
    q_values: list[int] = []
    edges: list[tuple[int, int]] = []
    for multiplier in multipliers:
        p_values.append(p_value)
        q_values.append(q_value)
        edges.append(tuple(sorted((p_value, q_value))))
        p_numerator = a_value * p_value - 1
        q_numerator = multiplier * q_value + 1
        assert p_numerator % multiplier == 0
        assert q_numerator % a_value == 0
        p_value = p_numerator // multiplier
        q_value = q_numerator // a_value
    assert (p_value, q_value) == (p0, q0)
    return p_values, q_values, edges


def invariant_row(
    a_value: int, multipliers: list[int], p0: int, q0: int
) -> dict[str, object]:
    p_values, q_values, edges = orbit(a_value, multipliers, p0, q0)
    lhs = prod(
        Fraction(a_value * p_value - 1, a_value * p_value)
        for p_value in p_values
    )
    rhs = prod(
        Fraction(a_value * q_value - 1, a_value * q_value)
        for q_value in q_values
    )
    multiplier_ratio = Fraction(prod(multipliers), a_value ** len(multipliers))
    assert lhs == rhs == multiplier_ratio
    assert sum(p_values) == sum(q_values)

    increments = [
        (p_values[index] - q_values[index - 1]) // a_value
        for index in range(len(p_values))
    ]
    assert all(
        p_values[index] - q_values[index - 1]
        == a_value * increments[index]
        for index in range(len(p_values))
    )
    assert sum(increments) == 0
    immediate_return = any(
        edges[index] == edges[index - 1] for index in range(len(edges))
    )
    return {
        "A": a_value,
        "multipliers": multipliers,
        "p_cycle": p_values,
        "q_cycle": q_values,
        "sum_p_equals_sum_q": sum(p_values),
        "euler_product": {
            "numerator": lhs.numerator,
            "denominator": lhs.denominator,
        },
        "increments": increments,
        "immediate_return": immediate_return,
    }


def main() -> None:
    # Composite, integral, nonbacktracking closed walk.  It proves that the
    # two length-independent identities alone do not force a backtrack;
    # primality remains essential.
    composite = invariant_row(4, [1, 3, 21], 23, 163)
    assert composite["p_cycle"] == [23, 91, 121]
    assert composite["q_cycle"] == [163, 41, 31]
    assert not composite["immediate_return"]
    assert any(
        value in (91, 121)
        for value in composite["p_cycle"] + composite["q_cycle"]
    )
    p_desc = sorted(composite["p_cycle"], reverse=True)
    q_desc = sorted(composite["q_cycle"], reverse=True)
    prefix_differences = [
        sum(p_desc[:index]) - sum(q_desc[:index])
        for index in range(1, len(p_desc))
    ]
    assert min(prefix_differences) < 0 < max(prefix_differences)

    # A prime closed walk satisfying the identities, but with an immediate
    # return (indeed the middle edge is traversed back).
    prime_degenerate = invariant_row(4, [1, 1, 57], 3, 43)
    assert prime_degenerate["p_cycle"] == [3, 11, 43]
    assert prime_degenerate["q_cycle"] == [43, 11, 3]
    assert prime_degenerate["immediate_return"]

    # Euler-product equality without the first moment: this independently
    # refutes an Euler-product-only uniqueness argument.
    p_multiset = [3, 11, 43]
    q_multiset = [5, 5, 19]
    euler_p = prod(Fraction(4 * p - 1, 4 * p) for p in p_multiset)
    euler_q = prod(Fraction(4 * q - 1, 4 * q) for q in q_multiset)
    assert euler_p == euler_q
    assert sum(p_multiset) != sum(q_multiset)

    result = {
        "schema": "amra.erdos635.r003-cycle-invariants.v1",
        "status": "PASS",
        "strict_invariants_for_every_fixed_A_cycle": [
            "sum_i p_i = sum_i q_i",
            (
                "product_i(1-1/(A*p_i)) = product_i h_i/A "
                "= product_i(1-1/(A*q_i))"
            ),
        ],
        "composite_nonbacktracking_counterwalk": composite,
        "composite_sorted_prefix_sum_differences": prefix_differences,
        "prime_immediate_return_control": prime_degenerate,
        "euler_product_only_collision": {
            "A": 4,
            "p_multiset": p_multiset,
            "q_multiset": q_multiset,
            "common_product": {
                "numerator": euler_p.numerator,
                "denominator": euler_p.denominator,
            },
            "sum_p": sum(p_multiset),
            "sum_q": sum(q_multiset),
        },
        "scope": (
            "The invariants are necessary and length-independent.  The "
            "counterexamples show they are not, by themselves, a proof that "
            "all fixed-A closed walks backtrack."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
