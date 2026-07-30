from independent_verify_top_nine import audit


def test_independent_top_nine_exact_polynomials():
    result = audit(spare_points=4)
    assert result["imports_existing_opg_verifier"] is False
    assert result["maximum_profile_loss"] == 12

    records = result["depth_records"]
    assert records["6"]["degree"] == 12
    assert records["7"]["degree"] == 14
    assert records["8"]["degree"] == 16
    assert records["6"]["leading_coefficient"] == "4/45"
    assert records["7"]["leading_coefficient"] == "8/315"
    assert records["8"]["leading_coefficient"] == "2/315"

    assert records["6"]["factorization"] == (
        "(k - 5)*(k - 4)*(k - 3)*(k - 2)*"
        "(4032*k**8 - 24192*k**7 + 9072*k**6 - 319760*k**5 "
        "- 296716*k**4 + 3115760*k**3 + 29380477*k**2 "
        "+ 103674567*k + 153772290)/45360"
    )
    assert records["7"]["factorization"] == (
        "(k - 6)*(k - 5)*(k - 4)*(k - 3)*(k - 2)*"
        "(576*k**9 - 4608*k**8 + 9744*k**7 - 75488*k**6 "
        "- 66724*k**5 + 254944*k**4 + 6661499*k**3 "
        "+ 37990606*k**2 + 117200435*k + 160178004)/22680"
    )
    assert records["8"]["factorization"] == (
        "(k - 6)*(k - 5)*(k - 4)*(k - 3)*(k - 2)*"
        "(34560*k**11 - 599040*k**10 + 3893760*k**9 "
        "- 17736960*k**8 + 55219360*k**7 - 15634240*k**6 "
        "+ 657272176*k**5 + 682878800*k**4 - 9060987065*k**3 "
        "- 88234978600*k**2 - 335731520391*k "
        "- 533577731400)/5443200"
    )


def test_independent_top_nine_active_positivity():
    records = audit(spare_points=4)["depth_records"]
    expected = {
        "6": {
            "boundary": [5, 0],
            "first_positive": [6, 31104],
            "positive_from": 6,
        },
        "7": {
            "boundary": [6, 0],
            "first_positive": [7, 2331720],
            "positive_from": 7,
        },
        "8": {
            "boundary": [6, 0],
            "first_positive": [7, 155520],
            "positive_from": 7,
        },
    }
    for depth, values in expected.items():
        positivity = records[depth]["positivity"]
        assert positivity["boundary_zero"] == values["boundary"]
        assert positivity["first_positive"] == values["first_positive"]
        assert (
            positivity["positive_for_all_k_at_least"]
            == values["positive_from"]
        )
        assert all(
            coefficient > 0
            for coefficient
            in positivity["residual_shifted_coefficients_ascending"]
        )
        assert len(records[depth]["spare_values"]) == 4
