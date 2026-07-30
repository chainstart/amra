from verify_ordinary_real_rootedness import audit


def test_small_exact_real_rootedness_audit():
    result = audit(maximum_depth=8, interval_decimal_digits=8)
    assert result["status"] == "finite_exact_certificate_passed"
    assert result["positive_simple_root_rows"] == 8
    assert result["positive_simple_poisson_root_rows"] == 8
    assert result["strict_residual_interlacing_pairs"] == 7
    assert result["strict_poisson_interlacing_pairs"] == 7
    assert result["favard_three_term_obstruction"] == {
        "first_failed_depth": 3,
        "alpha": "167/3",
        "beta": "13963/6",
        "nonzero_residual": "-41889*(k - 2)",
    }
