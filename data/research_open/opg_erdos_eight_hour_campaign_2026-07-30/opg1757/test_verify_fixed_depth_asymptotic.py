from verify_fixed_depth_asymptotic import audit


def test_fixed_depth_asymptotic_certificate() -> None:
    result = audit(
        maximum_component_count=11,
        maximum_k=22,
        maximum_depth=3,
    )
    assert result["schema"].endswith(".v1")
    assert result["expansion_checks"] == 22
    assert result["determinant_constant_checks"] == list(range(3, 12))
    assert len(result["coefficient_checks"]) == 4
