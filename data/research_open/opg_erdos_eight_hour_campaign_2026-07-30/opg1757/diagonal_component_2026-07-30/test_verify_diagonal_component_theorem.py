from verify_diagonal_component_theorem import audit


def test_all_orders_diagonal_component_audit():
    result = audit(maximum_degree=7)
    assert result["maximum_checked_order"] == 7
    assert result["component_polynomial_checks"] == 24
    assert result["uniform_growing_depth_positivity"] == "open_gap"
