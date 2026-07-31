from verify_dominant_zero_spectral_asymptotic import audit


def test_sharpened_dominant_zero_and_rate() -> None:
    result = audit()
    assert result["status"] == "PASS"
    assert result["dominant_zero_interval"] == [
        "1961/1000",
        "1962/1000",
    ]
    assert result["thresholds"]["relative_error_lt_1_over_100"] == 129
