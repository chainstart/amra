from verify_long_recurrence_leading_reduction import audit


def test_exact_long_recurrence_leading_search():
    result = audit(maximum_band=100)
    assert result["status"] == "NO_COUNTEREXAMPLE_FINITE_EXACT_SEARCH"
    assert result["maximum_band"] == 99
    assert result["counterexample_bands"] == []
    assert result["first_recurrence_leading_coefficients"][:3] == [
        "11/6",
        "341/432",
        "74317/186624",
    ]
