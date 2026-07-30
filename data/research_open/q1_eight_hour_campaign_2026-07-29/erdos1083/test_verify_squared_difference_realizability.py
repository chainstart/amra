from fractions import Fraction

from verify_squared_difference_realizability import (
    hadamard_realization,
    triangle_certificate,
    two_point_realization,
    symbolic_squared_differences,
)


def test_every_positive_two_value_set_examples() -> None:
    for first, second in ((1, 2), (1, 5), (7, 30), (190, 195), (984, 987)):
        left, right = two_point_realization(first, second)
        assert symbolic_squared_differences(left, right) == {first, second}


def test_exact_hadamard_realization() -> None:
    certificate = hadamard_realization()
    assert certificate.product_exponent == 5
    assert certificate.radial_offsets == (961, 196, 16)
    assert certificate.pair_intersections == (1, 1, 1)
    assert certificate.pair_symmetric_differences == (2, 2, 2)
    assert certificate.union_size == 4
    assert certificate.all_two_point_realizations_exact


def test_triangle_compatibility_and_support_bound() -> None:
    examples = (
        ((0, 1, 4), (0, 2, 9), (1, 5, 12)),
        ((0, 3, 6, 9),) * 3,
        ((-10, -2, 7), (-4, 0, 11, 20), (1, 2, 3, 8, 30)),
    )
    for example in examples:
        certificate = triangle_certificate(*example)
        assert certificate.all_values_satisfy_polynomial
        lower_bound = Fraction(
            certificate.support_lower_bound_numerator,
            certificate.support_lower_bound_denominator,
        )
        assert certificate.compatible_value_triples >= lower_bound
        if len(set(certificate.sizes)) == 1:
            size = certificate.sizes[0]
            assert certificate.compatible_value_triples >= Fraction(
                size * size,
                4,
            )
