#!/usr/bin/env python3
"""Exact rational exponent ledger for the proposed M01 -> M05 -> M10 chain."""

from fractions import Fraction
import json


def f(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def main() -> None:
    K = Fraction(5, 9)
    S = Fraction(7, 9)
    U = Fraction(5, 6)
    q = Fraction(13, 18)
    target = Fraction(3, 1)

    chart_only_gap = target - K
    optimistic_tuple = K + S + U + q
    optimistic_gap = target - optimistic_tuple
    assert chart_only_gap == Fraction(22, 9)
    assert optimistic_tuple == Fraction(26, 9)
    assert optimistic_gap == Fraction(1, 9)

    print(json.dumps({
        "schema": "amra.erdos1083.typed-chain-exponent-audit.v1",
        "native_exponents": {
            "K_rows": f(K), "S": f(S), "U": f(U), "q": f(q),
            "required_distinct_labels": ">3",
        },
        "subpower_preservation": {
            "heavy_factor_pigeonhole": "K/log_2(U)=t^(5/9-o(1))",
            "fixed_sign_selection": "K/2=t^(5/9-o(1))",
        },
        "gaps": {
            "chart_parameters_to_target": f(chart_only_gap),
            "optimistic_K_times_S_times_U_times_q": f(optimistic_tuple),
            "remaining_beyond_that_product": f(optimistic_gap),
        },
        "interpretation": (
            "The proved heavy-factor and fixed-sign steps preserve the row exponent, "
            "but chart distinctness supplies only t^(5/9-o(1)) labels. M10 still needs "
            "a genuine multiplicity/expansion theorem; no Jacobian bookkeeping fills it."
        ),
        "public_exponent_changed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
