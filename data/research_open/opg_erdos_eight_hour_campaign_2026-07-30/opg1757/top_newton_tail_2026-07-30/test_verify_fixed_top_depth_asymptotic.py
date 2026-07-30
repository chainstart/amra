from verify_fixed_top_depth_asymptotic import audit


def test_fixed_top_depth_asymptotic():
    result = audit(maximum_profile_loss=12, maximum_abstract_depth=64)
    assert result["profile_checks"] == 39
    assert result["abstract_depth"] == 64
    assert len(result["abstract_leading_constants"]) == 65
    assert len(result["exact_tail"]) == 6
    assert result["exact_tail"][-1] == {
        "depth": 5,
        "degree": 10,
        "leading_constant": "4/15",
    }
