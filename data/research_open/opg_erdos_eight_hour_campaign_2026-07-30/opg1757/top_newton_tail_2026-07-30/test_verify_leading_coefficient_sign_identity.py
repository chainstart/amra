from verify_leading_coefficient_sign_identity import audit


def test_symbolic_all_rank_leading_sign_identity():
    result = audit(maximum_rank=8)
    assert (
        result["status"]
        == "symbolic_all_rank_leading_sign_identity_passed"
    )
    assert result["records"][0]["signed_highest_laurent_layer"] == "2"
    assert result["records"][1]["signed_highest_laurent_layer"] == "22/3"
