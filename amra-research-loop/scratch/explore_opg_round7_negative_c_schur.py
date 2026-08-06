#!/usr/bin/env python3
"""Discovery scan for the K-positive chamber with c<0.

Write q0,q3,q4>=0 and

    c = -tau*q0*q3*q4 /
        (q0*q3*q4 + q0*q3 + q0*q4 + q3*q4),  0<=tau<=1.

This is the exact Schur parametrization of the part of K>0 with c<=0.
For each P/L/R page-activity chamber, construct B^2 times the existing
cleared Delta polynomial and inspect tensor Bernstein coefficients in all
bounded variables.  This remains discovery code until selected identities
are frozen in an evidence verifier.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import comb
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
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)
from verify_nonnegative_route_chambers import state_polynomial  # noqa: E402


B_EDGE = (0, 4)
COUNT = 8
ZERO = (0,) * COUNT


def add(left, right, scale=1):
    scale = Fraction(scale)
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, Fraction()) + scale * coefficient
    return {m: c for m, c in result.items() if c}


def multiply(left, right):
    result = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            monomial = tuple(a + b for a, b in zip(lm, rm))
            result[monomial] = result.get(monomial, Fraction()) + lc * rc
    return {m: c for m, c in result.items() if c}


def constant(value):
    value = Fraction(value)
    return {} if not value else {ZERO: value}


def variable(slot):
    monomial = [0] * COUNT
    monomial[slot] = 1
    return {tuple(monomial): Fraction(1)}


def power(poly, exponent):
    result = constant(1)
    for _ in range(exponent):
        result = multiply(result, poly)
    return result


def lift(poly):
    return {monomial + (0,): Fraction(coefficient) for monomial, coefficient in poly.items()}


def route_q(state, index):
    first = variable(1 + 2 * index)
    second = variable(2 + 2 * index)
    if state == "P":
        return add(add(multiply(first, second), first), second)
    return first


def schur_substitute(poly, states):
    """Return B^2*poly(c=-tau*P/B), with tau in slot 7."""
    q0, q3, q4 = (route_q(state, index) for index, state in enumerate(states))
    P = multiply(multiply(q0, q3), q4)
    B = add(
        P,
        add(add(multiply(q0, q3), multiply(q0, q4)), multiply(q3, q4)),
    )
    tauP = multiply(variable(7), P)
    result = {}
    for monomial, coefficient in lift(poly).items():
        c_degree = monomial[0]
        assert c_degree <= 2
        base = list(monomial)
        base[0] = 0
        term = {tuple(base): coefficient * (-1 if c_degree % 2 else 1)}
        term = multiply(term, power(tauP, c_degree))
        term = multiply(term, power(B, 2 - c_degree))
        result = add(result, term)
    return result


def bernstein_transform(poly, bounded_slots, elevation=0):
    result = dict(poly)
    for slot in bounded_slots:
        degree = max((m[slot] for m in result), default=0) + elevation
        grouped = {}
        for monomial, coefficient in result.items():
            key = monomial[:slot] + monomial[slot + 1 :]
            grouped.setdefault(key, {})[monomial[slot]] = coefficient
        transformed = {}
        for key, coefficients in grouped.items():
            for index in range(degree + 1):
                value = sum(
                    coefficients.get(power_degree, 0)
                    * Fraction(comb(index, power_degree), comb(degree, power_degree))
                    for power_degree in range(index + 1)
                )
                if value:
                    monomial = key[:slot] + (index,) + key[slot:]
                    transformed[monomial] = value
        result = transformed
    return result


def scan(delta, states):
    original = state_polynomial(delta, states)
    poly = schur_substitute(original, states)
    bounded = [2 + 2 * index for index, state in enumerate(states) if state != "P"]
    bounded.append(7)
    rows = {}
    for elevation in (0, 2, 4, 8):
        transformed = bernstein_transform(poly, bounded, elevation)
        values = tuple(transformed.values())
        rows[elevation] = {
            "nonzero": len(values),
            "negative": sum(value < 0 for value in values),
            "zero": sum(value == 0 for value in values),
            "minimum": str(min(values)),
        }
    return {
        "state": "".join(states),
        "terms": len(poly),
        "negative_power": sum(value < 0 for value in poly.values()),
        "bernstein": rows,
    }


def main():
    deletion, connectivity, _, _ = reconstruct_original()
    a_slope = derivative(deletion, (B_EDGE,))
    c_zero = restrict_original_zero(deletion, B_EDGE)
    d_slope = derivative(connectivity, (B_EDGE,))
    e_zero = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(
        multiply_original(a_slope, e_zero),
        multiply_original(d_slope, c_zero),
        -1,
    )
    for states in product("PLR", repeat=3):
        print(scan(delta, states), flush=True)


if __name__ == "__main__":
    main()
