"""Tests for the all-depth rank-six ordinary symbol."""

from independent_verify_ordinary_rank_six_symbol import fast_audit


def test_rank_six_symbol_and_newton_inequality():
    result = fast_audit()
    assert result["status"] == "PASS"
    assert result["rank_six_degree"] == 18
    assert result["euler_generating_function_identity"] is True
    assert result["finite_exact_ordinary_checks"] == 7
    assert len(result["rank_six_sign_shift_coefficients"]) == 19
    assert len(result["fifth_newton_shift_coefficients"]) == 32
    assert len(result["rank_six_C3_gap_shift_coefficients"]) == 19
