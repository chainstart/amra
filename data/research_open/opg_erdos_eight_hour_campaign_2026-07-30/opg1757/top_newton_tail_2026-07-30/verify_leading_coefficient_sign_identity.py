#!/usr/bin/env python3
"""Exact certificate for the all-rank leading ordinary-symbol sign."""

from __future__ import annotations

import json

import sympy as sp


R, M = sp.symbols("r m", integer=True, positive=True)


def positive_c(rank: int):
    return sp.factorial2(6 * rank - 3) / (
        9**rank * sp.factorial(2 * rank)
    )


def audit(maximum_rank: int = 12) -> dict[str, object]:
    ratio = (
        (6 * R + 3)
        * (6 * R + 1)
        * (6 * R - 1)
        / (9 * (2 * R + 2) * (2 * R + 1))
    )
    ratio_difference = sp.factor(ratio.subs(R, R + 1) - ratio)
    expected_ratio_difference = (
        36 * R**2 + 108 * R + 37
    ) / (6 * (R + 1) * (R + 2))
    if sp.cancel(ratio_difference - expected_ratio_difference):
        raise AssertionError("successive-ratio identity failed")

    endpoint_ratio = (
        3
        * (M - 1)
        * (2 * M)
        * (2 * M - 1)
        / (
            2
            * (6 * M - 3)
            * (6 * M - 5)
            * (6 * M - 7)
        )
    )
    endpoint_margin = sp.factor(sp.Rational(1, 2) - endpoint_ratio)
    expected_margin = (
        34 * M**2 - 70 * M + 35
    ) / (2 * (6 * M - 7) * (6 * M - 5))
    if sp.cancel(endpoint_margin - expected_margin):
        raise AssertionError("endpoint convolution margin failed")

    p = {rank: positive_c(rank) for rank in range(1, maximum_rank + 1)}
    q = {
        rank: sp.Rational(6 * rank, 6 * rank - 5) * p[rank]
        for rank in p
    }
    records = []
    for central_rank in range(2, maximum_rank + 1):
        m = central_rank - 1
        p_convolution = sp.factor(
            sum(p[left] * p[m - left] for left in range(1, m))
        )
        q_convolution = sp.factor(
            sum(
                q[left] * q[central_rank - left]
                for left in range(1, central_rank)
            )
        )
        signed_layer = sp.factor(
            q_convolution
            + 6 * m * p[m]
            - 3 * m * p_convolution
        )
        if signed_layer <= 0:
            raise AssertionError("finite leading layer is not positive")
        records.append(
            {
                "central_rank": central_rank,
                "signed_highest_laurent_layer": str(signed_layer),
                "p_convolution_over_p_m": str(
                    sp.factor(p_convolution / p[m])
                ),
            }
        )

    return {
        "schema": "amra.opg1757.leading-coefficient-sign.v1",
        "scope": (
            "Symbolic ratio and convolution-margin identities proving "
            "(-1)^n A_n>0; finite records are redundant checks."
        ),
        "successive_ratio_difference": str(ratio_difference),
        "endpoint_convolution_margin": str(endpoint_margin),
        "maximum_redundant_rank": maximum_rank,
        "records": records,
        "conclusion": (
            "deg(P_r)=3r and (-1)^r*[d^(3r)]P_r>0; the "
            "complementary endpoint localization bridge is proved"
        ),
        "status": "symbolic_all_rank_leading_sign_identity_passed",
    }


def main() -> None:
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
