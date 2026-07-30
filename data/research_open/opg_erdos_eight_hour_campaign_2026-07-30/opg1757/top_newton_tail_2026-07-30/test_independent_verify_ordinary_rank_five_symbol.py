"""Tests for the all-depth rank-five ordinary symbol."""

from independent_verify_ordinary_rank_five_symbol import fast_audit


def test_rank_five_symbol_and_newton_inequality():
    result = fast_audit()
    assert result["status"] == "PASS"
    assert result["rank_five_degree"] == 15
    assert result["euler_generating_function_identity"] is True
    assert result["finite_exact_ordinary_checks"] == 8
    assert len(result["rank_five_sign_shift_coefficients"]) == 16
    assert len(result["fourth_newton_shift_coefficients"]) == 26
    assert len(result["rank_five_C3_gap_shift_coefficients"]) == 16
