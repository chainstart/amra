from verify_determinant_second_order import audit


def test_determinant_second_order() -> None:
    result = audit(maximum_total=18)
    assert result["schema"].endswith(".v1")
    assert len(result["constant_checks"]) == 16
