from verify_first_active_newton_theorem import audit


def test_first_active_newton_theorem() -> None:
    result = audit(maximum_n=11, maximum_k=16)
    assert result["schema"].endswith(".v1")
    assert result["component_checks"] == 8 * 3 * 3
    assert len(result["coefficient_checks"]) == 15
    assert all(
        row["first_coefficient"] > 0
        for row in result["coefficient_checks"]
    )
    assert all(
        row["second_coefficient"] > 0
        for row in result["coefficient_checks"][1:]
    )
