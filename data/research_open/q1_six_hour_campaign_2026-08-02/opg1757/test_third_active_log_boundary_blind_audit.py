"""Regression test for the independent OPG blind-audit guards."""

from verify_third_active_log_boundary_blind_audit import run_all


def test_independent_log_boundary_and_obstruction_guards():
    result = run_all()
    assert result["retained_shifts"]["shift_rows"] > 1000
    assert result["retained_shifts"]["high_endpoint_rows"] > 0
    assert result["logarithmic_budget"]["p6_rational_slope"] > 30
    assert result["logarithmic_budget"]["p7_rational_slope"] > 36
    assert result["splices"]["splice_rows"] > 1000
    assert result["fixed_layer"]["first_witness"] == -1152
    assert result["pass"]
