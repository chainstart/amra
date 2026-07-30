import itertools

from verify_triangle_k4_compatibility import (
    all_triangle_equations,
    k4_identity,
    line_embedding_exists,
    obstruction_certificate,
    squared_six_tuple,
    support_certificate,
    triangle_polynomial,
    triangle_saturation,
)


def test_triangle_parameterization_and_saturation() -> None:
    for size in range(1, 20):
        assert triangle_saturation(size) == size * size
    for first in range(-10, 11):
        for second in range(-10, 11):
            assert triangle_polynomial(
                first * first,
                second * second,
                (first + second) ** 2,
            ) == 0


def test_minimum_k4_sign_obstruction() -> None:
    certificate = obstruction_certificate()
    assert certificate.all_triangle_equations_hold
    assert certificate.gram_entries == (-1, 2, 2)
    assert certificate.gram_product == -4
    assert certificate.required_product == 4
    assert not certificate.k4_identity_holds
    assert not certificate.line_embedding_exists


def test_k4_identity_on_integer_points() -> None:
    examples = (
        (0, 1, 2, 3),
        (-10, -2, 7, 30),
        (5, 5, 9, 100),
    )
    for points in examples:
        values = squared_six_tuple(points)
        squares = dict(
            zip(
                ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)),
                values,
            )
        )
        left, right = k4_identity(squares)
        assert left == right


def test_triangle_plus_k4_identity_is_sufficient_positive_small() -> None:
    edges = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    for values in itertools.product(range(1, 5), repeat=6):
        lengths = dict(zip(edges, values))
        squares = {edge: value * value for edge, value in lengths.items()}
        left, right = k4_identity(squares)
        if all_triangle_equations(squares) and left == right:
            assert line_embedding_exists(lengths)


def test_k4_support_bounds_and_cubic_scale() -> None:
    for size in range(1, 12):
        certificate = support_certificate(size)
        assert certificate.all_k4_identities_hold
        assert certificate.compatible_six_tuples >= certificate.lower_bound
        assert certificate.compatible_six_tuples <= (
            certificate.cubic_upper_bound
        )
