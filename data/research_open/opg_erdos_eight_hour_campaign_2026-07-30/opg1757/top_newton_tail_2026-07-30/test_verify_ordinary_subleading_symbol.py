from verify_ordinary_subleading_symbol import audit


def test_ordinary_subleading_symbol():
    result = audit(maximum_loss=12, maximum_depth=10)
    assert result["status"] == "finite_checks_passed"
    assert result["profile_checks"] == 138
    assert result["ordinary_polynomial_checks"] == 10
    assert result["rows"][-1]["subleading"] == "-1057"
