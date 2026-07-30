#!/usr/bin/env python3
"""Exact all-depth certificate for the sixth long-recurrence band."""

from __future__ import annotations

import argparse
import hashlib
import json

import sympy as sp

from independent_verify_ordinary_rank_six_symbol import (
    rank_six_polynomial,
)
from verify_ordinary_first_five_long_recurrence_bands import (
    D,
    N,
    U,
    beta_polynomials,
    derive_bands,
    signed_stirling_near_diagonal,
)


DENOMINATOR = sp.Integer(15359376162816000)
RESIDUAL_COEFFICIENTS = (
    810123093896375,
    -25921081431700875,
    313490671217497970,
    -1492874651122299900,
    -1887303336152228890,
    49625869946758088130,
    -167524355872717489604,
    -106706576731710308472,
    1816293817555406107219,
    -3108681098587146424959,
    -2327663884048779946070,
    9529661544865824480588,
    -493471326045590983080,
    -8190583449886689443856,
    -15710022013283259194016,
    29745938852108657679744,
    -5169307325421355490304,
)
SHIFTED_NUMERATOR_COEFFICIENTS = (
    810123093896375,
    117470706187957500,
    7916160141456279720,
    329090197951577059200,
    9446873816558259471810,
    198583558207712884868760,
    3162912470191756651508636,
    38951480639440722082621584,
    375079850835431480188544199,
    2836468344865020127987279932,
    16817548301644562228270567652,
    77567404341593653627142341584,
    274129824219295871333741310776,
    723941511230071673766897349008,
    1371903306568738801868891133792,
    1742598030043436615873060144832,
    1304914777582506924209367824640,
    421161144536910289212100915200,
)
FIRST_ADMISSIBLE_VALUE = sp.Rational(
    3316778722205903687,
    120960,
)


def derive_through_sixth_band() -> tuple[list[sp.Expr], list[sp.Expr]]:
    """Rebuild h_0,...,h_6 and gamma_0,...,gamma_5."""
    beta = beta_polynomials() + [rank_six_polynomial(D)]
    stirling = signed_stirling_near_diagonal(6)

    falling_rows = [sp.Integer(1)]
    for loss in range(1, 7):
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
                    * stirling[loss - index].subs(N, D - index)
                    for index in range(loss)
                )
            )
        )

    bands = []
    for band in range(6):
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


def expected_sixth_band() -> sp.Expr:
    residual = sum(
        coefficient * D ** (16 - index)
        for index, coefficient in enumerate(RESIDUAL_COEFFICIENTS)
    )
    return (D - 10) * residual / DENOMINATOR


def audit() -> dict[str, object]:
    falling_rows, bands = derive_through_sixth_band()
    _, previous_bands = derive_bands()
    assert all(
        sp.simplify(actual - previous) == 0
        for actual, previous in zip(bands[:5], previous_bands)
    )

    sixth = sp.cancel(bands[5])
    expected = expected_sixth_band()
    assert sp.simplify(sixth - expected) == 0
    assert sp.Poly(sixth, D).degree() == 17

    numerator, denominator = sixth.as_numer_denom()
    assert denominator == DENOMINATOR
    assert sp.rem(numerator, D - 10, D) == 0

    shifted = sp.Poly(sp.expand(numerator.subs(D, U + 11)), U)
    coefficients = tuple(int(item) for item in shifted.all_coeffs())
    assert coefficients == SHIFTED_NUMERATOR_COEFFICIENTS
    assert all(item > 0 for item in coefficients)
    assert sixth.subs(D, 11) == FIRST_ADMISSIBLE_VALUE

    forced_falling_factor = sp.prod(D - root for root in range(6, 12))
    falling_numerator = sp.cancel(falling_rows[6]).as_numer_denom()[0]
    assert sp.rem(falling_numerator, forced_falling_factor, D) == 0

    payload = ",".join(str(item) for item in coefficients)
    return {
        "schema": "amra.opg1757.sixth-long-recurrence-band.v1",
        "status": "PASS",
        "band": 5,
        "minimum_depth": 11,
        "degree": 17,
        "denominator": int(DENOMINATOR),
        "forced_factor": "d-10",
        "shifted_numerator_coefficients": list(coefficients),
        "shifted_coefficient_sha256": hashlib.sha256(
            payload.encode("ascii")
        ).hexdigest(),
        "first_admissible_value": str(FIRST_ADMISSIBLE_VALUE),
        "falling_row_six_forced_roots": list(range(6, 12)),
        "derivation": (
            "rank-six ordinary symbol -> ordinary-to-Newton triangle "
            "-> exact long-recurrence triangle"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
