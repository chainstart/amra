"""Independent tests for the cyclotomic tensor escape theorem."""

from fractions import Fraction

from independent_verify_cyclotomic_tensor_escape import (
    audit,
    degree_disjointness_sufficient,
    direct_coordinate_fibre_audit,
    numerical_consistency_audit,
    real_basis_label,
    real_cyclotomic_boundary_collisions,
    relation_space_dimension,
    selected_label_vectors,
)


def test_real_basis_vectors_cover_last_chord_index_correctly():
    # For p=7, b_3=-1-b_1-b_2 and a_3=3+b_1+b_2.
    vector = real_basis_label(7, Fraction(2), 3, Fraction(48, 5))
    assert vector == (Fraction(78, 5), Fraction(2), Fraction(2))


def test_exact_injectivity_for_radius_dependent_height_squares():
    for prime, fibres in (
        (
            7,
            (
                (Fraction(1), (Fraction(0), Fraction(2), Fraction(5, 3))),
                (Fraction(2), (Fraction(0), Fraction(1, 7))),
                (Fraction(5, 3), (Fraction(0), Fraction(3), Fraction(19, 4))),
            ),
        ),
        (
            11,
            (
                (Fraction(1, 2), (Fraction(0), Fraction(4, 3))),
                (Fraction(4, 3), (Fraction(0), Fraction(7, 5), Fraction(9))),
            ),
        ),
        (
            13,
            (
                (Fraction(2), (Fraction(0),)),
                (Fraction(7, 3), (Fraction(0), Fraction(11, 4))),
                (Fraction(11, 4), (Fraction(0), Fraction(5, 2), Fraction(13))),
            ),
        ),
    ):
        vectors = selected_label_vectors(prime, fibres)
        assert len(vectors) == ((prime - 1) // 2) * sum(
            len(squares) for _, squares in fibres
        )


def test_numerical_distances_match_distinct_exact_vectors():
    result = numerical_consistency_audit(
        7,
        (
            (Fraction(1), (Fraction(0), Fraction(7, 4), Fraction(13, 6))),
            (Fraction(7, 4), (Fraction(0), Fraction(2))),
            (Fraction(13, 6), (Fraction(0), Fraction(1, 3), Fraction(8))),
        ),
    )
    assert result["labels"] == 3 * (3 + 2 + 3)
    assert result["labels"] == result["expected_labels"]
    assert float(result["minimum_numerical_gap"]) > 0


def test_actual_radius_dependent_non_ap_height_coordinates():
    fibres = (
        (Fraction(1), (Fraction(0), Fraction(1, 2), Fraction(7, 3))),
        (Fraction(3, 2), (Fraction(0), Fraction(2), Fraction(5))),
        (Fraction(11, 5), (Fraction(0), Fraction(1, 7))),
    )
    result = direct_coordinate_fibre_audit(
        7, fibres, ("-sqrt(2)", "pi/7", "-5/3")
    )
    assert result["height_counts"] == [3, 3, 2]
    assert result["selected_coordinate_distances"] == 3 * 8
    assert (
        result["selected_coordinate_distances"]
        == result["expected_selected_distances"]
    )
    assert float(result["maximum_formula_error"]) < 1e-90


def test_relation_space_dimension_and_exact_disjoint_boundary():
    # q=1 gives the unique all-ones relation.
    assert relation_space_dimension(13, 1) == 1
    # q=2 or q=6 creates additional F-linear relations.
    assert relation_space_dimension(13, 2) == 4
    assert relation_space_dimension(13, 6) == 6
    assert relation_space_dimension(11, 5) == 5


def test_degree_only_sufficient_condition():
    assert degree_disjointness_sufficient(3, 11)
    assert not degree_disjointness_sufficient(5, 11)
    assert not degree_disjointness_sufficient(3, 13)
    assert degree_disjointness_sufficient(5, 13)


def test_real_cyclotomic_field_has_symmetric_product_collisions():
    for prime in (7, 11, 13):
        result = real_cyclotomic_boundary_collisions(prime)
        degree = (prime - 1) // 2
        assert result["ordered_selected_inputs"] == degree**2
        assert result["distinct_formal_product_labels"] == degree * (
            degree + 1
        ) // 2
        assert result["distinct_formal_product_labels"] < degree**2


def test_invalid_quantifiers_are_rejected():
    try:
        real_basis_label(7, Fraction(0), 1, Fraction(0))
    except ValueError:
        pass
    else:
        raise AssertionError("zero radius square was accepted")

    try:
        real_basis_label(7, Fraction(1), 1, Fraction(-1))
    except ValueError:
        pass
    else:
        raise AssertionError("negative anchored height square was accepted")


def test_full_independent_audit():
    result = audit()
    assert result["verdict"] == "PASS"
    assert not result["author_verifier_imported"]
    assert len(result["finite_rational_checks"]) == 3
    assert result["direct_radius_dependent_coordinate_check"][
        "height_counts"
    ] == [3, 3, 2]
