from verify_growing_degree_escape_search import dense_unit_polynomials
from verify_two_unit_nonrectangular_search import (
    bounded_word_independent,
    element_inverse,
    element_norm,
    field_mul,
    one_element,
    quartic_two_unit_search,
    small_second_units,
    theta_element,
)


def test_small_second_units_are_exact_units_and_bounded_word_independent():
    polynomial = dense_unit_polynomials(4, 2)[0]
    theta = theta_element(4)
    units = small_second_units(polynomial, maximum=2)
    assert units
    for unit in units:
        assert abs(element_norm(unit, polynomial)) == 1
        inverse = element_inverse(unit, polynomial)
        assert field_mul(unit, inverse, polynomial) == one_element(4)
        assert bounded_word_independent(theta, unit, polynomial, radius=6)


def test_exact_two_unit_search_has_fixed_finite_scope_and_misses_target():
    result = quartic_two_unit_search(
        coefficient_bound=2,
        units_per_field=1,
        word_radius=1,
    )
    assert result["accepted_fields"] == 122
    assert result["searched_fields"] > 0
    assert result["unit_pairs"] == result["searched_fields"]
    assert result["rank_two_subsets"] > 0
    best = result["overall_best_target"]
    assert best["target_ratio_float"] < 1
    assert best["distinct_curve_points"] >= 4
    assert best["target_ratio_float"] >= best["rectangular_target_ratio"]


def test_nonrectangular_search_really_checks_elementary_shears():
    result = quartic_two_unit_search(
        coefficient_bound=2,
        units_per_field=1,
        word_radius=1,
    )
    best = result["overall_best_target"]
    assert best["shear"] is None or len(best["shear"]) == 3
