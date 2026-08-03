#!/usr/bin/env python3
"""Exact four-channel orientation/Fourier reduction (stdlib only)."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json

from verify_c_zero_fibre import (
    EDGES,
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)


B_EDGE = (0, 4)
NAMES = ("p0", "p3", "p4", "d0", "d3", "d4", "q0", "q3", "q4", "c")
COUNT = len(NAMES)
ZERO = (0,) * COUNT


def add(left, right, scale=1):
    scale = Fraction(scale)
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, Fraction()) + scale * coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def multiply(left, right):
    result = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b in zip(left_monomial, right_monomial))
            result[monomial] = (
                result.get(monomial, Fraction()) + left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return {monomial: scalar * coefficient for monomial, coefficient in poly.items() if scalar}


def constant(value):
    value = Fraction(value)
    return {} if not value else {ZERO: value}


def variable(name, coefficient=1):
    monomial = [0] * COUNT
    monomial[NAMES.index(name)] = 1
    return {tuple(monomial): Fraction(coefficient)}


def power(poly, exponent):
    result = constant(1)
    for _ in range(exponent):
        result = multiply(result, poly)
    return result


def substitute_original(poly, factors):
    result = {}
    for original_monomial, coefficient in poly.items():
        term = constant(coefficient)
        for edge, degree in zip(EDGES, original_monomial):
            if degree:
                term = multiply(term, power(factors[edge], degree))
        result = add(result, term)
    return result


def quotient_reduce(poly, squares):
    """Reduce by d_i^2=S_i for the three orientation differences."""
    result = {}
    difference_slots = tuple(NAMES.index(name) for name in ("d0", "d3", "d4"))
    for monomial, coefficient in poly.items():
        base = list(monomial)
        term = constant(coefficient)
        for name, slot in zip(("0", "3", "4"), difference_slots):
            quotient, remainder = divmod(base[slot], 2)
            base[slot] = remainder
            if quotient:
                term = multiply(term, power(squares[name], quotient))
        term = multiply(term, {tuple(base): Fraction(1)})
        result = add(result, term)
    return result


def canonical(poly):
    return json.dumps(
        [
            [list(monomial), coefficient.numerator, coefficient.denominator]
            for monomial, coefficient in sorted(poly.items())
        ],
        separators=(",", ":"),
    )


def digest(poly):
    return sha256(canonical(poly).encode()).hexdigest()


def support(poly, names):
    slots = tuple(NAMES.index(name) for name in names)
    return sorted({tuple(monomial[slot] for slot in slots) for monomial in poly})


def F(pi, pj, qk, c):
    return add(
        scale(
            multiply(
                multiply(c, qk),
                add(add(pi, pj), scale(multiply(pi, pj), Fraction(1, 2))),
            ),
            1,
        ),
        multiply(add(c, qk), multiply(pi, pj)),
    )


def main():
    deletion, connectivity, forest_count, connected_count = reconstruct_original()
    assert (forest_count, connected_count) == (128, 58)
    a_slope = derivative(deletion, (B_EDGE,))
    c_zero = restrict_original_zero(deletion, B_EDGE)
    d_slope = derivative(connectivity, (B_EDGE,))
    e_zero = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(
        multiply_original(a_slope, e_zero),
        multiply_original(d_slope, c_zero),
        -1,
    )

    p = {name: variable(f"p{name}") for name in ("0", "3", "4")}
    d = {name: variable(f"d{name}") for name in ("0", "3", "4")}
    q = {name: variable(f"q{name}") for name in ("0", "3", "4")}
    c = variable("c")
    half = Fraction(1, 2)
    factors = {
        (0, 1): scale(add(p["0"], d["0"]), half),
        (0, 2): scale(add(p["0"], d["0"], -1), half),
        B_EDGE: {},
        (1, 2): c,
        (1, 3): scale(add(p["3"], d["3"]), half),
        (2, 3): scale(add(p["3"], d["3"], -1), half),
        (1, 4): scale(add(p["4"], d["4"]), half),
        (2, 4): scale(add(p["4"], d["4"], -1), half),
    }
    raw = substitute_original(delta, factors)
    squares = {
        name: add(add(power(p[name], 2), scale(p[name], 4)), scale(q[name], -4))
        for name in ("0", "3", "4")
    }
    reduced = quotient_reduce(raw, squares)
    assert support(reduced, ("d0", "d3", "d4")) == [
        (0, 0, 0),
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
    ]

    A = add(
        multiply(multiply(q["0"], q["3"]), q["4"]),
        multiply(
            c,
            add(
                add(multiply(q["0"], q["3"]), multiply(q["0"], q["4"])),
                add(
                    multiply(q["3"], q["4"]),
                    multiply(multiply(q["0"], q["3"]), q["4"]),
                ),
            ),
        ),
    )
    F03 = F(p["0"], p["3"], q["4"], c)
    F04 = F(p["0"], p["4"], q["3"], c)
    F34 = F(p["3"], p["4"], q["0"], c)
    U0 = add(
        add(
            scale(multiply(multiply(multiply(c, p["0"]), p["3"]), p["4"]), Fraction(1, 4)),
            multiply(multiply(p["0"], p["3"]), p["4"]),
        ),
        multiply(
            c,
            add(
                add(multiply(p["3"], p["4"]), multiply(p["0"], p["4"])),
                multiply(p["0"], p["3"]),
            ),
        ),
    )
    W0 = add(F34, scale(U0, -2))
    k03 = scale(multiply(c, q["4"]), half)
    k04 = scale(multiply(c, q["3"]), half)
    alpha = {
        "000": add(multiply(F03, F04), multiply(A, W0)),
        "110": add(multiply(k03, F04), scale(multiply(multiply(A, c), p["4"]), -half)),
        "101": add(multiply(k04, F03), scale(multiply(multiply(A, c), p["3"]), -half)),
        "011": add(
            multiply(multiply(k03, k04), squares["0"]),
            scale(
                multiply(multiply(A, c), add(q["0"], p["0"], -1)),
                half,
            ),
        ),
    }
    four_channel = alpha["000"]
    for key, monomial in (
        ("110", multiply(d["0"], d["3"])),
        ("101", multiply(d["0"], d["4"])),
        ("011", multiply(d["3"], d["4"])),
    ):
        four_channel = add(four_channel, multiply(alpha[key], monomial))
    assert reduced == four_channel

    # For fixed magnitudes D_i=sqrt(S_i), the four distinct edge-swap values
    # are the Hadamard eigenvalues of a 4x4 group-circulant matrix.  Congruence
    # by diag(1,sqrt(S0*S3),sqrt(S0*S4),sqrt(S3*S4)) removes every radical.
    g03 = multiply(squares["0"], squares["3"])
    g04 = multiply(squares["0"], squares["4"])
    g34 = multiply(squares["3"], squares["4"])
    triple = multiply(multiply(squares["0"], squares["3"]), squares["4"])
    polynomial_matrix = [
        [alpha["000"], multiply(alpha["110"], g03), multiply(alpha["101"], g04), multiply(alpha["011"], g34)],
        [multiply(alpha["110"], g03), multiply(alpha["000"], g03), multiply(alpha["011"], triple), multiply(alpha["101"], triple)],
        [multiply(alpha["101"], g04), multiply(alpha["011"], triple), multiply(alpha["000"], g04), multiply(alpha["110"], triple)],
        [multiply(alpha["011"], g34), multiply(alpha["101"], triple), multiply(alpha["110"], triple), multiply(alpha["000"], g34)],
    ]
    assert all(polynomial_matrix[row][column] == polynomial_matrix[column][row]
               for row in range(4) for column in range(4))

    records = {"raw_sum_difference": raw, "quotient_reduced": reduced, **{
        f"alpha_{name}": poly for name, poly in alpha.items()
    }}
    print(json.dumps({
        "schema": "amra.opg1757.round7.orientation-fourier.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
        },
        "coordinates": {
            "activities": "x_iL=(p_i+d_i)/2, x_iR=(p_i-d_i)/2",
            "route_relation": "d_i^2=p_i^2+4*p_i-4*q_i=:S_i",
            "edge_floor_domain": "S_i>=0 and p_i+2>0",
        },
        "four_channel": {
            "formula": "Delta_b=alpha000+alpha110*d0*d3+alpha101*d0*d4+alpha011*d3*d4",
            "orientation_support": ["000", "011", "101", "110"],
            "raw_terms": len(raw),
            "quotient_terms": len(reduced),
        },
        "fourier_matrix": {
            "distinct_swap_values": 4,
            "normalized_eigenvalues": "alpha000+eps*alpha110*D0*D3+eta*alpha101*D0*D4+eps*eta*alpha011*D3*D4",
            "characters": [[1, 1], [1, -1], [-1, 1], [-1, -1]],
            "polynomial_congruence_diagonal": ["1", "sqrt(S0*S3)", "sqrt(S0*S4)", "sqrt(S3*S4)"],
            "polynomial_matrix_entry_term_counts": [
                [len(entry) for entry in row] for row in polynomial_matrix
            ],
            "remaining_target": "prove the polynomially congruent 4x4 matrix positive semidefinite on K>0 and the edge-floor domain",
        },
        "records": {
            name: {"terms": len(poly), "sha256": digest(poly)}
            for name, poly in records.items()
        },
        "scope": "exact orientation quotient and PSD-equivalent interface; matrix positivity and generic Delta_b sign remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
