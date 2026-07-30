from fractions import Fraction

from independent_verify_polynomial_top_window import audit


def test_independent_polynomial_ratio_and_repair():
    result = audit(maximum_n=160)
    assert result["imports_existing_opg_verifier"] is False
    assert result["historical_coarse_step_verdict"] == "FAIL"
    assert result["current_revision_verdict"] == "PASS"
    assert result["mathematical_verdict_after_local_repair"] == "PASS"
    assert result["pair_lower_checks"] == 3160
    assert result["star_graph_upper_checks"] == 46620
    assert result["intermediate_ratio_checks"] == 46620
    assert result["final_ratio_checks"] == 46620
    assert result["maximum_log_actual_minus_bound"] <= 0

    counterexamples = result[
        "printed_coarse_exponent_counterexamples"
    ]
    assert counterexamples == [
        {
            "d": 2,
            "printed_left_coefficient": 32,
            "target_coefficient": 24,
        },
        {
            "d": 3,
            "printed_left_coefficient": 60,
            "target_coefficient": 54,
        },
    ]
    assert result["corrected_exponent_checks"] == 32896


def test_independent_absolute_eta_quantifiers():
    records = audit(maximum_n=96)["eta_records"]
    assert len(records) == 32
    for record in records:
        assert record["1_minus_eta_A_plus_1"] == "1/2"
        assert Fraction(record["1_minus_2eta"]) > 0
