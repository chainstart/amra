from verify_ordinary_rank_seven_and_seventh_band import audit


def test_rank_seven_and_seventh_band_certificate():
    result = audit()
    assert result["status"] == "PASS"
    assert result["rank_seven"]["interpolation_depths"] == list(
        range(7, 29)
    )
    assert result["rank_seven"]["holdout_depths"] == list(
        range(29, 33)
    )
    assert len(
        result["rank_seven"]["sixth_normalized_newton"][
            "shifted_reduced_numerator_coefficients"
        ]
    ) == 38
    assert len(
        result["rank_seven"]["rank_seven_C3_bound"][
            "shifted_reduced_numerator_coefficients"
        ]
    ) == 22
    assert result["seventh_band"]["band"] == 6
    assert result["seventh_band"]["minimum_depth"] == 13
    assert result["seventh_band"]["degree"] == 20
    assert (
        result["seventh_band"][
            "all_shifted_coefficients_positive"
        ]
        is True
    )
    assert result["seventh_band"]["forced_factor"] == "d-12"
