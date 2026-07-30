from verify_growing_degree_escape_search import (
    dense_unit_polynomials,
    exhaustive_cubic_quartic_search,
    field_mul,
    growing_degree_search,
    one_element,
    parameter_shifts,
    sparse_unit_polynomials,
    theta_element,
    theta_inverse,
)


def test_unit_inverse_and_defining_relation_are_exact():
    for degree in range(3, 9):
        polynomial = sparse_unit_polynomials(degree)[0]
        theta = theta_element(degree)
        inverse = theta_inverse(polynomial)
        assert field_mul(theta, inverse, polynomial) == one_element(degree)

        # Evaluate f(theta) using exact quotient-ring arithmetic.
        value = (0,) * degree
        power = one_element(degree)
        for coefficient in polynomial:
            value = tuple(
                left + coefficient * right
                for left, right in zip(value, power)
            )
            power = field_mul(power, theta, polynomial)
        assert value == (0,) * degree


def test_sparse_search_fields_are_linearly_disjoint_from_qy():
    expected_counts = {3: 20, 4: 16, 5: 16, 6: 16, 7: 20, 8: 16}
    assert {
        degree: len(sparse_unit_polynomials(degree))
        for degree in expected_counts
    } == expected_counts


def test_parameter_shifts_are_integral_in_the_half_power_basis():
    polynomial = sparse_unit_polynomials(3)[0]
    for exponent in range(-5, 6):
        u, c = parameter_shifts(exponent, polynomial)
        assert all(isinstance(value, int) for value in u + c)


def test_degree_three_to_eight_search_is_exact_and_below_target():
    result = growing_degree_search(exponent_radius=2)
    assert result["total_polynomials"] == 104
    assert result["total_subsets"] == 104 * 31
    for summary in result["degree_summary"].values():
        best = summary["best"]
        assert summary["best_target"]["target_ratio_float"] < 1
        assert best["distinct_curve_points"] >= 1


def test_dense_cubic_quartic_model_has_exact_bounded_scope():
    assert len(dense_unit_polynomials(3, 2)) == 36
    assert len(dense_unit_polynomials(4, 2)) == 122
    result = exhaustive_cubic_quartic_search(
        coefficient_bound=2, exponent_radius=1
    )
    assert result["total_polynomials"] == 158
    assert result["total_subsets"] == 158 * 7
    assert result["overall_best_target"]["target_ratio_float"] < 1
