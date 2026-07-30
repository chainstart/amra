#!/usr/bin/env python3
"""Exact finite audit of the localized rings used in the degree theorem."""

from __future__ import annotations

import argparse
import json

import sympy as sp

from independent_verify_all_fixed_rank_ordinary_symbol_algorithm import (
    K,
    T,
    W,
    X,
    Z,
    central_kernels,
    central_moment,
    determinant_kernels,
    profile_functions,
)


def is_polynomial(expression, variable) -> bool:
    expression = sp.cancel(expression)
    denominator = sp.denom(expression)
    return not sp.Poly(denominator, variable).degree()


def polynomial_valuation(expression, variable) -> int:
    numerator = sp.Poly(sp.numer(sp.cancel(expression)), variable)
    return min(int(monomial[0]) for monomial, _ in numerator.terms())


def audit(maximum_rank: int = 5) -> dict[str, object]:
    profiles = profile_functions(maximum_rank)
    normalized = [
        [sp.cancel(value / sp.sqrt(W)) for value in row]
        for row in profiles
    ]

    profile_records = []
    for rank in range(maximum_rank + 1):
        for profile_index in range(3):
            localized = sp.cancel(
                normalized[profile_index][rank] * W ** (3 * rank)
            )
            if not is_polynomial(localized, X):
                raise AssertionError("profile has a non-W denominator")
            numerator_degree = int(sp.Poly(localized, X).degree())
            if numerator_degree > 3 * rank:
                raise AssertionError("profile is not bounded at infinity")
            profile_records.append(
                {
                    "profile_index": profile_index,
                    "rank": rank,
                    "localized_numerator_degree": numerator_degree,
                    "maximum_degree": 3 * rank,
                }
            )

    delta_zero = sp.cancel(normalized[1][0] - normalized[0][0])
    epsilon_zero = sp.cancel(
        normalized[2][0] - 2 * normalized[1][0] + normalized[0][0]
    )
    epsilon_one = sp.cancel(
        normalized[2][1] - 2 * normalized[1][1] + normalized[0][1]
    )
    if (delta_zero, epsilon_zero, epsilon_one) != (0, 0, 0):
        raise AssertionError("low-rank marked cancellations failed")

    c_values = []
    d_values = []
    e_values = []
    leading_laurent_records = []
    half = sp.Rational(1, 2)
    for rank in range(maximum_rank + 1):
        c_value = sp.factor(
            sp.limit(normalized[0][rank] * W ** (3 * rank), X, half)
        )
        delta = sp.cancel(normalized[1][rank] - normalized[0][rank])
        d_value = (
            sp.S.Zero
            if rank == 0
            else sp.factor(
                sp.limit(delta * W ** (3 * rank - 2), X, half)
            )
        )
        epsilon = sp.cancel(
            normalized[2][rank]
            - 2 * normalized[1][rank]
            + normalized[0][rank]
        )
        e_value = (
            sp.S.Zero
            if rank < 2
            else sp.factor(
                sp.limit(epsilon * W ** (3 * rank - 4), X, half)
            )
        )
        if rank:
            expected_c = (
                (-1) ** (rank + 1)
                * sp.factorial2(6 * rank - 3)
                / (9**rank * sp.factorial(2 * rank))
            )
            expected_d = -sp.Rational(6 * rank, 6 * rank - 5) * c_value
            if sp.cancel(c_value - expected_c):
                raise AssertionError("C_0 highest Laurent layer failed")
            if sp.cancel(d_value - expected_d):
                raise AssertionError("delta highest Laurent layer failed")
        if rank >= 2 and sp.cancel(
            e_value + 6 * (rank - 1) * c_values[rank - 1]
        ):
            raise AssertionError(
                "finite epsilon leading-layer pattern failed"
            )
        c_values.append(c_value)
        d_values.append(d_value)
        e_values.append(e_value)
        leading_laurent_records.append(
            {
                "rank": rank,
                "c_r": str(c_value),
                "d_r": str(d_value),
                "e_r": str(e_value),
                "e_pattern_checked": rank >= 2,
            }
        )

    kernels = determinant_kernels(profiles, maximum_rank)
    central = central_kernels(kernels, maximum_rank)
    central_summand_records = []
    for total_rank in range(2, maximum_rank + 1):
        for determinant_rank in range(2, total_rank + 1):
            inverse_rank = total_rank - determinant_rank
            for derivative_order in range(
                0, 2 * inverse_rank + 1, 2
            ):
                coefficient = sp.expand(
                    central_moment(derivative_order).subs(K, 1 / Z)
                ).coeff(Z, inverse_rank)
                if not coefficient:
                    continue
                summand = sp.cancel(
                    coefficient
                    / sp.factorial(derivative_order)
                    * sp.diff(
                        kernels[determinant_rank],
                        X,
                        derivative_order,
                    ).subs(X, half)
                )
                if not summand:
                    continue
                t_valuation = polynomial_valuation(summand, T)
                required_valuation = determinant_rank + derivative_order
                if t_valuation < required_valuation:
                    raise AssertionError(
                        "central summand lost a chain-rule t factor"
                    )
                if total_rank >= 4 and t_valuation < 4:
                    raise AssertionError(
                        "central summand is not divisible by t^4"
                    )
                growth_degree = int(
                    sp.degree(sp.numer(summand), T)
                    - sp.degree(sp.denom(summand), T)
                )
                if growth_degree > total_rank + 1:
                    raise AssertionError(
                        "central summand grows too quickly at infinity"
                    )
                central_summand_records.append(
                    {
                        "total_rank": total_rank,
                        "determinant_rank": determinant_rank,
                        "derivative_order": derivative_order,
                        "t_valuation": t_valuation,
                        "chain_rule_lower_bound": required_valuation,
                        "growth_degree_at_infinity": growth_degree,
                        "maximum_growth_degree": total_rank + 1,
                    }
                )

    central_records = []
    for rank in range(2, maximum_rank + 1):
        localized = sp.cancel(
            central[rank] * (1 - T) ** (3 * rank - 5)
        )
        if not is_polynomial(localized, T):
            raise AssertionError("central kernel has another denominator")
        quotient = sp.cancel(central[rank] / T**4)
        if not is_polynomial(
            sp.cancel(quotient * (1 - T) ** (3 * rank - 5)),
            T,
        ):
            raise AssertionError("t=0 is not removable termwise")
        leading_layer = sp.factor(
            sp.limit(
                central[rank] * (1 - T) ** (3 * rank - 5),
                T,
                1,
            )
        )
        convolution_layer = sp.factor(
            sum(
                d_values[left_rank] * d_values[rank - left_rank]
                - c_values[left_rank] * e_values[rank - left_rank]
                for left_rank in range(rank + 1)
            )
        )
        if sp.cancel(leading_layer - convolution_layer):
            raise AssertionError(
                "highest central Laurent convolution failed"
            )
        central_records.append(
            {
                "rank": rank,
                "denominator_power": 3 * rank - 5,
                "t_four_divides": True,
                "growth_degree_at_infinity": int(
                    sp.degree(sp.numer(central[rank]), T)
                    - sp.degree(sp.denom(central[rank]), T)
                ),
                "highest_laurent_layer": str(leading_layer),
            }
        )

    symbol_records = []
    for symbol_rank in range(maximum_rank - 1):
        expression = sp.factor(
            sum(
                central[rank]
                for rank in range(2, symbol_rank + 3)
            )
            / (2 * T**4)
        )
        denominator_power = 3 * symbol_rank + 1
        localized = sp.cancel(
            expression * (1 - T) ** denominator_power
        )
        if not is_polynomial(localized, T):
            raise AssertionError("B_r has a non-(1-t) denominator")
        if sp.degree(localized, T) > 4 * symbol_rank:
            raise AssertionError("B_r numerator degree is too large")
        for depth in range(symbol_rank):
            if sp.series(expression, T, 0, symbol_rank + 1).removeO().coeff(
                T, depth
            ):
                raise AssertionError("low-depth truncation failed")
        symbol_records.append(
            {
                "symbol_rank": symbol_rank,
                "denominator_power_bound": denominator_power,
                "localized_numerator_degree": int(sp.degree(localized, T)),
                "maximum_numerator_degree": 4 * symbol_rank,
                "zero_coefficients_below_depth": symbol_rank,
            }
        )

    return {
        "schema": "amra.opg1757.all-rank-degree-localization-finite.v1",
        "scope": (
            "Exact finite symbolic audit of the rings and removable t=0 "
            "factor. The accompanying theorem supplies the all-rank proof."
        ),
        "maximum_profile_rank": maximum_rank,
        "profile_records": profile_records,
        "low_rank_marked_identities": {
            "delta_0": "0",
            "epsilon_0": "0",
            "epsilon_1": "0",
        },
        "leading_laurent_records": leading_laurent_records,
        "central_records": central_records,
        "central_summand_records": central_summand_records,
        "symbol_records": symbol_records,
        "status": "finite_exact_localization_audit_passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-rank", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(audit(args.maximum_rank), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
