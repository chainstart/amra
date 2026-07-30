"""Independent tests for partial prime-cyclotomic fibre escape."""

from fractions import Fraction

from independent_verify_partial_cyclotomic_fibre_escape import (
    audit,
    cauchy_davenport_audit,
    composite_algebraic_injection_collision,
    difference_set,
    equal_size_linear_constant_audit,
    exhaustive_prime_difference_audit,
    nonzero_sign_classes,
    partial_fibre_audit,
    smallest_composite_cyclic_counterexample,
)


def test_difference_direction_and_unoriented_quotient():
    anchor = frozenset({1, 4})
    target = frozenset({0, 2, 7})
    difference = difference_set(11, target, anchor)
    assert difference == frozenset({1, 3, 6, 7, 9, 10})
    classes = nonzero_sign_classes(11, difference)
    assert classes == frozenset({1, 2, 3, 4, 5})


def test_cauchy_davenport_rounding_with_and_without_zero():
    with_zero = cauchy_davenport_audit(
        7, frozenset({0, 1, 3}), frozenset({0, 1, 3})
    )
    assert with_zero["difference_size"] >= 5
    assert with_zero["sign_classes"] >= 2
    without_zero = cauchy_davenport_audit(
        7, frozenset({0, 2}), frozenset({1, 4})
    )
    assert 0 not in difference_set(
        7, frozenset({0, 2}), frozenset({1, 4})
    )
    assert without_zero["sign_classes"] >= without_zero["quotient_bound"]


def test_exhaustive_prime_7_subset_pairs():
    result = exhaustive_prime_difference_audit(7)
    assert result["ordered_nonempty_subset_pairs"] == 127**2
    assert result["minimum_quotient_slack"] >= 0


def test_cross_radius_and_height_selected_label_injection():
    fibres = (
        (
            Fraction(1),
            (
                (Fraction(0), frozenset({0, 1, 4})),
                (Fraction(1, 3), frozenset({2, 5})),
                (Fraction(8), frozenset({0, 3, 6, 9})),
            ),
        ),
        (
            Fraction(7, 4),
            (
                (Fraction(0), frozenset({1, 7})),
                (Fraction(2, 5), frozenset({0, 2, 4, 8, 10})),
            ),
        ),
    )
    result = partial_fibre_audit(11, fibres)
    assert result["selected_distances"] == result["sum_sign_classes"]
    assert result["layers"] == 5


def test_equal_size_constant_and_endpoint_rounding():
    for prime in (7, 11, 13):
        for size in range(2, (prime + 1) // 2 + 1):
            result = equal_size_linear_constant_audit(prime, size)
            assert result["unoriented_bound"] == size - 1
            assert result["distance_per_point_constant"] == str(
                Fraction(size - 1, size)
            )


def test_general_cyclic_extension_is_false():
    result = smallest_composite_cyclic_counterexample()
    assert result == {
        "modulus": 8,
        "subgroup_size": 4,
        "angular_set": [0, 2, 4, 6],
        "distinct_chord_distances": 2,
        "false_prime_analogue_bound": 3,
    }
    collision = composite_algebraic_injection_collision()
    assert collision["common_squared_distance"] == "2"


def test_full_independent_audit():
    result = audit()
    assert result["verdict"] == "PASS"
    assert not result["author_verifier_imported"]
    assert result["smallest_composite_counterexample"]["modulus"] == 8
