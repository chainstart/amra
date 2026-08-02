"""Regression tests for finite-quotient shadows and aperiodic escape."""

import unittest

from verify_finite_quotient_shadow_escape import (
    aperiodic_signed_escape_certificate,
    endpoint_extension_certificate,
    finite_quotient_shadow_certificate,
    two_point_minimality_certificate,
)


class FiniteQuotientShadowEscapeTests(unittest.TestCase):
    def test_nontrivial_finite_quotient_shadow(self) -> None:
        result = finite_quotient_shadow_certificate()
        self.assertTrue(result["exact_finite_tiling"])
        self.assertTrue(result["uniform_compressed_coefficients"])
        self.assertEqual(result["shadow_mass"], result["expected_quotient_mass"])
        self.assertTrue(result["H_divides_shadow"])
        self.assertTrue(result["pass"])

    def test_aperiodic_signed_escape(self) -> None:
        result = aperiodic_signed_escape_certificate()
        self.assertEqual(result["source_terms"], 3)
        self.assertEqual(result["quotient_augmentation"], 2)
        self.assertTrue(result["signed_quotient_has_negative_coefficient"])
        self.assertTrue(result["product_is_mask"])
        self.assertEqual(result["product_terms"], 6)
        self.assertTrue(result["strict_augmentation"])
        self.assertTrue(result["no_torsion_factor_in_checked_range"])
        self.assertTrue(result["pass"])

    def test_two_point_sources_have_finite_tiling_models(self) -> None:
        result = two_point_minimality_certificate()
        self.assertEqual(len(result["records"]), 20)
        self.assertTrue(result["all_two_point_models_tile"])
        self.assertTrue(result["pass"])

    def test_finite_tile_centres_keep_the_quadratic_endpoint_gap(self) -> None:
        result = endpoint_extension_certificate()
        self.assertEqual(result["finite_tile_bound_exponent"], "1/9")
        self.assertEqual(result["gap"], "4/9")
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
