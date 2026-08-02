"""Regression tests for the one-promotion rank-five chart."""

from verify_one_promotion_rank_five_chart import (
    EXPECTED_COUNTS,
    finite_unified_chart,
)


def test_unified_rank_five_chart() -> None:
    result = finite_unified_chart()
    assert result["pass"]
    assert result["antecedent_points"] == 219
    assert result["chamber_counts"] == EXPECTED_COUNTS
    assert result["global_minimum_gamma5"] == 4222
    assert result["global_minimum_chamber"] == "-- -> --"


def test_asymmetric_reverse_tail_is_present() -> None:
    result = finite_unified_chart()
    assert result["chamber_counts"]["-+ -> +-"] == 1
    record = result["chamber_minima"]["-+ -> +-"]
    assert record["gamma5"] == 78157
    assert record["q_K_r_b_h_g"] == [214, 4, 41, 218, 303, 2]
