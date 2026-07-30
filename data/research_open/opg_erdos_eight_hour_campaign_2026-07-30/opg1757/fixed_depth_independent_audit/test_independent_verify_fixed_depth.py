from independent_verify_fixed_depth import audit


def test_independent_fixed_depth_audit() -> None:
    result = audit()
    assert result["schema"].endswith(".v1")
    assert result["finite_product_prefix_checks"] == 30
    assert result["binomial_moments_checked_through"] == 30
    assert result["capacity_boundary_checked_through_n"] == 30
    assert len(result["equation_20_constant_checks"]) == 5
