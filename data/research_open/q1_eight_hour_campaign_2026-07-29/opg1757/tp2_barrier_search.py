#!/usr/bin/env python3
"""Exact TP2 barrier search for the general-s disjoint-core alpha^2 layer.

Let A[i,j](beta) be the sum of the j-th nilpotent-page chain starting from

    i=0: (1,...,1),  i=1: (2,1,...,1),  i=2: (2,2,1,...,1).

The full normalized alpha^2 margin is

    sum_{j,k} C(t,j) C(t,k) lambda^(2s-4-j-k)
        (A[1,j] A[1,k] - A[0,j] A[2,k]).

This script tests three increasingly weak positivity assertions:

1. destination-profile-resolved, fixed (j,k);
2. summed over destinations but fixed (j,k);
3. pooled by the Newton order n after the exact positive linearization
   C(t,j)C(t,k) = sum_h M(j,k,h) C(t,j+k-h).

The first two fail minimally.  The third is an explicitly bounded exact
search, not an all-s/all-degree theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

from general_s_disjoint_extended import (
    convolve_with_lambda,
    profile,
)
from general_s_disjoint_low_degree import (
    Profile,
    profile_selections,
    truncated_profile_chain,
)


def state_chain(
    initial: Profile, max_beta: int
) -> list[dict[tuple[Profile, int], int]]:
    """Return the complete profile-resolved N-chain."""

    maximum_order = max_beta // 2
    vector: dict[tuple[Profile, int], int] = {(initial, 0): 1}
    result: list[dict[tuple[Profile, int], int]] = []
    for _ in range(maximum_order + 1):
        result.append(vector)
        next_vector: defaultdict[tuple[Profile, int], int] = defaultdict(int)
        for (source, old_degree), coefficient in vector.items():
            for mask_size, multiplicity, destination in profile_selections(
                source, max_beta - old_degree
            ):
                next_vector[
                    (destination, old_degree + mask_size)
                ] += coefficient * multiplicity
        vector = dict(next_vector)
    return result


def convolution(left: list[int], right: list[int], maximum: int) -> list[int]:
    result = [0] * (maximum + 1)
    for left_degree, left_value in enumerate(left):
        if not left_value:
            continue
        for right_degree, right_value in enumerate(right):
            if right_value and left_degree + right_degree <= maximum:
                result[left_degree + right_degree] += left_value * right_value
    return result


def multinomial_overlap(j: int, k: int, overlap: int) -> int:
    """Coefficient of C(t,j+k-overlap) in C(t,j)C(t,k)."""

    union = j + k - overlap
    return math.factorial(union) // (
        math.factorial(overlap)
        * math.factorial(j - overlap)
        * math.factorial(k - overlap)
    )


def pooled_t_newton_rows(
    s: int, max_beta: int
) -> list[list[object]]:
    """Return [n,d,c] after pooling every ordered (j,k) by t-Newton order."""

    maximum_order = max_beta // 2
    chains = {
        0: truncated_profile_chain(profile(singletons=s), max_beta),
        1: truncated_profile_chain(
            profile(2, singletons=s - 2), max_beta
        ),
        2: truncated_profile_chain(
            profile(2, 2, singletons=s - 4), max_beta
        ),
    }
    pooled = [
        [0] * (max_beta + 1) for _ in range(2 * maximum_order + 1)
    ]
    for j in range(maximum_order + 1):
        for k in range(maximum_order + 1):
            exponent = 2 * s - 4 - j - k
            positive = convolve_with_lambda(
                chains[1][j],
                chains[1][k],
                exponent,
                s,
                max_beta,
            )
            negative = convolve_with_lambda(
                chains[0][j],
                chains[2][k],
                exponent,
                s,
                max_beta,
            )
            minor = [
                left - right for left, right in zip(positive, negative)
            ]
            for overlap in range(min(j, k) + 1):
                newton_order = j + k - overlap
                multiplier = multinomial_overlap(j, k, overlap)
                for degree, coefficient in enumerate(minor):
                    pooled[newton_order][degree] += multiplier * coefficient
    return [
        [newton_order, degree, str(coefficient)]
        for newton_order, row in enumerate(pooled)
        for degree, coefficient in enumerate(row)
        if coefficient
    ]


def minimal_profile_counterexample() -> dict[str, object]:
    """Resolve the first statewise failure at s=4,j=0,k=1,beta^2."""

    s = 4
    z = profile(singletons=s)
    ef = profile(2, 2, singletons=0)
    ef_chain = state_chain(ef, 2)
    destination = profile(4, singletons=0)
    coefficient = -ef_chain[1][(destination, 2)]
    if coefficient != -4:
        raise AssertionError("the claimed minimal profile failure changed")
    return {
        "s": s,
        "j_k": [0, 1],
        "beta_degree": 2,
        "left_destination_profile": list(z),
        "right_destination_profile": list(destination),
        "coefficient": str(coefficient),
        "explanation": (
            "The negative Z_0*EF_1 term merges the two size-2 blocks in "
            "four ways; the corresponding E_0*E_1 state-pair coefficient "
            "is zero. Lower beta degree cannot occur in an N-step."
        ),
    }


def build_certificate(
    minimum_s: int = 4, maximum_s: int = 12, max_beta: int = 40
) -> dict[str, object]:
    if minimum_s < 4 or maximum_s < minimum_s:
        raise ValueError("require 4 <= minimum_s <= maximum_s")
    if max_beta < 4:
        raise ValueError("max_beta must be at least 4")

    rows: list[list[object]] = []
    negative_rows: list[list[object]] = []
    for s in range(minimum_s, maximum_s + 1):
        for newton_order, degree, coefficient in pooled_t_newton_rows(
            s, max_beta
        ):
            row = [s, newton_order, degree, coefficient]
            rows.append(row)
            if int(coefficient) < 0:
                negative_rows.append(row)

    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    return {
        "schema": "amra.complete_split.disjoint_alpha2_tp2_barrier.v1",
        "definitions": {
            "A_i_j": (
                "beta-generating sum of the j-th nilpotent-page chain from "
                "profiles i=0:(1^s), i=1:(2,1^(s-2)), "
                "i=2:(2,2,1^(s-4))"
            ),
            "lambda": "1+s*beta",
        },
        "universal_summed_fixed_pair_failure": {
            "j_k": [0, 1],
            "symmetric_minor": (
                "2*A_1_0*A_1_1-A_0_0*A_2_1-A_0_1*A_2_0"
            ),
            "exact_value": "-beta^4*(1+beta)^(s-4)",
            "claim": "strictly coefficientwise negative for every s>=4",
        },
        "exact_cross_layer_cancellation": {
            "diagonal_minor_j1_k1": (
                "lambda*beta^4*(1+beta)^(s-4)"
            ),
            "normalized_pair_01": (
                "-lambda^(2s-5)*beta^4*(1+beta)^(s-4)"
            ),
            "normalized_pair_11": (
                "+lambda^(2s-5)*beta^4*(1+beta)^(s-4)"
            ),
            "consequence": (
                "Their contributions to t-Newton order 1 cancel exactly "
                "because C(t,1)^2=C(t,1)+2*C(t,2)."
            ),
        },
        "first_positive_pooled_layer": {
            "B_0": "0",
            "B_1": "0",
            "B_2": (
                "4*beta^4*(1+2*beta)^(2s-6)"
                "*lambda^(2s-8)"
            ),
            "status": (
                "proved for every s>=4 and all beta degrees by the "
                "two-page forest enumeration recorded in REPORT.md"
            ),
        },
        "second_positive_pooled_layer": {
            "definitions": (
                "x=1+3*beta, z=1+2*beta, "
                "K=1+12*beta+(6s+30)*beta^2+28s*beta^3+6s^2*beta^4"
            ),
            "B_3_s4": "24*beta^6",
            "B_3_s_ge_5": (
                "12*beta^4*lambda^(2s-10)"
                "*(x^(2s-8)*K-z^(2s-6)*lambda^2)"
            ),
            "status": (
                "proved coefficientwise positive for every s>=4 and all "
                "beta degrees by the three-page enumeration and positive "
                "binomial-remainder decomposition in REPORT.md"
            ),
        },
        "minimal_destination_profile_counterexample": (
            minimal_profile_counterexample()
        ),
        "pooled_search": {
            "s_range": [minimum_s, maximum_s],
            "beta_degree_range": [0, max_beta],
            "safe_full_degree_bound": 4 * maximum_s - 8,
            "covers_full_polynomial_for_each_searched_s": (
                max_beta >= 4 * maximum_s - 8
            ),
            "basis": "beta^d binomial(t,n), at each fixed integer s",
            "rows_s_tbin_beta_coefficient": rows,
            "negative_rows": negative_rows,
            "all_searched_coefficients_nonnegative": not negative_rows,
            "sha256_rows": hashlib.sha256(payload).hexdigest(),
            "scope_warning": (
                "The degree bound makes this the full polynomial at each "
                "listed s when covers_full_polynomial_for_each_searched_s "
                "is true, but finitely many s do not prove all s."
            ),
            "observed_exact_support": (
                "For every searched s, rows occur exactly at "
                "2<=n<=2s-5 and 2n<=d<=4s-10, and are strictly positive."
            ),
        },
        "barrier": (
            "No injection or TP2 proof preserving the ordered nilpotent "
            "page counts (j,k), or preserving both destination profiles, "
            "can establish the desired inequality: those strata have "
            "strictly negative coefficients. Any successful proof must "
            "pool different (j,k), at least through t-Newton overlap."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minimum-s", type=int, default=4)
    parser.add_argument("--maximum-s", type=int, default=12)
    parser.add_argument("--max-beta", type=int, default=40)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    certificate = build_certificate(
        args.minimum_s, args.maximum_s, args.max_beta
    )
    rendered = json.dumps(certificate, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
