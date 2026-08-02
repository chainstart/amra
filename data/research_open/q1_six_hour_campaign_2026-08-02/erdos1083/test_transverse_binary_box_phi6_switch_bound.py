"""Regression tests for the signed transverse binary-box switch bound."""

import unittest

from verify_transverse_binary_box_phi6_switch_bound import (
    endpoint_entropy_certificate,
    newton_zonotope_certificate,
    pairwise_hamming_certificate,
    quotient_tiling_certificate,
    shadow_factor_preservation_certificate,
    symbolic_pair_and_sharpness_certificate,
)


class TransverseBinaryBoxPhi6SwitchBoundTests(unittest.TestCase):
    def test_separating_finite_quotient_tiles(self) -> None:
        result = quotient_tiling_certificate()
        self.assertEqual(len(result["records"]), 16)
        self.assertGreater(result["total_group_elements_checked"], 6000)
        for record in result["records"]:
            self.assertEqual(
                record["centre_image_size"], 2 ** record["rank"]
            )
            self.assertTrue(record["all_coefficients_one"])
            self.assertTrue(record["pass"])
        self.assertTrue(result["pass"])

    def test_shadow_keeps_external_phi6_factor_and_exact_mass(self) -> None:
        result = shadow_factor_preservation_certificate()
        self.assertTrue(result["profiles_uniform"])
        self.assertEqual(result["shadow_mass"], result["expected_mass"])
        self.assertTrue(result["original_quotient_is_signed"])
        self.assertTrue(result["positive_product_identity"])
        self.assertTrue(result["phi6_divides_shadow"])
        self.assertTrue(result["pass"])

    def test_sharp_newton_zonotope_models(self) -> None:
        result = newton_zonotope_certificate()
        for record in result["records"]:
            self.assertEqual(record["mass"], 2 ** record["rank"])
            self.assertEqual(record["support_size"], 2 ** record["rank"])
            self.assertTrue(record["support_is_parallelotope_vertices"])
            self.assertTrue(record["all_coefficients_one"])
        self.assertTrue(result["pass"])

    def test_pairwise_one_sided_hamming_bounds(self) -> None:
        result = pairwise_hamming_certificate()
        self.assertEqual(result["one_sided_bound"], 3)
        self.assertTrue(result["all_one_sided_bounds_hold"])
        self.assertTrue(result["family_below_ball_bound"])
        self.assertTrue(result["pass"])

    def test_symbolic_pair_cancellation_and_sharp_models(self) -> None:
        result = symbolic_pair_and_sharpness_certificate()
        self.assertEqual(result["ordered_pairs_checked"], 256)
        self.assertTrue(result["all_pair_factorizations_and_coprimality"])
        for record in result["sharp_records"]:
            self.assertEqual(record["C"], 2 ** record["d"])
            self.assertTrue(record["common_products_equal"])
            self.assertTrue(record["all_complements_are_masks"])
            self.assertTrue(record["strict_exactly_before_uniform_endpoint"])
            self.assertTrue(record["pass"])
        self.assertTrue(result["pass"])

    def test_exact_endpoint_entropy_gap(self) -> None:
        result = endpoint_entropy_certificate()
        self.assertTrue(result["radius_is_k_over_7"])
        self.assertAlmostEqual(result["entropy"], 0.5916727785823273)
        self.assertAlmostEqual(result["t_exponent"], 0.46018993889736565)
        self.assertGreater(result["exponent_margin"], 0.095)
        self.assertTrue(result["exact_ball_below_entropy_bound"])
        self.assertTrue(result["uniform_endpoint_forces_C_at_least_S"])
        self.assertTrue(result["strict_block_contradiction"])
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
