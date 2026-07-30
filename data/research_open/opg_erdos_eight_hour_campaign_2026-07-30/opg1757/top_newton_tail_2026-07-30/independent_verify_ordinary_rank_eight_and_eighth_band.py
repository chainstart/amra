#!/usr/bin/env python3
"""Independent discovery/certificate for beta_(d,8) and gamma_(d,7).

No author rank-eight verifier or stored author rank-eight coefficient
table is imported.  Exact values come directly from the previously
audited finite-profile primitive and are reconstructed with defining
Lagrange products.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from functools import lru_cache

import sympy as sp

from independent_verify_all_fixed_rank_ordinary_symbol_algorithm import (
    D as PROFILE_D,
    exact_ordinary_value,
)
from independent_verify_ordinary_rank_seven_and_seventh_band import (
    COUNT,
    exact_lagrange_polynomial,
    polynomial_binomial,
    rank_seven_polynomial,
    signed_stirling_rows,
)
from independent_verify_ordinary_rank_six_symbol import (
    rank_six_polynomial,
)
from independent_verify_ordinary_sixth_long_recurrence_band import (
    printed_lower_rank_symbols,
)


DEPTH = sp.symbols("rank8_depth", integer=True)
PAGE = sp.symbols("rank8_page")
SHIFT = sp.symbols("rank8_shift", integer=True, nonnegative=True)

RANK_EIGHT_DENOMINATOR = sp.Integer(16395969401293614612480000)
RANK_EIGHT_COEFFICIENTS = (
    889430541350,
    14622142134600,
    548021093858420,
    -2856959481810720,
    28701596207603462,
    -1423489168742166240,
    12861217758561559244,
    -82998625358866417200,
    922977463212725257961,
    -8177441437699868025120,
    42938933142825418811336,
    -76677846419551695275328,
    -511184340302410319000404,
    3899371073189547912083712,
    -37899401549116356635663992,
    491762300999382375736137936,
    -3768699654323965134722976313,
    18306948644611241354070999096,
    -76768891977718913728168749960,
    337541647224593255540675147712,
    -1258527065761592686759918183056,
    3449860233699583645836821626752,
    -7267027629287109649368128456448,
    11300732071776760453999392614400,
    -9638644787509862596194526003200,
)
EIGHTH_BAND_DENOMINATOR = sp.Integer(113860898620094545920000)
EIGHTH_BAND_SHIFTED_COEFFICIENTS = (
    1561601241389666024275,
    378257654066055578742200,
    43399151014977476474715960,
    3137341234190203371435584480,
    160345102804655406389036745460,
    6162432321193972015605848689540,
    184930471488563387807542380122350,
    4441537634902915859699052686640620,
    86810758260458031410774898153155334,
    1396506238942381836020155538489736680,
    18627223852830009296590007747380961716,
    206892528211131527712409474560588414712,
    1916590565131653997450556325484105603348,
    14795096556097939423935444403243192448948,
    94848423278978965804367181698045318803998,
    501854322963927159548511227603583584664956,
    2170848974618952759804845680663967943292447,
    7571820422883198432491827526054561127879784,
    20880363921400777632652337367622449796361496,
    44244355779537170896799258677444794474104832,
    69010100928202046265813651364774426539617136,
    73917818536575003240583435087381568243730048,
    47854944406348979688454154428638998068366080,
    13762189506637017969286097171436879613132800,
)
FIRST_EIGHTH_BAND_VALUE = sp.Rational(
    2631644430366587366723616427, 21772800
)
EXPECTED_NEWTON_DENOMINATOR = (
    sp.Integer(17176032226397484747055763030016000000)
    * DEPTH**2
    * (DEPTH - 7)
    * (DEPTH - 6) ** 2
    * (DEPTH - 5) ** 2
    * (DEPTH - 4) ** 2
    * (DEPTH - 3) ** 2
    * (DEPTH - 2) ** 2
    * (DEPTH - 1) ** 2
)
EXPECTED_C3_DENOMINATOR = (
    sp.Integer(406646066500337664000)
    * DEPTH
    * (DEPTH - 7)
    * (DEPTH - 6)
    * (DEPTH - 5)
    * (DEPTH - 4)
    * (DEPTH - 3)
    * (DEPTH - 2)
    * (DEPTH - 1)
)
EXPECTED_HASHES = {
    "beta8_shift": (
        "fc42182bba415d93e3fc8ccece107311"
        "ab457b775be06240e9990ae2a017607d"
    ),
    "newton_shift": (
        "3beb8729bdbb110c7694c3da5b56b4"
        "f38cce48bfa23ffe90b9976df45b5bf2c3"
    ),
    "c3_shift": (
        "cc81f974a0d321000b5ed3a69a9e040"
        "a95240db41da897937573ccfe37826b87"
    ),
    "gamma7_shift": (
        "433f384ada20eaa4a9ea9869d8057e98"
        "a51ff2f6d3f0f195a2e55530badae019"
    ),
}


def descending_polynomial(coefficients, variable):
    degree = len(coefficients) - 1
    return sum(
        sp.Integer(coefficient) * variable ** (degree - index)
        for index, coefficient in enumerate(coefficients)
    )


def rank_eight_polynomial(variable=DEPTH):
    return descending_polynomial(
        RANK_EIGHT_COEFFICIENTS, variable
    ) / RANK_EIGHT_DENOMINATOR


def coefficient_hash(coefficients):
    payload = ",".join(str(value) for value in coefficients)
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def positive_shift_coefficients(expression, shift):
    numerator = sp.cancel(expression).as_numer_denom()[0]
    coefficients = tuple(
        int(value)
        for value in sp.Poly(
            sp.expand(numerator.subs(DEPTH, SHIFT + shift)),
            SHIFT,
        ).all_coeffs()
    )
    assert all(value > 0 for value in coefficients)
    return coefficients


@lru_cache(maxsize=None)
def independently_generated_rank_eight_value(depth: int):
    if depth < 8:
        raise ValueError("rank eight requires depth >= 8")
    start = max(2, (depth + 5) // 2) + 2
    points = []
    for page_count in range(start, start + depth + 1):
        value: Fraction = exact_ordinary_value(page_count, depth)
        points.append(
            (
                page_count,
                sp.Rational(value.numerator, value.denominator),
            )
        )
    polynomial = exact_lagrange_polynomial(points, PAGE)
    assert polynomial.degree() == depth
    assert polynomial.LC() == 1
    for page_count in (start - 1, start + depth + 1):
        value: Fraction = exact_ordinary_value(page_count, depth)
        assert polynomial.eval(page_count) == sp.Rational(
            value.numerator, value.denominator
        )
    return polynomial.coeff_monomial(PAGE ** (depth - 8))


@lru_cache(maxsize=1)
def reconstruct_rank_eight():
    interpolation_depths = tuple(range(9, 34))
    holdout_depths = (8, 34, 35, 36)
    points = tuple(
        (
            depth,
            independently_generated_rank_eight_value(depth),
        )
        for depth in interpolation_depths
    )
    polynomial = exact_lagrange_polynomial(points, DEPTH)
    assert polynomial.degree() == 24
    for depth in holdout_depths:
        assert polynomial.eval(depth) == (
            independently_generated_rank_eight_value(depth)
        )
    return polynomial, interpolation_depths, holdout_depths


@lru_cache(maxsize=1)
def derive_triangles():
    beta = printed_lower_rank_symbols(DEPTH) + [
        rank_six_polynomial(DEPTH),
        rank_seven_polynomial(DEPTH),
        rank_eight_polynomial(DEPTH),
    ]
    assert len(beta) == 9
    assert all(PROFILE_D not in expression.free_symbols for expression in beta)
    stirling = signed_stirling_rows(8)

    h_rows = [sp.Integer(1)]
    for loss in range(1, 9):
        ordinary_coefficient = sum(
            beta[rank]
            * polynomial_binomial(DEPTH - rank, loss - rank)
            * 2 ** (loss - rank)
            for rank in range(loss + 1)
        )
        correction = sum(
            h_rows[row]
            * stirling[loss - row].subs(COUNT, DEPTH - row)
            for row in range(loss)
        )
        h_rows.append(
            sp.factor(
                sp.cancel(
                    sp.expand(ordinary_coefficient - correction)
                )
            )
        )

    bands = []
    for band in range(8):
        value = (
            h_rows[band + 1]
            - h_rows[band + 1].subs(DEPTH, DEPTH + 1)
        )
        value -= sum(
            bands[lower_band]
            * h_rows[band - lower_band].subs(
                DEPTH, DEPTH - 1 - 2 * lower_band
            )
            for lower_band in range(band)
        )
        bands.append(
            sp.factor(sp.cancel(sp.expand(value)))
        )
    return tuple(h_rows), tuple(bands)


@lru_cache(maxsize=1)
def audit():
    assert DEPTH != PROFILE_D
    polynomial, interpolation_depths, holdout_depths = (
        reconstruct_rank_eight()
    )
    beta8 = sp.cancel(polynomial.as_expr())
    printed_beta8 = sp.cancel(rank_eight_polynomial(DEPTH))
    assert sp.cancel(beta8 - printed_beta8) == 0
    beta8_numerator, beta8_denominator = (
        printed_beta8.as_numer_denom()
    )
    assert beta8_denominator == RANK_EIGHT_DENOMINATOR
    assert sp.expand(beta8_numerator) == descending_polynomial(
        RANK_EIGHT_COEFFICIENTS, DEPTH
    )
    beta8_shift = positive_shift_coefficients(printed_beta8, 8)
    assert len(beta8_shift) == 25
    assert coefficient_hash(beta8_shift) == EXPECTED_HASHES[
        "beta8_shift"
    ]

    beta6 = rank_six_polynomial(DEPTH)
    beta7 = rank_seven_polynomial(DEPTH)
    a6 = beta6 / polynomial_binomial(DEPTH, 6)
    a7 = -beta7 / polynomial_binomial(DEPTH, 7)
    a8 = printed_beta8 / polynomial_binomial(DEPTH, 8)
    assert positive_shift_coefficients(a8, 8)

    newton = sp.cancel(a7**2 - a6 * a8)
    newton_numerator, newton_denominator = newton.as_numer_denom()
    assert sp.factor(newton_denominator) == sp.factor(
        EXPECTED_NEWTON_DENOMINATOR
    )
    newton_shift = positive_shift_coefficients(newton, 8)
    assert len(newton_shift) == 44
    assert coefficient_hash(newton_shift) == EXPECTED_HASHES[
        "newton_shift"
    ]

    c3_gap = sp.cancel((3 * DEPTH**2) ** 8 - a8)
    c3_numerator, c3_denominator = c3_gap.as_numer_denom()
    assert sp.factor(c3_denominator) == sp.factor(
        EXPECTED_C3_DENOMINATOR
    )
    c3_shift = positive_shift_coefficients(c3_gap, 8)
    assert len(c3_shift) == 25
    assert coefficient_hash(c3_shift) == EXPECTED_HASHES["c3_shift"]

    h_rows, bands = derive_triangles()
    gamma7 = sp.cancel(bands[7])
    gamma_numerator, gamma_denominator = gamma7.as_numer_denom()
    assert gamma_denominator == EIGHTH_BAND_DENOMINATOR
    assert sp.Poly(gamma7, DEPTH).degree() == 23
    gamma_shift = tuple(
        int(value)
        for value in sp.Poly(
            sp.expand(gamma_numerator.subs(DEPTH, SHIFT + 15)),
            SHIFT,
        ).all_coeffs()
    )
    assert gamma_shift == EIGHTH_BAND_SHIFTED_COEFFICIENTS
    assert all(value > 0 for value in gamma_shift)
    assert coefficient_hash(gamma_shift) == EXPECTED_HASHES[
        "gamma7_shift"
    ]
    assert sp.rem(gamma_numerator, DEPTH - 14, DEPTH) == 0
    assert gamma7.subs(DEPTH, 15) == FIRST_EIGHTH_BAND_VALUE

    h8 = sp.cancel(h_rows[8])
    forced_factor = sp.prod(DEPTH - root for root in range(8, 16))
    h8_quotient = sp.cancel(h8 / forced_factor)
    quotient_numerator, quotient_denominator = (
        h8_quotient.as_numer_denom()
    )
    assert sp.cancel(h8 - forced_factor * h8_quotient) == 0
    assert all(h8.subs(DEPTH, root) == 0 for root in range(8, 16))
    roots_are_simple = (
        sp.gcd(
            sp.Poly(quotient_numerator, DEPTH),
            sp.Poly(forced_factor, DEPTH),
        ).degree()
        == 0
    )
    assert roots_are_simple

    boundary_calls = tuple(
        (lower_band, 14 - 2 * lower_band, 7 - lower_band)
        for lower_band in range(7)
    )
    assert all(depth == 2 * row for _, depth, row in boundary_calls)

    return {
        "schema": (
            "amra.opg1757.rank-eight-eighth-band."
            "independent-certificate.v1"
        ),
        "status": "PASS",
        "author_rank_eight_verifier_imported": False,
        "common_axiom_layer": [
            "all-rank degree(beta_(d,8)) <= 24",
            "audited exact_ordinary_value finite-profile primitive",
            "independently audited beta_(d,0..7)",
        ],
        "rank_eight": {
            "degree": polynomial.degree(),
            "interpolation_depths": list(interpolation_depths),
            "holdout_depths": list(holdout_depths),
            "denominator": str(beta8_denominator),
            "coefficients": list(RANK_EIGHT_COEFFICIENTS),
            "shifted_coefficients": list(beta8_shift),
            "shifted_sha256": coefficient_hash(beta8_shift),
            "all_shifted_coefficients_positive": True,
        },
        "seventh_normalized_newton": {
            "claim": "a_(d,7)^2 > a_(d,6)*a_(d,8)",
            "denominator": str(sp.factor(newton_denominator)),
            "shifted_coefficient_count": len(newton_shift),
            "shifted_coefficients": list(newton_shift),
            "shifted_sha256": coefficient_hash(newton_shift),
        },
        "rank_eight_c3": {
            "claim": "0 < a_(d,8) < (3*d^2)^8",
            "denominator": str(sp.factor(c3_denominator)),
            "shifted_coefficient_count": len(c3_shift),
            "shifted_coefficients": list(c3_shift),
            "shifted_sha256": coefficient_hash(c3_shift),
        },
        "eighth_band": {
            "claim": "gamma_(d,7) > 0 for d >= 15",
            "degree": 23,
            "denominator": str(gamma_denominator),
            "shifted_coefficients": list(gamma_shift),
            "shifted_sha256": coefficient_hash(gamma_shift),
            "first_admissible_value": str(
                gamma7.subs(DEPTH, 15)
            ),
            "forced_factor": "rank8_depth-14",
            "h8_forced_roots": list(range(8, 16)),
            "h8_forced_roots_are_simple": roots_are_simple,
            "h8_quotient_denominator": str(quotient_denominator),
            "boundary_lower_calls": [
                list(item) for item in boundary_calls
            ],
        },
    }


def main():
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
