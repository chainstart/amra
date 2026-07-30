#!/usr/bin/env python3
"""Exact certificate for beta_(d,8) and gamma_(d,7)."""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache

import sympy as sp

from independent_verify_all_fixed_rank_ordinary_symbol_algorithm import (
    D,
    K,
    exact_ordinary_polynomial,
)
from independent_verify_ordinary_rank_six_symbol import (
    normalized_symbols,
    rank_six_polynomial,
)
from verify_ordinary_first_five_long_recurrence_bands import (
    D as TRIANGLE_D,
    N as TRIANGLE_N,
    beta_polynomials,
    signed_stirling_near_diagonal,
)
from verify_ordinary_rank_seven_and_seventh_band import (
    rank_seven_polynomial,
)


U = sp.symbols("u")

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


def digest(coefficients) -> str:
    payload = ",".join(str(value) for value in coefficients)
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def shifted_reduced(expression, shift):
    numerator, denominator = sp.cancel(
        expression
    ).as_numer_denom()
    if denominator.could_extract_minus_sign():
        numerator, denominator = -numerator, -denominator
    coefficients = tuple(
        int(value)
        for value in sp.Poly(
            sp.expand(numerator.subs(D, U + shift)),
            U,
        ).all_coeffs()
    )
    return numerator, denominator, coefficients


def rank_eight_polynomial(variable=D):
    return sum(
        coefficient * variable ** (24 - index)
        for index, coefficient in enumerate(RANK_EIGHT_COEFFICIENTS)
    ) / RANK_EIGHT_DENOMINATOR


def expected_eighth_band(variable=D):
    shifted = variable - 15
    return sum(
        coefficient * shifted ** (23 - index)
        for index, coefficient in enumerate(
            EIGHTH_BAND_SHIFTED_COEFFICIENTS
        )
    ) / EIGHTH_BAND_DENOMINATOR


def exact_rank_eight_value(depth):
    ordinary = exact_ordinary_polynomial(depth)
    return ordinary.coeff_monomial(K ** (depth - 8))


def derive_through_eighth_band():
    beta = [
        expression.subs(TRIANGLE_D, D)
        for expression in beta_polynomials()
    ] + [
        rank_six_polynomial(D),
        rank_seven_polynomial(D),
        rank_eight_polynomial(D),
    ]
    stirling = signed_stirling_near_diagonal(8)
    falling_rows = [sp.Integer(1)]
    for loss in range(1, 9):
        monomial_coefficient = sum(
            beta[rank]
            * sp.prod(
                D - rank - offset
                for offset in range(loss - rank)
            )
            / sp.factorial(loss - rank)
            * 2 ** (loss - rank)
            for rank in range(loss + 1)
        )
        falling_rows.append(
            sp.factor(
                monomial_coefficient
                - sum(
                    falling_rows[index]
                    * stirling[loss - index].subs(
                        TRIANGLE_N, D - index
                    )
                    for index in range(loss)
                )
            )
        )

    bands = []
    for band in range(8):
        value = (
            falling_rows[band + 1]
            - falling_rows[band + 1].subs(D, D + 1)
        )
        value -= sum(
            bands[index]
            * falling_rows[band - index].subs(
                D,
                D - 1 - 2 * index,
            )
            for index in range(band)
        )
        bands.append(sp.factor(value))
    return falling_rows, bands


@lru_cache(maxsize=1)
def audit():
    values = [
        (depth, exact_rank_eight_value(depth))
        for depth in range(8, 37)
    ]
    interpolated = sp.Poly(sp.interpolate(values[:25], D), D)
    expected_rank_eight = rank_eight_polynomial(D)
    assert interpolated.degree() == 24
    assert sp.simplify(
        interpolated.as_expr() - expected_rank_eight
    ) == 0
    assert all(
        interpolated.eval(depth) == value
        for depth, value in values[25:]
    )

    _, rank_eight_denominator, rank_eight_shift = shifted_reduced(
        expected_rank_eight, 8
    )
    assert rank_eight_denominator == RANK_EIGHT_DENOMINATOR
    assert len(rank_eight_shift) == 25
    assert all(value > 0 for value in rank_eight_shift)
    assert digest(rank_eight_shift) == (
        "fc42182bba415d93e3fc8ccece107311"
        "ab457b775be06240e9990ae2a017607d"
    )

    _, _, a6 = normalized_symbols()
    a7 = (
        sp.factorial(7)
        * (-rank_seven_polynomial(D))
        / sp.prod(D - offset for offset in range(7))
    )
    a8 = (
        sp.factorial(8)
        * expected_rank_eight
        / sp.prod(D - offset for offset in range(8))
    )
    _, newton_denominator, newton_shift = shifted_reduced(
        a7**2 - a6 * a8, 8
    )
    assert len(newton_shift) == 44
    assert all(value > 0 for value in newton_shift)
    assert digest(newton_shift) == (
        "3beb8729bdbb110c7694c3da5b56b4f"
        "38cce48bfa23ffe90b9976df45b5bf2c3"
    )

    _, c3_denominator, c3_shift = shifted_reduced(
        (3 * D**2) ** 8 - a8, 8
    )
    assert len(c3_shift) == 25
    assert all(value > 0 for value in c3_shift)
    assert digest(c3_shift) == (
        "cc81f974a0d321000b5ed3a69a9e040a"
        "95240db41da897937573ccfe37826b87"
    )

    falling_rows, bands = derive_through_eighth_band()
    eighth = sp.cancel(bands[7])
    expected = expected_eighth_band(D)
    assert sp.simplify(eighth - expected) == 0
    assert sp.Poly(eighth, D).degree() == 23
    numerator, denominator, shifted = shifted_reduced(eighth, 15)
    assert denominator == EIGHTH_BAND_DENOMINATOR
    assert shifted == EIGHTH_BAND_SHIFTED_COEFFICIENTS
    assert all(value > 0 for value in shifted)
    assert digest(shifted) == (
        "433f384ada20eaa4a9ea9869d8057e98"
        "a51ff2f6d3f0f195a2e55530badae019"
    )
    assert sp.rem(numerator, D - 14, D) == 0

    falling_numerator = sp.cancel(
        falling_rows[8]
    ).as_numer_denom()[0]
    forced_falling = sp.prod(D - root for root in range(8, 16))
    assert sp.rem(falling_numerator, forced_falling, D) == 0

    return {
        "schema": (
            "amra.opg1757.ordinary-rank-eight-and-"
            "eighth-long-band.v1"
        ),
        "status": "PASS",
        "rank_eight": {
            "degree_bound_source": (
                "ALL_RANK_ORDINARY_SYMBOL_DEGREE_THEOREM.md"
            ),
            "interpolation_depths": list(range(8, 33)),
            "holdout_depths": list(range(33, 37)),
            "value_source": (
                "exact_ordinary_polynomial(depth), coefficient "
                "of k^(depth-8)"
            ),
            "degree": 24,
            "denominator": int(RANK_EIGHT_DENOMINATOR),
            "shift": "d=u+8",
            "shifted_numerator_coefficients": list(
                rank_eight_shift
            ),
            "shifted_coefficient_sha256": digest(
                rank_eight_shift
            ),
            "seventh_normalized_newton": {
                "claim": "a_(d,7)^2 > a_(d,6)*a_(d,8)",
                "reduced_denominator": str(
                    sp.factor(newton_denominator)
                ),
                "shifted_reduced_numerator_coefficients": list(
                    newton_shift
                ),
                "shifted_coefficient_sha256": digest(
                    newton_shift
                ),
            },
            "rank_eight_C3_bound": {
                "claim": "a_(d,8) < (3*d^2)^8",
                "reduced_denominator": str(
                    sp.factor(c3_denominator)
                ),
                "shifted_reduced_numerator_coefficients": list(
                    c3_shift
                ),
                "shifted_coefficient_sha256": digest(c3_shift),
            },
        },
        "eighth_band": {
            "band": 7,
            "minimum_depth": 15,
            "degree": 23,
            "denominator": int(EIGHTH_BAND_DENOMINATOR),
            "shift": "d=u+15",
            "shifted_numerator_coefficients": list(shifted),
            "shifted_coefficient_sha256": digest(shifted),
            "all_shifted_coefficients_positive": True,
            "forced_factor": "d-14",
            "first_admissible_value": str(eighth.subs(D, 15)),
            "falling_row_eight_forced_roots": list(range(8, 16)),
        },
        "symbol_unification": (
            "Every lower beta polynomial is explicitly substituted "
            "from TRIANGLE_D to the independent symbol D."
        ),
    }


def main():
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
