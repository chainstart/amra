import sympy as sp

from verify_ordinary_second_subleading_symbol import (
    D,
    T,
    audit,
    claimed_h4,
    determinant_functions,
    formally_summed_second_symbol,
    second_symbol,
    symbol_generating_function,
)


def test_small_exact_certificate():
    result = audit(maximum_loss=9, maximum_depth=5)
    assert result["status"] == "finite_certificate_passed"
    assert result["rank_four_profile_checks"] == 18
    assert result["ordinary_polynomial_checks"] == 4


def test_h4_identity():
    *_, actual = determinant_functions()
    assert sp.simplify(actual - claimed_h4()) == 0
    assert sp.series(actual, T, 0, 8).removeO().expand() == (
        4 * T**5 + 130 * T**6 + 676 * T**7
    )


def test_second_symbol_values_and_generating_function():
    assert [second_symbol(depth) for depth in range(2, 7)] == [
        42,
        sp.Rational(557, 2),
        sp.Rational(2527, 2),
        sp.Rational(12025, 3),
        sp.Rational(245663, 24),
    ]
    assert sp.simplify(
        formally_summed_second_symbol() - symbol_generating_function()
    ) == 0
