from fractions import Fraction

import verify_cross_fibre_endpoint_reuse as verifier


def test_triangle_polynomial_and_preimage_bound() -> None:
    certificate = verifier.build_certificate(14)
    assert certificate["all_value_triples_compatible"]
    assert certificate["point_triple_count"] == 14**3
    assert certificate["maximum_point_preimage"] <= 4 * 14
    assert (
        certificate["distinct_value_triple_count"]
        >= certificate["theorem_lower_bound"]
    )


def test_mod_seven_selection_erases_all_triangle_tests() -> None:
    certificate = verifier.build_certificate(14)
    assert certificate["selected_mod_seven_value_count"] == 4
    assert certificate["selected_mod_seven_edge_count"] == 56
    assert certificate["selected_mod_seven_triangle_count"] == 0
    assert certificate["selected_mod_seven_value_triangle_count"] == 0


def test_retention_exponent_ledger() -> None:
    eta = Fraction(1, 30)
    delta = Fraction(1, 100)
    ledger = verifier.exponent_ledger(1, 30, 1, 100)
    assert ledger["large_block_count"] == 2 - delta
    assert ledger["bad_radius_triangles"] == 3 - delta
    assert ledger["retained_compatible_tests"] == (
        3 - 3 * eta - 3 * delta
    )
    assert (
        ledger["retained_compatible_tests"]
        == ledger["retained_tests_expected"]
    )
    assert ledger["test_degree_per_incidence"] == (
        -3 * eta - 3 * delta
    )


def test_triangle_polynomial_rejects_generic_incompatible_values() -> None:
    incompatible = [(1, 1, 1), (1, 4, 2), (2, 3, 7), (5, 6, 8)]
    assert all(
        not verifier.triangle_polynomial(triple)
        for triple in incompatible
    )
