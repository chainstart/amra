from verify_ordinary_rank_eight_and_eighth_band import audit


def test_rank_eight_and_eighth_band_certificate():
    result = audit()
    assert result["status"] == "PASS"
    assert result["rank_eight"]["interpolation_depths"] == list(
        range(8, 33)
    )
    assert result["rank_eight"]["holdout_depths"] == list(
        range(33, 37)
    )
    assert len(
        result["rank_eight"]["seventh_normalized_newton"][
            "shifted_reduced_numerator_coefficients"
        ]
    ) == 44
    assert len(
        result["rank_eight"]["rank_eight_C3_bound"][
            "shifted_reduced_numerator_coefficients"
        ]
    ) == 25
    assert result["eighth_band"]["band"] == 7
    assert result["eighth_band"]["minimum_depth"] == 15
    assert result["eighth_band"]["degree"] == 23
    assert result["eighth_band"]["forced_factor"] == "d-14"
    assert result["eighth_band"][
        "all_shifted_coefficients_positive"
    ]
