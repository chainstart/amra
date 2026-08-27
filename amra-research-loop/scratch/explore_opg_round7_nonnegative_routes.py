#!/usr/bin/env python3
"""Discovery-only exact sign scan on the nonnegative-route chamber.

For a length-two route with effective activity

    q = x_left*x_right + x_left + x_right >= 0,

at most one edge activity is negative because both edge floors are positive.
If x_left=-t with 0<=t<1, then x_right=(q+t)/(1-t).  This script clears a
square denominator for every such route and checks all 3^3 sign types using
only sparse integer polynomial arithmetic.  It is discovery code until any
useful output is frozen in a campaign verifier.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb
from itertools import product
from pathlib import Path
import sys


EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns"
    / "opg-1757-transverse-lift-round7"
    / "evidence"
)
sys.path.insert(0, str(EVIDENCE))

from verify_c_zero_fibre import (  # noqa: E402
    EDGES,
    add,
    derivative,
    multiply,
    reconstruct_original,
    restrict_original_zero,
)


B_EDGE = (0, 4)
C_EDGE = (1, 2)
ROUTES = (((0, 1), (0, 2)), ((1, 3), (2, 3)), ((1, 4), (2, 4)))


def local_multiply(left, right):
    result = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            monomial = tuple(a + b for a, b in zip(lm, rm))
            result[monomial] = result.get(monomial, 0) + lc * rc
    return {m: c for m, c in result.items() if c}


def variable(count, slot, coefficient=1):
    exponent = [0] * count
    exponent[slot] = 1
    return {tuple(exponent): coefficient}


def power(poly, exponent):
    count = len(next(iter(poly)))
    result = {(0,) * count: 1}
    for _ in range(exponent):
        result = local_multiply(result, poly)
    return result


def bernstein_coefficients(poly, states, elevation):
    bernstein = {monomial: Fraction(coefficient) for monomial, coefficient in poly.items()}
    for index, state in enumerate(states):
        if state == "P":
            continue
        slot = 2 + 2 * index
        degree = max(monomial[slot] for monomial in bernstein) + elevation
        grouped = {}
        for monomial, coefficient in bernstein.items():
            key = monomial[:slot] + monomial[slot + 1 :]
            grouped.setdefault(key, {})[monomial[slot]] = coefficient
        transformed = {}
        for key, power_coefficients in grouped.items():
            for bernstein_index in range(degree + 1):
                value = sum(
                    power_coefficients.get(power, 0)
                    * Fraction(comb(bernstein_index, power), comb(degree, power))
                    for power in range(bernstein_index + 1)
                )
                if not value:
                    continue
                monomial = key[:slot] + (bernstein_index,) + key[slot:]
                transformed[monomial] = value
        bernstein = transformed
    return tuple(bernstein.values())


def compactified_bernstein_coefficients(poly, states):
    """Tensor Bernstein coefficients after z=s/(1-s) compactification.

    Every slot except a negative-route t is an unbounded nonnegative
    variable.  Clearing its coordinatewise maximum denominator sends z^k to
    s^k(1-s)^(degree-k), a single Bernstein basis element.  Bounded t slots
    use the usual power-to-Bernstein triangular transform.
    """
    degrees = [max(monomial[slot] for monomial in poly) for slot in range(7)]
    bounded = {
        2 + 2 * index
        for index, state in enumerate(states)
        if state != "P"
    }
    tensor = {}
    for monomial, coefficient in poly.items():
        partial = {(): Fraction(coefficient)}
        for slot, power_degree in enumerate(monomial):
            degree = degrees[slot]
            expanded = {}
            if slot in bounded:
                choices = tuple(
                    (index, Fraction(comb(index, power_degree), comb(degree, power_degree)))
                    for index in range(power_degree, degree + 1)
                )
            else:
                choices = ((power_degree, Fraction(1, comb(degree, power_degree))),)
            for prefix, value in partial.items():
                for index, multiplier in choices:
                    expanded[prefix + (index,)] = (
                        expanded.get(prefix + (index,), Fraction()) + value * multiplier
                    )
            partial = expanded
        for index, value in partial.items():
            tensor[index] = tensor.get(index, Fraction()) + value
    # Missing tensor entries are zero and hence harmless.
    return degrees, tuple(value for value in tensor.values() if value)


def scan_state(delta, states):
    # Slots: c, then two variables for every route.  For P these are the two
    # nonnegative activities; for L/R they are q,t.
    count = 7
    zero = (0,) * count
    cvar = variable(count, 0)
    route_factors = []
    for index, state in enumerate(states):
        first = variable(count, 1 + 2 * index)
        second = variable(count, 2 + 2 * index)
        if state == "P":
            route_factors.append((first, second, None))
            continue
        q, t = first, second
        one_minus_t = {zero: 1, next(iter(t)): -1}
        q_plus_t = {**q}
        for monomial, coefficient in t.items():
            q_plus_t[monomial] = q_plus_t.get(monomial, 0) + coefficient
        # Tuple order is (left factor, right factor, cleared denominator).
        negative = {monomial: -coefficient for monomial, coefficient in t.items()}
        positive = q_plus_t
        if state == "L":
            route_factors.append((negative, positive, one_minus_t))
        else:
            route_factors.append((positive, negative, one_minus_t))

    result = {}
    for original_monomial, original_coefficient in delta.items():
        term = {zero: original_coefficient}
        c_degree = original_monomial[EDGES.index(C_EDGE)]
        term = local_multiply(term, power(cvar, c_degree))
        for state, edges, factors in zip(states, ROUTES, route_factors):
            left_degree = original_monomial[EDGES.index(edges[0])]
            right_degree = original_monomial[EDGES.index(edges[1])]
            left, right, denominator = factors
            term = local_multiply(term, power(left, left_degree))
            term = local_multiply(term, power(right, right_degree))
            if state != "P":
                # Delta has degree at most two in each original edge, so a
                # square clears every possible denominator of the positive
                # partner.  Only that partner carries a denominator.
                positive_degree = right_degree if state == "L" else left_degree
                term = local_multiply(term, power(denominator, 2 - positive_degree))
        for monomial, coefficient in term.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    result = {m: c for m, c in result.items() if c}
    coefficients = tuple(result.values())
    bernstein_by_elevation = {
        elevation: bernstein_coefficients(result, states, elevation)
        for elevation in (0, 2, 4, 8)
    }
    compact_degrees, compact_values = compactified_bernstein_coefficients(result, states)
    return {
        "state": "".join(states),
        "terms": len(result),
        "negative_coefficients": sum(coefficient < 0 for coefficient in coefficients),
        "minimum_coefficient": min(coefficients),
        "maximum_coefficient": max(coefficients),
        "bernstein": {
            elevation: {
                "negative": sum(coefficient < 0 for coefficient in values),
                "minimum": str(min(values)),
            }
            for elevation, values in bernstein_by_elevation.items()
        },
        "compactified_bernstein": {
            "degrees": compact_degrees,
            "nonzero": len(compact_values),
            "negative": sum(coefficient < 0 for coefficient in compact_values),
            "minimum": str(min(compact_values)),
        },
    }


def main():
    deletion, connectivity, _, _ = reconstruct_original()
    a_slope = derivative(deletion, (B_EDGE,))
    c_zero = restrict_original_zero(deletion, B_EDGE)
    d_slope = derivative(connectivity, (B_EDGE,))
    e_zero = restrict_original_zero(connectivity, B_EDGE)
    delta = add(multiply(a_slope, e_zero), multiply(d_slope, c_zero), -1)

    rows = [scan_state(delta, states) for states in product("PLR", repeat=3)]
    for row in rows:
        print(row)
    print({
        "all_power_nonnegative": all(not row["negative_coefficients"] for row in rows),
        "all_bernstein_elevation_8_nonnegative": all(
            not row["bernstein"][8]["negative"] for row in rows
        ),
    })


if __name__ == "__main__":
    main()
