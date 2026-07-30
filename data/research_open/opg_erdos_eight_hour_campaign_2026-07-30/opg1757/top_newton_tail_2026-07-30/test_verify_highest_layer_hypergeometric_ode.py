from verify_highest_layer_hypergeometric_ode import audit


def test_highest_layer_hypergeometric_ode():
    result = audit(maximum_band=40)
    assert result["status"] == "PASS"
    assert result["exact_differential_elimination"] is True
    assert result["maximum_redundant_sign_band"] == 39
    assert result["long_leading_counterexamples"] == []
    assert result["first_B_coefficients"][:3] == [
        "2",
        "22/3",
        "715/9",
    ]
