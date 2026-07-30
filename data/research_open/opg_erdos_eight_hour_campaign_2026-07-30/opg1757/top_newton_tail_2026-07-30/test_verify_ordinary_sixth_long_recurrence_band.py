from verify_ordinary_sixth_long_recurrence_band import audit


def test_sixth_long_recurrence_band():
    result = audit()
    assert result["status"] == "PASS"
    assert result["band"] == 5
    assert result["minimum_depth"] == 11
    assert result["degree"] == 17
    assert len(result["shifted_numerator_coefficients"]) == 18
    assert min(result["shifted_numerator_coefficients"]) > 0
