#!/usr/bin/env python3
"""Blind audit of the round-three quotient host and point-pair ledger."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import json

import sympy as sp


def main() -> None:
    # Reconstruct the universal Boolean host over independent formal factors.
    boolean_rows = []
    for D in range(1, 8):
        ys = sp.symbols(f"y0:{D}")
        hs = sp.symbols(f"H0:{D}")
        host = sp.prod((1 - ys[i]) + ys[i] * hs[i] for i in range(D))
        polynomial = sp.Poly(sp.expand(host), *ys)
        assert polynomial.total_degree() == D
        assert all(polynomial.degree(y) == 1 for y in ys)
        values = set()
        for bits in product((0, 1), repeat=D):
            value = sp.expand(host.subs(dict(zip(ys, bits))))
            expected = sp.prod(hs[i] for i, bit in enumerate(bits) if bit)
            assert sp.expand(value - expected) == 0
            values.add(str(value))
        assert len(values) == 2**D
        boolean_rows.append({"D": D, "specializations": len(values)})

    # A Laurent associate is not harmless for coefficient moments or
    # coefficientwise positivity: translation changes the first moment, and
    # the sign unit changes every coefficient sign.
    X = sp.symbols("X")
    normalized = 1 + X
    translated = sp.expand(X**3 * normalized)

    def augmentation(poly: sp.Expr) -> int:
        return int(poly.subs(X, 1))

    def first_exponent_moment(poly: sp.Expr) -> int:
        p = sp.Poly(poly, X)
        return sum(int(coef) * exponent[0] for exponent, coef in p.terms())

    assert augmentation(normalized) == augmentation(translated) == 2
    assert first_exponent_moment(normalized) == 1
    assert first_exponent_moment(translated) == 7
    assert all(coef > 0 for coef in sp.Poly(normalized, X).all_coeffs())
    assert all(coef < 0 for coef in sp.Poly(-normalized, X).all_coeffs())

    # Delta interpolation on K distinct nodes requires degree K-1 by root
    # count; construct the attaining Lagrange polynomial independently.
    T = sp.symbols("T")
    interpolation_rows = []
    for K_nodes in range(2, 10):
        nodes = list(range(K_nodes))
        numerator = sp.prod(T - node for node in nodes[:-1])
        denominator = sp.prod(nodes[-1] - node for node in nodes[:-1])
        interpolant = sp.cancel(numerator / denominator)
        assert sp.Poly(interpolant, T).degree() == K_nodes - 1
        assert [sp.simplify(interpolant.subs(T, node)) for node in nodes] == [0] * (K_nodes - 1) + [1]
        interpolation_rows.append({"K": K_nodes, "degree": K_nodes - 1})

    # Rebuild the exponent ledger from named point sets.
    K = Fraction(5, 9)
    S = Fraction(7, 9)
    U = Fraction(5, 6)
    q = Fraction(13, 18)
    sources = S
    all_targets = q + U
    selected_targets = K + U
    source_all_target = sources + all_targets
    selected_pairs = 2 * selected_targets
    selected_all_cross = selected_targets + all_targets
    all_target_pairs = 2 * all_targets
    fibre_threshold = all_target_pairs - 3
    native_untyped = K + S + U + q
    formal_two_source = K + 2*S + U + q

    assert source_all_target == Fraction(7, 3)
    assert selected_pairs == Fraction(25, 9)
    assert selected_all_cross == Fraction(53, 18)
    assert all_target_pairs == Fraction(28, 9)
    assert fibre_threshold == Fraction(1, 9)
    assert native_untyped == Fraction(26, 9) < 3
    assert formal_two_source == Fraction(11, 3)

    print(json.dumps({
        "schema": "amra.erdos1083.round3.independent-audit.v1",
        "boolean_host": {
            "checks": boolean_rows,
            "scope": "2^D distinct products requires independent formal factors; repeated actual occurrences can duplicate Boolean vectors",
            "unit_guard": {
                "augmentation_preserved": 2,
                "normalized_first_moment": 1,
                "translated_first_moment": 7,
                "sign_changes_coefficientwise_positivity": True,
            },
        },
        "interpolation": {
            "checks": interpolation_rows,
            "root_count_lower_bound": "K-1 distinct zero nodes force degree at least K-1",
            "scope": "arbitrary samples, not a realization by actual exact-block quotients",
        },
        "point_pair_ledger": {
            "source_to_all_targets": "7/3",
            "selected_target_pairs": "25/9",
            "selected_to_all_targets": "53/18",
            "all_target_pairs": "28/9",
            "required_fibre_for_3_plus_epsilon": "<1/9-epsilon",
            "inadmissible_KSUq": "26/9",
            "inadmissible_KS2Uq": "11/3 (not a point-pair domain)",
        },
        "dependency_guard": "The fibre implication also requires one actual occurrence domain of size t^(28/9-o(1)); a capacity upper bound alone is insufficient.",
        "M01_positivity_theorem_proved": False,
        "public_exponent_changed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
