"""Regression tests for the endpoint Følner counterexample."""

import unittest

from verify_approximate_transverse_counterexample import (
    bounded_transverse_cycle_certificate,
    coherent_cycle_classification_certificate,
    coherent_theta_amplification_certificate,
    defect_transition_trichotomy_certificate,
    directional_partition,
    directional_partition_general,
    diagonal_boundary_sharpness_certificate,
    difference_multiplicity_repair_certificate,
    endpoint_exponent_certificate,
    finite_partition_suite,
    fixed_tangent_transverse_rigidity_certificate,
    geometric_interface_certificate,
    optimized_tangent_disjointness_certificate,
    legacy_fixed_difference_projection_certificate,
    many_bounded_cycles_certificate,
    primitive_direction_tradeoff_certificate,
    path_energy_multiplicity_red_team_certificate,
    shared_endpoint_path_energy_certificate,
    tangent_transversality_dichotomy_certificate,
    transverse_nonzero_difference_certificate,
    transverse_certificate,
)


class ApproximateTransverseCounterexampleTests(unittest.TestCase):
    def test_endpoint_exponents(self) -> None:
        self.assertTrue(endpoint_exponent_certificate()["pass"])

    def test_pairwise_transverse_directions(self) -> None:
        result = transverse_certificate(100)
        self.assertTrue(result["all_pairwise_transverse"])
        self.assertEqual(result["minimum_abs_determinant"], 1)

    def test_directional_partition_is_direct(self) -> None:
        result = directional_partition(length=20, segment_size=4, r=5)
        self.assertTrue(result["representation_injective"])
        self.assertEqual(result["base_count"], 100)
        self.assertEqual(result["spectrum_size"], 400)
        self.assertEqual(
            result["symmetric_difference"],
            result["expected_symmetric_difference"],
        )

    def test_finite_partition_suite(self) -> None:
        result = finite_partition_suite()
        self.assertEqual(result["case_count"], 15)
        self.assertTrue(result["pass"])

    def test_general_primitive_direction(self) -> None:
        result = directional_partition_general(
            length=30, segment_size=5, p=2, q=3
        )
        self.assertEqual(result["line_count"], (2 + 3) * 30 - 2 * 3)
        self.assertTrue(result["representation_injective"])
        self.assertEqual(result["base_count"], 180)

    def test_primitive_direction_tradeoff(self) -> None:
        result = primitive_direction_tradeoff_certificate()
        self.assertTrue(result["direction_count_lower_bound"])
        self.assertTrue(result["all_pairwise_transverse"])
        self.assertTrue(result["uniform_error_bound_holds"])
        self.assertTrue(result["pass"])

    def test_diagonal_boundary_scale_is_exact(self) -> None:
        result = diagonal_boundary_sharpness_certificate()
        self.assertEqual(result["exact_boundary_scale"], "2(S-1)/L")
        self.assertTrue(result["pass"])

    def test_tangent_transversality_dichotomy(self) -> None:
        result = tangent_transversality_dichotomy_certificate()
        self.assertTrue(result["split_exact"])
        self.assertTrue(result["cs_bound_holds"])
        self.assertTrue(result["one_branch_reaches_half_cs_mass"])
        self.assertTrue(result["fixed_row_tangent_star_bound_holds"])
        self.assertTrue(result["pass"])

    def test_optimized_tangent_sets_are_disjoint(self) -> None:
        result = optimized_tangent_disjointness_certificate()
        self.assertTrue(result["separation_condition"])
        self.assertTrue(result["all_pairwise_disjoint"])
        self.assertEqual(result["union_size"], result["expected_union_size"])
        self.assertTrue(result["all_tangents_positive"])
        self.assertTrue(result["pass"])

    def test_fixed_tangent_transverse_rigidity_is_sharp(self) -> None:
        result = fixed_tangent_transverse_rigidity_certificate()
        self.assertTrue(result["spaces_pairwise_transverse"])
        self.assertEqual(result["intersection_size"], 1)
        self.assertTrue(result["sharp_constant_one"])
        self.assertTrue(result["packing_bound_holds"])
        self.assertTrue(result["pass"])

    def test_legacy_fixed_difference_projection_is_not_injective(self) -> None:
        result = legacy_fixed_difference_projection_certificate()
        self.assertTrue(result["minimal_collision_matches_document"])
        self.assertTrue(result["legacy_projection_injectivity_refuted"])
        self.assertEqual(result["dimension_six_maximum_multiplicity"], 16)
        self.assertTrue(result["pass"])

    def test_global_difference_multiplicity_repairs_the_bound(self) -> None:
        result = difference_multiplicity_repair_certificate()
        self.assertTrue(result["ordered_signed_difference_convention"])
        self.assertTrue(result["zero_difference_included"])
        self.assertEqual(result["dimension_count"], 4)
        for dimension in result["dimensions"]:
            self.assertTrue(dimension["weighted_identity_every_difference"])
            self.assertTrue(
                dimension["mu_bounded_by_global_difference_everywhere"]
            )
            self.assertEqual(
                dimension["zero_difference_global_multiplicity"],
                dimension["expected_zero_difference_global_multiplicity"],
            )
            self.assertTrue(dimension["sigma_mu_bounded_by_R2"])
            self.assertTrue(dimension["parameterized_bound_holds"])
            self.assertTrue(dimension["R2_bound_holds"])
        self.assertTrue(result["pass"])

    def test_transverse_nonzero_difference_compression(self) -> None:
        result = transverse_nonzero_difference_certificate()
        self.assertEqual(
            result["nonzero_global_difference_mass"],
            result["expected_nonzero_global_difference_mass"],
        )
        self.assertTrue(result["theorem_bound_holds"])
        self.assertEqual(result["fixed_nonzero_edge_exponent"], "8/9")
        self.assertEqual(result["fixed_nonzero_star_degree_exponent"], "1/6")
        self.assertTrue(result["pass"])

    def test_bounded_transverse_cycle_ledger(self) -> None:
        result = bounded_transverse_cycle_certificate()
        self.assertEqual(result["cycle_length_bound"], 10)
        self.assertEqual(result["average_degree_exponent"], "1/6")
        self.assertEqual(result["moore_margin"], "1/9")
        self.assertTrue(result["quadratic_terms_telescope"])
        self.assertTrue(result["noncoherent_coefficients_not_all_zero"])
        self.assertTrue(result["coherent_arithmetic_walk_closes"])
        self.assertTrue(result["pass"])

    def test_coherent_cycle_classification_and_strict_model(self) -> None:
        result = coherent_cycle_classification_certificate()
        self.assertEqual(result["total_raw_balanced_words"], 348)
        self.assertEqual(result["total_cycle_symmetry_orbits"], 36)
        self.assertEqual(result["maximum_normalized_level_count"], 6)
        self.assertEqual(
            {
                length: data["orbit_count"]
                for length, data in result["lengths"].items()
            },
            {4: 2, 6: 4, 8: 9, 10: 21},
        )
        model = result["strict_local_four_cycle_model"]
        self.assertEqual(model["traversal_sign_word"], "++--")
        self.assertTrue(model["adjacent_row_spaces_transverse"])
        self.assertTrue(model["every_edge_label_matches"])
        self.assertTrue(model["pass"])
        self.assertTrue(result["pass"])

    def test_many_bounded_cycles_exponent_ledger(self) -> None:
        result = many_bounded_cycles_certificate()
        self.assertEqual(result["high_girth_residual_exponent"], "13/15")
        self.assertEqual(result["high_girth_residual_gap"], "1/45")
        self.assertEqual(result["edge_disjoint_cycle_exponent"], "8/9")
        self.assertEqual(result["coherent_sign_orbit_count"], 36)
        self.assertTrue(result["residual_is_power_smaller"])
        self.assertTrue(result["pass"])

    def test_shared_endpoint_path_energy(self) -> None:
        result = shared_endpoint_path_energy_certificate()
        self.assertEqual(result["shared_endpoint_path_exponent"], "16/9")
        self.assertEqual(result["endpoint_label_pair_exponent"], "14/9")
        self.assertEqual(
            result["fixed_endpoint_label_and_sign_bundle_exponent"],
            "2/9",
        )
        self.assertEqual(result["orientation_sum_type_count"], 16)
        self.assertEqual(result["homogeneous_relation_support_bound"], 28)
        self.assertEqual(result["synthetic_coherent_defects"], ["0", "0"])
        self.assertEqual(result["synthetic_defective_defects"], ["4", "-3"])
        self.assertEqual(result["synthetic_homogeneous_relation_value"], "0")
        self.assertTrue(result["synthetic_relation_nontrivial"])
        self.assertTrue(result["pass"])

    def test_coherent_theta_amplification(self) -> None:
        result = coherent_theta_amplification_certificate()
        self.assertEqual(
            result["initial_shared_endpoint_path_exponent"],
            "227/18",
        )
        self.assertEqual(
            result["fixed_endpoint_labels_and_word_exponent"],
            "199/18",
        )
        self.assertEqual(result["midpoint_lengths"], [80, 40, 20, 10, 5])
        self.assertEqual(
            result["midpoint_family_exponents"],
            ["199/18", "31/6", "20/9", "3/4", "1/72"],
        )
        self.assertEqual(result["theta_or_hub_exponent"], "1/144")
        self.assertEqual(result["relation_support_bound"], 158)
        self.assertEqual(result["finite_theta_pair_cycle_lengths"], [10, 10, 10])
        self.assertTrue(result["finite_theta_arm_interiors_disjoint"])
        self.assertTrue(result["finite_theta_pair_cycles_simple"])
        self.assertTrue(result["pass"])

    def test_path_energy_multiplicity_red_team(self) -> None:
        result = path_energy_multiplicity_red_team_certificate()
        self.assertEqual(
            result["length_fifteen_fixed_label_bundle_exponent"],
            "2/9",
        )
        self.assertEqual(
            result["length_eighty_fixed_label_bundle_exponent"],
            "199/18",
        )
        self.assertEqual(result["length_five_exponent"], "1/72")
        self.assertEqual(result["hub_or_packing_exponent"], "1/144")
        self.assertEqual(result["complete_orientation_word_count"], 2**80)
        self.assertTrue(result["midpoint_fibre_is_rows_not_row_source_pairs"])
        self.assertTrue(result["individual_paths_are_simple"])
        self.assertTrue(result["common_defect_support_is_internal_only"])
        self.assertTrue(
            result["ordered_half_path_pair_determines_at_most_one_full_path"]
        )
        self.assertTrue(result["pass"])

    def test_defect_transition_trichotomy(self) -> None:
        result = defect_transition_trichotomy_certificate()
        self.assertTrue(result["nonzero_transition_pairing_lemma_holds"])
        self.assertEqual(result["relation_support_bound"], 158)
        self.assertEqual(result["noncoherent_cycle_length_bound"], 160)
        self.assertEqual(result["common_defect_support_internal_row_bound"], 79)
        self.assertEqual(result["minimum_checkpoint_exponent"], "2201/20160")
        self.assertEqual(result["minimum_checkpoint_length"], 79)
        self.assertEqual(result["minimum_checkpoint_segment_count"], 14)
        self.assertTrue(result["minimum_exceeds_one_tenth"])
        self.assertEqual(result["theta_or_hub_exponent"], "1/20")
        self.assertTrue(result["aligned_spine_is_nonzero"])
        self.assertTrue(result["aligned_detours_are_coherent"])
        self.assertTrue(result["pass"])

    def test_geometric_interface(self) -> None:
        result = geometric_interface_certificate()
        self.assertTrue(result["one_common_spectrum_used_for_every_row"])
        self.assertEqual(
            result["common_spectrum_size"],
            result["expected_common_spectrum_size"],
        )
        self.assertTrue(result["pairwise_nonaligned"])
        self.assertTrue(result["tangent_union_within_cap"])
        self.assertTrue(
            all(row["source_sines_distinct"] for row in result["rows"])
        )
        self.assertTrue(
            all(row["all_spectrum_values_positive"] for row in result["rows"])
        )
        self.assertTrue(
            all(
                row["relative_to_SU_equals_relative_to_V"]
                for row in result["rows"]
            )
        )
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
