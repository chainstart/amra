import audit_general_k_beta4_component_independent as audit


def test_component_tree_weight_small_cases() -> None:
    assert audit.component_tree_weight(0, 1, 1) == 1
    assert audit.component_tree_weight(1, 0, 1) == 2
    assert audit.component_tree_weight(0, 2, 2) == 4
    assert audit.component_tree_weight(1, 1, 2) == 12


def test_component_recurrence_small_polynomials() -> None:
    # K_{1,2}: 1 + 2 beta + beta^2.
    assert audit.bipartite_forest_coefficients(0, 1, 2, 2) == (1, 2, 1)
    # Weighted K_{1,2} with core weight two.
    assert audit.bipartite_forest_coefficients(1, 0, 2, 2) == (1, 4, 4)


def test_general_beta4_formula_by_independent_components() -> None:
    assert all(row["match"] for row in audit.audit_rows())
