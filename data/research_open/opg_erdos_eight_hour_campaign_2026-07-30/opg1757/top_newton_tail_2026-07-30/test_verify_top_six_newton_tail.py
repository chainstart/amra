from verify_top_six_newton_tail import audit


def test_top_six_newton_tail():
    result = audit(maximum_regression_k=10)
    # For each drop d=0,...,9 we check 3 values of h and
    # 2d+3 interpolation points in the edge parameter:
    # 3 * sum_{d=0}^9 (2d+3) = 360.
    assert result["profile_identity_checks"] == 360
    assert len(result["normalized_newton_tail"]) == 6
    assert len(result["regression_rows"]) == 9
