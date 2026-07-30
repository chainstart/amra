from verify_long_recurrence_leading_log_derivative import audit


def test_exact_leading_log_derivative_audit():
    result = audit(maximum_rank=40, continued_fraction_depth=8)
    assert result["status"] == "exact_leading_log_derivative_audit_passed"
    assert result["first_logarithmic_coefficients"][:3] == [
        "11/6",
        "341/432",
        "74317/186624",
    ]
    assert result["positive_logarithmic_coefficients_checked"] == 40
