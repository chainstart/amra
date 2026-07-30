#!/usr/bin/env python3
"""Independent coefficient audit of ORDINARY_TOP_SYMBOL_THEOREM.md.

This module imports no existing OPG verifier or recorded profile symbol.
"""

from __future__ import annotations

import json
import math

import sympy as sp


S, J, K, X = sp.symbols("s j k x")


def falling(value, degree):
    if degree < 0:
        return sp.S.Zero
    return sp.prod(value-index for index in range(degree))


def lagrange_e(s, parameter, degree):
    if degree < 0:
        return sp.S.Zero
    return sp.expand(sum(
        sp.Rational((-1)**index, 2**index)
        * falling(parameter, index)*s**(degree-index)
        / (math.factorial(index)*math.factorial(degree-index))
        for index in range(degree+1)
    ))


def source_profile(h, edge_count):
    if h == 0:
        return sp.expand(
            falling(S, edge_count)
            * (
                lagrange_e(S, S-edge_count, edge_count)
                - lagrange_e(S, S-edge_count, edge_count-1)
            )
        )
    if h == 1:
        return sp.expand(
            falling(S-2, edge_count)
            * (
                lagrange_e(S, S-2-edge_count, edge_count)
                - lagrange_e(S, S-2-edge_count, edge_count-1)
            )
        )
    assert h == 2
    return sp.expand(
        falling(S-4, edge_count)
        * (
            lagrange_e(S, S-4-edge_count, edge_count)
            - lagrange_e(S, S-4-edge_count, edge_count-1)
        )
        + 4*falling(S-4, edge_count-1)
        * lagrange_e(S, S-3-edge_count, edge_count-1)
    )


def profile_symbol(loss, h):
    values = []
    for edge_count in range(2*loss+3):
        polynomial = sp.Poly(source_profile(h, edge_count), S)
        power = 2*edge_count-loss
        coefficient = (
            sp.S.Zero if power < 0
            else polynomial.coeff_monomial(S**power)
        )
        values.append(sp.factor(
            coefficient*2**edge_count*math.factorial(edge_count)
        ))
    result = sp.interpolate(
        [(edge_count, values[edge_count])
         for edge_count in range(loss+1)],
        J,
    ).expand()
    assert sp.degree(result, J) <= loss
    for edge_count in range(loss+1, 2*loss+3):
        assert sp.expand(result.subs(J, edge_count)-values[edge_count]) == 0
    return sp.factor(result)


def build_symbols(maximum_loss):
    return {
        loss: {h: profile_symbol(loss, h) for h in range(3)}
        for loss in range(maximum_loss+1)
    }


def extract_abc(symbols):
    a, b, c = {}, {}, {}
    for loss, profiles in symbols.items():
        a[loss] = sp.Poly(profiles[0], J).coeff_monomial(J**loss)
        b[loss] = (
            sp.S.Zero if loss < 1
            else sp.Poly(profiles[1]-profiles[0], J)
            .coeff_monomial(J**(loss-1))
        )
        c[loss] = (
            sp.S.Zero if loss < 2
            else sp.Rational(1, 2)
            * sp.Poly(profiles[2]-2*profiles[1]+profiles[0], J)
            .coeff_monomial(J**(loss-2))
        )
    return a, b, c


def abc_audit(maximum_loss=10):
    symbols = build_symbols(maximum_loss)
    a, b, c = extract_abc(symbols)
    expected_a = sp.series(
        sp.sqrt(1-2*X), X, 0, maximum_loss+1
    ).removeO().expand()
    expected_b = sp.series(
        -2*X/sp.sqrt(1-2*X), X, 0, maximum_loss
    ).removeO().expand()
    expected_c = sp.series(
        -2*X**2/(1-2*X)**sp.Rational(3, 2),
        X,
        0,
        maximum_loss-1,
    ).removeO().expand()
    for loss in range(maximum_loss+1):
        assert a[loss] == expected_a.coeff(X, loss)
        assert b[loss] == (
            0 if loss < 1 else expected_b.coeff(X, loss-1)
        )
        assert c[loss] == (
            0 if loss < 2 else expected_c.coeff(X, loss-2)
        )
        # The missing coefficientwise second-difference expansion:
        expected_recurrence = (
            0 if loss < 2
            else 2*(loss-2)*(loss-3)*a.get(loss-2, 0)
        )
        assert c[loss] == expected_recurrence
    return symbols, a, b, c


def homogeneous_total(expression, degree):
    polynomial = sp.Poly(sp.expand(expression), J, K)
    return sp.expand(sum(
        coefficient*J**powers[0]*K**powers[1]
        for powers, coefficient in polynomial.terms()
        if sum(powers) == degree
    ))


def binomial_expectation(expression):
    result = sp.S.Zero
    for (power,), coefficient in sp.Poly(sp.expand(expression), J).terms():
        for degree in range(power+1):
            result += (
                coefficient
                * sp.functions.combinatorial.numbers.stirling(
                    power, degree, kind=2
                )
                * falling(K, degree)/2**degree
            )
    return sp.factor(result)


def determinant_audit(maximum_loss=8):
    symbols, a, b, c = abc_audit(maximum_loss)
    records = []
    for loss in range(4, maximum_loss+1):
        kernel = sp.expand(sum(
            symbols[left][1]
            * symbols[loss-left][1].subs(J, K-J)
            - symbols[left][0]
            * symbols[loss-left][2].subs(J, K-J)
            for left in range(loss+1)
        ))
        assert sp.Poly(kernel, J, K).total_degree() <= loss-1
        degree_l_minus_1 = homogeneous_total(kernel, loss-1)
        assert sp.expand(
            degree_l_minus_1
            + degree_l_minus_1.xreplace({J: K-J})
        ) == 0

        actual_symmetric = homogeneous_total(kernel, loss-2)
        actual_symmetric = sp.expand(
            (
                actual_symmetric
                + actual_symmetric.xreplace({J: K-J})
            ) / 2
        )
        expected_symmetric = sp.S.Zero
        for left in range(loss+1):
            right = loss-left
            if left >= 1 and right >= 1:
                expected_symmetric += (
                    b[left]*b[right]
                    * J**(left-1)*(K-J)**(right-1)
                )
            if right >= 2:
                expected_symmetric -= (
                    2*a[left]*c[right]
                    * J**left*(K-J)**(right-2)
                )
        expected_symmetric = sp.expand(
            (
                expected_symmetric
                + expected_symmetric.xreplace({J: K-J})
            ) / 2
        )
        assert sp.expand(actual_symmetric-expected_symmetric) == 0

        expectation = binomial_expectation(kernel)
        assert sp.degree(expectation, K) == loss-2
        assert sp.Poly(expectation, K).LC() == 2
        ordinary = sp.cancel(expectation/(2*K*(K-1)))
        assert sp.degree(ordinary, K) == loss-4
        assert sp.Poly(ordinary, K).LC() == 1

        center_symbol = sum(
            b[left]*b[loss-left]
            - 2*a[left]*c[loss-left]
            for left in range(loss+1)
        )
        assert sp.simplify(
            center_symbol/2**(loss-2)-2
        ) == 0
        records.append((loss, str(sp.factor(ordinary))))
    return records


def audit():
    symbols, a, b, c = abc_audit(10)
    determinant = determinant_audit(8)
    return {
        "schema": "amra.opg1757.independent-ordinary-top-symbol.v1",
        "verdict_as_written": "PASS",
        "formula_verdict": "PASS",
        "reason": (
            "Equations (23a)-(23c) supply the all-orders coefficientwise "
            "second-difference extraction, and equations (26a)-(27) give "
            "the complete degree-(L-2) determinant ledger with the "
            "correct separate BB and AC moments."
        ),
        "maximum_abc_loss": max(symbols),
        "maximum_determinant_loss": determinant[-1][0],
        "C_coefficient_identity": (
            "C_l=2*(l-2)*(l-3)*A_(l-2)"
        ),
        "determinant_leading_numerator": 2,
        "ordinary_leading_coefficient": 1,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
