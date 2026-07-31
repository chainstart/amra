#!/usr/bin/env python3
"""Small exact audit of the closed two-marked hyperforest EGF."""

from __future__ import annotations

import json
import math
import pathlib
import sys

import sympy as sp


HERE = pathlib.Path(__file__).resolve().parent
OLD = (
    HERE.parents[1]
    / "q1_three_hour_campaign_2026-07-31"
    / "opg1757"
)
sys.path.insert(0, str(OLD))


T, U = sp.symbols("t u")


def egf_value(s: int, excess: int, components: int) -> int:
    a = b = 2
    units = s - a - b
    phi = sum(
        U**j * T ** (j + 1) / sp.factorial(j + 1)
        for j in range(excess + 1)
    )
    v = (
        T
        + sum(
            U**j * T ** (j + 2) / sp.factorial(j + 2)
            for j in range(excess + 1)
        )
        - T
        * sum(
            U**j * T ** (j + 1) / sp.factorial(j + 1)
            for j in range(excess + 1)
        )
    )

    def truncate(expression: sp.Expr) -> sp.Expr:
        return sp.series(expression, U, 0, excess + 1).removeO()

    r_a = truncate(sp.exp(a * phi))
    r_b = truncate(sp.exp(b * phi))
    r_ab = truncate(
        a
        * b
        * sp.exp((a + b) * phi)
        * sp.exp(U * T)
        / (1 - T * sp.exp(U * T))
    )
    forest = r_ab * v ** (components - 1) / sp.factorial(
        components - 1
    )
    if components >= 2:
        forest += (
            r_a
            * r_b
            * v ** (components - 2)
            / sp.factorial(components - 2)
        )
    forest = truncate(forest)

    if units == 0:
        return int(sp.expand(forest).coeff(U, excess).subs(T, 0))
    integrand = truncate(
        sp.diff(forest, T) * sp.exp(units * phi)
    )
    coefficient_u = sp.cancel(
        sp.expand(integrand).coeff(U, excess)
    )
    coefficient_t = (
        sp.series(coefficient_u, T, 0, units)
        .removeO()
        .expand()
        .coeff(T, units - 1)
    )
    return int(math.factorial(units - 1) * coefficient_t)


def audit() -> dict[str, object]:
    from verify_second_deficit import hyperforest_component_weight

    cases = (
        # Minimal-block boundary: N=0, with same/separate marked components.
        (4, 0, 1),
        (4, 0, 2),
        (4, 1, 1),
        (5, 0, 1),
        (5, 0, 2),
        (5, 0, 3),
        (5, 1, 1),
        (5, 1, 2),
        (6, 0, 2),
        (6, 1, 1),
        (6, 2, 1),
        (7, 2, 2),
    )
    rows = []
    for s, excess, components in cases:
        measured = egf_value(s, excess, components)
        expected = hyperforest_component_weight(
            s, 2, excess, components
        )
        if measured != expected:
            raise AssertionError(
                "two-marked EGF mismatch at "
                f"{(s, excess, components)}"
            )
        rows.append([s, excess, components, measured])
    return {
        "schema": "amra.opg1757.two-marked-hyperforest-egf.v1",
        "status": "PASS",
        "claim_status": "PROVED",
        "exact_checks": len(rows),
        "rows": rows,
        "scope": "small checks audit an all-parameter species proof",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
