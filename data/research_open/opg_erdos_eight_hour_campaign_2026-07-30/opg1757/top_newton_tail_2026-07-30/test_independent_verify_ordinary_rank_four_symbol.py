"""Tests for the all-depth rank-four ordinary symbol."""

from independent_verify_ordinary_rank_four_symbol import fast_audit


def test_rank_four_symbol_and_newton_inequality():
    result = fast_audit()
    assert result["status"] == "PASS"
    assert result["rank_four_degree"] == 12
    assert result["euler_generating_function_identity"] is True
    assert result["finite_exact_ordinary_checks"] == 9
    assert len(result["rank_four_shift_coefficients"]) == 13
    assert len(result["third_newton_shift_coefficients"]) == 20
    assert len(result["rank_four_C3_gap_shift_coefficients"]) == 13
