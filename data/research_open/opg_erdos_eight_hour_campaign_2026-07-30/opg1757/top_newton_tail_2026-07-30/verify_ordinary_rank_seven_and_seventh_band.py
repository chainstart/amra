#!/usr/bin/env python3
"""Exact certificate for beta_(d,7) and gamma_(d,6).

The rank-seven symbol is reconstructed from exact fixed-depth ordinary
profiles, using the proved all-rank degree bound only after the values
have been computed.  Four additional depths are holdouts.  The seventh
long-recurrence band is then derived through the exact two triangles.
"""

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


U = sp.symbols("u")

RANK_SEVEN_DENOMINATOR = sp.Integer(2189632665771048960000)
RANK_SEVEN_COEFFICIENTS = (
    30217328900,
    588271610850,
    13643387596300,
    -13878287091900,
    -206865593275440,
    -13510109661967215,
    72376793545393304,
    23072778779075520,
    639389903532886168,
    -17666060968351929996,
    84496255105723314960,
    489445758683198578404,
    -5864687888148553029676,
    15666213093792343586097,
    -42538398347646927587972,
    643254880572068718227472,
    -3764530202112123124432752,
    10480876675598477563463664,
    -26911510436413086105307392,
    76861878762263173992232704,
    -137796321367666244115302400,
    129244798226101901724057600,
)

SEVENTH_BAND_DENOMINATOR = sp.Integer(121646259209502720000)
SEVENTH_BAND_SHIFTED_COEFFICIENTS = (
    3271787244462017050,
    623648042617358143000,
    55856875934329452263050,
    3124374449017856908566000,
    122355759286004351589595575,
    3564341289917374275903469920,
    80099132802493969498884814000,
    1421058904493630987185394627680,
    20200960399253804993196252363940,
    232183805877904273159570354721976,
    2167537096961864786157429994245990,
    16446364861467480300030466642161360,
    101115582702312578695739865178530355,
    500203837038278678128508374054816528,
    1967490179042233169037740486691569800,
    6042615980557589009769445887708502560,
    14099566784784874077474835182924882480,
    23963972915208111433458538784014037376,
    27687602384655981572175962384529653760,
    19132079682860615978089318293170457600,
    5797589639494004327761299341549568000,
)


def rank_seven_polynomial(variable=D):
    numerator = sum(
        coefficient * variable ** (21 - index)
        for index, coefficient in enumerate(
            RANK_SEVEN_COEFFICIENTS
        )
    )
    return -numerator / RANK_SEVEN_DENOMINATOR


def expected_seventh_band(variable=D):
    shifted = variable - 13
    numerator = sum(
        coefficient * shifted ** (20 - index)
        for index, coefficient in enumerate(
            SEVENTH_BAND_SHIFTED_COEFFICIENTS
        )
    )
    return numerator / SEVENTH_BAND_DENOMINATOR


def exact_rank_seven_value(depth: int):
    """Extract beta_(depth,7) from the original exact depth profile."""

    ordinary = exact_ordinary_polynomial(depth)
    return ordinary.coeff_monomial(K ** (depth - 7))


def derive_through_seventh_band():
    """Rebuild h_0,...,h_7 and gamma_0,...,gamma_6 exactly."""

    beta = [
        expression.subs(TRIANGLE_D, D)
        for expression in beta_polynomials()
    ] + [
        rank_six_polynomial(D),
        rank_seven_polynomial(D),
    ]
    stirling = signed_stirling_near_diagonal(7)

    falling_rows = [sp.Integer(1)]
    for loss in range(1, 8):
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
    for band in range(7):
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
def audit() -> dict[str, object]:
    values = [
        (depth, exact_rank_seven_value(depth))
        for depth in range(7, 33)
    ]

    interpolated = sp.Poly(
        sp.interpolate(values[:22], D),
        D,
    )
    expected_rank_seven = rank_seven_polynomial(D)
    assert interpolated.degree() == 21
    assert sp.simplify(
        interpolated.as_expr() - expected_rank_seven
    ) == 0
    assert all(
        interpolated.eval(depth) == value
        for depth, value in values[22:]
    )

    rank_seven_numerator = sp.cancel(
        -expected_rank_seven
    ).as_numer_denom()[0]
    rank_seven_shift = tuple(
        int(value)
        for value in sp.Poly(
            sp.expand(rank_seven_numerator.subs(D, U + 7)),
            U,
        ).all_coeffs()
    )
    assert len(rank_seven_shift) == 22
    assert all(value > 0 for value in rank_seven_shift)

    _, a5, a6 = normalized_symbols()
    a7 = (
        sp.factorial(7)
        * (-expected_rank_seven)
        / sp.prod(D - offset for offset in range(7))
    )
    newton_difference = sp.cancel(a6**2 - a5 * a7)
    newton_numerator, newton_denominator = (
        newton_difference.as_numer_denom()
    )
    expected_newton_denominator = (
        sp.Integer(162188424826230242096971776000000)
        * D**2
        * (D - 6)
        * (D - 5) ** 2
        * (D - 4) ** 2
        * (D - 3) ** 2
        * (D - 2) ** 2
        * (D - 1) ** 2
    )
    assert sp.factor(newton_denominator) == sp.factor(
        expected_newton_denominator
    )
    newton_shift = tuple(
        int(value)
        for value in sp.Poly(
            sp.expand(newton_numerator.subs(D, U + 7)),
            U,
        ).all_coeffs()
    )
    assert len(newton_shift) == 38
    assert all(value > 0 for value in newton_shift)
    newton_payload = ",".join(
        str(value) for value in newton_shift
    )
    assert hashlib.sha256(
        newton_payload.encode("ascii")
    ).hexdigest() == (
        "3279d8dd6f05921e1a9f5673693ca182"
        "1f755243a83d9740f1a226eb05be561c"
    )

    c3_gap = sp.cancel((3 * D**2) ** 7 - a7)
    c3_numerator, c3_denominator = c3_gap.as_numer_denom()
    c3_shift = tuple(
        int(value)
        for value in sp.Poly(
            sp.expand(c3_numerator.subs(D, U + 7)),
            U,
        ).all_coeffs()
    )
    assert len(c3_shift) == 22
    assert all(value > 0 for value in c3_shift)
    c3_payload = ",".join(str(value) for value in c3_shift)
    assert hashlib.sha256(
        c3_payload.encode("ascii")
    ).hexdigest() == (
        "e88a1cb1d3a7ecfe6a54a7ada8857336"
        "06a072303643dade1e0c669deba05375"
    )

    falling_rows, bands = derive_through_seventh_band()
    seventh = sp.cancel(bands[6])
    expected = expected_seventh_band(D)
    assert sp.simplify(seventh - expected) == 0
    assert sp.Poly(seventh, D).degree() == 20

    numerator, denominator = seventh.as_numer_denom()
    assert denominator == SEVENTH_BAND_DENOMINATOR
    shifted = tuple(
        int(value)
        for value in sp.Poly(
            sp.expand(numerator.subs(D, U + 13)),
            U,
        ).all_coeffs()
    )
    assert shifted == SEVENTH_BAND_SHIFTED_COEFFICIENTS
    assert all(value > 0 for value in shifted)
    assert sp.rem(numerator, D - 12, D) == 0

    forced_falling_factor = sp.prod(
        D - root for root in range(7, 14)
    )
    falling_numerator = sp.cancel(
        falling_rows[7]
    ).as_numer_denom()[0]
    assert sp.rem(
        falling_numerator,
        forced_falling_factor,
        D,
    ) == 0

    payload = ",".join(str(value) for value in shifted)
    return {
        "schema": (
            "amra.opg1757.ordinary-rank-seven-and-"
            "seventh-long-band.v1"
        ),
        "status": "PASS",
        "rank_seven": {
            "degree_bound_source": (
                "ALL_RANK_ORDINARY_SYMBOL_DEGREE_THEOREM.md"
            ),
            "interpolation_depths": list(range(7, 29)),
            "holdout_depths": list(range(29, 33)),
            "value_source": (
                "exact_ordinary_polynomial(depth), then coefficient "
                "of k^(depth-7)"
            ),
            "denominator": int(RANK_SEVEN_DENOMINATOR),
            "negative_shifted_numerator_coefficients": (
                list(rank_seven_shift)
            ),
            "sixth_normalized_newton": {
                "claim": "a_(d,6)^2 > a_(d,5)*a_(d,7)",
                "reduced_denominator": str(
                    sp.factor(newton_denominator)
                ),
                "shift": "d=u+7",
                "shifted_reduced_numerator_coefficients": (
                    list(newton_shift)
                ),
                "shifted_coefficient_sha256": hashlib.sha256(
                    newton_payload.encode("ascii")
                ).hexdigest(),
            },
            "rank_seven_C3_bound": {
                "claim": "a_(d,7) < (3*d^2)^7",
                "reduced_denominator": str(
                    sp.factor(c3_denominator)
                ),
                "shift": "d=u+7",
                "shifted_reduced_numerator_coefficients": (
                    list(c3_shift)
                ),
                "shifted_coefficient_sha256": hashlib.sha256(
                    c3_payload.encode("ascii")
                ).hexdigest(),
            },
        },
        "seventh_band": {
            "band": 6,
            "minimum_depth": 13,
            "degree": 20,
            "denominator": int(SEVENTH_BAND_DENOMINATOR),
            "shift": "d=u+13",
            "shifted_numerator_coefficients": list(shifted),
            "shifted_coefficient_sha256": hashlib.sha256(
                payload.encode("ascii")
            ).hexdigest(),
            "all_shifted_coefficients_positive": True,
            "forced_factor": "d-12",
            "first_admissible_value": str(seventh.subs(D, 13)),
            "falling_row_seven_forced_roots": list(range(7, 14)),
        },
        "symbol_unification": (
            "Every lower beta polynomial is explicitly substituted "
            "from TRIANGLE_D to the independent symbol D."
        ),
    }


def main() -> None:
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
