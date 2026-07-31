#!/usr/bin/env python3
"""Exact all-k audit for the beta^5,...,beta^8 fixed-page kernel window.

The inherited fixed-page theorem writes

    D_k = 2*k*(k-1)*beta^4*(1+k*beta)^(2*s-2*k-2)*K_k(s,beta).

This verifier reconstructs the coefficients of beta^(r+4) in D_k from
the primitive page-partition transfer, deconvolves the displayed power,
and proves the formulas for [beta^r] K_k, r=5,...,8, by exact bounded
interpolation.  No fixed value of k is promoted to a theorem.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
INHERITED = (
    HERE.parents[1]
    / "q1_eight_hour_campaign_2026-07-29"
    / "opg1757"
)
sys.path.insert(0, str(INHERITED))

from verify_general_k_low_coefficients import (  # noqa: E402
    reduced_beta_numerator,
)


K, S = sp.symbols("k s", integer=True)
M, U, V = sp.symbols("m u v", integer=True)


def positive_q_polynomials() -> dict[int, tuple[int, sp.Expr]]:
    """Return denominator and positive Q_r(m,u), where m=k-4,u=s-k."""

    q5 = (
        4 * M**8
        + 168 * M**7
        + 3008 * M**6
        + 29420 * M**5
        + 166604 * M**4
        + 531440 * M**3
        + 872122 * M**2
        + 721904 * M
        + 238080
        + U
        * (
            20 * M**6
            + 640 * M**5
            + 8295 * M**4
            + 53684 * M**3
            + 168913 * M**2
            + 203478 * M
            + 88560
        )
        + U**2
        * (
            15 * M**4
            + 350 * M**3
            + 3000 * M**2
            + 10225 * M
            + 7260
        )
    )
    q6 = (
        8 * M**10
        + 408 * M**9
        + 9152 * M**8
        + 117248 * M**7
        + 929752 * M**6
        + 4611972 * M**5
        + 13797996 * M**4
        + 23395624 * M**3
        + 23189488 * M**2
        + 12275712 * M
        + 2672640
        + U
        * (
            60 * M**8
            + 2440 * M**7
            + 42330 * M**6
            + 399378 * M**5
            + 2146868 * M**4
            + 6215432 * M**3
            + 8271358 * M**2
            + 5583984 * M
            + 1451520
        )
        + U**2
        * (
            90 * M**6
            + 2850 * M**5
            + 36605 * M**4
            + 232950 * M**3
            + 692755 * M**2
            + 646710 * M
            + 224640
        )
        + U**3
        * (
            15 * M**4
            + 360 * M**3
            + 3210 * M**2
            + 11415 * M
            + 7200
        )
    )
    q7 = (
        8 * M**12
        + 480 * M**11
        + 12936 * M**10
        + 204812 * M**9
        + 2087648 * M**8
        + 14086576 * M**7
        + 62233928 * M**6
        + 172660150 * M**5
        + 287624656 * M**4
        + 309531452 * M**3
        + 198955808 * M**2
        + 70373376 * M
        + 10321920
        + U
        * (
            84 * M**10
            + 4144 * M**9
            + 90006 * M**8
            + 1113812 * M**7
            + 8452766 * M**6
            + 39179477 * M**5
            + 103478960 * M**4
            + 137948167 * M**3
            + 113360666 * M**2
            + 46410528 * M
            + 7741440
        )
        + U**2
        * (
            210 * M**8
            + 8400 * M**7
            + 143465 * M**6
            + 1326759 * M**5
            + 6864074 * M**4
            + 18005946 * M**3
            + 17488604 * M**2
            + 10014942 * M
            + 1935360
        )
        + U**3
        * (
            105 * M**6
            + 3360 * M**5
            + 43785 * M**4
            + 281925 * M**3
            + 819840 * M**2
            + 560805 * M
            + 161280
        )
    )
    q8 = (
        16 * M**14
        + 1104 * M**13
        + 34736 * M**12
        + 654736 * M**11
        + 8154064 * M**10
        + 69654016 * M**9
        + 409313424 * M**8
        + 1614073776 * M**7
        + 4073034784 * M**6
        + 6391253288 * M**5
        + 7125239828 * M**4
        + 4765758200 * M**3
        + 2036873984 * M**2
        + 456228864 * M
        + 41287680
        + U
        * (
            224 * M**12
            + 12992 * M**11
            + 338856 * M**10
            + 5185432 * M**9
            + 50784048 * M**8
            + 324343504 * M**7
            + 1311075806 * M**6
            + 3088517882 * M**5
            + 3836692942 * M**4
            + 3600109830 * M**3
            + 1578177172 * M**2
            + 435493632 * M
            + 41287680
        )
        + U**2
        * (
            840 * M**10
            + 40600 * M**9
            + 864640 * M**8
            + 10463264 * M**7
            + 76822907 * M**6
            + 334127591 * M**5
            + 758131031 * M**4
            + 661112725 * M**3
            + 540966454 * M**2
            + 121735068 * M
            + 15482880
        )
        + U**3
        * (
            840 * M**8
            + 33600 * M**7
            + 574910 * M**6
            + 5311950 * M**5
            + 26986820 * M**4
            + 64636110 * M**3
            + 35513030 * M**2
            + 23349060 * M
            + 2580480
        )
        + U**4
        * (
            105 * M**6
            + 3465 * M**5
            + 46935 * M**4
            + 316155 * M**3
            + 951825 * M**2
            + 517335 * M
            + 161280
        )
    )
    return {
        5: (15, sp.expand(q5)),
        6: (90, sp.expand(q6)),
        7: (315, sp.expand(q7)),
        8: (2520, sp.expand(q8)),
    }


def claimed_coefficient(rank: int) -> sp.Expr:
    denominator, polynomial = positive_q_polynomials()[rank]
    shifted = (M + 1) * (M + 2) * polynomial / denominator
    return sp.expand(shifted.subs({M: K - 4, U: S - K}))


def full_domain_positive_polynomials() -> dict[int, tuple[int, sp.Expr]]:
    """Return Q*_r(m,v) for m=k-4>=0 and v=s-4>=0."""

    return {
        rank: (denominator, sp.expand(polynomial.subs(U, V - M)))
        for rank, (denominator, polynomial) in positive_q_polynomials().items()
    }


def interpolate_reduced_numerator(total_degree: int) -> tuple[sp.Expr, int]:
    """Reconstruct n_d on a degree-forcing rectangular exact grid."""

    maximum_k_degree = 2 * total_degree - 6
    maximum_s_degree = total_degree
    s_nodes = tuple(range(4, 4 + maximum_s_degree + 1))
    k_nodes = tuple(range(maximum_k_degree + 1))
    rows = []
    evaluations = 0
    for page_count in k_nodes:
        values = []
        for core_count in s_nodes:
            values.append(
                (
                    core_count,
                    reduced_beta_numerator(
                        core_count, page_count, total_degree
                    ),
                )
            )
            evaluations += 1
        rows.append((page_count, sp.interpolate(values, S)))
    return sp.factor(sp.interpolate(rows, K)), evaluations


def polynomial_digest(expression: sp.Expr) -> str:
    polynomial = sp.Poly(sp.expand(expression), K, S)
    payload = ";".join(
        f"{monomial}:{coefficient}"
        for monomial, coefficient in polynomial.terms()
    )
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def audit() -> dict[str, object]:
    records = []
    for rank, (denominator, positive) in (
        full_domain_positive_polynomials().items()
    ):
        total_degree = rank + 4
        reduced, evaluations = interpolate_reduced_numerator(total_degree)
        if sp.factor(reduced / (2 * K * (K - 1))) != sp.factor(
            claimed_coefficient(rank)
        ):
            raise AssertionError(f"beta^{rank} formula mismatch")

        positive_poly = sp.Poly(positive, M, V)
        if any(coefficient <= 0 for _, coefficient in positive_poly.terms()):
            raise AssertionError("positive shifted certificate failed")

        # Points outside both interpolation rectangles.
        holdouts = (
            (2 * total_degree - 5, total_degree + 5),
            (2 * total_degree - 4, total_degree + 6),
        )
        for page_count, core_count in holdouts:
            actual = reduced_beta_numerator(
                core_count, page_count, total_degree
            )
            expected = sp.cancel(
                2
                * K
                * (K - 1)
                * claimed_coefficient(rank)
            ).subs({K: page_count, S: core_count})
            if actual != expected:
                raise AssertionError("off-grid holdout failed")

        records.append(
            {
                "kernel_beta_rank": rank,
                "raw_determinant_degree": total_degree,
                "proved_degree_bounds": {
                    "k": 2 * total_degree - 6,
                    "s": total_degree,
                },
                "interpolation_evaluations": evaluations,
                "positive_form": (
                    f"(m+1)*(m+2)/{denominator} * Q_{rank}(m,v), "
                    "m=k-4, v=s-4"
                ),
                "positive_Q_term_count": len(positive_poly.terms()),
                "positive_Q_digest": polynomial_digest(
                    positive.subs({M: K, V: S})
                ),
                "off_grid_holdouts": [list(item) for item in holdouts],
            }
        )
    return {
        "schema": "amra.opg1757.general-k-beta5-beta8.v1",
        "status": "PASS",
        "theorem": (
            "For every k>=4 and s>=4, the coefficients beta^5 through "
            "beta^8 of K_k(s,beta) are strictly positive. For k=2,3 "
            "they vanish whenever the requested rank exceeds deg K_k."
        ),
        "proof_engine": (
            "Primitive exact page-partition transfer; universal "
            "(1+k*beta) deconvolution; exact a-priori bidegree bounds; "
            "full rectangular interpolation; disjoint holdouts; "
            "coefficientwise-positive shift m=k-4,v=s-4."
        ),
        "records": records,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
