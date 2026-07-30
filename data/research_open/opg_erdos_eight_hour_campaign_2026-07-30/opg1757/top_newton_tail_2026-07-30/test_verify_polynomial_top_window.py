from verify_polynomial_top_window import audit


def test_polynomial_top_window():
    result = audit(maximum_n=96)
    assert result["status"] == "finite_checks_passed"
    assert result["ratio_checks"] > 9_000
    assert result["ratio_checks"] == result["intermediate_exact_checks"]
    assert result["maximum_actual_over_bound"] <= 1
