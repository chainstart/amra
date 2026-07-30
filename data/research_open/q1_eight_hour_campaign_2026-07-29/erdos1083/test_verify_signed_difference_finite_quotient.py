from fractions import Fraction

import verify_signed_difference_finite_quotient as verifier


def test_exact_mod_seven_counts_and_zero_transversal_cycles() -> None:
    for height_count in (7, 14, 21):
        certificate = verifier.build_certificate(height_count)
        assert certificate["transversal_point_cycle_count"] == 0
        for edge in certificate["edge_certificates"]:
            assert edge["selected_value_count"] == 2 * height_count // 7
            assert edge["representation_count"] == 2 * height_count**2 // 7
            assert edge["average_representation_multiplicity"] == Fraction(
                height_count, 1
            )


def test_shifted_correlation_radius_pairs_are_valid() -> None:
    certificate = verifier.build_certificate(14)
    for edge in certificate["edge_certificates"]:
        assert edge["common_sum"] == sum(edge["external_pair"])
        assert edge["offset_positive"]
        assert edge["target_count"] == edge["selected_value_count"]
    assert certificate["all_external_indices_distinct"]
    assert certificate["external_indices_disjoint_from_cycle"]


def test_bad_mod_seven_colour_multisets_are_exactly_classified() -> None:
    assert verifier.bad_colour_multisets() == {
        (1, 1, 1, 2),
        (1, 3, 3, 3),
        (2, 2, 2, 3),
    }


def test_every_mod_seven_k23_has_a_liftable_cycle() -> None:
    assert verifier.all_k23_colourings_repair()
