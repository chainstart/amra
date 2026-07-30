#!/usr/bin/env python3
"""Exact finite audit of the all-rank falling-triangle corollary."""

from __future__ import annotations

import argparse
import json

import sympy as sp

from verify_ordinary_first_five_long_recurrence_bands import (
    D,
    derive_bands,
)


def audit() -> dict[str, object]:
    h, gamma = derive_bands()
    falling_records = []
    for rank in range(1, len(h)):
        forced = sp.prod(D - root for root in range(rank, 2 * rank))
        quotient, remainder = sp.div(
            sp.Poly(h[rank], D),
            sp.Poly(forced, D),
        )
        if not remainder.is_zero:
            raise AssertionError("forced falling factor is absent")
        degree = int(sp.degree(h[rank], D))
        residual_degree = int(quotient.degree())
        leading_coefficient = sp.Poly(h[rank], D).LC()
        if degree != 3 * rank:
            raise AssertionError("falling coefficient degree is not exact")
        if residual_degree != 2 * rank:
            raise AssertionError("falling residual degree is not exact")
        if (-1) ** rank * leading_coefficient <= 0:
            raise AssertionError("falling leading sign is incorrect")
        falling_records.append(
            {
                "rank": rank,
                "degree": degree,
                "forced_roots": list(range(rank, 2 * rank)),
                "residual_degree": residual_degree,
                "leading_coefficient": str(leading_coefficient),
                "alternating_leading_sign": True,
            }
        )

    recurrence_records = []
    for band, value in enumerate(gamma):
        if sp.degree(value, D) > 3 * band + 2:
            raise AssertionError("recurrence band degree is too large")
        if band:
            quotient, remainder = sp.div(
                sp.Poly(value, D),
                sp.Poly(D - 2 * band, D),
            )
            if not remainder.is_zero:
                raise AssertionError("recurrence boundary factor absent")
            residual_degree = quotient.degree()
        else:
            residual_degree = sp.degree(value, D)
        recurrence_records.append(
            {
                "band": band,
                "degree": int(sp.degree(value, D)),
                "forced_boundary_root": 2 * band if band else None,
                "residual_degree": int(residual_degree),
            }
        )

    return {
        "schema": "amra.opg1757.all-rank-falling-triangle.v1",
        "scope": (
            "Finite exact audit through available symbols. The theorem "
            "supplies the arbitrary-rank degree and factor proof."
        ),
        "falling_records": falling_records,
        "recurrence_records": recurrence_records,
        "status": "finite_exact_triangle_audit_passed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
